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
    """
    判断xml是否语法？语义正确
    """
    ...
    # sort by key
    sorted_gpt_answer = sorted(gpt_answer, key=lambda x: x["modulename"])

    # TODO 如果配置不合法怎么办？
    return True


def cal_prf(tp, fp, fn):
    recall = tp / (tp + fn) if tp + fn else ""
    precision = tp / (tp + fp) if tp + fp else ""
    f1 = 2 * recall * precision / (recall + precision) if recall and precision else ""
    return precision, recall, f1


def cal_macro_prf(data):
    precision = 0
    recall = 0
    f1 = 0
    n = len(data[0])
    iv_p = 0
    iv_r = 0
    iv_f = 0
    for i in range(n):
        p, r, f = cal_prf(data[0][i], data[2][i], data[3][i])
        # TODO 要不要 skip
        if type(p) == str:
            iv_p += 1
            ...
        else:
            precision += p
        if type(r) == str:
            iv_r += 1
            ...
        else:
            recall += r
        if type(f) == str:
            iv_f += 1
            ...
        else:
            f1 += f

    print(f"valid precision: {n - iv_p}/{n}, valid recall: {n - iv_r}/{n}, valid f1: {n - iv_f}/{n}")
    macro_p = precision / (n - iv_p) if n - iv_p else ""
    macro_r = recall / (n - iv_r) if n - iv_r else ""
    macro_f1 = f1 / (n - iv_f) if n - iv_f else ""
    return macro_p, macro_r, macro_f1


def cal_micro_prf(data):
    tp = sum(data[0])
    fp = sum(data[2])
    fn = sum(data[3])
    return cal_prf(tp, fp, fn)


def compare_config(gpt_answer, benchmark):
    """
    比较 benchmark 和 gpt answer 对于同一个 rule 的配置
    """
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
        module_res = [[], [], [], benchmark]
        option_name_res = [[], [], [], benchmark]
        option_value_res = [[], [], [], benchmark]
    return [module_res, option_name_res, option_value_res]


def check_option_match(gpt_module: dict, benchmark_module: dict):
    """
    对于一个 module ，从 module option name 和 option value 两个维度比较 benchmark 和 gpt answer
    """
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


def get_answer_config(csv_line):
    """
    判断 gpt answer 是否返回一个配置

    返回值：
    0: 不存在配置
    1: 存在配置
    2: 存在配置但是配置不合法
    """
    # ! NO + (Config|Invalid config) = Answer no config
    NO_CONFIG = 0
    VALID_CONFIG = 1
    INVALID_CONFIG = 2

    answer_exist_config = csv_line["gpt_answer"]
    answer_exist_config = (
        answer_exist_config == answer_exist_config
        and answer_exist_config.lower() == "yes"
    )
    if not answer_exist_config:
        return NO_CONFIG, None

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
            return INVALID_CONFIG, root
        return VALID_CONFIG, root
    return NO_CONFIG, None


