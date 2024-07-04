import os
import json
import re
import shutil
import sys
import xml.etree.ElementTree as ET
import pandas as pd
import tiktoken
from proj_code.compare_rules.gpt_agent_028 import GPTAgent
import util
from rag import (
    augmented_name_desc_opt_str,
    augmented_name_desc_str,
    augmented_name_sdesc_opt_str,
)


def valid_json(json_str):
    try:
        json.loads(json_str)
        return True
    except:
        return False


def gen_prompt(rule: str, tool_rules: str, style="ESLint"):
    prompt = ""
    template_path = "data/templates"
    # ! prompt 放在文件中
    if tool_rules == "":
        template_path = os.path.join(template_path, "google2eslint_js_empty_prompt.txt")
    else:
        template_path = os.path.join(template_path, "google2eslint_js_prompt.txt")
    with open(template_path, "r") as f:
        prompt = f.read()
        prompt = prompt.replace("{{style}}", style)
        prompt = prompt.replace("{{rule}}", rule)
        prompt = prompt.replace("{{tool_rules}}", tool_rules)
    if prompt == "":
        raise Exception("Prompt is empty")
    return prompt


baselines = [
    # "empty",
    # "name",
    # "name_desc",
    # "name_desc_opt", #! 159k tokens
    # "name_sdesc_opt",#! only extracted options
    # "rag_name_desc", #! extracted or origin
    # "rag_name_desc_opt", #! extracted or origin
    # "rag_name_sdesc_opt",#! only extracted options
    # "name_url",
    # "name_url_sdesc",
    # "name_sdesc",
]


def get_eslint_str(baseline, rule: str = ""):
    """
    将所有eslint规则转换为一个字符串
    """
    fname = "url_sum_desc_opt_2.json"
    jdata = json.load(open(f"data/rule/eslint/{fname}", "r", encoding="utf-8"))

    def empty():
        """
        empty
        """
        return ""

    def name():
        """
        name
        """
        name_str = "\n".join([f"[Rule]\n{k}" for k in jdata.keys()])
        return name_str

    def name_desc():
        """
        name & description

        average 98k tokens
        """
        name_desc_str = "\n".join(
            [f"[Rule]\n{k}\n[Description]\n{v[1]}\n{v[2]}" for k, v in jdata.items()]
        )
        return name_desc_str
    def name_desc_opt():
        """
        name & description & options

        average 159k tokens for extracted options
        average 223k tokens for origin options
        """
        jlist = []
        for rule, data in jdata.items():
            rule_str_list = []
            rule_str_list.append(f"[Rule]\n{rule}")
            rule_str_list.append(f"[Description]\n{data[1]}\n{data[2]}")
            rule_str_list.append(f"[Options]\n{data[3] if data[3] != '' else 'None'}")
            rule_str = "\n".join(rule_str_list)
            jlist.append(rule_str)
        name_desc_opt_str = "\n".join(jlist)

        return name_desc_opt_str

    def name_sdesc_opt():
        """
        name & short description & options

        average 67.5k tokens for extracted options
        average 131k tokens for origin options
        """
        jlist = []
        for rule, data in jdata.items():
            rule_str_list = []
            rule_str_list.append(f"[Rule]\n{rule}")
            sdesc = data[1].split("\n")[0] if data[1] != "" else "None"
            rule_str_list.append(f"[Description]\n{sdesc}")
            rule_str_list.append(f"[Options]\n{data[3] if data[3] != '' else 'None'}")
            rule_str = "\n".join(rule_str_list)
            jlist.append(rule_str)
        name_sdesc_opt_str = "\n".join(jlist)
        return name_sdesc_opt_str

    def rag_name_desc(rule: str):
        """
        name & description
        """
        return augmented_name_desc_str(rule, 20)

    def rag_name_desc_opt(rule: str):
        """
        name & description & modified options
        """
        return augmented_name_desc_opt_str(rule, 20)

    def rag_name_sdesc_opt(rule: str):
        """
        name & short description & options
        """
        return augmented_name_sdesc_opt_str(rule, 20)

    def name_url():
        """
        name & url
        """
        jlist = []
        for rule, data in jdata.items():
            rule_str_list = []
            rule_str_list.append(f"[Rule]\n{rule}")
            rule_str_list.append(f"[url]\n{data[0]}")
            rule_str = "\n".join(rule_str_list)
            jlist.append(rule_str)
        name_url_str = "\n".join(jlist)
        return name_url_str

    def name_url_sdesc():
        """
        name & url & short description
        """
        jlist = []
        for rule, data in jdata.items():
            rule_str_list = []
            rule_str_list.append(f"[Rule]\n{rule}")
            rule_str_list.append(f"[url]\n{data[0]}")
            sdesc = data[1].split("\n")[0] if data[1] != "" else "None"
            rule_str_list.append(f"[Description]\n{sdesc}")
            rule_str = "\n".join(rule_str_list)
            jlist.append(rule_str)
        name_url_sdesc_str = "\n".join(jlist)
        return name_url_sdesc_str

    def name_sdesc():
        """
        name & short description
        """
        jlist = []
        for rule, data in jdata.items():
            rule_str_list = []
            rule_str_list.append(f"[Rule]\n{rule}")
            sdesc = data[1].split("\n")[0] if data[1] != "" else "None"
            rule_str_list.append(f"[Description]\n{sdesc}")
            rule_str = "\n".join(rule_str_list)
            jlist.append(rule_str)
        name_sdesc_str = "\n".join(jlist)
        return name_sdesc_str

    for options in baselines:
        if options == baseline:
            if (
                baseline == "rag_name_desc"
                or baseline == "rag_name_desc_opt"
                or baseline == "rag_name_sdesc_opt"
            ):
                return locals()[options](rule)
            else:
                return locals()[options]()

    raise Exception(f"Invalid option: {baseline}")


