import numpy as np

def get_heartrate(rwave_indices, fs):
    rr_interval_point = np.diff(rwave_indices)
    rr_interval_time = rr_interval_point / fs
    instant_heartrate = 60 / rr_interval_time
    valid_instant_heartrate = instant_heartrate[(instant_heartrate > 30) & (instant_heartrate < 200)] #防止异常值干扰平均心率计算
    average_heartrate = np.mean(valid_instant_heartrate)
    return rr_interval_time, instant_heartrate, average_heartrate