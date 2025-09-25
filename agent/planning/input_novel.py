import json
import time
import traceback
import uuid

import toml

from agent.tools.agent_coze import AgentCoze
from agent.tools.common import cp_file, save_md


def input_novel():
    """
    根据用户输入生成文章
    """
    try:
        # 读取配置文件
        try:
            agent_coze_config = toml.load(f"./configs/agent_coze.toml")
            blog_config = toml.load(f"./configs/blog.toml")
            api_token = agent_coze_config["api"]["api_token"]
            api_base = agent_coze_config["api"]["api_base"]
            title_bot_id = agent_coze_config["title_bot"]["bot_id"]
            novel_bot_id = agent_coze_config["novel_bot"]["bot_id"]
            blog_dir = blog_config["blog"]["blog_dir"]
            print("读取配置文件成功")
        except Exception as e:
            print(f"[input_novel] <error>\n{traceback.format_exc()}")
            return

        # 创建 Coze 智能体实例
        try:
            coze_agent = AgentCoze(api_token=api_token, api_base=api_base)
            print("AgentCoze 实例创建成功")
        except Exception as e:
            print(f"[input_novel] <error>\n{traceback.format_exc()}")
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
            tik = time.time()
            try:
                title = coze_agent.agent_chat(
                    bot_id=title_bot_id,
                    user_id=user_id,
                    user_input=user_input,
                )
                title = json.loads(title)
            except Exception as e:
                print(f"[input_novel] <error>\n{traceback.format_exc()}")
                title = ""
            tok = time.time()
            if title == "":
                retry = input("生成标题错误,是否重新生成标题？(输入y/n):\n")
                while retry not in ["y", "n"]:
                    retry = input("请输入正确的选项(y/n):\n")
                if retry == "y":
                    continue
                else:
                    print(f"[input_novel] <error>\n生成标题为空, 退出程序")
                    return
            print(
                f"生成如下标题(耗时{tok - tik:.2f}秒):\n{json.dumps(title, ensure_ascii=False, indent=4)}"
            )

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
                    print(f"[input_novel] <input>\n输入错误, 请输入数字1-5")
                    title_index = input("请输入正确的标题序号(输入数字1-5):\n")
                title = title["标题" + title_index]
                print(f"文章标题: {title}")
                break

        # 生成文章内容
        print("正在生成文章内容...")
        tik = time.time()
        try:
            novel = coze_agent.agent_chat(
                bot_id=novel_bot_id,
                user_id=user_id,
                user_input=title,
            )
        except Exception as e:
            print(f"[input_novel] <error>\n{traceback.format_exc()}")
            novel = ""
        tok = time.time()
        if novel == "":
            print(f"[input_novel] <error>\n生成文章内容错误, 退出程序")
            return
        print(f"生成文章内容(耗时{tok - tik:.2f}秒):\n{novel}")

        # 保存文章到文件
        is_save = input("是否保存文章内容？(输入y/n):\n")
        while is_save not in ["y", "n"]:
            is_save = input("请输入正确的选项(y/n):\n")
        if is_save == "y":
            try:
                filename = save_md(directory="input_novel", title=title, novel=novel)
                print(f"文章已保存至 {filename}")
            except Exception as e:
                print(f"[input_novel] <error>\n{traceback.format_exc()}")
        else:
            print("文章未保存")

        # 复制文件到博客文件夹下
        is_upload = input("是否上传到博客？(输入y/n):\n")
        while is_upload not in ["y", "n"]:
            is_upload = input("请输入正确的选项(y/n):\n")
        if is_upload == "y":
            try:
                dst = cp_file(filename, f"{blog_dir}/input_novel/")
                print(f"文件已复制到 {dst}")
            except Exception as e:
                print(f"[input_novel] <error>\n{traceback.format_exc()}")
        else:
            print("文件未上传")
    except Exception as e:
        print(f"[input_novel] <error>\n{traceback.format_exc()}")
        return
