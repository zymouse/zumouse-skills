#!/bin/bash
# ROS2 Skill 全局部署脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="${SCRIPT_DIR}/.agents/skills"
TARGET_DIR="${HOME}/.kimi/skills"

echo "=== ROS2 Skill 部署 ==="
echo ""

# 创建目标目录
mkdir -p "${TARGET_DIR}"

# 遍历并部署所有 skill
for skill_path in "${SOURCE_DIR}"/*; do
    if [ -d "${skill_path}" ]; then
        skill_name=$(basename "${skill_path}")
        echo "部署: ${skill_name}"
        cp -r "${skill_path}" "${TARGET_DIR}/"
    fi
done

echo ""
echo "部署完成！目标路径: ${TARGET_DIR}"
echo "已部署 skills:"
ls -1 "${TARGET_DIR}"
