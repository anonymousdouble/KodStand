import pandas as pd
from xml.etree import ElementTree as ET
import json
import re
import os
import copy
import util
invalid_config_form_count = 0
xlist = []


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
            # iv_p += 1
            ...
        else:
            precision += p
        if type(r) == str:
            # iv_r += 1
            ...
        else:
            recall += r
        if type(f) == str:
            # iv_f += 1
            ...
        else:
            f1 += f

    # print(
    #     f"valid precision: {n - iv_p}/{n}, valid recall: {n - iv_r}/{n}, valid f1: {n - iv_f}/{n}"
    # )
    macro_p = precision / (n - iv_p) if n - iv_p else ""
    macro_r = recall / (n - iv_r) if n - iv_r else ""
    macro_f1 = f1 / (n - iv_f) if n - iv_f else ""
    return macro_p, macro_r, macro_f1


def cal_micro_prf(data):
    tp = sum(data[0])
    fp = sum(data[2])
    fn = sum(data[3])
    return cal_prf(tp, fp, fn)


def option_value_equal(value_1, value_2):
    if value_1 == "OurSetDefault" or value_2 == "OurSetDefault":
        return True
    str_pattern = r'^".*"$'
    if isinstance(value_1, str) and re.fullmatch(str_pattern, value_1):
        raise ValueError
    if isinstance(value_2, str) and re.fullmatch(str_pattern, value_2):
        raise ValueError

    return value_1 == value_2


def compare_config(gpt_answer, benchmark, benchmark_default, check_option_match_func):
    """
    比较 benchmark 和 gpt answer 对于同一个 rule 的配置
    """
    module_tp = {}
    option_name_tp = {}
    option_value_tp = {}


    module_fp: dict = copy.deepcopy(gpt_answer)
    option_name_fp: dict = copy.deepcopy(gpt_answer)
    option_value_fp: dict = copy.deepcopy(gpt_answer)

    module_fn: dict = copy.deepcopy(benchmark)
    option_name_fn: dict = copy.deepcopy(benchmark)
    option_value_fn: dict = copy.deepcopy(benchmark)
    for gpt_rule_name, gpt_rule_config in gpt_answer.items():
        if gpt_rule_name == "rules":
            aa = 1
        if not isinstance(gpt_rule_config, list) and not isinstance(
            gpt_rule_config, str
        ):
            # 非法配置，直接跳过

            # continue
            # if isinstance(gpt_rule_config, dict):
            gpt_rule_config = [gpt_rule_config]
            # else:
            #     global invalid_config_form_count
            #     invalid_config_form_count += 1
            #     global xlist
            #     xlist.append((gpt_rule_name, gpt_rule_config))

            # ! 这样是否合适

        # TODO check pop
        if gpt_rule_name in module_fn.keys():
            module_tp[gpt_rule_name] = gpt_rule_config
            module_fn.pop(gpt_rule_name)
            module_fp.pop(gpt_rule_name)

        if gpt_rule_name in option_name_fn.keys():
            # TODO check
            # TODO 实现default
            # default_rule_config = default_config[gpt_rule_name]
            benchmark_rule_config = option_name_fn[gpt_rule_name]
            benchmark_rule_default_config = benchmark_default[gpt_rule_name]
            all_prop_name_match, all_prop_value_match = check_option_match_func(
                gpt_rule_config, benchmark_rule_config, benchmark_rule_default_config
            )
            if all_prop_name_match:
                option_name_tp[gpt_rule_name] = gpt_rule_config
                option_name_fn.pop(gpt_rule_name)
                option_name_fp.pop(gpt_rule_name)

        if gpt_rule_name in option_value_fn.keys():
            # TODO check
            # TODO 实现default
            # default_rule_config = default_config[gpt_rule_name]
            benchmark_rule_config = option_value_fn[gpt_rule_name]
            benchmark_rule_default_config = benchmark_default[gpt_rule_name]
            all_prop_name_match, all_prop_value_match = check_option_match_func(
                gpt_rule_config, benchmark_rule_config, benchmark_rule_default_config
            )
            if all_prop_value_match:
                option_value_tp[gpt_rule_name] = gpt_rule_config
                option_value_fn.pop(gpt_rule_name)
                option_value_fp.pop(gpt_rule_name)

    module_res = [list(module_tp.keys()), [], list(module_fp.keys()), list(module_fn.keys())]

    option_name_res = [list(option_name_tp.keys()), [], list(option_name_fp.keys()), list(option_name_fn.keys())]

    option_value_res = [list(option_value_tp.keys()), [], list(option_value_fp.keys()), list(option_value_fn.keys())]
    return [module_res, option_name_res, option_value_res]


