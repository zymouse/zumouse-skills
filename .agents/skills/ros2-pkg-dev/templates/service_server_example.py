#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================
Python ROS2 Service Server 示例 (rclpy)
============================================
功能: 提供加法计算服务
服务类型: example_interfaces/srv/AddTwoInts
用法: 参考此代码在现有节点中添加 Service Server
============================================
"""

import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class ServiceServerExample(Node):
    """Service Server 示例节点"""

    def __init__(self):
        super().__init__('service_server_example')

        # 创建 Service Server
        # 参数: 服务类型, 服务名称, 回调函数
        self.service = self.create_service(
            AddTwoInts,
            'add_two_ints',
            self.handle_request)

        self.get_logger().info('Service Server 已启动，服务名: /add_two_ints')

    def handle_request(self, request: AddTwoInts.Request, response: AddTwoInts.Response):
        """服务回调函数
        
        Args:
            request: 客户端请求，包含 a 和 b 两个整数
            response: 返回给客户端的响应，包含 sum 字段
            
        Returns:
            response: 处理后的响应对象
        """
        self.get_logger().info(f'收到请求: a={request.a}, b={request.b}')

        # 执行业务逻辑
        response.sum = request.a + request.b

        self.get_logger().info(f'返回结果: sum={response.sum}')
        return response

    def destroy_node(self):
        """销毁节点"""
        self.get_logger().info('正在销毁 Service Server 节点...')
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = ServiceServerExample()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('收到键盘中断')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

"""
自定义服务接口定义示例 (srv/AddTwoInts.srv):

# 请求部分
int64 a
int64 b
---
# 响应部分
int64 sum
"""
