#! /usr/bin/python

def getHosts(hostFilter=lambda x: True, hostSort=lambda x: 1):
    hosts = [
        {   'hostname': 'R1',
            'ip': '192.168.245.1',
            'device_type': 'cisco_ios_ssh',
            'commands': 'IOS_ROUTER',
            'credential': 'GNS3',},
        {   'hostname': 'R2',
            'ip': '192.168.245.2',
            'device_type': 'cisco_ios_ssh',
            'commands': 'IOS_ROUTER',
            'credential': 'GNS3',},
        {   'hostname': 'R3',
            'ip': '192.168.245.3',
            'device_type': 'cisco_ios_ssh',
            'commands': 'IOS_ROUTER',
            'credential': 'GNS3',},
        {   'hostname': 'R4',
            'ip': '192.168.245.4',
            'device_type': 'cisco_ios_ssh',
            'commands': 'IOS_ROUTER',
            'credential': 'GNS3',},
        {   'hostname': 'R5',
            'ip': '192.168.245.5',
            'device_type': 'cisco_ios_ssh',
            'commands': 'IOS_ROUTER',
            'credential': 'GNS3',},
        {   'hostname': 'R6',
            'ip': '192.168.245.6',
            'device_type': 'cisco_ios_ssh',
            'commands': 'IOS_ROUTER',
            'credential': 'GNS3',},

    ]
    secrets = {
            'GNS3':          {'username': 'lsharon', 'password': 'tiny'},
        }
        
    for host in filter(hostFilter, sorted(hosts, key=hostSort)):
        host.update(secrets[host['credential']])
        yield host
