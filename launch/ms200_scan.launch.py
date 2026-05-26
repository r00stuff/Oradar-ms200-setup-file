#!/usr/bin/env python3
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    lidar_node = Node(
        package='oradar_lidar',
        executable='oradar_scan',
        name='ms200',
        output='screen',
        parameters=[
            {'port_name': '/dev/oradar'},
            {'baudrate': 230400},
            {'frame_id': 'laser_frame'},
            {'scan_topic': 'scan'},
            {'device_model': 'ms200'},
            {'angle_min': 0.0},
            {'angle_max': 360.0},
            {'range_min': 0.05},
            {'range_max': 20.0},
            {'clockwise': False},
            {'motor_speed': 10},
        ]
    )

    # Static TF: base_link → laser_frame
    # Adjust --z to match the actual lidar mounting height on the robot in metres.
    base_to_laser_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='base_link_to_laser_frame',
        arguments=['--x', '0', '--y', '0', '--z', '0.10',
                   '--roll', '0', '--pitch', '0', '--yaw', '0',
                   '--frame-id', 'base_link', '--child-frame-id', 'laser_frame']
    )

    return LaunchDescription([
        lidar_node,
        base_to_laser_tf,
    ])
