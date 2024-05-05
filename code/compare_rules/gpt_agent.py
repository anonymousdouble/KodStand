import json
import os
import re
import shutil

from gpt_wrapper import GPTWrapper

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


class GPTAgent:

    def __init__(self):
        self.wrapper = GPTWrapper.get_wrapper()
        # self.rule_set_root1 = "data\\rule\\google\\jsguide.json"
        # self.rule_set_root2 = "data\\rule\\eslint"

    def compare_rules_simple(self, rule: str):
        eslint_rules_simple = ""
        simple_path = "data\\rule\\eslint\\overview.md"
        with open(simple_path, 'r', encoding='utf-8') as f:
            eslint_rules_simple = f.read()

        if len(eslint_rules_simple) > 0:
            question = "Given a rule:\n\n"
            question += rule
            question += "\n\nCan you find a corresponding rule in the following rule set?\n\n"
            question += eslint_rules_simple
            answer = self.wrapper.ask(question)
            print(answer)

    def e2g(self, rule):
        if not hasattr(self, 'titles'):
            self.google_rules = []
            with open("data\\rule\\google\\jsguide.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                for r in data:
                    self.google_rules.append(r)
            self.titles = [" ".join(case["title"].split()[1:])
                           for case in self.google_rules if len(case["cases"]) > 0]

        question = "Given a rule:\n\n"
        question += rule
        question += "\n\nCan you find a corresponding rule in the following rule set?\n\n"

        question += '\n'.join(self.titles)

        question += "\n\n Only provide the most likely option."

        try:
            answer = self.wrapper.ask(question)
            print(answer)
        except Exception as e:
            print(e)
            return None
        # print(answer)
        for t in self.titles:
            if t in answer:
                return t

        return None


if __name__ == "__main__":
    agent = GPTAgent()
    # rule_desc = "Do not use the variadic Array constructor. The constructor is error-prone if arguments are added or removed. Use a literal instead."
    # agent.compare_rules_simple(rule_desc)
    rules = []
    with open("data\\config\\eslint\\google_config.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for r in data:
            rules.append(f"{r}")

    res = {}
    for r in rules:
        print(f"finding mapping of rule: {r}")
        correspond_rule = agent.e2g(r)
        print(f"corresponding rule is : {correspond_rule}")
        if correspond_rule is not None:
            res[r] = correspond_rule
        else:
            res[r] = None
        break
    # with open("output.json", "w", encoding="utf-8") as f:
    #     json.dump(res, f, ensure_ascii=False, indent=4)
