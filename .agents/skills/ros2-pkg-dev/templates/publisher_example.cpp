// ============================================
// C++ ROS2 Publisher 示例 (rclcpp)
// ============================================
// 功能: 定时发布 std_msgs/String 类型消息
// 用法: 参考此代码在现有节点中添加 Publisher
// ============================================

#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/string.hpp>

using namespace std::chrono_literals;

class PublisherExample : public rclcpp::Node
{
public:
  PublisherExample()
  : Node("publisher_example"), count_(0)
  {
    // 创建 Publisher
    // 参数: topic名称, QoS队列深度
    publisher_ = this->create_publisher<std_msgs::msg::String>("chatter", 10);

    // 创建定时器，每500ms发布一次消息
    timer_ = this->create_wall_timer(
      500ms, std::bind(&PublisherExample::timer_callback, this));

    RCLCPP_INFO(this->get_logger(), "Publisher 已启动，发布话题: /chatter");
  }

private:
  void timer_callback()
  {
    // 创建消息
    auto message = std_msgs::msg::String();
    message.data = "Hello ROS2! Count: " + std::to_string(count_++);

    // 发布消息
    publisher_->publish(message);

    RCLCPP_INFO(this->get_logger(), "发布: '%s'", message.data.c_str());
  }

  // Publisher 成员变量
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  // 定时器成员变量
  rclcpp::TimerBase::SharedPtr timer_;
  // 计数器
  size_t count_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<PublisherExample>());
  rclcpp::shutdown();
  return 0;
}
