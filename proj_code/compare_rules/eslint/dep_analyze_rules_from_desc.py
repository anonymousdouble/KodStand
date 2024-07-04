import os
import json
from gpt_agent_028 import GPTAgent

# handle csv
import pandas as pd

prompt_template = """Please analyze the following sentences of google style guide, and extract the following information:
- rule description # if the sentence describes a rule
- rule type # whether the rule is mandatory or optional

Google JavaScript Style Guide:

{{rule_name}}
{{desc}}

Your response should be in the following format:

1. Rule Description: # rule description
   - Rule Type: Mandatory | Optional
2. Rule Description: # rule description
    - Rule Type: Mandatory | Optional
...
"""
example_rule_name = """9.4.4.2 Aliasing with goog.scope"""
example_desc = """WARNING: `goog.scope` is deprecated. New files should not use `goog.scope` even in projects with existing `goog.scope` usage.
`goog.scope` may be used to shorten references to namespaced symbols in code using `goog.provide` / `goog.require` dependency management.
Only one `goog.scope` invocation may be added per file. Always place it in the global scope.
The opening `goog.scope(function(){` invocation must be preceded by exactly one blank line and follow any `goog.provide` statements, `goog.require` statements, or top-level comments. The invocation must be closed on the last line in the file. Append `//goog.scope` to the closing statement of the scope. Separate the comment from the semicolon by two spaces.
Similar to C++ namespaces, do not indent under `goog.scope` declarations. Instead, continue from the 0 column.
Only make aliases for names that will not be re-assigned to another object (e.g., most constructors, enums, and namespaces). Do not do this (see below for how to alias a constructor):
goog.scope(function() {
var Button = goog.ui.Button;

Button = function() { ... };
...

Names must be the same as the last property of the global that they are aliasing.
goog.provide('my.module.SomeType');

goog.require('goog.dom');
goog.require('goog.ui.Button');

goog.scope(function() {
var Button = goog.ui.Button;
var dom = goog.dom;

// Alias new types after the constructor declaration.
my.module.SomeType = function() { ... };
var SomeType = my.module.SomeType;

// Declare methods on the prototype as usual:
SomeType.prototype.findButton = function() {
  // Button as aliased above.
  this.button = new Button(dom.getElement('my-button'));
};
...
});  // goog.scope"""
example_response = """1. Rule Description: `goog.scope` is deprecated. New files should not use `goog.scope` even in projects with existing `goog.scope` usage.
   - Rule Type: Mandatory
2. Rule Description: `goog.scope` may be used to shorten references to namespaced symbols in code using `goog.provide` / `goog.require` dependency management.
   - Rule Type: Optional
3. Rule Description: Only one `goog.scope` invocation may be added per file. Always place it in the global scope.
   - Rule Type: Mandatory
4. Rule Description: The opening `goog.scope(function(){` invocation must be preceded by exactly one blank line and follow any `goog.provide` statements, `goog.require` statements, or top-level comments. The invocation must be closed on the last line in the file. Append `//goog.scope` to the closing statement of the scope. Separate the comment from the semicolon by two spaces.
   - Rule Type: Mandatory
5. Rule Description: Similar to C++ namespaces, do not indent under `goog.scope` declarations. Instead, continue from the 0 column.
   - Rule Type: Mandatory
6. Rule Description: Only make aliases for names that will not be re-assigned to another object (e.g., most constructors, enums, and namespaces). Do not do this (see below for how to alias a constructor):
   - Rule Type: Mandatory
7. Rule Description: Names must be the same as the last property of the global that they are aliasing.
   - Rule Type: Mandatory"""


def preprocess_prompt(prompt, rule_name, desc):
    my_prompt = prompt.replace("{{rule_name}}", rule_name)
    my_prompt = prompt.replace("{{desc}}", desc)
    return my_prompt


def gen_gpt_response(desc):
    agent = GPTAgent()
    results = {}
    example_prompt = preprocess_prompt(prompt_template, example_rule_name, example_desc)
    example = [[example_prompt, example_response]]
    # cnt = 0
    for item in desc:
        # cnt += 1
        # if cnt > 10:
        #     break
        rule_name = item["title"]
        cases = item["cases"]
        print(f"Processing rule: {rule_name}")
        rule_desc_data = []
        for case in cases:
            case_data = []
            for _, v in case.items():
                case_data.append(v)
            case_str = "\n".join(case_data)
            rule_desc_data.append(case_str)
        rule_desc = "\n".join(rule_desc_data)
        my_prompt = preprocess_prompt(prompt_template, rule_name, rule_desc)
        if rule_name == "1 Introduction" or rule_desc == "":
            results[rule_name] = [rule_desc, ""]
            continue
        response = agent.get_response_with_examples(my_prompt, examples=example)
        results[rule_name] = [rule_desc, response]
    output_dir = "data/google_js_rules"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(output_dir + "/google_js_rules.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
    return results


if __name__ == "__main__":
    #! online
    desc_file = "data/rule/google/jsguide.json"
    desc = None
    with open(desc_file, "r", encoding="utf-8") as f:
        desc = json.load(f)
    data = gen_gpt_response(desc)
    #! offline
    # with open("data/google_js_rules/google_js_rules.json", "r", encoding="utf-8") as f:
    #     data = json.load(f)
    csv_data = []
    for rule, [rule_desc, response] in data.items():
        csv_data.append([rule, rule_desc, response.strip() if rule_desc != "" else ""])
    heads = ["rule", "rule_desc", "response"]
    df = pd.DataFrame(csv_data, columns=heads)
    df.to_csv("data/google_js_rules/google_js_rules.csv", index=False)
