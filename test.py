from proj_code.compare_rules.gpt_agent_028 import GPTAgent


if __name__ == "__main__":
    agent = GPTAgent()
    question = open("data/debug/q.txt", "r", encoding="utf-8").read()
    answer = agent.get_response(question, model="gpt-4o")
    with open("data/debug/answer.txt", "w", encoding="utf-8") as f:
        f.write(answer)
