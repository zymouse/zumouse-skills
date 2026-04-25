---
name: autoware-ota-release
description: >
  自动驾驶系统Autoware OTA发版工作流。用于执行ROS2工作空间的OTA版本发布，
  包括自动驾驶园区版本(test)和公开道路版本(release)。
  当用户说"开始发版工作流"、"OTA发版"、"发布autoware版本"、
  "请发版autoware:<name>/<YYMMDD>"，或要求执行编译发版工作流时触发。
  支持两种版本：test/<YYMMDD>(园区版本) 和 release/<YYMMDD>(公开道路版本)。
  需要区分主机架构(amd64/arm64)使用不同编译指令。
---

# Autoware OTA 发版工作流

## 触发指令解析

当用户说：
> 开始发版工作流：请发版autoware:`<name>/<YYMMDD>`，release note: `...`

解析规则：
- `<name>`: `test` 或 `release`
  - `test/<YYMMDD>` → 自动驾驶**园区版本**
  - `release/<YYMMDD>` → 自动驾驶**公开道路版本**
- `<YYMMDD>`: 日期格式，如 `20260424`
- `release note`: 版本更新内容，格式为 `1.xxx 2.xxx 3.xxx`，**可以为空**

## 工作空间路径

| 版本类型 | 分支前缀 | 工作空间路径 |
|---------|---------|------------|
| 园区版本 | `test/` | `~/pix/robobus/autoware-robobus.dev-master.test/` |
| 公开道路版本 | `release/` | `~/pix/robobus/autoware-robobus.dev-master/` |

## 工作流步骤（严格顺序执行）

**核心原则：每步必须验证成功后才能继续下一步。所有命令输出必须保存到日志文件。工作流开始后直接顺序执行各步骤，不需要在每步前询问用户确认。**

日志文件统一存放在固定目录 `~/pix/ros2log/ota_release_logs/$(date +%Y%m%d_%H%M%S)/` 中，命名格式：`step<N>_<操作名>.log`

工作流开始时先创建日志目录和任务总览日志：
```bash
export LOG_DIR=~/pix/ros2log/ota_release_logs/$(date +%Y%m%d_%H%M%S)
mkdir -p "$LOG_DIR"
cat > "$LOG_DIR/progress.log" << 'EOF'
========================================
OTA 发版工作流 - 任务情况总览
版本号: <name>/<YYMMDD>
工作空间: <路径>
日志目录: $LOG_DIR
========================================
step1:  等待执行
step2:  等待执行
step3:  等待执行
step4:  等待执行
step5:  等待执行
step6:  等待执行
step7:  等待执行
step8:  等待执行
step9:  等待执行
step10: 等待执行
step11: 等待执行
========================================
Token消耗记录:
  输入tokens: 0
  输出tokens: 0
  总tokens: 0
========================================
EOF
```

### Step 1: 创建OTA配置文件并上传

**主机名判断**：先检测当前主机名 `hostname`，根据主机名决定执行范围：

```bash
HOSTNAME=$(hostname)
```

- **若主机名为 `pixwork-workstation-chassis`**：执行全部3步（生成配置 → 上传配置 → 验证上传）
- **其他主机名**：**仅执行第3步验证上传**即可

---

**仅在 `pixwork-workstation-chassis` 主机上执行：**

1. **生成配置文件**:
   使用 skill 内置脚本（或直接用 `generate_ota_config.py`）：
   ```bash
   python3 .agents/skills/autoware-ota-release/scripts/generate_ota_config.py <test|release> <version_name> <description...>
   ```
   - 参数说明:
     - `<test|release>`: 版本类型，`test`(园区) 或 `release`(公开道路)
     - `<version_name>`: 如 `test/20260424` 或 `release/20260424`
     - `<description...>`: release note 内容，每条作为一个参数，如 `"1. 修复xxx" "2. 优化yyy"`
   - 示例:
     ```bash
     python3 .agents/skills/autoware-ota-release/scripts/generate_ota_config.py test test/20260424 "1. 解决变道取消导致的轨迹突变" "2. 优化尾部轨迹稳定性"
     ```
   - 脚本会输出生成的配置文件路径
   - **验证**: 检查返回路径是否存在

