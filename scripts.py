# coding=utf-8
import os
import nbformat
from nbconvert import MarkdownExporter
from typing import List, Tuple
from functools import wraps
import time
from tqdm import tqdm


def count_time(func):
    @wraps(func)  # 引入wraps，对内层实现装饰器功能的函数进行装饰，主要是将传入的被装饰函数元信息复制给具体实现装饰器功能函数
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f'{func.__name__} runtime : {(end_time - start_time).__round__(2)}s')
        return result
    return wrapper


@count_time
def convert_jupyter_to_md(file_path: str) -> Tuple[List[str], List[str], List[str]]:
    count = 0
    titles = []
    jupyter_content = []
    tocs = []
    md_content = []
    exporter = MarkdownExporter()

    for root, _, files in os.walk(file_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                count += 1
                nb = nbformat.read(f, as_version=4)
                jupyter_content.append(nb)
                titles.append(f"# {count}. {file.split('.')[0]}")

    # 合并jupyter notebook文件,增加进度条
    for content, title in tqdm(zip(jupyter_content, titles), total=len(jupyter_content)):
        markdown, _ = exporter.from_notebook_node(content)
        toc = f"* [{title[2:].strip()}](#{title[2:].strip().replace(' ', '-').replace('.', '')})"
        tocs.append(toc)
        md_content.append(markdown)
    return tocs, md_content, titles


@count_time
def combine_md_files(
        tocs: List[str],
        md_content: List[str],
        titles: List[str],
        output_file: str
) -> None:

    with open(output_file, 'a', encoding='utf-8') as f:
        # 写入标题
        for toc in tocs:
            f.write(toc + '\n')

        # 写入分割线
        f.write('\n---\n\n')
        # 写入内容
        for content, title in zip(md_content, titles):
            f.write(title + '\n')
            f.write(content + '\n')
    f.close()
    print(f'combine finish : {output_file}')


if __name__ == '__main__':
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    TIP_DIR = os.path.join(ROOT_DIR, 'tip')
    README_PATH = os.path.join(ROOT_DIR, 'README.md')

    # 检查README.md文件是否存在，如果存在则删除
    if os.path.exists(README_PATH):
        os.remove(README_PATH)
    combine_md_files(*convert_jupyter_to_md(TIP_DIR), README_PATH)
