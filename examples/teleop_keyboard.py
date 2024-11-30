import time
import numpy as np
from rtde.rtde import RTDE
from pynput import keyboard


class Teleop:
    """A simple teleoperation class for controlling the robot tool pose.
    This class is needed mostly when the input devices have no "Home" position.
    (e.g. VR controller). Or the input command is relative to the current pose,
    instead of providing the absolute pose.
    In these two cases, it will require the class to store relative "Home"
    positions for both the input device and the robot tool.

    The logic in the code supports both position and rotation control.
    But the resume() and track() function are only implemented
    for position control just for demonstration.
    """

    def __init__(self, rtde, rate=0.008):
        self.rtde: RTDE = rtde
        self.rate = rate
        self.paused = True

        self.input_anchor = None  # [x, y, z, *quat]
        self.tool_anchor = None  # [x, y, z, *quat]

    def resume(self, input_anchor):
        # Assume input is [x, y, z, *quat]
        self.input_anchor = np.array(input_anchor)
        # Tool pose is [x, y, z, *quat]
        tool_anchor = self.rtde.get_tool_pose()
        self.tool_anchor = np.zeros(7)
        self.tool_anchor[:3] = tool_anchor[:3]
        # self.tool_anchor[3:] = rotvec_to_quat(tool_anchor[3:])
        # keep the same orientation
        self.tool_anchor[3:6] = tool_anchor[3:]

        self.target = np.copy(self.tool_anchor)
        self.paused = False

    def pause(self):
        self.paused = True

    def track(self, user_input):
        if self.paused:
            return
        user_input = np.array(user_input)

        # The relative input value is the difference
        # between the user input and the anchor
        rel_translation = user_input[:3] - self.input_anchor[:3]
        # rel_quat = quat_multiply(
        #     user_input[3:], quat_conjugate(self.input_anchor[3:])
        # )

        # The actual required tool pose is the sum of the anchor and the input
        global_translation = self.tool_anchor[:3] + rel_translation
        # global_quat = quat_multiply(rel_quat, self.tool_anchor[3:])

        self.target = np.zeros(6)
        self.target[:3] = global_translation
        # self.target[3:] = quat_to_rotvec(self.target[3:])
        # keep the same orientation
        self.target[3:] = self.tool_anchor[3:6]

        # Send control command
        self.rtde.servo_tool(self.target, time=self.rate)


def test():
    rtde = RTDE("192.168.1.102")
    teleop = Teleop(rtde, rate=0.01)

    # Test joint control functions
    # Set home first
    home_joint = np.array([1.57, -1.7, 2, -1.87, -1.57, 3.14])
    home = np.array([0.2, -0.6, 0.4, 3.14, 0, 0])

    # Input container
    input = [0, 0, 0]
    running = [True]
    pressed_keys = set()

    try:
        # Move to home
        rtde.move_joint(home_joint)
        rtde.move_tool(home)

        # Start teleop
        teleop.resume(input_anchor=[0, 0, 0])
        step = 0.001

        on_press, on_release = control_behavior(pressed_keys, running)
        with keyboard.Listener(on_press, on_release) as listener:
            while running[0]:
                if "w" in pressed_keys:
                    input[0] += step  # Increase X
                if "s" in pressed_keys:
                    input[0] -= step  # Decrease X
                if "a" in pressed_keys:
                    input[1] += step  # Increase Y
                if "d" in pressed_keys:
                    input[1] -= step  # Decrease Y
                if "i" in pressed_keys:
                    input[2] += step  # Increase Z
                if "j" in pressed_keys:
                    input[2] -= step  # Decrease Z

                # Send updated input to teleop
                teleop.track(input)
                # Delay for the control rate
                time.sleep(teleop.rate)

    finally:
        rtde.stop_script()


def control_behavior(pressed_keys, running):
    def on_press(key):
        try:
            pressed_keys.add(key.char)
            if key.char == "q":
                running[0] = False
        except AttributeError:
            pass

    def on_release(key):
        try:
            pressed_keys.discard(key.char)
        except AttributeError:
            pass

    return on_press, on_release


if __name__ == "__main__":
    test()
