import os
import json
import sys
import re
import shutil
from gpt_agent_028 import GPTAgent


root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
import util


google2dsl_examples = """For Example, Analyze the following {{Style}}, please parse the style using the given {{grammar}}. 

{{Style}}:
4.1.1 Use of optional braces
Braces are used with `if` , `else` , `for` , `do` and `while` statements, even when the body is empty or contains only a single statement.
Other optional braces, such as those in a lambda expression, remain optional.


Final RuleSet Representation:
Mandatory: [IfStatement], [ElseStatement], [ForStatement], [DoStatement], [WhileStatement] have [Brace]
Or
Mandatory: [body] of [IfStatement], [ElseStatement], [ForStatement], [DoStatement], [WhileStatement] is [Null] 
—> [IfStatement], [ElseStatement], [ForStatement], [DoStatement], [WhileStatement] have [Brace] 
Or
Mandatory: [Number] of [body] of [IfStatement], [ElseStatement], [ForStatement], [DoStatement], [WhileStatement] = 1
—> [IfStatement], [ElseStatement], [ForStatement], [DoStatement], [WhileStatement] have [Brace]
"""


def preprocess_promt(
    rule: str,
    dsl_syntax: str,
    style="Google Java Style Guide",
    grammar="Grammar",
    example="",
):
    prompt = """Analyze the following {{Style}}, please parse the style using the given {{grammar}} to make its semantics clear and correct.

1. Analyze whether each sentence is a rule and then classify it as mandatory or optional. If the rule is subjective, do not classify it as a rule.
2. When parsing the rule using a given {{grammar}}, pay attention to map to suitable formal Java term and select appropriate real operator characters. 

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


def get_all_gpt_res_for_java_google(rule_list, dsl, examples, style, model, output_dir):

    agent = GPTAgent()
    result = []
    result_simple = []
    for rule_description in rule_list[:10]:
        rule_name = rule_description.split("\n")[1]
        print(f"generate dsl for: {rule_name}")
        prompt = preprocess_promt(
            rule=rule_description, example=examples, dsl_syntax=dsl, style=style
        )
        answer = agent.get_response(prompt, model=model)
        res = {rule_description: [prompt, answer]}
        result.append(res)
        res_simple = {rule_name: [prompt, answer]}
        result_simple.append(res_simple)
        # break
    with open(os.path.join(output_dir, f"{model}_rule_prompt_response.json"), "w") as f:
        json.dump(res_simple, f, indent=4)
    with open(
        os.path.join(output_dir, f"{model}_rule_prompt_response_simple.json"), "w"
    ) as f:
        json.dump(res_simple, f, indent=4)


if __name__ == "__main__":
    from dsl import dsl

    agent = GPTAgent()
    models = ["gpt-4o", "gpt-3.5-turbo-0125"]
    gpt_answer_dir = "data/dsl_output/google/"
    all_rules = util.load_json(
        "data/benchmark/",
        "benchmark",
    )
    rule_list = ["\n" + k for k, _ in all_rules.items()]
    pargs = {
        "dsl_syntax": dsl,
        "example": google2dsl_examples,
        "style": "Google Java Style Guide",
    }
    for model in models:
        agent.gen_response_of_rules(
            rule_list,
            pargs,
            prompt_processor=preprocess_promt,
            model=model,
            output_dir=gpt_answer_dir,
        )
