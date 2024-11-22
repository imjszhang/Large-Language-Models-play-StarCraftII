import requests
from typing import List, Dict, Any, Tuple
import os
import time
import random


class ChatBot_MultiTurn:
    """
    ChatBot类,用于对话
    调用DIFY的API接口,实现对话
    query方法用于对话
    """

    def __init__(self, model_name, api_key, api_base, temperature, system_prompt, example):
        """
        __init__方法,初始化ChatBot类
        :param api_key: DIFY的API密钥
        :param api_base: DIFY的API基础URL
        :param system_prompt: 系统提示语
        :param example: 例子,用于初始化对话,格式为[用户输入,机器人回复]
        """
        self.model_name = model_name
        self.temperature = temperature

        self.api_key = api_key
        self.api_base = api_base
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.system_prompt = system_prompt
        self.example = example
        self.conversation_id = None  # 用于多轮对话的会话ID

    def query(self, user_input):
        """
        query方法,用于对话
        :param user_input: 用户输入
        :return: 机器人回复
        """
        url = f"{self.api_base}/chat-messages"
        payload = {
            "query": user_input,
            "inputs": {
                "system": self.system_prompt,
                "user": self.example[0],
                "assistant": self.example[1]
            },
            "response_mode": "blocking",
            "user": "unique_user_id",  # 替换为实际用户标识
        }

        # 如果是多轮对话，传递 conversation_id
        if self.conversation_id:
            payload["conversation_id"] = self.conversation_id

        response = requests.post(url, json=payload, headers=self.headers)

        if response.status_code == 200:
            data = response.json()
            self.conversation_id = data.get("conversation_id")  # 保存会话ID
            return data["answer"]
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return "I'm sorry, but I am unable to provide a response at this time due to technical difficulties."


class ChatBot_SingleTurn:
    """
    ChatBot类,用于单轮对话
    调用DIFY的API接口,实现对话
    query方法用于对话
    """

    def __init__(self, model_name, api_key, api_base, temperature, system_prompt, example_prompt):
        """
        __init__方法,初始化ChatBot类
        :param api_key: DIFY的API密钥
        :param api_base: DIFY的API基础URL
        :param system_prompt: 系统提示语
        :param example_prompt: 例子,用于初始化对话,格式为[用户输入,机器人回复]
        """
        self.model_name = model_name
        self.temperature = temperature

        self.api_key = api_key
        self.api_base = api_base
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.system_prompt = system_prompt
        self.example = example_prompt

    def query(self, user_input, max_retries=5):
        """
        query方法,用于对话
        :param user_input: 用户输入
        :return: 机器人回复
        """
        url = f"{self.api_base}/chat-messages"
        payload = {
            "query": user_input,
            "inputs": {
                "system": self.system_prompt,
                "user": self.example[0],
                "assistant": self.example[1]
            },
            "response_mode": "blocking",
            "user": "sc2_test",  # 替换为实际用户标识
        }

        # 尝试发送请求并获取回复
        for retries in range(max_retries):
            try:
                response = requests.post(url, json=payload, headers=self.headers)

                if response.status_code == 200:
                    data = response.json()
                    return data["answer"]
                else:
                    print(f"Error: {response.status_code}, {response.text}")
                    return "I'm sorry, but I am unable to provide a response at this time due to technical difficulties."
            except Exception as e:
                # 输出错误信息
                print(f"Error when calling the DIFY API: {e}")

                # 如果达到最大尝试次数，返回一个特定的回复
                if retries >= max_retries - 1:
                    print("Maximum number of retries reached. The DIFY API is not responding.")
                    return "I'm sorry, but I am unable to provide a response at this time due to technical difficulties."

                # 重试前等待一段时间，使用 exponential backoff 策略
                sleep_time = (2 ** retries) + random.random()
                print(f"Waiting for {sleep_time} seconds before retrying...")
                time.sleep(sleep_time)


if __name__ == '__main__':
    system_prompt = "You are a helpful assistant"
    example_prompt = ["Hello, who are you?", "I am a helpful assistant"]
    chat_bot = ChatBot_SingleTurn(api_key="app-testtesttest",
                                  api_base="https://test.dify.helixlife.app/v1",
                                  system_prompt=system_prompt,
                                  example_prompt=example_prompt)
    print(chat_bot.query("What is your name?"))