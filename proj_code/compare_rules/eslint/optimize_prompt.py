from proj_code.compare_rules.gpt_agent_028 import GPTAgent


if __name__ == '__main__':
    path = "data/templates/extract_eslint_options_prompt.txt"
    agent = GPTAgent()
    template = open(path, "r", encoding="utf-8").read()
    prompt = f"""Please optimize the following prompt:

{template}"""
    response = agent.get_response(prompt, model="gpt-4o")
    with open("data/debug/extract_eslint_options_prompt_optimized.txt", "w", encoding="utf-8") as f:
        f.write(response)