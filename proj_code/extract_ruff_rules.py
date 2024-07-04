'''
https://docs.astral.sh/ruff/rules/#rules
ruff-main/crates/ruff_linter/src/rules

msgs: Rule source
https://docs.astral.sh/ruff/rules/#pyflakes-f
ruff-main/crates/ruff_linter/src/rules/pyflakes/rules/unused_import.rs

code examples ---- test cases: Tests source
https://docs.astral.sh/ruff/rules/unused-import/
ruff-main/crates/ruff_linter/resources/test/fixtures/pyflakes/F401_0.py

'''
import os.path

'''
1. https://docs.astral.sh/ruff/rules/
从这个list中爬取 每个rule, 编号, name, msg, 

2. 
'''
import requests
import util
from urllib import request
import sys

sys.setrecursionlimit(10000)
def parse_ruff_rule(cols):
    '''
        ✔️     The rule is stable.
        🧪     The rule is unstable and is in "preview".
        ⚠️     The rule has been deprecated and will be removed in a future release.
        ❌     The rule has been removed only the documentation is available.
        🛠️     The rule is automatically fixable by the --fix command-line option.

        Rule is stable
        Rule is in preview
        Rule has been deprecated
        Rule has been removed
        Automatic fix not available
        Automatic fix available
        '''
    ident, name, msg, lengend = cols
    # print("code, name, msg, lengend: ", ident, "\n", name, "\n", msg, "\n", lengend)

    ident = ident.text.strip()
    rule_url = name.find('a')['href']
    name = name.text.strip()
    msg = msg.contents
    msg = "".join([str(e) for e in msg])
    # print("msg: ","".join(msg))
    # print("msg: ", msg)
    # parsedContent = BeautifulSoup(str(msg), 'lxml')
    # print("parsedContent: ", parsedContent, parsedContent.find_all('td'))
    # a = parsedContent.find("body")
    # print("a: ", a.contents)

    span_list=[span['title'] for span in lengend.find_all('span')]
    print("len(span): ",rule_url,len(span_list))#,lengend.find_all('span')
    state_str, fix_str =span_list[-2:] if len(span_list)>2 else span_list
    # if state_str == ""
    # for ind, span in  enumerate(lengend.find_all('span')):
    #     # span.title
    #     print("span: ",ind, span,span['title'],span.text )
    #     pass
    # print("code, name, msg, lengend: ", ident, "\n", name, "\n", msg, "\n", lengend)
    # print("rule_url: ",rule_url)
    # state = if lengend.find()
    return rule_url, ident, name, msg, state_str, fix_str

def save_each_rule_ruff_html(ruff_html_dir,file_name,rule_url):
    # if not os.path.exists(ruff_data_dir + "each_rule_html/" + file_name + ".html"):
        try:
            content = requests.get(rule_url)
            content = content.text
            # response = f.opener.open(f).read()  # f.read()
            # print("content: ",content)
            # print("html: ",issue_url)
            # parse the HTML
            soup = BeautifulSoup(content, "lxml")
            # print("soup: ",soup)
            util.save_file(ruff_html_dir, file_name, content, ".html")
        except:
            print("cannot save ",rule_url)
        # url = None, iden = None, name = None, description = None, msg = None, options = None, fix = None, state = "Stable", type = None, suggestion = None):

#https://docs.astral.sh/ruff/rules/
def parse_ruff_html(ruff_data_dir,file_path):

        with open(file_path, "r", encoding='utf-8', errors='ignore') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'lxml')  # 'html.parser')

            rule_body_list = soup.find_all('div', {'class': "md-typeset__table"})  # md-typeset__table
            print("rule_body_list: ", len(rule_body_list))
            for ind, rules in enumerate(rule_body_list):
                table = rules.find_all('table')
                # print("table: ",table)
                table_body = table[0].find('tbody')

                rows = table_body.find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    print("cols: ", len(cols))
                    rule_url, ident, name, msg, state_str, fix_str = parse_ruff_rule(cols)
                    cs = CodeStandard(rule_url, ident, name, msg, state_str, fix_str)
                    all_rules.append(cs)
                    # f = request.Request(rule_url)
                    file_name = rule_url.split("/")[-2].strip()
                    if not os.path.exists(ruff_data_dir + "each_rule_html/" + file_name + ".html"):
                        save_each_rule_ruff_html(ruff_data_dir + "each_rule_html/", file_name, rule_url)

                    print("parsed info: ", rule_url, ident, name, msg, state_str, fix_str)
                    # code, name, msg, lengend = cols
                    # CodeStandard ()
                    # for code, name, msg in cols:
                    # cols = [ele.text.strip() for ele in cols]
                    # break
                    # data.append([ele for ele in cols if ele])
                # break

            util.save_pkl(ruff_data_dir, "ruff_rules", all_rules)

