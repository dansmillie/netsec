import asyncio
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import INT, BOOL
from playground.network.common import StackingProtocol, StackingTransport, StackingProtocolFactory
import playground
import sys

class PlaneClient(asyncio.Protocol):
    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        print("client connected")
        self.transport = transport
        self._deserializer = PacketType.Deserializer()
        self.transport.write(RequestPlanePacket().__serialize__())

    def data_received(self, data):
        self._deserializer.update(data)
        for p in self._deserializer.nextPackets():
            if (isinstance(p, PlanePacket)):
                point = PointPacket()
                point.x = 0
                point.y = 0
                point.z = 0
                self.transport.write(point.__serialize__())
            elif (isinstance(p, ResultPacket)):
                if p.result:
                    print("I picked a point on the plane!")
                else:
                    print("I didn't pick a point on the plane")
            else:
                self.transport.close()

    def connection_lost(self, exc):
        self.transport = None

class PassThroughLayerOne(StackingProtocol):

    def connection_made(self, transport):
        self.transport = transport
        higherTransport = StackingTransport(self.transport)
        self.higherProtocol().connection_made(higherTransport)

    def data_received(self, data):
        self.higherProtocol().data_received(data)

    def connection_lost(self, exc):
        self.transport = None
        self.higherProtocol().connection_lost(exc)
class PlaneServer(asyncio.Protocol):
    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        print("Server connected")
        self.transport = transport
        self._deserializer = PacketType.Deserializer()
        self.a = 1
        self.b = 1
        self.c = 1
        self.d = 0

    def data_received(self, data):
        self._deserializer.update(data)
        for p in self._deserializer.nextPackets():
            if (isinstance(p, RequestPlanePacket)):
                plane = PlanePacket()
                plane.A = self.a
                plane.B = self.b
                plane.C = self.c
                plane.D = self.d
                self.transport.write(plane.__serialize__())
            elif (isinstance(p, PointPacket)):
                res = ResultPacket()
                res.result = (p.x*self.a +p.y*self.b + p.z*self.c == self.d)
                self.transport.write(res.__serialize__())
            else:
                self.transport.close()

    def connection_lost(self, exc):
        self.transport = None

class PassThroughLayerTwo(StackingProtocol):

    def connection_made(self, transport):
        self.transport = transport
        higherTransport = StackingTransport(self.transport)
        self.higherProtocol().connection_made(higherTransport)

    def data_received(self, data):
        self.higherProtocol().data_received(data)

    def connection_lost(self, exc):
        self.transport = None
        self.higherProtocol().connection_lost(exc)

if __name__=="__main__":
    echoArgs = {}

    args= sys.argv[1:]
    i = 0
    for arg in args:
        if arg.startswith("-"):
            k,v = arg.split("=")
            echoArgs[k]=v
        else:
            echoArgs[i] = arg
            i+=1

    if not 0 in echoArgs:
        sys.exit("")

    mode = echoArgs[0]
    loop = asyncio.get_event_loop()
    loop.set_debug(enabled=True)

    f = StackingProtocolFactory(lambda: PassThroughLayerOne(), lambda: PassThroughLayerTwo())
    ptConnector = playground.Connector(protocolStack=f)
    playground.setConnector("passthrough", ptConnector)
    if mode.lower() == 'server':
        playground.getConnector("passthrough").create_playground_server(lambda: PlaneServer(), 8000)
    else:
        playground.getConnector("passthrough").create_playground_connection (lambda: PlaneClient, '20174.1.1.1', 8000)
