# zumouse个人使用的AI技能库

本仓库包含用于增强Kimi Code CLI能力的各种技能(Skill)。

## 技能目录

| 技能名称 | 说明 | 适用场景 |
|---------|------|---------|
| [aliyun-oss-dev](.agents/skills/aliyun-oss-dev/) | 阿里云OSS开发指南 | 使用Go或Python SDK进行阿里云对象存储服务开发，包括bucket操作、文件上传下载、分片上传、预签名URL、客户端加密等 |
| [dingtalk-yida-form](.agents/skills/dingtalk-yida-form/) | 钉钉宜搭表单操作 | 通过Go或Python API与钉钉宜搭云表单实例交互，包括增删查改、批量操作、查询表单实例、更新子表等 |
| [kimi-agent-sdk-go](.agents/skills/kimi-agent-sdk-go/) | Kimi Agent SDK for Go | 使用Go开发基于Kimi Agent的应用程序，包括创建会话、发送prompt、处理响应、外部工具、审批请求、thinking模式、turn取消、用量追踪等 |
| [ros2-pkg-dev](.agents/skills/ros2-pkg-dev/) | ROS2功能包开发 | ROS2功能包开发规范与代码模板，支持C++ rclcpp和Python rclpy |
| [feishu-bot-dev](.agents/skills/feishu-bot-dev/) | 飞书机器人开发指南 | 使用Go SDK开发飞书机器人，包括认证、消息发送、回调处理、群聊管理、文件上传下载、卡片消息等 |
| [rustfs-go-dev](.agents/skills/rustfs-go-dev/) | 本地分布式存储 | 使用Go SDK开发本地存储工具 |

## 技能安装

将`.skill`文件复制到Kimi Code CLI的技能目录：

```bash
# 用户级技能目录（推荐）
~/.config/agents/skills/

# 或项目级技能目录
./.agents/skills/
```

## 技能开发

参考 [skill-creator](.agents/skills/skill-creator/SKILL.md) 了解如何创建和打包技能。

## 部署脚本

使用 `deploy_skills.sh` 脚本将技能部署到指定目录：

```bash
./deploy_skills.sh
```
