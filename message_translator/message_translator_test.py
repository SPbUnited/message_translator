from message_translator.message_translator import MessageTranslator
import ssl_packet_package.protopy.spbunited.robot.control_pb2 as rcpb


def test_old_format():
    robot_command = rcpb.RobotCommand(
        robot_id=1,
        old_format=rcpb.OldFormat(
            vel_x=0,
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

    translator = MessageTranslator()

    data = translator.proto2nrf(robot_command)

    binary_str = " ".join(bin(byte)[2:].zfill(8) for byte in data)
    print(binary_str)


def test_kicker_and_dribbler():
    robot_command = rcpb.RobotCommand(
        robot_id=1,
        kicker_and_dribbler=rcpb.KickerAndDribbler(
            kicker_mode=rcpb.KickerMode.AUTOKICK_STRAIGHT,
            kicker_setting=0,
            dribbler_setting=0,
        ),
    )

    translator = MessageTranslator()

    data = translator.proto2nrf(robot_command)

    binary_str = " ".join(bin(byte)[2:].zfill(8) for byte in data)
    print(binary_str)


def test_speed_control():

    for vel_x, vel_y, ang_vel in [
        (0.1, 0.2, 0.3),
        (100, -134, -41),
    ]:
        robot_command = rcpb.RobotCommand(
            robot_id=1,
            speed_control=rcpb.SpeedControl(
                vel_x=vel_x, vel_y=vel_y, angular_velocity=ang_vel
            ),
        )

        translator = MessageTranslator()

        data = translator.proto2nrf(robot_command)

        binary_str = " ".join(bin(byte)[2:].zfill(8) for byte in data)
        print(binary_str)

    for vel_x, vel_y, delta_angle in [
        (0.1, 0.2, 0),
        (100, -134, 3.14),
        (100, -134, -3.14),
        (100, -134, -7.14),
    ]:
        robot_command = rcpb.RobotCommand(
            robot_id=1,
            speed_control=rcpb.SpeedControl(
                vel_x=vel_x, vel_y=vel_y, delta_angle=delta_angle
            ),
        )

        translator = MessageTranslator()

        data = translator.proto2nrf(robot_command)

        binary_str = " ".join(bin(byte)[2:].zfill(8) for byte in data)
        print(binary_str)


def test_coordinate_control():
    for point_count in range(7):
        targets = [
            rcpb.Target(id=1, x=1, y=2, vx=3, vy=4, angle=5),
            rcpb.Target(id=2, x=6, y=7, vx=8, vy=9, angle=10.0),
            rcpb.Target(id=3, x=-1, y=-2, vx=-3, vy=-4, angle=-5),
            rcpb.Target(id=4, x=-6.0, y=-7.0, vx=-8.0, vy=-9.0, angle=-10.0),
            rcpb.Target(id=5, x=-11, y=-12, vx=-13, vy=-14, angle=-15),
            rcpb.Target(id=6, x=-11, y=-12, vx=-13, vy=-14, angle=-15),
        ]

        try:
            robot_command = rcpb.RobotCommand(
                robot_id=1,
                coordinate_control=rcpb.CoordinateControl(
                    targets=targets[:point_count]
                ),
            )

            translator = MessageTranslator()

            data = translator.proto2nrf(robot_command)

            binary_str = " ".join(bin(byte)[2:].zfill(8) for byte in data)
            print(binary_str)
        except ValueError:
            assert point_count == 0 or point_count == 6