def check_option_match(gpt_config, benchmark_config, benchmark_default_config):
    """
    对于一个 module ，从 module option name 和 option value 两个维度比较 benchmark 和 gpt answer

    简单判断，只考虑是否完全相等
    """
    #! 对于匿名option，如何计算 option name match？
    # config: [] or ""
    config_on_match, config_ov_match = check_option_match_benchmark(gpt_config, benchmark_config)
    default_on_match, default_ov_match = check_option_match_benchmark(gpt_config, benchmark_default_config)
    on_match = config_on_match or default_on_match
    ov_match = config_ov_match or default_ov_match
    if config_on_match ^ default_on_match:
        aa = 1
    if config_ov_match ^ default_ov_match:
        bb = 1
    return on_match, ov_match

def check_option_match_benchmark(gpt_config, benchmark_config):
    """
    
    """
    on_match = True
    ov_match = True

    if isinstance(gpt_config, list):
        if "error" not in gpt_config:
            gpt_config.append("error")

    if isinstance(gpt_config, str):
        # gpt: 'error'
        if not isinstance(benchmark_config, str) or gpt_config != benchmark_config:
            ov_match = False
            on_match = False
    elif isinstance(benchmark_config, str):
        # benchmark: 'error'
        # ! gpt: should be list
        if not isinstance(gpt_config, list):
            print(f"invalid config type: {gpt_config}")
            raise ValueError
        if len(gpt_config) > 1:
            ov_match = False
            on_match = False
        elif len(gpt_config) == 1:
            if gpt_config[0] != benchmark_config:
                # ["error"] case
                ov_match = False
                on_match = False
            else:
                ...
        else:
            print(f"how come? {gpt_config}")
            raise ValueError
    else:
        # gpt: list, benchmark: list
        name_in_bm, value_in_bm = options_in(
            gpt_config, benchmark_config
        )
        name_in_gpt, value_in_gpt = options_in(
            benchmark_config, gpt_config
        )
        if not name_in_bm or not name_in_gpt:
            on_match = False
        if not value_in_bm or not value_in_gpt:
            ov_match = False
        if (name_in_bm ^ name_in_gpt):
            aa = 1
        if (value_in_bm ^ value_in_gpt):
            bb = 1
        ...
    return on_match,ov_match


