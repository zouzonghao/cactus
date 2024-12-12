import os
import re

# 修改文件的函数
def modify_md_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 匹配 YAML Front Matter 的正则表达式
    yaml_pattern = re.compile(r"---\n(.*?)\n---", re.DOTALL)
    match = yaml_pattern.search(content)

    if not match:
        print(f"[WARNING] 文件 {file_path} 没有找到 YAML Front Matter，跳过。")
        return

    yaml_content = match.group(1)

    # 提取原始字段
    title_match = re.search(r"title:\s*(.+)", yaml_content)
    date_match = re.search(r"date:\s*(.+)", yaml_content)
    tag_match = re.search(r"tag:\s*(\n(\s+\-\s.+)+)", yaml_content)

    title = title_match.group(1).strip() if title_match else '未指定标题'
    date = date_match.group(1).strip() if date_match else '1970-01-01'

    # 处理 tags
    if tag_match:
        tags_raw = tag_match.group(1).strip()
        tags_list = [tag.strip() for tag in re.findall(r"\-\s(.+)", tags_raw)]
    else:
        tags_list = []

    tags_formatted = f"[{', '.join([f'\"{tag}\"' for tag in tags_list])}]"

    # 生成新的 YAML 内容
    new_yaml = f"---\n" \
               f"title: \"{title}\"\n" \
               f"description: \"none\"\n" \
               f"publishDate: \"{date}\"\n" \
               f"tags: {tags_formatted}\n" \
               f"---"

    # 替换原始 YAML
    new_content = yaml_pattern.sub(new_yaml, content)

    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)

    print(f"[SUCCESS] 文件 {file_path} 已成功修改。")

# 批量处理目录中的 Markdown 文件
def batch_modify_md_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                modify_md_file(file_path)

if __name__ == "__main__":
    target_directory = input("请输入需要批量修改的 Markdown 文件所在目录：").strip()

    if os.path.isdir(target_directory):
        batch_modify_md_files(target_directory)
    else:
        print(f"[ERROR] 目录 {target_directory} 不存在，请检查路径是否正确。")