def get_gpt_response_config(baseline, model, rules, use_examples=False):
    agent = GPTAgent()
    answer_dict = {}
    print(f"baseline: {baseline}")
    print(f"model: {model}")
    cnt = 0
    tokens = []
    for rule, _ in rules.items():
        # ! test
        cnt += 1
        rule_name = rule.split("\n")[0]
        print(f"rule_name: {rule_name}")
        rules_str = get_eslint_str(baseline, rule)
        prompt = gen_prompt(
            rule=rule,
            tool_rules=rules_str,
            style="ESLint",
        )
        # count tokens:
        if "4o" in model:
            encoding = tiktoken.get_encoding("o200k_base")
        else:
            encoding = tiktoken.encoding_for_model(model)
        tokens.append(len(encoding.encode(prompt)))
        # ! 暂不用examples
        # if use_examples:
        #     exmaple_root = "data/examples/google2eslint_baseline"
        #     with open(
        #         f"{exmaple_root}/{baseline}_prompt.txt", "r", encoding="utf-8"
        #     ) as f:
        #         exmaples.append({"role": "user", "content": f.read()})
        #     with open(f"{exmaple_root}/response.txt", "r", encoding="utf-8") as f:
        #         exmaples.append({"role": "assistant", "content": f.read()})
        # ! check prompt
        # with open(
        #     f"data/debug/{model}_{baseline}_prompt_{cnt}.txt", "w", encoding="utf-8"
        # ) as f:
        #     f.write(prompt)
        if DEBUG:
            continue
        try:
            answer = agent.get_response(prompt, model=model)
        except Exception as e:
            print(f"failed to get response for rule: {rule_name}")
            print(f"[error]: {e}")
            continue
        if answer.startswith("```json\n"):
            answer = answer[len("```json\n") :]
        if answer.endswith("\n```"):
            answer = answer[: -len("\n```")]
        answer_dict[rule_name] = [prompt, answer]
        # break
    print(f"{tokens}")
    print("------------------")
    return answer_dict


def offline_res(model: str, opt: str):
    res = util.load_json(offline_root, f"{model}_{opt}")
    return res


