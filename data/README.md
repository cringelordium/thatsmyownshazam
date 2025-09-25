# База данных

Эта директория содержит базу данных MyShazam.

## Файлы

- **fingerprints.db** - SQLite база данных с отпечатками песен
- **backup/** - Резервные копии базы данных

## Структура базы данных

### Таблица `songs`
- `id` - Уникальный идентификатор песни
- `name` - Название песни
- `artist` - Исполнитель
- `file_path` - Путь к файлу
- `duration` - Длительность в секундах
- `created_at` - Дата создания

### Таблица `fingerprints`
- `id` - Уникальный идентификатор отпечатка
- `song_id` - ID песни
- `hash_value` - MD5 хеш отпечатка
- `time_offset` - Временное смещение
- `frequency_bin` - Частотный бин

## Резервное копирование

```bash
# Создание резервной копии
cp fingerprints.db backup/fingerprints_$(date +%Y%m%d_%H%M%S).db

# Восстановление из резервной копии
cp backup/fingerprints_20240101_120000.db fingerprints.db
```

## Мониторинг

```bash
# Размер базы данных
ls -lh fingerprints.db

# Количество записей
sqlite3 fingerprints.db "SELECT COUNT(*) FROM songs;"
sqlite3 fingerprints.db "SELECT COUNT(*) FROM fingerprints;"
```

## Очистка

```bash
# Очистка базы данных
python -c "
from database import FingerprintDatabase
db = FingerprintDatabase('data/fingerprints.db')
db.clear_database()
print('База данных очищена')
"
```
