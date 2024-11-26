from rtde.rtde import RTDE


def test():
    rtde = RTDE("192.168.1.102")

    # Test joint control functions
    # Set home first
    home = [1.57, -1.7, 2, -1.87, -1.57, 3.14]

    target1 = [1.5, -1.6, 1.9, -1.8, -1.5, 3]
    target2 = [1.3, -1.5, 1.8, -1.7, -1.4, 2.9]
    target3 = [1.1, -1.4, 1.5, -1.8, -1.5, 3.14]
    traj = [home, target1, target2, target3]
    traj = [traj[i] + [0.5, 1.0, 0.02] for i in range(len(traj))]

    try:
        # Move to home
        rtde.move_joint(home)

        # Get current joint angle and tool pose
        curr_joint = rtde.get_joint_values()
        print("Joint values: ", curr_joint)

        # Test joint controls
        rtde.move_joint(target1)

        # Test joint trajectory
        rtde.move_joint(home)
        rtde.move_joint_trajectory(traj)

        # Stop the robot
        rtde.stop()

    finally:
        rtde.stop_script()


if __name__ == "__main__":
    test()
