# Используем легковесный образ
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Предотвращаем создание файлов .pyc и включаем немедленный вывод логов
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Устанавливаем зависимости системы (если понадобятся для сборки)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем библиотеки
RUN pip install --no-cache-dir -r requirements.txt

# Копируем скрипт и файл с данными
COPY main.py .
# Если данные в json файле, раскомментируйте строку ниже:
# COPY data.json . 

# Запуск скрипта
CMD ["python", "main.py"]