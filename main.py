import dataloader
import draw
import filter
import rwave
import matplotlib.pyplot as plt

# 载入数据
origin = dataloader.ECGDataLoader(record_id='100')  # 这里record_id是数据源序号，我选择100号数据

# 画图
draw.draw_signal(origin, start=0, duration=5, title="原始心电")

# 滤波
filtered = dataloader.ECGDataLoader(record_id='100')
filtered.signal = filter.bandpass_filter(origin.signal, origin.fs)
draw.draw_signal(filtered, start=0, duration=5, title="滤波后的心电")

# R波标记
rwave_indices = rwave.find_rwave(filtered.signal, filtered.fs)
print(f"R波检测完成，全段共检测到 {len(rwave_indices)} 个点")
print(f"前5个R波的索引为: {rwave_indices[:5]}")
draw.draw_signal(filtered, start=0, duration=5, title="R波标记的心电", rwave=rwave_indices)