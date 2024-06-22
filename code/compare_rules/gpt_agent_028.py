import os
import openai
import json
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

    def gen_dsl(
        self, rule_list, dsl, examples, prompt_processor, style, model, output_dir
    ):
        # ! test: 只取前10个rule
        result = {}
        result_simple = {}
        for rule_description in rule_list[:10]:
            rule_name = rule_description.split("\n")[1]
            print(f"generate dsl for: {rule_name}")
            prompt = prompt_processor(
                rule=rule_description, example=examples, dsl_syntax=dsl, style=style
            )
            answer = self.get_response(prompt, model=model)
            result[rule_description]=[prompt, answer]
            result_simple[rule_name]=[prompt, answer]
            break
        with open(
            os.path.join(output_dir, f"{model}_rule_prompt_response.json"), "w"
        ) as f:
            json.dump(result, f, indent=4)
        with open(
            os.path.join(output_dir, f"{model}_rule_prompt_response_simple.json"), "w"
        ) as f:
            json.dump(result_simple, f, indent=4)
