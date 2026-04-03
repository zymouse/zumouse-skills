# Ansible Runner 事件结构详解

## 标准事件字段

```json
{
  "uuid": "8c164553-8573-b1e0-76e1-000000000008",
  "parent_uuid": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "counter": 5,
  "stdout": "\r\nTASK [debug] *******************************************************************",
  "start_line": 5,
  "end_line": 7,
  "event": "playbook_on_task_start",
  "event_data": {
    "playbook": "test.yml",
    "playbook_uuid": "34437b34-addd-45ae-819a-4d8c9711e191",
    "play": "all",
    "play_uuid": "8c164553-8573-b1e0-76e1-000000000006",
    "play_pattern": "all",
    "task": "debug",
    "task_uuid": "8c164553-8573-b1e0-76e1-000000000008",
    "task_action": "debug",
    "task_path": "/path/to/test.yml:3",
    "task_args": "msg=Test!",
    "name": "debug",
    "is_conditional": false,
    "pid": 10640,
    "host": "localhost",
    "res": {"msg": "Test!", "changed": false}
  },
  "pid": 10640,
  "created": "2018-06-07T14:54:58.410605"
}
```

## 通用字段说明

| 字段 | 类型 | 说明 |
|-----|------|------|
| `uuid` | string | 事件唯一标识 |
| `parent_uuid` | string | 父事件标识 |
| `counter` | int | 事件序号 |
| `stdout` | string | 标准输出行 |
| `start_line` | int | stdout 起始行号 |
| `end_line` | int | stdout 结束行号 |
| `event` | string | 事件类型 |
| `event_data` | dict | 事件详细数据 |
| `pid` | int | 进程ID |
| `created` | string | ISO8601 时间戳 |

## 事件类型速查表

### Playbook 级别事件

| 事件类型 | 触发时机 | event_data 关键字段 |
|---------|---------|-------------------|
| `playbook_on_start` | Playbook 开始 | `playbook`, `playbook_uuid` |
| `playbook_on_vars_prompt` | 变量提示 | - |
| `playbook_on_notify` | Handler 通知 | `handler`, `host` |
| `playbook_on_no_hosts_matched` | 无匹配主机 | `play_pattern` |
| `playbook_on_no_hosts_remaining` | 无可用主机 | - |
| `playbook_on_play_start` | Play 开始 | `play`, `play_pattern`, `play_uuid` |
| `playbook_on_import_for_host` | 主机导入 | `host`, `filename` |
| `playbook_on_not_import_for_host` | 主机不导入 | `host`, `filename` |
| `playbook_on_stats` | Playbook 统计 | `ok`, `changed`, `failures`, `unreachable`, `skipped` |

### Task 级别事件

| 事件类型 | 触发时机 | event_data 关键字段 |
|---------|---------|-------------------|
| `playbook_on_task_start` | 任务开始 | `task`, `task_action`, `name`, `task_uuid` |
| `playbook_on_task_start` | Handler 任务开始 | `task`, `is_handler: true` |
| `playbook_on_cleanup_task_start` | 清理任务开始 | `task` |

### Runner 级别事件（主机任务执行）

| 事件类型 | 触发时机 | event_data 关键字段 |
|---------|---------|-------------------|
| `runner_on_ok` | 任务成功 | `host`, `task`, `res`, `duration` |
| `runner_on_failed` | 任务失败 | `host`, `task`, `res`, `exception` |
| `runner_on_skipped` | 任务跳过 | `host`, `task` |
| `runner_on_unreachable` | 主机不可达 | `host`, `task`, `res` |
| `runner_on_no_hosts` | 无匹配主机 | - |
| `runner_on_async_poll` | 异步任务轮询 | `host`, `task`, `jid` |
| `runner_on_async_ok` | 异步任务成功 | `host`, `task`, `jid` |
| `runner_on_async_failed` | 异步任务失败 | `host`, `task`, `jid` |
| `runner_on_file_diff` | 文件差异 | `host`, `diff` |

### 重试和包含事件

| 事件类型 | 触发时机 |
|---------|---------|
| `runner_retry_task` | 任务重试 |
| `runner_item_on_ok` | with_items 单项成功 |
| `runner_item_on_failed` | with_items 单项失败 |
| `runner_item_on_skipped` | with_items 单项跳过 |

## 统计数据结构

`playbook_on_stats` 事件的 event_data:

```json
{
  "playbook": "site.yml",
  "playbook_uuid": "34437b34-addd-45ae-819a-4d8c9711e191",
  "changed": {
    "webserver1": 3,
    "webserver2": 1
  },
  "dark": {},
  "failures": {
    "dbserver1": 1
  },
  "ok": {
    "webserver1": 15,
    "webserver2": 12,
    "dbserver1": 8
  },
  "processed": {
    "webserver1": 1,
    "webserver2": 1,
    "dbserver1": 1
  },
  "rescued": {},
  "skipped": {
    "webserver1": 2
  },
  "artifact_data": {},
  "pid": 12345
}
```

## 结果数据结构 (res)

`runner_on_ok` 和 `runner_on_failed` 中的 res 字段：

### 成功结果示例

```json
{
  "msg": "Hello World",
  "changed": false,
  "_ansible_verbose_always": true,
  "_ansible_no_log": false
}
```

### 失败结果示例

```json
{
  "msg": "Failed to connect to the host via ssh",
  "unreachable": true,
  "changed": false
}
```

### 命令结果示例

```json
{
  "changed": true,
  "cmd": ["uptime"],
  "delta": "0:00:00.123456",
  "end": "2023-01-01 12:00:00.123456",
  "rc": 0,
  "start": "2023-01-01 12:00:00.000000",
  "stderr": "",
  "stderr_lines": [],
  "stdout": "12:00:00 up 5 days, 3:00, 1 user, load average: 0.50, 0.30, 0.25",
  "stdout_lines": ["12:00:00 up 5 days, 3:00, 1 user, load average: 0.50, 0.30, 0.25"]
}
```

## 事件处理示例

### 过滤特定事件

```python
def event_handler(event_data):
    event = event_data.get('event', '')
    
    # 只处理任务完成事件
    if event in ['runner_on_ok', 'runner_on_failed', 'runner_on_skipped']:
        host = event_data['event_data'].get('host')
        task = event_data['event_data'].get('task')
        status = event.split('_')[-1]
        print(f"[{status.upper()}] {host}: {task}")
    
    return True
```

### 收集统计信息

```python
def collect_stats(event_data):
    event = event_data.get('event', '')
    
    if event == 'playbook_on_stats':
        stats = event_data['event_data']
        print("执行统计:")
        print(f"  成功: {stats.get('ok', {})}")
        print(f"  变更: {stats.get('changed', {})}")
        print(f"  失败: {stats.get('failures', {})}")
        print(f"  不可达: {stats.get('dark', {})}")
    
    return True
```

### 实时进度跟踪

```python
class ProgressTracker:
    def __init__(self, total_tasks):
        self.total_tasks = total_tasks
        self.completed = 0
    
    def event_handler(self, event_data):
        event = event_data.get('event', '')
        
        if event in ['runner_on_ok', 'runner_on_failed', 'runner_on_skipped']:
            self.completed += 1
            percent = (self.completed / self.total_tasks) * 100
            print(f"\r进度: {percent:.1f}% ({self.completed}/{self.total_tasks})", end='')
        
        return True
```
