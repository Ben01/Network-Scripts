import time, os, re, logging
import multiconnect, hosts

logging.basicConfig(filename=r'.\logs\backup log {}.txt'.format(time.strftime('%Y-%m-%d')), level=logging.INFO, format='%(asctime)s:%(levelname)s:%(module)s:%(message)s')
logger = logging.getLogger(__name__)

@multiconnect.hookToConnection
def updateACL(connection, hostProfile):
    def sortAcl(acl):
        out = []
        for line in acl:
            m = re.match(r'^\s*(\d+) ((?:permit|deny)[^()\n\r]+)', line)
            if m:
                out.append((int(m.group(1)), ' '.join(m.group(2).split())))
        return sorted(out)
    
    cfgSet = [
        'no ip access-list standard MANAGMENT',
        'ip access-list standard MANAGMENT',
        '10 permit 192.168.245.254',
        '20 permit 10.200.75.20',
        '30 permit 10.28.7.75',
        '40 deny any']
    
    if sortAcl(cfgSet) != sortAcl(connection.send_command('sh ip access-l MANAGMENT').splitlines()):    
        connection.config_mode()
        connection.send_config_set(cfgSet)
        connection.exit_config_mode()
    
    return {'success': sortAcl(cfgSet) == sortAcl(connection.send_command('sh ip access-l MANAGMENT').splitlines()),
            'description': 'update managment acl'}

@multiconnect.hookToConnection
def updateLineVty(connection, hostProfile):
    lineCfg = connection.send_command('show run | begin line vty')
    cfgSet = []
    for lineGroup in re.finditer(r'^line vty (\d+ \d+)((?:.(?<!^[^\s]))*)', lineCfg):
        m = re.search(r'access-class[^\r\n]+', lineGroup.group())
        if m and m.group() != 'access-class MANAGMENT in':
            cfgSet.append('line vty {}'.format(lineGroup.group(1)))
            cfgSet.append('no {}'.format(m.group()))
            cfgSet.append('access-class MANAGMENT in')
        elif not m:
            cfgSet.append('line vty {}'.format(lineGroup.group(1)))
            cfgSet.append('access-class MANAGMENT in')
            
    if cfgSet:
        connection.config_mode()
        connection.send_config_set(cfgSet)
        connection.exit_config_mode()
        
    return {'success': True,
            'description': 'configure line with access-class'}

multiconnect.run(hosts.getHosts())
