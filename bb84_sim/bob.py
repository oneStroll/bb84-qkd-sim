"""Bob 模块：接收方。

Bob 随机选择测量基来测量 Alice 发送的量子态，
之后与 Alice 公开比对测量基以筛选出 sifted key。
"""

import numpy as np

from .alice import BASES


class Bob:
    """模拟 BB84 协议中的接收方 Bob。

    Bob 随机选择测量基进行测量，测量结果取决于他的基与 Alice 的基是否一致。
    如果基一致：测量结果确定（与 Alice 编码一致）。
    如果基不一致：测量结果完全随机（50% 概率得到 0 或 1）。

    这一行为源自量子力学中的"不可克隆定理"和"测量坍缩"：
    - 当测量基与量子态基一致时，测量结果确定
    - 当测量基不匹配时，量子态坍缩到测量基的本征态，结果随机
    """

    def __init__(self, rng: np.random.Generator | None = None):
        self.rng = rng or np.random.default_rng()

    def generate_bases(self, n: int) -> np.ndarray:
        """随机选择 n 个测量基 ('Z' 或 'X')。"""
        return self.rng.choice(BASES, size=n)

    def measure(
        self, alice_bits: np.ndarray, alice_bases: np.ndarray, bob_bases: np.ndarray
    ) -> np.ndarray:
        """模拟测量过程，返回 Bob 测量得到的比特串。

        物理图像：
        - 如果 Bob 的测量基与 Alice 的编码基匹配 → 测量结果确定 = Alice 的比特
        - 如果不匹配 → 测量结果随机（量子态坍缩到测量基的本征态）

        参数:
            alice_bits: Alice 发送的原始比特
            alice_bases: Alice 的编码基
            bob_bases: Bob 的测量基
        """
        match = alice_bases == bob_bases
        n = len(alice_bits)
        bob_bits = np.zeros(n, dtype=int)

        # 基一致 → 确定结果
        bob_bits[match] = alice_bits[match]
        # 基不一致 → 随机结果
        bob_bits[~match] = self.rng.integers(0, 2, size=np.sum(~match))

        return bob_bits

    def sift_key(self, bob_bits: np.ndarray, alice_bases: np.ndarray, bob_bases: np.ndarray) -> np.ndarray:
        """基比对后筛选 Bob 的 sifted key。"""
        match = alice_bases == bob_bases
        return bob_bits[match]
