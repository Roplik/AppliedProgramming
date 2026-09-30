import numpy as np


def speed_up(data: np.ndarray, factor: float) -> np.ndarray:
    """Увеличивает скорость аудио в заданное количество раз.

    Реализовано с помощью линейной интерполяции массива сэмплов.

    Args:
        data (np.ndarray): Исходный массив сэмплов аудио.
        factor (float): Коэффициент ускорения (factor > 1).

    Returns:
        np.ndarray: Ускоренный массив сэмплов.
    """
    if factor <= 0:
        raise ValueError("Коэффициент ускорения должен быть больше 0.")

    num_samples = len(data)
    new_num_samples = int(num_samples / factor)

    
    indices = np.linspace(0, num_samples - 1, new_num_samples)

    if data.ndim == 1:
        return np.interp(indices, np.arange(num_samples), data)
    else:
        channels = [
            np.interp(indices, np.arange(num_samples), data[:, ch])
            for ch in range(data.shape[1])
        ]
        return np.column_stack(channels)

def concatenate_audio(data1: np.ndarray, data2: np.ndarray) -> np.ndarray:
    """Склеивает два аудиофайла один за другим.

    Args:
        data1 (np.ndarray): Первый массив сэмплов.
        data2 (np.ndarray): Второй массив сэмплов.

    Returns:
        np.ndarray: Объединенный массив сэмплов.
    """
    # Если количество каналов различается, приводим стерео к моно или наоборот
    if data1.ndim != data2.ndim:
        if data1.ndim == 1:
            data1 = np.column_stack((data1, data1))
        if data2.ndim == 1:
            data2 = np.column_stack((data2, data2))

    return np.concatenate((data1, data2), axis=0)

def boost_high_frequencies(data: np.ndarray, window_size: int = 15) -> np.ndarray:
    """Усиливает высокие частоты в аудио.

    Выделяет высокие частоты путем вычитания сглаженной версии (низких частот)
    из оригинального сигнала и прибавляет их к исходному аудио.

    Args:
        data (np.ndarray): Массив сэмплов аудио.
        window_size (int, optional): Размер окна для сглаживания numpy.convolve.
            По умолчанию равен 15.

    Returns:
        np.ndarray: Обработанный массив сэмплов с усиленными ВЧ.
    """
    window = np.ones(window_size) / window_size

    if data.ndim == 1:
        smoothed = np.convolve(data, window, mode="same")
        high_freqs = data - smoothed
        result = data + high_freqs
    else:
        channels = []
        for ch in range(data.shape[1]):
            smoothed_ch = np.convolve(data[:, ch], window, mode="same")
            high_freqs_ch = data[:, ch] - smoothed_ch
            channels.append(data[:, ch] + high_freqs_ch)
        result = np.column_stack(channels)

    
    return np.clip(result, -1.0, 1.0)
