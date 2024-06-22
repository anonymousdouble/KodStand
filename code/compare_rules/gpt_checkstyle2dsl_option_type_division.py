import os
import re
import shutil
import sys
import json
from dsl import dsl
from gpt_agent_028 import GPTAgent
from code.compare_rules.gpt_checkstyle2dsl_example import (
    get_checkstyle_rules_from_file,
    get_all_gpt_res_for_java_checkstyle,
)

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
import util

option_type_division_examples = """For Example, respond like: 
Options:
allowEmptyLoopBody : No # different behaviors
allowSingleLineStatement : No # different behaviors
tokens: Yes # specify data
format: Yes # specify dataobject
ignoreCase : No #Control checking behavior
message : No #Control reporting message
"""


def preprocess_promt(
    rule: str, DSL_Syntax: str, style="CheckStyle Rule", grammar="Grammar", example=""
):

    prompt = """Analyze the following {{Style}} consisting of Description and configurable Options. 
1. Extract all OptionNames
1. Analyze description of each option of {{Style}}, determine it is a data specification.

{{Style}}:
{{Description}}

{{grammar}}:
{{Syntax}}

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
    prompt = prompt.replace("{{Syntax}}", DSL_Syntax)
    prompt = prompt.replace("{{Description}}", rule)
    prompt = prompt.replace("{{grammar}}", grammar)

    return prompt


if __name__ == "__main__":

    file_path = "data/rule/checkstyle/java/url_name_desc_opt.json"
    rule_list = get_checkstyle_rules_from_file(file_path)
    agent = GPTAgent()
    agent.gen_dsl(
        rule_list,
        dsl,
        examples=option_type_division_examples,
        prompt_processor=preprocess_promt,
        style="CheckStyle Rule",
        model="gpt-4o",
        output_dir="data/dsl_output/checkstyle_opt_div",
    )
