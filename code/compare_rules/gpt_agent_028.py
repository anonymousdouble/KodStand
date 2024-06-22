import os
import openai
from retry import retry

"""
需要将openai版本降至openai==0.28.1
"""
class GPTAgent:
    """
    与chatGPT进行交互
    """

    def __init__(self) -> None:
        self.api_key = "sk-proj-0W1mHlj2J2BnYHauKePhT3BlbkFJF3W9NDdOrs0BOkyaOJqh"

    @retry(delay=0, tries=6, backoff=1, max_delay=120)
    def ask(self, content, messages=[], model="gpt-3.5-turbo-0125", temperature=0):
        openai.api_key = self.api_key
        messages.append({"role": "user", "content": content})
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=temperature,
        )

        return completion.choices[0].message["content"]

    def get_response(
        self, prompt, messages=[], model="gpt-3.5-turbo-0125", temperature=0
    ):
        answer = self.ask(
            content=prompt, messages=messages, model=model, temperature=temperature
        )
        return answer
