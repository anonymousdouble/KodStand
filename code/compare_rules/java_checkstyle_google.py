import os
import json
import re
import shutil
import sys
import xml.etree.ElementTree as ET
import pandas as pd
from gpt_wrapper_new import GPTAgent

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
import util


def gen_nocheckstyle_prompt(rule: str, style="CheckStyle"):
    prompt = """Please generate {{style}} configurations based on the following style convention. Ensure that the output includes only the relevant configurations for the style convention and excludes any unrelated rules.


Style Convention:
{{rule}}

Response Format Should be a json object:
{
    "Answer":  Respond with either Yes or No to show whether {{style}} configurations exist for the given style convention,
    "Configuration": If the answer is Yes, provide the configuration. There can be one or multiple {{style}} rules for the given style convention. The configuration format should be xml format:
    "<module name='rule_name_1'>
        <property name='id' value='id_value_1'/>
        <property name='name_1' value='value_1'/>
        <property name='name_2' value='value_2'/>
        ...
        <property name='name_n' value='value_n'/>"
    "</module>
    ...
    <module name='rule_name_x'>
        <property name='id' value='id_value_1'/>
        <property name='name_1' value='value_1'/>
        <property name='name_2' value='value_2'/>
        ...
        <property name='name_m' value='value_m'/>
    </module>"
}

Example:

{
    "Answer": "Yes",
    "Configuration":
    <module name="OperatorWrap">
        <property name="option" value="NL"/>
        <property name="tokens" value="EQUAL, NOT_EQUAL"/>
    </module>
    <module name="SeparatorWrap">
        <property name="id" value="SeparatorWrapNL"/>
        <property name="tokens" value="DOT, METHOD_REF"/>
        <property name="option" value="nl"/>
    </module>
    <module name="SeparatorWrap">
        <property name="id" value="SeparatorWrapEOL"/>
        <property name="tokens" value="COMMA, LPAREN"/>
        <property name="option" value="EOL"/>
    </module>
    <module name="MethodParamPad">
        <property name="allowLineBreaks" value="true"/>
        <property name="option" value="space"/>
        <property name="tokens" value="CTOR_DEF"/>
    </module>
}
"""
    prompt = prompt.replace("{{style}}", style)
    prompt = prompt.replace("{{rule}}", rule)
    return prompt


def gen_prompt(rule: str, tool_rules: str, style="CheckStyle"):
    prompt = """Please generate {{style}} configurations based on the following style convention and CheckStyle rules. Ensure that the output includes only the relevant configurations for the style convention and excludes any unrelated rules.


Style Convention:
{{rule}}

CheckStyle Rules:
{{checkstyle_rules}}

Response Format Should be a json object:
{
    "Answer":  Respond with either Yes or No to show whether {{style}} configurations exist for the given style convention,
    "Configuration": If the answer is Yes, provide the configuration. There can be one or multiple {{style}} rules for the given style convention. The configuration format should be xml format:
    "<module name='rule_name_1'>
        <property name='id' value='id_value_1'/>
        <property name='name_1' value='value_1'/>
        <property name='name_2' value='value_2'/>
        ...
        <property name='name_n' value='value_n'/>"
    "</module>
    ...
    <module name='rule_name_x'>
        <property name='id' value='id_value_1'/>
        <property name='name_1' value='value_1'/>
        <property name='name_2' value='value_2'/>
        ...
        <property name='name_m' value='value_m'/>
    </module>"
}

Example:

{
    "Answer": "Yes",
    "Configuration":
    <module name="OperatorWrap">
        <property name="option" value="NL"/>
        <property name="tokens" value="EQUAL, NOT_EQUAL"/>
    </module>
    <module name="SeparatorWrap">
        <property name="id" value="SeparatorWrapNL"/>
        <property name="tokens" value="DOT, METHOD_REF"/>
        <property name="option" value="nl"/>
    </module>
    <module name="SeparatorWrap">
        <property name="id" value="SeparatorWrapEOL"/>
        <property name="tokens" value="COMMA, LPAREN"/>
        <property name="option" value="EOL"/>
    </module>
    <module name="MethodParamPad">
        <property name="allowLineBreaks" value="true"/>
        <property name="option" value="space"/>
        <property name="tokens" value="CTOR_DEF"/>
    </module>
}
"""
    prompt = prompt.replace("{{style}}", style)
    prompt = prompt.replace("{{rule}}", rule)
    prompt = prompt.replace("{{checkstyle_rules}}", tool_rules)
    return prompt


