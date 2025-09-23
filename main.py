from agent.action.input_novel import input_novel


if __name__ == "__main__":
    option = input(
        "请选择以下功能：\n0. 退出程序\n1. 输入你的想法生成文章\n请输入你的选择：\n"
    )
    if option == "0":
        print("程序退出")
    elif option == "1":
        input_novel()
    else:
        print("请输入正确的选项")