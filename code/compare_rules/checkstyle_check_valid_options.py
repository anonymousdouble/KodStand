import os
import re
import shutil
import sys
import json
from dsl import dsl
from gpt_agent_028 import GPTAgent
from checkstyle2dsl import get_checkstyle_rules_from_file


root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
import util

option_cls_examples = """For Example, respond like: 
Options:
allowEmptyLoopBody : No # different behaviors
allowSingleLineStatement : No # different behaviors
tokens: Yes # specify data
format: Yes # specify dataobject
ignoreCase : No #Control checking behavior
message : No #Control reporting message
"""


def preprocess_prompt(
    rule: str, style="CheckStyle Rule", example=""
):

    prompt = """Analyze the following {{Style}} consisting of Description and configurable Options. 
1. Extract all OptionNames
1. Analyze description of each option of {{Style}}, determine it is a data specification.

{{Style}}:
{{Description}}

Response Format:
If there are no Options, please respond "No Option"
Otherwise, respond like:
Options:
OptionName1:  Yes or No
...
OptionNamek:  Yes or No

{{Example}}
"""

    prompt = prompt.replace("{{Example}}", example)
    prompt = prompt.replace("{{Style}}", style)
    prompt = prompt.replace("{{Description}}", rule)

    return prompt


if __name__ == "__main__":

    file_path = "data/rule/checkstyle/java/url_name_desc_opt.json"
    rule_list = get_checkstyle_rules_from_file(file_path)
    agent = GPTAgent()
    pargs = {
        "example": option_cls_examples,
        "style": "CheckStyle Rule",
    }
    for model in ["gpt-4o", "gpt-3.5-turbo-0125"]:
        agent.gen_response_of_rules(
            rule_list=rule_list,
            pargs=pargs,
            prompt_processor=preprocess_prompt,
            model=model,
            output_dir="data/valid_checkstyle_options",
        )
