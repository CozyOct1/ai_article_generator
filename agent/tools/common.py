import os
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
    :param str dst: 目标文件路径
    :return str: 返回目标文件路径
    """
    # 确保目标目录存在
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)
    return dst


def hexo_deploy(blog_dir: str):
    """部署 Hexo 博客

    :param str blog_dir: 博客目录路径
    """
    # 切换到 Hexo 博客目录并执行部署命令
    original_cwd = os.getcwd()
    os.chdir(blog_dir)
    os.system("git clean")
    os.system("hexo generate")
    os.system("hexo deploy")
    os.system("git add .")
    os.system("git commit -m 'update blog'")
    os.system("git push")
    os.chdir(original_cwd)
