"""BB84Protocol: BB84 量子密钥分发协议的全链路仿真编排器。

完整协议流程：
1. Alice 生成随机比特串和随机编码基 → 发送量子态
2. [可选] Eve 截获-重发攻击
3. Bob 随机选择测量基 → 测量量子态
4. Bob 公开测量基（不公开比特值）
5. Alice 和 Bob 基比对筛选 → sifted key
6. 公开比对 sifted key 子集 → 计算 QBER
"""

import time
import numpy as np

from .alice import Alice
from .bob import Bob
from .eve import Eve
from . import utils


class BB84Protocol:
    """BB84 QKD 协议仿真主控类。

    使用示例:
        >>> protocol = BB84Protocol()
        >>> result = protocol.run(n_qubits=1000, eve_present=True)
        >>> print(f"QBER: {result['qber']:.4f}")
    """

    def __init__(self, seed: int | None = None):
        self.rng = np.random.default_rng(seed)
        self.alice = Alice(rng=np.random.default_rng(self.rng.integers(2**31)))
        self.bob = Bob(rng=np.random.default_rng(self.rng.integers(2**31)))
        self.eve = Eve(rng=np.random.default_rng(self.rng.integers(2**31)))
        self.results: dict = {}

    def run(
        self,
        n_qubits: int = 1000,
        eve_present: bool = False,
        sample_fraction: float = 0.5,
    ) -> dict:
        """执行一次完整的 BB84 协议仿真。

        参数:
            n_qubits: 初始生成的量子比特数量
            eve_present: 是否存在 Eve 窃听
            sample_fraction: 用于 QBER 估算的样本比例

        返回:
            dict: 包含以下键值的字典
                - qber: QBER 值
                - n_errors: QBER 估算中的错误比特数
                - n_sample: QBER 估算的样本大小
                - sifted_len: sifted key 长度
                - alice_sifted: Alice 的 sifted key
                - bob_sifted: Bob 的 sifted key
                - eve_present: Eve 是否存在
        """
        t_start = time.perf_counter()

        # ── 步骤 1: Alice 制备量子态 ──
        alice_bits, alice_bases = self.alice.prepare_qubits(n_qubits)

        # ── 步骤 2: Eve 截获-重发（可选） ──
        if eve_present:
            eve_bits, eve_bases = self.eve.intercept_resend(alice_bits, alice_bases)
            bob_received_bits = eve_bits
            bob_received_bases = eve_bases
        else:
            bob_received_bits = alice_bits
            bob_received_bases = alice_bases

        # ── 步骤 3: Bob 随机选择测量基并测量 ──
        bob_bases = self.bob.generate_bases(n_qubits)
        bob_bits = self.bob.measure(bob_received_bits, bob_received_bases, bob_bases)

        # ── 步骤 4 & 5: 基比对 → sifted key ──
        alice_sifted, bob_sifted = utils.sift_keys(
            alice_bits, bob_bits, alice_bases, bob_bases
        )

        # ── 步骤 6: 计算 QBER ──
        qber, n_errors, n_sample = utils.compute_qber(
            alice_sifted, bob_sifted, sample_fraction, self.rng
        )

        t_elapsed = time.perf_counter() - t_start

        self.results = {
            "qber": qber,
            "n_errors": n_errors,
            "n_sample": n_sample,
            "sifted_len": len(alice_sifted),
            "alice_sifted": alice_sifted,
            "bob_sifted": bob_sifted,
            "eve_present": eve_present,
            "n_qubits": n_qubits,
            "elapsed": t_elapsed,
        }
        return self.results

    def print_report(self) -> str:
        """打印格式化的仿真报告。"""
        if not self.results:
            return "尚未运行仿真。请先调用 run() 方法。"
        report = utils.format_report(
            n_qubits=self.results["n_qubits"],
            sifted_len=self.results["sifted_len"],
            qber=self.results["qber"],
            n_errors=self.results["n_errors"],
            n_sample=self.results["n_sample"],
            eve_present=self.results["eve_present"],
            elapsed=self.results["elapsed"],
        )
        print(report, end="")
        return report

    def run_comparison(
        self,
        n_qubits: int = 1000,
        sample_fraction: float = 0.5,
        plot: bool = False,
        save_plot: str | None = None,
    ) -> dict:
        """对比运行有 Eve 和无 Eve 两种场景并输出结果。"""
        # 无 Eve
        result_clean = self.run(n_qubits=n_qubits, eve_present=False, sample_fraction=sample_fraction)
        print("【场景 1】无 Eve（理想信道）")
        self.print_report()

        # 有 Eve
        result_eve = self.run(n_qubits=n_qubits, eve_present=True, sample_fraction=sample_fraction)
        print("\n【场景 2】存在 Eve（截获-重发攻击）")
        self.print_report()

        if plot or save_plot:
            utils.plot_qber_comparison(
                qber_no_eve=result_clean["qber"],
                qber_with_eve=result_eve["qber"],
                save_path=save_plot,
            )

        return {"no_eve": result_clean, "with_eve": result_eve}
