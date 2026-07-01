# BB84 协议的物理背景与数学形式化

## 1. 量子比特与狄拉克符号

量子比特（qubit）是量子信息的基本单元，表示为二维 Hilbert 空间 $\mathcal{H} \cong \mathbb{C}^2$ 中的归一化向量。在 Dirac 符号中，计算基（Z 基）的两个正交基矢为：

$$
|0\rangle = \begin{pmatrix} 1 \\ 0 \end{pmatrix}, \quad
|1\rangle = \begin{pmatrix} 0 \\ 1 \end{pmatrix}
$$

任意单量子纯态可表示为：

$$
|\psi\rangle = \alpha|0\rangle + \beta|1\rangle, \quad |\alpha|^2 + |\beta|^2 = 1
$$

## 2. BB84 协议的四个量子态

BB84 协议使用两组共轭基（Conjugate Bases），每组包含两个正交态：

### Z 基（标准计算基 / 直线基）

$$
|0\rangle, \quad |1\rangle
$$

### X 基（Hadamard 基 / 对角基）

$$
|+\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle), \quad
|-\rangle = \frac{1}{\sqrt{2}}(|0\rangle - |1\rangle)
$$

两组基之间的关系由 Hadamard 变换联系：

$$
H = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}, \quad
|+\rangle = H|0\rangle, \quad |-\rangle = H|1\rangle
$$

**关键性质**：两组基是共轭的（mutually unbiased），即一组基中的任一态在另一组基的任意态上的投影模平方恒为 $1/2$：

$$
|\langle 0 | + \rangle|^2 = |\langle 0 | - \rangle|^2 = |\langle 1 | + \rangle|^2 = |\langle 1 | - \rangle|^2 = \frac{1}{2}
$$

这意味着一组基中的量子态在另一组基上测量时，结果是完全随机的。

## 3. 编码方案

| 编码比特 | Z 基 | X 基 |
|---------|------|------|
| 0 | $|0\rangle$ | $|+\rangle = \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)$ |
| 1 | $|1\rangle$ | $|-\rangle = \frac{1}{\sqrt{2}}(|0\rangle - |1\rangle)$ |

## 4. 协议流程的形式化描述

### 第 1 步：Alice 制备量子态

Alice 随机生成长度为 $n$ 的经典比特串 $\mathbf{b} = \{b_1, b_2, ..., b_n\}$ 和编码基序列 $\mathbf{\theta} = \{\theta_1, \theta_2, ..., \theta_n\}$，其中 $\theta_i \in \{Z, X\}$。

根据编码方案，Alice 制备 $n$ 个量子态：

$$
|\psi_i\rangle = \begin{cases}
|b_i\rangle & \text{if } \theta_i = Z \\
H|b_i\rangle & \text{if } \theta_i = X
\end{cases}
$$

### 第 2 步：量子信道传输（理想情况）

Alice 将 $n$ 个量子态通过量子信道发送给 Bob。

### 第 2b 步：Eve 截获-重发攻击（攻击场景）

Eve 截获所有量子态，对每个 $|\psi_i\rangle$ 随机选择测量基 $\gamma_i \in \{Z, X\}$ 进行测量。

根据量子测量公设（Measurement Postulate），测量过程由一组投影算子 $\{P_m\}$ 描述：

- 若 $\gamma_i = Z$：投影算子为 $\{|0\rangle\langle 0|, |1\rangle\langle 1|\}$
- 若 $\gamma_i = X$：投影算子为 $\{|+\rangle\langle +|, |-\rangle\langle -|\}$

测量结果 $e_i$ 的概率由 Born 规则给出：

$$
p(e_i) = \langle\psi_i|P_{e_i}|\psi_i\rangle
$$

测量后，量子态坍缩到 $P_{e_i}$ 对应的本征态 $|\phi_i\rangle$。Eve 将此坍缩后的量子态 $|\phi_i\rangle$ 转发给 Bob。

**关键洞察**：当 $\gamma_i \neq \theta_i$（Eve 选错基）时：
- Eve 以 50% 概率得到 $e_i = 0$，以 50% 概率得到 $e_i = 1$
- 无论得到哪个结果，转发的量子态都与 Alice 的原始态不同
- 这将在 Alice 和 Bob 的最终密钥中引入误码

### 第 3 步：Bob 测量

Bob 对每个接收到的量子态随机选择测量基 $\beta_i \in \{Z, X\}$ 进行测量，得到结果 $\tilde{b}_i$。

测量过程的数学描述：

- 若 $\beta_i = \theta_i$（基一致）：测量结果确定，$\tilde{b}_i = b_i$
- 若 $\beta_i \neq \theta_i$（基不一致）：测量结果以 50% 概率为 0，50% 概率为 1

证明（以 Alice 发送 $|0\rangle$、Bob 用 X 基测量为例）：

$$
|\langle+ | 0\rangle|^2 = \left|\frac{1}{\sqrt{2}}(\langle 0| + \langle 1|)|0\rangle\right|^2 = \left|\frac{1}{\sqrt{2}}\right|^2 = \frac{1}{2}
$$

$$
|\langle- | 0\rangle|^2 = \left|\frac{1}{\sqrt{2}}(\langle 0| - \langle 1|)|0\rangle\right|^2 = \left|\frac{1}{\sqrt{2}}\right|^2 = \frac{1}{2}
$$

### 第 4 步：基比对（Sifting）

