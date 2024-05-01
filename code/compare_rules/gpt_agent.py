import os
import re
import shutil

from gpt_wrapper import GPTWrapper
class CoTPatterns:
    ANALYZE_TASK = [
        {
            "role": "user",
            "content": "",
        },
    ]

class GPTAgent:

    def __init__(self):
        self.wrapper = GPTWrapper.get_wrapper()
        # self.rule_set_root1 = "data\\rule\\google\\jsguide.json"
        # self.rule_set_root2 = "data\\rule\\eslint"

    def compare_rules_simple(self, rule:str):
        eslint_rules_simple = ""
        simple_path = "data\\rule\\eslint\\overview.md"
        with open(simple_path,'r',encoding='utf-8') as f:
            eslint_rules_simple = f.read()
        
        if len(eslint_rules_simple) > 0:
            question = "Given a rule:\n\n"
            question += rule
            question += "Can you find a corresponding rule in the following rule set?\n\n"
            question += eslint_rules_simple
            answer = self.wrapper.ask(question)
            print(answer)

if __name__ == "__main__":
    agent =  GPTAgent()
    rule_desc = "Do not use the variadic Array constructor. The constructor is error-prone if arguments are added or removed. Use a literal instead."
    agent.compare_rules_simple(rule_desc)