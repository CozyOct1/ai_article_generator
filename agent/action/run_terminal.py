from agent.planning.github_md import github_md
from agent.planning.input_novel import input_novel


def run_terminal():
    """终端交互函数"""
    # 选择功能
    option = input(
        "请选择以下功能：\n0. 退出程序\n1. 输入你的想法生成文章\n2. 生成最近一周Github热榜文章\n请输入你的选择：\n"
    )
    if option == "0":
        print("程序退出")
    elif option == "1":
        input_novel()
    elif option == "2":
        github_md()
    else:
        print("请输入正确的选项")
