from rtde.rtde import RTDE


def test():
    rtde = RTDE("192.168.1.102")

    # Test joint control functions
    # Set home first
    home_joint = [1.57, -1.7, 2, -1.87, -1.57, 3.14]
    home = [0.2, -0.6, 0.4, 3.14, 0, 0]

    target1 = [0.3, -0.5, 0.4, 3.14, 0, 0]
    target2 = [0.2, -0.5, 0.4, 3.14, 0, 0]
    target3 = [0.2, -0.6, 0.4, 3.14, 0, 0]
    traj = [home, target1, target2, target3]
    traj = [traj[i] + [0.1, 1.0, 0.02] for i in range(len(traj))]

    try:
        # Move to home
        rtde.move_joint(home_joint)

        # Get current joint angle and tool pose
        curr_tool = rtde.get_tool_pose()
        print("Tool pose: ", curr_tool)

        # Test tool controls
        rtde.move_tool(target1)

        # Test tool trajectory
        rtde.move_tool(home)
        rtde.move_tool_trajectory(traj)

        # Stop the robot
        rtde.stop()

    finally:
        rtde.stop_script()


if __name__ == "__main__":
    test()
