import copy
import os
import json
import re
import shutil
import tiktoken
import sys
from gpt_agent_028 import GPTAgent
from proj_code.compare_rules.checkstyle.dsl import dsl

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
import util

examples = """For example, Given {{Style}},
```plaintext
RuleSet ::= 
    Mandatory: Order of [LicenseOrCopyrightInformation, PackageStatement, ImportStatements, TopLevelClass]
    And
    Mandatory: Number of [BlankLine] = 1 for [Section]
```
You should respond like
for the first rule "Mandatory: Order of [LicenseOrCopyrightInformation, PackageStatement, ImportStatements, TopLevelClass]", 
it doesn't corresponds to rule of CustomImportOrder of {{tool}} "Mandatory: Order of [import groups] is {{customImportOrderRules}}". Although CustomImportOrder and "Mandatory: Order of [LicenseOrCopyrightInformation, PackageStatement, ImportStatements, TopLevelClass]" are both Mandatory rule and same behavior semantics, but the objects that rules are different,   one is [LicenseOrCopyrightInformation, PackageStatement, ImportStatements, TopLevelClass], the other [import groups]. So "Mandatory: Order of [LicenseOrCopyrightInformation, PackageStatement, ImportStatements, TopLevelClass]" cannot correspond to rulename CustomImportOrder of {{tool}}.
So the configuration is as follows:
RuleName: None

for the second rule "Mandatory: Number of [BlankLine] = 1 for [Section]",
it correpsonds to EmptyLineSeparator of {{tool}}, first types are both Mandatory, and have same semantics. For objects, [Section] corresponds to {{tokens}} of {{tool}}. So we also need to determine corresponding values of {{tokens}}. the [Section] corresponds to [LicenseOrCopyrightInformation, PackageStatement, ImportStatements, TopLevelClass], where LicenseOrCopyrightInformation don't exists corresponding value in value range of {{tokens}}, PackageStatement corresponds to PACKAGE_DEF, ImportStatements corresponds to IMPORT and STATIC_IMPORT, TopLevelClass corresponds to CLASS_DEF, so the {{tokens}} should be 'PACKAGE_DEF, IMPORT, STATIC_IMPORT, CLASS_DEF'.
So the configuration is as follows:
RuleName: "EmptyLineSeparator";
Option that is data specification:
{{tokens}}: 'PACKAGE_DEF, IMPORT, STATIC_IMPORT, CLASS_DEF';
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
    prompt = """For each rule in the following {{Style}}, determine if there are corresponding rules in {{tool}} with the same semantics.

{{Style}} expressed in {{grammar}}. 
{{tool}} consists of RuleName, Basic Rule expressed in {{grammar}}, Option Rule and Options that is data specification. Each option rule consists of OptionName and different values have different DSL rules expressed in {{grammar}}. Option that is data specification consists of OptionName, Data Type, Value Range, Default Value.
Identify if each rule in {{Style}} has a semantically equivalent rule from Basic Rule or Option Rule of {{tool}} . 
1. Extract each rule in {{Style}}, and extract basic rule and option rule in {{tool}}, and determine possible matching rule from basic rule and option rule in {{tool}}.
2. for each rule in {{Style}}, the type of matching rule in {{tool}} is same (both Optional/Mandatory).
3. If yes, determine whether objects that the rule in {{Style}} checks is same as objects that the matching rule in {{tool}} checks.
4. If yes, analyze whether semantic of the rule in {{Style}} is same as the semantic of matching rule in {{tool}}.
5. If objects of matching rule in {{tool}} checks corresponds optionnames from Options that are data specifications, extract corresponding optionname and set values from the value range of options that have same semantics with objects of {{Style}}.
 
{{Style}}:
{{DSLruleset}}

{{tool}}:
{{toolruleset}}

{{grammar}}:
{{Syntax}}

{{Example}}

Response Format:
Give Explanation, the give the answer
Answer: Yes or No
Configuration: If Answer is Yes, give configuration. Otherwise, give None.
each rule of {{Style}} excerpted from {{Style}} : 
if matching rule of Basic Rule from {{tool}} that have same semantics with rule of {{Style}} excerpted from {{Style}}, give 
    RuleName: corresponding rulename from {{tool}}; if not exists, give None
          
    Option that is data specification: 
    {{optionaname}}: set corresponding value based on datatype, value range and default value;
    
else if matching an option rule from {{tool}} that have same semantics with rule of {{Style}} excerpted from {{Style}}, give 
    RuleName: corresponding rulename from {{tool}}; if not exists, give None
    
    Option Rule: corresponding OptionName, OptionValue; if not exists, give None    
    
    Option that is data specification: 
    {{optionaname}}: set corresponding value based on datatype, value range and default value;
    
else if do not exist corresponding rule from {{tool}}, give None
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


def get_all_gpt_res_for_checkstyle(
    goole_dsls,
    tool_rule_set,
    model,
    output_dir,
):  
    agent = GPTAgent()
    result = {}
    for rule in goole_dsls:
        if goole_dsls[rule]:
            tool_rule_set_des = tool_rule_set[rule]
            prompt = preprocess_promt(
                dsl_syntax=dsl,
                style="RuleSet of Google Java Style Guide",
                dsl_rule_set=rule,
                tool="Checkstyle",
                tool_rule_set=tool_rule_set_des,
                grammar="Grammar",
                example="",
            )
            answer = agent.get_response(prompt, model=model)
        else:
            answer = ""
        result[rule] = [prompt, answer]
    util.save_json(
        output_dir,
        f"{model}_rule_prompt_response",
        result,
    )
    return result