str_types = [
    "empty",
    "name",
    # "name_desc",
    # "name_desc_mopt",
    "name_sdesc_mopt",
    "name_url",
    "name_url_sdesc",
    "name_sdesc",
]


def get_checkstyle_str(opt):
    def empty():
        """
        empty
        """
        return ""

    def name():
        """
        name
        """
        fname = "url_name_sdesc_mopt"
        jdata = util.load_json("data/rule/checkstyle/java/", fname)
        name_str = "\n".join(
            [f"[Rule]\n{rule[1]}" for rule in jdata]
        )
        return name_str

    def name_desc():
        """
        name & description
        """
        fname = "url_name_desc_mopt"
        jdata = util.load_json("data/rule/checkstyle/java/", fname)
        name_desc_list = []
        for rule in jdata:
            rule_name = rule[1]
            rule_desc = rule[2]
            prefix = "Description"
            if rule_desc.startswith(prefix):
                rule_desc = rule_desc[len(prefix):]
            rule_desc = rule_desc.strip()
            name_desc_list.append(
                f"[Rule]\n{rule_name}\n[Description]\n{rule_desc}")
        name_desc_str = "\n".join(name_desc_list)
        return name_desc_str

    def name_desc_mopt():
        """
        name & description & modified options
        """
        fname = "url_name_desc_mopt"
        jdata = util.load_json("data/rule/checkstyle/java/", fname)
        name_desc_mopt_list = []
        for rule in jdata:
            rule_name = rule[1]
            rule_desc = rule[2]
            prefix = "Description"
            if rule_desc.startswith(prefix):
                rule_desc = rule_desc[len(prefix):]
            rule_desc = rule_desc.strip()
            rule_str = f"[Rule]\n{rule_name}\n[Description]\n{rule_desc}"
            if len(rule) == 4:
                rule_str += f"\n[Options]{rule[3]}"
            name_desc_mopt_list.append(rule_str)
        name_desc_mopt_str = "\n".join(name_desc_mopt_list)
        return name_desc_mopt_str

    def name_sdesc_mopt():
        """
        name & short description & modified options
        """
        fname = "url_name_sdesc_mopt"
        jdata = util.load_json("data/rule/checkstyle/java/", fname)
        jlist = []
        for rule in jdata:
            rule_str = f"[Rule]\n{rule[1]}"
            rule_str += f"\n[Description]\n{re.sub('[ ]+',' ',rule[2])}"
            if len(rule) == 4:
                rule_str += f"\n[Options]{rule[3]}"
            jlist.append(rule_str)
        name_sdesc_mopt_str = "\n".join(jlist)
        return name_sdesc_mopt_str

    def name_url():
        """
        name & url
        """
        fname = "url_name_sdesc_mopt"
        jdata = util.load_json("data/rule/checkstyle/java/", fname)
        name_url_str = "\n".join(
            [f"[Rule]\n{rule[1]}\n[URL]\n{rule[0]}" for rule in jdata]
        )
        return name_url_str

    def name_url_sdesc():
        """
        name & url & short description
        """
        fname = "url_name_sdesc_mopt"
        jdata = util.load_json("data/rule/checkstyle/java/", fname)
        name_url_sdesc_str = "\n".join(
            [
                f"[Rule]\n{rule[1]}\n[URL]\n{rule[0]}\n[Description]\n{re.sub('[ ]+',' ',rule[2])}"
                for rule in jdata
            ]
        )
        return name_url_sdesc_str

    def name_sdesc():
        """
        name & short description
        """
        fname = "url_name_sdesc_mopt"
        jdata = util.load_json("data/rule/checkstyle/java/", fname)
        name_sdesc_str = "\n".join(
            [
                f"[Rule]\n{rule[1]}\n[Description]\n{re.sub('[ ]+',' ',rule[2])}"
                for rule in jdata
            ]
        )
        return name_sdesc_str

    for options in str_types:
        if options == opt:
            return locals()[options]()

    raise Exception(f"Invalid option: {opt}")


