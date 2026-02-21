import dataloader
import draw
import filter
import rwave
import beat
import abnormal
import evaluate

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
print(f"最大瞬时心率: {max(instant_heartrate):.2f} bpm")
print(f"最小瞬时心率: {min(instant_heartrate):.2f} bpm")
print(f"平均心率: {average_heartrate:.2f} bpm")

# 异常检测
abnormal_results = abnormal.detect_abnormal_ecg(instant_heartrate, rr_interval_time)
print(f"异常检测结果: {abnormal_results['status']}, HRV(SDNN): {abnormal_results['hrv']:.2f} ms")

# 对比专家标注评估 R 波检测性能
ref_indices, ref_labels = origin.load_annotations()
result = evaluate.evaluate_detector(rwave_indices, ref_indices, origin.fs)
evaluate.print_evaluation(result, origin.record_id)

# ============================================================
#  多记录批量评估（由Claude Code完成）
# ============================================================

# MIT-BIH 心律失常数据库全部 48 条记录
MITDB_RECORDS = [
    '100', '101', '102', '103', '104', '105', '106', '107', '108', '109',
    '111', '112', '113', '114', '115', '116', '117', '118', '119', '121',
    '122', '123', '124', '200', '201', '202', '203', '205', '207', '208',
    '209', '210', '212', '213', '214', '215', '217', '219', '220', '221',
    '222', '223', '228', '230', '231', '232', '233', '234',
]

print("\n开始批量评估全部 MIT-BIH 记录...")
all_results = {}
for record_id in MITDB_RECORDS:
    try:
        loader = dataloader.ECGDataLoader(record_id=record_id)
        loader.signal = filter.bandpass_filter(loader.signal, loader.fs)
        detected = rwave.find_rwave(loader.signal, loader.fs)
        ref, _ = loader.load_annotations()
        r = evaluate.evaluate_detector(detected, ref, loader.fs)
        all_results[record_id] = r
        print(f"  记录 {record_id}: Se={r['se']*100:.2f}%, +P={r['pp']*100:.2f}%, F1={r['f1']*100:.2f}%")
    except Exception as e:
        print(f"  记录 {record_id}: 处理失败 - {e}")

evaluate.print_summary(all_results)
