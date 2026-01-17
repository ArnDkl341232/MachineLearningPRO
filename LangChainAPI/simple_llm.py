import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from openai import api_key, models
from langchain.schema import HumanMessage

load_dotenv()

# Обійти помилку, коли немає ключа та продовжити виконання коду
# try:
#     api_key = os.getenv("OPEN_API_KEY")
# except Exception as e:
#     print(e)
#     print("Немає ключа OPEN_API_KEY у .env!")

# Видасть нашу помилку(нас викине, проте покаже, що не так)
if not api_key:
    raise ValueError("Немає ключа OPEN_API_KEY у .env!")

llm = ChatOpenAI(model="",temperature= 0.7)