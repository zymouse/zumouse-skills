// ============================================
// C++ ROS2 Service Client 示例 (rclcpp)
// ============================================
// 功能: 调用加法计算服务
// 服务类型: example_interfaces/srv/AddTwoInts
// 用法: 参考此代码在现有节点中添加 Service Client
// ============================================

#include <rclcpp/rclcpp.hpp>
#include <example_interfaces/srv/add_two_ints.hpp>

#include <chrono>

using namespace std::chrono_literals;

class ServiceClientExample : public rclcpp::Node
{
public:
  ServiceClientExample()
  : Node("service_client_example")
  {
    // 创建 Service Client
    // 参数: 服务名称
    client_ = this->create_client<example_interfaces::srv::AddTwoInts>("add_two_ints");

    // 等待服务上线
    while (!client_->wait_for_service(1s)) {
      if (!rclcpp::ok()) {
        RCLCPP_ERROR(this->get_logger(), "被中断，退出");
        return;
      }
      RCLCPP_INFO(this->get_logger(), "等待服务 /add_two_ints 上线...");
    }

    RCLCPP_INFO(this->get_logger(), "Service Client 已启动，等待调用服务");

    // 示例：定时调用服务
    timer_ = this->create_wall_timer(
      2s, std::bind(&ServiceClientExample::send_request, this));
  }

private:
  void send_request()
  {
    // 判断服务是否就绪
    if (!client_->service_is_ready()) {
      RCLCPP_WARN(this->get_logger(), "服务 /add_two_ints 当前不可用，跳过本次请求");
      return;
    }

    // 创建请求
    auto request = std::make_shared<example_interfaces::srv::AddTwoInts::Request>();
    request->a = 10 + rand() % 90;  // 随机数 10-99
    request->b = 10 + rand() % 90;

    RCLCPP_INFO(this->get_logger(), "发送请求: a=%ld, b=%ld", request->a, request->b);

    // 异步发送请求
    auto result_future = client_->async_send_request(request);

    // 等待响应（阻塞方式，可选）
    // auto result = rclcpp::spin_until_future_complete(shared_from_this(), result_future);

    // 非阻塞方式：使用回调
    result_future.then(
      [this, request](rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedFuture future) {
        try {
          auto response = future.get();
          RCLCPP_INFO(this->get_logger(), 
            "收到响应: %ld + %ld = %ld", request->a, request->b, response->sum);
        } catch (const std::exception &e) {
          RCLCPP_ERROR(this->get_logger(), "服务调用失败: %s", e.what());
        }
      });
  }

  // Service Client 成员变量
  rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedPtr client_;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ServiceClientExample>());
  rclcpp::shutdown();
  return 0;
}
