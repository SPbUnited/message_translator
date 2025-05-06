import math
import ssl_packet_package.protopy.spbunited.robot.control_pb2 as rcpb
from attrs import define
import bitstruct.c as bs


@define
class GlobalCoordinates:

    def proto2nrf(self, control: rcpb.GlobalCoordinates) -> bytes:
        fstring = "u12u12 u8"
        names = ["x", "y", "angle"]

        data_dict = {
            "x": int(control.x * 100) & 0xFFF,  # [m] -> [cm]
            "y": int(control.y * 100) & 0xFFF,  # [m] -> [cm]
            "angle": int(control.angle * 128 / math.pi) & 0xFF,  # [rad] -> [pi/128 rad]
        }

        print(data_dict)

        data = bs.pack_dict(fstring, names, data_dict)

        return data
