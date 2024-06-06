# encoding=utf-8
"""
requires openai == 1.25.0

references:
- https://github.com/openai/openai-python
- https://api.xty.app

"""
from openai import OpenAI
import httpx
import re
wrapper = None


class GPTWrapper:

    def __init__(self) -> None:
        self.client = OpenAI(
            base_url="https://api.xty.app/v1",
            # api_key="sk-APsNwhpxXA7mMY24AfC2907d8cDa4798B37b53B38a6bBc14",
            http_client=httpx.Client(
                    base_url="https://api.xty.app/v1",
                    follow_redirects=True,
            ),
        )

    def ask(self, content, cot_pattern=[]):
        messages = cot_pattern.copy()
        messages.append({"role": "user", "content": content})
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0,
        )
        return completion.choices[0].message.content

    @classmethod
    def get_wrapper(cls):
        global wrapper
        if wrapper is None:
            wrapper = GPTWrapper()
        return wrapper
