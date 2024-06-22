import os,json
import re
import shutil

import util

from openai import OpenAI
from retry import retry
from code.compare_rules.gpt_agent import GPTAgent

def preprocess_promt(rule: str, DSL_Syntax: str, style="Google Java Style Guide",grammar="Grammar",example=""):

    prompt = '''Analyze the following {{Style}}, please parse the style using the given {{grammar}} to make its semantics clear and correct.

1. Analyze whether each sentence is a rule and then classify it as mandatory or optional. If the rule is subjective, do not classify it as a rule.
2. When parsing the rule using a given {{grammar}}, pay attention to map to suitable formal Java term and select appropriate real operator characters. 

{{Style}}:
{{Description}}

{{grammar}}:
{{Syntax}}

{{Example}}'''
    # '''

    prompt = prompt.replace("{{Example}}", example)
    prompt = prompt.replace("{{Style}}", style)
    prompt = prompt.replace("{{Syntax}}", DSL_Syntax)
    prompt = prompt.replace("{{Description}}", rule)
    prompt = prompt.replace("{{grammar}}", grammar)

    return prompt


def get_all_gpt_res_for_java_checkstyle(rule_list,dsl, examples=None,style="Google Java Style Guide",model="gpt-4o"):
    '''
    1. parse each rule of style guide as a string
    2. parse all rules of style tool as a string
    3. get and save GPT results
    '''

    agent = GPTAgent()
    data_dir = util.data_root + "rule/google/"

    for ind, rule_description in enumerate(rule_list[:]):
        prompt= preprocess_promt(rule=rule_description,example=examples,DSL_Syntax=dsl, style=style)
        answer = agent.get_response(prompt, model=model)
        util.save_json(gpt_answer_dir, str(ind), {ind: answer})

        # break

if __name__ == "__main__":
    gpt_answer_dir=util.data_root + "gpt_dsl_answer/GoogleJavaStyle_Simple_DSL_syntax_SplitSentence_example4/"
    all_rules = util.load_csv(util.data_root + "GoogleJavaStyle/javastyle_myanalyze.csv")
    rule_list = ["\n".join([rule_name, description]) for ind, (url, rule_name, description,*remain) in enumerate(all_rules) if ind>0]


    dsl = '''RuleSet ::= Rule1 [And|Or|; Rule2]* # And means should satisfy Rule1 and Rule2. Or means can satisfy Rule1 or Rule2. ; means Rule1,Rule2 belongs to diffent groups
Rule ::= {{'Optional'| 'Mandatory'}} [ ['Order' of | 'Number' of] TermList [Operator TermList]* | Rule1 '->' Rule2] [ExceptionRule] #'Order' of  means order rule, 'Number' of means numberConstraint, Rule1 '->' Rule2 means if Rule1 then Rule2
ExceptionRule ::= 'Except ' TermList | Rule # means rules not applied to TermList | Rule
Operator = 'is'| 'is not' | '>=' | '<=' | '=' | '!=' | 'for' | 'not for' | 'before' | 'not before' | 'after' | 'not after' | 'between' | 'not between' | 'have' | 'not have' | 'Add' | 'Sub' | 'Mult' | MatMult | 'Div' | 'Mod' | 'Pow' | 'LShift' | 'RShift' | 'BitOr' | 'BitXor' | 'BitAnd' | 'FloorDiv'
TermList ::= Term [, Term]*
Modifier ::= 'some' | 'each' | 'all' | 'except' | 'first' | 'last' | ...
Term :: = JavaTerm | Modifier* Term | Term of Term
JavaTerm means the formal expression using such format [XXX] "XXX" represent a JavaTerm
'''

    examples='''For Example, Analyze the following {{Style}}, please parse the style using the given {{grammar}}. 

{{Style}}:
4.1.1 Use of optional braces
Braces are used with `if` , `else` , `for` , `do` and `while` statements, even when the body is empty or contains only a single statement.
Other optional braces, such as those in a lambda expression, remain optional.


Final RuleSet Representation:
Mandatory: [IfStatement], [ElseStatement], [ForStatement], [DoStatement], [WhileStatement] have [Brace]
Or
Mandatory: [body] of [IfStatement], [ElseStatement], [ForStatement], [DoStatement], [WhileStatement] is [Null] 
—> [IfStatement], [ElseStatement], [ForStatement], [DoStatement], [WhileStatement] have [Brace] 
Or
Mandatory: [Number] of [body] of [IfStatement], [ElseStatement], [ForStatement], [DoStatement], [WhileStatement] = 1
—> [IfStatement], [ElseStatement], [ForStatement], [DoStatement], [WhileStatement] have [Brace]
'''



    get_all_gpt_res_for_java_checkstyle(rule_list,dsl,  examples=examples,style="Google Java Style Guide",model="gpt-4o")
