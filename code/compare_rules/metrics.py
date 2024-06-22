import pandas as pd
from xml.etree import ElementTree as ET
import json
import re
import os


def valid_xml(string):
    try:
        ET.fromstring(string)
        return True
    except:
        return False


def valid_config(gpt_answer):
    ...
    # sort by key
    sorted_gpt_answer = sorted(gpt_answer, key=lambda x: x["modulename"])

    # TODO 如果配置不合法怎么办？
    return True


def compare_config(gpt_answer, benchmark):
    if valid_config(gpt_answer):
        module_tp = []
        option_name_tp = []
        option_value_tp = []

        module_fp = gpt_answer.copy()
        option_name_fp = gpt_answer.copy()
        option_value_fp = gpt_answer.copy()

        module_fn = benchmark.copy()
        option_name_fn = benchmark.copy()
        option_value_fn = benchmark.copy()

        for gpt_module in gpt_answer:
            for benchmark_module in module_fn:
                # TODO 计算方法有问题：同一个module如果存在多个
                # 判断benchmark中是否存在该module
                if gpt_module["modulename"] == benchmark_module["modulename"]:
                    module_tp.append(gpt_module)
                    module_fn.remove(benchmark_module)
                    module_fp.remove(gpt_module)
                    break
            for benchmark_module in option_name_fn:
                if gpt_module["modulename"] == benchmark_module["modulename"]:
                    all_prop_name_match, all_prop_value_match = check_option_match(
                        gpt_module, benchmark_module
                    )
                    if all_prop_name_match:
                        option_name_tp.append(gpt_module)
                        option_name_fn.remove(benchmark_module)
                        option_name_fp.remove(gpt_module)
                        break
            for benchmark_module in option_value_fn:
                if gpt_module["modulename"] == benchmark_module["modulename"]:
                    all_prop_name_match, all_prop_value_match = check_option_match(
                        gpt_module, benchmark_module
                    )
                    if all_prop_value_match:
                        option_value_tp.append(gpt_module)
                        option_value_fn.remove(benchmark_module)
                        option_value_fp.remove(gpt_module)
                        break

        module_res = [module_tp, [], module_fp, module_fn]

        option_name_res = [option_name_tp, [], option_name_fp, option_name_fn]

        option_value_res = [
            option_value_tp,
            [],
            option_value_fp,
            option_value_fn,
        ]
    else:
        module_res = [[], [], [], []]
        option_name_res = [[], [], [], []]
        option_value_res = [[], [], [], []]
    return [module_res, option_name_res, option_value_res]


def check_option_match(gpt_module:dict, benchmark_module:dict):
    all_prop_name_match = True
    all_prop_value_match = True
    for prop in benchmark_module:
        if prop != "modulename":
            cor_prop = gpt_module.get(prop)
            if not cor_prop:
                all_prop_name_match = False
                all_prop_value_match = False
            elif cor_prop != benchmark_module[prop]:
                all_prop_value_match = False

    for prop in gpt_module:
        if prop != "modulename":
            cor_prop = benchmark_module.get(prop)
            if not cor_prop:
                all_prop_name_match = False
                all_prop_value_match = False
            elif cor_prop != gpt_module[prop]:
                all_prop_value_match = False
    return all_prop_name_match,all_prop_value_match


def cal_fp_fn(gpt_answer, benchmark, module_tp):
    # !处理同名 module
    # fp: gpt_answer中有，benchmark中没有
    # gpt_answer中有1个，benchmark中有多个？
    # gpt_answer中有多个，benchmark中有多个？
    # gpt_answer中有多个，benchmark中有1个？
    # gpt_answer中有多个，benchmark中有0个？
    # fn: gpt_answer中没有，benchmark中有

    module_fp = []
    module_fn = []
    for gpt_module in gpt_answer:
        if gpt_module["modulename"] not in module_tp:
            module_fp.append(gpt_module["modulename"])

    for benchmark_module in benchmark:
        if benchmark_module["modulename"] not in module_tp:
            module_fn.append(benchmark_module["modulename"])
    return module_fp, module_fn


