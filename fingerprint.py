"""
fingerprinting
"""
import numpy as np
import hashlib
from typing import List, Tuple, Dict, Set
from audio_processor import AudioProcessor

class AudioFingerprint:
    """Класс для создания и работы с аудио-отпечатками"""
    
    def __init__(self, target_zone_size: int = 10, target_zone_threshold: float = -40.0):
        """
        Инициализация системы создания отпечатков
        
        Args:
            target_zone_size: Размер целевой зоны для поиска пиков
            target_zone_threshold: Порог для определения значимых пиков
        """
        self.target_zone_size = target_zone_size
        self.target_zone_threshold = target_zone_threshold
        self.audio_processor = AudioProcessor()
    
    def create_fingerprint(self, audio_data: np.ndarray) -> Dict[str, List[Tuple[int, int]]]:
        """
        Создание отпечатка из аудио данных
        
        Args:
            audio_data: Аудио данные
            
        Returns:
            Словарь с хешами и их временными позициями
        """
        # Создаем спектрограмму
        frequencies, times, spectrogram = self.audio_processor.create_spectrogram(audio_data)
        
        # Находим пики
        peaks = self.audio_processor.find_peaks(spectrogram, self.target_zone_threshold)
        
        # Сортируем пики по времени
        peaks.sort(key=lambda x: x[1])  # Сортируем по time_bin
        
        # Создаем отпечатки
        fingerprints = {}
        
        for i, (f1, t1, amp1) in enumerate(peaks):
            # Ищем пики в целевой зоне
            target_peaks = []
            
            for j in range(i + 1, min(i + self.target_zone_size + 1, len(peaks))):
                f2, t2, amp2 = peaks[j]
                
                # Проверяем, что пик находится в целевой зоне
                if t2 - t1 <= self.target_zone_size:
                    target_peaks.append((f2, t2, amp2))
            
            # Создаем хеш для каждого пика в целевой зоне
            for f2, t2, amp2 in target_peaks:
                # Создаем хеш на основе частот и времени
                hash_input = f"{f1}:{f2}:{t2-t1}"
                hash_value = hashlib.md5(hash_input.encode()).hexdigest()
                
                if hash_value not in fingerprints:
                    fingerprints[hash_value] = []
                
                fingerprints[hash_value].append((t1, t2))
        
        return fingerprints
    
    def create_fingerprint_from_file(self, file_path: str) -> Dict[str, List[Tuple[int, int]]]:
        """
        Создание отпечатка из аудио файла
        
        Args:
            file_path: Путь к аудио файлу
            
        Returns:
            Словарь с хешами и их временными позициями
        """
        audio_data = self.audio_processor.load_audio_file(file_path)
        return self.create_fingerprint(audio_data)
    
    def create_fingerprint_from_recording(self, duration: float = 10.0) -> Dict[str, List[Tuple[int, int]]]:
        """
        Создание отпечатка из записи с микрофона
        
        Args:
            duration: Длительность записи в секундах
            
        Returns:
            Словарь с хешами и их временными позициями
        """
        audio_data = self.audio_processor.record_audio(duration)
        return self.create_fingerprint(audio_data)
    
    def compare_fingerprints(self, fingerprint1: Dict[str, List[Tuple[int, int]]], 
                           fingerprint2: Dict[str, List[Tuple[int, int]]]) -> float:
        """
        Сравнение двух отпечатков
        
        Args:
            fingerprint1: Первый отпечаток
            fingerprint2: Второй отпечаток
            
        Returns:
            Коэффициент схожести (0-1)
        """
        # Находим общие хеши
        common_hashes = set(fingerprint1.keys()) & set(fingerprint2.keys())
        
        if not common_hashes:
            return 0.0
        
        # Подсчитываем совпадения с учетом временных сдвигов
        matches = 0
        total_hashes = len(common_hashes)
        
        for hash_value in common_hashes:
            positions1 = fingerprint1[hash_value]
            positions2 = fingerprint2[hash_value]
            
            # Проверяем временные сдвиги
            for t1, t2 in positions1:
                for t3, t4 in positions2:
                    # Если временной сдвиг небольшой, считаем совпадением
                    if abs((t1 - t3) + (t2 - t4)) <= 2:
                        matches += 1
                        break
        
        return matches / total_hashes if total_hashes > 0 else 0.0
    
    def find_best_match(self, query_fingerprint: Dict[str, List[Tuple[int, int]]], 
                       database: Dict[str, Dict[str, List[Tuple[int, int]]]]) -> Tuple[str, float]:
        """
        Поиск лучшего совпадения в базе данных
        
        Args:
            query_fingerprint: Отпечаток запроса
            database: База данных отпечатков {song_name: fingerprint}
            
        Returns:
            Кортеж (название_песни, коэффициент_схожести)
        """
        best_match = None
        best_score = 0.0
        
        for song_name, song_fingerprint in database.items():
            score = self.compare_fingerprints(query_fingerprint, song_fingerprint)
            
            if score > best_score:
                best_score = score
                best_match = song_name
        
        return best_match, best_score
    
    def get_fingerprint_stats(self, fingerprint: Dict[str, List[Tuple[int, int]]]) -> Dict[str, int]:
        """
        Получение статистики отпечатка
        
        Args:
            fingerprint: Отпечаток для анализа
            
        Returns:
            Словарь со статистикой
        """
        total_hashes = len(fingerprint)
        total_positions = sum(len(positions) for positions in fingerprint.values())
        
        return {
            'total_hashes': total_hashes,
            'total_positions': total_positions,
            'average_positions_per_hash': total_positions / total_hashes if total_hashes > 0 else 0
        }

# Пример использования
if __name__ == "__main__":
    fingerprint_system = AudioFingerprint()
    
    # Создаем отпечаток из записи
    print("Создаем отпечаток из записи...")
    fingerprint = fingerprint_system.create_fingerprint_from_recording(duration=5.0)
    
    # Выводим статистику
    stats = fingerprint_system.get_fingerprint_stats(fingerprint)
    print(f"Статистика отпечатка:")
    print(f"  Всего хешей: {stats['total_hashes']}")
    print(f"  Всего позиций: {stats['total_positions']}")
    print(f"  Среднее позиций на хеш: {stats['average_positions_per_hash']:.2f}")
    
    # Показываем первые несколько хешей
    print(f"\nПервые 5 хешей:")
    for i, (hash_value, positions) in enumerate(list(fingerprint.items())[:5]):
        print(f"  {hash_value}: {positions}")
