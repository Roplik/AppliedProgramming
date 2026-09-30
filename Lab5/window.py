import os
import matplotlib.pyplot as plt
import soundfile as sf
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import QTime, QUrl, Qt
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSlider,
    QWidget,
    QGridLayout
)

from iterator import AudioPathIterator

class AudioPlayerApp(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Аудио Плеер Датасета — Лабораторная работа №5 (Вариант 19)")
        self.resize(750, 550)

        self.history = []          # Список пройденных путей
        self.current_index = -1    # Индекс текущего трека в истории

        self.iterator = None
        self.current_audio_path = None

        self.player = QMediaPlayer()

        self.init_ui()
        self.init_signals()

    def init_ui(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QGridLayout(central_widget)

        # 1. Кнопка выбора
        self.btn_select_source = QPushButton("Выбрать CSV / Папку")
        layout.addWidget(
            self.btn_select_source, 
            0, 0, 
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
        )

        # 2. Путь к источнику
        self.lbl_source_path = QLabel("Источник не выбран")
        self.lbl_source_path.setStyleSheet("color: gray;")
        layout.addWidget(self.lbl_source_path, 0, 1, Qt.AlignmentFlag.AlignCenter)

        # 3. Название трека
        self.lbl_title = QLabel("Название трека: —")
        self.lbl_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(self.lbl_title, 1, 0, 1, 2, Qt.AlignmentFlag.AlignLeft)

        # Длительность трека
        self.lbl_duration = QLabel("Длительность: 00:00 / 00:00")
        self.lbl_duration.setStyleSheet("font-size: 12px; color: #333;")
        layout.addWidget(self.lbl_duration, 2, 0, 1, 2, Qt.AlignmentFlag.AlignLeft)

        # 4. Визуализация звуковой волны (Matplotlib Canvas)
        self.figure, self.ax = plt.subplots(figsize=(6, 2))
        self.figure.patch.set_facecolor("#f0f0f0")
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas, 3, 0, 1, 2)

        # 5. Ползунок прогресса воспроизведения
        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        layout.addWidget(self.progress_slider, 4, 0, 1, 2)

        # 6. Кнопки управления проигрыванием
        controls_layout = QHBoxLayout()
        
        self.btn_prev = QPushButton("⏮")
        self.btn_play_pause = QPushButton("Play")
        self.btn_next = QPushButton("⏭")
        
        controls_layout.addWidget(self.btn_prev)
        controls_layout.addWidget(self.btn_play_pause)
        controls_layout.addWidget(self.btn_next)
        
        layout.addLayout(controls_layout, 5, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)

        # Настройка растяжения сетки
        layout.setRowStretch(3, 1)  # Растягиваем строку с графиком
        layout.setColumnStretch(1, 1)

    def init_signals(self) -> None:
        self.btn_select_source.clicked.connect(self.select_dataset_source)
        self.btn_play_pause.clicked.connect(self.toggle_play_pause)
        self.btn_next.clicked.connect(self.load_next_track)
        self.btn_prev.clicked.connect(self.load_prev_track)

        # Сигналы плеера
        self.player.positionChanged.connect(self.update_position)
        self.player.durationChanged.connect(self.update_duration)
        self.progress_slider.sliderMoved.connect(self.set_position)
        
    def select_dataset_source(self) -> None:
        """Открывает диалог выбора папки или CSV-файла."""
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите CSV аннотацию или перейдите к папке",
            "",
            "CSV Files (*.csv);;All Files (*)",
        )

        if not path:
            # Если файл не выбран, даем возможность выбрать папку
            path = QFileDialog.getExistingDirectory(self, "Выберите папку датасета")

        if path:
            try:
                self.iterator = AudioPathIterator(path)
                self.lbl_source_path.setText(os.path.basename(path))
                self.btn_next.setEnabled(True)
                self.load_next_track()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить датасет:\n{e}")

    def load_prev_track(self) -> None:
        """Воспроизводит предыдущий трек из истории."""
        if self.current_index > 0:
            self.current_index -= 1
            self.play_audio_by_path(self.history[self.current_index])
            self.btn_next.setEnabled(True)
            self.player.pause()
            self.btn_play_pause.setText("Play")
        else:
            QMessageBox.information(self, "Начало", "Это первый трек в истории.")


    def load_next_track(self) -> None:
        if not self.iterator:
            return

        # Если мы находимся в середине истории (возвращались назад), идем по истории вперед
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            self.play_audio_by_path(self.history[self.current_index])
            self.player.pause()
            self.btn_play_pause.setText("Play")
            return

        # Иначе запрашиваем следующий трек из итератора
        try:
            next_path = next(self.iterator)
        except StopIteration:
            QMessageBox.information(self, "Конец датасета", "Достигнут конец списка аудиофайлов.")
            self.btn_next.setEnabled(False)
            return

        if not os.path.exists(next_path):
            QMessageBox.warning(self, "Ошибка файла", f"Файл не найден:\n{next_path}")
            self.load_next_track()
            return

        # Добавляем в историю и воспроизводим
        self.history.append(next_path)
        self.current_index += 1
        self.play_audio_by_path(next_path)
        self.player.pause()
        self.btn_play_pause.setText("Play")

    def play_audio_by_path(self, audio_path: str) -> None:
        """Вспомогательный метод загрузки и отрисовки трека."""
        self.player.stop()
        self.current_audio_path = audio_path

        track_name = os.path.basename(self.current_audio_path)
        self.lbl_title.setText(f"Название трека: {track_name}")

        media_url = QUrl.fromLocalFile(self.current_audio_path)
        self.player.setMedia(QMediaContent(media_url))
        self.btn_play_pause.setEnabled(True)

        self.plot_waveform(self.current_audio_path)

    def toggle_play_pause(self) -> None:
        """Воспроизводит или ставит на паузу аудиокомпозицию."""
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.btn_play_pause.setText("Play")
        else:
            self.player.play()
            self.btn_play_pause.setText("Pause")

    def update_position(self, position: int) -> None:
        """Обновляет позицию ползунка прогресса и текущее время."""
        self.progress_slider.setValue(position)
        self.update_duration_label(position, self.player.duration())

    def update_duration(self, duration: int) -> None:
        """Настраивает диапазон ползунка при изменении длительности трека."""
        self.progress_slider.setRange(0, duration)
        self.update_duration_label(self.player.position(), duration)

    def set_position(self, position: int) -> None:
        """Перематывает трек по клику/перетаскиванию ползунка."""
        self.player.setPosition(position)

    def update_duration_label(self, current_ms: int, total_ms: int) -> None:
        """Форматирует миллисекунды в строку ММ:СС."""
        current_time = QTime(0, 0, 0).addMSecs(current_ms).toString("mm:ss")
        total_time = QTime(0, 0, 0).addMSecs(total_ms).toString("mm:ss")
        self.lbl_duration.setText(f"Длительность: {current_time} / {total_time}")

    def plot_waveform(self, file_path: str) -> None:
        """Считывает сэмплы аудио и отображает их график с помощью Matplotlib."""
        self.ax.clear()
        try:
            data, _ = sf.read(file_path)
            if data.ndim > 1:
                data = data[:, 0]  # Берем первый канал для стерео

            # Прореживание точек для ускорения отрисовки
            stride = max(1, len(data) // 2000)
            data_sub = data[::stride]

            self.ax.plot(data_sub, color="#007acc", linewidth=0.8)
            self.ax.set_title("Форма волны (Waveform)", fontsize=10)
            self.ax.set_axis_off()
            self.figure.tight_layout()
        except Exception:
            self.ax.text(
                0.5,
                0.5,
                "Ошибка чтения сэмплов аудио",
                ha="center",
                va="center",
                transform=self.ax.transAxes,
            )
            self.ax.set_axis_off()

        self.canvas.draw()