import ssl_packet_package.protopy.spbunited.robot.control_pb2 as rcpb
import google.protobuf.json_format as jf
from attrs import define
import bitstruct.c as bs


@define
class OldFormat:

    def proto2nrf(self, control: rcpb.OldFormat) -> bytes:
        old_format_fstring = "s8 s8 s8 u4u4 p1b1b1b1b1b1b1b1"
        old_format_names = list(
            jf.MessageToDict(control, preserving_proto_field_name=True).keys()
        )

        old_format_dict = jf.MessageToDict(control, preserving_proto_field_name=True)

        # old_format_dict["vel_x"] = int(old_format_dict["vel_x"] * 100)
        # old_format_dict["vel_y"] = int(old_format_dict["vel_y"] * 100)
        # old_format_dict["angular_velocity_or_delta_angle"] = int(
        #     old_format_dict["angular_velocity_or_delta_angle"] * 100
        # )
        # old_format_dict["kicker_voltage"] = int(old_format_dict["kicker_voltage"] / 100)
        # old_format_dict["dribbler_voltage"] = int(
        #     old_format_dict["dribbler_voltage"] / 100
        # )

        data = bs.pack_dict(old_format_fstring, old_format_names, old_format_dict)

        return data
