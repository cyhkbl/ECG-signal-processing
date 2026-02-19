import wfdb
import os

class ECGDataLoader:

    def __init__(self, db_name = 'mitdb', record_id, save_dir = 'data'):  # 这里record_id是数据源序号
        self.record_id = record_id
        self.save_dir = save_dir
        # 初始化数据属性
        self.record_path = os.path.join(self.save_dir, self.record_id)
        self.signal, self.fs = None, None
        # 数据导入
        self.ensure_data_exists()
        self.data_import()
    
    def ensure_data_exists(self):
        # 构建数据文件路径
        if not os.path.exists(self.record_path + '.dat'):
            print(f"数据文件不存在，正在从{self.db_name}数据库下载{self.record_id}...")
            os.makedirs(self.save_dir, exist_ok=True)
            wfdb.dl_database(self.db_name, dl_dir=self.save_dir, records=[self.record_id])

    def data_import(self):
        # 读取ECG数据并赋值给属性
        record = wfdb.rdrecord(self.record_path)
        self.signal = record.p_signal[:,0]
        self.fs = record.fs
        return self.signal, self.fs