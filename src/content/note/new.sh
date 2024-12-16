#!/bin/zsh

# 写死的目标文件夹路径
TARGET_FOLDER="/Users/macm4/code/cactus/src/content/note/2024/12月"  # 将此路径替换为你希望的文件夹路径

# 检查目标文件夹是否存在，如果不存在则创建
if [ ! -d "$TARGET_FOLDER" ]; then
    mkdir -p "$TARGET_FOLDER"
    if [ $? -ne 0 ]; then
        echo "Failed to create folder: $TARGET_FOLDER"
        exit 1
    fi
fi

# 获取当前时间戳
timestamp=$(date +"%Y%m%d%H%M%S")

# 定义文件名
filename="${timestamp}.md"

# 定义文件路径
filepath="${TARGET_FOLDER}/${filename}"

# 创建文件并写入 Front Matter
cat <<EOF > "$filepath"
---
title: "$timestamp"
description: none
publishDate: "$(date +"%Y-%m-%d %H:%M")"
---
EOF

# 检查文件是否创建成功
if [ -f "$filepath" ]; then
    echo "File created: $filepath"
else
    echo "Failed to create file."
    exit 1
fi

# 使用 Sublime Text 打开文件

subl "$filepath"

