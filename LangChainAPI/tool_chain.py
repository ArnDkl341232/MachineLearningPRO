import os
from idlelib.run import Executive
from importlib.resources import contents

from dotenv import load_dotenv
from langchain_classic.chains.question_answering.map_reduce_prompt import messages
from langchain_core.messages.tool import tool_call
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.tools import tool
from openai import embeddings, vector_stores

load_dotenv()

# Створюємо LLM-об'єкт
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

@tool(
    "calculator",
    description="Calculate math expression ('0123456789+-*/(). ')"
)
def safe_calculate(expression: str) -> str:
    "Калькулятор"
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
# def func():lan
#     pass
#
# func = decorator_name(func)
#
# @func
# def func_new():
#     n = "qwerty" # func() -> "qwerty"
#
# -------------------------------------
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

with open("data/faq.txt", "r", encoding="utf-8") as f:
    faq_text = f.read()
splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
docs = splitter.create_documents([faq_text])

embeddings = OpenAIEmbeddings()
# vector_store = FAISS(
#     embedding_function=embeddings,
#     index=index,
#     docstore=InMemoryDocstore(),
#     index_to_docstore_id={},
# )

vector_store = FAISS.from_documents(docs, embeddings)

@tool
def search_faq(query: str) -> str:
    "Питання/Відповідь FAQ"
    try:
        # result = vector_store.search(query)
        result = vector_store.similarity_search(query, k=1)
        if not result:
            return "Нічього не знайдено в FAQ"
        return result[0].page_content


    except Exception as e:
        return f"Error search: {e}"


@tool
def weather_api(city: str) -> str:
    "Відповідає на питання про погоду. Формат: Назва міста англіською "
    data = {
        "Kharkiv": "Сонячно, 0..+2°C,вітряно",
        "Kyiv": "Хмарно, -1..+1°C",
        "Kyiv": "Дощ, +2..+3°C",
    }
    return data.get(
        city,
        f"Немає даний для введеного міста, спробуйте: {', '.join(list(data.keys()))}" )


#створення агента
from langchain.agents import create_agent


tools = [safe_calculate, search_faq, weather_api]

#system prompt(If desired, specify custom instructions)
prompt = (
    "You have access to a tool that retrieves context from a blog post. "
    "Use the tool to help answer user queries."
    "Give straight answers to the questions without emojis"
    "Ти корисний асистент. Коли треба рахувати — використовуй 'calculator'. "
    "Про магазин — шукай у 'faq_search'. А погоду — 'weather_api'. "
    "Спершу зрозумій запит, потім виріши, який інструмент доречний."
)
# agent = create_agent(model, tools, system_prompt=prompt)
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=prompt,
    debug=True
)

def get_output(result: dict) -> str:
    messages = result.get("message",[])
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

if __name__ == "__main__":
    print("\n===Калькулятор===")
    result = agent.invoke({"messages": [{"role": "user","content": "Обчисли: (2+3)*4-5"}]})
    print(get_output(result))

if __name__ == "__main__":
    print("\n===FAQ===")
    result = agent.invoke({"messages": [{"role": "user","content": "Як здійснити оплату"}]})
    print(get_output(result))

if __name__ == "__main__":
    print("\n===Погода===")
    result = agent.invoke({"messages": [{"role": "user","content": "Яка погода у Kyiv"}]})
    print(get_output(result))