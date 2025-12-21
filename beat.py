def heartbeat():
    peak_times = peaks / fs
    rr = np.diff(peak_times)            # 单位：秒
    hr = 60 / rr                        # bpm

    print("平均心率:", np.mean(hr))