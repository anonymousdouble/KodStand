import os, json
import re
import shutil
import sys

from gpt_agent_028 import GPTAgent

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
import util


dsl = """RuleSet ::= Rule1 [And|Or|; Rule2]* # And means should satisfy Rule1 and Rule2. Or means can satisfy Rule1 or Rule2. ; means Rule1,Rule2 belongs to diffent groups
Rule ::= {{'Optional'| 'Mandatory'}} [ ['Order' of | 'Number' of] TermList [Operator TermList]* | Rule1 '->' Rule2] [ExceptionRule] #'Order' of  means order rule, 'Number' of means numberConstraint, Rule1 '->' Rule2 means if Rule1 then Rule2
ExceptionRule ::= 'Except ' TermList | Rule # means rules not applied to TermList | Rule
Operator = 'is'| 'is not' | '>=' | '<=' | '=' | '!=' | 'for' | 'not for' | 'before' | 'not before' | 'after' | 'not after' | 'between' | 'not between' | 'have' | 'not have' | 'Add' | 'Sub' | 'Mult' | MatMult | 'Div' | 'Mod' | 'Pow' | 'LShift' | 'RShift' | 'BitOr' | 'BitXor' | 'BitAnd' | 'FloorDiv'
TermList ::= Term [, Term]*
Modifier ::= 'some' | 'each' | 'all' | 'except' | 'first' | 'last' | ...
Term :: = JavaTerm | Modifier* Term | Term of Term
JavaTerm means the formal expression using such format [XXX] "XXX" represent a JavaTerm
"""

examples = """For Example, Analyze the following {{Style}}, please parse the {{Style}} using the given {{grammar}} to make its semantics clear and correct. {{Style}} consists of Description and configurable Options. 

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
    rule: str, DSL_Syntax: str, style="CheckStyle Rule", grammar="Grammar", example=""
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


def get_rules_from_file(file_path):
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
    rule_list = get_rules_from_file(file_path)

    # get_all_gpt_res_for_java_checkstyle(
    #     rule_list,
    #     dsl,
    #     examples=examples,
    #     style="CheckStyle Rule",
    #     model="gpt-3.5-turbo-0125",
    #     output_dir="data/dsl_output/",
    # )
    res = None
    with open("data/dsl_output/checkstyle/gpt-3.5-turbo-0125_response.json") as f:
        res = json.load(f)
    prompts = None
    with open("data/dsl_output/checkstyle/gpt-3.5-turbo-0125_prompt.json") as f:
        prompts = json.load(f)
    for i,rule in enumerate(rule_list[:10]):
        with open(f"data/dsl_output/checkstyle/{i}.txt", "w") as f:
            rule_name = rule.split("\n")[1]
            f.write(prompts[rule_name])
            f.write("\n=======================================================\n")
            f.write(res[rule_name])


