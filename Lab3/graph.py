import matplotlib.pyplot as plt
import numpy as np


def plot_audio_signals(
    original: np.ndarray,
    processed: np.ndarray,
    sr_orig: int,
    sr_proc: int,
) -> None:
    """Отображает графики исходного и обработанного аудиофайлов с помощью Matplotlib.

    Args:
        original (np.ndarray): Исходный сигнал.
        processed (np.ndarray): Обработанный сигнал.
        sr_orig (int): Частота дискретизации исходного аудио.
        sr_proc (int): Частота дискретизации обработанного аудио.
    """
    time_orig = np.linspace(0, len(original) / sr_orig, num=len(original))
    time_proc = np.linspace(0, len(processed) / sr_proc, num=len(processed))

    plt.figure(figsize=(12, 6))

    # Исходный сигнал
    plt.subplot(2, 1, 1)
    plt.plot(time_orig, original, color="blue", alpha=0.7)
    plt.title("Исходное аудио")
    plt.xlabel("Время (секунды)")
    plt.ylabel("Амплитуда")
    plt.grid(True, linestyle="--", alpha=0.6)

    # Обработанный сигнал
    plt.subplot(2, 1, 2)
    plt.plot(time_proc, processed, color="crimson", alpha=0.7)
    plt.title(
        "Обработанное аудио (Ускорение + Склейка + Усиление высоких частот)"
    )
    plt.xlabel("Время (секунды)")
    plt.ylabel("Амплитуда")
    plt.grid(True, linestyle="--", alpha=0.6)

    plt.tight_layout()
    plt.show()