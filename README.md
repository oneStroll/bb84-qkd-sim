# BB84 QKD 全链路基础仿真

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![CI](https://github.com/oneStroll/bb84-qkd-sim/actions/workflows/test.yml/badge.svg)

BB84 量子密钥分发（QKD）协议的全链路基础仿真。模拟 Alice（发送方）、Bob（接收方）和 Eve（窃听者）三个角色，支持 Eve 截获-重发攻击（Intercept-resend attack），并计算量子误码率（QBER）。

## 项目结构

```
bb84-qkd-sim/
├── bb84_sim/                   # 核心仿真包
│   ├── alice.py                # Alice：比特/基生成、编码
│   ├── bob.py                  # Bob：测量、基比对
│   ├── eve.py                  # Eve：截获-重发攻击
│   ├── utils.py                # QBER 计算、统计工具、可视化
│   └── protocol.py             # BB84Protocol 主协议编排器
├── tests/                      # pytest 单元测试
├── examples/
│   └── run_simulation.py       # 一键运行演示脚本
├── docs/
│   └── physics_background.md   # 物理背景（狄拉克符号详解）
├── AI-Collaboration.md         # AI 协同日志
└── requirements.txt            # 依赖清单
```

## 快速开始

### 环境要求

- Python ≥ 3.8
- 依赖：numpy, matplotlib, pytest

### 安装

```bash
# 克隆仓库
git clone https://github.com/oneStroll/bb84-qkd-sim.git
cd bb84-qkd-sim

# 安装依赖
pip install -r requirements.txt

# （可选）以可编辑模式安装包
pip install -e .
```

### 运行仿真

```bash
python examples/run_simulation.py
```

输出示例：

```
【场景 1】理想信道（无窃听者）
============================================================
BB84 QKD 协议仿真报告
============================================================
Eve 存在: 否
初始量子比特数: 1000
Sifted key 长度: 510
QBER 估算样本数: 255
错误比特数: 0
量子误比特率 (QBER): 0.0000 (0.00%)
============================================================

【场景 2】Eve 截获-重发攻击
============================================================
BB84 QKD 协议仿真报告
============================================================
Eve 存在: 是
初始量子比特数: 1000
Sifted key 长度: 504
QBER 估算样本数: 252
错误比特数: 68
量子误比特率 (QBER): 0.2698 (26.98%)
============================================================
```

### 运行测试

```bash
pytest tests/ -v
```

## 使用方法

### Python API

```python
from bb84_sim import BB84Protocol

protocol = BB84Protocol(seed=42)

# 无 Eve
result = protocol.run(n_qubits=1000, eve_present=False)
print(f"QBER: {result['qber']:.4f}")

# 有 Eve 截获-重发
result = protocol.run(n_qubits=1000, eve_present=True)
print(f"QBER: {result['qber']:.4f}")

# 一键对比
comparison = protocol.run_comparison(n_qubits=5000, plot=True)
```

### API 参考

| 方法 | 参数 | 返回 |
|------|------|------|
| `run(n_qubits, eve_present, sample_fraction)` | `n_qubits`-量子比特数, `eve_present`-是否窃听, `sample_fraction`-QBER 抽样比例 | `dict` 含 qber, n_errors, sifted_len 等 |
| `print_report()` | 无 | 打印格式化报告 |
| `run_comparison(n_qubits, plot)` | `plot`-是否显示对比图 | `dict` 含 no_eve 和 with_eve 结果 |

## 物理原理

BB84 协议由 Bennett 和 Brassard 于 1984 年提出，是世界上第一个量子密钥分发协议。其安全性基于量子力学的两个基本原理：

1. **不可克隆定理**：未知量子态无法被完美复制
2. **测量坍缩**：测量会扰动量子态，导致可被检测的误码

详细物理背景见 [docs/physics_background.md](docs/physics_background.md)。

## 仿真结果

| 场景 | 理论 QBER | 仿真 QBER (n=50000) |
|------|-----------|---------------------|
| 无 Eve（理想信道） | 0% | ≈ 0% |
| 有 Eve（截获-重发） | 25% | ≈ 25% |

有 Eve 时的 QBER ≈ 25% 来源于：
- Eve 选错测量基的概率：**50%**
- 选错基后 Bob 得到错误比特的概率：**50%**
- 综合误码率：**50% × 50% = 25%**

## 许可

MIT License
