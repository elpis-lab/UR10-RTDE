import time
import numpy as np
from rtde.rtde import RTDE
import keyboard


class Teleop:
    def __init__(self, rtde, rate=0.008):
        self.rtde: RTDE = rtde
        self.rate = rate
        self.paused = True

        self.input_anchor = None
        self.tool_anchor = None

    def resume(self, input_anchor):
        self.input_anchor = input_anchor
        self.tool_anchor = self.rtde.get_tool_pose()
        self.paused = False

    def pause(self):
        self.paused = True

    def track(self, input):
        if self.paused:
            return

        # The relative input value is the difference 
        # between the actual input and the anchor
        rel_input = [
            input[i] - self.input_anchor[i] for i in range(len(input))
        ]
        # The actual required tool pose is the sum of the anchor and the input
        global_tool = [
            self.tool_anchor[i] + rel_input[i] 
            for i in range(len(rel_input))
        ]
        # add rotation back
        global_tool += self.tool_anchor[3:]

        # Send control command
        self.rtde.servo_tool(global_tool, time=self.rate)


def test():
    rtde = RTDE("192.168.1.102")
    teleop = Teleop(rtde, rate=0.01)

    # Test joint control functions
    # Set home first
    home_joint = np.array([1.57, -1.7, 2, -1.87, -1.57, 3.14])
    home = np.array([0.2, -0.6, 0.4, 3.14, 0, 0])

    # Input container
    input = [0, 0, 0]

    try:
        # Move to home
        rtde.move_joint(home_joint)
        rtde.move_tool(home)

        # Start teleop
        teleop.resume(input_anchor=[0, 0, 0])
        step = 0.001
        while True:
            # Read keyboard input
            # w a s d j i for x y z
            # Handle keyboard input
            if keyboard.is_pressed("w"):  # Increase X
                input[0] += step
            if keyboard.is_pressed("s"):  # Decrease X
                input[0] -= step
            if keyboard.is_pressed("a"):  # Increase Y
                input[1] += step
            if keyboard.is_pressed("d"):  # Decrease Y
                input[1] -= step
            if keyboard.is_pressed("i"):  # Increase Z
                input[2] += step
            if keyboard.is_pressed("j"):  # Decrease Z
                input[2] -= step

            # Quit condition
            if keyboard.is_pressed("q"):
                print("Exiting teleop.")
                break

            # Send updated input to teleop
            teleop.track(input)
            # Delay for the control rate
            time.sleep(teleop.rate)

    finally:
        rtde.stop_script()


if __name__ == "__main__":
    test()