def get_different_state(all_rules):
    '''
                ✔️     The rule is stable.
                🧪     The rule is unstable and is in "preview".
                ⚠️     The rule has been deprecated and will be removed in a future release.
                ❌     The rule has been removed only the documentation is available.
                🛠️     The rule is automatically fixable by the --fix command-line option.

                Rule is stable
                Rule is in preview
                Rule has been deprecated
                Rule has been removed
                Automatic fix not available
                Automatic fix available
                '''
    stable_fix_rules, stable_no_fix_rules, preview_fix_rules, preview_no_fix_rules, \
    deprecated_fix_rules, deprecated_no_fix_rules, removed_fix_rules, removed_no_fix_rules = [[] for i in range(8)]
    a = [stable_fix_rules, stable_no_fix_rules, preview_fix_rules, preview_no_fix_rules, \
         deprecated_fix_rules, deprecated_no_fix_rules, removed_fix_rules, removed_no_fix_rules]
    for each_rule in all_rules:
        each_rule: CodeStandard
        # =CodeStandard(each_rule.value)
        if each_rule.state == "Rule is stable":
            if each_rule.fix == "Automatic fix not available":
                stable_no_fix_rules.append(each_rule)
            else:
                stable_fix_rules.append(each_rule)
        elif each_rule.state == "Rule is in preview":
            if each_rule.fix == "Automatic fix not available":
                preview_no_fix_rules.append(each_rule)
            else:
                preview_fix_rules.append(each_rule)
        elif each_rule.state == "Rule has been deprecated":
            if each_rule.fix == "Automatic fix not available":
                deprecated_no_fix_rules.append(each_rule)
            else:
                deprecated_fix_rules.append(each_rule)
        elif each_rule.state == "Rule has been removed":
            if each_rule.fix == "Automatic fix not available":
                removed_no_fix_rules.append(each_rule)
            else:
                removed_fix_rules.append(each_rule)
    for e in a:
        print("len:", len(e))
    print("sum: ", sum([len(e) for e in a]), len(all_rules))
    return a


def parse_code_example(contents):
    examples = []
    flag = 1
    for e in contents:
        # print(">>>>>example: ",e)
        if hasattr(e,'name') and e.name =="p" and e.text == "Use instead:":
            flag = 2
        elif hasattr(e,'name') and e.name =="p" and e.text:
            flag = 3
        # print(">>>>>has pre: ", hasattr(e, 'find_all') and e.find_all('pre'))
        code_list =  e.find_all('pre') if hasattr(e, 'find_all') else []
        # print(">>>>>code_list: ", code_list,examples)
        if code_list:
            if flag == 1:
                examples.append([code_list[0].text])
            elif flag == 2:
                examples[-1].append(code_list[0].text)
        if flag == 3:
            if len(examples)>0:
                examples[-1].append(e.text)
            else:
                examples.append([None,None,e.text])
    examples=[e[:2]+ ["".join(e[2:])] if len(e)>2 else e for e in examples ]
    return examples
