"""
由于eslint rule的option内容过于复杂，token会严重超出，因此需要将option内容提取出来

以下为某个rule对应prompt的token数目
"""

import os, json, shutil, re
from proj_code.compare_rules.gpt_agent_028 import GPTAgent


def get_prompt(template, rule_name, rule_data):
    prompt = template
    prompt = prompt.replace("{{rule_name}}", rule_name)
    prompt = prompt.replace("{{overview}}", rule_data[1])
    prompt = prompt.replace(
        "{{details}}", rule_data[2] if rule_data[2] != "" else "None"
    )
    prompt = prompt.replace(
        "{{options}}", rule_data[3] if rule_data[3] != "" else "None"
    )
    return prompt

def get_prompt_new(template, html_data):
    prompt = template
    prompt = prompt.replace("{{html_content}}", html_data)
    return prompt

def get_gpt_response_from_html(rule_dirs: list,save_dir, prompt_template_path):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    template = open(prompt_template_path, "r", encoding="utf-8").read()
    agent = GPTAgent()
    cnt = 0
    for dir in rule_dirs:
        for file in os.listdir(dir):
            if file.endswith(".html"):
                cnt += 1
                # if cnt > 20:
                #     return
                rule_name = file[:-5]
                print(f"Processing rule: {rule_name}")
                html_data = open(f"{dir}/{file}", "r", encoding="utf-8").read()
                prompt = get_prompt_new(template, html_data)
                response = agent.get_response(prompt, model="gpt-4o")
                with open(
                    f"{save_dir}/{rule_name}.txt", "w", encoding="utf-8"
                ) as f:
                    f.write(response)


def get_gpt_response():
    """
    step 1. 利用GPT提取文本中的option内容，并保存
    """
    jdata = json.load(
        open("data/rule/eslint/url_sum_desc_opt.json", "r", encoding="utf-8")
    )
    template = open(
        "data/templates/extract_eslint_options_prompt.txt", "r", encoding="utf-8"
    ).read()

    for idx, (k, v) in enumerate(jdata.items()):
        print("Processing rule:", k)
        prompt = get_prompt(template, k, v)
        agent = GPTAgent()
        response = agent.get_response(prompt, model="gpt-4o")
        with open(
            f"data/rule/eslint/gpt_option_answer/{k}.txt", "w", encoding="utf-8"
        ) as f:
            f.write(response)


def text2json():
    """
    step 2. 将gpt提取的option内容转换为json格式
    """
    output_dir = "data/rule/eslint"
    os.makedirs(output_dir, exist_ok=True)
    result = {}
    for file in os.listdir("data/rule/eslint/gpt_option_answer"):
        with open(
            f"data/rule/eslint/gpt_option_answer/{file}", "r", encoding="utf-8"
        ) as f:
            data = f.read()
            if data.startswith("```json"):
                data = data[7:]
            if data.endswith("```"):
                data = data[:-3]
            data = data.strip('"\n')
            try:
                json_data = json.loads(data)
                result[file[:-4]] = json_data
            except:
                if "does not exist" in data:
                    pass
                else:
                    print(data)
    with open(f"{output_dir}/eslint_options.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)


def dfs_get_option(json_data, options: set):
    """
    递归获取json中的option内容
    """
    if isinstance(json_data, dict):
        for k, v in json_data.items():
            options.add(k)
            if isinstance(v, dict):
                dfs_get_option(v, options)
            elif isinstance(v, list):
                for item in v:
                    dfs_get_option(item, options)
            else:
                ...
    elif isinstance(json_data, list):
        for item in json_data:
            dfs_get_option(item, options)
    else:
        options.add(json_data)
        return


def check_options():
    """
    根据option的文本信息，检查json文件是否缺少option
    """
    rules = json.load(
        open("data/rule/eslint/url_sum_desc_opt.json", "r", encoding="utf-8")
    )
    gpt_options = json.load(
        open("data/rule/eslint/eslint_options.json", "r", encoding="utf-8")
    )
    not_covered_by_gpt = {}
    not_found_in_text = {}
    for rule, rule_data in rules.items():
        if rule_data[3] != "":
            option_text = rule_data[2] + rule_data[3]
            # /*eslint xxx*/
            if rule == "key-spacing":
                bb = 2
            comment_pattern = r'/\* *eslint "?[\w-]+"?: *(.*)\*/'
            cmts = [
                re.sub(r"\n", " ", x)
                for x in re.findall(r"/\*.*?\*/", option_text, re.DOTALL)
            ]
            # option_pattern = r'(?<!: )"(\w+(-\w+)*)"|(?<!:)"(\w+(-\w+)*)"|(\w+(-\w+)*) *:'
            for cmt in cmts:
                ...
            eslint_configs = re.findall(comment_pattern, option_text)
            configs = set()
            for cfg_str in eslint_configs:
                # colon_idx = cfg_str.find(":")
                # 去掉第一个冒号前的内容
                # tmp_str = cfg_str[colon_idx+1:]
                tmp_str = cfg_str
                tmp_str = re.sub(r'((?<!"))(\w+(-\w+)*): ', r'\1"\2": ', tmp_str)
                try:
                    tmp_json = json.loads(tmp_str)
                except:
                    tmp_json = {}
                dfs_get_option(tmp_json, configs)
                # options = re.findall(option_pattern,tmp_str)
                # for option in options:
                #     configs.add(option[0])
                #     configs.add(option[2])
                #     configs.add(option[4])
            # if "" in configs:
            #     configs.remove("")
            if "error" in configs:
                configs.remove("error")
            correspond_gpt_json = gpt_options.get(rule)

            not_found = []
            for option in correspond_gpt_json:
                if option not in configs:
                    not_found.append(option)
            if len(not_found) > 0:
                not_found_in_text[rule] = not_found

            not_covered = []
            for cfg in configs:
                if cfg not in correspond_gpt_json:
                    not_covered.append(cfg)
            if len(not_covered) > 0:
                not_covered_by_gpt[rule] = not_covered

    print("Not covered by GPT:\n\n")
    for k, v in not_covered_by_gpt.items():
        print(k, v)
    print("Not found in text:\n\n")
    for k, v in not_found_in_text.items():
        print(k, v)


def optimize_prompt(prompt_template_path):
    agent = GPTAgent()
    template = open(
        prompt_template_path, "r", encoding="utf-8"
    ).read()
    prompt = f"""please optimize the following prompt, check the analysis part: 
    {template}"""
    res = agent.get_response(prompt, model="gpt-4o")
    with open(
        "data/templates/optimized_extract_eslint_options_prompt.txt",
        "w",
        encoding="utf-8",
    ) as f:
        f.write(res)


if __name__ == "__main__":
    save_dir = "data/rule/eslint/gpt_option_answer"
    prompt_template_path = "data/templates/extract_eslint_options_prompt_4.txt"
    rule_dirs = [
        "data/rule/eslint/deprecated",
        "data/rule/eslint/normal",
        ]
    # optimize_prompt(prompt_template_path)
    get_gpt_response_from_html(rule_dirs, save_dir, prompt_template_path)