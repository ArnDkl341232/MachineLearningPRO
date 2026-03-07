import os
import sys
from random import choice

from dotenv import  load_dotenv
from langchain_classic.chains.qa_generation.prompt import templ
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from tool_chain import agent

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature = 0.7)
chat_messages = []

agent = create_agent(
    model=llm,
    tools=[],
    system_prompt="Ти дружній агент, що відповідає просто і корисно",
    debug=False
)
#Витягує текст останньої відповіді AI з result["messages"]
#Ітеруємо reversed(), бо фінальна відповідь - зазвичай останній AIMessage без tool_calls
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


def chat(user_input: str, agent = agent) -> str:
    chat_messages.append({"role": "user", "content": user_input})
    result = agent.invoke({"messages": chat_messages})
    chat_messages.clear()
    chat_messages.extend(result["messages"])

    return get_output(result)


# Три повідомлення: введення імені, введення вподобання, запит на згадування
# Агент має використати контекст з попередніх турів (пам'ять працює)
def run_demo():
    print("\n" + "=" * 60)
    print("  ДЕМО РЕЖИМ   ")
    print("  Введіть 'exit', 'quit', 'q' або '/вихід' для завершення.")
    print("=" * 60 + "\n")
    """Запускає фіксований сценарій з трьома повідомленнями."""
    print("Відповідь 1:", chat("Привіт! Мене звати Оксана"))
    print("Відповідь 2:", chat("Запам'ятай, я люблю програмування"))
    print("Відповідь 3:", chat("Нагадай, як мене звати і що мені подобається?"))

    while True:
        try:
            user_input = input("Ви: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nДо побачення!")
            break

        if not user_input:
            continue

        # Команди виходу
        if user_input.lower() in ("exit", "quit", "q", "/вихід"):
            print("До побачення!")
            break



def run_interactive(agent = agent):
    """
    Інтерактивний чат у терміналі. Введіть повідомлення — отримаєте відповідь.
    Для виходу: exit, quit, q або /вихід
    """
    print("\n" + "=" * 60)
    print("  ІНТЕРАКТИВНИЙ РЕЖИМ - чат з агентом (пам'ять увімкнена)")
    print("  Введіть 'exit', 'quit', 'q' або '/вихід' для завершення.")
    print("=" * 60 + "\n")

    while True:
        try:
            user_input = input("Ви: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nДо побачення!")
            break

        if not user_input:
            continue

        # Команди виходу
        if user_input.lower() in ("exit", "quit", "q", "/вихід"):
            print("До побачення!")
            break

        response = chat(user_input, agent = agent)
        print(f"Бот: {response}\n")


if __name__ == "__main__":
    if "-i" in sys.argv or "--interactive" in sys.argv:
        run_interactive()
    if "-d" in sys.argv or "--demo" in sys.argv:
        run_demo()

    # else:
    #     run_demo()
    #     print("\n" + "-" * 40)
    #     try:
    #         choice = input("Перейти в інтерактивний режим? (y/n): ").strip().lower()
    #         if choice in ("y","yes","так","т"):
    #             run_interactive()
    #     except(EOFError, KeyboardInterrupt):
    #         pass

    # try:
    #     choice = input("Перейти в інтерактивний режим? (y/n): ").strip().lower()
    #     if choice in ("y","yes","так","т"):
    #         run_interactive()
    #     else:
    #         run_demo()
    # except(EOFError, KeyboardInterrupt):
    #     pass










