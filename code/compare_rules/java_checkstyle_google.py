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


def gen_prompt(rule: str, tool_rules: str, style="CheckStyle"):
    prompt = """Please generate {{style}} configurations based on the following style convention and CheckStyle rules, ensuring that the output only includes relevant configurations and excludes any unrelated rules.


Style Convention:
{{rule}}

CheckStyle Rules:
{{checkstyle_rules}}

Response Format Should be a json object:
{
    "Answer":  Respond with either Yes or No to show whether {{style}} configurations exist for the given style convention,
    "Configuration": If the answer is Yes, provide the configuration. There can be one or multiple {{style}} rules for the given style convention. The configuration format should be xml format:
    ["<module name='rulename1'>\n  <property name='id' value='id_value1'/>\n  <property name='name1' value='value1'/>\n  ...\n  <property name='name2' value='value2'/>"
    "</module>\n...\n<module name='rulename2'>\n  <property name='id' value='id_value1'/>\n  <property name='name1' value='value1'/>\n  ...\n  <property name='name2' value='value2'/>\n</module>"]
}

"""
    prompt = prompt.replace("{{style}}", style)
    prompt = prompt.replace("{{rule}}", rule)
    prompt = prompt.replace("{{checkstyle_rules}}", tool_rules)
    return prompt


str_types = [
    # "name_desc",
    # "name_desc_mopt",
    "name_sdesc_mopt",
    "name_url",
    "name_url_sdesc",
    "name_sdesc",
]


def get_checkstyle_str(opt):

    def name_desc():
        """
        name & description
        """
        fname = "url_name_desc_mopt"
        jdata = util.load_json("data/rule/checkstyle/java/", fname)
        name_desc_str = "\n".join(
            [
                f"[Rule]\n{rule[1]}\n[Description]\n{rule[2].strip('Description').strip()}"
                for rule in jdata
            ]
        )
        return name_desc_str

    def name_desc_mopt():
        """
        name & description & modified options
        """
        fname = "url_name_desc_mopt"
        jdata = util.load_json("data/rule/checkstyle/java/", fname)
        jlist = []
        for rule in jdata:
            rule_str = f"[Rule]\n{rule[1]}"
            rule_str += f"\n[Description]\n{rule[2].strip('Description').strip()}"
            if len(rule) == 4:
                rule_str += f"\n[Options]{rule[3]}"
            jlist.append(rule_str)
        name_desc_mopt_str = "\n".join(jlist)
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


def get_all_gpt_res_for_java_checkstyle(opt, rules):
    """
    1. parse each rule of style guide as a string
    2. parse all rules of style tool as a string
    3. get and save GPT results
    """
    agent = GPTAgent()
    checkstyle_str = get_checkstyle_str(opt)
    answer_dict = {}
    cnt = 0
    for _, row in rules.iterrows():
        rule_name = row.rule
        rule_desc = row.desc
        prompt = gen_prompt(
            rule=f"{rule_name}\n{rule_desc}",
            tool_rules=checkstyle_str,
            style="CheckStyle",
        )
        try:
            answer = agent.get_response(prompt)
        except Exception as e:
            print(f"failed to get response for rule: {rule_name}")
            continue
        answer_dict[rule_name] = answer
        cnt+=1
        if cnt == 2:
            break
    util.save_json(
        "data/gpt_answer/",
        opt,
        answer_dict,
    )
    return answer_dict


if __name__ == "__main__":
    all_rules = pd.read_excel(
        "data/benchmark/checkstyle2google_java_benchmark.xlsx")
    for str_type in str_types:
        gpt_answers = get_all_gpt_res_for_java_checkstyle(str_type, all_rules)
        csv_results = []
        for index, row in all_rules.iterrows():
            rule_name = row.rule
            answer = ""
            csv_results.append(
                [rule_name, row.desc, row.res if row.res == row.res else ""])
            if gpt_answers.get(rule_name):
                answer = gpt_answers[rule_name]
                try:
                    json_object = json.loads(answer)
                    print(">>>>>>: ", json_object)
                    y_or_n = json_object["Answer"]
                    csv_results[-1].append(y_or_n)
                    configuration_list = json_object["Configuration"]
                    csv_results[-1].append("\n******\n".join(configuration_list))
                except:
                    print(">>>>>>>exception")
                    if "'Answer': 'Yes'" in answer:
                        idx_start = answer.find("<module")
                        idx_end = answer.rfind(">")
                        if idx_start == -1 or idx_end == -1:
                            csv_results[-1].append("Yes")
                            csv_results[-1].append("Failed to parse")
                            continue
                        config = answer[idx_start:idx_end + 1]
                        config_str = "\n******\n".join(
                            [
                                "<module" + each_config
                                for each_config in config.split("<module")
                            ]
                        )
                        csv_results[-1].append("Yes")
                        csv_results[-1].append(config_str)
                        print(config_str)
                    elif '"Answer": "Yes"' in answer:
                        idx_start = answer.find("<module")
                        idx_end = answer.rfind(">")
                        if idx_start == -1 or idx_end == -1:
                            csv_results[-1].append("Yes")
                            csv_results[-1].append("Failed to parse")
                            continue
                        config = answer[idx_start:idx_end + 1]
                        config_str = "\n******\n".join(
                            [
                                "<module" + each_config
                                for each_config in config.split("<module")
                            ]
                        )
                        csv_results[-1].append("Yes")
                        csv_results[-1].append(config_str)
                        print(config_str)
                    else:
                        csv_results[-1].append("No")
        util.save_csv(
            f"data/gpt_answer/{str_type}.csv",
            csv_results,
            [
                "rule_name",
                "description",
                "benchmark",
                "gpt_answer",
                "gpt_configuration",
            ],
        )
