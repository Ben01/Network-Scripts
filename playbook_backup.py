import time, os, re, logging
import multiconnect, hosts

logging.basicConfig(filename=r'.\logs\backup log {}.txt'.format(time.strftime('%Y-%m-%d')), level=logging.INFO, format='%(asctime)s:%(levelname)s:%(module)s:%(message)s')
logger = logging.getLogger(__name__)

@multiconnect.hookToConnection
def showRun(connection, hostProfile):
    commands = [
        'show run', 'show interface', 'show ip interface', 'show vrf detail', 'sh run vrf', 'show version', 'show inventory', 'show cdp neighbors detail',
        'show ip access-list', 'show ip route connected', 'show standby brief', 'show arp', 'show logging', 'show debug']
    return {'results': '\n'.join(('{}\n{}\n'.format(cmd, connection.send_command(cmd).strip()) for cmd in commands)), 'resultMsg': 'backup successful'}

@multiconnect.hookToOutput
def saveResults(hostProfile):
    savePath = r'.\temp\{} {}.txt'.format(hostProfile['hostname'], time.strftime('%Y-%m-%d'))
    os.makedirs(os.path.dirname(savePath), exist_ok=True)
    with open(savePath, 'w') as fh:
        fh.write('Hostname: {hostname}\nIP: {ip}\nRun Time: {runTime:.2f}\n\n'.format(**hostProfile))
        fh.write(hostProfile['results'])
    return dict()

multiconnect.run(hosts.getHosts())
