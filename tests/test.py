import toml

from agent.tools.common import md_clean_header, md_to_richtext_zhihu
from agent.tools.uploader import zhihu_uploader

if __name__ == "__main__":
    # 读取markdown
    title = "⚡️ 2025-09-22 GitHub Trending 一周热榜速报 | 305亿参数智能体模型"
    with open(
        f"/data1/niewenjie/private/vault/ai_article_generator/agent/memory/github_md/{title}.md",
        "r",
        encoding="utf-8",
    ) as f:
        content = f.read()

    # 清理markdown标题块
    content = md_clean_header(content)

    # 转换为知乎格式
    content = md_to_richtext_zhihu(content)
    # print(content)

    # 读取cookies
    with open(
        "/data1/niewenjie/private/vault/ai_article_generator/configs/cookies.toml",
        "r",
        encoding="utf-8",
    ) as f:
        cookies = toml.load(f)
    # print(cookies["zhihu"]["cookie"])

    # 上传到专栏
    column_id = "c_1954607489719965596"
    if zhihu_uploader(cookies["zhihu"]["cookie"], title, content, column_id):
        print("上传成功")
    else:
        print("上传失败")
