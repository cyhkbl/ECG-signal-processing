import dataloader
import draw
import filter
import rwave
import matplotlib.pyplot as plt
import beat
import abnormal

# 载入数据
origin = dataloader.ECGDataLoader(record_id='100')  # 这里record_id是数据源序号，我选择100号数据

# 画图
draw.draw_signal(origin, start=0, duration=5, title="原始心电")

# 滤波
origin.signal = filter.bandpass_filter(origin.signal, origin.fs)
draw.draw_signal(origin, start=0, duration=5, title="滤波后的心电")

# R波标记
rwave_indices = rwave.find_rwave(origin.signal, origin.fs)
print(f"R波检测完成，全段共检测到 {len(rwave_indices)} 个点")
print(f"前5个R波的索引为: {rwave_indices[:5]}")
draw.draw_signal(origin, start=0, duration=5, title="R波标记的心电", rwave=rwave_indices)

# 算心率
rr_interval_time, instant_heartrate, average_heartrate = beat.get_heartrate(rwave_indices, origin.fs)
print(f"最大瞬时心率: {max(instant_heartrate):.2f} bpm") # 保留2位小数
print(f"最小瞬时心率: {min(instant_heartrate):.2f} bpm")
print(f"平均心率: {average_heartrate:.2f} bpm")

# 异常检测
abnormal_results = abnormal.detect_abnormal_ecg(instant_heartrate, rr_interval_time)
print(f"异常检测结果: {abnormal_results['status']}, HRV(SDNN): {abnormal_results['hrv']:.2f}")