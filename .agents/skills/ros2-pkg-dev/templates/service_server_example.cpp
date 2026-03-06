// ============================================
// C++ ROS2 Service Server 示例 (rclcpp)
// ============================================
// 功能: 提供加法计算服务
// 服务类型: example_interfaces/srv/AddTwoInts
// 用法: 参考此代码在现有节点中添加 Service Server
// ============================================

#include <rclcpp/rclcpp.hpp>
#include <example_interfaces/srv/add_two_ints.hpp>

class ServiceServerExample : public rclcpp::Node
{
public:
  ServiceServerExample()
  : Node("service_server_example")
  {
    // 创建 Service Server
    // 参数: 服务名称, 回调函数
    service_ = this->create_service<example_interfaces::srv::AddTwoInts>(
      "add_two_ints", std::bind(&ServiceServerExample::handle_request, this, 
      std::placeholders::_1, std::placeholders::_2));

    RCLCPP_INFO(this->get_logger(), "Service Server 已启动，服务名: /add_two_ints");
  }

private:
  // 服务回调函数
  // 参数: request - 客户端请求, response - 返回给客户端的响应
  void handle_request(
    const std::shared_ptr<example_interfaces::srv::AddTwoInts::Request> request,
    std::shared_ptr<example_interfaces::srv::AddTwoInts::Response> response)
  {
    RCLCPP_INFO(this->get_logger(), 
      "收到请求: a=%ld, b=%ld", request->a, request->b);

    // 执行业务逻辑
    response->sum = request->a + request->b;

    RCLCPP_INFO(this->get_logger(), "返回结果: sum=%ld", response->sum);
  }

  // Service Server 成员变量
  rclcpp::Service<example_interfaces::srv::AddTwoInts>::SharedPtr service_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ServiceServerExample>());
  rclcpp::shutdown();
  return 0;
}

/* 
 * 自定义服务接口定义示例 (srv/AddTwoInts.srv):
 * 
 * # 请求部分
 * int64 a
 * int64 b
 * ---
 * # 响应部分
 * int64 sum
 */
