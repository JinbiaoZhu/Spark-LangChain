# -*- coding: utf-8 -*-
import _thread as thread
import base64
import datetime
import hashlib
import hmac
import json
from urllib.parse import urlparse
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
from dotenv import load_dotenv, find_dotenv
import os
import websocket


class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, gpt_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(gpt_url).netloc
        self.path = urlparse(gpt_url).path
        self.gpt_url = gpt_url

    # 生成url
    def create_url(self):
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"

        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.APIKey}", ' \
                               f'algorithm="hmac-sha256", ' \
                               f'headers="host date request-line", ' \
                               f'signature="{signature_sha_base64}"'

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        # 拼接鉴权参数，生成url
        url = self.gpt_url + '?' + urlencode(v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        return url


# 2023 07 28 v2
class SparkLLMBase:
    def __init__(self, max_tokens=2048, temperature=0.5):
        self.total_content_replaced = None
        load_dotenv(find_dotenv(), verbose=True)
        self.wsParam = None
        self.total_content = ''

        self.max_tokens = max_tokens
        self.temperature = temperature

        self.appid = os.getenv('appid')
        self.apikey = os.getenv('apikey')
        self.apisecret = os.getenv('apisecret')
        self.gpt_url = os.getenv('gpt_url')

        self.chat_history = []

    def __call__(self, inprompt: str):
        return self.call_function(inprompt)

    def call_function(self, prompt: str):
        self._add_to_chat_history('user', prompt)
        self.wsParam = Ws_Param(APPID=self.appid,
                                APIKey=self.apikey,
                                APISecret=self.apisecret,
                                gpt_url=self.gpt_url)
        websocket.enableTrace(False)
        wsUrl = self.wsParam.create_url()
        ws = websocket.WebSocketApp(wsUrl,
                                    on_message=self._on_message,
                                    on_error=self._on_error,
                                    on_close=self._on_close,
                                    on_open=self._on_open)
        ws.appid = self.appid
        ws.question = prompt
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        response_to_return = self.total_content_replaced
        self._add_to_chat_history('assistant', response_to_return)
        self.total_content_replaced = ''
        return response_to_return

    def _add_to_chat_history(self, role, content):
        assert role == "user" or role == "assistant"
        self.chat_history += [{'role': role, 'content': content}]

    def _on_error(self, ws, error):
        print("### error:", error)

    # 收到websocket关闭的处理
    def _on_close(self, ws, *args):
        response = self.total_content
        response_format = self._format_print(10)
        self.total_content = ''
        # print(response_format)
        # print("\n### closed ###")
        return response

    def _gen_params(self, appid, question):
        """
        通过appid和用户的提问来生成请参数
        """
        data = {
            "header": {
                "app_id": appid,
                "uid": "1234"
            },
            "parameter": {
                "chat": {
                    "domain": "general",
                    "random_threshold": self.temperature,
                    "max_tokens": self.max_tokens,
                    "auditing": "default"
                }
            },
            "payload": {
                "message": {
                    "text": self.chat_history
                }
            }
        }
        # print('\n', data, '\n')
        return data

    def _run(self, ws, *args):
        data = json.dumps(self._gen_params(appid=ws.appid, question=ws.question))
        ws.send(data)

    # 收到websocket连接建立的处理
    def _on_open(self, ws):
        thread.start_new_thread(self._run, (ws,))

    def _on_message(self, ws, message):
        # print(message)
        data = json.loads(message)
        code = data['header']['code']
        if code != 0:
            print(f'请求错误: {code}, {data}')
            ws.close()
        else:
            choices = data["payload"]["choices"]
            status = choices["status"]
            content = choices["text"][0]["content"]
            # print(content, end='')
            self.total_content += content
            if status == 2:
                ws.close()

    def _format_print(self, line_length=10):

        self.total_content_replaced = self.total_content.replace("\n", "")
        # 将字符串按照每行字符数切分为列表
        lines = [self.total_content_replaced[i:i + line_length]
                 for i in range(0, len(self.total_content_replaced), line_length)]

        # 将列表中的每个元素用换行符连接成一个字符串
        result = "\n".join(lines)

        return result


# --------------------- test code ---------------------
if __name__ == "__main__":
    spark_test = SparkLLMBase(max_tokens=2048,
                              temperature=0.1)
    # ----------- test case 1 -----------
    # prompt = "How big is the earth?"
    # r = spark_test(prompt)
    # print(r)

    # ----------- test case 2 -----------
    # while True:
    #     user_question = input("用户：")
    #     ai_response = spark_test(user_question)
    #     print("星火认知大模型：", ai_response)
    #
    #     if user_question == '':
    #         break
