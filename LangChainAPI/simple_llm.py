import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from openai import api_key, models
from langchain_core.messages import HumanMessage

# Завантажуємо змінні середовища з .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Обійти помилку, коли немає ключа та продовжити виконання коду
# try:
#     api_key = os.getenv("OPEN_API_KEY")
# except Exception as e:
#     print(e)
#     print("Немає ключа OPEN_API_KEY у .env!")

# Видасть нашу помилку(нас викине, проте покаже, що не так)
if not api_key:
    raise ValueError("Немає ключа OPEN_API_KEY у .env!")

# Створюємо LLM-об'єкт
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Готуємо повідомлення від людини (HumanMessage) - формат LangChain
user_question = "Поясни простими словами: що таке штучний інтелект?"

# Викликаємо модель: передаємо список повідомлень (тут лише одне)
response = llm.invoke([HumanMessage(content=user_question)])

# Друкуємо чистий текст відповіді
print("Відповідь LLM:\n", response.content)