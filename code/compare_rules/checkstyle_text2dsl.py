import copy
import os
import sys
from checkstyle2dsl import get_checkstyle_rules_from_file
from gpt_agent_028 import GPTAgent

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)
import util

text2dsl_examples = [
    [
        """Extract Final Ruleset Description from given analyze text. 

Text:
Let's analyze and parse the CheckStyle Rule "IllegalInstantiation" using the given Grammar.

### Step 1: Analyze Description

**Description:**
- "Checks for illegal instantiations where a factory method is preferred."

This is a rule. It specifies that instantiations should be done using factory methods instead of direct constructor calls. This rule is **mandatory**.

- "Rationale: Depending on the project, for some classes it might be preferable to create instances through factory methods rather than calling the constructor."

This is not a rule. It provides a rationale and is subjective.

- "A simple example is the java.lang.Boolean class. For performance reasons, it is preferable to use the predefined constants TRUE and FALSE. Constructor invocations should be replaced by calls to Boolean.valueOf()."

This is an example and not a rule. It is subjective and provides context.

- "Some extremely performance sensitive projects may require the use of factory methods for other classes as well, to enforce the usage of number caches or object pools."

This is not a rule. It is subjective and provides additional context.

### Step 2: Analyze Options

**Options:**
- `classes`: "Specify fully qualified class names that should not be instantiated.", `String[]`, `{}`

This option is a configurable term. It allows specifying class names that should not be instantiated directly. We will use `{{classes}}` to represent this term.

### Step 3: Parse the Rule

**Basic Rule:**
- The rule specifies that instantiations should be done using factory methods instead of direct constructor calls.

Using the given Grammar, we can represent this as:
```plaintext
{{Mandatory}} [Instantiation] of {{classes}} is not [Constructor] -> [Instantiation] of {{classes}} is [FactoryMethod]
```

**Option Rule:**
- The `classes` option allows specifying fully qualified class names that should not be instantiated directly.

Using the given Grammar, we can represent this as:
```plaintext
{{classes}} has [ClassName]
```

### Final RuleSet Representation

```plaintext
Basic Rule:
{{Mandatory}} [Instantiation] of {{classes}} is not [Constructor] -> [Instantiation] of {{classes}} is [FactoryMethod]

Option Rule:
{{classes}} has [ClassName]
```

### Explanation

- **Basic Rule:** This rule mandates that if there is an instantiation of any class specified in `{{classes}}`, it should not be done using a constructor. Instead, it should be done using a factory method.
- **Option Rule:** This option allows specifying the fully qualified class names that should not be instantiated directly.

This representation makes the semantics of the CheckStyle Rule "IllegalInstantiation" clear and correct according to the given Grammar.
""",
        """The Extracted Final Ruleset Description is:
Basic Rule:
{{Mandatory}} [Instantiation] of {{classes}} is not [Constructor] -> [Instantiation] of {{classes}} is [FactoryMethod]

Option Rule:
{{classes}} has [ClassName]
""",
    ]
]


def preprocess_promt(text: str, example=""):
    prompt = """Extract Final Ruleset Description from given analyze text. 

Text:
{{Input}}

{{Example}}"""

    prompt = prompt.replace("{{Example}}", example)
    prompt = prompt.replace("{{Input}}", text)

    return prompt


def extract_dsl_from_text(dsl_of_rules):
    result = {}
    for rule, [_, response] in dsl_of_rules.items():
        agent = GPTAgent()
        prompt = preprocess_promt(text=response, example="")
        answer = agent.get_response_with_examples(
            prompt, examples=text2dsl_examples, model="gpt-4o"
        )
        result[rule] = [prompt, answer]
        break
    return result


if __name__ == "__main__":
    for model in ["gpt-4o", "gpt-3.5-turbo-0125"]:

        dsl_output_dir = "data/dsl_output/checkstyle_option_cls_complex/"
        dsl_of_rules = util.load_json(
            dsl_output_dir, f"{model}_rule_prompt_response_simple"
        )
        extracted_dsl_data = extract_dsl_from_text(dsl_of_rules)

        # save as csv
        rule_list = util.load_json("data/rule/checkstyle/java/","url_name_desc_opt")
        res_list = []
        one_rule = ["url", "rule_name", "description", "options", "GPT-DSL"]
        res_list.append(one_rule)
        for rule in rule_list[:10]:
            url = rule[0]
            rule_name = rule[1]
            description = rule[2]
            options = rule[3]
            dsl = dsl_of_rules[rule_name][1]
            one_rule = [url, rule_name, description, options, dsl]
            res_list.append(one_rule)
        pps_output_path = f"data/pps_dsl_output/{model}_checkstyle_dsl.csv"
        util.save_csv(pps_output_path, res_list)
