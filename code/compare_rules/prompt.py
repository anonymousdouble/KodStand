import os
import re

class CoTPatterns:
    MAPPING_TASK = [
        {
            "role": "user",
            "content": "Given a rule:\n\nquotes\n\nCan you find a corresponding rule in the following rule set?\n\nNested functions and closures\nUse single quotes\nNo line continuations",
        },
        {
            "role": "assistant",
            "content": "Use single quotes",
        },
        {
            "role": "user",
            "content": "Given a rule:\n\lines-around-directive\n\nCan you find a corresponding rule in the following rule set?\n\nNested functions and closures\nUse single quotes\nNo line continuations",
        },
        {
            "role": "assistant",
            "content": "No matching rule in the rule set",
        },
    ]


target_rule = """
"Do not use the variadic Array constructor. The constructor is error-prone if arguments are added or removed. Use a literal instead."
"""

response_format = """
{
    "Answer": Your respond with Yes or No for whether exists an ESLint configuration for the given style convention,
    
    "Configuration": [

        rule-name_1: [
            'error', 
            {
                option_1: value_1,
                ...
                option_n: value_n
            }
        ],
        ...
        rule-name_n: [
            'error',
            {
                option_1: value_1,
                ...
                option_n: value_n
            }
        ]
    ]
}
"""


class PrompGenerator:

    def __get_rule_simple(self):
        """
        获取rule的简单信息
        """
        def get_single(path):
            rule = path.split("\\")[-1].replace(".md", "")
            desc = ""
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                desc = lines[5].strip()
            return rule, desc
        root_path = "data\\rule\\eslint"
        normal_dir = os.path.join(root_path, "normal")
        deprecated_dir = os.path.join(root_path, "deprecated")
        removed_dir = os.path.join(root_path, "removed")
        res = []
        for file in os.listdir(normal_dir):
            if file.endswith('.md'):
                rule, desc = get_single(
                    os.path.join(normal_dir, file))
                res.append((rule, desc))
        for file in os.listdir(deprecated_dir):
            if file.endswith('.md'):
                rule, desc = get_single(
                    os.path.join(deprecated_dir, file))
                res.append((rule, desc))
        # for file in os.listdir(removed_dir):
        #     if file.endswith('.md'):
        #         rule, desc = get_single_name_desc(os.path.join(removed_dir, file))
        #         res.append((rule, desc))

        return "\n".join([f"{r[0]}: {r[1]}" for r in res])

    def __get_rule_name_desc(self):
        """
        获取rule的详细信息

        """
        def get_single(path):
            rule = path.split("\\")[-1].replace(".md", "")
            desc = []
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines[5:]:
                    if line.startswith("## Rule Details"):
                        break
                    desc.append(line)
            desc = "\n".join(desc)
            # combine multiple '\n'
            desc = re.sub(r'\n+', '\n', desc)
            return rule, desc
        root_path = "data\\rule\\eslint"
        normal_dir = os.path.join(root_path, "normal")
        deprecated_dir = os.path.join(root_path, "deprecated")
        removed_dir = os.path.join(root_path, "removed")
        res = []
        for file in os.listdir(normal_dir):
            if file.endswith('.md'):
                rule, desc = get_single(
                    os.path.join(normal_dir, file))
                res.append((rule, desc))
        for file in os.listdir(deprecated_dir):
            if file.endswith('.md'):
                rule, desc = get_single(
                    os.path.join(deprecated_dir, file))
                res.append((rule, desc))
        # for file in os.listdir(removed_dir):
        #     if file.endswith('.md'):
        #         rule, desc = get_single(os.path.join(removed_dir, file))
        #         res.append((rule, desc))
        return "\n".join([f"# {r[0]}\n## desc\n{r[1]}" for r in res])

    def __get_rule_name_desc_option(self):
        """
        获取rule的详细信息和配置信息
        """
        ...

    def get_rules(self, flag):
        if flag == "simple":
            return self.__get_rule_simple()
        elif flag == "name_desc":
            return self.__get_rule_name_desc()
        elif flag == "name_desc_option":
            return self.__get_rule_name_desc_option()
        else:
            raise ValueError("Invalid flag")

    def get_prompt(self, rule_desc, flag="simple"):
        """

        """

        PROMPT = f"""
Please generate an ESLint configuration based on the following style convention and ESLint rules.
The configuration should only include rules that are relevant to the given style convention.

Style Convention:
{rule_desc}

ESLint Rules:
{self.get_rules(flag)}

Response Format Should be a json object:{response_format}
"""
        return PROMPT


if __name__ == '__main__':
    with open("test_prompt.txt", 'w', encoding="utf-8") as f:
        f.write(PrompGenerator().get_prompt(target_rule, "simple"))
