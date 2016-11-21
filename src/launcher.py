from tornado.ioloop import IOLoop
from tornado.netutil import Resolver, OverrideResolver
from tornado.simple_httpclient import SimpleAsyncHTTPClient
from tornado.httpclient import HTTPRequest
from tornado import gen

request = HTTPRequest('http://www.baidu.com', validate_cert=False)

reslover = OverrideResolver(Resolver(),
                            mapping={"www.baidu.com": "111.13.101.208"})

client = SimpleAsyncHTTPClient(resolver=reslover)


@gen.coroutine
def get_response():
    xxx = yield reslover.resolve('www.baidu.com', 80)
    print xxx
    rs = yield client.fetch(request)
    print rs.body


IOLoop.current().run_sync(get_response)
