"""Eve 模块：窃听者（攻击者）。

Eve 实施"截获-重发攻击"（Intercept-resend attack）：
1. 截获 Alice 发送的量子态
2. 随机选择测量基进行测量
3. 根据测量结果重新制备量子态并发给 Bob

由于 Eve 不知道 Alice 使用的编码基，她的测量会引入扰动，
这种扰动会反映在 QBER 的升高上，从而被 Alice 和 Bob 发现。
"""

import numpy as np

from .alice import BASES


class Eve:
    """模拟 BB84 协议中的窃听者 Eve（截获-重发攻击）。

    截获-重发攻击的效果：
    - Eve 选对基的概率：50%（此时她不引入错误）
    - Eve 选错基的概率：50%（此时她以 50% 概率转发错误比特）
    - 总体 Eve 引入的 QBER ≈ 25%
    """

    def __init__(self, rng: np.random.Generator | None = None):
        self.rng = rng or np.random.default_rng()
        self.intercepted_bits: np.ndarray | None = None
        self.intercepted_bases: np.ndarray | None = None

    def intercept_resend(
        self, alice_bits: np.ndarray, alice_bases: np.ndarray
    ) -> np.ndarray:
        """实施截获-重发攻击。

        步骤：
        1. Eve 随机选择测量基
        2. Eve"测量"截获的量子态：获取测量结果比特
        3. Eve 基于自己的测量结果重新制备量子态并发给 Bob

        返回: 转发给 Bob 的比特串（即篡改后的比特）
        """
        n = len(alice_bits)
        self.intercepted_bases = self.rng.choice(BASES, size=n)

        # Eve 测量 Alice 的量子态
        match = self.intercepted_bases == alice_bases
        eve_bits = np.zeros(n, dtype=int)
        eve_bits[match] = alice_bits[match]          # 选对基 → 正确测量
        eve_bits[~match] = self.rng.integers(0, 2, size=np.sum(~match))  # 选错基 → 随机结果

        self.intercepted_bits = eve_bits.copy()

        # Eve 根据测量结果重发（即把 eve_bits 当作发送给 Bob 的"原始比特"）
        # 同时 Eve 用自己的测量基作为"编码基"重发
        # 返回 (转发的比特, 转发的基)
        return eve_bits, self.intercepted_bases
