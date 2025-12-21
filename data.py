import wfdb

def data_import():
    record = wfdb.rdrecord('mitdb/100')
    signal = record.p_signal[:,0]
    fs = record.fs
    return signal, fs