#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================
Python ROS2 Publisher 示例 (rclpy)
============================================
功能: 定时发布 std_msgs/String 类型消息
用法: 参考此代码在现有节点中添加 Publisher
============================================
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class PublisherExample(Node):
    """Publisher 示例节点"""

    def __init__(self):
        super().__init__('publisher_example')
        self.count = 0

        # 创建 Publisher
        # 参数: 消息类型, topic名称, QoS队列深度
        self.publisher = self.create_publisher(String, 'chatter', 10)

        # 创建定时器，每0.5秒发布一次消息
        self.timer = self.create_timer(0.5, self.timer_callback)

        self.get_logger().info('Publisher 已启动，发布话题: /chatter')

    def timer_callback(self):
        """定时器回调函数"""
        # 创建消息
        msg = String()
        msg.data = f'Hello ROS2! Count: {self.count}'
        self.count += 1

        # 发布消息
        self.publisher.publish(msg)

        self.get_logger().info(f"发布: '{msg.data}'")

    def destroy_node(self):
        """销毁节点"""
        self.get_logger().info('正在销毁 Publisher 节点...')
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = PublisherExample()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('收到键盘中断')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
