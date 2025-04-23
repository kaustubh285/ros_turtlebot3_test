#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Pose
from sensor_msgs.msg import LaserScan
import random
import math


class TurtleBot3Node(Node):
    """
    Node to publish and subscribe for TurtleBot3 test.

    Publishers:
    - /turtle1/cmd_vel (geometry_msgs/Twist)
    - /robot_description (sensor_msgs/LaserScan)

    Subscribers:
    - /turtle1/pose (geometry_msgs/Pose)
    """

    def __init__(self):
        super().__init__("turtlebot3_test_node")

        # Create publishers
        self.cmd_vel_publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.laser_publisher = self.create_publisher(
            LaserScan, "/robot_description", 10
        )

        # Create subscribers
        self.pose_subscription = self.create_subscription(
            Pose, "/turtle1/pose", self.pose_callback, 10
        )

        # Create timers for publishers
        self.cmd_vel_timer = self.create_timer(0.1, self.publish_cmd_vel)
        self.laser_timer = self.create_timer(1.0, self.publish_laser_scan)

        # Initialize variables to store the latest pose
        self.latest_pose = None

        self.get_logger().info("TurtleBot3 test node has been started")

    def pose_callback(self, msg):
        """Callback for the pose subscription."""
        self.latest_pose = msg
        self.get_logger().info(
            f"Received pose: x={msg.x:.2f}, y={msg.y:.2f}, theta={msg.theta:.2f}"
        )

    def publish_cmd_vel(self):
        """Publish velocity commands."""
        msg = Twist()

        # Create random velocity commands
        msg.linear.x = 0.2  # Forward velocity
        msg.angular.z = 0.3  # Angular velocity

        # If we have pose data, adjust the velocity based on it
        if self.latest_pose is not None:
            # Simple example: slow down if we're getting far from the origin
            distance = math.sqrt(self.latest_pose.x**2 + self.latest_pose.y**2)
            if distance > 8.0:
                msg.linear.x = 0.1
                msg.angular.z = 0.5  # Turn more to go back toward the center

        self.cmd_vel_publisher.publish(msg)
        self.get_logger().debug(
            f"Published cmd_vel: linear.x={msg.linear.x}, angular.z={msg.angular.z}"
        )

    def publish_laser_scan(self):
        """Publish fake laser scan data."""
        msg = LaserScan()

        # Set header
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "base_scan"

        # Set laser scan parameters
        msg.angle_min = 0.0
        msg.angle_max = 2 * math.pi
        msg.angle_increment = (2 * math.pi) / 360
        msg.time_increment = 0.0
        msg.scan_time = 0.0
        msg.range_min = 0.120
        msg.range_max = 3.5

        # Generate fake range data (360 points for a full scan)
        ranges = []
        for i in range(360):
            # Generate random distance between range_min and range_max
            range_val = random.uniform(msg.range_min, msg.range_max)
            ranges.append(range_val)

        msg.ranges = ranges

        # Publish the laser scan message
        self.laser_publisher.publish(msg)
        self.get_logger().debug("Published laser scan data")


def main(args=None):
    rclpy.init(args=args)

    node = TurtleBot3Node()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Keyboard interrupt, shutting down")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
