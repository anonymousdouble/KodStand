import os
import json
import re
import shutil

import util

from openai import OpenAI
from retry import retry
from gpt_wrapper_new import GPTAgent


def preprocess_promt(
    rule: str,
    DSL_Syntax: str,
    style="Google Java Style Guide",
    grammar="Grammar",
    example="",
):
    prompt = """Analyze the following {{Style}}, please parse the style using the given {{grammar}}. 

1. Analyze whether each sentence constitutes a mandatory rule. If the rule is optional or subjective, do not classify it as a rule.
2. If the sentence represents a mandatory rule, explain its meaning using the provided {{grammar}}. If the sentence is complex and cannot be expressed using a single rule, you can split it into multiple simple sentences using the "And" or "Or" connectors. And then determine the appropriate ruletypes and select suitable JavaTerm and Operators from the given {{grammar}} to express the rule, and finally connect these rules, ensuring adherence to the specified {{grammar}}.
3. If the rule cannot be described using the given {{grammar}}, refine and expand the {{grammar}} to accommodate it.

{{Style}}:
{{Description}}

{{grammar}}:
{{Syntax}}

{{Example}}"""

    prompt = prompt.replace("{{Example}}", example)
    prompt = prompt.replace("{{Style}}", style)
    prompt = prompt.replace("{{Syntax}}", DSL_Syntax)
    prompt = prompt.replace("{{Description}}", rule)
    prompt = prompt.replace("{{grammar}}", grammar)

    return prompt


def get_all_gpt_res_for_java_checkstyle(
    rule_list, dsl, examples=None, style="Google Java Style Guide", model="gpt-4o"
):
    """
    1. parse each rule of style guide as a string
    2. parse all rules of style tool as a string
    3. get and save GPT results
    """

    agent = GPTAgent()

    """
    GPT results_rule_name_descr_options
    GPT results_rule_name_descr	
    GPT results_html
    """

    for ind, rule_description in enumerate(rule_list[:]):
        print(">>>>>>rule: ", rule_description)

        prompt = preprocess_promt(
            rule=rule_description, example=examples, DSL_Syntax=dsl, style=style
        )
        print(">>>>>prompt: ", prompt)
        answer = agent.get_response(prompt, model=model)
        print(">>>>>>answer: ", ind, answer)
        util.save_json(util.data_root + gpt_answer_dir, str(ind), {ind: answer})


if __name__ == "__main__":
    data_root = "data/"
    gpt_answer_dir = (
        "data/gpt_dsl_answer/GoogleJavaStyle_DSL_syntax differentTypeRule SeparatorType SplitSentence3/"
    )
    all_rules = util.load_csv(
        data_root + "GoogleJavaStyle/javastyle_myanalyze.csv"
    )
    rule_list = [
        "\n".join([rule_name, description])
        for ind, (url, rule_name, description, *remain) in enumerate(all_rules)
        if ind > 0
    ]
    dsl = """RuleSet ::= Rule [And|OR Rule]*
Rule ::= [Term* | Number | Name | Order] operator Term* [operator Term*]* 
Modifier ::= some | each | all | except | first | last | ...
Operator ::= —> | of | have | not have | is | is not | start | end | before | after | between| > |  < | = | != | ...
Term :: = JavaTerm | Modifier* Term* 
(Note JavaTerm is formal term description in Java)
"""
    dsl = """RuleSet ::= Rule [And|Or Rule]*
Rule ::= OrderRule | NumberRule | ValueRule | SequenceRule | InclusionRule | ConditionRule
OrderRule ::= 'Order ' valueOperator TermList
NumberRule ::= 'Number of' TermList numberOperator TermList
SequenceRule ::= TermList positionOperator TermList
ValueRule ::= TermList valueOperator TermList
InclusionRule ::= TermList inclusionOperator TermList
ConditionRule ::= Rule '—>' Rule  # means if Rule then Rule
numberOperator ::=  '>=' | '<=' | '=' | '!='
positionOperator ::=  'before' | 'after' | 'between' | 'not before' | 'not after' | 'not between'
inclusionOperator ::=  'have' | 'not have'
valueOperator ::=  'is' | 'is not'
TermList ::=  Term [, Term]*
Modifier ::= 'some' | 'each' | 'all' | 'except' | 'first' | 'last' | ...
Term :: = JavaTerm | Modifier* Term | Term of Term
JavaTerm :: = formal term description in Java
    """
    dsl = """RuleSet ::= Rule [And|Or Rule]*
Rule ::= OrderRule | NumberRule | ValueRule | SequenceRule | InclusionRule | ConditionRule | SeparatorRule
OrderRule ::= 'Order ' ['is' | 'is not'] TermList # means order should be/ should not be ordered TermList
NumberRule ::= 'Number of' TermList numberOperator TermList
SequenceRule ::= TermList1 positionOperator TermList2  # means how terms of TermList1 are positioned in relation to the terms in TermList2
SeparatorRule ::= TermList1 'between' TermList2 # means TermList2 separated by TermList1
ValueRule ::= TermList valueOperator TermList
InclusionRule ::= TermList inclusionOperator TermList
ConditionRule ::= Rule '—>' Rule # means if Rule then Rule
numberOperator ::= '>=' | '<=' | '=' | '!='
positionOperator ::= 'before' | 'after' | 'between' | 'not before' | 'not after' | 'not between'
inclusionOperator ::= 'have' | 'not have'
valueOperator ::= 'is' | 'is not'
TermList ::= Term [, Term]*
Modifier ::= 'some' | 'each' | 'all' | 'except' | 'first' | 'last' | ...
Term :: = JavaTerm | Modifier* Term | Term of Term
"""
    examples = """Analyze the following {{Style}}, please parse the style using the given {{grammar}}. 

{{Style}}:
4.1.1 Use of optional braces
Braces are used with `if` , `else` , `for` , `do` and `while` statements, even when the body is empty or contains only a single statement.
Other optional braces, such as those in a lambda expression, remain optional.


Final RuleSet Representation:
[IfStatement], [ElseStatement], [ForStatement], [DoStatement], [WhileStatement] have [Brace]
Or
[body] of [IfStatement], [ElseStatement], [ForStatement], [DoStatement], [WhileStatement] is [Null] 
—> [IfStatement], [ElseStatement], [ForStatement], [DoStatement], [WhileStatement] have [Brace] 
Or
[Number] of [body] of [IfStatement], [ElseStatement], [ForStatement], [DoStatement], [WhileStatement] = 1
—> [IfStatement], [ElseStatement], [ForStatement], [DoStatement], [WhileStatement] have [Brace]
"""

    get_all_gpt_res_for_java_checkstyle(
        rule_list,
        dsl,
        examples=examples,
        style="Google Java Style Guide",
        model="gpt-4o",
    )
