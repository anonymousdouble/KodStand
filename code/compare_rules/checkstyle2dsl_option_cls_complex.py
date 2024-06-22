import os
import json
import re
import shutil
import sys
from gpt_agent_028 import GPTAgent
from dsl import dsl

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
from checkstyle2dsl import get_checkstyle_rules_from_file
import util

option_cls_examples = """For Example, respond like: 
Final RuleSet Representation:
Basic Rule:
Mandatory: Order of [import groups] is {{customImportOrderRules}}
And
Mandatory: {{customImportOrderRules}} not have [an import group] -> [the import group] at end of [import groups]

Option Rule:
separateLineBetweenGroups option:
true: Mandatory: [empty line] between [import groups]
false: Optional: [empty line] not between [import groups]

sortImportsInGroupAlphabetically option:
true: Mandatory: Order of [imports] of [import group] is [ASCII sort order]
false: Optional: Order of [imports] of [import group] is not [ASCII sort order]

Options that are data specifications:
{{customImportOrderRules}}: String[]; {STATIC, SAME_PACKAGE(n), SPECIAL_IMPORTS, STANDARD_JAVA_PACKAGE, THIRD_PARTY_PACKAGE}; {};
{{thirdPartyPackageRegExp}}: Pattern; RegExp; “.*”;

Final RuleSet Representation:
[block] of {{tokens}} have [Brace]

Option Rule:
allowEmptyLoopBody option:
false: Mandatory: [body] of [loop statement] is not [Null]
true: Optional: [body] of [loop statement] is [Null]

allowSingleLineStatement option:
false: Mandatory: Number of [statement] of [body] of {{tokens}} is 1 —> [body] of {{tokens}} have [Brace]
true: Optional: Number of [statement] of [body] of [{{tokens}} is 1 —> [body] of {{tokens}} not have [Brace]

Options that are data specifications:
tokens: String[]; {LITERAL_DO, LITERAL_ELSE, LITERAL_FOR, LITERAL_IF, LITERAL_WHILE, LITERAL_CASE, LITERAL_DEFAULT,LAMBDA}; {LITERAL_DO, LITERAL_ELSE, LITERAL_FOR, LITERAL_IF, LITERAL_WHILE};
"""


def preprocess_promt(
    rule: str,
    dsl_syntax: str,
    style="CheckStyle Rule",
    grammar="Grammar",
    example="",
    options="Answer about Options are data specifications or not",
    options_answer=None,
):

    prompt = """Analyze the following {{Style}} and DSL representation parsed using given grammar, please delete unexisted OptionName. 

1. Analyze whether each sentence of descriptions of {{Style}} is a rule or not. If it is a rule, parsing it as a rule using the given {{grammar}}. If terms of rule refer to options that are data specifications, pay attention to using {{OptionName}} to represent the term. Otherwise, skip it. If the rule is subjective, skip it too. 
2. For each option that is not data specification, for each value, please parse it as a rule using giving {{grammar}}. If terms of rule are options refer to are data specifications, pay attention to using {{OptionName}} to represent the term.
3. For each option that is data specification, please provide the option type, value range, default value. 
4. When parsing a rule using the given {{grammar}}, pay attention to map to suitable formal Java term and select appropriate real operator characters. 

{{Style}}:
{{Description}}

{{Options}}
{{Options_Answer}}

{{grammar}}:
{{Syntax}}

{{Example}}

Response Format:
If there is no option, you only give basic rule
Final RuleSet Representation:
Basic Rule:
...

Otherwise,
Final RuleSet Representation:
Basic Rule:
...

Option Rule:
...

Options that are data specifications:
...
"""
    prompt = prompt.replace("{{Example}}", example)
    prompt = prompt.replace("{{Style}}", style)
    prompt = prompt.replace("{{Syntax}}", dsl_syntax)
    prompt = prompt.replace("{{Description}}", rule)
    prompt = prompt.replace("{{Options_Answer}}", options_answer)
    prompt = prompt.replace("{{Options}}", options)
    prompt = prompt.replace("{{grammar}}", grammar)
    return prompt


if __name__ == "__main__":
    gpt_answer_dir = "data/dsl_output/checkstyle_option_cls_complex"
    file_path = "data/rule/checkstyle/java/url_name_desc_opt.json"
    rule_list = get_checkstyle_rules_from_file(file_path)

    pargs = {
        "dsl_syntax": dsl,
        "style": "CheckStyle Rule",
        "grammar": "Grammar",
        "example": option_cls_examples,
        "options": "Answer about Options are data specifications or not",
        "options_answer": "None",
    }
    agent = GPTAgent()
    agent.gen_dsl(
        rule_list = rule_list,
        pargs=pargs,
        prompt_processor=preprocess_promt,
        model="gpt-4o",
        output_dir=gpt_answer_dir,
    )
