from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from pydantic import BaseModel, ValidationError
import json

from langchain.agents import create_agent

# ====== 1. Инициализация ======
model = ChatOllama(model='qwen2.5:3b')
chat_history = []


# ====== 2. Классы для данных ======
class Person(BaseModel):
    name: str
    age: int
    city: str
    profession: str


# ====== 3. Функции для работы с историей ======
def add_to_history(role, message):
    chat_history.append({"role": role, "content": message})


def show_history():
    for msg in chat_history:
        print(f"{msg['role']}: {msg['content']}")


def save_history(filename='chat_history.json'):
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(chat_history, f, ensure_ascii=False, indent=2)
    print(f"История сохранена в {filename}")


def load_history(filename="chat_history.json"):
    global chat_history

    try:
        with open(filename, 'r', encoding="utf-8") as f:
            chat_history = json.load(f)
        print(f"История загружена из {filename}")
    except FileNotFoundError:
        print("Файл не найден, начинаем с пустой истории")
        chat_history = []


# ====== 4. Обычный чат с памятью ======
def chat_with_memory(user_input):
    add_to_history("user", user_input)

    messages = []

    for msg in chat_history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))

    response = model.invoke(messages)
    ai_response = response.content

    add_to_history("assistant", ai_response)

    return ai_response


# ====== 5. Структурированный вывод ======
def extract_person_info(text):
    prompt = f"""
    Извлеки информацию о человеке из следующего текста.
    Текст: "{text}"

    Верни ТОЛЬКО JSON в таком формате:
    {{
        "name": "имя человека",
        "age": возраст (число),
        "city": "город",
        "profession": "профессия"
    }}

    Не добавляй никаких пояснений, только JSON.
    """

    response = model.invoke([HumanMessage(content=prompt)])
    response_text = response.content

    print("Сырой ответ модели:", response_text)

    cleaned = response_text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned.replace("```json", "").replace("```", "")
    elif cleaned.startswith("```"):
        cleaned = cleaned.replace("```", "")

    cleaned = cleaned.strip()

    try:
        data = json.loads(cleaned)

        person = Person(**data)
        return person

    except json.JSONDecodeError as e:
        print(f"Ошибка парсинга JSON: {e}")
        return None
    except ValidationError as e:
        print(f"Ошибка валидации Pydantic: {e}")
        return None


@tool("calculator")
def calculate(a: float, b: float, operation: str) -> str:
    """
    Performs arithmetic calculations. Use this for math problems (+, -, *, /).
    """
    if operation == '+':
        return f"The result is {str(a + b)}"

    elif operation == '-':
        return f"The result is {str(a - b)}"

    elif operation == '*':
        return f"The result is {str(a * b)}"

    elif operation == '/':
        try:
            return f"The result is {str(a / b)}"
        except ZeroDivisionError:
            return "Error: division by zero"

    else:
        return "Unsupported operation"

@tool("save_note")
def save_note(text: str) -> str:
    """
    Saves a text note to a file. Use this when user asks to save information,
    create a note, or write something to a file.
    """
    try:
        with open('../simple_lang_graph/notes.txt', 'a', encoding="utf-8") as f:
            f.write(text + '\n')
        return f"Note '{text[:30]}...' saved to notes.txt"
    except FileNotFoundError:
        return "File not found"

tools = [calculate, save_note]


# ====== 7. Простой агент с инструментами ======
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="You are a helpful assistant with access to tools. Use calculator "
                  "for math problems. Use save_note when user asks to save notes "
                  "or information. Respond in Russian."
)

# Тестируем калькулятор
result1 = agent.invoke({
    "messages": [
        {"role": "user", "content": "сколько будет 15 * 7?"}
    ]
})

print("Калькулятор:", result1)

# Тестируем сохранение заметки
result2 = agent.invoke({
    "messages": [
        {"role": "user", "content": "запиши заметку: купить молоко"}
    ]
})
print("Заметка:", result2)

# Посмотрим, как выглядят инструменты
print("\nИнструменты:")
for tool in tools:
    print(f"- {tool.name}: {tool.description}")
    print(f"  Аргументы: {tool.args}")