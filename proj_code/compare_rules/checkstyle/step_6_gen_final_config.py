import copy
import os
import sys

from gpt_agent_028 import GPTAgent
from proj_code.compare_rules.checkstyle.dsl import dsl
from step_5_mapping import get_all_google_dsl
from step_1_a_checkstyle_check_valid_options import get_checkstyle_rules_from_file

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
import util

examples = """For example, given ### Explanation

To determine if each rule in the RuleSet of the Google Java Style Guide has a semantically equivalent rule in Checkstyle, we need to follow these steps:

1. **Extract each rule in the RuleSet of the Google Java Style Guide.**
2. **Extract basic rules and option rules in Checkstyle.**
3. **Determine possible matching rules from basic rules and option rules in Checkstyle.**
4. **Check if the type of matching rule in Checkstyle is the same (both Optional/Mandatory).**
5. **Check if the objects that the rule in the RuleSet of the Google Java Style Guide checks are the same as the objects that the matching rule in Checkstyle checks.**
6. **Analyze whether the semantics of the rule in the RuleSet of the Google Java Style Guide are the same as the semantics of the matching rule in Checkstyle.**
7. **If the objects of the matching rule in Checkstyle correspond to option names from Options that are data specifications, extract the corresponding option name and set values from the value range of options that have the same semantics with objects of the RuleSet of the Google Java Style Guide.**

### RuleSet of Google Java Style Guide

1. **Kernighan and Ritchie Style for Nonempty Blocks and Block-like Constructs:**
   - **Mandatory:** Braces must follow the Kernighan and Ritchie style for nonempty blocks and block-like constructs.

2. **Line Break Rules:**
   - **Mandatory:** No line break before the opening brace of nonempty blocks and block-like constructs.
   - **Mandatory:** Line break after the opening brace of nonempty blocks and block-like constructs.
   - **Mandatory:** Line break before the closing brace of nonempty blocks and block-like constructs.
   - **Mandatory:** Line break after the closing brace of nonempty blocks and block-like constructs if the closing brace terminates a statement or the body of a method, constructor, or named class.

3. **Exception Rule:**
   - **Mandatory:** In places where a single statement ending with a semicolon is allowed, a block of statements can appear, and the opening brace of this block is preceded by a line break.

### Checkstyle Rules

1. **LeftCurly:**
   - **Basic Rule:** Mandatory: [block] of {{tokens}} have [Brace]
   - **Option Rule:**
     - `ignoreEnums` option:
       - `true`: Optional: [enum] not for [block] of {{tokens}}
     - `option` option:
       - `eol`: Mandatory: [Brace] at end of [line] of [block] of {{tokens}}
       - `nl`: Mandatory: [Brace] at begin of [line] of [block] of {{tokens}}
       - `alone`: Mandatory: [Brace] at begin of [line] of [block] of {{tokens}}
   - **Options that are data specifications:**
     - `{{tokens}}`: String[]; {ANNOTATION_DEF, CLASS_DEF, CTOR_DEF, ENUM_CONSTANT_DEF, ENUM_DEF, INTERFACE_DEF, LAMBDA, LITERAL_CASE, LITERAL_CATCH, LITERAL_DEFAULT, LITERAL_DO, LITERAL_ELSE, LITERAL_FINALLY, LITERAL_FOR, LITERAL_IF, LITERAL_SWITCH, LITERAL_SYNCHRONIZED, LITERAL_TRY, LITERAL_WHILE, METHOD_DEF, OBJBLOCK, STATIC_INIT, RECORD_DEF, COMPACT_CTOR_DEF}

2. **RightCurly:**
   - **Basic Rule:** Mandatory: [placement] of [right curly brace] of {{tokens}} is [correct]
   - **Option Rule:**
     - `option`:
       - `same`: Mandatory: [placement] of [right curly brace] of {{tokens}} is [same line]
       - `alone`: Mandatory: [placement] of [right curly brace] of {{tokens}} is [new line]
       - `alone_or_singleline`: Mandatory: [placement] of [right curly brace] of {{tokens}} is [new line] or [single line]
   - **Options that are data specifications:**
     - `{{tokens}}`: String[]; {LITERAL_TRY, LITERAL_CATCH, LITERAL_FINALLY, LITERAL_IF, LITERAL_ELSE, CLASS_DEF, METHOD_DEF, CTOR_DEF, LITERAL_FOR, LITERAL_WHILE, LITERAL_DO, STATIC_INIT, INSTANCE_INIT, ANNOTATION_DEF, ENUM_DEF, INTERFACE_DEF, RECORD_DEF, COMPACT_CTOR_DEF, LITERAL_SWITCH, LITERAL_CASE}

### Analysis and Matching

#### Rule 1: Kernighan and Ritchie Style for Nonempty Blocks and Block-like Constructs
- **Google Java Style Guide:** Mandatory: Braces must follow the Kernighan and Ritchie style for nonempty blocks and block-like constructs.
- **Checkstyle:**
  - **RuleName:** LeftCurly
  - **Option Rule:** `option: eol`
  - **Option that is data specification:**
    - `{{tokens}}`: Set corresponding value based on datatype, value range, and default value.

**Answer:** Yes
**Configuration:**
```plaintext
RuleName: LeftCurly
Option Rule: option, eol
Option that is data specification:
{{tokens}}: {CLASS_DEF, METHOD_DEF, CTOR_DEF, LITERAL_FOR, LITERAL_WHILE, LITERAL_DO, STATIC_INIT, INSTANCE_INIT, ANNOTATION_DEF, ENUM_DEF, INTERFACE_DEF, RECORD_DEF, COMPACT_CTOR_DEF, LITERAL_SWITCH, LITERAL_CASE}
```

#### Rule 2: No line break before the opening brace of nonempty blocks and block-like constructs
- **Google Java Style Guide:** Mandatory: No line break before the opening brace of nonempty blocks and block-like constructs.
- **Checkstyle:**
  - **RuleName:** LeftCurly
  - **Option Rule:** `option: eol`
  - **Option that is data specification:**
    - `{{tokens}}`: Set corresponding value based on datatype, value range, and default value.

**Answer:** Yes
**Configuration:**
```plaintext
RuleName: LeftCurly
Option Rule: option, eol
Option that is data specification:
{{tokens}}: {CLASS_DEF, METHOD_DEF, CTOR_DEF, LITERAL_FOR, LITERAL_WHILE, LITERAL_DO, STATIC_INIT, INSTANCE_INIT, ANNOTATION_DEF, ENUM_DEF, INTERFACE_DEF, RECORD_DEF, COMPACT_CTOR_DEF, LITERAL_SWITCH, LITERAL_CASE}
```

#### Rule 3: Line break after the opening brace of nonempty blocks and block-like constructs
- **Google Java Style Guide:** Mandatory: Line break after the opening brace of nonempty blocks and block-like constructs.
- **Checkstyle:**
  - **RuleName:** LeftCurly
  - **Option Rule:** `option: nl`
  - **Option that is data specification:**
    - `{{tokens}}`: Set corresponding value based on datatype, value range, and default value.

**Answer:** Yes
**Configuration:**
```plaintext
RuleName: LeftCurly
Option Rule: option, nl
Option that is data specification:
{{tokens}}: {CLASS_DEF, METHOD_DEF, CTOR_DEF, LITERAL_FOR, LITERAL_WHILE, LITERAL_DO, STATIC_INIT, INSTANCE_INIT, ANNOTATION_DEF, ENUM_DEF, INTERFACE_DEF, RECORD_DEF, COMPACT_CTOR_DEF, LITERAL_SWITCH, LITERAL_CASE}
```

#### Rule 4: Line break before the closing brace of nonempty blocks and block-like constructs
- **Google Java Style Guide:** Mandatory: Line break before the closing brace of nonempty blocks and block-like constructs.
- **Checkstyle:**
  - **RuleName:** RightCurly
  - **Option Rule:** `option: alone`
  - **Option that is data specification:**
    - `{{tokens}}`: Set corresponding value based on datatype, value range, and default value.

**Answer:** Yes
**Configuration:**
```plaintext
RuleName: RightCurly
Option Rule: option, alone
Option that is data specification:
{{tokens}}: {CLASS_DEF, METHOD_DEF, CTOR_DEF, LITERAL_FOR, LITERAL_WHILE, LITERAL_DO, STATIC_INIT, INSTANCE_INIT, ANNOTATION_DEF, ENUM_DEF, INTERFACE_DEF, RECORD_DEF, COMPACT_CTOR_DEF, LITERAL_SWITCH, LITERAL_CASE}
```

#### Rule 5: Line break after the closing brace of nonempty blocks and block-like constructs if the closing brace terminates a statement or the body of a method, constructor, or named class
- **Google Java Style Guide:** Mandatory: Line break after the closing brace of nonempty blocks and block-like constructs if the closing brace terminates a statement or the body of a method, constructor, or named class.
- **Checkstyle:**
  - **RuleName:** RightCurly
  - **Option Rule:** `option: alone_or_singleline`
  - **Option that is data specification:**
    - `{{tokens}}`: Set corresponding value based on datatype, value range, and default value.

**Answer:** Yes
**Configuration:**
```plaintext
RuleName: RightCurly
Option Rule: option, alone_or_singleline
Option that is data specification:
{{tokens}}: {CLASS_DEF, METHOD_DEF, CTOR_DEF, LITERAL_FOR, LITERAL_WHILE, LITERAL_DO, STATIC_INIT, INSTANCE_INIT, ANNOTATION_DEF, ENUM_DEF, INTERFACE_DEF, RECORD_DEF, COMPACT_CTOR_DEF, LITERAL_SWITCH, LITERAL_CASE}
```

#### Rule 6: Exception Rule: In places where a single statement ending with a semicolon is allowed, a block of statements can appear, and the opening brace of this block is preceded by a line break
- **Google Java Style Guide:** Mandatory: In places where a single statement ending with a semicolon is allowed, a block of statements can appear, and the opening brace of this block is preceded by a line break.
- **Checkstyle:** No direct equivalent rule found.

**Answer:** No
**Configuration:** None

### Summary

1. **Kernighan and Ritchie Style for Nonempty Blocks and Block-like Constructs:**
   - **Answer:** Yes
   - **Configuration:**
     ```plaintext
     RuleName: LeftCurly
     Option Rule: option, eol
     Option that is data specification:
     {{tokens}}: {CLASS_DEF, METHOD_DEF, CTOR_DEF, LITERAL_FOR, LITERAL_WHILE, LITERAL_DO, STATIC_INIT, INSTANCE_INIT, ANNOTATION_DEF, ENUM_DEF, INTERFACE_DEF, RECORD_DEF, COMPACT_CTOR_DEF, LITERAL_SWITCH, LITERAL_CASE}
     ```

2. **No line break before the opening brace of nonempty blocks and block-like constructs:**
   - **Answer:** Yes
   - **Configuration:**
     ```plaintext
     RuleName: LeftCurly
     Option Rule: option, eol
     Option that is data specification:
     {{tokens}}: {CLASS_DEF, METHOD_DEF, CTOR_DEF, LITERAL_FOR, LITERAL_WHILE, LITERAL_DO, STATIC_INIT, INSTANCE_INIT, ANNOTATION_DEF, ENUM_DEF, INTERFACE_DEF, RECORD_DEF, COMPACT_CTOR_DEF, LITERAL_SWITCH, LITERAL_CASE}
     ```

3. **Line break after the opening brace of nonempty blocks and block-like constructs:**
   - **Answer:** Yes
   - **Configuration:**
     ```plaintext
     RuleName: LeftCurly
     Option Rule: option, nl
     Option that is data specification:
     {{tokens}}: {CLASS_DEF, METHOD_DEF, CTOR_DEF, LITERAL_FOR, LITERAL_WHILE, LITERAL_DO, STATIC_INIT, INSTANCE_INIT, ANNOTATION_DEF, ENUM_DEF, INTERFACE_DEF, RECORD_DEF, COMPACT_CTOR_DEF, LITERAL_SWITCH, LITERAL_CASE}
     ```

4. **Line break before the closing brace of nonempty blocks and block-like constructs:**
   - **Answer:** Yes
   - **Configuration:**
     ```plaintext
     RuleName: RightCurly
     Option Rule: option, alone
     Option that is data specification:
     {{tokens}}: {CLASS_DEF, METHOD_DEF, CTOR_DEF, LITERAL_FOR, LITERAL_WHILE, LITERAL_DO, STATIC_INIT, INSTANCE_INIT, ANNOTATION_DEF, ENUM_DEF, INTERFACE_DEF, RECORD_DEF, COMPACT_CTOR_DEF, LITERAL_SWITCH, LITERAL_CASE}
     ```

5. **Line break after the closing brace of nonempty blocks and block-like constructs if the closing brace terminates a statement or the body of a method, constructor, or named class:**
   - **Answer:** Yes
   - **Configuration:**
     ```plaintext
     RuleName: RightCurly
     Option Rule: option, alone_or_singleline
     Option that is data specification:
     {{tokens}}: {CLASS_DEF, METHOD_DEF, CTOR_DEF, LITERAL_FOR, LITERAL_WHILE, LITERAL_DO, STATIC_INIT, INSTANCE_INIT, ANNOTATION_DEF, ENUM_DEF, INTERFACE_DEF, RECORD_DEF, COMPACT_CTOR_DEF, LITERAL_SWITCH, LITERAL_CASE}
     ```

6. **Exception Rule: In places where a single statement ending with a semicolon is allowed, a block of statements can appear, and the opening brace of this block is preceded by a line break:**
   - **Answer:** No
   - **Configuration:** None

You should respond like
<module name='LeftCurly'>
<property name='id' value='LeftCurlyKR'/># an identifier for the configuration
<property name='option' value='eol'/>  
<property name='tokens' value='CLASS_DEF, METHOD_DEF, CTOR_DEF, LITERAL_FOR, LITERAL_WHILE, LITERAL_DO, STATIC_INIT, INSTANCE_INIT, ANNOTATION_DEF, ENUM_DEF, INTERFACE_DEF, RECORD_DEF, COMPACT_CTOR_DEF, LITERAL_SWITCH, LITERAL_CASE'/>"
</module>

<module name='LeftCurly'>
<property name='id' value='LineBreakAfterLeftCurly'/># an identifier for the configuration
<property name='option' value='nl'/> 
<property name='tokens' value='CLASS_DEF, METHOD_DEF, CTOR_DEF, LITERAL_FOR, LITERAL_WHILE, LITERAL_DO, STATIC_INIT, INSTANCE_INIT, ANNOTATION_DEF, ENUM_DEF, INTERFACE_DEF, RECORD_DEF, COMPACT_CTOR_DEF, LITERAL_SWITCH, LITERAL_CASE'/>
</module>

<module name='RightCurly'>
<property name='id' value='LineBreakBeforeRightCurly'/># an identifier for the configuration
<property name='option' value='alone'/> 
<property name='tokens' value='CLASS_DEF, METHOD_DEF, CTOR_DEF, LITERAL_FOR, LITERAL_WHILE, LITERAL_DO, STATIC_INIT, INSTANCE_INIT, ANNOTATION_DEF, ENUM_DEF, INTERFACE_DEF, RECORD_DEF, COMPACT_CTOR_DEF, LITERAL_SWITCH, LITERAL_CASE'/>
</module>

<module name='RightCurly'>
<property name='id' value='LineBreakAfterRightCurly'/># an identifier for the configuration
<property name='option' value='alone_or_singleline'/> 
<property name='tokens' value='CLASS_DEF, METHOD_DEF, CTOR_DEF, LITERAL_FOR, LITERAL_WHILE, LITERAL_DO, STATIC_INIT, INSTANCE_INIT, ANNOTATION_DEF, ENUM_DEF, INTERFACE_DEF, RECORD_DEF, COMPACT_CTOR_DEF, LITERAL_SWITCH, LITERAL_CASE'/>
</module>
"""


