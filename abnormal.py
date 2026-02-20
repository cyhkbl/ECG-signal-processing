import numpy as np

def detect_abnormal_ecg(bpm_list):
    # 定义正常心率范围
    normal_min = 60
    normal_max = 100

    # 检测异常心率
    too_quick = np.where(bpm_list > normal_max)[0]
    too_slow = np.where(bpm_list < normal_min)[0]

    # 异常情况统计
    results = {
        "too_quick": len(too_quick),
        "too_slow": len(too_slow),
        "status": "正常"
    }
    if len(too_quick) > 5 and len(too_slow) > 5:
        results["status"] = "心律过速和过缓"
    elif len(too_slow) > 5:
        results["status"] = "心律过缓"
    elif len(too_quick) > 5:
        results["status"] = "心律过速"

    # 心率变异性分析
    hrv = np.std(bpm_list)
    results["hrv"] = hrv
    
    return results