#!/usr/bin/env python3
"""
Быстрый тест системы MyShazam
"""
import sys
import os

def test_imports():
    """Тест импорта всех модулей"""
    print("Тестирование импорта модулей...")
    
    try:
        import numpy as np
        print("imported numpy")
    except ImportError as e:
        print(f"ERROR numpy: {e}")
        return False
    
    try:
        import scipy
        print("imported scipy")
    except ImportError as e:
        print(f"ERROR scipy: {e}")
        return False
    
    try:
        import librosa
        print("imported librosa")
    except ImportError as e:
        print(f"ERROR librosa: {e}")
        return False
    
    try:
        import sounddevice as sd
        print("✅ sounddevice")
    except ImportError as e:
        print(f"❌ sounddevice: {e}")
        return False
    
    try:
        import matplotlib
        print("✅ matplotlib")
    except ImportError as e:
        print(f"❌ matplotlib: {e}")
        return False
    
    try:
        import sqlite3
        print("✅ sqlite3")
    except ImportError as e:
        print(f"❌ sqlite3: {e}")
        return False
    
    try:
        import tkinter
        print("✅ tkinter")
    except ImportError as e:
        print(f"❌ tkinter: {e}")
        return False
    
    return True

def test_modules():
    """Тест импорта наших модулей"""
    print("\nТестирование наших модулей...")
    
    try:
        from audio_processor import AudioProcessor
        print("✅ audio_processor")
    except ImportError as e:
        print(f"❌ audio_processor: {e}")
        return False
    
    try:
        from fingerprint import AudioFingerprint
        print("✅ fingerprint")
    except ImportError as e:
        print(f"❌ fingerprint: {e}")
        return False
    
    try:
        from database import FingerprintDatabase
        print("✅ database")
    except ImportError as e:
        print(f"❌ database: {e}")
        return False
    
    try:
        from music_recognizer import MusicRecognizer
        print("✅ music_recognizer")
    except ImportError as e:
        print(f"❌ music_recognizer: {e}")
        return False
    
    try:
        from gui import MusicRecognizerGUI
        print("✅ gui")
    except ImportError as e:
        print(f"❌ gui: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Тест базовой функциональности"""
    print("\nТестирование базовой функциональности...")
    
    try:
        from music_recognizer import MusicRecognizer
        recognizer = MusicRecognizer()
        print("✅ Инициализация MusicRecognizer")
        
        stats = recognizer.get_database_stats()
        print(f"✅ Получение статистики: {stats['songs_count']} песен, {stats['fingerprints_count']} отпечатков")
        
        return True
    except Exception as e:
        print(f"❌ Ошибка базовой функциональности: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("=== Тест системы MyShazam ===\n")
    
    # Тест импорта зависимостей
    if not test_imports():
        print("\n❌ Не все зависимости установлены. Установите их командой:")
        print("pip install -r requirements.txt")
        return 1
    
    # Тест импорта наших модулей
    if not test_modules():
        print("\n❌ Ошибки в наших модулях. Проверьте код.")
        return 1
    
    # Тест базовой функциональности
    if not test_basic_functionality():
        print("\n❌ Ошибки в базовой функциональности.")
        return 1
    
    print("\n✅ Все тесты пройдены успешно!")
    print("\nТеперь вы можете:")
    print("1. Запустить GUI: python main.py")
    print("2. Запустить пример: python example.py")
    print("3. Добавить песню: python main.py --add-song 'путь/к/песне.mp3'")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
