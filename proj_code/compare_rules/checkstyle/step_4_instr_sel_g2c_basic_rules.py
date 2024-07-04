import copy
import os
import json
import re
import shutil
import tiktoken
import sys
from gpt_agent_028 import GPTAgent
from proj_code.compare_rules.checkstyle.dsl import dsl
import tiktoken

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
import util

examples = """For Example, respond like:
Mapping of {{Style}} to {{tool}}:
"Mandatory: [IfStatement], [ElseStatement], [ForStatement], [DoStatement], [WhileStatement] have [Brace]" : ["NeedBraces"]
"Mandatory: [body] of [IfStatement], [ElseStatement], [ForStatement], [DoStatement], [WhileStatement] is [Null] —> [IfStatement], [ElseStatement], [ForStatement], [DoStatement], [WhileStatement] have [Brace]" : []
"Mandatory: [Number] of [body] of [IfStatement], [ElseStatement], [ForStatement], [DoStatement], [WhileStatement] = 1 —> [IfStatement], [ElseStatement], [ForStatement], [DoStatement], [WhileStatement] have [Brace]" : []
"""


def preprocess_promt(
    dsl_syntax: str,
    style="RuleSet of Google Java Style Guide",
    dsl_rule_set=None,
    tool="Checkstyle",
    tool_rule_set=None,
    grammar="Grammar",
    example="",
):
    prompt = """Select the corresponding {{tool}} rules for each DSL rule from {{Style}}.

{{Style}}:
{{DSLruleset}}

{{tool}}:
{{toolruleset}}

{{grammar}}:
{{Syntax}}

Response Format:
Mapping of {{Style}} to {{tool}}:
first rule representation from {{Style}} : if exists, only give corresponding RuleName of {{tool}} as a list. otherwise, gives None
second rule representation from {{Style}} : ...
...

{{Example}}
"""

    prompt = prompt.replace("{{Example}}", example)
    prompt = prompt.replace("{{Style}}", style)
    prompt = prompt.replace("{{DSLruleset}}", dsl_rule_set)
    prompt = prompt.replace("{{tool}}", tool)
    prompt = prompt.replace("{{toolruleset}}", tool_rule_set)
    prompt = prompt.replace("{{Syntax}}", dsl_syntax)
    prompt = prompt.replace("{{grammar}}", grammar)

    return prompt


def instr_sel(
    google_dsl_results,
    model,
    checkstyle_dsl_basic_rules,
    gpt_answer_dir,
):
    agent = GPTAgent()
    print("Model:", model)
    result = {}
    # cnt = 0
    for rule,data in google_dsl_results.items():
        # cnt += 1
        # if cnt > 5:
        #     break
        print(f"select instruction for: {rule}")
        if data:
            prompt = preprocess_promt(
                dsl_syntax=dsl,
                style="RuleSet of Google Java Style Guide",
                dsl_rule_set=data,
                tool="Checkstyle",
                tool_rule_set=checkstyle_dsl_basic_rules,
                grammar="Grammar",
                example=examples,
            )
            answer = agent.get_response(prompt, model=model)
            
        else:
            answer = ""
        result[rule] = [prompt, answer]
        break
    util.save_json(gpt_answer_dir, f"{model}_rule_prompt_response", result)
    return result


def extract_basic_rule(tex):
    if "Basic Rule" in tex:
        ind = tex.index("Basic Rule")
        pre = tex[ind:].strip()
    else:
        try:
            pre = tex.split("plaintext")[1]
        except:
            pre = tex
        pre = "Basic Rule: " + pre
    basic_rule = []
    for e in pre.split("\n"):
        if e:
            basic_rule.append(e)
        else:
            break
    return "\n".join(basic_rule)



def pps_dsl(text):
    try:
        ind = text.index("Description is:")
        res = text[ind + len("Description is:") :].strip()
    except:
        try:
            ind = text.index(":")
            res = text[ind + 1 :].strip()
        except:
            res = text
    return res


def get_google_rule_dsl(google_dsl_json):
    """
    只是预处理一下response？
    """
    google_rule_dsl = {}
    # cnt = 0
    for rule, [_, response] in google_dsl_json.items():
        # cnt += 1
        # if cnt > 5:
        #     break
        ppsed_dsl = pps_dsl(response)
        if "NO RULE" in ppsed_dsl:
            google_rule_dsl.append([rule, ""])
            continue
        google_rule_dsl[rule] = ppsed_dsl
    return google_rule_dsl

def get_checkstyle_basic_rules(all_checkstyle_dsls):
    """
    将所有GPT生成的DSL，提取其中的Basic Rule，并序列化为string返回
    """
    checkstyle_dsl_basic_rules = "\n\n".join(
        [
            "RuleName: " + name + "\n" + extract_basic_rule(dsl_text)
            for name, [_, dsl_text] in all_checkstyle_dsls.items()
        ]
    )
    return checkstyle_dsl_basic_rules

def check_sel_result(google_dsls_results, instr_sel_result_simple, benchmark):
    """
    检查指令选择结果是否正确
    """
    correct_count, wrong_count = 0, 0
    for rule, _ in google_dsls_results.items():
        bm_config = benchmark[rule]
        res = instr_sel_result_simple[rule][1]
        if bm_config:
            checkstyle_modules = [module["modulename"] for module in bm_config]
            for rule_name in checkstyle_modules:
                if rule_name not in res:
                    wrong_count += 1
                    break
            else:
                correct_count += 1
        else:
            if res == "":
                correct_count += 1
            else:
                if "None" not in res.split(":")[-1]:
                    print(f"Rule: \n{rule}")
                    # print("BM res: \n", bm_config)
                    print("Selection result: \n", res)
                    wrong_count += 1
    print(f"Correct count: {correct_count}, Wrong count: {wrong_count}")

if __name__ == "__main__":
    #! 统一用simple.json
    all_checkstyle_dsls = util.load_json(
        "data/dsl_output/checkstyle_advanced/extracted/", "gpt-4o_extracted"
    )
    checkstyle_dsl_basic_rules = get_checkstyle_basic_rules(all_checkstyle_dsls)
    google_dsl_json = util.load_json(
        "data/dsl_output/google/extracted/", "gpt-4o_extracted"
    )
    google_dsls_results = get_google_rule_dsl(google_dsl_json)
    instr_sel_output_dir = "data/dsl_output/instr_sel/"
    # ! online
    instr_sel_result = instr_sel(
        google_dsls_results,
        model="gpt-4o",
        checkstyle_dsl_basic_rules=checkstyle_dsl_basic_rules,
        gpt_answer_dir=instr_sel_output_dir,
    )
    # ! offline
    # instr_sel_result = util.load_json(instr_sel_output_dir, "gpt-4o_rule_prompt_response")
    benchmark = util.load_json("data/benchmark/", "simple_benchmark")
    check_sel_result(google_dsls_results, instr_sel_result, benchmark)
