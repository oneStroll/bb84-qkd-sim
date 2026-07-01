"""Alice 模块：发送方。

在 BB84 协议中，Alice 随机生成比特串和测量基，
将每个比特用对应基编码到量子态上发送给 Bob。
"""

import numpy as np

BASES = ("Z", "X")


class Alice:
    """模拟 BB84 协议中的发送方 Alice。

    Alice 随机生成原始比特和编码基，并将 (比特, 基) 对发送出去。
    在经典后处理阶段，Alice 与 Bob 比对测量基，筛选出 sifted key。
    """

    def __init__(self, rng: np.random.Generator | None = None):
        self.rng = rng or np.random.default_rng()

    def generate_bits(self, n: int) -> np.ndarray:
        """生成长度为 n 的随机比特串 (0/1)。"""
        return self.rng.integers(0, 2, size=n)

    def generate_bases(self, n: int) -> np.ndarray:
        """随机选择 n 个编码基 ('Z' 或 'X')。"""
        return self.rng.choice(BASES, size=n)

    def prepare_qubits(self, n: int):
        """完整执行：生成比特 + 选择基，返回 (bits, bases)。"""
        bits = self.generate_bits(n)
        bases = self.generate_bases(n)
        return bits, bases

    def sift_key(
        self,
        alice_bits: np.ndarray,
        alice_bases: np.ndarray,
        bob_bases: np.ndarray,
    ) -> np.ndarray:
        """基比对后筛选 Alice 的 sifted key。

        只保留 Bob 测量基与 Alice 编码基一致的比特位。
        Bob 公开自己的测量基（不公开结果），Alice 据此筛选。
        """
        match = alice_bases == bob_bases
        return alice_bits[match]
