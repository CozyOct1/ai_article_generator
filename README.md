# AI Article Generator

基于 Coze 平台的智能文章生成器，能够根据用户输入的关键词、大纲或简介自动生成高质量的文章内容。

## 功能特性

- 🤖 **智能标题生成**：基于用户输入生成多个候选标题供选择
- 📝 **文章内容生成**：根据选定标题生成完整的文章内容
- 🔗 **参考链接收集**：自动收集相关参考资料链接
- 💾 **Markdown 保存**：将生成的文章保存为格式化的 Markdown 文件
- 🎯 **交互式体验**：提供友好的命令行交互界面

## 项目架构

```
ai_article_generator/
├── agent/                      # 核心代理模块
│   ├── action/                 # 动作执行模块
│   │   └── input_novel.py     # 终端交互主程序
│   ├── memory/                 # 文章存储目录
│   ├── planning/               # 规划和核心逻辑
│   │   └── planning.py         # 文章生成核心功能
│   └── tools/                  # 工具模块
│       └── agent_coze.py       # Coze API 集成
├── configs/                    # 配置文件目录
├── tests/                      # 测试文件
├── main.py                     # 程序入口
├── pyproject.toml              # 项目配置和依赖
└── README.md                   # 项目说明文档
```

## 部署

### 环境要求

- Python >= 3.10
- 有效的 Coze API 访问权限

### 安装步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd ai_article_generator
   ```

2. **安装依赖**
   ```bash
   # 使用 uv（推荐）
   uv sync
   
   # 或使用 pip
   pip install -e .
   ```

3. **配置 Coze API**
   
   在 `configs/` 目录下创建 `agent_coze.toml` 配置文件：
   ```toml
   [api]
   api_token = "your_coze_api_token"
   api_base = "https://api.coze.com"
   
   [title_bot]
   bot_id = "your_title_bot_id"
   
   [novel_bot]
   bot_id = "your_novel_bot_id"
   ```

### 配置说明

- `api_token`: Coze 平台的 API 访问令牌
- `api_base`: Coze API 的基础地址
- `title_bot.bot_id`: 用于生成标题的机器人 ID
- `novel_bot.bot_id`: 用于生成文章内容的机器人 ID

## 使用

### 启动程序

```bash
uv run main.py
```

### 使用流程

1. **输入内容**：根据提示输入文章大纲、关键词或简介
2. **选择标题**：从生成的 5 个候选标题中选择最合适的一个
3. **生成文章**：系统自动生成完整的文章内容和参考链接
4. **保存文章**：选择是否将文章保存为 Markdown 文件

### 示例交互

```
请输入你想生成的文章大纲、关键词或简介(输入exit退出):
> 人工智能在教育领域的应用

正在生成标题...
生成如下标题(耗时2.34秒):
{
    "标题1": "AI赋能教育：智能化学习的未来之路",
    "标题2": "人工智能革命：重塑现代教育生态",
    "标题3": "从传统到智能：AI如何改变教育方式",
    "标题4": "教育4.0时代：人工智能的创新应用",
    "标题5": "智慧教育新纪元：AI技术的深度融合"
}

请你选择你觉得合适的标题序号1-5(输入exit退出,输入0重新生成标题)：
> 1

文章标题: AI赋能教育：智能化学习的未来之路
正在生成文章内容...
生成文章内容(耗时15.67秒):
[文章内容...]

参考链接:
[参考链接列表...]

是否保存文章内容？(输入y/n):
> y

文章已保存至 ./agent/memory/AI赋能教育：智能化学习的未来之路.md
```

## 核心模块说明

### AgentCoze 类
- **位置**：`agent/tools/agent_coze.py`
- **功能**：封装 Coze API 调用，提供与 Coze 平台的交互接口

### Planning 模块
- **位置**：`agent/planning/planning.py`
- **功能**：
  - `agent_create()`: 创建 Coze 智能体实例
  - `title_create()`: 生成文章标题
  - `novel_create()`: 生成文章内容
  - `save_md()`: 保存文章为 Markdown 格式

### Terminal 交互
- **位置**：`agent/action/input_novel.py`
- **功能**：提供完整的命令行交互流程，协调各个模块完成文章生成任务

## 依赖说明

- **cozepy**: Coze 平台的 Python SDK，用于 API 调用
- **toml**: 配置文件解析库

## 注意事项

1. 确保 Coze API 配置正确且有足够的调用额度
2. 生成的文章将保存在 `agent/memory/` 目录下
3. 如果标题生成失败，可以选择重新生成
4. 程序支持随时输入 `exit` 退出

## 开发

### 运行测试
```bash
uv run tests/test.py
```

### 项目结构说明
- `agent/`: 核心业务逻辑
- `configs/`: 配置文件存放
- `tests/`: 测试代码
- `main.py`: 程序入口点