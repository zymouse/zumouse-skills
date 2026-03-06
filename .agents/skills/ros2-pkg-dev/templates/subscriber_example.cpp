// ============================================
// C++ ROS2 Subscriber 示例 (rclcpp)
// ============================================
// 功能: 订阅 std_msgs/String 类型消息
// 用法: 参考此代码在现有节点中添加 Subscriber
// ============================================

#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/string.hpp>

class SubscriberExample : public rclcpp::Node
{
public:
  SubscriberExample()
  : Node("subscriber_example")
  {
    // 创建 Subscriber
    // 参数: topic名称, QoS队列深度, 回调函数
    subscription_ = this->create_subscription<std_msgs::msg::String>(
      "chatter", 10, std::bind(&SubscriberExample::topic_callback, this, std::placeholders::_1));

    RCLCPP_INFO(this->get_logger(), "Subscriber 已启动，订阅话题: /chatter");
  }

private:
  // 消息回调函数
  void topic_callback(const std_msgs::msg::String::SharedPtr msg)
  {
    RCLCPP_INFO(this->get_logger(), "收到消息: '%s'", msg->data.c_str());

    // 在这里添加你的业务逻辑
    process_message(msg->data);
  }

  // 业务处理函数示例
  void process_message(const std::string &data)
  {
    // 例如：解析消息内容、触发其他操作等
    RCLCPP_DEBUG(this->get_logger(), "处理消息: %s", data.c_str());
  }

  // Subscriber 成员变量
  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<SubscriberExample>());
  rclcpp::shutdown();
  return 0;
}
