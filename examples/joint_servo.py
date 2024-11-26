import time
import numpy as np
from rtde.rtde import RTDE


def test():
    rtde = RTDE("192.168.1.102")

    # Test joint control functions
    # Set home first
    home = np.array([1.57, -1.7, 2, -1.87, -1.57, 3.14])
    incremental = 0.001 * np.ones(6)

    try:
        # Move to home
        rtde.move_joint(home)

        # Start servoing (Go from 0 -> -100 -> 100 -> 0)
        for i in range(0, -101, -1):
            rtde.servo_joint(home + incremental * i, time=0.008)
            time.sleep(0.008)
        for i in range(-100, 101, 1):
            rtde.servo_joint(home + incremental * i, time=0.008)
            time.sleep(0.008)
        for i in range(101, -1, -1):
            rtde.servo_joint(home + incremental * i, time=0.008)
            time.sleep(0.008)

    finally:
        rtde.stop_script()


if __name__ == "__main__":
    test()
