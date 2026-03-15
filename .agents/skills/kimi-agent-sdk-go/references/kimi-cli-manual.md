# Kimi CLI 使用文档

## 目录
1. [简介](#简介)
2. [全局选项](#全局选项)
3. [认证命令](#认证命令)
4. [运行模式命令](#运行模式命令)
5. [信息查询命令](#信息查询命令)
6. [MCP 管理命令](#mcp-管理命令)
7. [配置优先级](#配置优先级)
8. [使用示例](#使用示例)

---

## 简介

`kimi-cli` 是 Kimi 的命令行工具，提供 AI 助手功能，支持交互式对话、TUI 界面、Web 界面以及 MCP 服务器管理。

**基本语法**：
```bash
kimi-cli [OPTIONS] COMMAND [ARGS...]
```

---

## 全局选项

| 选项 | 简写 | 参数 | 说明 | 默认值 |
|------|------|------|------|--------|
| `--version` | `-V` | - | 显示版本并退出 | - |
| `--verbose` | - | - | 打印详细信息 | no |
| `--debug` | - | - | 记录调试信息 | no |
| `--work-dir` | `-w` | `DIRECTORY` | 工作目录 | 当前目录 |
| `--session` | `-S` | `TEXT` | 会话 ID（恢复用）| 新会话 |
| `--continue` | `-C` | - | 继续上一个会话 | no |
| `--config` | - | `TEXT` | 配置 TOML/JSON 字符串 | none |
| `--config-file` | - | `FILE` | 配置文件路径 | `~/.kimi/config.toml` |
| `--model` | `-m` | `TEXT` | LLM 模型 | 配置文件默认 |
| `--thinking` / `--no-thinking` | - | - | 启用/禁用思考模式 | 配置文件默认 |
| `--yolo`, `--yes`, `--auto-approve` | `-y` | - | 自动批准所有操作 | no |
| `--prompt`, `--command` | `-p`, `-c` | `TEXT` | 用户提示词 | 交互式输入 |
| `--print` | - | - | 打印模式（非交互式）| - |
| `--input-format` | - | `[text\|stream-json]` | 输入格式 | text |
| `--output-format` | - | `[text\|stream-json]` | 输出格式 | text |
| `--final-message-only` | - | - | 只打印最终消息 | - |
| `--quiet` | - | - | 安静模式 | - |
| `--agent` | - | `[default\|okabe]` | 内置 Agent 规格 | default |
| `--agent-file` | - | `FILE` | 自定义 Agent 规格文件 | - |
| `--mcp-config-file` | - | `FILE` | MCP 配置文件（可多次指定）| none |
| `--mcp-config` | - | `TEXT` | MCP 配置 JSON（可多次指定）| none |
| `--skills-dir` | - | `DIRECTORY` | 技能目录路径（覆盖自动发现）| - |
| `--max-steps-per-turn` | - | `INTEGER` | 每轮最大步数 | 来自配置 |
| `--max-retries-per-step` | - | `INTEGER` | 每步最大重试次数 | 来自配置 |
| `--max-ralph-iterations` | - | `INTEGER` | Ralph 模式额外迭代次数 | 来自配置 |
| `--help` | `-h` | - | 显示帮助 | - |

---

## 认证命令

### login - 登录 Kimi 账号

```bash
kimi-cli login [OPTIONS]
```

| 选项 | 说明 |
|------|------|
| `--json` | 以 JSON 行格式输出 OAuth 事件 |
| `--help`, `-h` | 显示帮助 |

**示例**：
```bash
# 交互式登录
kimi-cli login

# JSON 输出模式
kimi-cli login --json
```

---

### logout - 登出 Kimi 账号

```bash
kimi-cli logout [OPTIONS]
```

| 选项 | 说明 |
|------|------|
| `--json` | 以 JSON 行格式输出 OAuth 事件 |
| `--help`, `-h` | 显示帮助 |

**示例**：
```bash
kimi-cli logout
```

---

## 运行模式命令

### term - 运行 Toad TUI（终端界面）

```bash
kimi-cli term [OPTIONS]
```

| 选项 | 说明 |
|------|------|
| `--help`, `-h` | 显示帮助 |

**说明**：启动基于 ACP 服务器的 Toad TUI 界面。

**示例**：
```bash
kimi-cli term
```

---

### acp - 运行 ACP 服务器

```bash
kimi-cli acp [OPTIONS]
```

| 选项 | 说明 |
|------|------|
| `--help`, `-h` | 显示帮助 |

**说明**：运行 Kimi Code CLI 的 ACP（Agent Communication Protocol）服务器。

**示例**：
```bash
kimi-cli acp
```

---

### web - 运行 Web 界面

```bash
kimi-cli web [OPTIONS]
```

| 选项 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--host` | `-h` | 绑定主机 | `127.0.0.1` |
| `--port` | `-p` | 绑定端口 | `5494` |
| `--reload` | - | 启用自动重载 | - |
| `--open` / `--no-open` | - | 自动打开浏览器 | `open` |
| `--help` | - | 显示帮助 | - |

**示例**：
```bash
# 默认启动（127.0.0.1:5494，自动打开浏览器）
kimi-cli web

# 指定端口
kimi-cli web --port 8080

# 允许外部访问
kimi-cli web --host 0.0.0.0

# 不自动打开浏览器
kimi-cli web --no-open

# 开发模式（自动重载）
kimi-cli web --reload
```

---

## 信息查询命令

### info - 显示版本和协议信息

```bash
kimi-cli info [OPTIONS]
```

| 选项 | 说明 |
|------|------|
| `--json` | 以 JSON 格式输出信息 |
| `--help`, `-h` | 显示帮助 |

**示例**：
```bash
# 文本输出
kimi-cli info

# JSON 输出
kimi-cli info --json
```

**输出示例**：
```
kimi-cli version: 1.5
agent spec versions: 1
wire protocol: 1.1
python version: 3.13.11
```

---

## MCP 管理命令

> MCP（Model Context Protocol）用于管理外部工具服务器。

### mcp 子命令概览

| 子命令 | 说明 |
|--------|------|
| `add` | 添加 MCP 服务器 |
| `remove` | 移除 MCP 服务器 |
| `list` | 列出所有 MCP 服务器 |
| `auth` | 为支持 OAuth 的 MCP 服务器授权 |
| `reset-auth` | 重置 MCP 服务器的 OAuth 授权 |
| `test` | 测试 MCP 服务器连接并列出可用工具 |

---

### mcp add - 添加 MCP 服务器

```bash
kimi-cli mcp add [OPTIONS] NAME [TARGET_OR_COMMAND...]
```

| 参数 | 说明 |
|------|------|
| `NAME` (必填) | MCP 服务器名称 |
| `TARGET_OR_COMMAND` | HTTP: 服务器 URL；Stdio: 运行命令（用 `--` 前缀）|

| 选项 | 简写 | 说明 |
|------|------|------|
| `--transport` | `-t` | 传输类型：`stdio` 或 `http`（默认：`stdio`）|
| `--env` | `-e` | 环境变量（格式：`KEY=VALUE`，可多次指定）|
| `--header` | `-H` | HTTP 头（格式：`KEY:VALUE`，可多次指定）|
| `--auth` | `-a` | 授权类型（如 `oauth`）|
| `--help` | `-h` | 显示帮助 |

**示例**：
```bash
# 添加 Streamable HTTP 服务器
kimi mcp add --transport http context7 https://mcp.context7.com/mcp \
  --header "CONTEXT7_API_KEY: ctx7sk-your-key"

# 添加带 OAuth 的 HTTP 服务器
kimi mcp add --transport http --auth oauth linear https://mcp.linear.app/mcp

# 添加 stdio 服务器
kimi mcp add --transport stdio chrome-devtools -- npx chrome-devtools-mcp@latest
```

---

### mcp remove - 移除 MCP 服务器

```bash
kimi-cli mcp remove [OPTIONS] NAME
```

| 参数 | 说明 |
|------|------|
| `NAME` (必填) | 要移除的 MCP 服务器名称 |

**示例**：
```bash
kimi mcp remove context7
```

---

### mcp list - 列出所有 MCP 服务器

```bash
kimi-cli mcp list [OPTIONS]
```

**示例**：
```bash
kimi mcp list
```

---

### mcp auth - OAuth 授权

```bash
kimi-cli mcp auth [OPTIONS] NAME
```

| 参数 | 说明 |
|------|------|
| `NAME` (必填) | 要授权的 MCP 服务器名称 |

**示例**：
```bash
kimi mcp auth linear
```

---

### mcp reset-auth - 重置 OAuth 授权

```bash
kimi-cli mcp reset-auth [OPTIONS] NAME
```

| 参数 | 说明 |
|------|------|
| `NAME` (必填) | 要重置授权的 MCP 服务器名称 |

**示例**：
```bash
kimi mcp reset-auth linear
```

---

### mcp test - 测试 MCP 服务器连接

```bash
kimi-cli mcp test [OPTIONS] NAME
```

| 参数 | 说明 |
|------|------|
| `NAME` (必填) | 要测试的 MCP 服务器名称 |

**示例**：
```bash
kimi mcp test context7
```

---

## 配置优先级

当同一设置在多处指定时，优先级从高到低：

1. **命令行选项**（如 `--model`, `--skills-dir`）
2. **环境变量**（`KIMI_API_KEY`, `KIMI_BASE_URL`, `KIMI_MODEL_NAME`）
3. **配置文件**（`~/.kimi/config.toml`）

---

## 使用示例

### 首次使用

```bash
# 1. 登录
kimi-cli login

# 2. 查看版本信息
kimi-cli info

# 3. 启动交互式对话
kimi-cli
```

### 日常开发

```bash
# 在指定目录运行，自动批准所有操作
kimi-cli --work-dir /path/to/project --yolo

# 使用特定模型，启用思考模式
kimi-cli --model kimi-k2-thinking-turbo --thinking

# 执行单条命令（非交互式）
kimi-cli --print --yolo -p "分析这个项目的代码结构"
```

### 添加外部工具（MCP）

```bash
# 添加 Context7 文档搜索工具
kimi mcp add --transport http context7 \
  https://mcp.context7.com/mcp \
  --header "CONTEXT7_API_KEY: your-api-key"

# 测试连接
kimi mcp test context7

# 查看已添加的工具
kimi mcp list
```

### 启动 Web IDE

```bash
# 本地开发
kimi-cli web

# 局域网共享（允许其他设备访问）
kimi-cli web --host 0.0.0.0 --port 8080 --no-open
```

### 恢复会话

```bash
# 继续上次的会话
kimi-cli --continue

# 或指定会话 ID
kimi-cli --session <session-id>
```

---

## 相关资源

- **文档**：https://moonshotai.github.io/kimi-cli/
- **LLM 友好版本**：https://moonshotai.github.io/kimi-cli/llms.txt
