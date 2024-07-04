import os
import shutil
import sys
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
import json

dbm = None
os.environ["OPENAI_API_KEY"] = (
    "sk-proj-pl6tyVRB5V7vbQj4NSNdT3BlbkFJlCzsHfc8jFzoEhzLgbfD"
)


class DBManager:

    def __init__(self) -> None:

        self.name_desc_db = Chroma(
            persist_directory="data/Chroma/eslint/name_desc",
            embedding_function=OpenAIEmbeddings(),
        )
        self.name_desc_opt_db = Chroma(
            persist_directory="data/Chroma/eslint/name_desc_opt",
            embedding_function=OpenAIEmbeddings(),
        )
        self.name_sdesc_opt_db = Chroma(
            persist_directory="data/Chroma/eslint/name_sdesc_opt",
            embedding_function=OpenAIEmbeddings(),
        )

    def get_name_desc_db(self):
        return self.name_desc_db

    def get_name_desc_opt_db(self):
        return self.name_desc_opt_db

    def get_name_sdesc_opt_db(self):
        return self.name_sdesc_opt_db


def cdb_name_desc():
    with open("data/rule/eslint/url_sum_desc_opt.json") as f:
        jdata = json.load(f)
    rule_data_list = []
    for rule,rule_data in jdata.items():
        rule_name = rule
        overview = rule_data[1]
        details = rule_data[2]
        rule_options = rule_data[3]
        rule_str = f"[Rule]\n{rule_name}\n[Overview]\n{overview}"
        if details != "":
            rule_str += f"\n[Details]\n{details}"
        # if rule_options != "":
        #     rule_str += f"\n[Options]\n{rule_options}"
        rule_data_list.append(rule_str)

    embedmodel = OpenAIEmbeddings()
    # 清空目录

    vs_name_desc = Chroma.from_texts(
        rule_data_list,
        embedmodel,
        persist_directory="data/Chroma/eslint/name_desc",
    )
    vs_name_desc.persist()
    return vs_name_desc


def cdb_name_desc_opt():
    with open("data/rule/eslint/url_sum_desc_opt.json") as f:
        jdata = json.load(f)
    rule_data_list = []
    for rule,rule_data in jdata.items():
        rule_name = rule
        overview = rule_data[1]
        details = rule_data[2]
        rule_options = rule_data[3]
        rule_str = f"[Rule]\n{rule_name}\n[Overview]\n{overview}"
        if details != "":
            rule_str += f"\n[Details]\n{details}"
        if rule_options != "":
            rule_str += f"\n[Options]\n{rule_options}"
        rule_data_list.append(rule_str)
    embedmodel = OpenAIEmbeddings()
    vs_name_desc_mopt = Chroma.from_texts(
        rule_data_list,
        embedmodel,
        persist_directory="data/Chroma/eslint/name_desc_opt",
    )
    vs_name_desc_mopt.persist()
    return vs_name_desc_mopt

def cdb_name_sdesc_opt():
    with open("data/rule/eslint/url_sum_desc_opt.json") as f:
        jdata = json.load(f)
    rule_data_list = []
    for rule,rule_data in jdata.items():
        rule_name = rule
        overview = rule_data[1].split("\n")[0]
        rule_options = rule_data[3]
        rule_str = f"[Rule]\n{rule_name}\n[Overview]\n{overview}"
        if rule_options != "":
            rule_str += f"\n[Options]\n{rule_options}"
        rule_data_list.append(rule_str)
    embedmodel = OpenAIEmbeddings()
    vs_name_sdesc_opt = Chroma.from_texts(
        rule_data_list,
        embedmodel,
        persist_directory="data/Chroma/eslint/name_sdesc_opt",
    )
    vs_name_sdesc_opt.persist()
    return vs_name_sdesc_opt

def augmented_name_desc_str(query: str, candadite_num: int = 10):
    global dbm
    if dbm is None:
        dbm = DBManager()
    
    x = dbm.get_name_desc_db().as_retriever()
    results = dbm.get_name_desc_db().similarity_search(query, k=candadite_num)
    source_knowledge = "\n".join([x.page_content for x in results])
    return source_knowledge


def augmented_name_desc_opt_str(query: str, candadite_num: int = 10):
    global dbm
    if dbm is None:
        dbm = DBManager()
    results = dbm.get_name_desc_opt_db().similarity_search(query, k=candadite_num)
    source_knowledge = "\n".join([x.page_content for x in results])
    return source_knowledge

def augmented_name_sdesc_opt_str(query: str, candadite_num: int = 10):
    global dbm
    if dbm is None:
        dbm = DBManager()
    results = dbm.get_name_sdesc_opt_db().similarity_search(query, k=candadite_num)
    source_knowledge = "\n".join([x.page_content for x in results])
    return source_knowledge

if __name__ == "__main__":
    root = "data/Chroma/eslint/name_desc"
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root)
    root = "data/Chroma/eslint/name_desc_opt"
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root)
    root = "data/Chroma/eslint/name_sdesc_opt"
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root)
    cdb_name_desc()
    cdb_name_desc_opt()
    cdb_name_sdesc_opt()