from scipy import signal

def bandpass_filter(data, fs, lowcut=0.5, highcut=40, order=4):
    nyq = 0.5 * fs
    # 归一化
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='band')
    filtered_data = signal.filtfilt(b, a, data)
    return filtered_data