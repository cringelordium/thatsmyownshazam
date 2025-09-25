"""
Графический пользовательский интерфейс для приложения распознавания музыки
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from typing import Optional, Tuple
from music_recognizer import MusicRecognizer

class MusicRecognizerGUI:
    """Графический интерфейс для распознавания музыки"""
    
    def __init__(self):
        """Инициализация GUI"""
        self.root = tk.Tk()
        self.root.title("MyShazam - Распознавание музыки")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Инициализируем систему распознавания
        self.recognizer = MusicRecognizer()
        
        # Переменные для состояния
        self.is_recording = False
        self.recording_thread = None
        
        self.setup_ui()
        self.update_database_info()
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Создаем главный фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настраиваем растягивание
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="MyShazam", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Информация о базе данных
        db_frame = ttk.LabelFrame(main_frame, text="База данных", padding="10")
        db_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        db_frame.columnconfigure(1, weight=1)
        
        self.db_info_label = ttk.Label(db_frame, text="Загрузка...")
        self.db_info_label.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Кнопки управления базой данных
        ttk.Button(db_frame, text="Добавить песню", command=self.add_song_dialog).grid(row=1, column=0, padx=(0, 5))
        ttk.Button(db_frame, text="Показать песни", command=self.show_songs_dialog).grid(row=1, column=1, padx=(5, 0))
        
        # Распознавание музыки
        recognition_frame = ttk.LabelFrame(main_frame, text="Распознавание музыки", padding="10")
        recognition_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        recognition_frame.columnconfigure(1, weight=1)
        
        # Кнопка записи
        self.record_button = ttk.Button(recognition_frame, text="🎤 Записать и распознать", 
                                       command=self.toggle_recording)
        self.record_button.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Кнопка загрузки файла
        ttk.Button(recognition_frame, text="📁 Загрузить файл", 
                  command=self.recognize_from_file).grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        # Настройки записи
        settings_frame = ttk.Frame(recognition_frame)
        settings_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        settings_frame.columnconfigure(1, weight=1)
        
        ttk.Label(settings_frame, text="Длительность записи:").grid(row=0, column=0, sticky=tk.W)
        self.duration_var = tk.StringVar(value="10")
        duration_spinbox = ttk.Spinbox(settings_frame, from_=5, to=30, width=10, 
                                      textvariable=self.duration_var)
        duration_spinbox.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        ttk.Label(settings_frame, text="сек").grid(row=0, column=2, sticky=tk.W, padx=(5, 0))
        
        # Результат распознавания
        result_frame = ttk.LabelFrame(main_frame, text="Результат", padding="10")
        result_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Текстовое поле для результата
        self.result_text = tk.Text(result_frame, height=8, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Статус бар
        self.status_var = tk.StringVar(value="Готов к работе")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def update_database_info(self):
        """Обновление информации о базе данных"""
        try:
            stats = self.recognizer.get_database_stats()
            self.db_info_label.config(text=f"Песен: {stats['songs_count']}, Отпечатков: {stats['fingerprints_count']}")
        except Exception as e:
            self.db_info_label.config(text=f"Ошибка: {str(e)}")
    
    def add_song_dialog(self):
        """Диалог добавления песни"""
        file_path = filedialog.askopenfilename(
            title="Выберите аудио файл",
            filetypes=[
                ("Аудио файлы", "*.mp3 *.wav *.flac *.m4a *.ogg"),
                ("Все файлы", "*.*")
            ]
        )
        
        if file_path:
            # Создаем диалог ввода информации о песне
            dialog = tk.Toplevel(self.root)
            dialog.title("Добавить песню")
            dialog.geometry("400x200")
            dialog.resizable(False, False)
            dialog.transient(self.root)
            dialog.grab_set()
            
            # Центрируем диалог
            dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
            
            # Поля ввода
            ttk.Label(dialog, text="Название:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
            name_var = tk.StringVar(value=os.path.splitext(os.path.basename(file_path))[0])
            name_entry = ttk.Entry(dialog, textvariable=name_var, width=30)
            name_entry.grid(row=0, column=1, padx=10, pady=5)
            
            ttk.Label(dialog, text="Исполнитель:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
            artist_var = tk.StringVar()
            artist_entry = ttk.Entry(dialog, textvariable=artist_var, width=30)
            artist_entry.grid(row=1, column=1, padx=10, pady=5)
            
            # Кнопки
            button_frame = ttk.Frame(dialog)
            button_frame.grid(row=2, column=0, columnspan=2, pady=20)
            
            def add_song():
                try:
                    name = name_var.get().strip()
                    artist = artist_var.get().strip()
                    
                    if not name:
                        messagebox.showerror("Ошибка", "Введите название песни")
                        return
                    
                    self.status_var.set("Добавление песни...")
                    self.root.update()
                    
                    # Добавляем песню в отдельном потоке
                    def add_song_thread():
                        try:
                            song_id = self.recognizer.add_song_to_database(file_path, name, artist)
                            self.root.after(0, lambda: self.on_song_added(song_id, name, artist))
                        except Exception as e:
                            self.root.after(0, lambda: self.on_song_add_error(str(e)))
                    
                    threading.Thread(target=add_song_thread, daemon=True).start()
                    dialog.destroy()
                    
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Ошибка при добавлении песни: {str(e)}")
            
            ttk.Button(button_frame, text="Добавить", command=add_song).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="Отмена", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def on_song_added(self, song_id: int, name: str, artist: str):
        """Обработка успешного добавления песни"""
        self.status_var.set(f"Песня '{name}' добавлена (ID: {song_id})")
        self.update_database_info()
        self.log_result(f"✅ Песня добавлена: {name} - {artist}")
    
    def on_song_add_error(self, error: str):
        """Обработка ошибки добавления песни"""
        self.status_var.set("Ошибка при добавлении песни")
        self.log_result(f"❌ Ошибка: {error}")
        messagebox.showerror("Ошибка", f"Не удалось добавить песню: {error}")
    
    def show_songs_dialog(self):
        """Диалог показа списка песен"""
        try:
            songs = self.recognizer.list_database_songs()
            
            if not songs:
                messagebox.showinfo("Песни", "База данных пуста")
                return
            
            # Создаем диалог
            dialog = tk.Toplevel(self.root)
            dialog.title("Песни в базе данных")
            dialog.geometry("600x400")
            dialog.transient(self.root)
            dialog.grab_set()
            
            # Центрируем диалог
            dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
            
            # Создаем Treeview
            tree_frame = ttk.Frame(dialog)
            tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            tree = ttk.Treeview(tree_frame, columns=("name", "artist", "duration"), show="headings")
            tree.heading("name", text="Название")
            tree.heading("artist", text="Исполнитель")
            tree.heading("duration", text="Длительность")
            
            tree.column("name", width=200)
            tree.column("artist", width=150)
            tree.column("duration", width=100)
            
            # Добавляем данные
            for song_id, name, artist, file_path, duration in songs:
                duration_str = f"{duration:.1f}s" if duration else "N/A"
                tree.insert("", tk.END, values=(name, artist or "Неизвестно", duration_str))
            
            # Скроллбар
            scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Кнопка закрытия
            ttk.Button(dialog, text="Закрыть", command=dialog.destroy).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить список песен: {str(e)}")
    
    def toggle_recording(self):
        """Переключение режима записи"""
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()
    
    def start_recording(self):
        """Начало записи"""
        try:
            duration = float(self.duration_var.get())
            self.is_recording = True
            self.record_button.config(text="⏹️ Остановить запись")
            self.status_var.set("Запись...")
            
            # Запускаем запись в отдельном потоке
            self.recording_thread = threading.Thread(
                target=self.record_and_recognize, 
                args=(duration,), 
                daemon=True
            )
            self.recording_thread.start()
            
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную длительность записи")
    
    def stop_recording(self):
        """Остановка записи"""
        self.is_recording = False
        self.record_button.config(text="🎤 Записать и распознать")
        self.status_var.set("Остановка записи...")
    
    def record_and_recognize(self, duration: float):
        """Запись и распознавание в отдельном потоке"""
        try:
            # Записываем аудио
            self.root.after(0, lambda: self.status_var.set(f"Записываем {duration} секунд..."))
            
            result = self.recognizer.recognize_from_recording(duration)
            
            if not self.is_recording:  # Проверяем, не была ли остановлена запись
                return
            
            # Обрабатываем результат
            self.root.after(0, lambda: self.on_recognition_result(result))
            
        except Exception as e:
            self.root.after(0, lambda: self.on_recognition_error(str(e)))
        finally:
            self.root.after(0, self.reset_recording_state)
    
    def recognize_from_file(self):
        """Распознавание из файла"""
        file_path = filedialog.askopenfilename(
            title="Выберите аудио файл для распознавания",
            filetypes=[
                ("Аудио файлы", "*.mp3 *.wav *.flac *.m4a *.ogg"),
                ("Все файлы", "*.*")
            ]
        )
        
        if file_path:
            self.status_var.set("Распознавание файла...")
            
            # Запускаем распознавание в отдельном потоке
            def recognize_thread():
                try:
                    result = self.recognizer.recognize_from_file(file_path)
                    self.root.after(0, lambda: self.on_recognition_result(result))
                except Exception as e:
                    self.root.after(0, lambda: self.on_recognition_error(str(e)))
            
            threading.Thread(target=recognize_thread, daemon=True).start()
    
    def on_recognition_result(self, result: Optional[Tuple[str, str, float]]):
        """Обработка результата распознавания"""
        if result:
            name, artist, similarity = result
            self.status_var.set(f"Распознано: {name} - {artist}")
            self.log_result(f"🎵 Распознано: {name} - {artist}")
            self.log_result(f"   Схожесть: {similarity:.1%}")
            
            # Получаем дополнительную информацию
            try:
                confidence = self.recognizer.get_recognition_confidence(
                    self.recognizer.audio_processor.record_audio(1.0)  # Короткая запись для анализа
                )
                self.log_result(f"   Уверенность: {confidence['overall_confidence']:.1%}")
            except:
                pass
        else:
            self.status_var.set("Песня не распознана")
            self.log_result("❌ Песня не найдена в базе данных")
    
    def on_recognition_error(self, error: str):
        """Обработка ошибки распознавания"""
        self.status_var.set("Ошибка распознавания")
        self.log_result(f"❌ Ошибка: {error}")
        messagebox.showerror("Ошибка", f"Ошибка при распознавании: {error}")
    
    def reset_recording_state(self):
        """Сброс состояния записи"""
        self.is_recording = False
        self.record_button.config(text="🎤 Записать и распознать")
        if self.status_var.get() == "Остановка записи...":
            self.status_var.set("Готов к работе")
    
    def log_result(self, message: str):
        """Добавление сообщения в лог результатов"""
        self.result_text.insert(tk.END, message + "\n")
        self.result_text.see(tk.END)
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()

# Запуск приложения
if __name__ == "__main__":
    app = MusicRecognizerGUI()
    app.run()
