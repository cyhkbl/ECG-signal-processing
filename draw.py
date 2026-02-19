import matplotlib.pyplot as plt
from dataloader import *

signal, fs = data_import()

def draw(signal, fs):
    t = [i/fs for i in range(len(signal))]
    plt.figure()
    plt.plot(t[:5*fs], signal[:5*fs])
    plt.xlabel("时间(s)")
    plt.ylabel("电压(mV)")
    plt.show()