import ssl_packet_package.protopy.spbunited.robot.control_pb2 as rcpb
import google.protobuf.json_format as jf
from attrs import define
import bitstruct.c as bs


@define
class KickerAndDribbler:

    def proto2nrf(self, control: rcpb.KickerAndDribbler) -> bytes:
        fstring = "u8 u4u4"
        names = ["kicker_mode", "kicker_setting", "dribbler_setting"]
        data_dict = jf.MessageToDict(
            control, preserving_proto_field_name=True, use_integers_for_enums=True
        )

        print(data_dict)

        data = bs.pack_dict(fstring, names, data_dict)

        return data
