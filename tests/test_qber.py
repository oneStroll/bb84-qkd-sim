"""QBER 计算相关的单元测试。

核心验证：
1. 无 Eve 时 QBER ≈ 0%（理想信道无噪声）
2. 有 Eve 截获-重发时 QBER ≈ 25%
3. 统计显著性：大样本下应可靠收敛
"""

import numpy as np
from bb84_sim import BB84Protocol


def test_no_eve_qber_is_zero():
    """无 Eve 时 QBER 应接近于 0（允许统计波动 < 2%）。"""
    protocol = BB84Protocol(seed=42)
    result = protocol.run(n_qubits=10000, eve_present=False, sample_fraction=0.5)
    # 在 10000 个 qubits、5000 个比对样本下，误差应 < 1%
    assert result["qber"] < 0.02, f"无 Eve 时 QBER 过高: {result['qber']:.4f}"


def test_with_eve_qber_around_25_percent():
    """有 Eve 截获-重发时 QBER 应接近 25%（允许 ±5% 统计波动）。"""
    protocol = BB84Protocol(seed=42)
    result = protocol.run(n_qubits=20000, eve_present=True, sample_fraction=0.5)
    assert 0.20 <= result["qber"] <= 0.30, (
        f"有 Eve 时 QBER 不在预期范围: {result['qber']:.4f}"
    )


def test_qber_increases_with_eve():
    """有 Eve 时的 QBER 应显著高于无 Eve 时。"""
    protocol = BB84Protocol(seed=42)
    clean = protocol.run(n_qubits=5000, eve_present=False)
    with_eve = protocol.run(n_qubits=5000, eve_present=True)
    assert with_eve["qber"] > clean["qber"], "Eve 应导致 QBER 上升"


def test_sifted_key_length():
    """Sifted key 长度约为初始比特数的一半（因基比对会丢弃约 50%）。"""
    n_qubits = 10000
    protocol = BB84Protocol(seed=42)
    result = protocol.run(n_qubits=n_qubits, eve_present=False)
    sifted = result["sifted_len"]
    # 理论上丢弃约 50%，允许 ±10% 波动
    assert 0.35 * n_qubits <= sifted <= 0.65 * n_qubits, (
        f"Sifted key 长度异常: {sifted} (预期 ~{n_qubits // 2})"
    )


def test_reproducibility_with_seed():
    """相同 seed 应产生相同的仿真结果。"""
    r1 = BB84Protocol(seed=123).run(n_qubits=1000, eve_present=True)
    r2 = BB84Protocol(seed=123).run(n_qubits=1000, eve_present=True)
    assert r1["qber"] == r2["qber"], "相同 seed 应产生相同 QBER"
    assert np.array_equal(r1["alice_sifted"], r2["alice_sifted"]), (
        "相同 seed 应产生相同的 sifted key"
    )


def test_sample_fraction_effect():
    """sample_fraction 不应显著影响 QBER 估计值（种子固定时）。"""
    protocol = BB84Protocol(seed=42)
    r1 = protocol.run(n_qubits=10000, eve_present=True, sample_fraction=0.3)
    r2 = protocol.run(n_qubits=10000, eve_present=True, sample_fraction=0.7)
    assert abs(r1["qber"] - r2["qber"]) < 0.05, (
        f"不同 sample_fraction 下 QBER 差异过大: {r1['qber']:.4f} vs {r2['qber']:.4f}"
    )
