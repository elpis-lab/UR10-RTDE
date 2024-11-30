import time
import numpy as np
from rtde.rtde import RTDE

from examples.teleop_keyboard import Teleop
import pygame


def test():
    rtde = RTDE("192.168.1.102")
    teleop = Teleop(rtde, rate=0.01)

    # Test joint control functions
    # Set home first
    home_joint = np.array([1.57, -1.7, 2, -1.87, -1.57, 3.14])
    home = np.array([0.2, -0.6, 0.4, 3.14, 0, 0])

    # Input container
    input = [0, 0, 0]

    # Initialize pygame for joystick input
    pygame.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        print(f"Joystick initialized: {joystick.get_name()}")
    else:
        print("No joystick found")
        return
    clock = pygame.time.Clock()

    try:
        # Move to home
        rtde.move_joint(home_joint)
        rtde.move_tool(home)

        # Start teleop
        teleop.resume(input_anchor=[0, 0, 0])
        step = 0.001

        running = True
        while running:
            if not joystick:
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update input based on controller
            axis_y = joystick.get_axis(0)
            axis_x = -joystick.get_axis(1)
            axis_z = -joystick.get_axis(4)
            input[0] += axis_x * step
            input[1] += axis_y * step
            input[2] += axis_z * step

            # Send updated input to teleop
            teleop.track(input)
            # Delay for the control rate
            clock.tick(int(1 / teleop.rate))

    finally:
        rtde.stop_script()


if __name__ == "__main__":
    test()
