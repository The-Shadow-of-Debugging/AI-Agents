import requests
import httpx

MODEL_NAME = "qwen3.6:35b-a3b"
TEMPERATURE = 0
MAX_TOKENS = 1000
AGENT_MODE = "добрый"

def get_system_prompt():
    if AGENT_MODE == "саркастичный":
        return "Ты саркастичный агент. Отвечай с юмором, используй местный колорит Таганрога"
    else:
        return "Ты добрый агент. Отвечай вежливо с пониманием, не груби и показывай свою готовность помочь"

def get_weather():
    return 'Сегодня +25 и солнечно в Таганроге'

async def ask_agent(question, history):
    try:
        prompt = ' '.join([get_system_prompt(), history, question])
        async with httpx.AsyncClient() as client:
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
            error_msg = "Ой, я потерял связь с моделью. Попробуй позже."
            print(error_msg)
            return error_msg

        if not response or not response.json()["response"]:
            error_msg = "Кажется, я не понял вопрос. Можешь переформулировать?"
            print(error_msg)
            return error_msg

        return response.json()["response"]
    except requests.exceptions.RequestException:
        error_msg = "Ой, я потерял связь с моделью. Попробуй позже."
        print(error_msg)
        return error_msg
    except Exception as e:
        print(e)
        return e