def parse_descrip_suggestion_example_options(rule_filepath):
    # rule_filepath = ruff_data_dir + "each_rule_html/" + file_name + ".html"
    with open(rule_filepath, "r", encoding='utf-8', errors='ignore') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'lxml')  # 'html.parser')
        # soup.find_all()"md-content"
        # rule_body_list = soup.find_all('div', {'class': "md-content"})  # md-typeset__table
        rule_body_list = soup.find_all('article', {'class': "md-content__inner md-typeset"})  # md-typeset__table
        article = rule_body_list[0]
        # print("len: ", len(rule_body_list))
        # rule.description = soup.text

        # print(soup)
        # print(soup.contents)
        code_examples = []
        options = []
        description = []  # soup.text
        suggestion = []
        other = []
        flag = None
        for c in list(article.contents):
            # print(">>>>>: ",c)
            if hasattr(c,'name')  and c.name == 'h2' and c["id"] == "what-it-does":
                flag = 1
                # description.append(c.text)
            elif hasattr(c,'name')  and c.name == 'h2' and c["id"] == "why-is-this-bad":
                flag = 2
            elif hasattr(c,'name')  and c.name == 'h2' and c["id"] == "example":
                flag = 3
            elif hasattr(c,'name')  and c.name == 'h2' and c["id"] == "options":
                # print("flag is 4")
                flag = 4
            elif hasattr(c,'name')  and c.name == 'h2' and c["id"] == "references":
                flag = 5

            if flag == 1:
                description.append(c.text)
            elif flag == 2:
                suggestion.append(c.text)
            elif flag == 3:
                code_examples.append(c)
            elif flag == 4:
                def parse_option(c,option_html_dir,file_name):
                    options = []
                    if hasattr(c, 'name') and c.name == "ul":
                        # print(">>>>>>>>> It has li list ")
                        li_list = c.find_all('li')
                        for li in li_list:
                            href = li.find_all('a')[0]['href']
                            if href.startswith("../../"):
                                href = "https://docs.astral.sh/ruff/" + href[len("../../"):]
                            if not os.path.exists(option_html_dir + file_name + ".html"):
                                save_each_rule_ruff_html(option_html_dir, file_name, href)
                            code_option = CodeStandardOption(href, li.text.strip())
                            options.append(code_option)
                    return options

                option_html_dir = ruff_data_dir + "options/"
                options.extend(parse_option(c,option_html_dir,file_name))
                '''
                # print(">>>>>>c: ", c)
                if hasattr(c, 'name') and c.name == "ul":
                    # print(">>>>>>>>> It has li list ")
                    li_list = c.find_all('li')
                    for li in li_list:
                        href = li.find_all('a')[0]['href']
                        if href.startswith("../../"):
                            href = "https://docs.astral.sh/ruff/" + href[len("../../"):]
                        option_html_dir=ruff_data_dir + "options/"
                        if not os.path.exists(option_html_dir + file_name + ".html"):
                            save_each_rule_ruff_html(option_html_dir, file_name, href)

                        # "https://docs.astral.sh/ruff/"+li.find_all('a')[0]['href']
                        code_option = CodeStandardOption(href, li.text.strip())
                        # pass
                    # https: // docs.astral.sh / ruff / settings /  # lint_ignore-init-module-imports
                    options.append(code_option)
                '''
            else:
                other.append(c)

            # print(">>>>>>extract", c.extract())

        # description_str = "".join([e for e in description if "What it does" not in e])
        # suggestion_str = "".join([e for e in suggestion if "Why is this bad" not in e])
        description_str = "".join(description)
        suggestion_str = "".join(suggestion)
        # rule.options = options
        # rule.codeExamples = code_examples
        code_examples = parse_code_example(code_examples)
        print(description_str, "\n-----\n", suggestion_str, "\n-----\n", code_examples, "\n-----\n",
              [(op.name, op.url) for op in options],"\n-----other:\n", other )
        return description_str,suggestion_str,code_examples,options,other
