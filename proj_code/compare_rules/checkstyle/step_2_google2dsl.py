import os
import json
import sys
import re
import shutil
from gpt_agent_028 import GPTAgent
from proj_code.compare_rules.checkstyle.dsl import dsl

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
import util


example_google_rule = """
4.1.1 Use of optional braces
Braces are used with `if` , `else` , `for` , `do` and `while` statements, even when the body is empty or contains only a single statement.
Other optional braces, such as those in a lambda expression, remain optional.
"""
exmaple_gpt_response = """Final RuleSet Representation:
Mandatory: [IfStatement], [ElseStatement], [ForStatement], [DoStatement], [WhileStatement] have [Brace]
Or
Mandatory: [body] of [IfStatement], [ElseStatement], [ForStatement], [DoStatement], [WhileStatement] is [Null] 
—> [IfStatement], [ElseStatement], [ForStatement], [DoStatement], [WhileStatement] have [Brace] 
Or
Mandatory: [Number] of [body] of [IfStatement], [ElseStatement], [ForStatement], [DoStatement], [WhileStatement] = 1
—> [IfStatement], [ElseStatement], [ForStatement], [DoStatement], [WhileStatement] have [Brace]
"""

basic_prompt = """Analyze the following {{Style}}, please parse the style using the given {{grammar}} to make its semantics clear and correct.

1. Analyze whether each sentence is a rule and then classify it as mandatory or optional. If the rule is subjective, do not classify it as a rule.
2. When parsing the rule using a given {{grammar}}, pay attention to map to suitable formal Java term and select appropriate real operator characters. 

{{Style}}:
{{Description}}

{{grammar}}:
{{Syntax}}
"""


def preprocess_promt(
    rule: str,
    dsl_syntax: str,
    style="Google Java Style Guide",
    grammar="Grammar",
):
    prompt = basic_prompt
    prompt = prompt.replace("{{Style}}", style)
    prompt = prompt.replace("{{Syntax}}", dsl_syntax)
    prompt = prompt.replace("{{Description}}", rule)
    prompt = prompt.replace("{{grammar}}", grammar)
    return prompt


def get_all_gpt_res_for_java_google(rule_list, model, output_dir):
    """
    example采用cot形式
    """
    agent = GPTAgent()
    result = {}
    result_simple = {}
    for rule_description in rule_list:
        rule_name = rule_description.split("\n")[1]
        print(f"generate dsl for: {rule_name}")
        example_prompt = preprocess_promt(
            rule=example_google_rule,
            dsl_syntax=dsl,
        )
        exmaples = [[example_prompt, exmaple_gpt_response]]
        prompt = preprocess_promt(
            rule=rule_description,
            dsl_syntax=dsl,
        )
        answer = agent.get_response_with_examples(prompt, exmaples, model)
        result[rule_description] = [prompt, answer]
        result_simple[rule_name] = [prompt, answer]
    with open(os.path.join(output_dir, f"{model}_rule_prompt_response.json"), "w") as f:
        json.dump(result, f, indent=4)
    with open(
        os.path.join(output_dir, f"{model}_rule_prompt_response_simple.json"), "w"
    ) as f:
        json.dump(result_simple, f, indent=4)


if __name__ == "__main__":
    agent = GPTAgent()
    models = ["gpt-4o"]
    gpt_answer_dir = "data/dsl_output/google/"
    all_rules = util.load_json(
        "data/benchmark/",
        "benchmark",
    )
    rule_list = ["\n" + k for k, _ in all_rules.items()]
    for model in models:
        get_all_gpt_res_for_java_google(rule_list, model, gpt_answer_dir)
