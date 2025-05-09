import time
from ssl_packet_package.protopy.spbunited.robot import control_pb2 as rcpb
import zmq

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.connect("ipc:///tmp/united.robot_control")

time.sleep(1)

old_format_robot_command = rcpb.RobotCommand(
    robot_id=1,
    old_format=rcpb.OldFormat(
        vel_x=-20,
        vel_y=0,
        angular_velocity_or_delta_angle=0,
        kicker_setting=0,
        dribbler_setting=0,
        high_voltage=False,
        dribbler_is_enabled=False,
        angvel_angle_toggle=True,
        kick_high=False,
        kick_straight=True,
        autokick_high=False,
        autokick_straight=True,
    ),
)

speed_control_robot_command = rcpb.RobotCommand(
    robot_id=1,
    speed_control=rcpb.SpeedControl(
        vel_x=-20,
        vel_y=0,
        delta_angle=0,
    ),
)

coordinate_control_robot_command = rcpb.RobotCommand(
    robot_id=1,
    coordinate_control=rcpb.CoordinateControl(
        targets=[
            rcpb.Target(id=1, x=1, y=2, vx=3, vy=4, angle=5),
            rcpb.Target(id=2, x=6, y=7, vx=8, vy=9, angle=10),
            rcpb.Target(id=3, x=-1, y=-2, vx=-3, vy=-4, angle=-5),
            rcpb.Target(id=4, x=-6, y=-7, vx=-8, vy=-9, angle=-10),
            rcpb.Target(id=5, x=-11, y=-12, vx=-13, vy=-14, angle=-15),
        ]
    ),
)

kicker_and_dribbler_robot_command = rcpb.RobotCommand(
    robot_id=1,
    kicker_and_dribbler=rcpb.KickerAndDribbler(
        kicker_mode=rcpb.KickerMode.AUTOKICK_STRAIGHT,
        kicker_setting=0,
        dribbler_setting=0,
    ),
)

global_coordinates_robot_command = rcpb.RobotCommand(
    robot_id=1,
    global_coordinates=rcpb.GlobalCoordinates(x=1, y=2, angle=3),
)

cap_vel_and_accel_robot_command = rcpb.RobotCommand(
    robot_id=1,
    cap_vel_and_accel=rcpb.CapVelAndAccel(
        max_vel=1,
        max_accel=2,
    ),
)

for robot_command in [
    old_format_robot_command,
    speed_control_robot_command,
    coordinate_control_robot_command,
    kicker_and_dribbler_robot_command,
    global_coordinates_robot_command,
    cap_vel_and_accel_robot_command,
]:
    socket.send(robot_command.SerializeToString())
