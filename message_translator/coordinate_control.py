import math
import ssl_packet_package.protopy.spbunited.robot.control_pb2 as rcpb
from attrs import define
import bitstruct.c as bs
from minifloat.minifloat import float_to_minifloat


@define
class CoordinateControl:

    def proto2nrf(self, control: rcpb.CoordinateControl) -> bytes:

        point_count = len(control.targets)

        if point_count == 0:
            raise ValueError("No points")
        if point_count > 5:
            raise ValueError("Too many points")

        first_point_id = control.targets[0].id

        print(first_point_id, point_count)

        byte1_fstring = "u4u4"
        data = bs.pack(byte1_fstring, first_point_id & 0xF, point_count)

        for point in control.targets:
            point_fstring = "u12u12 u1u4u3 u1u4u3 u8"
            point_names = [
                "x",
                "y",
                "vx_sign",
                "vx_exp",
                "vx_mantissa",
                "vy_sign",
                "vy_exp",
                "vy_mantissa",
                "angle",
            ]

            vx_sign, vx_exp, vx_mantissa = float_to_minifloat(point.vx, 4, 3)
            vy_sign, vy_exp, vy_mantissa = float_to_minifloat(point.vy, 4, 3)

            data_dict = {
                "x": int(point.x * 100) & 0xFFF,  # [m] -> [cm]
                "y": int(point.y * 100) & 0xFFF,  # [m] -> [cm]
                "vx_sign": vx_sign,
                "vx_exp": vx_exp,
                "vx_mantissa": vx_mantissa,
                "vy_sign": vy_sign,
                "vy_exp": vy_exp,
                "vy_mantissa": vy_mantissa,
                "angle": int(point.angle * 128 / math.pi)
                & 0xFF,  # [rad] -> [pi/128 rad]
            }

            print(point_names)
            print(data_dict)

            point_data = bs.pack_dict(point_fstring, point_names, data_dict)
            data += point_data

        return data
