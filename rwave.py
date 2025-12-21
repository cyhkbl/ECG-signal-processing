from scipy.signal import find_peaks
from data import *
import numpy as np
import matplotlib.pyplot as plt

signal, fs = data_import()

def rwave(signal, fs):
    ecg = signal

    enhanced = ecg ** 2

    min_distance = int(0.25 * fs)
    peaks, props = find_peaks(enhanced, distance=min_distance, prominence=np.std(enhanced))

    plt.figure(figsize=(10,4))
    seg = slice(0, 5*fs)
    plt.plot(t[seg], ecg[seg], label='filtered ECG')
    plt.plot([t[i] for i in peaks if i < 5*fs], ecg[[i for i in peaks if i < 5*fs]], 'rx', label='R peaks')
    plt.legend()
    plt.title("R-peak detection (first 5s)")
    plt.show()