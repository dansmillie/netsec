import asyncio
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import INT, BOOL
import random

class RequestPlanePacket(PacketType):
    DEFINITION_IDENTIFIER = "lab1b.dsmilli1.RequestPacket"
    DEFINITION_VERSION = "1.0"

class PlanePacket(PacketType):
    DEFINITION_IDENTIFIER = "lab1b.dsmilli1.PlanePacket"
    DEFINITION_VERSION = "1.0"
    FIELDS = [
            ("A", INT),
            ("B", INT),
            ("C", INT),
            ("D", INT)
            ]

class PointPacket(PacketType):
    DEFINITION_IDENTIFIER = "lab1b.dsmilli1.PointPacket"
    DEFINITION_VERSION = "1.0"
    FIELDS = [
            ("x", INT),
            ("y", INT),
            ("z", INT)
            ]

class ResultPacket(PacketType):
    DEFINITION_IDENTIFIER = "lab1b.dsmilli1.ResultPacket"
    DEFINITION_VERSION = "1.0"
    FIELDS = [
            ("result", BOOL),
            ]

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
        self.transport

def unitTest():
    #for now params are picked within the protocols
    from playground.network.testing import MockTransportToProtocol
    from playground.asyncio_lib.testing import TestLoopEx

    asyncio.set_event_loop(TestLoopEx())

    server = PlaneServer()
    client = PlaneClient()
    cTransport, sTransport = MockTransportToProtocol.CreateTransportPair(client, server)
    server.connection_made(sTransport)
    client.connection_made(cTransport)

if __name__=="__main__":
    unitTest()
