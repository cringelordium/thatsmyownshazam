#!/bin/bash

# Скрипт для настройки Docker окружения MyShazam

set -e

echo "🐳 Настройка Docker окружения для MyShazam..."

# Создаем необходимые директории
echo "📁 Создание директорий..."
mkdir -p audio_files
mkdir -p data
mkdir -p config

# Устанавливаем права доступа
echo "🔐 Настройка прав доступа..."
chmod 755 audio_files
chmod 755 data
chmod 755 config

# Проверяем наличие Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Установите Docker и попробуйте снова."
    exit 1
fi

# Проверяем наличие Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен. Установите Docker Compose и попробуйте снова."
    exit 1
fi

# Собираем образ
echo "🔨 Сборка Docker образа..."
docker-compose build

# Запускаем тесты
echo "🧪 Запуск тестов..."
docker-compose -f docker-compose.yml -f docker-compose.cli.yml run --rm myshazam-test

echo "✅ Настройка завершена!"
echo ""
echo "🚀 Доступные команды:"
echo "  docker-compose up                    # Запуск GUI приложения"
echo "  docker-compose -f docker-compose.cli.yml up  # Запуск CLI режима"
echo "  docker-compose -f docker-compose.dev.yml up  # Запуск в режиме разработки"
echo "  docker-compose -f docker-compose.prod.yml up # Запуск в продакшене"
echo ""
echo "📁 Поместите аудио файлы в директорию audio_files/"
echo "💾 База данных будет сохранена в директории data/"
