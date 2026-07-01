"""工具函数：基比对、QBER 计算、统计报告。"""

import numpy as np


def sift_keys(
    alice_bits: np.ndarray,
    bob_bits: np.ndarray,
    alice_bases: np.ndarray,
    bob_bases: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """基比对（Basis Sifting）。

    Alice 和 Bob 公开比对各自的测量基（不公开比特值），
    只保留双方使用相同基的位置上的比特，作为 sifted key。

    参数:
        alice_bits: Alice 的原始比特
        bob_bits: Bob 的测量结果比特
        alice_bases: Alice 的编码基
        bob_bases: Bob 的测量基

    返回:
        (alice_sifted, bob_sifted): 双方筛选后的密钥
    """
    match = alice_bases == bob_bases
    return alice_bits[match], bob_bits[match]


def compute_qber(
    alice_key: np.ndarray,
    bob_key: np.ndarray,
    sample_fraction: float = 0.5,
    rng: np.random.Generator | None = None,
) -> tuple[float, int, int]:
    """计算量子误比特率 QBER (Quantum Bit Error Rate)。

    从 sifted key 中随机抽取一个子集公开比对以估算误码率。
    剩余未公开的比特位作为最终密钥。

    QBER = 错误比特数 / 比对总比特数

    参数:
        alice_key: Alice 的 sifted key
        bob_key: Bob 的 sifted key
        sample_fraction: 用于比对的样本比例 (0~1)
        rng: 随机数生成器

    返回:
        (qber, n_errors, n_sample): QBER 值、错误数、样本大小
    """
    if rng is None:
        rng = np.random.default_rng()

    n = len(alice_key)
    n_sample = max(1, int(n * sample_fraction))

    # 随机抽取样本位置
    indices = rng.choice(n, size=n_sample, replace=False)

    n_errors = int(np.sum(alice_key[indices] != bob_key[indices]))
    qber = n_errors / n_sample

    return qber, n_errors, n_sample


def format_report(
    n_qubits: int,
    sifted_len: int,
    qber: float,
    n_errors: int,
    n_sample: int,
    eve_present: bool,
    elapsed: float | None = None,
) -> str:
    """生成格式化的仿真统计报告。"""
    lines = [
        "=" * 60,
        "BB84 QKD 协议仿真报告",
        "=" * 60,
        f"Eve 存在: {'是' if eve_present else '否'}",
        f"初始量子比特数: {n_qubits}",
        f"Sifted key 长度: {sifted_len}",
        f"QBER 估算样本数: {n_sample}",
        f"错误比特数: {n_errors}",
        f"量子误比特率 (QBER): {qber:.4f} ({qber * 100:.2f}%)",
    ]
    if elapsed is not None:
        lines.insert(2, f"仿真耗时: {elapsed:.4f} 秒")
    lines.append("=" * 60)
    return "\n".join(lines) + "\n"


def plot_qber_comparison(
    qber_no_eve: float,
    qber_with_eve: float,
    save_path: str | None = None,
) -> None:
    """绘制 QBER 对比柱状图。"""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return  # matplotlib 不可用时静默跳过

    # Use English labels to avoid CJK font dependency
    labels = ["No Eve", "With Eve\n(Intercept-resend)"]
    values = [qber_no_eve * 100, qber_with_eve * 100]

    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(labels, values, color=["#4CAF50", "#F44336"], width=0.5)
    ax.set_ylabel("QBER (%)")
    ax.set_title("BB84 QKD: QBER Comparison")
    ax.set_ylim(0, max(values) * 1.4 + 5)

    for bar, val in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.5,
            f"{val:.2f}%",
            ha="center",
            fontsize=12,
        )

    # Theoretical reference lines
    ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.8, label="Theory: 0%")
    ax.axhline(y=25, color="orange", linestyle="--", linewidth=0.8, label="Theory: 25%")
    ax.legend()

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
    plt.show()


def plot_qber_vs_qubits(
    qubit_counts: list[int],
    qber_no_eve: list[float],
    qber_with_eve: list[float],
    save_path: str | None = None,
) -> None:
    """绘制 QBER 随量子比特数变化的曲线。"""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(qubit_counts, qber_no_eve, "o-", label="No Eve", color="#4CAF50")
    ax.plot(qubit_counts, qber_with_eve, "s-", label="With Eve (Intercept-resend)", color="#F44336")
    ax.axhline(y=25, color="orange", linestyle="--", linewidth=0.8, label="Theory: 25%")
    ax.set_xlabel("Number of Initial Qubits")
    ax.set_ylabel("QBER (%)")
    ax.set_title("BB84 QKD: QBER vs Number of Qubits")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
    plt.show()
