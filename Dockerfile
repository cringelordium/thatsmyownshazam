# Используем официальный Python образ
FROM python:3.11-slim

# Устанавливаем системные зависимости для аудио
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    libasound2-dev \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Создаем директорию для базы данных
RUN mkdir -p /app/data

# Устанавливаем переменные окружения
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Открываем порт для веб-интерфейса (если будет добавлен)
EXPOSE 8000

# Команда по умолчанию
CMD ["python", "main.py"]
