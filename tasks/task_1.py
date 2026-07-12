import requests

MODEL_NAME = "qwen2.5:3b"
TEMPERATURE = 0
MAX_TOKENS = 2
AGENT_MODE = "добрый"

def get_system_prompt():
    if AGENT_MODE == "саркастичный":
        return "Ты саркастичный агент. Отвечай с юмором, используй местный колорит Таганрога"
    else:
        return "Ты добрый агент. Отвечай вежливо с пониманием, не груби и показывай свою готовность помочь"

def get_weather():
    return 'Сегодня +25 и солнечно в Таганроге'

def ask_agent(question, history):
    try:
        prompt = ' '.join([get_system_prompt(), history, question])
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "temperature": TEMPERATURE,
                "options": {
                    "num_predict": MAX_TOKENS
                }
            }
        )

        if response.status_code != 200:
            print("Ой, я потерял связь с моделью. Попробуй позже.")
            return

        if not response or not response.json()["response"]:
            print("Кажется, я не понял вопрос. Можешь переформулировать?")
            return

        return response.json()["response"]
    except requests.exceptions.RequestException:
        print("Ой, я потерял связь с моделью. Попробуй позже.")
        return
    except Exception as e:
        print(e)

history = []

while True:
    question = input()

    if question.lower() == 'пока':
        break

    history.append(question)
    history_str = '\n'.join(history)

    if 'погода' in question.lower():
        answer = get_weather()

    else:
        answer = ask_agent(question, history_str)

        if not answer:
            continue

    print(f'Ответ: {answer}')
    history.append(answer)
