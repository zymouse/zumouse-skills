// 标准节点框架 - 继承Node基类
#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/string.hpp>

class MinimalPublisher : public rclcpp::Node {
public:
    explicit MinimalPublisher(const rclcpp::NodeOptions &options) 
        : Node("minimal_publisher", options), count_(0) {
        
        // 参数声明（必须在构造函数中）
        this->declare_parameter("publish_rate", 1.0);
        double rate = this->get_parameter("publish_rate").as_double();
        
        // QoS配置（显式指定，不默认）
        rclcpp::QoS qos(10).reliable().transient_local();
        
        pub_ = this->create_publisher<std_msgs::msg::String>("topic", qos);
        timer_ = this->create_wall_timer(
            std::chrono::duration<double>(1.0/rate),
            std::bind(&MinimalPublisher::timer_callback, this));
    }

private:
    void timer_callback() {
        auto msg = std_msgs::msg::String();
        msg.data = "Hello ROS2: " + std::to_string(count_++);
        pub_->publish(msg);
        RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", msg.data.c_str());
    }
    
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr pub_;
    rclcpp::TimerBase::SharedPtr timer_;
    size_t count_;
};

// 现代入口点（简洁版）
#include <rclcpp_components/register_node_macro.hpp>
RCLCPP_COMPONENTS_REGISTER_NODE(MinimalPublisher)