2. **上传配置**:
   `PixRover-Ota cfg_push` 会交互式要求输入 `y` 确认，使用以下方式自动确认：
   ```bash
   echo "y" | PixRover-Ota cfg_push <配置文件路径>
   ```
   或：
   ```bash
   yes | PixRover-Ota cfg_push <配置文件路径>
   ```

---

**所有主机均执行：**

3. **验证上传**:
   ```bash
   PixRover-Ota cfg_info
   ```
   - **验证**: 确认配置文件信息正确显示

### Step 2-9: 工作空间准备

2. **进入工作空间**:
   ```bash
   cd <对应版本的工作空间路径>
   ```

3. **拉取最新代码**:
   ```bash
   export https_proxy=http://192.168.6.110:17897 http_proxy=http://192.168.6.110:17897 all_proxy=socks5://192.168.6.110:17897
   for i in 1 2 3; do
       git pull 2>&1 | tee "$LOG_DIR/step3_git_pull.log" && break
       echo "git pull 失败，第 $i 次重试..."
       sleep 2
       if [ $i -eq 3 ]; then
           echo "git pull 连续3次失败，触发错误处理"
           exit 1
       fi
   done
   ```
   - **验证**: 检查输出无错误，无冲突

4. **切换分支**:
   ```bash
   export https_proxy=http://192.168.6.110:17897 http_proxy=http://192.168.6.110:17897 all_proxy=socks5://192.168.6.110:17897
   for i in 1 2 3; do
       git checkout <name>/<YYMMDD> 2>&1 | tee "$LOG_DIR/step4_git_checkout.log" && break
       echo "git checkout 失败，第 $i 次重试..."
       sleep 2
       if [ $i -eq 3 ]; then
           echo "git checkout 连续3次失败，触发错误处理"
           exit 1
       fi
   done
   ```
   - 例如: `git checkout test/20260424`

5. **确认分支**:
   ```bash
   export https_proxy=http://192.168.6.110:17897 http_proxy=http://192.168.6.110:17897 all_proxy=socks5://192.168.6.110:17897
   git branch 2>&1 | tee "$LOG_DIR/step5_git_branch.log"
   ```
   - **验证**: 当前分支标记为 `* <name>/<YYMMDD>`

6. **导入autoware依赖**:
   ```bash
   export https_proxy=http://192.168.6.110:17897 http_proxy=http://192.168.6.110:17897 all_proxy=socks5://192.168.6.110:17897
   for i in 1 2 3; do
       vcs import src < autoware.repos --recursive 2>&1 | tee "$LOG_DIR/step6_vcs_import_autoware.log" && break
       echo "vcs import autoware 失败，第 $i 次重试..."
       sleep 2
       if [ $i -eq 3 ]; then
           echo "vcs import autoware 连续3次失败，触发错误处理"
           exit 1
       fi
   done
   ```

7. **导入robobus依赖**:
   ```bash
   export https_proxy=http://192.168.6.110:17897 http_proxy=http://192.168.6.110:17897 all_proxy=socks5://192.168.6.110:17897
   for i in 1 2 3; do
       vcs import src < robobus.repos --recursive 2>&1 | tee "$LOG_DIR/step7_vcs_import_robobus.log" && break
       echo "vcs import robobus 失败，第 $i 次重试..."
       sleep 2
       if [ $i -eq 3 ]; then
           echo "vcs import robobus 连续3次失败，触发错误处理"
           exit 1
       fi
   done
   ```

8. **导入hmi依赖**:
   ```bash
   export https_proxy=http://192.168.6.110:17897 http_proxy=http://192.168.6.110:17897 all_proxy=socks5://192.168.6.110:17897
   for i in 1 2 3; do
       vcs import src < hmi.repos --recursive 2>&1 | tee "$LOG_DIR/step8_vcs_import_hmi.log" && break
       echo "vcs import hmi 失败，第 $i 次重试..."
       sleep 2
       if [ $i -eq 3 ]; then
           echo "vcs import hmi 连续3次失败，触发错误处理"
           exit 1
       fi
   done
   ```

