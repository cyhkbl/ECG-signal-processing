import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体为黑体
plt.rcParams['font.sans-serif'] = ['SimHei'] 
# 解决负号 '-' 显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False

def draw_signal(loader, start = 0, duration = 5, title="心电", rwave = None):  # loader 是一个 ECGDataLoader 对象，在 main.py 中创建并传入，默认从0秒开始画，画5秒
    start_index = int(start * loader.fs)
    end_index = int((start + duration) * loader.fs)
    # 生成时间轴，总时间长度为样本长度/采样率
    time_axis = np.arange(start_index, end_index) / loader.fs # 将样本索引转换为时间（秒）
    # 绘制 ECG 信号
    plt.figure(figsize=(15, 5))
    plt.plot(time_axis, loader.signal[start_index:end_index], color='red', linewidth=1)
    if rwave is not None:
        rwave_range = (rwave >= start_index) & (rwave < end_index)  # 只保留在当前绘制范围内的 R 波索引 
        rwave_time = rwave[rwave_range] / loader.fs  # 将 R 波索引转换为时间
        rwave_amplitude = loader.signal[rwave[rwave_range]]  # 获取 R 波峰值的幅度
        plt.scatter(rwave_time, rwave_amplitude, color='blue', marker='o', label='R 波峰值')
        plt.legend()
    plt.xlabel("时间(s)")
    plt.ylabel("电压(mV)")
    plt.title(f"{title} (Record ID: {loader.record_id})")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()