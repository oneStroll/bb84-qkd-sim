#!/usr/bin/env python3
"""BB84 QKD 协议全链路仿真 — 演示脚本。

直接运行本脚本即可看到完整仿真过程：
    python examples/run_simulation.py
"""

import sys
import os

# 将项目根目录加入 sys.path（确保可以直接运行）
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from bb84_sim import BB84Protocol


import numpy as np


def show_sifting_process():
    """详细展示基底比对（Basis Sifting）过程。"""
    n = 20  # 小样本便于展示
    rng = np.random.default_rng(42)

    # Alice 生成比特和编码基
    alice_bits = rng.integers(0, 2, size=n)
    alice_bases = rng.choice(["Z", "X"], size=n)

    # Bob 随机选择测量基
    bob_bases = rng.choice(["Z", "X"], size=n)

    # 基比对
    match = alice_bases == bob_bases

    # 筛选后的 sifted key
    alice_sifted = alice_bits[match]

    print("=" * 70)
    print("【基底比对过程演示】（n = 20）")
    print("=" * 70)
    print()
    print(f"{'位置':>4} {'Alice比特':>8} {'Alice基':>8} {'Bob基':>8} {'匹配?':>6} {'保留?':>6}")
    print("-" * 45)
    for i in range(n):
        keep = "*" if match[i] else " "
        print(f"{i:>4} {alice_bits[i]:>8} {alice_bases[i]:>8} {bob_bases[i]:>8} {str(match[i]):>6} {keep:>6}")

    print()
    print(f"基匹配数: {np.sum(match)} / {n}  (预期 ~50%)")
    print(f"Alice 的 sifted key: {alice_sifted}")
    print(f"Sifted key 长度: {len(alice_sifted)}")
    print("=" * 70)
    print()


def main():
    print("=" * 60)
    print("BB84 量子密钥分发（QKD）协议 — 全链路仿真")
    print("=" * 60)

    # ── 基底比对过程展示 ──
    show_sifting_process()

    # ── 场景 1: 无 Eve 的理想信道 ──
    print("\n【场景 1】理想信道（无窃听者）\n")
    protocol = BB84Protocol(seed=42)
    result_clean = protocol.run(n_qubits=1000, eve_present=False)
    protocol.print_report()

    # ── 场景 2: 有 Eve 截获-重发攻击 ──
    print("\n【场景 2】Eve 截获-重发攻击\n")
    result_eve = protocol.run(n_qubits=1000, eve_present=True)
    protocol.print_report()

    # ── 结果分析 ──
    print("\n【分析】")
    print(f"  无 Eve 时 QBER:  {result_clean['qber']:.4f} ({result_clean['qber'] * 100:.2f}%)")
    print(f"  有 Eve 时 QBER:  {result_eve['qber']:.4f} ({result_eve['qber'] * 100:.2f}%)")
    print(f"  理论预期（有 Eve）: ≈ 25.00%")
    print()

    if result_eve["qber"] > 0.10:
        print("  [OK] Eve 的存在被检测到！QBER 显著升高，通信不安全。")
    else:
        print("  [FAIL] QBER 过低，可能未正确触发 Eve 攻击。")

    # ── 大规模仿真验证 ──
    print("\n" + "=" * 60)
    print("大规模仿真验证（n = 50000，提高统计精度）")
    print("=" * 60)

    print("\n无 Eve 场景（中）：")
    protocol.run(n_qubits=50000, eve_present=False, sample_fraction=0.2)
    protocol.print_report()

    print("\n有 Eve 场景（中）：")
    protocol.run(n_qubits=50000, eve_present=True, sample_fraction=0.2)
    protocol.print_report()

    # ── QBER 对比图 ──
    print("\n生成 QBER 对比图...")
    comparison = protocol.run_comparison(
        n_qubits=5000,
        sample_fraction=0.5,
        save_plot="qber_comparison.png",
    )
    print("QBER 对比图已保存至: qber_comparison.png")


if __name__ == "__main__":
    main()
