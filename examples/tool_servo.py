import time
import numpy as np
from rtde.rtde import RTDE


def test():
    rtde = RTDE("192.168.1.102")

    # Test joint control functions
    # Set home first
    home_joint = np.array([1.57, -1.7, 2, -1.87, -1.57, 3.14])
    home = np.array([0.2, -0.6, 0.4, 3.14, 0, 0])

    # Design the path
    num_points = 1000
    # Generate circle points in XY plane
    radius = 0.1
    angles = np.linspace(0, 4 * np.pi, num_points)
    circle_points = np.array(
        [
            [radius * np.cos(theta), radius * np.sin(theta), 0]
            for theta in angles
        ]
    )
    # Attach Z and orientation
    trajectory = [
        home + np.concatenate((point, [0, 0, 0])) for point in circle_points
    ]

    try:
        # Move to home
        rtde.move_joint(home_joint)
        rtde.move_tool(trajectory[0])

        for point in trajectory:
            rtde.servo_tool(point, time=0.008)
            time.sleep(0.008)

    finally:
        rtde.stop_script()


if __name__ == "__main__":
    test()