def preprocess_promt(
    dsl_syntax: str,
    style="RuleSet of Google Java Style Guide",
    dsl_rule_set=None,
    tool="Checkstyle",
    tool_rule_set=None,
    grammar="Grammar",
    example="",
):
    prompt = """For each rule in the following {{Style}}, it gives analysis for whether there is corresponding configuration of {{tool}}. Extract and generate final configuration. If there are multiple same RuleName of final configuration, if configurations do not conflict, you should merge them into one. 

{{Style}}:
{{DSLruleset}}

{{tool}}:
{{toolruleset}}

Response Format: Response Format: Only give results, do not explain.
If configuration is null, give None. Otherwise, give final configuration. The configuration format should be xml format: 
<module name='RuleName1'>
<property name='id' value='id_value1'/># an identifier for the configuration
<property name='OptionName1' value='value1'/>  
... 
<property name='OptionName1' value='value2'/>"
</module>

<module name='RuleName2'>
<property name='id' value='id_value1'/># an identifier for the configuration
<property name='OptionName1' value='value1'/>
  ...
<property name='OptionName2' value='value2'/>
</module>

{{Example}}
"""
    prompt = prompt.replace("{{Example}}", example)
    prompt = prompt.replace("{{Style}}", style)
    prompt = prompt.replace("{{DSLruleset}}", dsl_rule_set)
    prompt = prompt.replace("{{tool}}", tool)
    prompt = prompt.replace("{{toolruleset}}", tool_rule_set)
    prompt = prompt.replace("{{Syntax}}", dsl_syntax)
    prompt = prompt.replace("{{grammar}}", grammar)
    return prompt


