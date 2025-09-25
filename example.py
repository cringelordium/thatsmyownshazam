"""
Пример использования MyShazam
"""
import numpy as np
from music_recognizer import MusicRecognizer

def create_test_audio():
    """Создание тестового аудио сигнала"""
    # Создаем простой синусоидальный сигнал
    sample_rate = 22050
    duration = 5.0
    frequency = 440  # Ля первой октавы
    
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio = np.sin(2 * np.pi * frequency * t)
    
    # Добавляем немного шума для реалистичности
    noise = np.random.normal(0, 0.1, len(audio))
    audio = audio + noise
    
    return audio

def main():
    """Основная функция примера"""
    print("=== MyShazam - Пример использования ===\n")
    
    # Инициализируем систему распознавания
    recognizer = MusicRecognizer()
    
    # Показываем статистику базы данных
    stats = recognizer.get_database_stats()
    print(f"Статистика базы данных:")
    print(f"  Песен: {stats['songs_count']}")
    print(f"  Отпечатков: {stats['fingerprints_count']}\n")
    
    if stats['songs_count'] == 0:
        print("База данных пуста. Создаем тестовую песню...")
        
        # Создаем тестовое аудио
        test_audio = create_test_audio()
        
        # Добавляем в базу данных
        song_id = recognizer.add_song_to_database(
            "test_audio.wav",  # Виртуальный путь
            "Тестовая песня",
            "Тестовый исполнитель"
        )
        
        print(f"Тестовая песня добавлена с ID: {song_id}")
        
        # Обновляем статистику
        stats = recognizer.get_database_stats()
        print(f"Новая статистика:")
        print(f"  Песен: {stats['songs_count']}")
        print(f"  Отпечатков: {stats['fingerprints_count']}\n")
    
    # Показываем список песен
    songs = recognizer.list_database_songs()
    print("Песни в базе данных:")
    for song_id, name, artist, file_path, duration in songs:
        print(f"  {song_id}: {name} - {artist}")
    
    print("\n=== Тестирование распознавания ===")
    
    # Создаем тестовое аудио для распознавания
    test_audio = create_test_audio()
    
    # Тестируем распознавание
    print("Тестируем распознавание...")
    result = recognizer.recognize_from_audio_data(test_audio)
    
    if result:
        name, artist, similarity = result
        print(f"✅ Распознано: {name} - {artist}")
        print(f"   Схожесть: {similarity:.1%}")
    else:
        print("❌ Песня не распознана")
    
    # Получаем метрики уверенности
    print("\n=== Анализ качества ===")
    confidence = recognizer.get_recognition_confidence(test_audio)
    print(f"Уверенность в распознавании: {confidence['overall_confidence']:.1%}")
    print(f"Качество отпечатка: {confidence['fingerprint_quality']:.1%}")
    print(f"Качество аудио: {confidence['audio_quality']:.1%}")
    
    # Анализируем качество аудио
    quality = recognizer.analyze_audio_quality(test_audio)
    print(f"\nМетрики качества аудио:")
    print(f"  RMS: {quality['rms']:.4f}")
    print(f"  SNR: {quality['snr_db']:.1f} дБ")
    print(f"  Динамический диапазон: {quality['dynamic_range_db']:.1f} дБ")
    
    print("\n=== Пример завершен ===")

if __name__ == "__main__":
    main()
