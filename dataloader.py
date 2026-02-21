import wfdb
import os

class ECGDataLoader:

    def __init__(self, record_id, db_name = 'mitdb', save_dir = 'data'):  # 这里record_id是数据源序号
        self.db_name = db_name
        self.record_id = str(record_id)
        self.save_dir = save_dir
        # 初始化数据属性
        self.record_path = os.path.join(self.save_dir, self.record_id)
        self.signal, self.fs = None, None
        # 数据导入
        self.ensure_data_exists()
        self.data_import()

    def ensure_data_exists(self):
        extensions = ['hea', 'dat', 'atr']
        needed_files = [f"{self.record_id}.{ext}" for ext in extensions]
        files_exists = all(os.path.exists(os.path.join(self.save_dir, f)) for f in needed_files)
        # 构建数据文件路径
        if not files_exists:
            print(f"数据文件不存在，正在从{self.db_name}数据库下载{self.record_id}...")
            os.makedirs(self.save_dir, exist_ok=True)
            wfdb.dl_files(self.db_name, dl_dir=self.save_dir, files=needed_files)

    def data_import(self):
        # 读取ECG数据并赋值给类属性，现在signal是信号数据，fs是采样率
        record = wfdb.rdrecord(self.record_path)
        self.signal = record.p_signal[:,0]
        self.fs = record.fs
        return self.signal, self.fs

    def load_annotations(self):
        """读取 MIT-BIH 专家标注，返回所有搏动标注的样本索引和标注符号"""
        ann = wfdb.rdann(self.record_path, 'atr')
        # MIT-BIH 中搏动类标注符号（非搏动标注如 '+', '~', '|' 等需排除）
        beat_symbols = {'N', 'L', 'R', 'B', 'A', 'a', 'J', 'S', 'V', 'r',
                        'F', 'e', 'j', 'n', 'E', '/', 'f', 'Q', '?'}
        beat_mask = [s in beat_symbols for s in ann.symbol]
        beat_indices = ann.sample[beat_mask]
        beat_labels = [s for s, m in zip(ann.symbol, beat_mask) if m]
        return beat_indices, beat_labels

    def get_segment(self, start_time, end_time):
        # 计算起始和结束样本索引
        start_index = int(start_time * self.fs)
        end_index = int(end_time * self.fs)
        # 返回信号片段
        return self.signal[start_index:end_index]