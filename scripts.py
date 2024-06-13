# coding=utf-8
import os
import nbformat
from nbconvert import MarkdownExporter

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# print(ROOT_DIR)
TIP_DIR = os.path.join(ROOT_DIR, 'tip')
# 检查README.md文件是否存在，如果存在则删除
if os.path.exists(os.path.join(ROOT_DIR, 'README.md')):
    os.remove(os.path.join(ROOT_DIR, 'README.md'))

# 遍历tip文件夹
for root, dirs, files in os.walk(TIP_DIR):
    count = 0
    titles = []
    jupyter_content = []
    exporter = MarkdownExporter()
    for file in files:
        file_path = os.path.join(root, file)
        output_path = os.path.join(ROOT_DIR, 'tmp', file)
        with open(file_path, 'r', encoding='utf-8') as f:
            count += 1
            nb = nbformat.read(f, as_version=4)
            jupyter_content.append(nb)
            titles.append(f"# {count}. {file.split('.')[0]}")
    # 合并jupyter notebook文件
    for content, title in zip(jupyter_content, titles):
        markdown, _ = exporter.from_notebook_node(content)
        # 覆盖原本的README.md文件
        with open(os.path.join(ROOT_DIR, 'README.md'), 'a', encoding='utf-8') as f:
            f.write(title)
            f.write('\n')
            f.write(markdown)
            f.write('\n')




