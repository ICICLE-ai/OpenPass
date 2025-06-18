#!/usr/bin/python3

import dns.resolver

def getIpAddress(service_name):
    with open('/etc/resolv.kube', 'r') as f:
        kubedns = str(f.read()).strip()
    res = dns.resolver.Resolver(configure=False)
    res.nameservers = [ kubedns ]
    r = res.resolve(f"{service_name}.default.svc.cluster.local")
    ipaddr = str(r[0])

    return ipaddr