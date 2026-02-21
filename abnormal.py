import numpy as np

def detect_abnormal_ecg(bpm_list, rr_intervals, abnormal_ratio=0.01):
    # 定义正常心率范围
    normal_min = 60
    normal_max = 100

    # 检测异常心率
    too_quick = np.where(bpm_list > normal_max)[0]
    too_slow = np.where(bpm_list < normal_min)[0]

    # 当异常搏动数量超过总搏动数的一定比例时判定为异常
    threshold = len(bpm_list) * abnormal_ratio
    results = {
        "too_quick": len(too_quick),
        "too_slow": len(too_slow),
        "status": "正常"
    }
    if len(too_quick) > threshold and len(too_slow) > threshold:
        results["status"] = "心律过速和过缓"
    elif len(too_slow) > threshold:
        results["status"] = "心律过缓"
    elif len(too_quick) > threshold:
        results["status"] = "心律过速"

    # 心率变异性分析（SDNN，单位 ms）
    rr_ms = rr_intervals * 1000  # 秒转毫秒
    sdnn = np.std(rr_ms)
    results["hrv"] = sdnn
    
    return results