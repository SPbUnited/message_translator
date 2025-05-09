import math
import ssl_packet_package.protopy.spbunited.robot.control_pb2 as rcpb
from attrs import define
import bitstruct.c as bs
from minifloat.minifloat import float_to_minifloat


@define
class CapVelAndAccel:

    def proto2nrf(self, control: rcpb.CapVelAndAccel) -> bytes:
        fstring = "u1u4u3 u1u4u3"
        names = [
            "vel_cap_sign",
            "vel_cap_exp",
            "vel_cap_mantissa",
            "accel_cap_sign",
            "accel_cap_exp",
            "accel_cap_mantissa",
        ]

        data_dict = {}

        (
            data_dict["vel_cap_sign"],
            data_dict["vel_cap_exp"],
            data_dict["vel_cap_mantissa"],
        ) = float_to_minifloat(control.max_vel, 4, 3)

        (
            data_dict["accel_cap_sign"],
            data_dict["accel_cap_exp"],
            data_dict["accel_cap_mantissa"],
        ) = float_to_minifloat(control.max_accel / 2, 4, 3)

        print(data_dict)

        data = bs.pack_dict(fstring, names, data_dict)

        return data
