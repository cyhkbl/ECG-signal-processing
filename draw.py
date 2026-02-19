import matplotlib.pyplot as plt
import numpy as np

def draw_signal(loader, start = 0, duration = 5, title="心电"):  # loader 是一个 ECGDataLoader 对象，在 main.py 中创建并传入，默认从0秒开始画，画5秒
    start_index = int(start * loader.fs)
    end_index = int((start + duration) * loader.fs)
    # 生成时间轴，总时间长度为样本长度/采样率
    segment_length = len(loader.signal[start_index:end_index])
    time_axis = np.linspace(start, start + duration, segment_length)  # 将样本索引转换为时间（秒）
    # 绘制 ECG 信号
    plt.figure(figsize=(15, 5))
    plt.plot(time_axis, loader.signal[start_index:end_index], color='red', linewidth=1)
    plt.xlabel("时间(s)")
    plt.ylabel("电压(mV)")
    plt.title(f"{title} (Record ID: {loader.record_id})")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()