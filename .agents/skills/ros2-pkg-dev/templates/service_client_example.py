#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================
Python ROS2 Service Client 示例 (rclpy)
============================================
功能: 调用加法计算服务
服务类型: example_interfaces/srv/AddTwoInts
用法: 参考此代码在现有节点中添加 Service Client
============================================
"""

import functools
import random

import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class ServiceClientExample(Node):
    """Service Client 示例节点"""

    def __init__(self):
        super().__init__('service_client_example')

        # 创建 Service Client
        # 参数: 服务类型, 服务名称
        self.client = self.create_client(AddTwoInts, 'add_two_ints')

        # 等待服务上线
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('等待服务 /add_two_ints 上线...')
            if not rclpy.ok():
                self.get_logger().error('被中断，退出')
                return

        self.get_logger().info('Service Client 已启动，服务已连接')

        # 创建定时器，每2秒调用一次服务
        self.timer = self.create_timer(2.0, self.send_request)
        self.call_count = 0

    def send_request(self):
        """发送服务请求"""
        # 创建请求
        request = AddTwoInts.Request()
        request.a = random.randint(10, 99)
        request.b = random.randint(10, 99)

        self.get_logger().info(f'发送请求: a={request.a}, b={request.b}')

        # 异步发送请求
        future = self.client.call_async(request)

        # 使用 functools.partial 绑定额外参数到回调函数
        # 比 lambda 更清晰，且能正确处理异常
        future.add_done_callback(
            functools.partial(self._handle_response, request.a, request.b))

        self.call_count += 1
        # 示例：只调用5次
        if self.call_count >= 5:
            self.timer.cancel()
            self.get_logger().info('已完成5次调用，停止定时器')

    def _handle_response(self, a: int, b: int, future):
        """处理服务响应
        
        Args:
            a: 请求的第一个数（通过 partial 绑定）
            b: 请求的第二个数（通过 partial 绑定）
            future: 包含响应结果的 Future 对象（由 ROS2 传入）
        """
        try:
            response = future.result()
            self.get_logger().info(f'收到响应: {a} + {b} = {response.sum}')
        except Exception as e:
            self.get_logger().error(f'服务调用失败: {str(e)}')

    def destroy_node(self):
        """销毁节点"""
        self.get_logger().info('正在销毁 Service Client 节点...')
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = ServiceClientExample()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('收到键盘中断')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
