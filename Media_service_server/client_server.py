import socket

from twisted.internet.protocol import Factory
from twisted.internet import reactor, protocol

def processing(in_str):
    in_str_decoded = in_str.decode()
    if in_str_decoded == 'stop':
        print('should stop')
        return 'ssss'
    elif in_str_decoded == 'continue':
        print('should continue')
        return 'continue'
    elif in_str_decoded == 'test':
        print('should test')
        return 'test'
    else:
        return 'kokoloko'

    pass
class ServeProtocol(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.numConnections += 1
        self.sendConnectionMade()

    def sendConnectionMade(self):
        self.transport.write((socket.gethostname()).encode())

    def dataReceived(self, data):
        print ("Number of active connections: %d" % (self.factory.numConnections,))
        # print ("> Received: ``%s''\n> Sending: ``%s''" % (data, self.getQuote()))
        self.responding = processing(data).encode()
        if self.responding == 1:
            print('')
        # processing(data)
        # self.transport.write(self.getQuote())
        self.transport.write(self.responding)
        print ("> Received: ``%s''\n> Sending: ``%s''" % (data, self.responding))

        self.updateQuote(data)
        print(self.transport.getHost())
        print(self.transport.getPeer())

    def connectionLost(self, reason):
        self.factory.numConnections -= 1

    def getQuote(self):
        return self.factory.quote

    def updateQuote(self, quote):
        self.factory.quote = quote


class ServeFactory(Factory):
    numConnections = 0

    def __init__(self, quote=None):
        self.quote = quote or "An apple a day keeps the doctor away".encode()

    def buildProtocol(self, addr):
        return ServeProtocol(self)


reactor.listenTCP(8000, ServeFactory())
reactor.run()