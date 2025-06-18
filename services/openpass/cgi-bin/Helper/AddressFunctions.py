import dns.resolver

def getPodAddress(pod):
    with open('/etc/resolv.kube', 'r') as f:
        kubedns = str(f.read()).strip()
    res = dns.resolver.Resolver(configure=False)
    res.nameservers = [ kubedns ]
    r = res.resolve(f"{pod}.default.svc.cluster.local")
    ipaddr = str(r[0])

    return ipaddr