from bs4 import BeautifulSoup
from code_standard import CodeStandard,CodeStandardOption,RuffCodeStandard
if __name__ == '__main__':
    all_rules=[]
    ruff_data_dir=util.data_root +"ruff/"
    file_path =ruff_data_dir + "Rules-Ruff.html"

    # 1. initialize msg, url, name, state, fix
    if not os.path.exists(ruff_data_dir + "ruff_rules.pkl"):
        parse_ruff_html(ruff_data_dir, file_path)

    all_rules = util.load_pkl(ruff_data_dir,"ruff_rules")

    # 2. initialize descrip, suggestion, example, options
    # '''
    if not os.path.exists(ruff_data_dir + "ruff_rules_descrp_sugg_examp_option.pkl"):
        all_rules_add_descrip_suggestion_example_options = []
        for rule_1 in all_rules:
            rule_1:CodeStandard
            rule = RuffCodeStandard()
            rule.__dict__.update(rule_1.__dict__)
            rule.other = None
            # rule = type(RuffCodeStandard)(rule)
            rule:RuffCodeStandard
            file_name,state,fix= rule.name,rule.state, rule.fix
            print(">>>>link: ",rule.url)
            # if file_name!="unused-import":
            #     continue

            # print("state: ",rule.fix)
            rule_filepath = ruff_data_dir + "each_rule_html/" + file_name + ".html"
            rule.content_file_path = rule_filepath
            rule.description, rule.suggestion, rule.codeExamples, rule.options, rule.other = \
                parse_descrip_suggestion_example_options(rule_filepath)

            all_rules_add_descrip_suggestion_example_options.append(rule)
            # rule.preprocess_description()
            # rule.preprocess_suggestion()
            # break
        util.save_pkl(ruff_data_dir, "ruff_rules_descrp_sugg_examp_option",all_rules_add_descrip_suggestion_example_options)
    # '''

    # 3. write to csv
    csv_result_list = []
    all_rules_add_descrip_suggestion_example_options = util.load_pkl(
        ruff_data_dir,"ruff_rules_descrp_sugg_examp_option")
    column_list = ['url','iden','name', 'msg','state','fix', 'description', 'suggestion','codeExamples', 'options', 'other' ]
    # csv_result_list.append(column_list)
    for rule in all_rules_add_descrip_suggestion_example_options:
        # print("rule: ",rule.__dict__)
        # RuffCodeStandard
        # rule = RuffCodeStandard()
        # rule.__dict__.update(rule_1.__dict__)
        dict_rule = rule.__dict__
        print("rule: ",rule.__dict__)
        one_row = []
        for key in column_list:
            if key =="other":
                one_row.append("".join([str(e) for e in dict_rule[key]]))
            elif key == "codeExamples":
                one_row.append(rule.parse_code_examples())
            elif key == "options":
                one_row.append(rule.parse_options())
            else:
                one_row.append(dict_rule[key])
        csv_result_list.append(one_row)
    #     break
    # print(">>csv_result_list: ",csv_result_list)

    util.save_csv(ruff_data_dir+"ruff_rules_descrp_sugg_examp_option.csv",csv_result_list,column_list)



    # stable_fix_rules, stable_no_fix_rules, preview_fix_rules, preview_no_fix_rules, \
    # deprecated_fix_rules, deprecated_no_fix_rules, removed_fix_rules, removed_no_fix_rules = get_different_state(all_rules)






        # print(each_rule.iden,each_rule.name,each_rule.state)
        # break



    # with open(file_path, "r", encoding='utf-8', errors='ignore') as f:
    #     content = f.read()
    #     soup = BeautifulSoup(content, 'lxml')  # 'html.parser')
    #
    #     rule_body_list = soup.find_all('div', {'class': "md-typeset__table"}) #md-typeset__table
    #     print("rule_body_list: ",len(rule_body_list))
    #     for ind, rules in enumerate(rule_body_list):
    #         table = rules.find_all('table')
    #         # print("table: ",table)
    #         table_body = table[0].find('tbody')
    #
    #         rows = table_body.find_all('tr')
    #         for row in rows:
    #             cols = row.find_all('td')
    #             print("cols: ",len(cols))
    #             rule_url,ident, name, msg,state_str,fix_str = parse_ruff_rule(cols)
    #             cs = CodeStandard(rule_url,ident,name,msg,state_str,fix_str)
    #             all_rules.append(cs)
    #             # f = request.Request(rule_url)
    #             file_name = rule_url.split("/")[-2].strip()
    #             save_each_ruff_html(ruff_data_dir, file_name, rule_url)
    #
    #             print("parsed info: ",rule_url,ident, name, msg,state_str,fix_str)
    #             # code, name, msg, lengend = cols
    #             # CodeStandard ()
    #             # for code, name, msg in cols:
    #             # cols = [ele.text.strip() for ele in cols]
    #             # break
    #             # data.append([ele for ele in cols if ele])
    #         # break
    #
    #     util.save_pkl(ruff_data_dir,"ruff_rules",all_rules)
    # pass