9. **更新所有依赖**:
   ```bash
   export https_proxy=http://192.168.6.110:17897 http_proxy=http://192.168.6.110:17897 all_proxy=socks5://192.168.6.110:17897
   for i in 1 2 3; do
       vcs pull src 2>&1 | tee "$LOG_DIR/step9_vcs_pull.log" && break
       echo "vcs pull 失败，第 $i 次重试..."
       sleep 2
       if [ $i -eq 3 ]; then
           echo "vcs pull 连续3次失败，触发错误处理"
           exit 1
       fi
   done
   ```

### Step 10: 编译

10. **执行编译**:
    - 使用 skill 内置脚本执行编译，**设置1小时超时**（3600秒）：
      ```bash
      timeout 3600 bash .agents/skills/autoware-ota-release/scripts/build.sh <工作空间路径> "$LOG_DIR/step10_compile.log"
      ```
    - 或直接用 tee 同时显示输出并保存日志：
      ```bash
      timeout 3600 bash .agents/skills/autoware-ota-release/scripts/build.sh <工作空间路径> 2>&1 | tee "$LOG_DIR/step10_compile.log"
      ```
    - **编译耗时较长，请耐心等待，不要中断**
    - **Agent 持续等待**: 开始执行编译后，**不要结束对话**，保持连接状态，实时输出编译进度，等待编译完成后再继续下一步
    - **超时处理**: 若1小时内未完成，编译进程将被终止，向用户报告超时并询问是否继续等待或中止
    - **验证**: 检查编译是否成功完成，无致命错误
    - **编译失败的特殊处理**:
      1. `build.sh` 在编译失败时会直接输出报错的功能包名称和错误信息（包括 `Starting >>>`、stderr 和 `Failed <<<`），直接利用其输出即可
      2. 在工作空间的 `src/` 目录下定位该功能包的源码路径
      3. 阅读相关源码（报错文件、CMakeLists.txt、package.xml 等），分析编译失败的根本原因
      4. 结合代码上下文，提出处理方案（如：修改代码、更新依赖、调整编译参数、跳过该包等）
      5. **向用户汇报**：报错功能包、错误摘要、原因分析、建议的处理方案
      6. **等待用户审核**：用户确认方案后，再执行修复操作或按用户指示处理
      7. **修复后执行指定包编译验证**：
         - 向用户说明本次修改了哪些文件（列出具体文件路径）
         - 先对该功能包执行指定包编译，验证修复是否生效：
           ```bash
           colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release --packages-select <报错功能包名>
           ```
         - 确认该功能包单独编译通过
      8. **重新执行 Step 10（全量编译）**：指定包编译通过后，再重新执行全量编译，直至成功

### Step 11: OTA 推送

11. **执行 OTA 推送**:
    - **必须等待用户人工确认后再执行**
    - 向用户确认以下内容：
      - 版本号: `<name>/<YYMMDD>`
      - 配置文件名: `autoware-robobus.dev-master.<name>-<YYMMDD>.yaml`
      - 工作空间: `<路径>`
      - 编译结果: 成功
    - 用户确认后，执行推送命令：
      ```bash
      PixRover-Ota push autoware-robobus.dev-master.<name>-<YYMMDD>
      ```
    - 示例：
      - `test/20260424` → `PixRover-Ota push autoware-robobus.dev-master.test-20260424`
      - `release/20260424` → `PixRover-Ota push autoware-robobus.dev-master.release-20260424`
    - **验证**: 确认推送成功，无错误输出

## 执行规范

### 日志保存要求

- 每个步骤的命令输出必须重定向保存到日志文件
- 日志目录: `~/pix/ros2log/ota_release_logs/$(date +%Y%m%d_%H%M%S)/`
- 日志命名: `step<N>_<简要描述>.log`
- **任务总览日志**: `$LOG_DIR/progress.log`，实时记录各步骤执行状态，方便快速查看整体进度
- 工作流开始时创建日志目录并设置环境变量:
  ```bash
  export LOG_DIR=~/pix/ros2log/ota_release_logs/$(date +%Y%m%d_%H%M%S)
  mkdir -p "$LOG_DIR"
  ```
