#!/bin/bash
# Autoware OTA Release Build Script
# 自动检测架构并执行对应的编译指令
# 编译失败时自动提取报错功能包和报错内容

set -e

WORKSPACE="$1"
LOG_FILE="$2"

if [ -z "$WORKSPACE" ]; then
    echo "Usage: $0 <workspace_path> [log_file_path]"
    echo "Example: $0 ~/pix/robobus/autoware-robobus.dev-master.test"
    exit 1
fi

cd "$WORKSPACE" || exit 1

ARCH=$(uname -m)

START_TIME=$(date +%s)
START_TIME_STR=$(date '+%Y-%m-%d %H:%M:%S')

echo "开始编译，编译时间较长，请耐心等待..."

# 执行编译（不立即退出，需要捕获退出码并解析日志）
set +e

if [ "$ARCH" = "x86_64" ]; then
    if [ -n "$LOG_FILE" ]; then
        colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release --parallel-workers 1 --packages-skip yabloc_image_processing bevfusion nvenc_multicam > "$LOG_FILE" 2>&1
    else
        colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release --parallel-workers 1 --packages-skip yabloc_image_processing bevfusion nvenc_multicam
    fi
elif [ "$ARCH" = "aarch64" ]; then
    if [ -n "$LOG_FILE" ]; then
        colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release --parallel-workers 1 --packages-skip autoware_elevation_map_loader autoware_lidar_apollo_instance_segmentation yabloc_image_processing nebula_ros nebula_examples nebula_tests blind_spot_monitor cloud_control_platform_msgs database_operations_msgs get_osm_info get_osm_info_msgs hmi_launch mongodb_operations mqtt_protobuf_test pix_io_context pix_protocol_adapter pix_tcp_driver pixmoving_api_central_analysis pixmoving_api_central_business pixmoving_api_central_common pixmoving_api_central_platform pixmoving_chassis_interface pixmoving_chassis_interface_common pixmoving_hmi_msgs pixmoving_hmi_stack pixmoving_ros_mqtt_bridge pixmoving_ros_proto_bridge pixmoving_ros_zenoh_bridge pixmoving_vehicle_display_bridge relay_autoware_transfer circular_publisher crow_vendor failcase_tools failcase_ui sqlite3_rest autoware_ar_tag_based_localizer > "$LOG_FILE" 2>&1
    else
        colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release --parallel-workers 1 --packages-skip autoware_elevation_map_loader autoware_lidar_apollo_instance_segmentation yabloc_image_processing nebula_ros nebula_examples nebula_tests blind_spot_monitor cloud_control_platform_msgs database_operations_msgs get_osm_info get_osm_info_msgs hmi_launch mongodb_operations mqtt_protobuf_test pix_io_context pix_protocol_adapter pix_tcp_driver pixmoving_api_central_analysis pixmoving_api_central_business pixmoving_api_central_common pixmoving_api_central_platform pixmoving_chassis_interface pixmoving_chassis_interface_common pixmoving_hmi_msgs pixmoving_hmi_stack pixmoving_ros_mqtt_bridge pixmoving_ros_proto_bridge pixmoving_ros_zenoh_bridge pixmoving_vehicle_display_bridge relay_autoware_transfer circular_publisher crow_vendor failcase_tools failcase_ui sqlite3_rest autoware_ar_tag_based_localizer
    fi
else
    echo "ERROR: Unknown architecture: $ARCH"
    exit 1
fi

BUILD_EXIT_CODE=$?

set -e

END_TIME=$(date +%s)
END_TIME_STR=$(date '+%Y-%m-%d %H:%M:%S')
ELAPSED=$((END_TIME - START_TIME))
ELAPSED_MIN=$((ELAPSED / 60))
ELAPSED_SEC=$((ELAPSED % 60))

if [ $BUILD_EXIT_CODE -ne 0 ]; then
    echo "编译失败"
    if [ -n "$LOG_FILE" ] && [ -f "$LOG_FILE" ]; then
        # 编译失败：输出失败功能包的 Starting >>>、stderr 和 Failed   <<<
        awk '
        BEGIN { in_stderr = 0; current_pkg = "" }

        /^Starting >>>/ {
            pkg = $3
            gsub(/[ \t]+$/, "", pkg)
            starting_text[pkg] = $0
            next
        }

        /^--- stderr:/ {
            in_stderr = 1
            current_pkg = $3
            gsub(/[ \t]+$/, "", current_pkg)
            stderr_text[current_pkg] = ""
            next
        }

        in_stderr && /^---$/ {
            in_stderr = 0
            current_pkg = ""
            next
        }

        in_stderr {
            if (stderr_text[current_pkg] != "") {
                stderr_text[current_pkg] = stderr_text[current_pkg] "\n" $0
            } else {
                stderr_text[current_pkg] = $0
            }
        }

        /Failed   <<</ {
            failed_pkg = $3
            gsub(/\[.*$/, "", failed_pkg)
            gsub(/[ \t]+$/, "", failed_pkg)
            failed_list[failed_pkg] = 1
            failed_text[failed_pkg] = $0
        }

        END {
            for (pkg in failed_list) {
                if (pkg in starting_text) {
                    print starting_text[pkg]
                }
                if (pkg in stderr_text) {
                    print stderr_text[pkg]
                }
                if (pkg in failed_text) {
                    print failed_text[pkg]
                }
            }
        }
        ' "$LOG_FILE"
    fi
    exit 1
fi

# 编译成功：输出完成信息和耗时统计
echo "编译结束"
echo "编译完成"
echo "编译时间统计:"
echo "  开始时间: $START_TIME_STR"
echo "  结束时间: $END_TIME_STR"
echo "  总耗时: ${ELAPSED_MIN}分${ELAPSED_SEC}秒"

exit 0
