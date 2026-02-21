# ECG 信号处理项目 (ECG Signal Processing)

> 一个基于 Python 的心电信号（ECG）处理与分析工具集。
>
> 从 MIT-BIH 心律失常数据库中获取数据，进行信号滤波、R 波检测、心率计算以及异常心律检测。

## 项目结构

```
ECG-signal-processing/
├── data/                  # ECG 数据文件（自动下载）
├── examples/              # 示例输出图像
├── dataloader.py          # 数据加载模块
├── filter.py              # 信号滤波模块
├── rwave.py               # R 波检测模块
├── beat.py                # 心率计算模块
├── abnormal.py            # 异常心律检测模块
├── draw.py                # 信号可视化模块
├── main.py                # 主程序入口
├── requirements.txt       # 依赖列表
└── README.md
```

## 处理流程

```
原始 ECG 数据 (MIT-BIH)
    ↓
数据加载 (dataloader.py)
    ↓
带通滤波去噪 (filter.py)
    ↓
R 波峰值检测 (rwave.py)
    ↓
心率计算与分析 (beat.py)
    ↓
异常心律检测 (abnormal.py)
    ↓
可视化输出 (draw.py)
```

## 功能模块

### 数据加载 (`dataloader.py`)

- 使用 `wfdb` 库载入 MIT-BIH 心律失常数据库中的 ECG 信号
- 自动检测本地数据文件，缺失时从数据库自动下载
- 提供信号 (`signal`)、采样率 (`fs`) 的读取及时间段截取功能

### 信号滤波 (`filter.py`)

- **带通滤波**：基于 Butterworth 滤波器，去除 0.5Hz 以下的基线漂移和 40Hz 以上的高频噪声
- 使用 `scipy.signal.filtfilt` 实现零相位失真滤波

### R 波检测 (`rwave.py`)

- 应用平方能量增强法突出 R 波特征
- 利用 `scipy.signal.find_peaks` 实现 R 波峰值的自动定位
- 最小峰间距约束为 0.3 秒（对应最大心率 200 BPM）

### 心率分析 (`beat.py`)

- 根据 R 波位置计算 RR 间期（RR Interval）
- 计算瞬时心率（BPM）及全段平均心率
- 异常值过滤（排除 30-200 BPM 范围外的数据）

### 异常心律检测 (`abnormal.py`)

- 检测心动过速（>100 BPM）和心动过缓（<60 BPM）
- 计算心率变异性（HRV，基于 BPM 标准差）
- 综合判定心律状态：正常 / 心律过速 / 心律过缓 / 混合异常

### 信号可视化 (`draw.py`)

- 基于 `matplotlib` 绘制 ECG 波形，时间轴以秒为单位
- 支持 R 波标注叠加显示
- 支持中文标题和标签（SimHei 字体）

## 示例输出

![示例输出](examples/直出图像.png)

```
R波检测完成，全段共检测到 X 个点
前5个R波的索引为: [...]
最大瞬时心率: XX.XX bpm
最小瞬时心率: XX.XX bpm
平均心率: XX.XX bpm
异常检测结果: 正常, HRV: XX.XX
```

## 环境配置

### 1. 安装依赖

本项目依赖于 `numpy`、`scipy`、`matplotlib` 和 `wfdb`。

```bash
pip install -r requirements.txt
```

### 2. 数据准备

程序默认读取 MIT-BIH 数据库中的 100 号记录。首次运行时，若 `data/` 目录下缺少对应文件，程序会自动从数据库下载。

## 使用方法

```bash
python main.py
```

程序将依次执行：绘制原始信号 → 带通滤波 → R 波检测 → 心率计算 → 异常检测，并在每个阶段输出可视化图表和分析结果。

## 未来优化计划

基于当前系统架构，从生物医学工程专业角度出发，建议在以下维度进行深度优化：

1. **全波段特征定界 (Waveform Delineation)**：引入 Pan-Tompkins 算法改进版，实现 P 波、QRS 复合波、T 波的起止点自动定位，用于诊断房室传导阻滞及 QT 间期延长。

2. **心率变异性 (HRV) 深度分析**：增加时域分析（SDNN、RMSSD）和频域分析（FFT / Lomb-Scargle 计算 LF/HF 比值），定量评估自主神经系统调节功能。

3. **高级非平稳去噪**：引入小波变换 (Wavelet Transform) 或经验模态分解 (EMD)，在保留 ECG 细节特征的同时实现自适应去噪，弥补固定频率滤波的不足。

4. **信号质量指数 (SQI) 评估**：通过特征相关性或功率谱分布自动检测运动伪迹，标记不可信信号段，提高系统鲁棒性。

5. **搏动分类与智能诊断**：依照 AAMI 标准将搏动分类为正常 (N)、室性异位 (V)、室上性异位 (S) 等，结合轻量化 CNN 或 Random Forest 实现自动异常分类。