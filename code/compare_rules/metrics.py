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


def cal_prfa(tp, fp, fn):
    recall = tp / (tp + fn) if tp + fn > 0 else ""
    precision = tp / (tp + fp) if tp + fp > 0 else ""
    f1 = 2 * recall * precision / (recall + precision) if recall and precision else ""
    accuracy = tp / (tp + fp + fn) if tp + fp + fn > 0 else ""
    return precision, recall, f1, accuracy


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


def check_option_match(gpt_module: dict, benchmark_module: dict):
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
    return all_prop_name_match, all_prop_value_match


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


def get_answer_config(csv_line):
    # ! NO + Config/Invalid config = Yes + Invalid config = Answer no config
    answer_exist_config = csv_line["gpt_answer"]
    answer_exist_config = (
        answer_exist_config == answer_exist_config
        and answer_exist_config.lower() == "yes"
    )
    if not answer_exist_config:
        return False, None, "no config"

    answer = csv_line["gpt_configuration"]
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
            return False, None, "invalid config"
        return True, root, ""
    return False, None, "no config"


def compare_benchmark_output(csv_path, benchmark_path):

    data = pd.read_csv(csv_path)

    output_csv_data = []
    jdata = json.load(open(benchmark_path))
    failed_cnt = 0

    module_all_res = [0, 0, 0, 0]
    option_name_all_res = [0, 0, 0, 0]
    option_value_all_res = [0, 0, 0, 0]

    m_rule_correct = 0  # TP
    on_rule_correct = 0
    ov_rule_correct = 0

    exist_mapping_tp = 0
    exist_mapping_fp = 0
    exist_mapping_fn = 0

    # algo1: no config 不算 code pair
    cp_m_algo1_tp = 0
    cp_m_algo1_fp = 0
    cp_m_algo1_fn = 0
    cp_on_algo1_tp = 0
    cp_on_algo1_fp = 0
    cp_on_algo1_fn = 0
    cp_ov_algo1_tp = 0
    cp_ov_algo1_fp = 0
    cp_ov_algo1_fn = 0

    # algo2: no config 算 code pair
    cp_m_algo2_tp = 0
    cp_m_algo2_fp = 0
    cp_m_algo2_fn = 0
    cp_on_algo2_tp = 0
    cp_on_algo2_fp = 0
    cp_on_algo2_fn = 0
    cp_ov_algo2_tp = 0
    cp_ov_algo2_fp = 0
    cp_ov_algo2_fn = 0

    # algo3: 只考虑aw 和 bm 都有 config 的情况
    cp_m_algo3_tp = 0
    cp_m_algo3_fp = 0
    cp_m_algo3_fn = 0
    cp_on_algo3_tp = 0
    cp_on_algo3_fp = 0
    cp_on_algo3_fn = 0
    cp_ov_algo3_tp = 0
    cp_ov_algo3_fp = 0
    cp_ov_algo3_fn = 0

    for _, line in data.iterrows():
        rule = line["rule_name"]
        cor_benchmark = jdata[rule]
        benchmark_exist_config = len(cor_benchmark) > 0
        output_csv_data.append(
            [
                line["rule_name"],
                line["description"],
                line["benchmark"],
                line["gpt_answer"],
                line["gpt_configuration"],
            ]
        )

        answer_exist_config, answer_config_xml, aw_stat = get_answer_config(line)
        if answer_exist_config:
            output_csv_data[-1].append("true")
            answer_config_list = []
            for child in answer_config_xml:
                answer_config_list.append({})
                answer_config_list[-1]["modulename"] = child.attrib["name"]
                for prop in child:
                    if prop.tag == "property":
                        answer_config_list[-1][prop.attrib["name"]] = prop.attrib[
                            "value"
                        ]
            compare_result = compare_config(answer_config_list, cor_benchmark)
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
                output_csv_data[-1].append(
                    "\n".join([mod.get("modulename") for mod in compare_result[i][j]])
                )

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

            # rule level match
            if module_level_res[2] == 0 and module_level_res[3] == 0:
                m_rule_correct += 1
                cp_m_algo1_tp += 1
                cp_m_algo2_tp += 1
                cp_m_algo3_tp += 1
            else:
                # diff res -> bm not in aw_set, aw not in bm_set
                cp_m_algo2_fn += 1
                cp_m_algo2_fp += 1
                if benchmark_exist_config:
                    # diff res and both have config -> bm not in aw_set, aw not in bm_set
                    cp_m_algo1_fn += 1
                    cp_m_algo1_fp += 1
                    cp_m_algo3_fn += 1
                    cp_m_algo3_fp += 1

            # option name level match
            if option_name_level_res[2] == 0 and option_name_level_res[3] == 0:
                on_rule_correct += 1
                cp_on_algo1_tp += 1
                cp_on_algo2_tp += 1
                cp_on_algo3_tp += 1
            else:
                cp_on_algo2_fn += 1
                cp_on_algo2_fp += 1
                if benchmark_exist_config:
                    cp_on_algo1_fn += 1
                    cp_on_algo1_fp += 1
                    cp_on_algo3_fn += 1
                    cp_on_algo3_fp += 1

            # option value level match
            if option_value_level_res[2] == 0 and option_value_level_res[3] == 0:
                ov_rule_correct += 1
                cp_ov_algo1_tp += 1
                cp_ov_algo2_tp += 1
                cp_ov_algo3_tp += 1
            else:
                cp_ov_algo2_fn += 1
                cp_ov_algo2_fp += 1
                if benchmark_exist_config:
                    cp_ov_algo1_fn += 1
                    cp_ov_algo1_fp += 1
                    cp_ov_algo3_fn += 1
                    cp_ov_algo3_fp += 1
        else:
            if aw_stat == "invalid config":
                failed_cnt += 1
            output_csv_data[-1].append("false")
            error_fn = len(cor_benchmark)
            error_res = [
                "",
                "",
                "\n".join([mod["modulename"] for mod in cor_benchmark]),
            ]

            if benchmark_exist_config:
                cp_m_algo1_fn += 1
                cp_on_algo1_fn += 1
                cp_ov_algo1_fn += 1

            output_csv_data[-1].extend(error_res * 3)
            module_all_res[3] += error_fn
            option_name_all_res[3] += error_fn
            option_value_all_res[3] += error_fn
            continue

        if benchmark_exist_config and answer_exist_config:
            exist_mapping_tp += 1
        if answer_exist_config and not benchmark_exist_config:
            exist_mapping_fp += 1

            cp_m_algo1_fp += 1
            cp_on_algo1_fp += 1
            cp_ov_algo1_fp += 1
        if not answer_exist_config and benchmark_exist_config:
            exist_mapping_fn += 1

            cp_m_algo1_fn += 1
            cp_on_algo1_fn += 1
            cp_ov_algo1_fn += 1

    output_df = pd.DataFrame(
        output_csv_data,
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
    (m_precision, m_recall, m_f1, m_accuracy) = cal_prfa(
        module_all_res[0], module_all_res[2], module_all_res[3]
    )

    (on_precision, on_recall, on_f1, on_accuracy) = cal_prfa(
        option_name_all_res[0], option_name_all_res[2], option_name_all_res[3]
    )

    (ov_precision, ov_recall, ov_f1, ov_accuracy) = cal_prfa(
        option_value_all_res[0], option_value_all_res[2], option_value_all_res[3]
    )

    (
        exist_mapping_precision,
        exist_mapping_recall,
        exist_mapping_f1,
        exist_mapping_accuracy,
    ) = cal_prfa(exist_mapping_tp, exist_mapping_fp, exist_mapping_fn)

    (
        cp_m_algo1_precision,
        cp_m_algo1_recall,
        cp_m_algo1_f1,
        cp_m_algo1_accuracy,
    ) = cal_prfa(cp_m_algo1_tp, cp_m_algo1_fp, cp_m_algo1_fn)

    (
        cp_on_algo1_precision,
        cp_on_algo1_recall,
        cp_on_algo1_f1,
        cp_on_algo1_accuracy,
    ) = cal_prfa(cp_on_algo1_tp, cp_on_algo1_fp, cp_on_algo1_fn)

    (
        cp_ov_algo1_precision,
        cp_ov_algo1_recall,
        cp_ov_algo1_f1,
        cp_ov_algo1_accuracy,
    ) = cal_prfa(cp_ov_algo1_tp, cp_ov_algo1_fp, cp_ov_algo1_fn)

    (
        cp_m_algo2_precision,
        cp_m_algo2_recall,
        cp_m_algo2_f1,
        cp_m_algo2_accuracy,
    ) = cal_prfa(cp_m_algo2_tp, cp_m_algo2_fp, cp_m_algo2_fn)

    (
        cp_on_algo2_precision,
        cp_on_algo2_recall,
        cp_on_algo2_f1,
        cp_on_algo2_accuracy,
    ) = cal_prfa(cp_on_algo2_tp, cp_on_algo2_fp, cp_on_algo2_fn)

    (
        cp_ov_algo2_precision,
        cp_ov_algo2_recall,
        cp_ov_algo2_f1,
        cp_ov_algo2_accuracy,
    ) = cal_prfa(cp_ov_algo2_tp, cp_ov_algo2_fp, cp_ov_algo2_fn)

    (
        cp_m_algo3_precision,
        cp_m_algo3_recall,
        cp_m_algo3_f1,
        cp_m_algo3_accuracy,
    ) = cal_prfa(cp_m_algo3_tp, cp_m_algo3_fp, cp_m_algo3_fn)

    (
        cp_on_algo3_precision,
        cp_on_algo3_recall,
        cp_on_algo3_f1,
        cp_on_algo3_accuracy,
    ) = cal_prfa(cp_on_algo3_tp, cp_on_algo3_fp, cp_on_algo3_fn)

    (
        cp_ov_algo3_precision,
        cp_ov_algo3_recall,
        cp_ov_algo3_f1,
        cp_ov_algo3_accuracy,
    ) = cal_prfa(cp_ov_algo3_tp, cp_ov_algo3_fp, cp_ov_algo3_fn)

    print(f"baseline: {csv_path}")
    print(f"Module level: {module_all_res}")
    print(f"Option name level: {option_name_all_res}")
    print(f"Option value level: {option_value_all_res}")
    print("failed to parse:", failed_cnt)
    return_list = [
        failed_cnt,
        m_precision,
        m_recall,
        m_f1,
        m_accuracy,
        on_precision,
        on_recall,
        on_f1,
        on_accuracy,
        ov_precision,
        ov_recall,
        ov_f1,
        ov_accuracy,
        m_rule_correct,
        on_rule_correct,
        ov_rule_correct,
        exist_mapping_tp,
        exist_mapping_fp,
        exist_mapping_fn,
        exist_mapping_precision,
        exist_mapping_recall,
        exist_mapping_f1,
        exist_mapping_accuracy,
        cp_m_algo1_tp,
        cp_m_algo1_fp,
        cp_m_algo1_fn,
        cp_m_algo1_precision,
        cp_m_algo1_recall,
        cp_m_algo1_f1,
        cp_m_algo1_accuracy,
        cp_on_algo1_tp,
        cp_on_algo1_fp,
        cp_on_algo1_fn,
        cp_on_algo1_precision,
        cp_on_algo1_recall,
        cp_on_algo1_f1,
        cp_on_algo1_accuracy,
        cp_ov_algo1_tp,
        cp_ov_algo1_fp,
        cp_ov_algo1_fn,
        cp_ov_algo1_precision,
        cp_ov_algo1_recall,
        cp_ov_algo1_f1,
        cp_ov_algo1_accuracy,
        cp_m_algo2_tp,
        cp_m_algo2_fp,
        cp_m_algo2_fn,
        cp_m_algo2_precision,
        cp_m_algo2_recall,
        cp_m_algo2_f1,
        cp_m_algo2_accuracy,
        cp_on_algo2_tp,
        cp_on_algo2_fp,
        cp_on_algo2_fn,
        cp_on_algo2_precision,
        cp_on_algo2_recall,
        cp_on_algo2_f1,
        cp_on_algo2_accuracy,
        cp_ov_algo2_tp,
        cp_ov_algo2_fp,
        cp_ov_algo2_fn,
        cp_ov_algo2_precision,
        cp_ov_algo2_recall,
        cp_ov_algo2_f1,
        cp_ov_algo2_accuracy,
        cp_m_algo3_tp,
        cp_m_algo3_fp,
        cp_m_algo3_fn,
        cp_m_algo3_precision,
        cp_m_algo3_recall,
        cp_m_algo3_f1,
        cp_m_algo3_accuracy,
        cp_on_algo3_tp,
        cp_on_algo3_fp,
        cp_on_algo3_fn,
        cp_on_algo3_precision,
        cp_on_algo3_recall,
        cp_on_algo3_f1,
        cp_on_algo3_accuracy,
        cp_ov_algo3_tp,
        cp_ov_algo3_fp,
        cp_ov_algo3_fn,
        cp_ov_algo3_precision,
        cp_ov_algo3_recall,
        cp_ov_algo3_f1,
        cp_ov_algo3_accuracy,
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
            "m_precision",
            "m_recall",
            "m_f1",
            "m_accuracy",
            "on_precision",
            "on_recall",
            "on_f1",
            "on_accuracy",
            "ov_precision",
            "ov_recall",
            "ov_f1",
            "ov_accuracy",
            "m_rule_correct",
            "on_rule_correct",
            "ov_rule_correct",
            "exist_mapping_tp",
            "exist_mapping_fp",
            "exist_mapping_fn",
            "exist_mapping_precision",
            "exist_mapping_recall",
            "exist_mapping_f1",
            "exist_mapping_accuracy",
            "cp_m_algo1_tp",
            "cp_m_algo1_fp",
            "cp_m_algo1_fn",
            "cp_m_algo1_precision",
            "cp_m_algo1_recall",
            "cp_m_algo1_f1",
            "cp_m_algo1_accuracy",
            "cp_on_algo1_tp",
            "cp_on_algo1_fp",
            "cp_on_algo1_fn",
            "cp_on_algo1_precision",
            "cp_on_algo1_recall",
            "cp_on_algo1_f1",
            "cp_on_algo1_accuracy",
            "cp_ov_algo1_tp",
            "cp_ov_algo1_fp",
            "cp_ov_algo1_fn",
            "cp_ov_algo1_precision",
            "cp_ov_algo1_recall",
            "cp_ov_algo1_f1",
            "cp_ov_algo1_accuracy",
            "cp_m_algo2_tp",
            "cp_m_algo2_fp",
            "cp_m_algo2_fn",
            "cp_m_algo2_precision",
            "cp_m_algo2_recall",
            "cp_m_algo2_f1",
            "cp_m_algo2_accuracy",
            "cp_on_algo2_tp",
            "cp_on_algo2_fp",
            "cp_on_algo2_fn",
            "cp_on_algo2_precision",
            "cp_on_algo2_recall",
            "cp_on_algo2_f1",
            "cp_on_algo2_accuracy",
            "cp_ov_algo2_tp",
            "cp_ov_algo2_fp",
            "cp_ov_algo2_fn",
            "cp_ov_algo2_precision",
            "cp_ov_algo2_recall",
            "cp_ov_algo2_f1",
            "cp_ov_algo2_accuracy",
            "cp_m_algo3_tp",
            "cp_m_algo3_fp",
            "cp_m_algo3_fn",
            "cp_m_algo3_precision",
            "cp_m_algo3_recall",
            "cp_m_algo3_f1",
            "cp_m_algo3_accuracy",
            "cp_on_algo3_tp",
            "cp_on_algo3_fp",
            "cp_on_algo3_fn",
            "cp_on_algo3_precision",
            "cp_on_algo3_recall",
            "cp_on_algo3_f1",
            "cp_on_algo3_accuracy",
            "cp_ov_algo3_tp",
            "cp_ov_algo3_fp",
            "cp_ov_algo3_fn",
            "cp_ov_algo3_precision",
            "cp_ov_algo3_recall",
            "cp_ov_algo3_f1",
            "cp_ov_algo3_accuracy",
        ],
    )
    stat_df.to_csv("stat.csv", index=False)
