import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")


def call_ai(messages):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openrouter/free",
            "messages": messages,
            "max_tokens": 1500
        }
    )

    data = response.json()

    # 🔥 debugging مهم
    if "error" in data:
        print("API ERROR:", data)
        return "ERROR"

    return data["choices"][0]["message"]["content"]


def manager_agent(user_input):
    messages = [
        {
            "role": "system",
            "content": """
You are a senior AI project manager.

IMPORTANT:
- Do NOT solve the task
- Do NOT write the final content

Your job ONLY:
1. Understand the task
2. Break it into steps
3. Assign tasks to:
   - Research Agent
   - Writer Agent
   - Critic Agent

Output format:

1. Task Understanding
(short explanation)

2. Execution Plan
(step by step)

3. Agent Responsibilities
- Research Agent: ...
- Writer Agent: ...
- Critic Agent: ...
"""
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    return call_ai(messages)
def research_agent(plan):
    messages = [
        {
            "role": "system",
            "content": """
You are a market research expert.

Give short, clear, useful insights.

Output:

1. Market Trends
2. Target Audience
3. Competitors
4. Opportunities
"""
        },
        {
            "role": "user",
            "content": plan
        }
    ]

    return call_ai(messages)


def writer_agent(plan, research):
    messages = [
        {
            "role": "system",
            "content": """
You are a senior marketing strategist.

Write a strong marketing plan based on the given inputs.

Keep it:
- Clear
- Structured
- Practical

Output:

1. Executive Summary
2. Positioning
3. Target Audience
4. Strategy
5. Action Plan
"""
        },
        {
            "role": "user",
            "content": f"""
Manager Plan:
{plan}

Research:
{research}
"""
        }
    ]

    return call_ai(messages)
def critic_agent(content):
    messages = [
        {
            "role": "system",
            "content": """
You are a senior marketing critic.

IMPORTANT:
- Stay within the SAME topic (coffee startup)
- Do NOT change the domain
- Do NOT rewrite everything

Your job:
- Analyze the marketing plan
- Find realistic weaknesses
- Suggest practical improvements

Output:

1. Weaknesses (specific)
2. Missing Elements
3. Risks (related to coffee startup)
4. Improvement Suggestions (clear and actionable)
"""
        },
        {
            "role": "user",
            "content": content
        }
    ]

    return call_ai(messages)
def improve_agent(content, feedback):
    messages = [
        {
            "role": "system",
            "content": """
You are a marketing expert improving a plan.

IMPORTANT:
- KEEP the same idea (coffee startup)
- Improve it, DO NOT change it
- Keep structure, just enhance

Make it:
- clearer
- stronger
- more realistic
- more persuasive

Do NOT change topic.
"""
        },
        {
            "role": "user",
            "content": f"""
Original Plan:
{content}

Critic Feedback:
{feedback}
"""
        }
    ]

    return call_ai(messages)




if __name__ == "__main__":
    user_input = input("Enter your idea: ")

    # Manager
    plan = manager_agent(user_input)
    print("\n=== MANAGER ===\n")
    print(plan)

    # Research
    research = research_agent(plan)
    print("\n=== RESEARCH ===\n")
    print(research)

    # Writer
    content = writer_agent(plan, research)
    print("\n=== WRITER OUTPUT ===\n")
    print(content)

    # Critic 😈
    feedback = critic_agent(content)
    print("\n=== CRITIC ===\n")
    print(feedback)

    # Final 💀
    final = improve_agent(content, feedback)
    print("\n=== FINAL VERSION ===\n")
    print(final)
