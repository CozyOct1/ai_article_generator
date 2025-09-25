import os
import re
import shutil


def save_md(directory: str, title: str, novel: str) -> str:
    """保存文章为 Markdown 文件

    :param str directory: 保存目录
    :param str title: 文章标题
    :param str novel: 文章内容
    :return str: 返回保存的文件路径
    """
    os.makedirs(f"./agent/memory/{directory}", exist_ok=True)
    filename = f"./agent/memory/{directory}/{title}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(novel)
    return filename


def cp_file(src: str, dst: str) -> str:
    """复制文件

    :param str src: 源文件路径
    :param str dst: 目标路径（可以是文件路径或目录路径）
    :return str: 返回目标文件路径
    """
    # 如果目标是目录，则在目录中创建同名文件
    if os.path.isdir(dst):
        filename = os.path.basename(src)
        dst = os.path.join(dst, filename)

    # 确保目标目录存在
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)
    return dst
