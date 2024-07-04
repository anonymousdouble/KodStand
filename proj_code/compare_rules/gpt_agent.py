# encoding=utf-8
"""
requires openai == 1.25.0

references:
- https://github.com/openai/openai-python
- https://flowus.cn/share/bf106afc-6e3c-4b52-b7e4-bf23b3ec758

"""
from openai import OpenAI
from retry import retry
import httpx
import re
wrapper = None
class GPTAgent:

    def __init__(self) -> None:
        self.client = OpenAI(
            # api_key="sk-proj-0W1mHlj2J====2BnYHauKePhT3BlbkFJF3W9NDdOrs0BOkyaOJqh"
        )

    @retry(delay=0, tries=6, backoff=1, max_delay=120)
    def ask(self, content,examples=None,model="gpt-3.5-turbo-0125",temperature=0):
        messages = []
        if examples:
            for user_prompt, response in examples:
                messages.extend([
                    {"role": "user",
                     "content": user_prompt},
                    {"role": "assistant",
                     "content": str(response)}])
        messages.append({"role": "user", "content": content})
        completion = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        return completion.choices[0].message.content

    def get_response(self, prompt,examples=None,model="gpt-3.5-turbo-0125",temperature=0):
        answer = self.ask(prompt,examples,model,temperature)
        return answer
