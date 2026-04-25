#!/usr/bin/env python3
"""
OTA 配置文件生成脚本

使用方法:
    python3 generate_ota_config.py <test|release> <version_name> <description...>

参数说明:
    <test|release>   版本类型: test(园区版本) 或 release(公开道路版本)
    <version_name>   版本名称, 格式: test/YYYYMMDD 或 release/YYYYMMDD
    <description...> 版本描述, 可传多个参数, 每个参数作为列表的一项

示例:
    python3 generate_ota_config.py test test/20260425 "0. 园区版本" "1. 修复感知bug" "2. 优化规划稳定性"
    python3 generate_ota_config.py release release/20260425 "0. 公开道路版本" "1. 优化变道"

功能逻辑:
    1. 根据版本类型和日期生成目标配置文件路径
    2. 若目标文件已存在, 直接打印并返回
    3. 若不存在, 找到同类型最新的参考文件, 基于它生成新配置:
       - 全局替换旧版本号为新版本号
       - 替换 version_description 为传入的字符串列表
       - 替换 ddf_remote_info_update 行末尾的描述为一行字符串
    4. 将最新参考文件的 version_archived: false 改为 true
"""
import sys
import os
import re
import glob

BASE_DIR = "/home/ipc/pix/test/PixRover-Tools/ota/config/autoware-robobus"


def find_latest_ref(version_type: str):
    """Find the latest reference YAML file for the given version type."""
    pattern = os.path.join(BASE_DIR, f"autoware-robobus.dev-master.{version_type}-*.yaml")
    files = glob.glob(pattern)
    if not files:
        return None, None

    def extract_date(filepath: str):
        basename = os.path.basename(filepath)
        m = re.search(rf"{version_type}-(\d{{6,8}})\.yaml$", basename)
        return m.group(1) if m else "000000"

    files.sort(key=extract_date)
    latest = files[-1]
    return latest, extract_date(latest)


def main():
    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} <test|release> <version_name> <description...>")
        print("  version_name: release/YYMMDD or test/YYMMDD")
        sys.exit(1)

    version_type = sys.argv[1]
    version_name = sys.argv[2]
    descriptions = sys.argv[3:]

    if version_type not in ("test", "release"):
        print(f"Error: version_type must be 'test' or 'release', got '{version_type}'")
        sys.exit(1)

    if "/" not in version_name:
        print("Error: version_name must contain '/', e.g. 'test/20260425'")
        sys.exit(1)

    name_part, date_part = version_name.split("/", 1)
    if not re.match(r"^\d{6,8}$", date_part):
        print(f"Error: date part must be 6-8 digits (YYMMDD or YYYYMMDD), got '{date_part}'")
        sys.exit(1)

    # e.g. test-20260425
    converted_version = f"{version_type}-{date_part}"
    cfg_filename = f"autoware-robobus.dev-master.{converted_version}.yaml"
    cfg_path = os.path.join(BASE_DIR, cfg_filename)

    # 1. File already exists -> print and return
    if os.path.exists(cfg_path):
        print(f"已创建好{cfg_path}")
        return

    # 2. Find latest reference file
    latest_ref, ref_date = find_latest_ref(version_type)
    if not latest_ref:
        print(f"Error: No reference file found for type '{version_type}' in {BASE_DIR}")
        sys.exit(1)

    old_version_str = f"{version_type}-{ref_date}"
    single_description = " ".join(descriptions)

    with open(latest_ref, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    in_version_desc = False

    for line in lines:
        # Global replacement of old version string with new one
        line = line.replace(old_version_str, converted_version)

        # Replace version_description block
        if line.strip().startswith("version_description:"):
            in_version_desc = True
            new_lines.append("version_description: \n")
            for desc in descriptions:
                new_lines.append(f"  - {desc}\n")
            continue

        if in_version_desc:
            if line.startswith("  - "):
                continue
            else:
                in_version_desc = False

        # Replace description in ddf_remote_info_update line
        if "ddf_remote_info_update" in line:
            prefix = f'args: "ddf_remote_info_update 自驾 {converted_version} '
            idx = line.find(prefix)
            if idx != -1:
                end_quote_idx = line.rfind('"')
                if end_quote_idx != -1 and end_quote_idx > idx + len(prefix):
                    line = line[: idx + len(prefix)] + single_description + line[end_quote_idx:]

        new_lines.append(line)

    # Write new configuration file
    with open(cfg_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print(f"Generated: {cfg_path}")

    # 3. Update latest reference file: version_archived: false -> true
    with open(latest_ref, "r", encoding="utf-8") as f:
        ref_content = f.read()

    ref_content = re.sub(
        r"(version_archived:\s*)false",
        r"\1true",
        ref_content,
        count=1,
    )

    with open(latest_ref, "w", encoding="utf-8") as f:
        f.write(ref_content)
    print(f"Updated version_archived=true in: {latest_ref}")


if __name__ == "__main__":
    main()
