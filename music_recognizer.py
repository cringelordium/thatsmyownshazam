"""
модуль для распознавания музыки
"""
import numpy as np
from typing import List, Tuple, Optional, Dict
from audio_processor import AudioProcessor
from fingerprint import AudioFingerprint
from database import FingerprintDatabase

class MusicRecognizer:
    def __init__(self, db_path: str = "data/fingerprints.db"):
        """
        Инициализация системы распознавания
        
        Args:
            db_path: Путь к базе данных отпечатков
        """
        self.audio_processor = AudioProcessor()
        self.fingerprint_system = AudioFingerprint()
        self.database = FingerprintDatabase(db_path)
        
    def recognize_from_recording(self, duration: float = 10.0, 
                                threshold: float = 0.1) -> Optional[Tuple[str, str, float]]:
        """
        Распознавание музыки из записи с микрофона
        
        Args:
            duration: Длительность записи в секундах
            threshold: Минимальный порог схожести
            
        Returns:
            Кортеж (название, исполнитель, коэффициент_схожести) или None
        """
        print(f"Записываем аудио {duration} секунд...")
        
        # Записываем аудио
        audio_data = self.audio_processor.record_audio(duration)
        
        # Создаем отпечаток
        fingerprint = self.fingerprint_system.create_fingerprint(audio_data)
        
        # Ищем в базе данных
        matches = self.database.search_song(fingerprint, threshold)
        
        if matches:
            name, artist, similarity = matches[0]
            return name, artist, similarity
        
        return None
    
    def recognize_from_file(self, file_path: str, 
                           threshold: float = 0.1) -> Optional[Tuple[str, str, float]]:
        """
        Распознавание музыки из файла
        
        Args:
            file_path: Путь к аудио файлу
            threshold: Минимальный порог схожести
            
        Returns:
            Кортеж (название, исполнитель, коэффициент_схожести) или None
        """
        # Загружаем аудио
        audio_data = self.audio_processor.load_audio_file(file_path)
        
        # Создаем отпечаток
        fingerprint = self.fingerprint_system.create_fingerprint(audio_data)
        
        # Ищем в базе данных
        matches = self.database.search_song(fingerprint, threshold)
        
        if matches:
            name, artist, similarity = matches[0]
            return name, artist, similarity
        
        return None
    
    def recognize_from_audio_data(self, audio_data: np.ndarray, 
                                 threshold: float = 0.1) -> Optional[Tuple[str, str, float]]:
        """
        Распознавание музыки из аудио данных
        
        Args:
            audio_data: Аудио данные
            threshold: Минимальный порог схожести
            
        Returns:
            Кортеж (название, исполнитель, коэффициент_схожести) или None
        """
        # Создаем отпечаток
        fingerprint = self.fingerprint_system.create_fingerprint(audio_data)
        
        # Ищем в базе данных
        matches = self.database.search_song(fingerprint, threshold)
        
        if matches:
            name, artist, similarity = matches[0]
            return name, artist, similarity
        
        return None
    
    def add_song_to_database(self, file_path: str, name: str = None, artist: str = None) -> int:
        """
        Добавление песни в базу данных
        
        Args:
            file_path: Путь к аудио файлу
            name: Название песни
            artist: Исполнитель
            
        Returns:
            ID добавленной песни
        """
        return self.database.add_song_from_file(file_path, name, artist)
    
    def get_database_stats(self) -> Dict[str, int]:
        """
        Получение статистики базы данных
        
        Returns:
            Словарь со статистикой
        """
        return {
            'songs_count': self.database.get_song_count(),
            'fingerprints_count': self.database.get_fingerprint_count()
        }
    
    def list_database_songs(self) -> List[Tuple[int, str, str, str, float]]:
        """
        Получение списка песен в базе данных
        
        Returns:
            Список кортежей (id, название, исполнитель, путь_к_файлу, длительность)
        """
        return self.database.list_songs()
    
    def search_with_multiple_results(self, audio_data: np.ndarray, 
                                   threshold: float = 0.05, 
                                   max_results: int = 5) -> List[Tuple[str, str, float]]:
        """
        Поиск с возвратом нескольких результатов
        
        Args:
            audio_data: Аудио данные
            threshold: Минимальный порог схожести
            max_results: Максимальное количество результатов
            
        Returns:
            Список кортежей (название, исполнитель, коэффициент_схожести)
        """
        # Создаем отпечаток
        fingerprint = self.fingerprint_system.create_fingerprint(audio_data)
        
        # Ищем в базе данных
        matches = self.database.search_song(fingerprint, threshold)
        
        return matches[:max_results]
    
    def analyze_audio_quality(self, audio_data: np.ndarray) -> Dict[str, float]:
        """
        Анализ качества аудио
        
        Args:
            audio_data: Аудио данные
            
        Returns:
            Словарь с метриками качества
        """
        # Вычисляем RMS (Root Mean Square) - средняя мощность сигнала
        rms = np.sqrt(np.mean(audio_data**2))
        
        # Вычисляем SNR (Signal-to-Noise Ratio) - отношение сигнал/шум
        # Простая оценка: считаем, что шум - это низкоамплитудные компоненты
        signal_power = np.mean(audio_data**2)
        noise_threshold = 0.01
        noise_mask = np.abs(audio_data) < noise_threshold
        noise_power = np.mean(audio_data[noise_mask]**2) if np.any(noise_mask) else 0.001
        snr = 10 * np.log10(signal_power / noise_power) if noise_power > 0 else 100
        
        # Вычисляем динамический диапазон
        dynamic_range = 20 * np.log10(np.max(np.abs(audio_data)) / (np.mean(np.abs(audio_data)) + 1e-10))
        
        return {
            'rms': rms,
            'snr_db': snr,
            'dynamic_range_db': dynamic_range,
            'max_amplitude': np.max(np.abs(audio_data))
        }
    
    def get_recognition_confidence(self, audio_data: np.ndarray, 
                                  threshold: float = 0.1) -> Dict[str, float]:
        """
        Получение уверенности в распознавании
        
        Args:
            audio_data: Аудио данные
            threshold: Минимальный порог схожести
            
        Returns:
            Словарь с метриками уверенности
        """
        # Создаем отпечаток
        fingerprint = self.fingerprint_system.create_fingerprint(audio_data)
        
        # Получаем статистику отпечатка
        fingerprint_stats = self.fingerprint_system.get_fingerprint_stats(fingerprint)
        
        # Ищем в базе данных
        matches = self.database.search_song(fingerprint, threshold)
        
        # Анализируем качество аудио
        quality_metrics = self.analyze_audio_quality(audio_data)
        
        confidence_metrics = {
            'fingerprint_quality': fingerprint_stats['total_hashes'] / 1000.0,  # Нормализуем
            'audio_quality': min(quality_metrics['snr_db'] / 20.0, 1.0),  # Нормализуем SNR
            'best_match_similarity': matches[0][2] if matches else 0.0,
            'matches_count': len(matches)
        }
        
        # Общая уверенность
        confidence_metrics['overall_confidence'] = (
            confidence_metrics['fingerprint_quality'] * 0.3 +
            confidence_metrics['audio_quality'] * 0.3 +
            confidence_metrics['best_match_similarity'] * 0.4
        )
        
        return confidence_metrics

# Пример использования
if __name__ == "__main__":
    recognizer = MusicRecognizer()
    
    # Показываем статистику базы данных
    stats = recognizer.get_database_stats()
    print(f"Статистика базы данных:")
    print(f"  Песен: {stats['songs_count']}")
    print(f"  Отпечатков: {stats['fingerprints_count']}")
    
    # Если база пуста, добавляем тестовую песню
    if stats['songs_count'] == 0:
        print("\nБаза данных пуста. Добавьте песни для тестирования.")
        print("Пример: recognizer.add_song_to_database('path/to/song.mp3', 'Song Name', 'Artist')")
    else:
        # Показываем список песен
        songs = recognizer.list_database_songs()
        print(f"\nПесни в базе данных:")
        for song_id, name, artist, file_path, duration in songs:
            print(f"  {name} - {artist}")
        
        # Тестируем распознавание
        print(f"\nТестируем распознавание...")
        result = recognizer.recognize_from_recording(duration=5.0)
        
        if result:
            name, artist, similarity = result
            print(f"Распознано: {name} - {artist} (схожесть: {similarity:.2%})")
        else:
            print("Песня не распознана")
