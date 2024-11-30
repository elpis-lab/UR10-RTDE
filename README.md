# UR10 RTDE
This project provides a wrapper class in Python to communicate with UR robot using RTDE

## Usage

This project uses the UR **RTDE** interface provided by UR robot.

```
pip install ur-rtde
```

The wrapper class `RTDE` is provided to communicate and control UR robots with **RTDE** interface. The complete **RTDE** API is provided in the [official documentation](https://sdurobotics.gitlab.io/ur_rtde/api/api.html#rtde-control-interface-api). This class includes the most commonly used ones:

### Receive Interface
- get_joint_values()
- get_joint_velocities()
- get_tool_pose()
- get_tool_speed()

### Control Interface
Joint Space Control
- move_joint()
- move_joint_trajectory()
- speed_joint()
- servo_joint()

Tool Space Control
- move_tool()
- move_tool_trajectory()
- speed_tool()
- servo_tool()

## Examples
This repository provides examples such as joint control, tool control, servoing and teleoperation. Check out the scripts in **examples** folder for more details.