def get_gpt_response(mappings, google_dsls, model, output_dir):
    agent = GPTAgent()
    result = {}
    print(f"Model: {model}")
    for rule, [_, mapping] in mappings.items():
        print(f"gen config for Rule: {rule}")
        prompt = preprocess_promt(
            dsl_syntax=dsl,
            style="RuleSet of Google Java Style Guide",
            dsl_rule_set=google_dsls[rule][1],
            tool="Checkstyle",
            tool_rule_set=mapping,
            grammar="Grammar",
            example="",
        )
        answer = agent.get_response(prompt, model=model)
        # ! 处理一下
        answer = answer.replace("```xml", "")
        answer = answer.replace("```", "")
        result[rule] = answer  # prompt 太长了
        break
    util.save_json(output_dir, f"{model}_rule_prompt_response", result)
    return result


def save_as_csv(google_dsls, mappings, result, output_path):
    bm = util.load_json("data/benchmark/", "simple_benchmark")
    csv_result = []
    csv_result.append(["rule", "status", "benchmark", "dsl", "prompt", "config"])
    for rule, res in result.items():
        google_dsl = google_dsls[rule] # 处理过的，key是rule，value是dsl
        benchmark = bm[rule]
        if benchmark == []:
            benchmark = ""
        if google_dsl:
            tool_rule_set = mappings[rule][1]
            prompt = preprocess_promt(
                dsl_syntax=dsl,
                style="RuleSet of Google Java Style Guide",
                dsl_rule_set=google_dsl,
                tool="Checkstyle",
                tool_rule_set=tool_rule_set,
                grammar="Grammar",
                example="",
            )
        else:
            prompt = "No need"

        if "module" in res:
            status = "Yes"
        else:
            status = "No"
        one_rule = [
            rule,
            status,
            benchmark,
            google_dsl,
            prompt,
            res,
        ]
        csv_result.append(one_rule)
    util.save_csv(
        output_path,
        csv_result,
    )

if __name__ == "__main__":
    mappings = util.load_json(
        "data/dsl_output/instr_sel/", "gpt-4o_rule_prompt_response"
    )
    check_style_rule_list = get_checkstyle_rules_from_file(
        "data/rule/checkstyle/java/url_name_desc_opt.json"
    )
    google_jdata = util.load_json(
        "data/dsl_output/google/extracted/", "gpt-4o_extracted"
    )
    google_dsls_results = get_all_google_dsl(google_jdata)

    result = get_gpt_response(
        mappings,
        google_dsls_results,
        "gpt-4o",
        "data/dsl_output/final_config/",
    )
    save_as_csv(
        google_dsls_results,
        mappings,
        result,
        "data/dsl_output/final_config/final_config.csv",)
