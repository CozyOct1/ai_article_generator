import os
import re
import re
import shutil

import bleach
from markdown import Markdown


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
    os.system("hexo clean")
    os.system("hexo generate")
    os.system("hexo deploy")
    os.system("git add .")
    os.system("git commit -m 'update blog'")
    os.system("git push")
    os.chdir(original_cwd)


def md_clean_header(md_content: str) -> str:
    """清理 Markdown 内容中的标题块

    :param str md_content: Markdown 内容
    :return str: 清理后的 Markdown 内容
    """
    pattern = r"^---\s*\n.*?\n---\s*\n"
    cleaned_content = re.sub(
        pattern, "", md_content, count=1, flags=re.DOTALL | re.MULTILINE
    )
    cleaned_content = re.sub(r"\n\s*\n\s*\n", "\n\n", cleaned_content)
    cleaned_content = cleaned_content.strip()

    return cleaned_content


def md_to_zhihu_table(md_content: str) -> str:
    """将Markdown内容中的表格转换为知乎专用的表格格式

    :param str md_content: Markdown 内容
    :return str: 转换后的知乎表格格式内容
    """
    # 先进行基本的Markdown到HTML转换
    md = Markdown(
        output_format="html",
        extensions=["extra", "codehilite"],
    )
    html = md.convert(md_content)

    table_pattern = r"<table.*?>(.*?)</table>"

    def convert_to_zhihu_table(match):
        """转换Markdown表格为知乎表格格式

        :param _type_ match: 匹配到的Markdown表格HTML
        :return str: 转换后的知乎表格格式HTML
        """
        table_html = match.group(1)

        # 提取表头
        headers = []
        header_match = re.search(r"<thead>(.*?)</thead>", table_html, re.DOTALL)
        if header_match:
            headers = re.findall(
                r"<th[^>]*>(.*?)</th>", header_match.group(1), re.DOTALL
            )

        # 提取数据行
        rows = []
        tbody_match = re.search(r"<tbody>(.*?)</tbody>", table_html, re.DOTALL)
        if tbody_match:
            for tr_match in re.finditer(
                r"<tr[^>]*>(.*?)</tr>", tbody_match.group(1), re.DOTALL
            ):
                cells = re.findall(r"<td[^>]*>(.*?)</td>", tr_match.group(1), re.DOTALL)
                if cells:
                    rows.append(cells)

        # 如果没有thead/tbody，直接提取所有行
        if not headers and not rows:
            all_rows = []
            for tr_match in re.finditer(r"<tr[^>]*>(.*?)</tr>", table_html, re.DOTALL):
                cells = re.findall(
                    r"<t[dh][^>]*>(.*?)</t[dh]>", tr_match.group(1), re.DOTALL
                )
                if cells:
                    all_rows.append(cells)

            if all_rows:
                headers = all_rows[0]
                rows = all_rows[1:]

        if headers:
            # 构建知乎表格HTML
            zhihu_table = f'<table class="Table FocusPlugin--unfocused" data-draft-node="block" data-draft-type="table" data-size="normal" data-row-style="normal"><tbody>'

            # 表头行
            zhihu_table += '<tr class="Table-row">'
            for header in headers:
                zhihu_table += f'<th class="Table-data Table-header"><div class="Table-dataInputContainer"><div class="Table-dataInput" contenteditable="true">{header}</div></div></th>'
            zhihu_table += "</tr>"

            # 数据行
            for row in rows:
                zhihu_table += '<tr class="Table-row">'
                for cell in row:
                    zhihu_table += f'<td class="Table-data"><div class="Table-dataInputContainer"><div class="Table-dataInput" contenteditable="true">{cell}</div></div></td>'
                zhihu_table += "</tr>"

            zhihu_table += "</tbody></table>"
            return zhihu_table

        return match.group(0)

    # 替换所有表格
    html = re.sub(table_pattern, convert_to_zhihu_table, html, flags=re.DOTALL)

    return html


def md_to_richtext_zhihu(md_content: str) -> str:
    """将 Markdown 转换为知乎支持的富文本 HTML（使用知乎专用表格格式）

    :param str md_content: Markdown 内容
    :return str: 转换后的知乎支持的富文本 HTML
    """
    # 转换表格为知乎格式
    html = md_to_zhihu_table(md_content)

    # 知乎允许的标签与属性（添加表格相关标签）
    allowed_tags = [
        "p",
        "br",
        "div",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "strong",
        "b",
        "em",
        "i",
        "u",
        "ul",
        "ol",
        "li",
        "blockquote",
        "a",
        "img",
        "pre",
        "code",
        "table",
        "tbody",
        "tr",
        "th",
        "td",
    ]

    allowed_attrs = {
        "a": ["href", "title", "target", "rel"],
        "img": ["src", "alt", "title", "width", "height"],
        "code": ["class"],
        "pre": ["class"],
        "table": [
            "class",
            "data-draft-node",
            "data-draft-type",
            "data-size",
            "data-row-style",
        ],
        "tbody": ["class"],
        "tr": ["class"],
        "th": ["class"],
        "td": ["class"],
        "div": ["class", "contenteditable"],
    }

    # 过滤
    clean_html = bleach.clean(
        html,
        tags=allowed_tags,
        attributes=allowed_attrs,
        strip=True,
    )

    # 统一把 h1/h2 降级成 h3
    clean_html = re.sub(r"<h[12](.*?)>", r"<h3\1>", clean_html)
    clean_html = re.sub(r"</h[12]>", "</h3>", clean_html)

    # 压缩多余空行
    clean_html = re.sub(r"\n{3,}", "\n\n", clean_html.strip())
    return clean_html
