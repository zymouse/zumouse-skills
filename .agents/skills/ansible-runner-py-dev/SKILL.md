---
name: ansible-runner-py-dev
description: Ansible Runner Python3 开发指南。Use when user needs to programmatically execute Ansible playbooks, ad-hoc commands, or interact with Ansible via Python API, including running playbooks, modules, handling events, managing artifacts, execution environments, remote job execution, or integrating Ansible into Python applications.
---

# Ansible Runner Python3 开发指南

Ansible Runner 是一个用于以编程方式执行 Ansible 的 Python 库（>=3.10）和运行时工具。它提供了一个稳定且一致的接口抽象层，使得 Ansible 可以被嵌入到其他系统中。

## 安装

```bash
pip install ansible-runner
```

## 核心概念

### 私有数据目录结构

```
private_data_dir/
├── env/              # 环境配置
│   ├── envvars      # 环境变量
│   ├── extravars    # 额外变量 (-e)
│   ├── passwords    # 密码自动响应
│   ├── settings     # Runner 配置
│   └── ssh_key      # SSH 私钥
├── inventory/       # 主机清单
├── project/         # Playbook 和 Roles
└── artifacts/       # 执行结果（自动生成）
```

详细配置参考: [references/configuration.md](references/configuration.md)

## 快速开始

### 运行 Playbook

```python
import ansible_runner

result = ansible_runner.run(
    private_data_dir='/tmp/demo',
    playbook='site.yml'
)

print(f"状态: {result.status}")  # successful / failed / timeout / canceled
print(f"返回码: {result.rc}")    # 0 = 成功
```

### 异步执行

```python
import time

thread, runner = ansible_runner.run_async(
    private_data_dir='/tmp/demo',
    playbook='deploy.yml'
)

while runner.status not in ['successful', 'failed', 'timeout', 'canceled']:
    print(f"状态: {runner.status}")
    time.sleep(0.5)

print(f"返回码: {runner.rc}")
```

### 执行 Ansible 模块 (Ad-hoc)

```python
result = ansible_runner.run(
    private_data_dir='/tmp/demo',
    host_pattern='webservers',
    module='shell',
    module_args='uptime'
)
```

### 运行 Role

```python
result = ansible_runner.run(
    private_data_dir='/tmp/demo',
    role='common',
    role_vars={'ntp_server': 'pool.ntp.org'}
)
```

## Python API 接口

### 主要接口函数

| 函数 | 说明 |
|-----|------|
| `run()` | 同步执行 Playbook/模块/Role |
| `run_async()` | 异步执行 |
| `run_command()` | 执行任意命令 |
| `run_command_async()` | 异步执行命令 |
| `get_plugin_docs()` | 获取模块文档 |
| `get_plugin_list()` | 获取插件列表 |
| `get_inventory()` | 获取清单信息 |
| `get_ansible_config()` | 获取 Ansible 配置 |
| `get_role_list()` | 获取 Role 列表 |
| `get_role_argspec()` | 获取 Role 参数规范 |

### Runner 对象

```python
result = ansible_runner.run(...)

# 基本属性
result.rc       # 返回码 (int)
result.status   # 状态 (str)

# 输出访问
with result.stdout as f:
    print(f.read())

# 事件遍历
for event in result.events:
    print(event['event'])

# 获取统计
print(result.stats)

# 获取主机 facts
facts = result.get_fact_cache(hostname='web1')
```

## 回调函数

### 事件处理器

```python
def event_handler(event_data):
    """返回 True 保留事件，False 丢弃"""
    event = event_data.get('event', '')
    if event == 'runner_on_ok':
        host = event_data['event_data']['host']
        task = event_data['event_data']['task']
        print(f"[OK] {host}: {task}")
    return True

result = ansible_runner.run(
    private_data_dir='/tmp/demo',
    playbook='test.yml',
    event_handler=event_handler
)
```

### 状态处理器

```python
def status_handler(status_data, runner_config):
    status = status_data['status']  # starting / running / successful / failed / canceled / timeout
    print(f"状态变更: {status}")

result = ansible_runner.run(..., status_handler=status_handler)
```

### 取消回调

```python
cancel_requested = False

def cancel_callback():
    """返回 True 取消任务"""
    return cancel_requested

result = ansible_runner.run(..., cancel_callback=cancel_callback)
```

## 容器执行环境

```python
result = ansible_runner.run(
    private_data_dir='/tmp/demo',
    playbook='site.yml',
    process_isolation=True,
    container_image='quay.io/ansible/ansible-runner:latest',
    container_volume_mounts=[
        '/host/data:/container/data:Z',
        '/home/user/.ssh:/root/.ssh:ro'
    ]
)
```

## 远程作业执行

支持 transmit / worker / process 三阶段模式（用于 Receptor）：

```python
# 打包作业
result = ansible_runner.run(
    private_data_dir='/tmp/demo',
    playbook='test.yml',
    streamer='transmit'
)

# 执行作业
result = ansible_runner.run(streamer='worker')

# 处理结果
result = ansible_runner.run(
    private_data_dir='/tmp/demo',
    streamer='process',
    ident='job-001'
)
```

## 事件结构

常见事件类型:

| 事件 | 说明 |
|-----|------|
| `playbook_on_start` | Playbook 开始 |
| `playbook_on_task_start` | 任务开始 |
| `runner_on_ok` | 任务成功 |
| `runner_on_failed` | 任务失败 |
| `runner_on_unreachable` | 主机不可达 |
| `runner_on_skipped` | 任务跳过 |
| `playbook_on_stats` | 执行统计 |

详细事件结构参考: [references/events.md](references/events.md)

## 完整示例

### 实时监控与报告

```python
import ansible_runner

class PlaybookMonitor:
    def __init__(self):
        self.results = []
    
    def event_handler(self, event_data):
        event = event_data.get('event', '')
        if event == 'runner_on_ok':
            data = event_data['event_data']
            print(f"✓ {data['host']}: {data['task']}")
        elif event == 'runner_on_failed':
            data = event_data['event_data']
            print(f"✗ {data['host']}: {data['task']} FAILED")
        return True

monitor = PlaybookMonitor()
result = ansible_runner.run(
    private_data_dir='/tmp/demo',
    playbook='site.yml',
    event_handler=monitor.event_handler
)
print(f"最终状态: {result.status}")
```

更多完整示例参考: [references/examples.md](references/examples.md)

## 注意事项

1. **路径**: 尽量使用绝对路径，相对路径是相对于 `project/` 目录的
2. **资源清理**: 定期清理 `artifacts/` 目录以避免磁盘空间问题
3. **并发**: 使用 `run_async()` + 线程池控制并发执行
4. **错误处理**: 始终检查 `result.status` 和 `result.rc`
5. **SSH 密钥**: 使用 `env/ssh_key` 文件时，Runner 会自动使用 ssh-agent

## 参考文档

- [配置详解](references/configuration.md) - 目录结构、配置文件、API 参数
- [事件结构](references/events.md) - 事件字段、类型、处理示例
- [完整示例](references/examples.md) - 监控、动态环境、批量执行、容器、远程作业
