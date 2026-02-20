from scipy.signal import find_peaks
import numpy as np

def find_rwave(signal, fs):
    squared_signal = signal ** 2
    # 设置最大心率
    threshold = np.mean(squared_signal) * 5
    # 设置最小距离为0.3秒（如果心率不超过200 bpm，那至少0.3秒跳一次），点的个数=采样率*时间
    min_data_points = int(0.3 * fs)
    peaks = find_peaks(squared_signal, height=threshold, distance=min_data_points)[0]
    return peaks