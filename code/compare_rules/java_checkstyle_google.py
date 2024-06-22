import os
import json
import re
import shutil
import sys
import xml.etree.ElementTree as ET
import pandas as pd
from rag import augmented_name_desc_mopt_str,augmented_name_desc_str
# from gpt_wrapper_new import GPTAgent
from gpt_agent_028 import GPTAgent # openai==0.28

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
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
        <property name='name_n' value='value_n'/>
    </module>
    ...
    <module name='rule_name_x'>
        <property name='id' value='id_value_1'/>
        <property name='name_1' value='value_1'/>
        <property name='name_2' value='value_2'/>
        ...
        <property name='name_m' value='value_m'/>
    </module>"
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


def get_checkstyle_str(opt, rule: str=""):
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

    def name_desc(rule: str):
        """
        name & description
        """
        return augmented_name_desc_str(rule)

    def name_desc_mopt(rule: str):
        """
        name & description & modified options
        """
        return augmented_name_desc_mopt_str(rule)

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
            if opt == "name_desc" or opt == "name_desc_mopt":
                return locals()[options](rule)
            else:
                return locals()[options]()

    raise Exception(f"Invalid option: {opt}")


def get_all_gpt_res_for_java_checkstyle(opt, model, rules,use_examples=False):
    """
    1. parse each rule of style guide as a string
    2. parse all rules of style tool as a string
    3. get and save GPT results
    """
    agent = GPTAgent()
    
    answer_dict = {}
    print(f"baseline: {opt}")
    print(f"model: {model}")
    for i, row in rules.iterrows():
        # if i < 3:
        #     continue
        rule_name = row.rule
        rule_desc = row.desc
        checkstyle_str = get_checkstyle_str(opt,f"{rule_name}\n{rule_desc}")
        print(f"rule_name: {rule_name}")
        if opt == "empty":
            prompt = gen_nocheckstyle_prompt(rule=f"{rule_name}\n{rule_desc}")
        else:
            prompt = gen_prompt(
                rule=f"{rule_name}\n{rule_desc}",
                tool_rules=checkstyle_str,
                style="CheckStyle",
            )
        exmaples = []
        if use_examples:
            with open(f"data/examples/{opt}_prompt.txt", "r") as f:
                exmaples.append({"role": "user", "content": f.read()})
            with open(f"data/examples/response.txt", "r") as f:
                exmaples.append({"role": "assistant", "content": f.read()})
        # ! check prompt
        # with open(f"data/testdata/{model}_{opt}_prompt_{i}.txt", "w") as f:
        #     f.write(prompt)
        #     continue
        try:
            if model == "3.5":
                answer = agent.get_response(prompt,messages=exmaples)
            else:
                answer = agent.get_response(prompt,messages=exmaples, model="gpt-4o")
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
            gpt_answers = get_all_gpt_res_for_java_checkstyle(str_type, model, all_rules,use_examples=True)
            # continue
            # gpt_answers = offline_res(model,str_type)
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
