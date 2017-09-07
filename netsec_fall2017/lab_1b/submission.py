from playground.network.packet import PacketType
from playground.network.packet.fieldtypes import INT, BOOL

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

def unitTest():
    p1 = RequestPlanePacket()
    p1Bytes = p1.__serialize__()
    p1a = RequestPlanePacket.Deserialize(p1Bytes)
    assert p1 == p1a

    p2 = PlanePacket()
    p2.A = 1
    p2.B = -4
    p2.C = 0
    p2.D = 3
    p2Bytes = p2.__serialize__()
    p2a = PlanePacket.Deserialize(p2Bytes)
    assert p2a == p2
    assert p2a.A == 1
    assert p2a.B == -4
    assert p2a.C == 0
    assert p2a.D == 3

    p3 = PointPacket()
    p3.x = 17
    p3.y = -1
    p3.z = 0
    p3Bytes = p3.__serialize__()
    p3a = PointPacket.Deserialize(p3Bytes)
    assert p3 == p3a
    assert p3a.x == 17
    assert p3a.y == -1
    assert p3a.z == 0

    p4 = ResultPacket()
    p4.result = True
    p4Bytes = p4.__serialize__()
    p4a = ResultPacket.Deserialize(p4Bytes)
    assert p4 == p4a
    assert p4a.result

    p5 = ResultPacket()
    p5.result = False
    p5Bytes = p5.__serialize__()

    resultBytes = p4Bytes + p5Bytes
    deserializer = ResultPacket.Deserializer()
    while len(resultBytes) > 0:
        byte, resultBytes = resultBytes[:1], resultBytes[1:]
        deserializer.update(byte)
        for p in deserializer.nextPackets():
            print(p.result)

if __name__=="__main__":
    unitTest()
