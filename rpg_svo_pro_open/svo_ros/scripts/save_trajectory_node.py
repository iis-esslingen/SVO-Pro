#!/usr/bin/env python3
import os
from typing import cast

import rospy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path


class SaveTrajectoryNode:
    def __init__(self):
        rospy.init_node("save_trajectory_node", anonymous=True)
        rospy.on_shutdown(self.shutdown)

        # Create a subscriber to the specified topic
        rospy.Subscriber("/svo/pose_cam/0", PoseStamped, self.path_callback)

        # Create a file to write the odometry data
        file_name = rospy.get_param("~file_name")
        self.file = open(file_name, "w")
        self.file.write("# timestamp x y z qx qy qz qw\n")
        print("Trajectory saved in: " + os.path.realpath(self.file.name))

    def path_callback(self, msg: PoseStamped):

        self.file.write(
            str(msg.header.stamp.secs)
            + "."
            + str(msg.header.stamp.nsecs)
            + " "
            + str(msg.pose.position.x)
            + " "
            + str(msg.pose.position.y)
            + " "
            + str(msg.pose.position.z)
            + " "
            + str(msg.pose.orientation.x)
            + " "
            + str(msg.pose.orientation.y)
            + " "
            + str(msg.pose.orientation.z)
            + " "
            + str(msg.pose.orientation.w)
            + "\n"
        )

        self.file.truncate()

    def shutdown(self):
        # Close the file before shutting down the node
        self.file.close()


if __name__ == "__main__":
    node = SaveTrajectoryNode()
    rospy.spin()
