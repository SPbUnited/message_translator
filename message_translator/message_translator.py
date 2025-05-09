from ssl_packet_package.protopy.spbunited.robot import control_pb2 as rcpb
from attrs import define, field
from .old_format import OldFormat
from .kicker_and_dribbler import KickerAndDribbler
from .speed_control import SpeedControl
from .coordinate_control import CoordinateControl
from .global_coordinate import GlobalCoordinates
from .cap_vel_and_accel import CapVelAndAccel
import bitstruct.c as bs

MESSAGE_MAP = {
    "old_format": OldFormat,
    "kicker_and_dribbler": KickerAndDribbler,
    "speed_control": SpeedControl,
    "coordinate_control": CoordinateControl,
    "global_coordinates": GlobalCoordinates,
    "cap_vel_and_accel": CapVelAndAccel,
}


@define
class MessageTranslator:

    def proto2nrf(self, robot_command: rcpb.RobotCommand) -> bytes:
        control_type = robot_command.WhichOneof("control")
        translator = MESSAGE_MAP[control_type]()
        control_bytes = translator.proto2nrf(getattr(robot_command, control_type))
        command_type_number = rcpb.RobotControlType.Value(control_type.upper())
        id_bytes = self.id2nrf(command_type_number, robot_command.robot_id)
        return id_bytes + control_bytes

    def id2nrf(self, command_type_number: int, robot_id: int) -> bytes:
        fstring = "u4u4"
        data = bs.pack(fstring, command_type_number, robot_id)
        return data


if __name__ == "__main__":
    robot_command = rcpb.RobotCommand(
        robot_id=1,
        # old_format=rcpb.OldFormat(
        #     vel_x=0,
        #     vel_y=0,
        #     angular_velocity_or_delta_angle=0,
        #     kicker_voltage=0,
        #     dribbler_voltage=0,
        #     high_voltage=False,
        #     dribbler_is_enabled=False,
        #     angvel_angle_toggle=True,
        #     kick_high=False,
        #     kick_straight=True,
        #     autokick_high=False,
        #     autokick_straight=True,
        # ),
        # kicker_and_dribbler=rcpb.KickerAndDribbler(
        #     kicker_mode=rcpb.KickerMode.AUTOKICK_STRAIGHT,
        #     kicker_setting=0,
        #     dribbler_setting=0,
        # ),
        # speed_control=rcpb.SpeedControl(vel_x=0, vel_y=0, delta_angle=1),
        # coordinate_control=rcpb.CoordinateControl(
        #     targets=[
        #         rcpb.Target(id=1, x=1, y=2, vx=3, vy=4, angle=5),
        #         rcpb.Target(id=2, x=6, y=7, vx=8, vy=9, angle=10),
        #         rcpb.Target(id=3, x=-1, y=-2, vx=-3, vy=-4, angle=-5),
        #         rcpb.Target(id=4, x=-6, y=-7, vx=-8, vy=-9, angle=-10),
        #         rcpb.Target(id=5, x=-11, y=-12, vx=-13, vy=-14, angle=-15),
        #         # rcpb.Target(id=6, x=-11, y=-12, vx=-13, vy=-14, angle=-15),
        #     ]
        # ),
        global_coordinates=rcpb.GlobalCoordinates(x=1, y=2, angle=3),
    )

    print(robot_command)

    translator = MessageTranslator()

    data = translator.proto2nrf(robot_command)

    binary_str = " ".join(bin(byte)[2:].zfill(8) for byte in data)
    print(data)
    print(len(data))
    print(binary_str)
