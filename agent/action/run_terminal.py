import json
import traceback
import uuid
import time
import toml

from agent.planning.planning import agent_create, novel_create, save_md, title_create


def run_terminal():
    """运行终端交互程序，完成文章生成的完整流程"""
    try:
        # 读取配置文件
        try:
            agent_coze_config = toml.load("./configs/agent_coze.toml")
            api_token = agent_coze_config["api"]["api_token"]
            api_base = agent_coze_config["api"]["api_base"]
            title_bot_id = agent_coze_config["title_bot"]["bot_id"]
            novel_bot_id = agent_coze_config["novel_bot"]["bot_id"]
            print("读取配置文件成功")
        except Exception as e:
            print(f"[run_terminal] <error>\n{traceback.format_exc()}")
            return

        # 创建 Coze 智能体实例
        try:
            coze_agent = agent_create(api_token=api_token, api_base=api_base)
            print("AgentCoze 实例创建成功")
        except Exception as e:
            print(f"[run_terminal] <error>\n{traceback.format_exc()}")
            return

        # 生成用户ID并获取用户输入
        user_id = str(uuid.uuid4())
        print(f"用户ID: {user_id}")
        user_input = input("请输入你想生成的文章大纲、关键词或简介(输入exit退出):\n")
        if user_input == "exit":
            return

        # 生成文章标题（循环直到用户选择满意的标题）
        while True:
            print("正在生成标题...")
            try:
                tik = time.time()
                title = title_create(
                    coze_agent=coze_agent,
                    title_bot_id=title_bot_id,
                    user_id=user_id,
                    user_input=user_input,
                )
                tok = time.time()
                if title == "":
                    retry = input("生成标题为空,是否重新生成标题？(输入y/n):\n")
                    while retry not in ["y", "n"]:
                        retry = input("请输入正确的选项(y/n):\n")
                    if retry == "y":
                        continue
                    else:
                        print(f"[run_terminal] <error>\n生成标题为空, 退出程序")
                        return
                print(
                    f"生成如下标题(耗时{tok - tik:.2f}秒):\n{json.dumps(title, ensure_ascii=False, indent=4)}"
                )
            except Exception as e:
                print(f"[run_terminal] <error>\n{traceback.format_exc()}")
                return

            # 用户选择标题
            title_index = input(
                "请你选择你觉得合适的标题序号1-5(输入exit退出,输入0重新生成标题)：\n"
            )
            if title_index == "exit":
                return
            elif title_index == "0":
                continue
            else:
                while not title_index.isdigit() or int(title_index) not in range(1, 6):
                    print(f"[run_terminal] <input>\n输入错误, 请输入数字1-5")
                    title_index = input("请输入正确的标题序号(输入数字1-5):\n")
                title = title["标题" + title_index]
                print(f"文章标题: {title}")
                break

        # 生成文章内容
        print("正在生成文章内容...")
        try:
            tik = time.time()
            novel = novel_create(
                coze_agent=coze_agent,
                novel_bot_id=novel_bot_id,
                user_id=user_id,
                title=title,
            )
            tok = time.time()
            if novel == "":
                print(f"[run_terminal] <error>\n生成文章内容为空, 退出程序")
                return
            content = novel["内容"]
            link = novel["参考链接"]
            print(f"生成文章内容(耗时{tok - tik:.2f}秒):\n{content}")
            print(f"参考链接:\n{link}")
        except Exception as e:
            print(f"[run_terminal] <error>\n{traceback.format_exc()}")
            return

        # 保存文章到文件
        is_save = input("是否保存文章内容？(输入y/n):\n")
        while is_save not in ["y", "n"]:
            print(f"[run_terminal] <input>\n输入错误, 请输入y/n")
            is_save = input("请输入正确的选项(y/n):\n")
        if is_save == "y":
            try:
                filename = save_md(title=title, content=content, link=link)
                print(f"文章已保存至 {filename}")
            except Exception as e:
                print(f"[run_terminal] <error>\n{traceback.format_exc()}")
        else:
            print("文章未保存")
    except Exception as e:
        print(f"[run_terminal] <error>\n{traceback.format_exc()}")


if __name__ == "__main__":
    run_terminal()
