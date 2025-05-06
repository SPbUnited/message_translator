# Message translator

## Installation

```bash
make init
source venv/bin/activate
make build
```

## Usage

```bash
make up
```

## API

`ssl_packet_package/proto/spbunited/robot/control.proto` : `RobotCommand`

It binds zmq adress: `ipc:///tmp/united.robot_control::SUB`

### Example

```python
from ssl_packet_package.protopy.spbunited.robot import control_pb2 as rcpb
import zmq

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.connect("ipc:///tmp/united.robot_control")

robot_command = rcpb.RobotCommand(
    robot_id=1,
    old_format=rcpb.OldFormat(
        vel_x=0,
        vel_y=0,
        angular_velocity_or_delta_angle=0,
        kicker_voltage=0,
        dribbler_voltage=0,
        high_voltage=False,
        dribbler_is_enabled=False,
        angvel_angle_toggle=True,
        kick_high=False,
        kick_straight=True,
        autokick_high=False,
        autokick_straight=True,
    ),
)

socket.send(robot_command.SerializeToString())
```
