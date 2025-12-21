from data import *
import numpy as np
from scipy.signal import butter, filtfilt, iirnotch

signal,fs = data_import()

def filter(signal,fs):

    def bandpass_filter(x, fs, low=0.5, high=40, order=4):
        nyq = 0.5 * fs
        b, a = butter(order, [low/nyq, high/nyq], btype='band')
        return filtfilt(b, a, x)

    def notch_filter(x, fs, f0=50, Q=30):
        b, a = iirnotch(w0=f0, Q=Q, fs=fs)
        return filtfilt(b, a, x)

    x1 = bandpass_filter(signal, fs)
    x2 = notch_filter(x1, fs, f0=50) 

    plt.figure()
    plt.plot(t[:5*fs], signal[:5*fs], label='raw')
    plt.plot(t[:5*fs], x2[:5*fs], label='filtered')
    plt.legend()
    plt.title("ECG: raw vs filtered (first 5s)")
    plt.show()
