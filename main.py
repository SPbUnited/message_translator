from message_translator.message_translator import MessageTranslator
from ssl_packet_package.protopy.spbunited.robot import (
    control_pb2 as rcpb,
)
import zmq

context = zmq.Context()
s_robot_control = context.socket(zmq.SUB)
s_robot_control.bind("ipc:///tmp/united.robot_control")
s_robot_control.setsockopt_string(zmq.SUBSCRIBE, "")

translator = MessageTranslator()


to_rrc = context.socket(zmq.CLIENT)
to_rrc.bind("https://10.0.120.210:8001")
# to_rrc.setsockopt_string(zmq.SUBSCRIBE, "")

def print_bin(data: bytes):
    print(" ".join(bin(byte)[2:].zfill(8) for byte in data))


if __name__ == "__main__":
    robot_command = rcpb.RobotCommand()
    while True:
        data = s_robot_control.recv()
        robot_command.ParseFromString(data)
        print(robot_command)

        data = translator.proto2nrf(robot_command)
        to_rrc.send(data)
        print(data)
        print(len(data))
        print_bin(data)
