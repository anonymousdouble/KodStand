import os
import sys
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
import util

vs_name_desc = None
vs_name_desc_mopt = None

def create_store_name_desc():
    global vs_name_desc
    if vs_name_desc is None:
        os.environ["OPENAI_API_KEY"] = "sk-proj-0W1mHlj2J2BnYHauKePhT3BlbkFJF3W9NDdOrs0BOkyaOJqh"
        fname = "url_name_desc_mopt"
        jdata = util.load_json("data/rule/checkstyle/java/", fname)
        name_desc_list = []
        for rule in jdata:
            rule_name = rule[1]
            rule_desc = rule[2]
            prefix = "Description"
            if rule_desc.startswith(prefix):
                rule_desc = rule_desc[len(prefix):]
            rule_desc = rule_desc.strip()
            name_desc_list.append(
                f"[Rule]\n{rule_name}\n[Description]\n{rule_desc}")
        embedmodel = OpenAIEmbeddings()
        vs_name_desc = Chroma.from_texts(name_desc_list, embedmodel)
    return vs_name_desc

def create_store_name_desc_mopt():
    global vs_name_desc_mopt
    if vs_name_desc_mopt is None:
        fname = "url_name_desc_mopt"
        jdata = util.load_json("data/rule/checkstyle/java/", fname)
        name_desc_mopt_list = []
        for rule in jdata:
            rule_name = rule[1]
            rule_desc = rule[2]
            prefix = "Description"
            if rule_desc.startswith(prefix):
                rule_desc = rule_desc[len(prefix):]
            rule_desc = rule_desc.strip()
            rule_str = f"[Rule]\n{rule_name}\n[Description]\n{rule_desc}"
            if len(rule) == 4:
                rule_str += f"\n[Options]{rule[3]}"
            name_desc_mopt_list.append(rule_str)
        embedmodel = OpenAIEmbeddings()
        vs_name_desc_mopt = Chroma.from_texts(name_desc_mopt_list, embedmodel)
    return vs_name_desc_mopt

def augmented_name_desc_str(query:str, candadite_num:int=10):
    results = create_store_name_desc().similarity_search(query,k=candadite_num)
    source_knowledge = "\n".join([x.page_content for x in results])
    return source_knowledge

def augmented_name_desc_mopt_str(query:str,candadite_num:int=10):
    results = create_store_name_desc_mopt().similarity_search(query,k=candadite_num)
    source_knowledge = "\n".join([x.page_content for x in results])
    return source_knowledge