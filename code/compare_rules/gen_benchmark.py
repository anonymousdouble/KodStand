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
        java_desc = "\n".join([rule,desc])
        result[java_desc] = config
        simple_result[rule] = config
    with open ('data/benchmark/benchmark.json','w',encoding='utf-8') as f:
        f.write(json.dumps(result,ensure_ascii=False, indent=4))
    with open ('data/benchmark/simple_benchmark.json','w',encoding='utf-8') as f:
        f.write(json.dumps(simple_result,ensure_ascii=False, indent=4))

if __name__ == '__main__':
    file_path = 'data/benchmark/checkstyle2google_java_benchmark.xlsx'
    gen_benchmark(file_path)


    