"""
обработка аудио и создание спектрограмм
"""
import numpy as np
import librosa
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy import signal
from typing import Tuple, List

class AudioProcessor:
    """Класс для обработки аудио сигналов"""
    
    def __init__(self, sample_rate: int = 22050):
        """
   
        args:
            sample_rate: Частота дискретизации (по умолчанию 22050 Гц)
        """
        self.sample_rate = sample_rate
        
    def record_audio(self, duration: float = 10.0) -> np.ndarray:
        """
        Запись аудио с микрофона
        
        Args:
            duration: Длительность записи в секундах
            
        Returns:
            numpy array с аудио данными
        """
        print(f"Записываем аудио {duration} секунд...")
        audio_data = sd.rec(
            int(duration * self.sample_rate), 
            samplerate=self.sample_rate, 
            channels=1, 
            dtype='float64'
        )
        sd.wait()  # Ждем завершения записи
        print("Запись завершена!")
        return audio_data.flatten()
    
    def load_audio_file(self, file_path: str) -> np.ndarray:
        """
        Загрузка аудио файла
        
        Args:
            file_path: Путь к аудио файлу
            
        Returns:
            numpy array с аудио данными
        """
        audio_data, _ = librosa.load(file_path, sr=self.sample_rate)
        return audio_data
    
    def create_spectrogram(self, audio_data: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Создание спектрограммы из аудио данных
        
        Args:
            audio_data: Аудио данные
            
        Returns:
            Кортеж (frequencies, times, spectrogram)
        """
        # Используем STFT (Short-Time Fourier Transform)
        frequencies, times, spectrogram = signal.spectrogram(
            audio_data,
            fs=self.sample_rate,
            nperseg=1024,  # Размер окна
            noverlap=512,  # Перекрытие окон
            window='hann'
        )
        
        # Преобразуем в децибелы для лучшей визуализации
        spectrogram_db = 10 * np.log10(spectrogram + 1e-10)
        
        return frequencies, times, spectrogram_db
    
    def find_peaks(self, spectrogram: np.ndarray, threshold: float = -40.0) -> List[Tuple[int, int, float]]:
        """
        Поиск пиков в спектрограмме
        
        Args:
            spectrogram: Спектрограмма
            threshold: Порог для определения пиков
            
        Returns:
            Список кортежей (frequency_bin, time_bin, amplitude)
        """
        peaks = []
        
        # Ищем локальные максимумы
        for t in range(1, spectrogram.shape[1] - 1):
            for f in range(1, spectrogram.shape[0] - 1):
                current = spectrogram[f, t]
                
                # Проверяем, является ли точка локальным максимумом
                if (current > threshold and 
                    current > spectrogram[f-1, t] and 
                    current > spectrogram[f+1, t] and
                    current > spectrogram[f, t-1] and 
                    current > spectrogram[f, t+1]):
                    peaks.append((f, t, current))
        
        return peaks
    
    def visualize_spectrogram(self, frequencies: np.ndarray, times: np.ndarray, 
                            spectrogram: np.ndarray, peaks: List[Tuple[int, int, float]] = None):
        """
        Визуализация спектрограммы
        
        Args:
            frequencies: Массив частот
            times: Массив времен
            spectrogram: Спектрограмма
            peaks: Список пиков для отображения
        """
        plt.figure(figsize=(12, 8))
        
        # Отображаем спектрограмму
        plt.pcolormesh(times, frequencies, spectrogram, shading='gouraud')
        plt.colorbar(label='Амплитуда (дБ)')
        
        # Отмечаем пики, если они есть
        if peaks:
            peak_freqs = [frequencies[f] for f, t, _ in peaks]
            peak_times = [times[t] for f, t, _ in peaks]
            plt.scatter(peak_times, peak_freqs, c='red', s=20, alpha=0.7, label='Пики')
            plt.legend()
        
        plt.xlabel('Время (с)')
        plt.ylabel('Частота (Гц)')
        plt.title('Спектрограмма с выделенными пиками')
        plt.yscale('log')
        plt.show()

# Пример использования
if __name__ == "__main__":
    processor = AudioProcessor()
    
    # Записываем аудио
    audio = processor.record_audio(duration=5.0)
    
    # Создаем спектрограмму
    freqs, times, spec = processor.create_spectrogram(audio)
    
    # Находим пики
    peaks = processor.find_peaks(spec)
    
    print(f"Найдено {len(peaks)} пиков")
    
    # Визуализируем результат
    processor.visualize_spectrogram(freqs, times, spec, peaks)
