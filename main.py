import os
import ollama
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

# 1. Настройка окружения
# Исправлено: теперь используем переменные окружения для подключения
QDRANT_HOST = os.getenv("QDRANT_HOST", "172.20.8.1")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://172.20.8.1:11434")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "test")
os.environ["OLLAMA_HOST"] = OLLAMA_HOST

qclient = QdrantClient(host=QDRANT_HOST, port=6333, api_key=QDRANT_API_KEY, https=False)
COLLECTION_NAME = "local_data"

# 2. Создание коллекции
if not qclient.collection_exists(COLLECTION_NAME):
    qclient.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=768, distance=Distance.COSINE)
    )

# 3. Чтение данных из файла
file_path = "local_data"

if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        # Читаем файл построчно и убираем пустые строки
        text_data = [line.strip() for line in f if line.strip()]
    
    print(f"Загрузка {len(text_data)} строк из файла...")

    for i, text in enumerate(text_data):
        try:
            # Получаем вектор
            response = ollama.embeddings(model="nomic-embed-text", prompt=text)
            vector = response['embedding']
            
            # Загружаем в Qdrant
            qclient.upsert(
                collection_name=COLLECTION_NAME,
                points=[
                    PointStruct(id=i, vector=vector, payload={"content": text})
                ]
            )
            print(f"Добавлено: {i}")
        except Exception as e:
            print(f"Ошибка на строке {i}: {e}")
else:
    print(f"Файл {file_path} не найден!")