def json_from_text(json_str):
    if valid_json(json_str):
        return json.loads(json_str)
    tmp_str = re.sub(r'\\"', '"', json_str)
    if valid_json(tmp_str):
        return json.loads(tmp_str)
    tmp_str = tmp_str.strip().strip("{}").strip().strip('"')
    if valid_json(tmp_str):
        return json.loads(tmp_str)
    if valid_json(f"{{{tmp_str}}}"):
        return json.loads(f"{{{tmp_str}}}")
    return None


if __name__ == "__main__":
    DEBUG = True
    DEBUG = False
    save_root = "data/config_output/google2eslint_js/baseline/"
    bm_data_path = "data/benchmark/google2eslint_js_benchmark.json"
    offline_root = save_root
    all_rules = json.load(open(bm_data_path, "r", encoding="utf-8"))
    for model in ["gpt-4o"]:
        for baseline in baselines:
            print(f"model: {model}, baseline: {baseline}")
            # gpt_answers = get_gpt_response_config(
            #     baseline, model, all_rules, use_examples=False
            # )
            if DEBUG:
                continue
            ## ! use offline data
            gpt_answers = offline_res(model, baseline)
            csv_results = []
            for rule, config in all_rules.items():
                rule_name = rule.split("\n")[0]
                try:
                    rule_desc = rule[rule.find("\n") + 1 :].strip()
                except:
                    rule_desc = ""
                if gpt_answers.get(rule_name):
                    answer = gpt_answers[rule_name][1]
                else:
                    continue
                csv_results.append(
                    [rule_name, rule_desc, config if len(config) > 0 else ""]
                )
                try:
                    if valid_json(answer):
                        json_object = json.loads(answer)
                        y_or_n = json_object["Answer"]
                        if y_or_n == "Yes":
                            csv_results[-1].append(y_or_n)
                            cfg_str = json_object.get("Configuration")
                            if not isinstance(cfg_str, dict):
                                cfg_json = json_from_text(cfg_str)
                                if cfg_json:
                                    csv_results[-1].append(cfg_json)
                                    csv_results[-1].append("valid config part")
                                else:
                                    csv_results[-1].append(cfg_str)
                                    csv_results[-1].append("invalid config part")
                            else:
                                csv_results[-1].append(cfg_str)
                                csv_results[-1].append("valid config part")
                        else:
                            csv_results[-1].append(y_or_n)
                            csv_results[-1].append(answer)
                            csv_results[-1].append("y_or_n is not Yes")
                    else:
                        raise Exception("Invalid json")
                except Exception as e:
                    answer_strs = [
                        "'Answer': 'Yes'",
                        '"Answer": "Yes"',
                        '"Answer": Yes',
                    ]
                    if any([s in answer for s in answer_strs]):
                        csv_results[-1].append("Yes")
                        if "Configuration" in answer:
                            idx = answer.find("Configuration")
                            cfg_str = answer[idx + len("Configuration") :]
                            cfg_str = cfg_str.strip("}")
                            open_brace_idx = cfg_str.find("{")
                            close_brace_idx = cfg_str.rfind("}")
                            if (open_brace_idx != -1) and (close_brace_idx != -1):
                                cfg_str = cfg_str[open_brace_idx : close_brace_idx + 1]
                            cfg_json = json_from_text(cfg_str)
                            if cfg_json:
                                csv_results[-1].append(cfg_json)
                            else:
                                print(f"{rule_name}: {e}")
                                csv_results[-1].append(cfg_str)
                            csv_results[-1].append("exist config in str")
                        else:
                            # csv_results[-1].append("")
                            csv_results[-1].append(answer)
                            csv_results[-1].append("No Configuration in str")
                    else:
                        csv_results[-1].append("No")
                        csv_results[-1].append(answer)
                        csv_results[-1].append("No 'Yes' in str")
            util.save_json(
                save_root,
                f"{model}_{baseline}",
                gpt_answers,
            )
            util.save_csv(
                os.path.join(save_root, f"{model}_{baseline}.csv"),
                csv_results,
                [
                    "rule_name",
                    "description",
                    "benchmark",
                    "gpt_answer",
                    "gpt_configuration",
                    "tag",
                ],
            )
