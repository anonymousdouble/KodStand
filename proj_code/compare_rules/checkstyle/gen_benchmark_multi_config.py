# 处理 xlsx
import pandas as pd
from xml.etree import ElementTree as ET
import json
def gen_benchmark(file_path):
    df = pd.read_excel(file_path)
    result = {}
    simple_result = {}
    for index, row in df.iterrows():
        rule = row.rule
        desc = row.desc
        res = row.res
        res2 = row.res2
        res3 = row.res3
        try:
            config = xmlstr2json(res)
            config2 = xmlstr2json(res2)
            config3 = xmlstr2json(res3)
        except Exception as e:
            print(f"error in {rule}: {e}")
            continue
        java_desc = "\n".join([rule,desc])
        result[java_desc] = [config, config2, config3]
        simple_result[rule] = [config, config2, config3]
    with open ('data/benchmark/java_benchmark_7.json','w',encoding='utf-8') as f:
        f.write(json.dumps(result,ensure_ascii=False, indent=4))
    with open ('data/benchmark/java_simple_benchmark_7.json','w',encoding='utf-8') as f:
        f.write(json.dumps(simple_result,ensure_ascii=False, indent=4))

def xmlstr2json(res):
    config = []
    if res == res:
        res = ET.fromstring(res)
        for child in res:
            modules = []
            if child.attrib['name'] == 'TreeWalker':
                for subchild in child:
                        module = {}
                        module['modulename'] = subchild.attrib['name']
                        for subsubchild in subchild:
                            if subsubchild.tag == 'property':
                                pname = subsubchild.attrib['name']
                                pvalue = subsubchild.attrib['value']
                                module[pname] = pvalue
                        modules.append(module)
            else:
                module = {}
                module['modulename'] = child.attrib['name']
                for subchild in child:
                    if subchild.tag == 'property':
                        pname = subchild.attrib['name']
                        pvalue = subchild.attrib['value']
                        module[pname] = pvalue
                modules.append(module)
            config.extend(modules)
    return config

if __name__ == '__main__':
    # file_path = 'data/benchmark/checkstyle2google_java_benchmark_old.xlsx'
    # gen_benchmark(file_path)
    file_path = 'data/benchmark/java_bm_7.xlsx'

    gen_benchmark(file_path)