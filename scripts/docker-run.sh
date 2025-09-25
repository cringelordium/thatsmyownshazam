#!/bin/bash

# Скрипт для запуска MyShazam в Docker

set -e

# Функция для показа помощи
show_help() {
    echo "🐳 MyShazam Docker Runner"
    echo ""
    echo "Использование: $0 [КОМАНДА]"
    echo ""
    echo "Команды:"
    echo "  gui        Запуск GUI приложения"
    echo "  cli        Запуск CLI режима"
    echo "  dev        Запуск в режиме разработки"
    echo "  prod       Запуск в продакшене"
    echo "  test       Запуск тестов"
    echo "  example    Запуск примера"
    echo "  add        Добавление песен из audio_files/"
    echo "  recognize  Распознавание песен из audio_files/"
    echo "  list       Показать список песен"
    echo "  stop       Остановить все сервисы"
    echo "  clean      Очистить все контейнеры и образы"
    echo "  help       Показать эту помощь"
    echo ""
    echo "Примеры:"
    echo "  $0 gui     # Запуск GUI"
    echo "  $0 cli     # Запуск CLI"
    echo "  $0 test    # Запуск тестов"
}

# Функция для запуска GUI
run_gui() {
    echo "🎵 Запуск MyShazam GUI..."
    docker-compose -f docker-compose.yml -f docker-compose.gui.yml up
}

# Функция для запуска CLI
run_cli() {
    echo "🎵 Запуск MyShazam CLI..."
    docker-compose -f docker-compose.yml -f docker-compose.cli.yml up
}

# Функция для запуска в режиме разработки
run_dev() {
    echo "🎵 Запуск MyShazam в режиме разработки..."
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
}

# Функция для запуска в продакшене
run_prod() {
    echo "🎵 Запуск MyShazam в продакшене..."
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
}

# Функция для запуска тестов
run_test() {
    echo "🧪 Запуск тестов..."
    docker-compose -f docker-compose.yml -f docker-compose.cli.yml run --rm myshazam-test
}

# Функция для запуска примера
run_example() {
    echo "📚 Запуск примера..."
    docker-compose -f docker-compose.yml -f docker-compose.cli.yml run --rm myshazam-example
}

# Функция для добавления песен
run_add() {
    echo "➕ Добавление песен..."
    docker-compose -f docker-compose.yml -f docker-compose.cli.yml run --rm myshazam-add-songs
}

# Функция для распознавания
run_recognize() {
    echo "🔍 Распознавание песен..."
    docker-compose -f docker-compose.yml -f docker-compose.cli.yml run --rm myshazam-recognize
}

# Функция для показа списка песен
run_list() {
    echo "📋 Список песен..."
    docker-compose -f docker-compose.yml -f docker-compose.cli.yml run --rm myshazam-list
}

# Функция для остановки сервисов
run_stop() {
    echo "⏹️ Остановка сервисов..."
    docker-compose down
    docker-compose -f docker-compose.yml -f docker-compose.gui.yml down
    docker-compose -f docker-compose.yml -f docker-compose.cli.yml down
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml down
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml down
}

# Функция для очистки
run_clean() {
    echo "🧹 Очистка Docker..."
    docker-compose down --rmi all --volumes --remove-orphans
    docker system prune -f
}

# Основная логика
case "${1:-help}" in
    gui)
        run_gui
        ;;
    cli)
        run_cli
        ;;
    dev)
        run_dev
        ;;
    prod)
        run_prod
        ;;
    test)
        run_test
        ;;
    example)
        run_example
        ;;
    add)
        run_add
        ;;
    recognize)
        run_recognize
        ;;
    list)
        run_list
        ;;
    stop)
        run_stop
        ;;
    clean)
        run_clean
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "❌ Неизвестная команда: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
