import os
from idlelib.run import Executive

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import tool

load_dotenv()

# Створюємо LLM-об'єкт
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

@tool(
    "calculator",
    description="Calculate math expression ('0123456789+-*/(). ')"
)
def safe_calculate(expression: str) -> str:
    # "2 + 3 * 5"
    allowed_chars = "0123456789+-*/()."
    if not all(ch in allowed_chars for ch in expression):
        return "Error! allowed chars: 0123456789+-*/()."
    try:
        result = eval(expression, {"__builtins__": {}},{})
        return result
    except Exception as e:
        return f"Error: {e}"

#------------------------------------
#Декоратор
#
# def func():
#     pass
#
# func = decorator_name(func)
#
# @func
# def func_new():
#     n = "qwerty" # func() -> "qwerty"
#
# -------------------------------------
