from setuptools import setup
import os
from glob import glob

package_name = "ros_turtlebot3_test"

setup(
    name=package_name,
    version="0.0.1",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Your Name",
    maintainer_email="user@example.com",
    description="A ROS 2 package for testing TurtleBot3 publishing and subscribing",
    license="Apache License 2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "turtlebot3_node = ros_turtlebot3_test.turtlebot3_node:main",
        ],
    },
)
