#!/usr/bin/env python3
"""
ROS2 Python节点模板 - 标准订阅者节点
使用方式：复制此文件并修改类名和逻辑
"""
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from std_msgs.msg import String


class MinimalSubscriber(Node):
    """
    最小订阅者节点示例
    
    功能：
    - 订阅指定话题并打印接收到的消息
    - 支持通过参数配置话题名称
    """
    
    def __init__(self):
        super().__init__('minimal_subscriber')
        
        # 参数声明（支持运行时配置）
        self.declare_parameter('topic_name', 'topic')
        topic = self.get_parameter('topic_name').value
        
        # QoS配置（显式指定，不依赖默认）
        qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )
        
        # 创建订阅者
        self.sub = self.create_subscription(
            String, topic, self.listener_callback, qos)
        self.get_logger().info(f'Subscribed to {topic}')

    def listener_callback(self, msg: String):
        """消息回调函数"""
        self.get_logger().info(f'Received: "{msg.data}"')


def main(args=None):
    """节点入口函数"""
    rclpy.init(args=args)
    
    node = MinimalSubscriber()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('收到键盘中断信号，正在关闭...')
    finally:
        # 清理资源
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
