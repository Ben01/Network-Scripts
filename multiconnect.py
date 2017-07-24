import netmiko, time, logging
from multiprocessing.dummy import Pool

def connectionHandler(host):
    cStartTime = time.time()
    with netmiko.ConnectHandler(**{k:v for k,v in host.items() if k in {'ip', 'device_type', 'username', 'password', 'secret'}}) as c:
        c.enable()
        for action in connectionActions:
            host.update(action(c, host))
        host['runTime'] = time.time() - cStartTime
        return host

def outputHandler(host):
    for action in outputActions:
        host.update(action(host))
    return host

connectionActions = []
def hookToConnection(f):
    connectionActions.append(f)

outputActions = []
def hookToOutput(f):
    outputActions.append(f)

def run(hostProfiles):
    with Pool(3) as threadPool:
        for result in [threadPool.apply_async(connectionHandler, (h,)) for h in hostProfiles]:
            try:
                host = outputHandler(result.get())
                print('{} {:.2f}'.format(host['hostname'], host['runTime']))
                if host['results']:
                    print(' Success: {}'.format(host['resultMsg']))
                else:
                    print(' Failed: {}'.format(host['resultMsg']))
            except Exception as e:
                logging.exception('host failed with exception')
                print('Exception: {}'.format(e))
