'''
https://eslint.org/docs/latest/rules/
https://eslint.org/docs/latest/rules/array-callback-return#allowvoid

eslint-8.57.0/docs/src/rules
eslint-8.57.0/docs/src/rules/valid-jsdoc.md

msgs: Rule source
https://github.com/eslint/eslint/blob/main/lib/rules/array-callback-return.js
eslint-8.57.0/lib/rules/array-callback-return.js

code examples ---- test cases: Tests source
https://github.com/eslint/eslint/blob/main/tests/lib/rules/array-callback-return.js
eslint-8.57.0/tests/lib/rules

Google JavaScript style
eslint-config-google-master/index.js
https://github.com/google/eslint-config-google/blob/master/index.js
'''
import subprocess
import os
import shutil
import time
from multiprocessing import Pool
import json
import re
from bs4 import BeautifulSoup, Tag
import requests

root_url = "https://eslint.org/docs/v8.x/rules/"
root_path = "data\\rule\\eslint"

titles = ["h1", "h2", "h3", "h4", "h5", "h6", "h7"]
escapes = ['nav',]


def parse_all():
    """
    解析所有rule的html文件
    """
    normal_dir = os.path.join(root_path, "normal")
    deprecated_dir = os.path.join(root_path, "deprecated")
    removed_dir = os.path.join(root_path, "removed")
    for file in os.listdir(normal_dir):
        if file.endswith('.html'):
            parse_single_html(os.path.join(normal_dir, file), normal_dir)
    for file in os.listdir(deprecated_dir):
        if file.endswith('.html'):
            parse_single_html(os.path.join(
                deprecated_dir, file), deprecated_dir)
    for file in os.listdir(removed_dir):
        if file.endswith('.html'):
            parse_single_html(os.path.join(removed_dir, file), removed_dir)


