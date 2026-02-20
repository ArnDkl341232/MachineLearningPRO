import os
from idlelib.run import Executive

from dotenv import load_dotenv
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
vector_store = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)

vector_store = FAISS.from_documents(docs, embeddings)

@tool
def search_faq(query: str) -> str:
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


tools = ["calculator",search_faq]

#system prompt(If desired, specify custom instructions)
prompt = (
    "You have access to a tool that retrieves context from a blog post. "
    "Use the tool to help answer user queries."
    "Give straight answers to the questions without emojis"
)
# agent = create_agent(model, tools, system_prompt=prompt)
agent = create_agent(llm, tools, system_prompt=prompt)