def get_all_gpt_res_for_java_checkstyle(opt, model, rules):
    """
    1. parse each rule of style guide as a string
    2. parse all rules of style tool as a string
    3. get and save GPT results
    """
    agent = GPTAgent()
    checkstyle_str = get_checkstyle_str(opt)
    answer_dict = {}
    print(f"baseline: {opt}")
    print(f"model: {model}")
    for _, row in rules.iterrows():
        rule_name = row.rule
        rule_desc = row.desc
        print(f"rule_name: {rule_name}")
        if opt == "empty":
            prompt = gen_nocheckstyle_prompt(rule=f"{rule_name}\n{rule_desc}")
        else:
            prompt = gen_prompt(
                rule=f"{rule_name}\n{rule_desc}",
                tool_rules=checkstyle_str,
                style="CheckStyle",
            )
        #! check prompt
        # with open(f"{opt}_prompt.txt", "w") as f:
        #     f.write(prompt)
        #     return
        try:
            if model == "3.5":
                answer = agent.get_response(prompt)
            else:
                answer = agent.get_response(prompt, model="gpt-4o")
        except Exception as e:
            print(f"failed to get response for rule: {rule_name}")
            continue
        if answer.startswith("```json\n"):
            answer = answer[len("```json\n"):]
        if answer.endswith("\n```"):
            answer = answer[:-len("\n```")]
        answer_dict[rule_name] = answer
        # break

    return answer_dict

def offline_res(model:str, opt:str):
    res = util.load_json(f"data/gpt_answer/{model}/", opt)
    return res

if __name__ == "__main__":
    all_rules = pd.read_excel(
        "data/benchmark/checkstyle2google_java_benchmark.xlsx")
    for model in ["3.5", "4o"]:
        for str_type in str_types:
            # gpt_answers = get_all_gpt_res_for_java_checkstyle(
            #     str_type, model, all_rules)
            if model == "4o" and "mopt" in str_type:
                aa = 1
            gpt_answers = offline_res(model,str_type)
            csv_results = []
            for index, row in all_rules.iterrows():
                rule_name = row.rule
                if rule_name == "2.3.2 Special escape sequences":
                    aa = 2
                answer = ""
                csv_results.append(
                    [rule_name, row.desc, row.res if row.res == row.res else ""])
                if gpt_answers.get(rule_name):
                    answer = gpt_answers[rule_name]
                    try:
                        json_object = json.loads(answer)
                        y_or_n = json_object["Answer"]
                        ET.fromstring(json_object["Configuration"])
                        csv_results[-1].append(y_or_n)
                        csv_results[-1].append(json_object["Configuration"])
                    except:
                        if "'Answer': 'Yes'" in answer:
                            idx_start = answer.find("<module")
                            idx_end = answer.rfind(">")
                            if idx_start == -1 or idx_end == -1:
                                csv_results[-1].append("Yes")
                                csv_results[-1].append("Failed to parse")
                                continue
                            config = answer[idx_start:idx_end + 1]
                            config_list = []
                            for each_config in config.split("<module"):
                                if len(each_config.strip()) > 0:
                                    config_list.append("<module" + each_config)
                            config_str = "\n".join(config_list)
                            csv_results[-1].append("Yes")
                            csv_results[-1].append(config_str)
                        elif '"Answer": "Yes"' in answer:
                            idx_start = answer.find("<module")
                            idx_end = answer.rfind(">")
                            if idx_start == -1 or idx_end == -1:
                                csv_results[-1].append("Yes")
                                csv_results[-1].append("Failed to parse")
                                continue
                            config = answer[idx_start:idx_end + 1]
                            config_list = []
                            for each_config in config.split("<module"):
                                if len(each_config.strip()) > 0:
                                    config_list.append("<module" + each_config)
                            config_str = "\n".join(config_list)
                            csv_results[-1].append("Yes")
                            csv_results[-1].append(config_str)
                        else:
                            csv_results[-1].append("No")
            util.save_json(
                f"data/gpt_answer/{model}/",
                str_type,
                gpt_answers,
            )
            util.save_csv(
                f"data/gpt_answer/{model}/{str_type}.csv",
                csv_results,
                [
                    "rule_name",
                    "description",
                    "benchmark",
                    "gpt_answer",
                    "gpt_configuration",
                ],
            )
