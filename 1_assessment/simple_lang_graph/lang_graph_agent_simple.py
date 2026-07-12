from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage

from langgraph.graph import StateGraph, MessagesState, START, END

# ====== 1. Инициализация ======
model = ChatOllama(model='qwen2.5:3b')
chat_history = []

# ====== 3. Функции для работы с историей ======
def add_to_history(role, message):
    chat_history.append({"role": role, "content": message})

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
        with open('notes.txt', 'a', encoding="utf-8") as f:
            f.write(text + '\n')
        return f"Note '{text[:30]}...' saved to notes.txt"
    except FileNotFoundError:
        return "File not found"

def decide(state: MessagesState)->MessagesState:
    messages = state["messages"]

    if not any(isinstance(msg, SystemMessage) for msg in messages):
        system_msg = SystemMessage(content="""ТЫ РУССКОЯЗЫЧНЫЙ АССИСТЕНТ. 
КАТЕГОРИЧЕСКИ ЗАПРЕЩЕНО отвечать на английском.
Если пользователь пишет по-русски - отвечай по-русски.
Даже если инструменты вернули английский текст - переведи ответ на русский.
Твой язык: ТОЛЬКО РУССКИЙ.""")
        messages = [system_msg] + messages

    model_with_tools = model.bind_tools([calculate, save_note])

    response = model_with_tools.invoke(messages)

    new_messages = state["messages"] + [response]

    return {"messages": new_messages}

def should_continue(state: MessagesState) -> str:
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "execute"
    else:
        return "respond"

def execute(state: MessagesState)->MessagesState:
    last_message = state["messages"][-1]
    new_messages = state["messages"]

    for tool_call in last_message.tool_calls:
        if tool_call["name"] == "calculator":
            result = calculate.invoke(tool_call["args"])
        elif tool_call["name"] == "save_note":
            result = save_note.invoke(tool_call["args"])
        else:
            result = f"Unknown tool: {tool_call['name']}"

        tool_message = ToolMessage(content=result, tool_call_id=tool_call["id"])
        new_messages = new_messages + [tool_message]

    return {"messages": new_messages}


def respond(state: MessagesState)->MessagesState:
    messages = state["messages"]

    has_tool_result = any(isinstance(msg, ToolMessage) for msg in messages)

    if has_tool_result:
        # Если инструмент выполнялся, просто просим подтвердить на русском
        prompt = "На предыдущем шаге инструмент уже сохранил заметку. Просто подтверди пользователю на русском языке, что заметка сохранена."
        messages = messages + [HumanMessage(content=prompt)]

    response = model.invoke(messages)
    new_messages = state["messages"] + [response]
    return {"messages": new_messages}

graph = StateGraph(MessagesState)
graph.add_node("decide", decide)
graph.add_node("execute", execute)
graph.add_node("respond", respond)

graph.add_edge(START, "decide")
graph.add_conditional_edges("decide", should_continue, {
    "execute": "execute",
    "respond": "respond"
})
graph.add_edge("execute", "respond")
graph.add_edge("respond", END)



app = graph.compile()


# Тестируем на разных запросах
def test_agent(query):
    print(f"\n🔍 Запрос: {query}")
    print("-" * 50)

    # Создаем начальное состояние
    initial_state = {
        "messages": [HumanMessage(content=query)]
    }

    # Запускаем граф
    result = app.invoke(initial_state)

    # Выводим все сообщения
    for i, msg in enumerate(result["messages"]):
        role = msg.__class__.__name__
        content = msg.content[:50] + "..." if len(msg.content) > 50 else msg.content
        print(f"{i + 1}. {role}: {content}")

    # Финальный ответ
    print(f"\n✅ Ответ: {result['messages'][-1].content}")

    return result


# Тест 1: Простой вопрос (без инструментов)
test_agent("Привет, как дела?")

# Тест 2: Математика (с инструментом)
test_agent("Сколько будет 15 * 7?")

# Тест 3: Сохранение заметки (с инструментом)
test_agent("Запиши заметку: купить молоко")
