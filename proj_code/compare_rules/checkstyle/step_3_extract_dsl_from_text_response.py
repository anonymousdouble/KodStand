import os
import sys
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


def preprocess_prompt(text: str, example=""):
    prompt = """Extract Final Ruleset Description from given analyze text. 

Text:
{{Input}}

{{Example}}"""
    prompt = prompt.replace("{{Example}}", example)
    prompt = prompt.replace("{{Input}}", text)
    return prompt


def extract_dsl_from_text(model, dsl_of_rules):
    result = {}
    agent = GPTAgent()
    for rule, [_, response] in dsl_of_rules.items():
        print(f"extract dsl for: {rule}")
        prompt = preprocess_prompt(text=response, example="")
        answer = agent.get_response_with_examples(
            prompt, examples=text2dsl_examples, model=model
        )
        result[rule] = [prompt, answer]
    return result


if __name__ == "__main__":
    # 已生成google和checkstyle的dsl output，从中进一步提取dsl
    rule_list = util.load_json("data/rule/checkstyle/java/","url_name_desc_opt")
    for dsl_output_dir in ["data/dsl_output/checkstyle_advanced/",]:
        for model in ["gpt-4o",]:
            print("Model:", model)
            dsl_of_rules = util.load_json(
                dsl_output_dir, f"{model}_rule_prompt_response_simple"
            )
            extracted_dsl_data = extract_dsl_from_text(model,dsl_of_rules)
            output_root = os.path.join(dsl_output_dir,"extracted/")
            util.save_json(output_root, f"{model}_extracted", extracted_dsl_data)