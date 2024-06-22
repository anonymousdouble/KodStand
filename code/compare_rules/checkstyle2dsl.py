import os, json
import re
import shutil
import sys

from gpt_agent_028 import GPTAgent
from dsl import dsl
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
import util


checkstyle_dsl_examples = """For Example, Analyze the following {{Style}}, please parse the {{Style}} using the given {{grammar}} to make its semantics clear and correct. {{Style}} consists of Description and configurable Options. 

{{Style}}:
Rulename:
NeedBraces

Description
Checks for braces around code blocks.

Options:
allowEmptyLoopBody, Allow loops with empty bodies., boolean, false
allowSingleLineStatement, Allow single-line statements without braces., boolean, false
tokens, tokens to check, subset of tokens

LITERAL_DO
,
LITERAL_ELSE
,
LITERAL_FOR
,
LITERAL_IF
,
LITERAL_WHILE
,
LITERAL_CASE
,
LITERAL_DEFAULT
,
LAMBDA
.
,

LITERAL_DO
,
LITERAL_ELSE
,
LITERAL_FOR
,
LITERAL_IF
,
LITERAL_WHILE
.

Final RuleSet Representation:
Basic Rule:
{{tokens}} has [Brace] 

Option Rule:
allowEmptyLoopBody option:
False: Mandatory: [body] of {{tokens}} is not [Null]
True: Optional: [body] of {{tokens}} is [Null]

allowSingleLineStatement option:
False: Mandatory: Number of [statement] of [body] of [tokens] is 1 -> [tokens] has [Brace] 
True: Optional: Number of [statement] of [body] of [tokens] is 1 -> [tokens] not has [Brace]
"""


def preprocess_promt(
    rule: str, dsl_syntax: str, style="CheckStyle Rule", grammar="Grammar", example=""
):
    # then determine formal term of Java for objects of style and determine the appropriate operators between terms. Pay attention to
    prompt = """Analyze the following {{Style}}, please parse the {{Style}} using the given {{grammar}} to make its semantics clear and correct. {{Style}} consists of Description and configurable Options. 

1. Analyze whether each sentence of Description of {{Style}} is a rule and then classify it as mandatory or optional. If the rule is same as an option, do not need to parse it as a rule. If the rule is subjective, do not classify it as a rule. 
2. Analyze whether each option is a rule. If option is a configurable term, using {{OptionName}} to represent the term. If the option is to configure violation messages or reporting granularity, do not classify it as a rule. If the option is a rule, parse rule for each value of the option.
3. When parsing a rule using the given {{grammar}}, pay attention to map to suitable formal Java term and select appropriate real operator characters. 

{{Style}}:
{{Description}}

{{grammar}}:
{{Syntax}}

{{Example}}"""

    prompt = prompt.replace("{{Example}}", example)
    prompt = prompt.replace("{{Style}}", style)
    prompt = prompt.replace("{{Syntax}}", dsl_syntax)
    prompt = prompt.replace("{{Description}}", rule)
    prompt = prompt.replace("{{grammar}}", grammar)

    return prompt

def get_checkstyle_rules_from_file(file_path):
    with open(file_path) as f:
        jdata = json.load(f)

    rule_list = [
        (
            "\n".join(["Rulename", rule_name, description, "Options", options])
            if options
            else "\n".join(["Rulename", rule_name, description])
        )
        for url, rule_name, description, options in jdata
    ]
    
    return rule_list

if __name__ == "__main__":

    file_path = "data/rule/checkstyle/java/url_name_desc_opt.json"
    rule_list = get_checkstyle_rules_from_file(file_path)
    agent = GPTAgent()
    agent.gen_dsl(
        rule_list,
        dsl,
        examples=checkstyle_dsl_examples,
        prompt_processor=preprocess_promt,
        style="CheckStyle Rule",
        model="gpt-3.5-turbo-0125",
        output_dir="data/dsl_output/checkstyle",
    )
    res = None
    with open("data/dsl_output/checkstyle/gpt-3.5-turbo-0125_rule_prompt_response_simple.json") as f:
        res = json.load(f)
    for i,rule in enumerate(rule_list[:1]):
        with open(f"data/dsl_output/checkstyle/{i}.txt", "w") as f:
            rule_name = rule.split("\n")[1]
            f.write(res[rule_name][0])
            f.write("\n=======================================================\n")
            f.write(res[rule_name][1])