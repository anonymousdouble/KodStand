import os
import re


def split_by_h2(data: str):
    lines = data.split("\n")
    content_list = []
    data = {}
    record = False
    title = ""
    for line in lines:
        if line.startswith("## "):
            record = True
            if content_list != [] and title != "":
                data[title] = "\n".join(content_list)
                content_list = []
            title = line[3:]
        elif record:
            content_list.append(line)
    data[title] = "\n".join(content_list)
    return data


def find_options_in_details(data: str):
    lines = data.split("\n")
    options = {}
    record = False
    option_data_list = []
    for line in lines:
        if line.startswith("### Options"):
            record = True
            continue
        if record:
            if line.startswith("### "):
                break
            option_data_list.append(line)
    if option_data_list == []:
        return None
    option_info = "\n".join(option_data_list)
    return option_info


def markdown_to_json(data: str):
    """
    只保留Overview, Rule Details, Options三个字段
    """
    splited = split_by_h2(data)
    if "Options" not in splited:
        if "Rule Details" in splited:
            option_info = find_options_in_details(splited["Rule Details"])
            if option_info:
                splited["Options"] = option_info

    result = {}
    if "Overview" in splited:
        result["Overview"] = splited["Overview"].strip()
    if "Rule Details" in splited:
        result["Rule Details"] = splited["Rule Details"].strip()
    if "Options" in splited:
        result["Options"] = splited["Options"].strip()
    return result


if __name__ == "__main__":
    # test
    path = "data/rule/eslint/deprecated/array-bracket-newline.md"
    str_data = open(path, "r", encoding="utf-8").read()
    json_data = markdown_to_json(str_data)
    aa = 1
