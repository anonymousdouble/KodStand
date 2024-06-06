import os
import json
import re
import shutil

import util

from openai import OpenAI
from retry import retry


def preprocess_promt(rule: str, tool_rules: str, style="CheckStyle"):
    prompt = """
    Generate {{style}} configurations based on CheckStyle rules for the following style convention.

    Style Convention:
    {{rule}}

    CheckStyle Rules:
    {{checkstyle_rules}}

    Response Format Should be a json object:
    {
        "Answer":  Respond with either Yes or No to show whether {{style}} configurations exist for the given style convention,
        "Configuration": If the answer is Yes, provide the configuration. There can be one or multiple {{style}} rules for the given style convention. The configuration format should be xml format:
        ["<module name='rulename1'>\n  <property name='id' value='id_value1'/>\n  <property name='name1' value='value1'/>\n  ...\n  <property name='name2' value='value2'/>"
        "</module>\n...\n<module name='rulename2'>\n  <property name='id' value='id_value1'/>\n  <property name='name1' value='value1'/>\n  ...\n  <property name='name2' value='value2'/>\n</module>"]
    }

    """
    prompt = prompt.replace("{{style}}", style)
    prompt = prompt.replace("{{rule}}", rule)
    prompt = prompt.replace("{{checkstyle_rules}}", tool_rules)
    return prompt


class GPTAgent:

    def __init__(self) -> None:
        self.client = OpenAI(
            api_key="sk-proj-vrNPSb5ttqXsOV39pl7FT3BlbkFJ93LlRultIv7DLd7Pwe8e"
        )

    @retry(delay=0, tries=6, backoff=1, max_delay=120)
    def ask(self, content):
        messages = []
        messages.append({"role": "user", "content": content})
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=messages,
            temperature=0,
            response_format={"type": "json_object"},
        )
        return completion.choices[0].message.content

    def get_response(self, prompt):
        """
        Answer: You respond with Yes or No for whether exists an ESLint configuration for the given style convention
        Configuration:
        rule-name: ['error', {
          option1: value1,
          ...
          optionn: valuen
        }]
        """
        answer = self.ask(prompt)
        return answer


def get_all_gpt_res_for_java_checkstyle():
    """
    1. parse each rule of style guide as a string
    2. parse all rules of style tool as a string
    3. get and save GPT results
    """
    agent = GPTAgent()
    data_dir = util.data_root + "rule/google/"
    all_rules = util.load_csv(util.data_root + "GoogleJavaStyle/googlejavastyle.csv")

    rule_list = [
        "\n".join([rule_name, description]) for url, rule_name, description in all_rules
    ]
    # html
    """
    GPT results_rule_name_descr_options
    GPT results_rule_name_descr	
    GPT results_html
    """
    check_style_rule_list = util.load_json(
        util.data_root + "style_tool_rules/",
        "checkstyle_name_completedes_options_process",
    )
    check_style_rule_list = [
        (
            "\n".join(["Rulename", rule_name, description, options])
            if options
            else "\n".join(["Rulename", rule_name, description])
        )
        for url, rule_name, description, options in check_style_rule_list
    ]
    checkstyle_str = "\n".join(check_style_rule_list)
    for ind, rule_description in enumerate(rule_list[:]):
        print(">>>>>>rule: ", rule_description)
        prompt = preprocess_promt(
            rule=rule_description, tool_rules=checkstyle_str, style="CheckStyle"
        )
        answer = agent.get_response(prompt)
        print(">>>>>>answer: ", {ind: answer})
        util.save_json(
            util.data_root
            + "gpt_direct_answer/java_checkstyle_completedes_options_process/",
            str(ind),
            {ind: answer},
        )


if __name__ == "__main__":
    get_all_gpt_res_for_java_checkstyle()
