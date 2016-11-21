import time
import random
from netaddr import *
from tornado import gen
from tornado.httpclient import HTTPRequest
from tornado.ioloop import IOLoop
from tornado.netutil import Resolver, OverrideResolver
from tornado.simple_httpclient import SimpleAsyncHTTPClient

with open(r'./all_good_ip.txt') as f:
    text = f.read()

good_ips = text.split('\n')
for i in good_ips:
    i.replace('\n', '')
# print len(ips)


subnet = [
    "64.18.0.0/20",
    "64.233.160.0/19",
    "66.102.0.0/20",
    "66.249.80.0/20",
    "72.14.192.0/18",
    "74.125.0.0/16",
    "108.177.8.0/21",
    "173.194.0.0/16",
    "207.126.144.0/20",
    "209.85.128.0/17",
    "216.58.192.0/19",
    "216.239.32.0/19"
]
all_ip = []
for n in subnet:
    ip = IPNetwork(n)
    for l in list(ip):
        all_ip.append(str(l))

print len(all_ip)

ips = random.sample(all_ip, 20000)


@gen.coroutine
def do_test(ips):
    print len(ips)
    rss = []
    rs = []
    old = 0
    ips = list(set(ips))
    for i, item in enumerate(ips):
        resolver = OverrideResolver(
            Resolver(),
            mapping={
                'clarkhillgo1.appspot.com': item.replace('\n', '')
            })

        request = HTTPRequest('https://clarkhillgo1.appspot.com',
                              validate_cert=False)
        client = SimpleAsyncHTTPClient(resolver=resolver, force_instance=True)
        rs.append((client.fetch(request), item, client))

    while len(rs) > 0:
        if old != len(rs):
            print time.time(), len(rs)
            old = len(rs)
        for f in rs:
            if f[0].done():
                rs = [_ for _ in rs if _ != f]
                if f[0].exception():
                    f[2].close()
                    # print 'exception: ', f[0].exception()
                else:
                    body = f[0].result().body
                    if 'GoAgent' in body:
                        print body, f[1]
                        rss.append(f[1])
                    f[2].close()
        yield gen.sleep(0.5)
    if rss:
        with open('./all_good_ip.txt', 'a') as f:
            for r in rss:
                f.writelines(r + '\n')


@gen.coroutine
def main():
    # yield do_test(good_ips)
    while True:
        yield do_test(random.sample(all_ip, 500))
        yield gen.sleep(1)


IOLoop.current().run_sync(main)
