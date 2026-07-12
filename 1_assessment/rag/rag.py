from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage

from langgraph.graph import StateGraph, MessagesState, START, END
from sentence_transformers import SentenceTransformer
import faiss
import pickle

# ====== 1. Инициализация ======
# model = ChatOllama(model='qwen2.5:3b')
embedding_model = SentenceTransformer('intfloat/multilingual-e5-small')

def read_text():
    with open('article.txt', 'r', encoding='utf-8') as f:
        text = f.read()

    return text

def split_into_chunks(text, chunk_size=500, overlap_size = 50, min_chunk_size = 100):
    chunk_list = []
    position = 0

    while position < len(text):
        step = chunk_size - overlap_size
        chunk_end = position + chunk_size

        if chunk_end > len(text):
            chunk_end = len(text)

        chunk = text[position:chunk_end]

        if len(chunk) < min_chunk_size and chunk_list:
            # Добавляем к предыдущему чанку
            chunk_list[-1] = chunk_list[-1] + " " + chunk
            print(f"⚠️ Короткий чанк {len(chunk)} символов присоединен к предыдущему")
        else:
            chunk_list.append(chunk)

        position = position + step

    print(f"Всего чанков после обработки: {len(chunk_list)}")
    return chunk_list

def search(query, k=3):
    embedding = embedding_model.encode([query])

    index = faiss.read_index("my_index.faiss")

    distances, indices = index.search(embedding.astype('float32'), k)

    with open('chunks.pkl', 'rb') as f:
        chunks = pickle.load(f)

    print(f"\n🔍 Поиск: '{query}'")
    print("=" * 60)

    for i, (idx, dist) in enumerate(zip(indices[0], distances[0])):
        if idx != -1:  # -1 означает, что результат не найден
            print(f"\n{i + 1}. [Расстояние: {dist:.4f}]")
            print(f"   Чанк #{idx}")
            print(f"   Текст: {chunks[idx][:200]}...")

    return distances, indices, chunks


# Читаем файл
text = read_text()

# Разбиваем на чанки
chunks = split_into_chunks(text)
embeddings = embedding_model.encode(chunks)

dimension = embeddings.shape[1]  # 384
index = faiss.IndexFlatL2(dimension)

# Добавляем векторы (FAISS требует float32)
index.add(embeddings.astype('float32'))

print(f"Векторов в индексе: {index.ntotal}")

# Сохраняем индекс и чанки
faiss.write_index(index, 'my_index.faiss')

with open('chunks.pkl', 'wb') as f:
    pickle.dump(chunks, f)

print("Индекс и чанки сохранены")


# Тестируем поиск
search("трансформеры архитектура")
search("обучение нейросетей")
search("внимание механизм")