import os
import json
import pandas as pd
import re
import tiktoken
from md2json import markdown_to_json

json_dirs = ["data/rule/eslint/deprecated_json", "data/rule/eslint/normal_json"]

baselines = [
    "empty",
    "name",
    "name_url",
    "name_desc",
    "name_url_sdesc",
    "name_sdesc_opt",
    "name_sdesc",
    "name_desc_opt",
]

def gen_json_files():
    """
    将eslint的markdown文件转换为json文件
    """
    for dir in ['deprecated','normal']:
        root = f"data/rule/eslint/{dir}"
        output_root = f"data/rule/eslint/{dir}_json"
        os.makedirs(output_root, exist_ok=True)
        for file in os.listdir(root):
            if file.endswith(".md"):
                with open(f"{root}/{file}", "r",encoding="utf-8") as f:
                    data = f.read()
                    json_data = markdown_to_json(data)
                    save_path = os.path.join(output_root, file.replace(".md", ".json"))
                    with open(save_path, "w", encoding="utf-8") as f:
                        json.dump(json_data, f, indent=4, ensure_ascii=False)
    print("done")

def pps_summary(summary):
    summary = re.sub(r"This rule was deprecated.*Please.*\n", "", summary)
    return summary

def extract_and_merge():
    """
    从json中选取需要的字段，合并到一个json文件中
    """
    all_eslint_rules = {}
    url_prefix = "https://eslint.org/docs/v8.x/rules/"
    for root in json_dirs:
        for file in os.listdir(root):
            with open(f"{root}/{file}", "r",encoding="utf-8") as f:
                data = json.load(f)
                rule_name = file[:-5]
                summary = data["Overview"]
                details = data.get("Rule Details")
                options = data.get("Options")
                summary = pps_summary(summary)
                url = url_prefix + rule_name
                all_eslint_rules[rule_name] = [url,summary,details if details else "",options if options else ""]
    output_path = "data/rule/eslint/url_sum_desc_opt.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_eslint_rules, f, indent=4)

def check_features():
    """
    由于eslint规则的编写没有统一的格式，需要检查各个字段的格式

    改了json格式，此方法弃用
    """
    return
    option_types = {}
    detail_types = set()
    no_detail_cnt = 0
    no_option_cnt = 0
    no_option_root = "data/rule/eslint/no_option"
    has_dict_option_root = "data/rule/eslint/has_dict_option"
    has_str_option_root = "data/rule/eslint/has_str_option"
    os.makedirs(no_option_root, exist_ok=True)
    os.makedirs(has_dict_option_root, exist_ok=True)
    os.makedirs(has_str_option_root, exist_ok=True)
    for root in json_dirs:
        for file in os.listdir(root):
            with open(f"{root}/{file}", "r",encoding="utf-8") as f:
                data = json.load(f)
                rule_name = file[:-5]
                config = data[rule_name]
                options = data.get("Options")
                details = data.get("Rule Details")
                if details:
                    detail_types.add(type(details))
                    if type(details) == dict:
                        if "Options" in details:
                            # 有的option在details里面
                            options = details["Options"]
                else:
                    no_detail_cnt += 1
                if options:
                    ot = type(options)
                    if ot in option_types:
                        option_types[ot] += 1
                    else:
                        option_types[ot] = 1
                    if ot == str:
                        output_path = os.path.join(has_str_option_root, f"{rule_name}.json")
                        with open(output_path, "w", encoding="utf-8") as f:
                            json.dump(config, f, indent=4)
                    else:
                        output_path = os.path.join(has_dict_option_root, f"{rule_name}.json")
                        with open(output_path, "w", encoding="utf-8") as f:
                            json.dump(config, f, indent=4)
                else:
                    no_option_cnt += 1
                    output_path = os.path.join(no_option_root, f"{rule_name}.json")
                    with open(output_path, "w", encoding="utf-8") as f:
                        json.dump(config, f, indent=4)
                summary = config.get("Overview")
                if not summary:
                    print(rule_name)
    print(option_types)
    print(f"no option cnt: {no_option_cnt}")
    print(detail_types)
    print(f"no detail cnt: {no_detail_cnt}")
    
def count_tokens_for_baselines():
    ...
    jdata = json.load(open("data/rule/eslint/url_sum_desc_opt.json", "r", encoding="utf-8"))

if __name__ == '__main__':
    output_path = "data/rule/eslint/url_sum_desc_opt_2.json"
    txt_root = "data/rule/eslint/gpt_option_answer"
    jdata = json.load(open("data/rule/eslint/url_sum_desc_opt_old.json", "r", encoding="utf-8"))
    result = {}
    for rule_name,rule_data in jdata.items():
        simple_option = open(f"{txt_root}/{rule_name}.txt", "r", encoding="utf-8").read()
        result[rule_name] = [rule_data[0],rule_data[1],rule_data[2], simple_option]
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)
    print("done")


