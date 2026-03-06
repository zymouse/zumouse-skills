#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================
Python ROS2 Subscriber 示例 (rclpy)
============================================
功能: 订阅 std_msgs/String 类型消息
用法: 参考此代码在现有节点中添加 Subscriber
============================================
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class SubscriberExample(Node):
    """Subscriber 示例节点"""

    def __init__(self):
        super().__init__('subscriber_example')

        # 创建 Subscriber
        # 参数: 消息类型, topic名称, 回调函数, QoS队列深度
        self.subscription = self.create_subscription(
            String,
            'chatter',
            self.topic_callback,
            10)

        self.get_logger().info('Subscriber 已启动，订阅话题: /chatter')

    def topic_callback(self, msg: String):
        """消息回调函数
        
        Args:
            msg: 收到的 String 类型消息
        """
        self.get_logger().info(f"收到消息: '{msg.data}'")

        # 在这里添加你的业务逻辑
        self.process_message(msg.data)

    def process_message(self, data: str):
        """业务处理函数示例
        
        Args:
            data: 消息内容字符串
        """
        # 例如：解析消息内容、触发其他操作等
        self.get_logger().debug(f'处理消息: {data}')

    def destroy_node(self):
        """销毁节点"""
        self.get_logger().info('正在销毁 Subscriber 节点...')
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = SubscriberExample()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('收到键盘中断')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