def options_in(child_set, parent_set):
    """
    判断a中的option是否都在b中
    """
    name_in = True
    value_in = True
    tmp_child: list = copy.deepcopy(child_set)
    # simplify tmp_child
    tmp_child = remove_irrelevant_elements(tmp_child)
    tmp_child = remove_empty_elements(tmp_child)

    for parent_option in parent_set:
        if isinstance(parent_option, dict):
            parent_keys = parent_option.keys()
            matched_child_option: dict = None
            for child_option in tmp_child:
                if isinstance(child_option, dict):
                    child_keys = child_option.keys()
                    if all([k in parent_keys for k in child_keys]):
                        matched_child_option = child_option
                        break
            if matched_child_option:
                tmp_child.remove(matched_child_option)
        else:
            if parent_option in tmp_child:
                tmp_child.remove(parent_option)
    if len(tmp_child) > 0:
        name_in = False
    
    tmp_child: list = copy.deepcopy(child_set)
    tmp_child = remove_irrelevant_elements(tmp_child)
    tmp_child = remove_empty_elements(tmp_child)

    for parent_option in parent_set:
        if isinstance(parent_option, dict):
            ...
            # TODO handle OurSetDefault
            parent_keys = parent_option.keys()
            matched_child_option: dict = None
            for child_option in tmp_child:
                if isinstance(child_option, dict):
                    child_keys = child_option.keys()
                    if all([k in parent_keys for k in child_keys]):
                        matched_child_option = child_option
                        break
            if matched_child_option:
                dict_value_match = True
                for k in matched_child_option:
                    if not option_value_equal(parent_option[k], matched_child_option[k]):
                        dict_value_match = False
                        break
                if dict_value_match:
                    tmp_child.remove(matched_child_option)
                else:
                    ...  # 存在 dict, all keys match, 但值不相同
            else:
                ...  # 不存在 dict 满足 all keys match
        else:
            if parent_option in tmp_child:  # ?
                tmp_child.remove(parent_option)
    if len(tmp_child) > 0:
        value_in = False
    else:
        if not name_in:
            raise ValueError(f"value in but name not in")
    return name_in, value_in

def remove_empty_elements(data):
    if isinstance(data, list):
        return [remove_empty_elements(item) for item in data if item not in ([], {})]
    elif isinstance(data, dict):
        return {key: remove_empty_elements(value) for key, value in data.items() if value not in ([], {})}
    else:
        return data

def remove_irrelevant_elements(data):
    if isinstance(data, list):
        return [remove_irrelevant_elements(child) for child in data if child != "OurSetDefault"]
    elif isinstance(data, dict):
        return {k: remove_irrelevant_elements(v) for k, v in data.items() if v != "OurSetDefault"}
    else:
        return data


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
        try:
            root = eval(answer)
            if not isinstance(root, dict):
                raise Exception("failed to convert string to dict")
        except Exception as e:
            # print(f"failed to parse json: {e}")
            root = None
            return INVALID_CONFIG, root
        return VALID_CONFIG, root
    return NO_CONFIG, None


