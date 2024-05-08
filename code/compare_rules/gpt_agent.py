import json
import os
import re
import shutil
import pandas as pd
from gpt_wrapper import GPTWrapper
from prompt import PrompGenerator


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

    def simple_qa(self,question):
        try:
            answer = self.wrapper.ask(question)
        except Exception as e:
            print(e)
            return None
        return answer

    def match_from_excel(self,excel_path):
        df = pd.read_excel(excel_path)
        generator = PrompGenerator()

        result = []
        for i in range(len(df)):
            google_rule = df.loc[i, "Section Name"]
            desc = df.loc[i, "Total Description"]
            if not pd.isnull(desc):
                rule_detail = f"{google_rule}\n{desc}"
                print(f"Matching {google_rule}")
                prompt = generator.get_prompt(rule_detail, "simple")
                answer = self.simple_qa(prompt)
                if answer is not None:
                    result.append(f"{google_rule}\n{answer}")
        with open("data\\matching\\google2eslint\\matching_auto.txt", "w", encoding="utf-8") as f:
            for r in result:
                f.write(f"{r}\n")

if __name__ == "__main__":
    agent = GPTAgent()
    agent.match_from_excel("data\\matching\\google2eslint\\google.xlsx")