import math
import ssl_packet_package.protopy.spbunited.robot.control_pb2 as rcpb
from attrs import define
import bitstruct.c as bs
from minifloat.minifloat import float_to_minifloat


@define
class SpeedControl:

    def proto2nrf(self, control: rcpb.SpeedControl) -> bytes:
        fstring = "u1u4u3 u1u4u3 "  # b1u3u3b1"
        names = [
            "vel_x_sign",
            "vel_x_exp",
            "vel_x_mantissa",
            "vel_y_sign",
            "vel_y_exp",
            "vel_y_mantissa",
            # "anvedelta_sign",
            # "anvedelta_exp",
            # "anvedelta_mantissa",
        ]

        vel_x_sign, vel_x_exp, vel_x_mantissa = float_to_minifloat(control.vel_x, 4, 3)
        vel_y_sign, vel_y_exp, vel_y_mantissa = float_to_minifloat(control.vel_y, 4, 3)

        data_dict = {
            "vel_x_sign": vel_x_sign,
            "vel_x_exp": vel_x_exp,
            "vel_x_mantissa": vel_x_mantissa,
            "vel_y_sign": vel_y_sign,
            "vel_y_exp": vel_y_exp,
            "vel_y_mantissa": vel_y_mantissa,
        }

        angular_velocity_or_angle_name = control.WhichOneof("angular_velocity_or_angle")

        data_dict["is_delta_angle"] = angular_velocity_or_angle_name == "delta_angle"

        if angular_velocity_or_angle_name == "delta_angle":
            names.append("delta_angle")
            fstring += "u7b1"
            data_dict["delta_angle"] = int(control.delta_angle * 64 / math.pi) & 0x7F

        else:
            names.append("ang_vel_sign")
            names.append("ang_vel_exp")
            names.append("ang_vel_mantissa")
            fstring += "u1u3u3b1"
            (
                data_dict["ang_vel_sign"],
                data_dict["ang_vel_exp"],
                data_dict["ang_vel_mantissa"],
            ) = float_to_minifloat(control.angular_velocity, 3, 3)

        names.append("is_delta_angle")

        print(names)
        print(data_dict)

        data = bs.pack_dict(fstring, names, data_dict)

        return data
