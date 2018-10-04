import json

from twisted.internet import reactor
from twisted.python import log
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
from twisted.web.server import Site


from txrtpengine.NGCP import NGCPClient


class NGCPProxy(Resource):
    def __init__(self, addr):
        self.c = NGCPClient(addr)
        self.isLeaf = True
        Resource.__init__(self)

    def _onResponse(self, response, request):
        request.write(json.dumps(response).encode('utf-8'))
        request.finish()

    def _onError(self, error, request):
        request.write(json.dumps({'error': str(error)}).encode('utf-8'))
        request.finish()

    def render_POST(self, request):
        request.setHeader('Content-Type', 'application/json; charset=utf-8')

        # copy-paste from https://stackoverflow.com/a/33571117
        def _byteify(data, ignore_dicts=False):
            # if this is a unicode string, return its string representation
            if isinstance(data, unicode):
                return data.encode('utf-8')
            # if this is a list of values, return list of byteified values
            if isinstance(data, list):
                return [_byteify(item, ignore_dicts=True) for item in data]
            # if this is a dictionary, return dictionary of byteified keys and values
            # but only if we haven't already byteified it
            if isinstance(data, dict) and not ignore_dicts:
                return {
                    _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
                    for key, value in data.iteritems()
                }
            # if it's anything else, return it in its original form
            return data

        try:
            content = request.content.read().decode("utf-8")
            cmd = json.loads(content, object_hook=_byteify)

            d = self.c.command(cmd)
            d.addCallback(self._onResponse, request)
            d.addErrback(self._onError, request)

            return NOT_DONE_YET
        except Exception as e:
            return json.dumps({'error': str(e)}, ensure_ascii=False, indent=1).encode('utf-8')


if __name__ == '__main__':
    import sys
    from twisted.web.client import getPage
    log.startLogging(sys.stdout)


    def test():
        reactor.listenTCP(1222, Site(NGCPProxy(('127.0.0.1', 16222))))

        def onResponse(data):
            log.msg("response: %s" % data)

        getPage('http://localhost:1222/', method='POST', postdata='{"command":"ping"}').addBoth(onResponse)


    reactor.callWhenRunning(test)
    reactor.run()
