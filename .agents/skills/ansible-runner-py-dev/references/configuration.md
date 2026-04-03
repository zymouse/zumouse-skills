# Ansible Runner 配置参考

## 目录结构

```
.
├── env/                    # 环境配置
│   ├── envvars            # 环境变量 (YAML/JSON)
│   ├── extravars          # 额外变量，传递给 Ansible -e (YAML/JSON)
│   ├── passwords          # 密码配置，正则匹配提示
│   ├── cmdline            # 命令行参数字符串
│   ├── settings           # Runner 行为设置
│   └── ssh_key            # SSH 私钥
├── inventory/             # 主机清单文件或脚本
│   └── hosts
├── project/               # Playbook 根目录（工作目录）
│   ├── test.yml
│   └── roles/
└── artifacts/             # 执行结果（自动生成）
    └── <uuid>/            # 每次执行的标识目录
        ├── job_events/    # 结构化事件数据 (JSON)
        ├── fact_cache/    # 主机 facts 缓存
        ├── stdout         # 原始标准输出
        ├── stderr         # 标准错误（subprocess 模式）
        ├── rc             # 返回码文件
        └── status         # 状态文件
```

## 环境配置文件

### env/envvars - 运行时环境变量

定义传递给 Ansible 进程的环境变量。

```yaml
---
TESTVAR: exampleval
ANSIBLE_STDOUT_CALLBACK: json
ANSIBLE_RETRY_FILES_ENABLED: "false"
ANSIBLE_HOST_KEY_CHECKING: "false"
ANSIBLE_PIPELINING: "true"
```

### env/extravars - 额外变量

传递给 Ansible 的额外变量，优先级最高（相当于 -e 参数）。

```yaml
---
ansible_connection: local
app_version: "1.2.3"
deploy_environment: production
users:
  - name: alice
    role: admin
  - name: bob
    role: user
```

### env/passwords - 自动响应密码提示

使用正则表达式匹配 Ansible 提示，自动输入密码。

```yaml
---
"^SSH password:\s*?$": "ssh_password"
"^BECOME password.*:\s*?$": "sudo_password"
"^Vault password:\s*?$": "vault_password"
"^Enter passphrase for key.*:\s*?$": "key_passphrase"
```

### env/cmdline - 命令行参数

传递给 Ansible 的额外命令行参数（字符串格式）。

```
--tags deploy,config --skip-tags test -u ansible --become --become-user root
```

注意: 此方法设置的参数优先级低于 Runner 直接设置的参数。

### env/ssh_key - SSH 私钥

包含 SSH 私钥内容。Runner 检测到私钥时会自动使用 ssh-agent 包装调用。

## Settings 配置 (env/settings)

### 超时设置

```yaml
---
idle_timeout: 600          # 无输出超时（秒），默认600，0表示禁用
job_timeout: 3600          # 最大运行时间（秒），默认3600，0表示禁用
pexpect_timeout: 10        # pexpect 等待输入超时，默认10
pexpect_use_poll: true     # 使用 poll() 替代 select()，默认true
                          # poll() 支持超过1024个文件描述符
```

### 输出控制

```yaml
---
suppress_output_file: false      # 禁止写入 stdout/stderr 文件，默认false
suppress_ansible_output: false   # 禁止屏幕输出，默认false
```

### Fact 缓存

```yaml
---
fact_cache: 'fact_cache'        # fact 缓存目录名，相对于 artifacts
fact_cache_type: 'jsonfile'     # 缓存类型，目前仅支持 jsonfile
```

### 进程隔离设置

```yaml
---
process_isolation: false                    # 启用进程隔离，默认false
process_isolation_executable: 'podman'      # 隔离工具: podman/docker/bwrap
process_isolation_path: '/tmp'              # 隔离进程的工作路径
process_isolation_hide_paths:               # 对 playbook 隐藏的路径
  - /etc/sensitive
  - /home/user/secrets
process_isolation_show_paths:               # 额外暴露的路径
  - /shared/data
process_isolation_ro_paths:                 # 以只读方式暴露的路径
  - /etc/ansible
  - /usr/share/ansible
```

### 容器配置

```yaml
---
container_image: 'quay.io/ansible/ansible-runner:latest'
container_options:
  - '--network=host'
  - '--privileged'
  - '--memory=2g'

container_volume_mounts:
  - '/host/data:/container/data:Z'           # 共享数据，Z标签用于SELinux
  - '/home/user/.ssh:/root/.ssh:ro'          # SSH 密钥只读挂载
  - '/etc/ssl/certs:/etc/ssl/certs:ro'       # SSL 证书
```

### 私有镜像仓库认证

```yaml
---
container_auth_data:
  host: "registry.example.com"
  username: "user"
  password: "pass"
  verify_ssl: true
```

安全提示: 此方法会将敏感信息写入文件。在 AWX 中，这些信息会被写入临时 JSON 文件，作业完成后自动删除。

## 完整 Settings 示例

```yaml
---
# 超时设置
idle_timeout: 600
job_timeout: 3600
pexpect_timeout: 10
pexpect_use_poll: true

# 输出控制
suppress_output_file: false
suppress_ansible_output: false

# Fact 缓存
fact_cache: 'fact_cache'
fact_cache_type: 'jsonfile'

# 进程隔离
process_isolation: true
process_isolation_executable: 'podman'
process_isolation_path: '/tmp'
process_isolation_hide_paths:
  - /etc/sensitive
process_isolation_show_paths:
  - /shared/data
process_isolation_ro_paths:
  - /etc/ansible

# 容器配置
container_image: 'quay.io/ansible/ansible-runner:latest'
container_options:
  - '--network=host'
container_volume_mounts:
  - '/host/data:/container/data:Z'

# 容器认证
container_auth_data:
  host: "registry.example.com"
  username: "user"
  password: "pass"
  verify_ssl: true
```

## Python API 参数

### run() / run_async() 常用参数

| 参数 | 类型 | 说明 |
|-----|------|------|
| private_data_dir | str | 私有数据目录路径（必需） |
| playbook | str | Playbook 文件名（相对于 project/） |
| module | str | 模块名（用于 ad-hoc 执行） |
| module_args | str | 模块参数 |
| host_pattern | str | 主机模式（如 'all', 'webservers'） |
| inventory | list | 清单文件路径列表 |
| limit | str | 限制执行的主机 |
| tags | list/str | 执行带指定标签的任务 |
| skip_tags | list/str | 跳过带指定标签的任务 |
| extravars | dict | 额外变量 |
| verbosity | int | 详细程度（0-4，对应 -v 到 -vvvv） |
| quiet | bool | 抑制标准输出 |
| json_mode | bool | 以 JSON 模式运行 |
| ident | str | 执行标识（用于 artifacts 子目录） |
| timeout | int | 作业超时（秒） |

### 进程隔离参数

| 参数 | 类型 | 说明 |
|-----|------|------|
| process_isolation | bool | 启用进程隔离 |
| process_isolation_executable | str | 隔离工具 |
| process_isolation_path | str | 隔离路径 |
| container_image | str | 容器镜像 |
| container_options | list | 容器选项 |
| container_volume_mounts | list | 卷挂载 |
| container_auth_data | dict | 镜像仓库认证 |

### 回调函数参数

| 参数 | 类型 | 说明 |
|-----|------|------|
| event_handler | callable | 事件处理函数 |
| status_handler | callable | 状态变更处理函数 |
| cancel_callback | callable | 取消检查回调 |
| finished_callback | callable | 完成回调 |
| artifacts_handler | callable | 制品处理回调 |
