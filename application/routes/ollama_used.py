import requests
import json
from starlette.responses import JSONResponse, StreamingResponse
from ..orm import create_new_chat_records, get_chat_record


class OllamaStreamChatter:
    def __init__(self, model="deepseek-r1:1.5b",
                 system_prompt=None
                 ):
        self.url = "http://localhost:11434/api/chat"
        self.headers = {"Content-Type": "application/json"}
        self.messages = []
        self.model = model

        if system_prompt:
            self.messages.append({
                "role": "system",
                "content": system_prompt
            })

    def chat_stream_first(self, user_input, feature, id, db, session_new_id):
        self.messages = []
        self.messages.append({"role": "user", "content": "舌象特征是" + feature + "," + user_input})
        data = {
            "model": self.model,
            "messages": self.messages,
            "stream": True
        }
        try:
            response = requests.post(
                self.url,
                headers=self.headers,
                json=data,
                stream=True
            )
            response.raise_for_status()

            def generate():
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line.decode('utf-8'))
                        if 'message' in chunk:
                            content = chunk['message']['content']
                            full_response += content
                            yield json.dumps({
                                "token": content,
                                "session_id": session_new_id,
                                "is_complete": False
                            }) + "\n"
                yield json.dumps({
                    "token": full_response,
                    "session_id": session_new_id,
                    "is_complete": True
                }) + "\n"
                self._save_to_db_async(db, full_response, session_new_id)
            return StreamingResponse(
                generate(),
                media_type='application/x-ndjson'
            )
        except requests.exceptions.RequestException as e:
            return JSONResponse(
                status_code=500,
                content={"error": f"请求失败: {str(e)}"}
            )

    def chat_stream_add(self, id, db, session_id):
        chat_record = get_chat_record(ID=id, sessionid=session_id, db=db)
        records = []
        for record in chat_record:
            role = "user" if record.role == 1 else "assistant"
            records.append({"role": role, "content": record.content})
        self.messages = records
        data = {
            "model": self.model,
            "messages": self.messages,
            "stream": True
        }
        try:
            response = requests.post(self.url, headers=self.headers, json=data, stream=True)
            response.raise_for_status()

            def generate():
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line.decode('utf-8'))
                        if 'message' in chunk:
                            content = chunk['message']['content']
                            full_response += content
                            # 将每个 token 包装为 JSON 并添加换行符
                            yield json.dumps({
                                "token": content,
                                "session_id": session_id,
                                "is_complete": False
                            }) + "\n"
                yield json.dumps({
                    "token": full_response,
                    "session_id": session_id,
                    "is_complete": True
                }) + "\n"
                self._save_to_db_async(db, full_response, session_id)
            return StreamingResponse(
                generate(),
                media_type='application/x-ndjson'
            )
        except requests.exceptions.RequestException as e:
            return JSONResponse(
                status_code=500,
                content={"error": f"请求失败: {str(e)}"}
            )

    def _save_to_db_async(self, db, content, session_id):
        import threading
        def save_task():
            try:
                create_new_chat_records(
                    db=db,
                    content=content,
                    session_id=session_id,
                    role=2
                )
            except Exception as e:
                print(f"数据库保存失败: {e}")

        threading.Thread(target=save_task).start()
