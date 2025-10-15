import json
import time
import traceback

import toml

from agent.tools.agent_coze import AgentCoze
from agent.tools.common import cp_file, hexo_deploy, save_md


def github_md():
    """
    生成最近每日Github热榜文章
    """
    try:
        # 读取配置文件
        try:
            agent_coze_config = toml.load(f"./configs/agent_coze.toml")
            blog_config = toml.load(f"./configs/hexo_blog.toml")
            api_token = agent_coze_config["api"]["api_token"]
            api_base = agent_coze_config["api"]["api_base"]
            github_workflow = agent_coze_config["github_workflow"]["workflow_id"]
            blog_dir = blog_config["blog"]["blog_dir"]
            print("读取配置文件成功")
        except Exception as e:
            print(f"[github_md] <error>\n{traceback.format_exc()}")
            return

        # 创建 Coze 智能体实例
        try:
            coze_agent = AgentCoze(api_token=api_token, api_base=api_base)
            print("AgentCoze 实例创建成功")
        except Exception as e:
            print(f"[github_md] <error>\n{traceback.format_exc()}")
            return

        # 生成文章内容
        print(f"正在生成Github热榜文章...")
        try:
            tik = time.time()
            workflow_data = coze_agent.workflow_chat(
                workflow_id=github_workflow, user_input=""
            )
            tok = time.time()
            workflow_data = json.loads(workflow_data)
            title = workflow_data["title"]
            novel = workflow_data["novel"]
            redbook = workflow_data["redbook"]
            print(f"文章标题: {title}")
            print(f"生成内容(耗时{tok - tik:.2f}秒):: \n{novel}")
        except Exception as e:
            print(f"[github_md] <error>\n{traceback.format_exc()}")
            return

        # 保存文章到文件
        is_save = input("是否保存文章内容？(输入y/n):\n")
        while is_save not in ["y", "n"]:
            is_save = input("请输入正确的选项(y/n):\n")
        if is_save == "y":
            try:
                filename = save_md(directory="github_md", title=title, novel=novel)
                print(f"文章已保存至 {filename}")
                # 保存红书文章到文件
                redbook_filename = save_md(
                    directory="github_md", title=f"{title}_redbook", novel=redbook
                )
                print(f"红书文章已保存至 {redbook_filename}")
            except Exception as e:
                print(f"[github_md] <error>\n{traceback.format_exc()}")
        else:
            print("文章未保存")
            return

        # 复制文件到博客文件夹下
        is_upload = input("是否上传到博客？(输入y/n):\n")
        while is_upload not in ["y", "n"]:
            is_upload = input("请输入正确的选项(y/n):\n")
        if is_upload == "y":
            try:
                dst = f"{blog_dir}/source/_posts/github_md/{title}.md"
                cp_file(filename, dst)
                print(f"文件已复制到 {dst}")
            except Exception as e:
                print(f"[github_md] <error>\n{traceback.format_exc()}")
        else:
            print("文件未上传")
            return

        # 部署 Hexo 博客
        print("正在部署 Hexo 博客...")
        try:
            hexo_deploy(blog_dir)
            print("Hexo 博客已部署")
        except Exception as e:
            print(f"[github_md] <error>\n{traceback.format_exc()}")
            return

        # 封面生成,"|"分隔title
        title = title.split("｜")[1]
        print("https://www.doubao.com/chat/create-image")
        print(
            f"提示词：图片风格为「像素风格」，艺术字标题「{title}」，标题位于图片中部，背景体现标题内容，比例 「21:9」，不要生成比例相关的文字"
        )
        # 发表到以下博客地址：
        ## 知乎
        print("知乎：https://zhuanlan.zhihu.com/write")
        ## 简书
        print("简书：https://www.jianshu.com/writer#/notebooks/56349606")
        ## 思否
        print("思否：https://segmentfault.com/write?freshman=1")
        ## 博客园
        print("博客园：https://i.cnblogs.com/articles/edit")
        ## 小红书
        print(
            "小红书：https://creator.xiaohongshu.com/publish/publish?from=menu&target=article"
        )
        ## CSDN
        print("CSDN：https://editor.csdn.net/md")
        ## 稀土掘金
        print("稀土掘金：https://juejin.cn/editor/drafts/new?v=2")
        ## 微信公众号
        print(
            "微信公众号：https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&createType=8&token=1529114311&lang=zh_CN&timestamp=1760423443911"
        )

    except Exception as e:
        print(f"[github_md] <error>\n{traceback.format_exc()}")
        return
