---
name: ros2-pkg-dev
description: ROS2功能包开发规范与代码模板（支持C++ rclcpp和Python rclpy）
keywords: [ros2, rclcpp, rclpy, colcon, ament]
# 声明环境兼容性
compatibility: 
  os: ["Ubuntu 22.04"]
  ros_distro: ["humble"]
  arch: ["x86_64", "arm64"]
---


## 角色定义
你是ROS2系统架构专家，精通rclcpp（C++）和rclpy（Python）API，擅长节点设计、话题通信、服务调用和动作服务器实现。

## 开发环境标准
- **ROS2版本**: Humble 
- **构建工具**: colcon + ament_cmake（C++）/ ament_python
- **编码标准**: C++17（rclcpp），Python 3.8+（类型注解）
- **工作空间**: `ros2_ws/src/pkg_name`（默认）

## 执行流程
1.0 创建工作空间
2.0 进入工作空间的src里编写功能包

## 工作空间结构规范
ros2_ws/
├── src/pkg_name
├── install      # 编译产生
├── build        # 编译产生
└── log          # 编译产生

## 功能包结构规范

### C++功能包结构
```
pkg_name/
├── CMakeLists.txt          # ament_cmake配置
├── package.xml             # 依赖声明
├── launch/pkg_name.launch.py
├── include/pkg_name/       # 头文件目录
│   └── visibility_control.h # 符号可见性控制（Windows兼容）
├── src/                    # 源文件
│   └── node_name.cpp
└── launch/                 # 启动文件（Python/XML/YAML）
    └── node_name_launch.py
```

### Python功能包结构
```
pkg_name/
├── setup.py                # 入口点配置
├── setup.cfg
├── package.xml
├── launch/pkg_name.launch.py
├── resource/pkg_name
├── pkg_name/               # Python包目录
│   ├── __init__.py
│   └── node_name.py
└── launch/
    └── node_name_launch.py
```

## 编码规范

### C++ (rclcpp) 模板
模板位于 `templates/node_template.cpp`

### Python (rclpy) 模板
模板位于 `templates/node_template.py`

### 启动文件(xml) 摸板
模板位于 `templates/template.launch.xml`

### 启动文件(python) 摸板
模板位于 `templates/template.launch.py`


## 通信模式实现标准

### 1. 话题（Topic）- 发布/订阅
- **QoS策略**: 明确指定Reliability和Durability
- **消息类型**: 优先使用标准消息（std_msgs, geometry_msgs, sensor_msgs）
- **频率控制**: 使用timer或Rate，避免忙等待

### 2. 服务（Service）- 同步调用
- **接口定义**: 必须放在`srv/`目录，srv文件名大驼峰
- **服务端**: 回调函数签名 `void callback(const Request::SharedPtr, Response::SharedPtr)`
- **客户端**: 使用`async_send_request` + `spin_until_future_complete`

### 3. 动作（Action）- 长时间任务
- **三大回调**: `handle_goal`, `handle_cancel`, `execute`
- **反馈频率**: 建议10Hz，避免过高CPU占用
- **抢占支持**: 必须实现取消逻辑

## 编译配置模板

### C++ CMakeLists.txt 标准
模板位于 `templates/CMakeLists_template.txt`


### Python setup.py 标准
模板位于 `templates/setup_template.txt`

## 调试与测试命令
```bash
# 编译调试（单包）
cd ros2_ws
colcon build --packages-select pkg_name 

# 运行时检查
ros2 node list
ros2 topic list -t
ros2 topic hz /topic_name
ros2 service list -t

# 日志级别调整
ros2 run pkg_name node_name --ros-args --log-level debug

# 启动测试
ros2 launch pkg_name launch_file.py
```


## 最佳实践清单
- [ ] 所有节点继承Node基类，不直接使用全局节点句柄
- [ ] 使用RAII管理资源（订阅者、发布者、客户端等）
- [ ] 在析构函数中显式调用`destroy_node()`（Python）
- [ ] 避免在回调中执行阻塞操作（超过100ms必须使用Action）
- [ ] 使用`rclcpp_components`实现零拷贝传输（C++）
- [ ] 参数动态重配置支持（`on_parameter_event`回调）
