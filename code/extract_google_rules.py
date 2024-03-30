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
        p.append(parent.text.strip(' \n'))
    title:str = p[-1]
    # if "Test double packages and types" in title:
    #     stoptheworld = 1
    current["title"] = title.strip(' \n')
    current["belongs to"] = "/".join(p)
    current["cases"] = []
    cur_case = {"description": "", "example": []}
    record = False
    for node in nodes:
        # fp.write(f"{node.text}")
        if record == True or node.name == "pre":
            cur_case["example"].append(node.text)
            current["cases"].append(cur_case)
            cur_case = {"description": "", "example": []}
            record = False
            continue
        case1 = "Example:".lower() in node.text.lower()
        case2 = "Examples:".lower() in node.text.lower()
        if case1 or case2:
            record = True
        if record:
            # 截取"Example"之后的内容
            if case1:
                if "Example:" in node.text:
                    text = node.text.split("Example:", 1)[1]
                else:
                    text = node.text.split("example:", 1)[1]
            else:
                if "Examples:" in node.text:
                    text = node.text.split("Examples:", 1)[1]
                else:
                    text = node.text.split("examples:", 1)[1]
            # 判断 text中是否包含字母
            if len(re.findall("\w", text)) > 0:
                cur_case["example"].append(text)
                desc = node.text.split(text, 1)[0]
                cur_case["description"] += desc
                current["cases"].append(cur_case)
                cur_case = {"description": "", "example": []}
                record = False
            else:
                cur_case["description"] += node.text
        else:
            cur_case["description"] += node.text
    # 判断cur_case是否为{}
    if cur_case:
        current["cases"].append(cur_case)
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


def extract_and_parse(input_path, output_path):
    os.makedirs(output_path, exist_ok=True)
    for root, dirs, files in os.walk(input_path):
        for file in files:
            if file.endswith(".html"):
                parse_html(os.path.join(root, file), output_path)

if __name__ == "__main__":
    # 遍历google文件夹
    input_path = "data/google/google_go_out"
    output_path = "data/google/google_go_out"
    extract_and_parse(input_path, output_path)
