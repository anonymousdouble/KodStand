import os
import shutil
import sys
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
import json

dbm = None
os.environ["OPENAI_API_KEY"] = (
    "sk-proj-0W1mHlj2J2BnYHauKePhT3BlbkFJF3W9NDdOrs0BOkyaOJqh"
)


class DBManager:

    def __init__(self) -> None:

        self.name_desc_db = Chroma(
            persist_directory="data/Chroma/name_desc",
            embedding_function=OpenAIEmbeddings(),
        )
        self.name_desc_mopt_db = Chroma(
            persist_directory="data/Chroma/name_desc_mopt",
            embedding_function=OpenAIEmbeddings(),
        )

    def get_name_desc_db(self):
        return self.name_desc_db

    def get_name_desc_mopt_db(self):
        return self.name_desc_mopt_db


def cdb_name_desc():
    with open("data/rule/checkstyle/java/url_name_desc_mopt.json") as f:
        jdata = json.load(f)
    name_desc_list = []
    for rule in jdata:
        rule_name = rule[1]
        rule_desc = rule[2]
        prefix = "Description"
        if rule_desc.startswith(prefix):
            rule_desc = rule_desc[len(prefix) :]
        rule_desc = rule_desc.strip()
        name_desc_list.append(f"[Rule]\n{rule_name}\n[Description]\n{rule_desc}")
    embedmodel = OpenAIEmbeddings()
    # 清空目录

    vs_name_desc = Chroma.from_texts(
        name_desc_list,
        embedmodel,
        persist_directory="data/Chroma/name_desc",
    )
    vs_name_desc.persist()
    return vs_name_desc


def cdb_name_desc_mopt():
    with open("data/rule/checkstyle/java/url_name_desc_mopt.json") as f:
        jdata = json.load(f)
    name_desc_mopt_list = []
    for rule in jdata:
        rule_name = rule[1]
        rule_desc = rule[2]
        prefix = "Description"
        if rule_desc.startswith(prefix):
            rule_desc = rule_desc[len(prefix) :]
        rule_desc = rule_desc.strip()
        rule_str = f"[Rule]\n{rule_name}\n[Description]\n{rule_desc}"
        if len(rule) == 4:
            rule_str += f"\n[Options]{rule[3]}"
        name_desc_mopt_list.append(rule_str)
    embedmodel = OpenAIEmbeddings()
    vs_name_desc_mopt = Chroma.from_texts(
        name_desc_mopt_list,
        embedmodel,
        persist_directory="data/Chroma/name_desc_mopt",
    )
    vs_name_desc_mopt.persist()
    return vs_name_desc_mopt


def augmented_name_desc_str(query: str, candadite_num: int = 10):
    global dbm
    if dbm is None:
        dbm = DBManager()
    results = dbm.get_name_desc_db().similarity_search(query, k=candadite_num)
    source_knowledge = "\n".join([x.page_content for x in results])
    return source_knowledge


def augmented_name_desc_mopt_str(query: str, candadite_num: int = 10):
    global dbm
    if dbm is None:
        dbm = DBManager()
    results = dbm.get_name_desc_mopt_db().similarity_search(query, k=candadite_num)
    source_knowledge = "\n".join([x.page_content for x in results])
    return source_knowledge


if __name__ == "__main__":
    # root = "data/Chroma/name_desc"
    # shutil.rmtree(root, ignore_errors=True)
    # os.makedirs(root)
    # root = "data/Chroma/name_desc_mopt"
    # shutil.rmtree(root, ignore_errors=True)
    # os.makedirs(root)
    # cdb_name_desc()
    # cdb_name_desc_mopt()
    query = '2.3.3 Non-ASCII characters\nFor the remaining non-ASCII characters, either the actual Unicode character (e.g. `∞` ) or the equivalent Unicode escape (e.g. `\\u221e` ) is used. The choice depends only on which makes the code easier to read and understand , although Unicode escapes outside string literals and comments are strongly discouraged.\n Tip: In the Unicode escape case, and occasionally even when actual Unicode characters are used, an explanatory comment can be very helpful.\n Examples:\n Example \n Discussion \n `StringunitAbbrev="μs";` \n Best: perfectly clear even without a comment. \n `StringunitAbbrev="\\u03bcs";//"μs"` \n Allowed, but there\'s no reason to do this. \n `StringunitAbbrev="\\u03bcs";//Greeklettermu,"s"` \n Allowed, but awkward and prone to mistakes. \n `StringunitAbbrev="\\u03bcs";` \n Poor: the reader has no idea what this is. \n `return\'\\ufeff\'+content;//byteordermark` \n Good: use escapes for non-printable characters, and comment if necessary.\n Tip: Never make your code less readable simply out of fear that some programs might not handle non-ASCII characters properly. If that should happen, those programs are broken and they must be fixed .'

    resp1 = augmented_name_desc_mopt_str(query)
    resp2 = augmented_name_desc_str(query)
    resp1 = augmented_name_desc_mopt_str(query)
    resp2 = augmented_name_desc_str(query)
    with open('resp1.txt','w') as f:
        f.write(resp1)
    with open('resp2.txt','w') as f:
        f.write(resp2)
