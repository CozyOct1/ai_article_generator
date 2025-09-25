from cozepy import ChatStatus, Coze, Message, TokenAuth


class AgentCoze:
    """AgentCoze 类用于与 Coze 平台进行交互"""

    def __init__(self, api_token: str, api_base: str):
        """
        初始化 AgentCoze 实例

        :param str api_token: Coze API 的访问令牌
        :param str api_base: Coze API 的基础 URL
        """
        self.api_token = api_token
        self.api_base = api_base
        self.coze = Coze(auth=TokenAuth(token=api_token), base_url=api_base)

    def agent_chat(self, bot_id: str, user_id: str, user_input: str) -> str:
        """
        与 Coze 机器人进行聊天

        :param str bot_id: 机器人的 ID
        :param str user_id: 用户的 ID
        :param str user_input: 用户的输入消息
        :return str: 机器人回复的消息内容
        """
        title_bot = self.coze.chat.create_and_poll(
            bot_id=bot_id,
            user_id=user_id,
            additional_messages=[Message.build_user_question_text(user_input)],
        )
        if title_bot.chat.status == ChatStatus.COMPLETED:
            return title_bot.messages[-2].content
        else:
            print(
                f"[agent_chat] <error>\n对话失败, title_bot.chat.status={title_bot.chat.status}"
            )
            return ""

    def workflow_chat(self, workflow_id: str, user_input: str) -> str:
        """
        与 Coze 工作流机器人进行聊天

        :param str workflow_id: 工作流机器人的 ID
        :param str user_input: 用户的输入消息
        :return str: 机器人回复的消息内容
        """
        workflow = self.coze.workflows.runs.create(
            workflow_id=workflow_id,
            parameters={"user_input": user_input},
        )
        if workflow.data:
            return workflow.data
        else:
            print(f"[workflow_chat] <error>\n对话失败, workflow.data={workflow.data}")
            return {}
