import numpy as np


def match_peaks(detected, reference, tolerance):
    """
    将检测到的 R 波与专家标注进行逐一匹配。

    参数:
        detected: 检测到的 R 波索引数组
        reference: 专家标注的 R 波索引数组
        tolerance: 允许的最大偏差（样本数）

    返回:
        tp: 正确检测数（True Positive）
        fp: 误检数（False Positive）
        fn: 漏检数（False Negative）
    """
    matched_ref = set()
    tp = 0

    for det in detected:
        # 找到与当前检测点最近的标注点
        distances = np.abs(reference - det)
        nearest_idx = np.argmin(distances)
        if distances[nearest_idx] <= tolerance and nearest_idx not in matched_ref:
            tp += 1
            matched_ref.add(nearest_idx)

    fp = len(detected) - tp
    fn = len(reference) - tp
    return tp, fp, fn


def evaluate_detector(detected, reference, fs, tolerance_ms=150):
    """
    评估 R 波检测算法的性能，对比专家标注计算各项指标。

    参数:
        detected: 算法检测到的 R 波索引数组
        reference: 专家标注的 R 波索引数组
        fs: 采样率 (Hz)
        tolerance_ms: 匹配容差 (毫秒)，默认 150ms（ANSI/AAMI 标准）

    返回:
        dict: 包含 TP, FP, FN, 灵敏度(Se), 阳性预测值(+P), F1 分数
    """
    tolerance = int(tolerance_ms * fs / 1000)  # 毫秒转换为样本数

    tp, fp, fn = match_peaks(detected, reference, tolerance)

    se = tp / (tp + fn) if (tp + fn) > 0 else 0.0   # 灵敏度
    pp = tp / (tp + fp) if (tp + fp) > 0 else 0.0   # 阳性预测值
    f1 = 2 * se * pp / (se + pp) if (se + pp) > 0 else 0.0

    return {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "se": se,
        "pp": pp,
        "f1": f1,
        "total_ref": len(reference),
        "total_det": len(detected),
    }


def print_evaluation(result, record_id):
    """格式化打印单条记录的评估结果"""
    print(f"\n{'='*50}")
    print(f"  记录 {record_id} - R 波检测性能评估")
    print(f"{'='*50}")
    print(f"  专家标注搏动数:   {result['total_ref']}")
    print(f"  算法检测搏动数:   {result['total_det']}")
    print(f"  正确检测 (TP):    {result['tp']}")
    print(f"  误检 (FP):        {result['fp']}")
    print(f"  漏检 (FN):        {result['fn']}")
    print(f"  灵敏度 (Se):      {result['se']:.4f}  ({result['se']*100:.2f}%)")
    print(f"  阳性预测值 (+P):  {result['pp']:.4f}  ({result['pp']*100:.2f}%)")
    print(f"  F1 分数:          {result['f1']:.4f}  ({result['f1']*100:.2f}%)")
    print(f"{'='*50}")


def print_summary(all_results):
    """汇总多条记录的评估结果并打印"""
    total_tp = sum(r["tp"] for r in all_results.values())
    total_fp = sum(r["fp"] for r in all_results.values())
    total_fn = sum(r["fn"] for r in all_results.values())
    total_ref = sum(r["total_ref"] for r in all_results.values())
    total_det = sum(r["total_det"] for r in all_results.values())

    se = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
    pp = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
    f1 = 2 * se * pp / (se + pp) if (se + pp) > 0 else 0.0

    print(f"\n{'#'*55}")
    print(f"  全部记录汇总 ({len(all_results)} 条记录)")
    print(f"{'#'*55}")
    # 逐记录一览表
    print(f"  {'记录':<8} {'标注数':<8} {'检测数':<8} {'Se':>8} {'+P':>8} {'F1':>8}")
    print(f"  {'-'*48}")
    for rid, r in all_results.items():
        print(f"  {rid:<8} {r['total_ref']:<8} {r['total_det']:<8} "
              f"{r['se']*100:>7.2f}% {r['pp']*100:>7.2f}% {r['f1']*100:>7.2f}%")
    print(f"  {'-'*48}")
    print(f"  {'汇总':<8} {total_ref:<8} {total_det:<8} "
          f"{se*100:>7.2f}% {pp*100:>7.2f}% {f1*100:>7.2f}%")
    print(f"{'#'*55}")