def compare_and_cal_metrics(csv_path, benchmark_path, check_option_match_func):
    """
    比较所有 gpt answer 和 benchmark 的配置，计算各种指标
    """

    data = pd.read_csv(csv_path)
    # data = util.load_csv(csv_path)


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
    useless_configs = 0
    invalid_configs = 0
    rule_count = 0
    for _, line in data.iterrows():
        rule = line["rule_name"]
        if rule == "2.2 File encoding: UTF-8" and "name_url_sdesc" in csv_path:
            aa = 1  # debug
        if rule not in jdata:
            print(f"rule {rule} not in benchmark")
            continue
        # print(f"Processing rule: {rule}")
        rule_count += 1
        cor_benchmark,cor_benchmark_default,cor_benchmark_third = jdata[rule]
        benchmark_exist_config = len(cor_benchmark) > 0
        line_result = [
            line["rule_name"],
            line["description"],
            "\n".join([f"{rule}: {config}" for rule, config in cor_benchmark.items()]),
            "\n".join([f"{rule}: {config}" for rule, config in cor_benchmark_default.items()]),
            "\n".join([f"{rule}: {config}" for rule, config in cor_benchmark_third.items()]),
            line["gpt_answer"],
            line["gpt_configuration"],
        ]
        answer_stat, answer_json = get_answer_config(line)
        if answer_stat == 0:
            if not benchmark_exist_config:
                exmap_tn += 1
                rule_m_correct += 1
                rule_on_correct += 1
                rule_ov_correct += 1
            else:
                exmap_fn += 1
                # all false negative
                line_result.append("false")
                error_data = [
                    "",
                    "",
                    "\n".join([rule_name for rule_name in cor_benchmark]),
                ]
                line_result.extend(error_data * 3)
                error_res = [0, 0, 0, len(cor_benchmark)]
                for i in range(4):
                    m_all_res[i].append(error_res[i])
                    on_all_res[i].append(error_res[i])
                    ov_all_res[i].append(error_res[i])
        elif answer_stat == 1:
            if benchmark_exist_config:
                exmap_tp += 1
            else:
                exmap_fp += 1
                useless_configs += len(answer_json)
                # continue

            line_result.append("true")
            if not isinstance(answer_json, dict):
                aa = 1
            answer_str = "\n".join([f"{k}: {v}" for k, v in answer_json.items()])
            line_result[5] = answer_str

            # ! 分别使用 benchmark + default 和 third config 进行比较
            compare_result = compare_config(
                answer_json,
                cor_benchmark,
                cor_benchmark_default,
                check_option_match_func,
            )
            if cor_benchmark_third != {}:
                compare_result_third = compare_config(
                    answer_json,
                    cor_benchmark_third,
                    cor_benchmark_third,
                    check_option_match_func
                )
                for i in range(3):

                    # TP 取并集
                    origin_fp = copy.deepcopy(compare_result[i][2])
                    third_tp = copy.deepcopy(compare_result_third[i][0])
                    for rule_name in origin_fp:
                        if rule_name in third_tp:
                            compare_result[i][2].remove(rule_name)
                            compare_result[i][0].append(rule_name)

                    origin_fn = compare_result[i][3]
                    third_fn = compare_result_third[i][3]
                    # FN 取小的
                    if len(origin_fn) > len(third_fn):
                        compare_result[i][3] = third_fn
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
            ## TODO 针对 json格式修改
            for i, j in indices:
                line_result.append(
                    "\n".join([rule_name for rule_name in compare_result[i][j]])
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
            # invalid config
            # 对于benchmark存在config情况，将benchmark中所有rule作为FN，忽略 invalid config string中提取出的所有rule
            # 对于benchmark不存在config情况，将invalid config string中提取出的所有rule作为FP
            line_result.append("false")
            failed_cnt += 1
            if benchmark_exist_config:
                ##! method 1: ignore invalid config
                exmap_tp += 1
                error_res = [0, 0, 0, len(cor_benchmark)]
                
                ## ! method2 : treat invalid config as false negative
                # rule_name_pattern = (
                #     r"['\"](\w+(-\w+)*)['\"]: \[|['\"](\w+(-\w+)*)['\"]: \"error\""
                # )
                # rule_names = [
                #     x[0] if x[0] != "" else x[2]
                #     for x in re.findall(rule_name_pattern, line["gpt_configuration"])
                # ]
                # rule_names = set(rule_names)
                # error_data = [
                #     "",
                #     "\n".join([rule_name for rule_name in rule_names]),
                #     "\n".join([rule_name for rule_name in cor_benchmark]),
                # ]
                # line_result.extend(error_data * 3)
                # error_res = [0, 0, len(rule_names), len(cor_benchmark)]
                for i in range(4):
                    m_all_res[i].append(error_res[i])
                    on_all_res[i].append(error_res[i])
                    ov_all_res[i].append(error_res[i])
            else:
                exmap_fp += 1
                rule_name_pattern = (
                    r"['\"](\w+(-\w+)*)['\"]: \[|['\"](\w+(-\w+)*)['\"]: \"error\""
                )
                rule_names = [
                    x[0] if x[0] != "" else x[2]
                    for x in re.findall(rule_name_pattern, line["gpt_configuration"])
                ]
                rule_names = set(rule_names)
                if len(rule_names) == 0:
                    aa = 1
                # print(f"invalid config: {rule_names}")
                invalid_configs += len(rule_names)
                error_data = [
                    "",
                    "\n".join([rule_name for rule_name in rule_names]),
                    "",
                ]
                line_result.extend(error_data * 3)
                error_res = [0, 0, len(rule_names), 0]
                for i in range(4):
                    m_all_res[i].append(error_res[i])
                    on_all_res[i].append(error_res[i])
                    ov_all_res[i].append(error_res[i])
        output_csv_data.append(line_result)

    output_df = pd.DataFrame(
        output_csv_data,
        columns=[
            "rule_name",
            "description",
            "benchmark",
            "benchmark_default",
            "benchmark_third",
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
    benchmark_module_count = sum([len(x) for _, x in jdata.items()])
    print(f"+ {useless_configs} useless configs")
    print(f"+ {invalid_configs} invalid configs")
    # print("tp + fp = answer module count")
    # print("tp + fn = benchmark module count")
    print(f"benchmark module count: {benchmark_module_count}")
    print(f"Module level: {[sum(x) for x in m_all_res]}")
    print(f"Option name level: {[sum(x) for x in on_all_res]}")
    print(f"Option value level: {[sum(x) for x in ov_all_res]}")
    print("failed to parse:", failed_cnt)

    m_acc = rule_m_correct / rule_count
    on_acc = rule_on_correct / rule_count
    ov_acc = rule_ov_correct / rule_count
    return_list = [
        failed_cnt,
        f"{m_acc*100:.1f}, {rule_m_correct}/{rule_count}",
        f"{on_acc*100:.1f}, {rule_on_correct}/{rule_count}",
        f"{ov_acc*100:.1f}, {rule_ov_correct}/{rule_count}",
        exmap_tp,
        exmap_tn,
        exmap_fp,
        exmap_fn,
        f"{exmap_precision*100:.1f}",
        f"{exmap_recall*100:.1f}",
        f"{exmap_f1*100:.1f}",
        f"{exmap_accuracy*100:.1f}",
        m_all_tp,
        m_all_fp,
        m_all_fn,
        on_all_tp,
        on_all_fp,
        on_all_fn,
        ov_all_tp,
        ov_all_fp,
        ov_all_fn,
        # m_macro_precision,
        # m_macro_recall,
        # m_macro_f1,
        # on_macro_precision,
        # on_macro_recall,
        # on_macro_f1,
        # ov_macro_precision,
        # ov_macro_recall,
        # ov_macro_f1,
        f"{m_micro_precision*100:.1f}",
        f"{m_micro_recall*100:.1f}",
        f"{m_micro_f1*100:.1f}",
        f"{on_micro_precision*100:.1f}",
        f"{on_micro_recall*100:.1f}",
        f"{on_micro_f1*100:.1f}",
        f"{ov_micro_precision*100:.1f}",
        f"{ov_micro_recall*100:.1f}",
        f"{ov_micro_f1*100:.1f}",
    ]
    return return_list


if __name__ == "__main__":
    stat_data = []

    input_data_root = "data/debug/js_res/"
    # input_data_root = "data/config_output/google2eslint_js/baseline"
    benchmark_path = "data/benchmark/google2eslint_js_benchmark_simple_v5.json"

    statistic_path = os.path.join(input_data_root, "stat.csv")
    for file in os.listdir(input_data_root):
        if (
            file.endswith(".csv")
            and not file.endswith("_compared.csv")
            and not file.endswith("stat.csv")
        ):
            res_csv_path = os.path.join(input_data_root, file)
            stat_data.append([file[:-4]])
            print("=====================================")
            print(f"Baseline: {file[:-4]}")
            metrics = compare_and_cal_metrics(
                res_csv_path, benchmark_path, check_option_match
            )
            stat_data[-1].extend(metrics)

    stat_df = pd.DataFrame(
        stat_data,
        columns=[
            "baseline",
            "failed_cnt",
            "m_acc",
            "on_acc",
            "ov_acc",
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
            # "m_macro_precision",
            # "m_macro_recall",
            # "m_macro_f1",
            # "on_macro_precision",
            # "on_macro_recall",
            # "on_macro_f1",
            # "ov_macro_precision",
            # "ov_macro_recall",
            # "ov_macro_f1",
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
    stat_df.to_csv(statistic_path, index=False)
    print(f"invalid config form count: {invalid_config_form_count}")
    for x in xlist:
        print(x[0])
        print(x[1])
        print("=====================================")
