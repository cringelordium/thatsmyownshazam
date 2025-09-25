# Docker для MyShazam 🐳

## Зачем Docker?

✅ **Простая установка** - одна команда для запуска  
✅ **Работает везде** - одинаково на всех компьютерах  
✅ **Не ломает систему** - изолированная среда  
✅ **Легко удалить** - просто удали контейнер  

## Быстрый старт

### 1. Установка Docker
```bash
# Ubuntu/Debian
sudo apt-get install docker.io docker-compose

# macOS
brew install docker docker-compose

# Windows - скачай Docker Desktop
```

### 2. Запуск
```bash
# Простой запуск
docker compose up

# С пересборкой
docker compose up --build
```

### 3. Готово! 🎉

## Основные команды

### Запуск GUI
```bash
docker compose up
```

### CLI команды
```bash
# Добавить песню
docker compose -f docker-compose.cli.yml run --rm myshazam-add-songs

# Узнать что за песня
docker compose -f docker-compose.cli.yml run --rm myshazam-recognize

# Показать все песни
docker compose -f docker-compose.cli.yml run --rm myshazam-list
```

### Режим разработки
```bash
docker compose -f docker-compose.dev.yml up
```

## Структура файлов

```
Shazam/
├── Dockerfile                 # Образ программы
├── docker-compose.yml         # Основная конфигурация
├── docker-compose.cli.yml     # CLI режим
├── docker-compose.dev.yml     # Режим разработки
├── audio_files/               # Твои аудио файлы
├── data/                      # База данных
└── config/                    # Настройки
```

## Настройки

### Переменные окружения
- `PYTHONPATH=/app` - Путь к Python
- `DB_PATH=/app/data/fingerprints.db` - База данных
- `SAMPLE_RATE=22050` - Качество звука

### Volumes (папки)
- `./audio_files:/app/audio_files` - Аудио файлы
- `./data:/app/data` - База данных
- `./config:/app/config` - Настройки

## Проблемы и решения

### GUI не открывается
```bash
# Разреши X11 forwarding
xhost +local:docker

# Проверь DISPLAY
echo $DISPLAY
```

### Нет звука
```bash
# Проверь аудио устройства
ls -la /dev/snd/

# Проверь права доступа
sudo usermod -a -G audio $USER
```

### Проблемы с папками
```bash
# Проверь права доступа
ls -la audio_files/
ls -la data/

# Создай папки
mkdir -p audio_files data config
```

## Мониторинг

### Логи
```bash
# Смотреть логи
docker compose logs -f

# Логи конкретного сервиса
docker compose logs -f myshazam
```

### Статистика
```bash
# Использование ресурсов
docker stats

# Информация о контейнерах
docker compose ps
```

## Развертывание

### Локально
```bash
docker compose -f docker-compose.prod.yml up -d
```

### В облаке
- Docker Swarm
- Kubernetes
- AWS ECS
- Google Cloud Run

## Готово! 🎉

Теперь MyShazam работает в Docker!