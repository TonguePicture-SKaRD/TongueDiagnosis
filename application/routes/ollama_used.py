import requests
import json
from ..orm import create_new_chat_records, get_chat_record
from datetime import datetime
from ..models import schemas


class OllamaStreamChatter:
    def __init__(self, model="deepseek-r1:14b",
                 system_prompt=None
                 ):
        self.url = "http://localhost:11434/api/chat"
        self.headers = {"Content-Type": "application/json"}
        self.messages = []
        self.model = model

        # 初始化系统提示
        if system_prompt:
            self.messages.append({
                "role": "system",
                "content": system_prompt
            })

    def chat_stream_first(self, user_input, feature, id, db, session_new_id):
        """流式对话（逐字输出）"""
        # 添加用户消息到历史
        self.messages = []
        self.messages.append({"role": "user", "content": "舌象特征是"+feature+","+user_input})
        # 构建请求数据
        data = {
            "model": self.model,
            "messages": self.messages,
            "stream": True  # 启用流式传输
        }

        full_response = ""
        try:
            # 发起流式请求
            response = requests.post(
                self.url,
                headers=self.headers,
                json=data,
                stream=True
            )
            response.raise_for_status()

            # 处理流式响应
            print("Assistant: ", end="", flush=True)
            for line in response.iter_lines():
                if line:
                    # 解析数据块
                    chunk = json.loads(line.decode('utf-8'))
                    if 'message' in chunk:
                        content = chunk['message']['content']
                        # 实时逐字输出
                        print(content, end="", flush=True)
                        full_response += content

            # 将完整回复加入历史
            self.messages.append({
                "role": "assistant",
                "content": full_response
            })
            create_new_chat_records(db=db, content=full_response, session_id=session_new_id, role=2)

        except requests.exceptions.RequestException as e:
            print(f"\n请求失败: {str(e)}")
            return None

        return full_response

    def chat_stream_add(self, id, db, session_id):
        """流式对话（逐字输出）"""
        chat_record = get_chat_record(ID=id, sessionid=session_id, db=db)
        records = []
        for record in chat_record:
            if record.role == 1:
                message = {
                    "role":"user",
                    "content":record.content
                }
            else:
                message = {
                    "role": "assistant",
                    "content": record.content
                }
            records.append(message)
        self.messages = records
        # 构建请求数据
        data = {
            "model": self.model,
            "messages": self.messages,
            "stream": True  # 启用流式传输
        }

        full_response = ""
        try:
            # 发起流式请求
            response = requests.post(
                self.url,
                headers=self.headers,
                json=data,
                stream=True
            )
            response.raise_for_status()

            # 处理流式响应
            print("Assistant: ", end="", flush=True)
            for line in response.iter_lines():
                if line:
                    # 解析数据块
                    chunk = json.loads(line.decode('utf-8'))
                    if 'message' in chunk:
                        content = chunk['message']['content']
                        # 实时逐字输出
                        print(content, end="", flush=True)
                        full_response += content

            # 将完整回复加入历史
            self.messages.append({
                "role": "assistant",
                "content": full_response
            })
            create_new_chat_records(db=db, content=full_response, session_id=session_id, role=2)

        except requests.exceptions.RequestException as e:
            print(f"\n请求失败: {str(e)}")
            return None

        return full_response


# # 使用示例 ============================================
# if __name__ == "__main__":
#     # 初始化聊天实例（带系统提示）
#     bot = OllamaStreamChatter(
#         model="deepseek-r1:14b"
#         # system_prompt="你是一个幽默的助手，回答要简短且用中文"
#     )
#
#     # 第一轮对话（流式）
#     print("User: 四个特征：舌色是暗红，舌苔颜色白，舌头厚，舌苔偏腐")
#     bot.chat_stream("四个特征：舌色是暗红，舌苔颜色白，舌头厚，舌苔偏腐")
#
#     # 第二轮对话（模型能记住上下文）
#     print("\nUser: 给我一点饮食上的建议")
#     bot.chat_stream("给我一点饮食上的建议")  # 能基于上下文回答


    # def chat_stream(self, user_input):
    #     """流式对话（逐字输出）"""
    #     # 添加用户消息到历史
    #     self.messages.append({"role": "user", "content": user_input})
    #
    #     # 构建请求数据
    #     data = {
    #         "model": self.model,
    #         "messages": self.messages,
    #         "stream": True  # 启用流式传输
    #     }
    #
    #     full_response = ""
    #     try:
    #         # 发起流式请求
    #         response = requests.post(
    #             self.url,
    #             headers=self.headers,
    #             json=data,
    #             stream=True
    #         )
    #         response.raise_for_status()
    #
    #         # 处理流式响应
    #         print("Assistant: ", end="", flush=True)
    #         for line in response.iter_lines():
    #             if line:
    #                 # 解析数据块
    #                 chunk = json.loads(line.decode('utf-8'))
    #                 if 'message' in chunk:
    #                     content = chunk['message']['content']
    #                     # 实时逐字输出
    #                     print(content, end="", flush=True)
    #                     full_response += content
    #
    #         # 将完整回复加入历史
    #         self.messages.append({
    #             "role": "assistant",
    #             "content": full_response
    #         })
    #
    #     except requests.exceptions.RequestException as e:
    #         print(f"\n请求失败: {str(e)}")
    #         return None
    #
    #     return full_response