- 使用 `tee` 命令同时显示输出并保存到文件:
  ```bash
  <命令> 2>&1 | tee "$LOG_DIR/step<N>_描述.log"
  ```
- **每步更新总览日志**: 每执行一个步骤前/后，更新 `progress.log` 中对应步骤的状态
  - 更新方式示例（将 step3 标记为进行中）：
    ```bash
    sed -i 's/^step3:.*/step3: 进行中 ⚠️/' "$LOG_DIR/progress.log"
    ```
  - 更新方式示例（将 step3 标记为已完成）：
    ```bash
    sed -i 's/^step3:.*/step3: 已完成 ✅/' "$LOG_DIR/progress.log"
    ```

### 总览日志状态说明

`progress.log` 中各步骤的状态值规范：

| 状态值 | 含义 | 使用场景 |
|--------|------|---------|
| `等待执行` | 尚未开始 | 初始化时 |
| `进行中 ⚠️` | 正在执行 | 步骤开始执行时 |
| `已完成 ✅` | 执行成功 | 步骤验证通过后 |
| `重试中 ⚠️` | 自动重试 | git/vcs 命令失败自动重试时 |
| `报错AI生成方案中 ⚠️` | 编译失败，正在分析源码生成修复方案 | Step 10 编译失败后 |
| `等待审核方案中 ⚠️` | 方案已生成，等待用户审核 | 向用户汇报方案后 |
| `步骤再次执行中 ⚠️` | 用户审核通过，正在重新执行 | 修复后重新编译时 |
| `失败 ❌` | 最终失败 | 重试3次后仍失败或用户否定方案时 |

### 错误处理

- 每一步执行后立即检查退出状态码 (`$?`)
- `git` 和 `vcs` 相关命令（拉取代码、切换分支、导入依赖、更新依赖）失败时，**自动重试最多3次**，每次间隔2秒
- 其他命令或 `git`/`vcs` 连续3次重试后仍失败（退出码非0）:
  1. 立即停止后续步骤
  2. 向用户报告失败的步骤和错误信息
  3. 提供日志文件路径供查看

### 成功确认

- 每步成功后向用户简要汇报该步骤结果
- 所有11步完成后，汇总报告:
  - 版本号: `<name>/<YYMMDD>`
  - 工作空间: `<路径>`
  - OTA配置上传状态
  - 编译结果
  - OTA推送状态
  - release note内容
  - **执行的指令列表**: 列出本次工作流执行的所有关键命令（git pull、vcs import、colcon build、PixRover-Ota 等）
  - **创建的文件列表**: 列出本次工作流中新创建的所有文件路径（如 OTA 配置文件、编译生成的安装文件等）
  - **修改的文件列表**: 列出本次工作流中修改过的所有文件路径（如编译修复时修改的源码文件）
  - **生成的日志列表**: 列出 `$LOG_DIR/` 目录下所有生成的日志文件
  - **方案审核统计**:
    - 发起方案审核次数: `<N>` 次
    - 通过: `<N>` 个
    - 否定: `<N>` 个
  - **Token消耗记录**:
    - 输入tokens: `<N>`
    - 输出tokens: `<N>`
    - 总tokens: `<N>`
  - 所有日志文件位置: `$LOG_DIR/`

## 示例

用户指令：
> 开始发版工作流：请发版autoware:test/20260424，release note:1. 解决变道取消导致的轨迹突变；2. 优化尾部轨迹稳定性；3. 解决因为地图错误导致的规划崩溃；4. 解决因为地图高程过高导致轨迹出现在地下问题；5. 优化重规划功能；6. jpeg输出frame_id与camera_info统一；开始OTA发版工作流

解析结果：
- 版本类型: 园区版本 (test)
- 分支: `test/20260424`
- 工作空间: `~/pix/robobus/autoware-robobus.dev-master.test/`
- release note: 6条更新内容
