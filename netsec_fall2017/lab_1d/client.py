import asyncio
from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import INT, BOOL
import random

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

if __name__=="__main__":
    playground.getConnector().create_playground_connection (lambda: PlaneClient, '20174.1.1.1', 8000)
