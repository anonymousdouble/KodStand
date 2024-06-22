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
            # api_key="sk-proj-vrNPSb5ttqXsOV39pl7FT3BlbkFJ93LlRultIv7DLd7Pwe8e"
            # api_key="sk-proj-0W1mHlj2J2BnYHauKePhT3BlbkFJF3W9NDdOrs0BOkyaOJqh"
        )
        # self.client = OpenAI(
        #     base_url="https://api.xty.app/v1",
        #     api_key="sk-APsNwhpxXA7mMY24AfC2907d8cDa4798B37b53B38a6bBc14",
        #     http_client=httpx.Client(
        #             base_url="https://api.xty.app/v1",
        #             follow_redirects=True,
        #     ),
        # )

    @retry(delay=0, tries=6, backoff=1, max_delay=120)
    def ask(self, content,examples=None,model="gpt-3.5-turbo-0125",temperature=0):
        messages = []
        # if isinstance(content,list):
        #     for i,each_prompt in enumerate(content):
        #         if i%2:
        #             messages.append({"role": "user", "content": content})
        #         else:
        #             messages.append({"role": "user", "content": content})
        if examples:
            '''
            https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb
              {"role": "user", "content": "Help me translate the following corporate jargon into plain English."},
            {"role": "assistant", "content": "Sure, I'd be happy to!"},
            '''
            for user_prompt, response in examples:
                messages.extend([
                    {"role": "user",
                     "content": user_prompt},
                    {"role": "assistant",
                     "content": str(response)}])
        messages.append({"role": "user", "content": content})
        # print(">>>>messages: ",messages)
        completion = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            # response_format={"type": "json_object"}
        )
        # print(completion)
        return completion.choices[0].message.content

    def get_response(self, prompt,examples=None,model="gpt-3.5-turbo-0125",temperature=0):
        '''
        Answer: You respond with Yes or No for whether exists an ESLint configuration for the given style convention
        Configuration:
        rule-name: ['error', {
          option1: value1,
          ...
          optionn: valuen
        }]
        '''
        # if model == 'gpt-4o':
        #     self.client = OpenAI(api_key="sk-proj-0W1mHlj2J2BnYHauKePhT3BlbkFJF3W9NDdOrs0BOkyaOJqh")
        # else:
        #     self.client = OpenAI(
        #         base_url="https://api.xty.app/v1",
        #         api_key="sk-APsNwhpxXA7mMY24AfC2907d8cDa4798B37b53B38a6bBc14",
        #         http_client=httpx.Client(
        #                 base_url="https://api.xty.app/v1",
        #                 follow_redirects=True,
        #         ),
        #     )
        answer = self.ask(prompt,examples,model,temperature)
        return answer
        # if len(eslint_rules_simple) > 0:
        #     # question = "Given a rule:\n\n"
        #     # question += rule
        #     # question += "Can you find a corresponding rule in the following rule set?\n\n"
        #     # question += eslint_rules_simple
        #     answer = self.wrapper.ask(prompt)
        #     print(answer)

class GPTWrapper:

    def __init__(self) -> None:
        self.client = OpenAI(
            api_key="sk-proj-vrNPSb5ttqXsOV39pl7FT3BlbkFJ93LlRultIv7DLd7Pwe8e"

        )
        # self.client = OpenAI(
        #     base_url="https://api.xty.app/v1",
        #     api_key="sk-proj-vrNPSb5ttqXsOV39pl7FT3BlbkFJ93LlRultIv7DLd7Pwe8e",
        #     http_client=httpx.Client(
        #             base_url="https://api.xty.app/v1",
        #             follow_redirects=True,
        #     ),
        # )

    @retry(delay=0, tries=6, backoff=1, max_delay=120)
    def ask(self, content, cot_pattern=[]):
        messages =[]
        messages.append({"role": "user", "content": content})
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=messages,
            temperature=0,
            response_format={"type": "json_object"}
        )
        # print(completion)
        return completion.choices[0].message.content
