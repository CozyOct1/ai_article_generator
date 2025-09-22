import json
import traceback

from agent.tools.agent_coze import AgentCoze


def agent_create(api_token: str, api_base: str) -> AgentCoze:
    """创建 Coze 智能体实例

    :param str api_token: Coze API 访问令牌
    :param str api_base: Coze API 基础地址
    :return AgentCoze: 返回创建的 Coze 智能体实例
    """
    try:
        coze_agent = AgentCoze(api_token=api_token, api_base=api_base)
        return coze_agent
    except Exception as e:
        print(f"[agent_create] <error>\n{traceback.format_exc()}")
        return None


def title_create(
    coze_agent: AgentCoze, title_bot_id: str, user_id: str, user_input: str
) -> str:
    """生成文章标题

    :param AgentCoze coze_agent: Coze 智能体实例
    :param str title_bot_id: 标题生成机器人的 ID
    :param str user_id: 用户唯一标识符
    :param str user_input: 用户输入的内容或关键词
    :return str: 返回生成的文章标题
    """
    try:
        title = coze_agent.agent_chat(
            bot_id=title_bot_id,
            user_id=user_id,
            user_input=user_input,
        )
    except Exception as e:
        print(f"[title_create] <error>\n{traceback.format_exc()}")
        return ""

    # 检查返回值是否为空或无效
    if not title or title.strip() == "":
        print(f"[title_create] <error>\n生成标题无效, 原始输入: {user_input}")
        return ""

    try:
        title = json.loads(title)
    except Exception as e:
        print(f"[title_create] <error>\nJSON解析失败, 原始内容: {title}")
        return ""

    return title


def novel_create(
    coze_agent: AgentCoze, novel_bot_id: str, user_id: str, title: str
) -> str:
    """生成文章内容

    :param AgentCoze coze_agent: Coze 智能体实例
    :param str novel_bot_id: 文章生成机器人的 ID
    :param str user_id: 用户唯一标识符
    :param str title: 文章标题
    :return str: 返回生成的文章内容
    """
    try:
        novel = coze_agent.agent_chat(
            bot_id=novel_bot_id,
            user_id=user_id,
            user_input=title,
        )
    except Exception as e:
        print(f"[novel_create] <error>\n{traceback.format_exc()}")
        return ""

    # 检查返回值是否为空或无效
    if not novel or novel.strip() == "":
        print(f"[novel_create] <error>\n生成文章无效, 原始输入: {title}")
        return ""

    try:
        novel = json.loads(novel)
    except json.JSONDecodeError as e:
        print(f"[novel_create] <error>\nJSON解析失败, 原始内容: {novel}")
        return ""

    return novel


def save_md(title: str, content: str, link: str) -> str:
    """保存文章为 Markdown 文件

    :param str title: 文章标题
    :param str content: 文章内容
    :param str link: 参考链接
    :return str: 返回保存的文件路径
    """
    
    filename = f"./agent/memory/{title}.md"
    with open(filename, "w", encoding="utf-8") as f:
        # 格式化参考链接为正确的 Markdown 格式
        formatted_links = []
        if isinstance(link, dict):
            for title_text, url in link.items():
                # 清理 URL，移除多余的空格和反引号
                clean_url = url.strip().strip("`").strip()
                formatted_links.append(f"- [{title_text}]({clean_url})")
        else:
            formatted_links.append(f"- {link}")

        links_text = "\n".join(formatted_links)
        f.write(f"{content}\n\n## 参考链接\n\n{links_text}")
    return filename
