import asyncio
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import INT, BOOL
import random

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

if __name__=="__main__":
    playground.getConnector().create_playground_server(lambda: PlaneServer(), 8000)
