from bs4 import BeautifulSoup
from bs4.element import Tag
import re
import json
import os
import shutil
import requests

titles = ["h1", "h2", "h3", "h4", "h5", "h6", "h7"]


def crawl_page(url, start_url, depth, visited, max_depth, dir):
    if depth > max_depth:
        return
    if url in visited:
        return
    tmp_url = url.removeprefix(start_url)
    tmp_url.strip()
    if tmp_url != "" and not ("#" in tmp_url):
        tmp_url = tmp_url.replace("/", "_")
        path = os.path.join(dir, tmp_url)
        if not url.endswith(".html") and not url.endswith(".xml"):
            path = path + ".html"
        print(path)
        with open(path, "w", encoding="utf-8") as f:
            f.write(requests.get(url).text)
    visited.add(url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            for link in soup.find_all("a"):
                next_url = link.get("href")
                if next_url and start_url in next_url:
                    crawl_page(next_url, start_url, depth + 1, visited, max_depth, dir)
    except Exception as e:
        print("Error crawling:", url)
        print(e)

def crawl_website(start_url, max_depth, output_dir):
    """
    Crawl a website and save the pages in the output_dir
    """
    visited = set()
    os.makedirs(output_dir, exist_ok=True)
    crawl_page(start_url, start_url, 0, visited, max_depth, output_dir)


def is_child(node1: Tag, node2: Tag):
    if node1.name not in titles or node2.name not in titles:
        return None
    return titles.index(node1.name) > titles.index(node2.name)

def save_example(parents, nodes, data: list):
    current = {}
    p = []
    for parent in parents:
        p.append(re.sub('[\n* ]+',' ',parent.text.strip(' \n')))
    title:str = p[-1]
    current["title"] = title.strip(' \n')
    current["belongs to"] = "/".join(p)
    current["cases"] = []
    cur_case = {}
    for node in nodes:
        sdata = []
        dfs_collect_content(node,sdata)
        cur_node_buf = []
        for n,dat in sdata:
            if n != 'pre':
                # 描述节点
                if cur_case.get("description") is None:
                    cur_case["description"] = dat
                else:
                    cur_case["description"] += dat
            else:
                # 代码节点
                if cur_case.get("description") is not None:
                    cur_case["description"] = re.sub('[ ]+',' ',cur_case["description"].strip(" \n"))
                    cur_case["description"] = re.sub('[\n]+','\n',cur_case["description"])
                cur_case["example"] = dat
                cur_node_buf.append(cur_case)
                cur_case = {}
        if cur_case.get("description") is not None and cur_case.get("example") is None:
            cur_case["description"] = re.sub('[ ]+',' ',cur_case["description"].strip(" \n"))
            cur_case["description"] = re.sub('[\n]+','\n',cur_case["description"])
            if cur_case.get("description")!="":
                
                if len(cur_node_buf) > 0:
                    cur_node_buf[-1]["appendix"] = cur_case["description"]
                else:
                    cur_node_buf.append(cur_case)
            cur_case = {}
        current["cases"].extend(cur_node_buf)
    
    merged = []
    buf = {}
    for c in current["cases"]:
        if c.get("example") is None:

            if buf.get("description") is None:
                buf["description"] = c["description"]
            else:
                buf["description"] += f"\n{c['description']}"

        else:
            if c.get("description"):
                if buf.get("description") is None:
                    buf["description"] = c["description"]
                else:
                    buf["description"] += f"\n{c['description']}"
            else:
                # 向上合并
                if len(merged) > 0 and buf.get("description") is None:
                    if merged[-1].get("appendix") is None:
                        merged[-1]["example"] += f"\n{c['example']}"
                        if c.get("appendix"):
                            merged[-1]["appendix"] = c["appendix"]
                        buf = {}
                        continue
            buf["example"] = c['example']
            if c.get("appendix"):
                buf["appendix"] = c["appendix"]
            merged.append(buf)
            buf = {}

    if buf:
        merged.append(buf)
    current["cases"] = merged
    data.append(current)


def parse_html(file: str, output_path, root_level="h2"):
    # 解析html文件
    with open(file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        data = []
        # 找到所有的 h 标签
        for h in soup.find_all(root_level):

            parents = [h]
            nodes = h.find_next_siblings()
            current_data = []
            for node in nodes:
                if node.name == root_level:
                    save_example(parents, current_data, data)
                    current_data.clear()
                    break
                child = is_child(node, parents[-1])
                if child is None:
                    current_data.append(node)
                elif child:
                    save_example(parents, current_data, data)
                    parents.append(node)
                    current_data.clear()
                else:
                    save_example(parents, current_data, data)
                    parents[-1] = node
                    current_data.clear()
            if len(current_data) > 0:
                save_example(parents, current_data, data)
        # data作为 json 存储
        fname = file.replace(".html", ".json").split(os.sep)[-1]
        with open(os.path.join(output_path,fname), "w", encoding="utf-8") as fp:
            print(f"writing {file.replace('.html','.json')}")
            json.dump(data, fp, ensure_ascii=False, indent=4)
        # 将原始html文件存储到output_path
        with open(os.path.join(output_path, file.split(os.sep)[-1]), "w", encoding="utf-8") as fp:
            fp.write(soup.prettify())


def dfs_collect_content(node: Tag, data: list):
    if type(node) is not Tag:
        # print(type(node))
        processed_text = node.strip("\n ")
        if processed_text != "":
            processed_text = re.sub('[\n]+',' ',processed_text)
            processed_text = f"{processed_text} "
            data.append(("string",processed_text))
        else:
            data.append(("string",'\n'))
        return
    if node.name == "pre":
        data.append((node.name,node.text))
        return
    if node.name == "a":
        processed_text = node.text.strip("\n ")
        if processed_text != "":
            processed_text = f"{processed_text} "
            data.append(("a_string",processed_text))
        return
    if node.name == "code":
        processed_text = node.text.strip("\n ").replace("\n", "").replace("\t", "").replace(" ", "")
        processed_text = f"`{processed_text}` "
        data.append((node.name,processed_text))
        return
    for child in node.children:
        dfs_collect_content(child,data)

def extract_and_parse(input_path, output_path):
    os.makedirs(output_path, exist_ok=True)
    for root, dirs, files in os.walk(input_path):
        for file in files:
            if file.endswith(".html"):
                parse_html(os.path.join(root, file), output_path)

if __name__ == "__main__":
    # 遍历google文件夹
    google_path = "data/google/google_output"
    go_path = "data/google/google_go_out"
    extract_and_parse(google_path, google_path)
    extract_and_parse(go_path, go_path)
    #? 为什么有的json中会有' '字符 \u00a0