Bob 通过经典信道广播自己的测量基序列 $\mathbf{\beta}$（**不广播测量结果**）。
Alice 和 Bob 各自保留 $\theta_i = \beta_i$ 的位置上的比特，丢弃其余比特。

保留的位置集合：

$$
S = \{i \;|\; \theta_i = \beta_i\}
$$

Alice 的 sifted key：$\mathbf{k}_A = \{b_i\}_{i \in S}$
Bob 的 sifted key：$\mathbf{k}_B = \{\tilde{b}_i\}_{i \in S}$

由于 $\theta_i$ 和 $\beta_i$ 都是独立均匀随机选择的，$\mathbb{P}(\theta_i = \beta_i) = \frac{1}{2}$，因此 sifted key 的预期长度约为 $n/2$。

### 第 5 步：QBER 估算

Alice 和 Bob 从各自的 sifted key 中随机选取相同位置的子集 $T \subset S$ 进行公开比对。量子误码率定义为：

$$
\text{QBER} = \frac{\#\{i \in T \;|\; k_{A,i} \neq k_{B,i}\}}{|T|}
$$

### 第 6 步：密钥提取

如果 QBER 低于安全阈值（通常 $\text{QBER} \lesssim 11\%$），Alice 和 Bob 认为信道安全，将剩余未公开的比特 $S \setminus T$ 作为原始密钥。

## 5. 无 Eve 时的 QBER 分析

在理想信道（无噪声、无窃听）中：

- 当 $\theta_i = \beta_i$ 时：$\tilde{b}_i = b_i$ 确定成立
- $\{\theta_i = \beta_i\}$ 的概率为 $1/2$

因此在 sifted key 中，Alice 和 Bob 的比特完全相同，QBER = 0。

## 6. 有 Eve（截获-重发）时的 QBER 分析

考虑 Eve 对每个量子态实施截获-重发攻击。Eve 随机选择测量基 $\gamma_i$。

### 6.1 条件概率分析

对于任意位置 $i$，考虑 Alice 和 Bob 基一致的情况（$\theta_i = \beta_i$）：

| Eve 的基 $\gamma_i$ | 概率 | 条件 | 结果 |
|:---:|:---:|:---|:---:|
| $\gamma_i = \theta_i$ | $1/2$ | Eve 选对基，不引入错误 | $\tilde{b}_i = b_i$ |
| $\gamma_i \neq \theta_i$ | $1/2$ | Eve 选错基，测量结果 $e_i$ 随机 | 以 $1/2$ 概率 $\tilde{b}_i = b_i$（偶然正确）<br/>以 $1/2$ 概率 $\tilde{b}_i \neq b_i$（错误） |

### 6.2 QBER 计算

$$
\begin{aligned}
\text{QBER} &= \mathbb{P}(\tilde{b}_i \neq b_i \;|\; \theta_i = \beta_i) \\
&= \mathbb{P}(\gamma_i \neq \theta_i) \times \mathbb{P}(\tilde{b}_i \neq b_i \;|\; \gamma_i \neq \theta_i, \theta_i = \beta_i) \\
&= \frac{1}{2} \times \frac{1}{2} \\
&= \frac{1}{4} = 25\%
\end{aligned}
$$

### 6.3 物理直觉

- Eve 不知道 Alice 使用的编码基，所以她有 50% 的概率选错基
- 当 Eve 选错基时，她的测量结果与 Alice 的比特无关（完全随机）
- Eve 基于错误的测量结果重发后，Bob 即使使用正确的基测量，也有 50% 的概率得到与 Alice 不同的比特
- 因此总体误码率为 $1/2 \times 1/2 = 1/4$

### 6.4 安全阈值

如果 Alice 和 Bob 观测到 QBER > 11%，他们可以确定存在窃听者（Eve），并丢弃该次通信的密钥。11% 的安全阈值来源于考虑更复杂攻击（如 PNS 攻击）时的信息论分析。

## 7. 代码实现与物理图像的对应关系

```python
# ── Alice 随机选择编码基 ──
alice_bases = np.random.choice(["Z", "X"], size=n)

# ── Eve 截获-重发 ──
eve_bases = np.random.choice(["Z", "X"], size=n)
# Eve 在正确基上测得正确结果
eve_bits[eve_bases == alice_bases] = alice_bits[eve_bases == alice_bases]
# Eve 在错误基上测得随机结果
eve_bits[eve_bases != alice_bases] = np.random.randint(0, 2, ...)

# ── Bob 测量 ──
bob_bases = np.random.choice(["Z", "X"], size=n)
# 基一致 → 确定结果
bob_bits[match] = received_bits[match]
# 基不一致 → 随机结果
bob_bits[~match] = np.random.randint(0, 2, ...)
```

代码中的 `np.random.choice` 统计模拟了量子测量的概率性质——当测量基与量子态基一致时获得确定结果，不一致时获得随机结果，这正是 Born 规则的体现。

## 参考文献

1. Bennett, C. H., & Brassard, G. (1984). Quantum cryptography: Public key distribution and coin tossing. *Proceedings of IEEE International Conference on Computers, Systems and Signal Processing*, 175-179.
2. Nielsen, M. A., & Chuang, I. L. (2010). *Quantum Computation and Quantum Information: 10th Anniversary Edition*. Cambridge University Press.
3. Scarani, V., et al. (2009). The security of practical quantum key distribution. *Reviews of Modern Physics*, 81(3), 1301-1350.
