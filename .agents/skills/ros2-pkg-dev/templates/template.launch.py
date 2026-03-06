#!/usr/bin/env python3
"""
ROS2 Python启动文件模板
使用方式：复制此文件并根据需要配置节点参数
"""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    """
    生成启动描述
    
    示例：启动一个ROS2节点，支持通过命令行参数配置
    """
    # 声明启动参数（可选）
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true'
    )
    
    declare_node_name = DeclareLaunchArgument(
        'node_name',
        default_value='minimal_node',
        description='Name of the node'
    )
    
    # 获取参数值
    use_sim_time = LaunchConfiguration('use_sim_time')
    node_name = LaunchConfiguration('node_name')
    
    return LaunchDescription([
        # 声明参数
        declare_use_sim_time,
        declare_node_name,
        
        # 启动节点示例
        # 请根据实际包名和可执行文件名修改
        Node(
            package='pkg_name',           # 修改：包名
            executable='node_executable',  # 修改：可执行文件名
            name=node_name,
            output='screen',
            parameters=[{
                'use_sim_time': use_sim_time,
                'param1': 'value1',       # 添加节点参数
            }],
            remappings=[
                ('/old_topic', '/new_topic'),  # 可选：话题重映射
            ]
        ),
    ])
