import os
from http.cookiejar import debug

from dotenv import  load_dotenv
from langchain_classic.chains.qa_generation.prompt import templ
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from tool_chain import agent

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature = 0.7)

agent = create_agent(
    model=llm,
    tools=[],
    system_prompt="Ти дружній агент, що відповідає просто і корисно",
    debug=False
)

def get_output(result: dict) -> str:
    messages = result.get("messages", [])
    for msg in reversed(messages):
     content = getattr(msg, "content", None)
     tool_calls = getattr(msg, "tool_calls", None) or []
     if content and not tool_calls:
         if isinstance(content, str):
             return content
         if isinstance(content, list):
             return "".join(
                 c.get("text", str(c)) if isinstance(c, dict) else str(c) for c in content
             )
    return ""

chat_messages = []
def chat(user_input: str) -> str:
    chat_messages.append({"role": "user", "content": user_input})
    result = agent.invoke({"messages": chat_messages})
    chat_messages.clear()
    chat_messages.extend(result["messages"])

    return get_output(result)

def run_demo():
    print("Відповідь 1:", chat("Привіт! Мене звати Оксана"))
    print("Відповідь 2:", chat("Запам'ятай, я люблю програмування"))
    print("Відповідь 3:", chat("Нагадай, як мене звати і що мені подобається?"))

if __name__ == "__main__":
    run_demo()


















