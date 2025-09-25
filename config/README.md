# Конфигурация

Эта директория содержит файлы конфигурации MyShazam.

## Файлы конфигурации

### `config.yaml` (опционально)
```yaml
# Настройки аудио
audio:
  sample_rate: 22050
  target_zone_size: 10
  target_zone_threshold: 0.1

# Настройки базы данных
database:
  path: "data/fingerprints.db"
  backup_interval: 3600  # секунды

# Настройки GUI
gui:
  window_size: "600x500"
  default_duration: 10
  max_duration: 30

# Настройки логирования
logging:
  level: "INFO"
  file: "logs/myshazam.log"
```

### `logging.conf` (опционально)
```ini
[loggers]
keys=root,myshazam

[handlers]
keys=consoleHandler,fileHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=INFO
handlers=consoleHandler

[logger_myshazam]
level=DEBUG
handlers=consoleHandler,fileHandler
qualname=myshazam
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=INFO
formatter=simpleFormatter
args=(sys.stdout,)

[handler_fileHandler]
class=FileHandler
level=DEBUG
formatter=simpleFormatter
args=('logs/myshazam.log',)

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
datefmt=%Y-%m-%d %H:%M:%S
```

## Переменные окружения

### Основные
- `MYSHAM_DEBUG=1` - Включить отладку
- `MYSHAM_LOG_LEVEL=DEBUG` - Уровень логирования
- `MYSHAM_DB_PATH=data/fingerprints.db` - Путь к базе данных

### Настройки аудио
- `MYSHAM_SAMPLE_RATE=22050` - Частота дискретизации
- `MYSHAM_TARGET_ZONE_SIZE=10` - Размер целевой зоны
- `MYSHAM_TARGET_ZONE_THRESHOLD=0.1` - Порог для пиков

### Настройки GUI
- `MYSHAM_WINDOW_SIZE=600x500` - Размер окна
- `MYSHAM_DEFAULT_DURATION=10` - Длительность записи по умолчанию

## Использование

### Загрузка конфигурации
```python
import yaml
import os

def load_config():
    config_path = os.path.join('config', 'config.yaml')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    return {}

config = load_config()
```

### Переменные окружения
```python
import os

# Получение настроек из переменных окружения
debug = os.getenv('MYSHAM_DEBUG', '0') == '1'
log_level = os.getenv('MYSHAM_LOG_LEVEL', 'INFO')
db_path = os.getenv('MYSHAM_DB_PATH', 'data/fingerprints.db')
```

## Примеры

### Создание конфигурации
```bash
# Создание базовой конфигурации
cat > config/config.yaml << EOF
audio:
  sample_rate: 22050
  target_zone_size: 10
  target_zone_threshold: 0.1

database:
  path: "data/fingerprints.db"
  backup_interval: 3600

gui:
  window_size: "600x500"
  default_duration: 10
  max_duration: 30

logging:
  level: "INFO"
  file: "logs/myshazam.log"
EOF
```

### Настройка логирования
```bash
# Создание директории для логов
mkdir -p logs

# Создание конфигурации логирования
cat > config/logging.conf << EOF
[loggers]
keys=root,myshazam

[handlers]
keys=consoleHandler,fileHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=INFO
handlers=consoleHandler

[logger_myshazam]
level=DEBUG
handlers=consoleHandler,fileHandler
qualname=myshazam
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=INFO
formatter=simpleFormatter
args=(sys.stdout,)

[handler_fileHandler]
class=FileHandler
level=DEBUG
formatter=simpleFormatter
args=('logs/myshazam.log',)

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
datefmt=%Y-%m-%d %H:%M:%S
EOF
```
