import better_bencode as bencode
from twisted.internet import defer
from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol
from twisted.python import log


class NGControlProtocol(DatagramProtocol):
    cookies = {}
    cache = []
    count = 0

    def __init__(self, addr):
        self.addr = addr

    def gencookie(self):
        self.count += 1
        return '%s_%s' % (id(self), self.count)

    def send(self, data):
        self.transport.write(data)
        log.msg('Sent %r to %s' % (data, self.addr))

    def command(self, cmd):
        c = self.gencookie()
        df = defer.Deferred()
        self.cookies[c] = df

        msg = c + ' ' + bencode.dumps(cmd)

        if self.transport:
            self.send(msg)
        else:
            log.msg('Not ready, will be sent later')
            self.cache.append(msg)
        return df

    def startProtocol(self):
        self.transport.connect(*self.addr)
        for msg in self.cache:
            self.send(msg)

    def datagramReceived(self, data, addr):
        log.msg("Received %r from %s" % (data, addr))
        cookie, res = data.split(' ', 1)
        msg = bencode.loads(res)
        df = self.cookies.pop(cookie)
        if df:
            df.callback(msg)
        else:
            log.err("Unknown cookie: %s" % cookie)

    def ping(self):
        cmd = {"command": "ping"}
        return self.command(cmd)

    def offer(self, sdp, callid, fromtag, viabranch=None, flags=[], replace=["origin", "session connection"],
              direction=None, receivedfrom=None, ice=None, transportprotocol=None, mediaaddress=None,
              addressfamily=None, tos=None, rtcpmux=None, dtls=None, sdes=None, recordcall=None, metadata=None,
              codec={}, ptime=None, supports=None):
        cmd = {'command': 'offer',
               'call-id': callid,
               'from-tag': fromtag,
               'sdp': sdp
               }
        if viabranch:
            cmd['via-branch'] = viabranch
        if flags:
            cmd['flags'] = flags
        if replace:
            cmd['replace'] = replace
        if ice:
            cmd['ICE'] = ice
        if transportprotocol:
            cmd['transport protocol'] = transportprotocol
        if rtcpmux:
            cmd['rtcp-mux'] = rtcpmux
        if dtls:
            cmd['DTLS'] = dtls
        if sdes:
            cmd['SDES'] = sdes
        if codec:
            cmd['codec'] = codec
        if direction:
            cmd['direction'] = direction
        if receivedfrom:
            cmd['received from'] = receivedfrom
        if mediaaddress:
            cmd['media address'] = mediaaddress
        if addressfamily:
            cmd['address family'] = addressfamily
        if tos:
            cmd['tos'] = tos
        if recordcall:
            cmd['record call'] = recordcall
        if metadata:
            cmd['metadata'] = metadata
        if ptime:
            cmd['ptime'] = ptime
        if supports:
            cmd['supports'] = supports
        return self.command(cmd)

    def answer(self, sdp, callid, fromtag, totag, viabranch=None, flags=[], replace=["origin", "session connection"],
               direction=None, receivedfrom=None, ice=None, transportprotocol=None, mediaaddress=None,
               addressfamily=None, tos=None, rtcpmux=None, dtls=None, sdes=None, recordcall=None, metadata=None,
               codec={}, ptime=None, supports=None):
        cmd = {'command': 'answer',
               'call-id': callid,
               'from-tag': fromtag,
               'to-tag': totag,
               'sdp': sdp
               }
        if viabranch:
            cmd['via-branch'] = viabranch
        if flags:
            cmd['flags'] = flags
        if replace:
            cmd['replace'] = replace
        if ice:
            cmd['ICE'] = ice
        if transportprotocol:
            cmd['transport protocol'] = transportprotocol
        if rtcpmux:
            cmd['rtcp-mux'] = rtcpmux
        if dtls:
            cmd['DTLS'] = dtls
        if sdes:
            cmd['SDES'] = sdes
        if codec:
            cmd['codec'] = codec
        if direction:
            cmd['direction'] = direction
        if receivedfrom:
            cmd['received from'] = receivedfrom
        if mediaaddress:
            cmd['media address'] = mediaaddress
        if addressfamily:
            cmd['address family'] = addressfamily
        if tos:
            cmd['tos'] = tos
        if recordcall:
            cmd['record call'] = recordcall
        if metadata:
            cmd['metadata'] = metadata
        if ptime:
            cmd['ptime'] = ptime
        if supports:
            cmd['supports'] = supports
        return self.command(cmd)

    def delete(self, callid, fromtag, totag=None, viabranch=None, flags=[], deletedelay=None):
        cmd = {'command': 'delete',
               'call-id': callid,
               'from-tag': fromtag,
               }
        if totag:
            cmd['to-tag'] = totag
        if viabranch:
            cmd['via-branch'] = viabranch
        if flags:
            cmd['flags'] = flags
        if deletedelay:
            cmd['delete delay'] = deletedelay

        return self.command(cmd)

    def list(self, limit=None):
        cmd = {'command': 'list'}
        if limit:
            cmd['limit'] = limit
        return self.command(cmd)

    def query(self, callid, fromtag=None, totag=None):
        cmd = {'command': 'query',
               'call-id': callid}
        if fromtag:
            cmd['from-tag'] = fromtag
        if totag:
            cmd['to-tag'] = totag
        return self.command(cmd)

    def startrecording(self, callid, fromtag=None, totag=None, viabranch=None):
        cmd = {'command': 'start recording',
               'call-id': callid}
        if fromtag:
            cmd['from-tag'] = fromtag
        if totag:
            cmd['to-tag'] = totag
        if viabranch:
            cmd['via-branch'] = viabranch
        return self.command(cmd)

    def stoprecording(self, callid, fromtag=None, totag=None, viabranch=None):
        cmd = {'command': 'stop recording',
               'call-id': callid}
        if fromtag:
            cmd['from-tag'] = fromtag
        if totag:
            cmd['to-tag'] = totag
        if viabranch:
            cmd['via-branch'] = viabranch
        return self.command(cmd)

    def blockdtmf(self, callid):
        cmd = {'command': 'block DTMF',
               'call-id': callid}
        return self.command(cmd)

    def unblockdtmf(self, callid):
        cmd = {'command': 'unblock DTMF',
               'call-id': callid}
        return self.command(cmd)

    def blockmedia(self, callid):
        cmd = {'command': 'block media',
               'call-id': callid}
        return self.command(cmd)

    def unblockmedia(self, callid):
        cmd = {'command': 'unblock media',
               'call-id': callid}
        return self.command(cmd)


class NGCPClient(NGControlProtocol):
    def __init__(self, addr):
        NGControlProtocol.__init__(self, addr)
        reactor.listenUDP(0, self)


if __name__ == '__main__':
    import sys

    log.startLogging(sys.stdout)


    def test():
        c = NGCPClient(('127.0.0.1', 16222))

        def onResponse(data):
            log.msg("response: %s" % data)

        c.ping().addBoth(onResponse)


    reactor.callWhenRunning(test)
    reactor.run()
