"""
Главный файл для запуска приложения MyShazam
"""
import sys
import os
import argparse
from music_recognizer import MusicRecognizer
from gui import MusicRecognizerGUI

def main():
    """Главная функция"""
    parser = argparse.ArgumentParser(description="MyShazam - Распознавание музыки")
    parser.add_argument("--gui", action="store_true", help="Запустить графический интерфейс")
    parser.add_argument("--add-song", type=str, help="Добавить песню в базу данных")
    parser.add_argument("--recognize", type=str, help="Распознать песню из файла")
    parser.add_argument("--list-songs", action="store_true", help="Показать список песен в базе данных")
    parser.add_argument("--db-path", type=str, default="data/fingerprints.db", help="Путь к базе данных")
    
    args = parser.parse_args()
    
    # Инициализируем систему распознавания
    recognizer = MusicRecognizer(args.db_path)
    
    if args.gui:
        # Запускаем графический интерфейс
        print("Запуск графического интерфейса...")
        app = MusicRecognizerGUI()
        app.run()
    
    elif args.add_song:
        # Добавляем песню
        if not os.path.exists(args.add_song):
            print(f"Ошибка: Файл {args.add_song} не найден")
            return 1
        
        print(f"Добавление песни: {args.add_song}")
        try:
            song_id = recognizer.add_song_to_database(args.add_song)
            print(f"Песня добавлена с ID: {song_id}")
        except Exception as e:
            print(f"Ошибка при добавлении песни: {e}")
            return 1
    
    elif args.recognize:
        # Распознаем песню
        if not os.path.exists(args.recognize):
            print(f"Ошибка: Файл {args.recognize} не найден")
            return 1
        
        print(f"Распознавание песни: {args.recognize}")
        try:
            result = recognizer.recognize_from_file(args.recognize)
            if result:
                name, artist, similarity = result
                print(f"Результат: {name} - {artist} (схожесть: {similarity:.1%})")
            else:
                print("Песня не распознана")
        except Exception as e: # try to another (reminder)
            print(f"Ошибка при распознавании: {e}")
            return 1
    
    elif args.list_songs:
        # Показываем список песен
        try:
            songs = recognizer.list_database_songs()
            if songs:
                print("Песни в базе данных:")
                for song_id, name, artist, file_path, duration in songs:
                    duration_str = f"{duration:.1f}s" if duration else "N/A"
                    print(f"  {song_id}: {name} - {artist} ({duration_str})")
            else:
                print("База данных пуста")
        except Exception as e:
            print(f"Ошибка при получении списка песен: {e}")
            return 1
    
    else:
        # По умолчанию запускаем GUI
        print("Запуск графического интерфейса...")
        app = MusicRecognizerGUI()
        app.run()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