def compare_benchmark_output(csv_path, benchmark_path):

    data = pd.read_csv(csv_path)

    output_data = []
    jdata = json.load(open(benchmark_path))
    failed_cnt = 0

    module_all_res = [0, 0, 0, 0]
    option_name_all_res = [0, 0, 0, 0]
    option_value_all_res = [0, 0, 0, 0]

    m_rule_correct = 0
    on_rule_correct = 0
    ov_rule_correct = 0
    exist_mapping_tp = 0
    exist_mapping_fp = 0
    exist_mapping_fn = 0
    for _, line in data.iterrows():
        rule = line["rule_name"]
        cor_benchmark = jdata[rule]
        benchmark_exist_config = len(cor_benchmark) > 0
        if rule == "2.3.2 Special escape sequences" and "4o" in csv_path and "mopt" in csv_path:
            aa = 1
        answer_exist_config = line['gpt_answer']
        answer_exist_config = answer_exist_config == answer_exist_config and answer_exist_config.lower() == "yes"

        #! cal exist mapping metrics
        if benchmark_exist_config and answer_exist_config:
            exist_mapping_tp += 1
        elif benchmark_exist_config and not answer_exist_config:
            exist_mapping_fn += 1
        elif not benchmark_exist_config and answer_exist_config:
            exist_mapping_fp += 1

        answer = line["gpt_configuration"]
        output_data.append(
            [
                line["rule_name"],
                line["description"],
                line["benchmark"],
                line["gpt_answer"],
                line["gpt_configuration"],
            ]
        )
        if answer == answer:
            if answer.startswith("<module\n"):
                answer = answer[8:]
            answer = f"<module name='Checker'>{answer}</module>"
            root = None
            if valid_xml(answer):
                root = ET.fromstring(answer)
            elif valid_xml(answer := re.sub('>["]*,', ">", answer)):
                root = ET.fromstring(answer)
            elif valid_xml(answer := re.sub('["]*<,', "<", answer)):
                root = ET.fromstring(answer)
            elif valid_xml(answer := re.sub(' ["]+', "", answer)):
                root = ET.fromstring(answer)
            elif valid_xml(answer := re.sub("\\\\n<", "<", answer)):
                root = ET.fromstring(answer)
            elif valid_xml(answer := re.sub(">\\\\n", ">", answer)):
                root = ET.fromstring(answer)
            elif valid_xml(answer := re.sub(" +\n", "", answer)):
                root = ET.fromstring(answer)
            else:
                # print(f"[cannot parse]:{rule}")
                failed_cnt += 1
                output_data[-1].append("false")
                # 全部都是 FN
                error_fn = len(cor_benchmark)
                error_res = [
                    "",
                    "",
                    "\n".join([mod["modulename"] for mod in cor_benchmark]),
                ]

                output_data[-1].extend(error_res * 3)
                module_all_res[3] += error_fn
                option_name_all_res[3] += error_fn
                option_value_all_res[3] += error_fn
                continue
            output_data[-1].append("true")
            answer_config = []
            for child in root:
                answer_config.append({})
                answer_config[-1]["modulename"] = child.attrib["name"]
                for prop in child:
                    if prop.tag == "property":
                        answer_config[-1][prop.attrib["name"]] = prop.attrib["value"]
            # if rule == "3.4.1 Exactly one top-level class declaration":
            #     if "4o" in csv_path:
            #         if "name_simpledesc_opt" in csv_path:
            #             print(answer_config)
            compare_result = compare_config(answer_config, cor_benchmark)
            indices = [
                (0, 0),
                (0, 2),
                (0, 3),
                (1, 0),
                (1, 2),
                (1, 3),
                (2, 0),
                (2, 2),
                (2, 3),
            ]
            for i, j in indices:
                output_data[-1].append("\n".join([mod.get("modulename") for mod in compare_result[i][j]]))

            module_level_res = [
                len(compare_result[0][0]),
                len(compare_result[0][1]),
                len(compare_result[0][2]),
                len(compare_result[0][3]),
            ]
            option_name_level_res = [
                len(compare_result[1][0]),
                len(compare_result[1][1]),
                len(compare_result[1][2]),
                len(compare_result[1][3]),
            ]
            option_value_level_res = [
                len(compare_result[2][0]),
                len(compare_result[2][1]),
                len(compare_result[2][2]),
                len(compare_result[2][3]),
            ]
            module_all_res = [module_all_res[i] + module_level_res[i] for i in range(4)]
            option_name_all_res = [
                option_name_all_res[i] + option_name_level_res[i] for i in range(4)
            ]
            option_value_all_res = [
                option_value_all_res[i] + option_value_level_res[i] for i in range(4)
            ]
            # if module_level_res[0] > 0:
            #     print(rule)
            if module_level_res[2] == 0 and module_level_res[3] == 0:
                m_rule_correct += 1
                # print(f"---rule level match {rule}")
            if option_name_level_res[2] == 0 and option_name_level_res[3] == 0:
                on_rule_correct += 1
                # print(f"===option name level match {rule}")
            if option_value_level_res[2] == 0 and option_value_level_res[3] == 0:
                ov_rule_correct += 1
                # print(f"+++option value level match {rule}")

    output_df = pd.DataFrame(
        output_data,
        columns=[
            "rule_name",
            "description",
            "benchmark",
            "gpt_answer",
            "gpt_configuration",
            "valid_config",
            "module_tp",
            "module_fp",
            "module_fn",
            "option_name_tp",
            "option_name_fp",
            "option_name_fn",
            "option_value_tp",
            "option_value_fp",
            "option_value_fn",
        ],
    )
    output_df.to_csv(f"{csv_path[:-4]}_compared.csv", index=False)
    m_tp_fn = module_all_res[0] + module_all_res[3]
    m_tp_fp = module_all_res[0] + module_all_res[2]
    m_recall = module_all_res[0] / m_tp_fn if m_tp_fn > 0 else ""
    m_precision = module_all_res[0] / m_tp_fp if m_tp_fp > 0 else ""
    m_accuracy = (module_all_res[0] + module_all_res[1]) / sum(module_all_res)

    on_tp_fn = option_name_all_res[0] + option_name_all_res[3]
    on_tp_fp = option_name_all_res[0] + option_name_all_res[2]
    on_recall = option_name_all_res[0] / on_tp_fn if on_tp_fn > 0 else ""
    on_precision = option_name_all_res[0] / on_tp_fp if on_tp_fp > 0 else ""
    on_accuracy = (option_name_all_res[0] + option_name_all_res[1]) / sum(
        option_name_all_res
    )

    ov_tp_fn = option_value_all_res[0] + option_value_all_res[3]
    ov_tp_fp = option_value_all_res[0] + option_value_all_res[2]
    ov_recall = option_value_all_res[0] / ov_tp_fn if ov_tp_fn > 0 else ""
    ov_precision = option_value_all_res[0] / ov_tp_fp if ov_tp_fp > 0 else ""
    ov_accuracy = (option_value_all_res[0] + option_value_all_res[1]) / sum(
        option_value_all_res
    )
    print(f"baseline: {csv_path}")
    print(f"Module level: {module_all_res}")
    print(f"Option name level: {option_name_all_res}")
    print(f"Option value level: {option_value_all_res}")
    print("failed to parse:", failed_cnt)
    return_list = [
        failed_cnt,
        m_recall,
        m_precision,
        m_accuracy,
        on_recall,
        on_precision,
        on_accuracy,
        ov_recall,
        ov_precision,
        ov_accuracy,
        m_rule_correct,
        on_rule_correct,
        ov_rule_correct,
    ]
    return return_list


if __name__ == "__main__":
    stat_data = []
    root = "data/gpt_answer"
    bm_path = "data/benchmark/simple_benchmark.json"
    for file in os.listdir(root + "/3.5"):
        if file.endswith(".csv") and not file.endswith("_compared.csv"):
            stat_data.append(["GPT3.5_" + file[:-4]])
            stat_data[-1].extend(
                compare_benchmark_output(f"{root}/3.5/{file}", bm_path)
            )
    for file in os.listdir(root + "/4o"):
        if file.endswith(".csv") and not file.endswith("_compared.csv"):
            stat_data.append(["GPT4o_" + file[:-4]])
            # if "simpledesc_opt" in file:
            stat_data[-1].extend(compare_benchmark_output(f"{root}/4o/{file}", bm_path))

    stat_df = pd.DataFrame(
        stat_data,
        columns=[
            "baseline",
            "failed_cnt",
            "m_recall",
            "m_precision",
            "m_accuracy",
            "on_recall",
            "on_precision",
            "on_accuracy",
            "ov_recall",
            "ov_precision",
            "ov_accuracy",
            "m_rule_accuracy",
            "on_rule_accuracy",
            "ov_rule_accuracy",
        ],
    )
    stat_df.to_csv("stat.csv", index=False)
