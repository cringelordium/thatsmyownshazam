"""
Модуль для работы с базой данных отпечатков
"""
import sqlite3
import json
import os
import numpy as np
from typing import Dict, List, Tuple, Optional
from fingerprint import AudioFingerprint

class FingerprintDatabase:
    """Класс для работы с базой данных отпечатков"""
    
    def __init__(self, db_path: str = "fingerprints.db"):
        """
        Инициализация базы данных
        
        Args:
            db_path: Путь к файлу базы данных
        """
        self.db_path = db_path
        self.fingerprint_system = AudioFingerprint()
        self.init_database()
    
    def init_database(self):
        """Инициализация структуры базы данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Создаем таблицу для песен
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                artist TEXT,
                file_path TEXT,
                duration REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Создаем таблицу для отпечатков
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fingerprints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                song_id INTEGER,
                hash_value TEXT NOT NULL,
                time_offset INTEGER,
                frequency_bin INTEGER,
                FOREIGN KEY (song_id) REFERENCES songs (id)
            )
        ''')
        
        # Создаем индексы для быстрого поиска
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_hash ON fingerprints (hash_value)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_song_id ON fingerprints (song_id)')
        
        conn.commit()
        conn.close()
    
    def add_song(self, name: str, artist: str = None, file_path: str = None, 
                 duration: float = None) -> int:
        """
        Добавление песни в базу данных
        
        Args:
            name: Название песни
            artist: Исполнитель
            file_path: Путь к файлу
            duration: Длительность в секундах
            
        Returns:
            ID добавленной песни
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO songs (name, artist, file_path, duration)
            VALUES (?, ?, ?, ?)
        ''', (name, artist, file_path, duration))
        
        song_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return song_id
    
    def add_fingerprint(self, song_id: int, fingerprint: Dict[str, List[Tuple[int, int]]]):
        """
        Добавление отпечатка в базу данных
        
        Args:
            song_id: ID песни
            fingerprint: Отпечаток песни
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Подготавливаем данные для вставки
        fingerprint_data = []
        for hash_value, positions in fingerprint.items():
            for time_offset, frequency_bin in positions:
                fingerprint_data.append((song_id, hash_value, time_offset, frequency_bin))
        
        # Вставляем данные пакетами
        cursor.executemany('''
            INSERT INTO fingerprints (song_id, hash_value, time_offset, frequency_bin)
            VALUES (?, ?, ?, ?)
        ''', fingerprint_data)
        
        conn.commit()
        conn.close()
    
    def add_song_with_fingerprint(self, name: str, audio_data: np.ndarray, 
                                 artist: str = None, file_path: str = None) -> int:
        """
        Добавление песни с автоматическим созданием отпечатка
        
        Args:
            name: Название песни
            audio_data: Аудио данные
            artist: Исполнитель
            file_path: Путь к файлу
            
        Returns:
            ID добавленной песни
        """
        # Создаем отпечаток
        fingerprint = self.fingerprint_system.create_fingerprint(audio_data)
        
        # Добавляем песню
        song_id = self.add_song(name, artist, file_path)
        
        # Добавляем отпечаток
        self.add_fingerprint(song_id, fingerprint)
        
        return song_id
    
    def add_song_from_file(self, file_path: str, name: str = None, artist: str = None) -> int:
        """
        Добавление песни из файла
        
        Args:
            file_path: Путь к аудио файлу
            name: Название песни (если не указано, берется из имени файла)
            artist: Исполнитель
            
        Returns:
            ID добавленной песни
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")
        
        if name is None:
            name = os.path.splitext(os.path.basename(file_path))[0]
        
        # Загружаем аудио
        audio_data = self.fingerprint_system.audio_processor.load_audio_file(file_path)
        
        return self.add_song_with_fingerprint(name, audio_data, artist, file_path)
    
    def search_song(self, query_fingerprint: Dict[str, List[Tuple[int, int]]], 
                   threshold: float = 0.1) -> List[Tuple[str, str, float]]:
        """
        Поиск песни по отпечатку
        
        Args:
            query_fingerprint: Отпечаток запроса
            threshold: Минимальный порог схожести
            
        Returns:
            Список кортежей (название, исполнитель, коэффициент_схожести)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Получаем все хеши из запроса
        query_hashes = set(query_fingerprint.keys())
        
        if not query_hashes:
            return []
        
        # Создаем плейсхолдеры для SQL запроса
        placeholders = ','.join(['?' for _ in query_hashes])
        
        # Ищем совпадающие хеши
        cursor.execute(f'''
            SELECT DISTINCT s.id, s.name, s.artist, f.hash_value, f.time_offset
            FROM songs s
            JOIN fingerprints f ON s.id = f.song_id
            WHERE f.hash_value IN ({placeholders})
        ''', list(query_hashes))
        
        results = cursor.fetchall()
        conn.close()
        
        # Группируем результаты по песням
        song_matches = {}
        for song_id, name, artist, hash_value, time_offset in results:
            if song_id not in song_matches:
                song_matches[song_id] = {
                    'name': name,
                    'artist': artist,
                    'matches': 0,
                    'total_hashes': 0
                }
            
            song_matches[song_id]['matches'] += 1
        
        # Подсчитываем общее количество хешей для каждой песни
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for song_id in song_matches.keys():
            cursor.execute('SELECT COUNT(*) FROM fingerprints WHERE song_id = ?', (song_id,))
            total_hashes = cursor.fetchone()[0]
            song_matches[song_id]['total_hashes'] = total_hashes
        
        conn.close()
        
        # Вычисляем коэффициенты схожести
        matches = []
        for song_id, data in song_matches.items():
            similarity = data['matches'] / len(query_hashes)
            if similarity >= threshold:
                matches.append((data['name'], data['artist'], similarity))
        
        # Сортируем по убыванию схожести
        matches.sort(key=lambda x: x[2], reverse=True)
        
        return matches
    
    def get_song_count(self) -> int:
        """Получение количества песен в базе данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM songs')
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def get_fingerprint_count(self) -> int:
        """Получение количества отпечатков в базе данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM fingerprints')
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def list_songs(self) -> List[Tuple[int, str, str, str, float]]:
        """
        Получение списка всех песен
        
        Returns:
            Список кортежей (id, название, исполнитель, путь_к_файлу, длительность)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, artist, file_path, duration FROM songs ORDER BY name')
        songs = cursor.fetchall()
        conn.close()
        return songs
    
    def delete_song(self, song_id: int):
        """
        Удаление песни из базы данных
        
        Args:
            song_id: ID песни для удаления
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Удаляем отпечатки
        cursor.execute('DELETE FROM fingerprints WHERE song_id = ?', (song_id,))
        
        # Удаляем песню
        cursor.execute('DELETE FROM songs WHERE id = ?', (song_id,))
        
        conn.commit()
        conn.close()
    
    def clear_database(self):
        """Очистка всей базы данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM fingerprints')
        cursor.execute('DELETE FROM songs')
        
        conn.commit()
        conn.close()

# Пример использования
if __name__ == "__main__":
    db = FingerprintDatabase()
    
    print(f"Песен в базе: {db.get_song_count()}")
    print(f"Отпечатков в базе: {db.get_fingerprint_count()}")
    
    # Показываем список песен
    songs = db.list_songs()
    if songs:
        print("\nПесни в базе данных:")
        for song_id, name, artist, file_path, duration in songs:
            print(f"  {song_id}: {name} - {artist} ({duration}s)")
    else:
        print("База данных пуста")