def compare_and_cal_metrics(csv_path, benchmark_path):
    """
    比较所有 gpt answer 和 benchmark 的配置，计算各种指标
    """

    data = pd.read_csv(csv_path)

    output_csv_data = []
    jdata = json.load(open(benchmark_path))
    failed_cnt = 0

    m_all_res = [[], [], [], []]
    on_all_res = [[], [], [], []]
    ov_all_res = [[], [], [], []]

    rule_m_correct = 0  # TP
    rule_on_correct = 0
    rule_ov_correct = 0

    exmap_tp = 0
    exmap_tn = 0
    exmap_fp = 0
    exmap_fn = 0

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

        answer_stat, answer_config_xml = get_answer_config(line)

        if answer_stat == 0:
            if not benchmark_exist_config:
                exmap_tn += 1
            else:
                exmap_fn += 1
        elif answer_stat == 1:
            if benchmark_exist_config:
                exmap_tp += 1
            else:
                exmap_fp += 1
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
            for i in range(4):
                m_all_res[i].append(module_level_res[i])
                on_all_res[i].append(option_name_level_res[i])
                ov_all_res[i].append(option_value_level_res[i])
            # rule level match
            if module_level_res[2] == 0 and module_level_res[3] == 0:
                rule_m_correct += 1
            # option name level match
            if option_name_level_res[2] == 0 and option_name_level_res[3] == 0:
                rule_on_correct += 1
            # option value level match
            if option_value_level_res[2] == 0 and option_value_level_res[3] == 0:
                rule_ov_correct += 1
        else:
            if benchmark_exist_config:
                exmap_tp += 1
                failed_cnt += 1
                output_csv_data[-1].append("false")
                error_data = [
                    "",
                    "",
                    "\n".join([mod["modulename"] for mod in cor_benchmark]),
                ]
                output_csv_data[-1].extend(error_data * 3)
                error_res = [0, 0, 0, len(cor_benchmark)]
                for i in range(4):
                    m_all_res[i].append(error_res[i])
                    on_all_res[i].append(error_res[i])
                    ov_all_res[i].append(error_res[i])
            else:
                exmap_fp += 1

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

    m_macro_precision, m_macro_recall, m_macro_f1 = cal_macro_prf(m_all_res)
    on_macro_precision, on_macro_recall, on_macro_f1 = cal_macro_prf(on_all_res)
    ov_macro_precision, ov_macro_recall, ov_macro_f1 = cal_macro_prf(ov_all_res)

    m_micro_precision, m_micro_recall, m_micro_f1 = cal_micro_prf(m_all_res)
    on_micro_precision, on_micro_recall, on_micro_f1 = cal_micro_prf(on_all_res)
    ov_micro_precision, ov_micro_recall, ov_micro_f1 = cal_micro_prf(ov_all_res)

    exmap_precision, exmap_recall, exmap_f1 = cal_prf(exmap_tp, exmap_fp, exmap_fn)
    exmap_accuracy = (exmap_tp + exmap_tn) / (exmap_tp + exmap_tn + exmap_fp + exmap_fn)

    m_all_tp, m_all_fp, m_all_fn = (
        sum(m_all_res[0]),
        sum(m_all_res[2]),
        sum(m_all_res[3]),
    )
    on_all_tp, on_all_fp, on_all_fn = (
        sum(on_all_res[0]),
        sum(on_all_res[2]),
        sum(on_all_res[3]),
    )
    ov_all_tp, ov_all_fp, ov_all_fn = (
        sum(ov_all_res[0]),
        sum(ov_all_res[2]),
        sum(ov_all_res[3]),
    )

    print(f"Module level: {[sum(x) for x in m_all_res]}")
    print(f"Option name level: {[sum(x) for x in on_all_res]}")
    print(f"Option value level: {[sum(x) for x in ov_all_res]}")
    print("failed to parse:", failed_cnt)
    return_list = [
        failed_cnt,
        rule_m_correct,
        rule_on_correct,
        rule_ov_correct,
        exmap_tp,
        exmap_tn,
        exmap_fp,
        exmap_fn,
        exmap_precision,
        exmap_recall,
        exmap_f1,
        exmap_accuracy,
        m_all_tp,
        m_all_fp,
        m_all_fn,
        on_all_tp,
        on_all_fp,
        on_all_fn,
        ov_all_tp,
        ov_all_fp,
        ov_all_fn,
        m_macro_precision,
        m_macro_recall,
        m_macro_f1,
        on_macro_precision,
        on_macro_recall,
        on_macro_f1,
        ov_macro_precision,
        ov_macro_recall,
        ov_macro_f1,
        m_micro_precision,
        m_micro_recall,
        m_micro_f1,
        on_micro_precision,
        on_micro_recall,
        on_micro_f1,
        ov_micro_precision,
        ov_micro_recall,
        ov_micro_f1,
    ]
    return return_list


if __name__ == "__main__":
    stat_data = []
    root = "data/gpt_answer"
    bm_path = "data/benchmark/simple_benchmark.json"
    for file in os.listdir(root + "/3.5"):
        if file.endswith(".csv") and not file.endswith("_compared.csv"):
            stat_data.append(["GPT3.5_" + file[:-4]])
            print("=====================================")
            print(f"Model: 3.5\nBaseline: {file[:-4]}")
            stat_data[-1].extend(compare_and_cal_metrics(f"{root}/3.5/{file}", bm_path))
    for file in os.listdir(root + "/4o"):
        if file.endswith(".csv") and not file.endswith("_compared.csv"):
            stat_data.append(["GPT4o_" + file[:-4]])
            print("=====================================")
            print(f"Model: 4o\nBaseline: {file[:-4]}")
            stat_data[-1].extend(compare_and_cal_metrics(f"{root}/4o/{file}", bm_path))

    stat_df = pd.DataFrame(
        stat_data,
        columns=[
            "baseline",
            "failed_cnt",
            "rule_m_correct",
            "rule_on_correct",
            "rule_ov_correct",
            "exmap_tp",
            "exmap_tn",
            "exmap_fp",
            "exmap_fn",
            "exmap_precision",
            "exmap_recall",
            "exmap_f1",
            "exmap_accuracy",
            "m_all_tp",
            "m_all_fp",
            "m_all_fn",
            "on_all_tp",
            "on_all_fp",
            "on_all_fn",
            "ov_all_tp",
            "ov_all_fp",
            "ov_all_fn",
            "m_macro_precision",
            "m_macro_recall",
            "m_macro_f1",
            "on_macro_precision",
            "on_macro_recall",
            "on_macro_f1",
            "ov_macro_precision",
            "ov_macro_recall",
            "ov_macro_f1",
            "m_micro_precision",
            "m_micro_recall",
            "m_micro_f1",
            "on_micro_precision",
            "on_micro_recall",
            "on_micro_f1",
            "ov_micro_precision",
            "ov_micro_recall",
            "ov_micro_f1",
        ],
    )
    stat_df.to_csv("stat.csv", index=False)
