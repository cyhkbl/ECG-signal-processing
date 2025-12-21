
def abnormal():
    abnormal_fast = hr > 100
    abnormal_slow = hr < 60
    print("过速次数:", abnormal_fast.sum())
    print("过缓次数:", abnormal_slow.sum())