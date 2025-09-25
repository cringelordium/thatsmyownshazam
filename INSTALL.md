# Установка MyShazam 📦

## Что нужно

- Python 3.7 или новее
- Микрофон
- 100 МБ свободного места

## Установка Python

Если Python не установлен:
- **Windows**: Скачай с [python.org](https://python.org)
- **macOS**: `brew install python3`
- **Linux**: `sudo apt install python3`

## Установка библиотек

```bash
pip install -r requirements.txt
```

Если не работает, попробуй:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Дополнительные библиотеки

### Windows
```bash
pip install pyaudio
```

### macOS
```bash
brew install portaudio
pip install pyaudio
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get install python3-pyaudio
sudo apt-get install portaudio19-dev
pip install pyaudio
```

## Первый запуск

```bash
python main.py
```

## Тестирование

```bash
python test.py
```

## Проблемы и решения

### "No module named 'sounddevice'"
```bash
pip install sounddevice
```

### "No module named 'librosa'"
```bash
pip install librosa
```

### Ошибка с PyAudio на Windows
Скачай готовый файл:
```bash
pip install https://download.lfd.uci.edu/pythonlibs/archived/pyaudio-0.2.11-cp39-cp39-win_amd64.whl
```

### Нет доступа к микрофону
- **Windows**: Настройки → Конфиденциальность → Микрофон
- **macOS**: Системные настройки → Безопасность → Микрофон
- **Linux**: `sudo usermod -a -G audio $USER`

## Готово! 🎉

Теперь можешь запускать MyShazam!