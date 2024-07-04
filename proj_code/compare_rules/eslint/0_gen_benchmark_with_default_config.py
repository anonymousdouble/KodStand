import pandas as pd
import json
import re
if __name__ == "__main__":

    input_csv = "data/benchmark/google2eslint_js_benchmark_v3.csv"
    df = pd.read_csv(input_csv, encoding="utf-8")
    result = {}
    result_simple = {}
    for index, row in df.iterrows(): 
        rule_name = row["rule"]
        rule_desc = row["rule_desc"]
        rule_desc = rule_desc if rule_desc == rule_desc else ""
        config = row["config"]
        config = config if config == config else {}
        default_config = row["default_config"]
        default_config = default_config if default_config == default_config else {}
        if type(config) == str:
            config = re.sub(r"(\w+)((-\w+)*) *:", r'"\1\2":', config)
            # config = f"{{{config}}}"
            config = eval(config) 
        if type(default_config) == str:
            default_config = re.sub(r"(\w+)((-\w+)*) *:", r'"\1\2":', default_config)
            default_config = eval(default_config)
        key = f"{rule_name}\n{rule_desc}" if rule_desc != "" else rule_name
        result[key] = [config, default_config]
        result_simple[rule_name] = [config, default_config]
    json.dump(
        result,
        open("data/benchmark/google2eslint_js_benchmark_v3.json", "w", encoding="utf-8"),
        indent=4,
    )
    json.dump(
        result_simple,
        open("data/benchmark/google2eslint_js_benchmark_simple_v3.json", "w", encoding="utf-8"),
        indent=4,
    )
