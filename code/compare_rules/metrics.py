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


def compare_config(gpt_answer, benchmark):

    module_tp = []
    module_tn = []
    option_name_tp = []
    option_name_tn = []
    option_name_fp = []

    option_value_tp = []
    option_value_tn = []
    option_value_fp = []
    module_without_true_option = 0
    module_with_true_option = 0
    for gpt_module in gpt_answer:
        for benchmark_module in benchmark:
            # TODO 计算方法有问题：同一个module如果存在多个
            # 判断benchmark中是否存在该module
            if gpt_module["modulename"] == benchmark_module["modulename"]:
                module_tp.append(gpt_module["modulename"])

                if len(gpt_module) > 1:
                    if len(benchmark_module) > 1:
                        # 该 module 实际有配置，answer中也有
                        all_prop_name_match, all_prop_value_match = check_option_match(gpt_module, benchmark_module)
                        if all_prop_name_match:
                            option_name_tp.append(gpt_module["modulename"])
                        if all_prop_value_match:
                            option_value_tp.append(gpt_module["modulename"])
                    else:
                        # 该 module 实际无配置，answer中有配置
                        ...
                elif len(benchmark_module) == 1:
                    # 该 module 无配置，answer中也无配置
                    option_name_tp.append(gpt_module["modulename"])
                    option_value_tp.append(gpt_module["modulename"])
                else:
                    # 该 module 有配置，answer中无配置
                    ...
    module_fp, module_fn = cal_fp_fn(gpt_answer, benchmark, module_tp)
    module_res = [module_tp, module_tn, module_fp, module_fn]

    option_name_fp, option_name_fn = cal_fp_fn(gpt_answer, benchmark, option_name_tp)
    option_name_res = [option_name_tp, option_name_tn, option_name_fp, option_name_fn]

    option_value_fp, option_value_fn = cal_fp_fn(gpt_answer, benchmark, option_value_tp)
    option_value_res = [
        option_value_tp,
        option_value_tn,
        option_value_fp,
        option_value_fn,
    ]

    return [module_res, option_name_res, option_value_res]

def check_option_match(gpt_module, benchmark_module):
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

    for row, line in data.iterrows():
        rule = line["rule_name"]
        # if rule == '3.3.3 Ordering and spacing' and "simpledesc_opt" in csv_path:
        #     aa = 1
        cor_benchmark = jdata[rule]
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
            elif valid_xml(answer := re.sub("\*\*\*\*\*\*", "", answer)):
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
            if "5.2.4 Constant names" in rule:
                aa = 1
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
                output_data[-1].append("\n".join(compare_result[i][j]))

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
                print(f"---rule level match {rule}")
            if option_name_level_res[2] == 0 and option_name_level_res[3] == 0:
                on_rule_correct += 1
                print(f"===option name level match {rule}")
            if option_value_level_res[2] == 0 and option_value_level_res[3] == 0:
                ov_rule_correct += 1
                print(f"+++option value level match {rule}")

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
    # for file in os.listdir(root + "/3.5"):
    #     if file.endswith(".csv") and not file.endswith("_compared.csv"):
    #         stat_data.append(["GPT3.5_" + file[:-4]])
    #         stat_data[-1].extend(
    #             compare_benchmark_output(f"{root}/3.5/{file}", bm_path)
    #         )
    for file in os.listdir(root + "/4o"):
        if file.endswith(".csv") and not file.endswith("_compared.csv"):
            stat_data.append(["GPT4o_" + file[:-4]])
            if "simpledesc_opt" in file:
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
            "m_rule_correct",
            "on_rule_correct",
            "ov_rule_correct",
        ],
    )
    stat_df.to_csv("stat.csv", index=False)
