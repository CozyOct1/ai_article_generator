from agent.tools.common import cp_file, hexo_deploy

if __name__ == "__main__":
    cp_file("./agent/memory/input_novel/Conda环境初始化与默认配置：Linux系统Anaconda部署详解.md", "../hexo_blog/source/_posts/input_novel/Conda环境初始化与默认配置：Linux系统Anaconda部署详解.md")
    hexo_deploy("../hexo_blog")