def parse_single_html(file: str, output_path):
    """
    解析单个rule的html
    """
    # 解析html文件
    print(f"parsing {file}")
    with open(file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        data = []
        alters = []
        # 找到所有的 h 标签
        root_node = None
        for node in soup.find_all("div"):
            if node.get('class') is not None and node.get('class')[0] == 'docs-main__content':
                root_node = node
                break
        if root_node is None:
            print(f"err in {file}")
            return
        for child in root_node.children:
            dfs_collect_content(child, data, alters)
            data.append("\n")

        if len(alters) > 0:
            data.append("\n## Replaced by")
            for alter in alters:
                data.append("\n" + alter)

        fname = file.split("/")[-1].split("\\")[-1].replace(".html", ".md")
        md_path = os.path.join(output_path, fname)
        cnt = 0
        with open(md_path, 'w', encoding='utf-8') as f:
            for d in data:
                if d == "\n":
                    cnt += 1
                    if cnt > 2:
                        continue
                else:
                    cnt = 0
                f.write(d)

        # zipped = []
        # with open(md_path, 'r', encoding='utf-8') as f:
        #     lines = f.readlines()
        #     for line in lines:
        #         if line == "- \n":
        #             continue
        #         zipped.append(line)

        # with open(md_path, 'w', encoding='utf-8') as f:
        #     for line in zipped:
        #         f.write(line)


def parse_html_overview(file: str, output_path):
    """
    解析overview界面的html
    """
    # 解析html文件
    with open(file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        rules = []
        deprecated_rules = []
        removed_rules = []
        for node in soup.find_all("article"):
            clas = node.get('class')
            if len(clas) == 1:
                if node.get('class')[0] == 'rule':
                    rules.append(handle_rule(node, ""))
            elif len(clas) == 2:
                if node.get('class')[1] == 'rule--deprecated':
                    deprecated_rules.append(
                        handle_deprecated(node, ""))
                elif node.get('class')[1] == 'rule--removed':
                    rule, alters = handle_removed(node, "")
                    removed_rules.append((rule, alters))
        with open(output_path, "w", encoding="utf-8") as f:
            for r in rules:
                f.write(f"{r}\n")
            for r in deprecated_rules:
                f.write(f"{r}\n")


def dfs_collect_content(node: Tag, data: list, alters: list):

    def wrap_title(node):
        level = int(node.name[-1])
        prefix = level * '#'
        content = f"{prefix} {node.text}"
        if level == 1:
            content += "\n## Overview"
        return content

    def wrap_code_block(node: Tag):
        text = node.text
        text = '\n'.join(text.split('\n')[:-1])
        content = f"\n```json\n{text}\n```\n"
        return content

    def wrap_text(node: str):
        content = node
        return content

    def wrap_herf(node):
        content = node.text.strip().strip('\n').strip()
        if content != "":
            if "Open in Playground" in content:
                return ""
            content = f"{content} "
        return content

    def wrap_code(node: Tag):
        content = f"`{node.text}`"
        return content

    if type(node) is not Tag:
        content = wrap_text(node)
        data.append(content)
        return
    elif node.name == "pre":
        content = wrap_code_block(node)
        data.append(content)
        return
    elif node.name == "a":
        content = wrap_herf(node)
        if content != "":
            data.append(content)
        return
    elif node.name == "code":
        content = wrap_code(node)
        data.append(content)
        return
    elif node.name == "div":
        clas = node.get("class")
        if clas and clas[0] == "rule-categories":
            return
    elif node.name == "li":
        data.append(f"\n- ")
    elif node.name in titles:
        content = wrap_title(node)
        data.append(content)
        return
    elif node.name in escapes:
        return
    elif node.name == 'aside':
        text = node.text.strip('\n').split('. ')[0]
        # print(text)
        text = text[text.find("the") + 4:-6]
        text = text.replace(" and ", " ")
        alters.extend([r.strip() for r in text.strip().split(' ')])
        return
    for child in node.children:
        dfs_collect_content(child, data, alters)


def handle_rule(node, dir, get_detail=False):
    # print("hello")
    rule = node.text.split('\n')[1]
    if get_detail:
        url = root_url + rule
        response = requests.get(url)
        path = os.path.join(dir, rule+'.html')
        if response.status_code == 200:
            with open(path, "w", encoding="utf-8") as f:
                f.write(requests.get(url).text)
        else:
            print("err", url)
    return rule


def handle_deprecated(node, dir, get_detail=False):
    rule = node.text.split('\n')[2]
    if get_detail:
        url = root_url + rule
        response = requests.get(url)
        path = os.path.join(dir, rule+'.html')
        if response.status_code == 200:
            with open(path, "w", encoding="utf-8") as f:
                f.write(requests.get(url).text)
        else:
            print("err", url)
    return rule


def handle_removed(node, dir, get_detail=False):
    text = node.text.split('\n')
    rule = text[2]
    alters = text[4].split(" ")[2:]
    if get_detail:
        if alters[0] == 'no-confusing-arrowno-constant-condition':
            alters = ['no-confusing-arrow', 'no-constant-condition']
        elif alters[0] == 'object-curly-spacingarray-bracket-spacing':
            alters = ['object-curly-spacing', 'array-bracket-spacing']
        url = root_url + rule
        response = requests.get(url)
        path = os.path.join(dir, rule+'.html')
        if response.status_code == 200:
            with open(path, "w", encoding="utf-8") as f:
                f.write(requests.get(url).text)
        else:
            print("err", url)
    return rule, alters


def get_rules():
    os.makedirs(root_path, exist_ok=True)
    normal_dir = os.path.join(root_path, "normal")
    if not os.path.exists(normal_dir):
        os.mkdir(normal_dir)
    deprecated_dir = os.path.join(root_path, "deprecated")
    if not os.path.exists(deprecated_dir):
        os.mkdir(deprecated_dir)
    removed_dir = os.path.join(root_path, "removed")
    if not os.path.exists(removed_dir):
        os.mkdir(removed_dir)
    response = requests.get(root_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        rules = []
        deprecated_rules = []
        removed_rules = []
        for node in soup.find_all("article"):
            clas = node.get('class')
            if len(clas) == 1:
                if node.get('class')[0] == 'rule':
                    rules.append(handle_rule(node, normal_dir))
            elif len(clas) == 2:
                if node.get('class')[1] == 'rule--deprecated':
                    deprecated_rules.append(
                        handle_deprecated(node, deprecated_dir))
                elif node.get('class')[1] == 'rule--removed':
                    rule, alters = handle_removed(node, removed_dir)
                    removed_rules.append((rule, alters))


if __name__ == "__main__":
    # parse_all()
