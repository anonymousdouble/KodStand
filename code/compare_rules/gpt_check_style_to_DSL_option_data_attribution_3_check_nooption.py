import os
import re
import shutil
import sys
import json

from gpt_agent_028 import GPTAgent
from gpt_check_style_to_DSL_example import get_rules_from_file,get_all_gpt_res_for_java_checkstyle
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
import util

dsl = """RuleSet ::= Rule1 [And|Or|; Rule2]* # And means should satisfy Rule1 and Rule2. Or means can satisfy Rule1 or Rule2. ; means Rule1,Rule2 belongs to diffent groups
Rule ::= {{'Optional'| 'Mandatory'}} [ ['Order' of | 'Number' of] TermList [Operator TermList]* | Rule1 '->' Rule2] [ExceptionRule] #'Order' of  means order rule, 'Number' of means numberConstraint, Rule1 '->' Rule2 means applying Rule2 under the premise of Rule1 
ExceptionRule ::= 'Except ' TermList | Rule # means rules not applied to TermList | Rule # means rules not applied to TermList | Rule
Operator = 'is'| 'is not' | '>=' | '<=' | '=' | '!=' | 'for' | 'not for' | 'before' | 'not before' | 'after' | 'not after' | 'between' | 'not between' | 'have' | 'not have' | 'Add' | 'Sub' | 'Mult' | MatMult | 'Div' | 'Mod' | 'Pow' | 'LShift' | 'RShift' | 'BitOr' | 'BitXor' | 'BitAnd' | 'FloorDiv'
TermList ::= Term [, Term]*
Modifier ::= 'some' | 'each' | 'all' | 'except' | 'first' | 'last' | ...
Term :: = JavaTerm | Modifier* Term | Term of Term
JavaTerm means the formal expression using such format [XXX] "XXX" represent a JavaTerm
"""

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
    # '''

    prompt = prompt.replace("{{Example}}", example)
    prompt = prompt.replace("{{Style}}", style)
    prompt = prompt.replace("{{Syntax}}", DSL_Syntax)
    prompt = prompt.replace("{{Description}}", rule)
    prompt = prompt.replace("{{grammar}}", grammar)

    return prompt


def get_all_gpt_res_for_java_checkstyle(
    rule_list, dsl, examples, style, model, output_dir
):

    agent = GPTAgent()
    result = {}
    prompts = {}
    for rule_description in rule_list[:10]:
        rule_name = rule_description.split("\n")[1]
        print(f"generate dsl for: {rule_name}")

        prompt = preprocess_promt(
            rule=rule_description, example=examples, DSL_Syntax=dsl, style=style
        )
        answer = agent.get_response(prompt, model=model)
        result[rule_name] = answer
        prompts[rule_name] = prompt
    with open(os.path.join(output_dir, f"{model}_prompt.json"), "w") as f:
        json.dump(prompts, f, indent=4)
    with open(os.path.join(output_dir, f"{model}_response.json"), "w") as f:
        json.dump(result, f, indent=4)


if __name__ == "__main__":



    get_all_gpt_res_for_java_checkstyle(
        rule_list, dsl, examples=option_type_division_examples, style="CheckStyle Rule", model="gpt-4o"
    )

    checkstyle_options_classify = []
    for i in range(len(os.listdir(gpt_answer_dir))):
        data = util.load_json(gpt_answer_dir, str(i))
        checkstyle_options_classify.append(data)
    util.save_json(
        util.data_root + "gpt_dsl_answer/",
        "checkstyle_options_classify_3_check_nooption",
        checkstyle_options_classify,
    )