def extract_basic_rule(tex):
    if "Basic Rule" in tex:
        ind = tex.index("Basic Rule") if "Basic Rule" in tex else tex.index("plaintext")
        pre = tex[ind:].strip()
    else:
        pre = tex.split("plaintext")[1]
        pre = "Basic Rule: " + pre
    basic_rule = []
    for e in pre.split("\n"):
        if e:
            basic_rule.append(e)
        else:
            break
    return "\n".join(basic_rule)


def pps_checkstyle_dsl(dir):
    checkstyle_rules = []
    for ind in range(len(os.listdir(dir))):
        gpt_dsl_rule_list = util.load_json(dir, str(ind))
        text = gpt_dsl_rule_list[str(ind)]
        basic_rule = extract_basic_rule(text)
        checkstyle_rules.append(basic_rule)
    return "\n".join(checkstyle_rules)


def pps_cs_dsl_all_results(gpt_checkstyle_dsls_dir, file_name):
    cs_rules = dict()
    gpt_cs_dsls = util.load_json(gpt_checkstyle_dsls_dir, file_name)
    for ind, (url, rule_name, text) in enumerate(gpt_cs_dsls):
        basic_rule = extract_basic_rule(text)
        cs_rules[rule_name] = basic_rule
    return cs_rules


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


def get_all_google_dsl(jdata):
    google_dsl_rules = {}
    for rule, [_,response_dsl] in jdata.items():
        checkstype_dsl = pps_dsl(response_dsl)
        if "NO RULE" in checkstype_dsl:
            google_dsl_rules[rule] = ""
        else:
            google_dsl_rules[rule] = checkstype_dsl
    return google_dsl_rules


def get_google_dsl(json_data):
    gpt_dsl_rule_list = json_data
    google_dsl_rules = []
    for ind, (url, rule_name, text) in enumerate(gpt_dsl_rule_list):
        checkstype_dsl = pps_dsl(text)
        if "NO RULE" in checkstype_dsl:
            google_dsl_rules.append([url, rule_name, ""])
            continue
        google_dsl_rules.append([url, rule_name, checkstype_dsl])
    return google_dsl_rules


def count_token(tex):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    num_tokens = len(encoding.encode(tex))
    print("num_tokens: ", num_tokens)


def parse_result(gpt_answer_dir, pure_dsl_lst, few_checkstyle_dsls, google_dsl_list):
    all_rules = ...  # csv
    bench_mark = ...  # json
    csv_output_path = ...
    csv_results = []
    for ind in range(len(os.listdir(gpt_answer_dir))):
        file_name = str(ind)
        json_res = util.load_json(gpt_answer_dir, file_name)
        res = json_res[file_name]
        one_rule = copy.deepcopy(all_rules[ind + 1])
        key = all_rules[ind + 1][1] + "\n" + all_rules[ind + 1][2]
        flag_key = None
        for key2 in bench_mark:
            if key[:20] == key2[:20]:
                flag_key = key2
                break
        rule_description = pure_dsl_lst[ind]
        if rule_description:
            tool_rule_set_des = few_checkstyle_dsls[ind]
            prompt = preprocess_promt(
                dsl_syntax=dsl,
                style="RuleSet of Google Java Style Guide",
                dsl_rule_set=rule_description,
                tool="Checkstyle",
                tool_rule_set=tool_rule_set_des,
                grammar="Grammar",
                example="",
            )

        else:
            prompt = "No need"
        one_rule.insert(3, bench_mark[flag_key] if flag_key else "None")
        one_rule.insert(3, prompt)
        one_rule.insert(3, res)
        one_rule.insert(3, google_dsl_list[ind][2])
        csv_results.append(one_rule)
    util.save_csv(
        csv_output_path,
        csv_results,
    )


if __name__ == "__main__":
    checkstyle_dsl = util.load_json(
        "data/dsl_output/checkstyle_advanced/extracted/", "gpt-4o_extracted"
    )
    checkstyle_dsl_basic_rules = {}
    for rule, data in checkstyle_dsl.items():
        checkstyle_dsl_basic_rules[rule] = data[1]
    instr_sel_result = util.load_json("data/dsl_output/instr_sel/", "gpt-4o_rule_prompt_response")
    few_checkstyle_dsls = {}
    # 根据 instruction selection 的结果，提取出可能的 checkstyle dsl
    for rule, data in instr_sel_result.items():
        if data:
            instrs = data[1]
            possible_checkstype_rules = []
            for key in checkstyle_dsl_basic_rules:
                if key in instrs:
                    key_str = key + ": " + checkstyle_dsl_basic_rules[key]
                    if key_str not in possible_checkstype_rules:
                        possible_checkstype_rules.append(
                            f'\nRuleName: "{key}"\n"{ checkstyle_dsl_basic_rules[key]}'
                        )
            if possible_checkstype_rules:
                few_checkstyle_dsls[rule] = "\n".join(possible_checkstype_rules)
            else:
                few_checkstyle_dsls[rule] = "\n".join(
                    ["No Possible Configuration Rules"]
                )
        else:
            few_checkstyle_dsls[rule] = "\n".join(["No Possible Configuration Rules"])

    google_dsl_jdata = util.load_json(
        "data/dsl_output/google/extracted/", "gpt-4o_extracted"
    )
    print("len: ", len(google_dsl_jdata))

    result = get_all_gpt_res_for_checkstyle(
        google_dsl_jdata, few_checkstyle_dsls, model="gpt-4o", output_dir="data/dsl_output/mapping/"
    )