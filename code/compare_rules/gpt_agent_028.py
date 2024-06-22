import os
import openai
from retry import retry

class GPTAgent:
    """
    与chatGPT进行交互
    """

    def __init__(self) -> None:
        self.api_key = "sk-proj-0W1mHlj2J2BnYHauKePhT3BlbkFJF3W9NDdOrs0BOkyaOJqh"

    @retry(delay=0, tries=6, backoff=1, max_delay=120)
    def ask(self, content, model="gpt-3.5-turbo-0125",temperature=0):
        openai.api_key = self.api_key
        messages = []
        messages.append({"role": "user", "content": content})
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=temperature,
        )

        return completion.choices[0].message["content"]
    
    def get_response(self, prompt,examples=None,model="gpt-3.5-turbo-0125",temperature=0):
        answer = self.ask(prompt,examples,model,temperature)
        return answer