import copy
import os
from gpt_agent import GPTAgent
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


def extract_dsl_from_text(gpt_answer_dir, gpt_preprocess_answer_dir_standard_example):

    for ind in range(len(os.listdir(gpt_answer_dir))):
        agent = GPTAgent()
        gpt_dsl_rule_list = util.load_json(gpt_answer_dir, str(ind))
        text = gpt_dsl_rule_list[str(ind)]
        prompt = preprocess_promt(text=text, example="")
        print(">>>>>prompt: ", prompt)
        answer = agent.get_response(prompt, examples=text2dsl_examples, model="gpt-4o")
        print(">>>>>>answer: ", ind, answer)
        util.save_json(
            gpt_preprocess_answer_dir_standard_example, str(ind), {ind: answer}
        )


if __name__ == "__main__":
    gpt_answer_dir = (
        util.data_root
        + "gpt_dsl_answer/CheckStyle_options_3_Simple_DSL_syntax_SplitSentence_example4/"
    )

    gpt_preprocess_answer_dir = (
        util.data_root
        + "gpt_dsl_answer/GoogleJavaStyle_Simple_DSL_syntax_SplitSentence_example4_preprocess/"
    )
    gpt_preprocess_answer_dir_standard_example = (
        util.data_root
        + "gpt_dsl_answer/GoogleJavaStyle_Simple_DSL_syntax_SplitSentence_example4_preprocess/"
    )
    all_rules = util.load_json(
        util.data_root + "style_tool_rules/",
        "checkstyle_name_completedes_options_3_process",
    )

    rule_list_add_gpt_result = []
    one_rule = ["url", "rule_name", "description", "options", "GPT-DSL"]
    rule_list_add_gpt_result.append(one_rule)

    extract_dsl_from_text(gpt_answer_dir, gpt_preprocess_answer_dir_standard_example)
    
    for ind in range(len(os.listdir(gpt_preprocess_answer_dir_standard_example))):
        gpt_dsl_rule_list = util.load_json(
            gpt_preprocess_answer_dir_standard_example, str(ind)
        )

        text = gpt_dsl_rule_list[str(ind)]
        print(text)
        ruleone = copy.deepcopy(all_rules[ind])
        ruleone.insert(4, text)

        rule_list_add_gpt_result.append(ruleone)
    util.save_csv(
        util.data_root
        + "CheckStyle/CheckStyle_options_3_Simple_DSL_syntax_SplitSentence_example4_add_GPT_answer.csv",
        rule_list_add_gpt_result,
    )
