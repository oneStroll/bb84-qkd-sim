# BB84 协议的物理背景与数学形式化

## 1. 量子比特与狄拉克符号

量子比特（qubit）是量子信息的基本单元，表示为二维 Hilbert 空间 ℋ ≅ ℂ² 中的归一化向量。在 Dirac 符号中，计算基（Z 基）的两个正交基矢为：

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
|:--------:|:----:|:----:|
| 0 | ∣0⟩ | ∣+⟩ = (∣0⟩ + ∣1⟩)/√2 |
| 1 | ∣1⟩ | ∣-⟩ = (∣0⟩ - ∣1⟩)/√2 |

## 4. 协议流程的形式化描述

### 第 1 步：Alice 制备量子态

Alice 随机生成长度为 $n$ 的经典比特串 $\mathbf{b} = \{b\_1, b\_2, ..., b\_n\}$ 和编码基序列 $\mathbf{\theta} = \{\theta\_1, \theta\_2, ..., \theta\_n\}$，其中 $\theta\_i \in \{Z, X\}$。

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

Eve 截获所有量子态，对每个 $\vert\psi\_i\rangle$ 随机选择测量基 $\gamma\_i \in \{Z, X\}$ 进行测量。

根据量子测量公设（Measurement Postulate），测量过程由一组投影算子 $\{P\_m\}$ 描述：

- 若 $\gamma\_i = Z$：投影算子为 $\{\vert 0\rangle\langle 0\vert, \vert 1\rangle\langle 1\vert\}$
- 若 $\gamma\_i = X$：投影算子为 $\{\vert +\rangle\langle +\vert, \vert -\rangle\langle -\vert\}$

测量结果 $e\_i$ 的概率由 Born 规则给出：

$$
p(e_i) = \langle\psi_i|P_{e_i}|\psi_i\rangle
$$

测量后，量子态坍缩到 $P\_{e\_i}$ 对应的本征态 $\vert\phi\_i\rangle$。Eve 将此坍缩后的量子态 $\vert\phi\_i\rangle$ 转发给 Bob。

**关键洞察**：当 $\gamma\_i \neq \theta\_i$（Eve 选错基）时：
- Eve 以 50% 概率得到 $e\_i = 0$，以 50% 概率得到 $e\_i = 1$
- 无论得到哪个结果，转发的量子态都与 Alice 的原始态不同
- 这将在 Alice 和 Bob 的最终密钥中引入误码

### 第 3 步：Bob 测量

Bob 对每个接收到的量子态随机选择测量基 $\beta\_i \in \{Z, X\}$ 进行测量，得到结果 $\tilde{b}\_i$。

测量过程的数学描述：

- 若 $\beta\_i = \theta\_i$（基一致）：测量结果确定，$\tilde{b}\_i = b\_i$
- 若 $\beta\_i \neq \theta\_i$（基不一致）：测量结果以 50% 概率为 0，50% 概率为 1

证明（以 Alice 发送 $\vert 0\rangle$、Bob 用 X 基测量为例）：

$$
\vert\langle+ \vert 0\rangle\vert^2 = \left\vert\frac{1}{\sqrt{2}}(\langle 0\vert + \langle 1\vert)\vert 0\rangle\right\vert^2 = \left\vert\frac{1}{\sqrt{2}}\right\vert^2 = \frac{1}{2}
$$

$$
\vert\langle- \vert 0\rangle\vert^2 = \left\vert\frac{1}{\sqrt{2}}(\langle 0\vert - \langle 1\vert)\vert 0\rangle\right\vert^2 = \left\vert\frac{1}{\sqrt{2}}\right\vert^2 = \frac{1}{2}
$$

### 第 4 步：基比对（Sifting）

Bob 通过经典信道广播自己的测量基序列 $\mathbf{\beta}$（**不广播测量结果**）。
Alice 和 Bob 各自保留 $\theta\_i = \beta\_i$ 的位置上的比特，丢弃其余比特。

保留的位置集合：

$$
S = \{i \mid \theta_i = \beta_i\}
$$

Alice 的 sifted key：$\mathbf{k}\_A = \{b\_i\}\_{i\in S}$
Bob 的 sifted key：$\mathbf{k}\_B = \{\tilde{b}\_i\}\_{i\in S}$

由于 $\theta\_i$ 和 $\beta\_i$ 都是独立均匀随机选择的，$\mathbb{P}(\theta\_i = \beta\_i) = \frac{1}{2}$，因此 sifted key 的预期长度约为 $n/2$。

### 第 5 步：QBER 估算

Alice 和 Bob 从各自的 sifted key 中随机选取相同位置的子集 $T \subset S$ 进行公开比对。量子误码率定义为：

$$
\text{QBER} = \frac{|\{i \in T \mid k_{A,i} \neq k_{B,i}\}|}{|T|}
$$

### 第 6 步：密钥提取

如果 QBER 低于安全阈值（通常 $\text{QBER} \lesssim 11\%$），Alice 和 Bob 认为信道安全，将剩余未公开的比特 $S \setminus T$ 作为原始密钥。

## 5. 无 Eve 时的 QBER 分析

在理想信道（无噪声、无窃听）中：

- 当 $\theta\_i = \beta\_i$ 时：$\tilde{b}\_i = b\_i$ 确定成立
- $\{\theta\_i = \beta\_i\}$ 的概率为 $1/2$

因此在 sifted key 中，Alice 和 Bob 的比特完全相同，QBER = 0。

## 6. 有 Eve（截获-重发）时的 QBER 分析

考虑 Eve 对每个量子态实施截获-重发攻击。Eve 随机选择测量基 $\gamma\_i$。

### 6.1 条件概率分析

对于任意位置 $i$，考虑 Alice 和 Bob 基一致的情况（$\theta\_i = \beta\_i$）：

| Eve 的基 $\gamma\_i$ | 概率 | 条件 | 结果 |
|:---:|:---:|:---|:---|
| $\gamma\_i = \theta\_i$ | $1/2$ | Eve 选对基，不引入错误 | $\tilde{b}\_i = b\_i$ |
| $\gamma\_i \neq \theta\_i$ | $1/2$ | Eve 选错基，测量结果 $e\_i$ 随机 | 以 $1/2$ 概率 $\tilde{b}\_i = b\_i$（偶然正确），或以 $1/2$ 概率 $\tilde{b}\_i \neq b\_i$（错误） |

### 6.2 QBER 计算

$$
\begin{aligned}
\text{QBER} &= \mathbb{P}(\tilde{b}_i \neq b_i \mid \theta_i = \beta_i) \\
&= \mathbb{P}(\gamma_i \neq \theta_i) \times \mathbb{P}(\tilde{b}_i \neq b_i \mid \gamma_i \neq \theta_i, \theta_i = \beta_i) \\
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

### 7.1 Alice 编码：经典比特 → 量子态

```python
# 核心代码
bits = alice.generate_bits(n)     # 随机比特串 b_i ∈ {0, 1}
bases = alice.generate_bases(n)    # 随机编码基 θ_i ∈ {Z, X}
```

**物理图像**：Alice 将每个经典比特 $b\_i$ 编码到量子态 $\vert\psi\_i\rangle$ 上：

$$
|\psi_i\rangle = \begin{cases}
|b_i\rangle & \text{if } \theta_i = Z \quad\text{(计算基)} \\\\
H|b_i\rangle & \text{if } \theta_i = X \quad\text{(Hadamard 基)}
\end{cases}
$$

其中

$$
H = \frac{1}{\sqrt{2}}\begin{pmatrix}1&1\\ 1 & -1\end{pmatrix}
$$

是 Hadamard 门。当 $\theta\_i = X$ 时，$H$ 将计算基矢映射到对角基矢：

$$
H|0\rangle = |+\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}},\quad
H|1\rangle = |-\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}}
$$

**物理含义**：随机选择编码基是 BB84 协议安全性的核心。如果 Alice 只用一组基编码，Eve 可以用相同基直接测量而不引入扰动。

---

### 7.2 Eve 截获-重发：量子测量坍缩

```python
# 核心代码
eve_bases = np.random.choice(["Z", "X"], size=n)      # Eve 随机选测量基 γ_i

# 基一致时：测量结果确定
eve_bits[eve_bases == alice_bases] = alice_bits[...]

# 基不一致时：测量结果随机（Born 规则）
eve_bits[eve_bases != alice_bases] = np.random.randint(0, 2, ...)
```

**物理图像**：Eve 截获量子态 $\vert\psi\_i\rangle$ 并用基 $\gamma\_i$ 测量。根据量子测量公设（Measurement Postulate），测量由投影算子描述：

- $\gamma\_i = Z$ 时：投影算子 $\{P\_0, P\_1\} = \{\vert0\rangle\langle 0\vert, \vert1\rangle\langle 1\vert\}$
- $\gamma\_i = X$ 时：投影算子 $\{P\_0, P\_1\} = \{\vert+\rangle\langle +\vert, \vert-\rangle\langle -\vert\}$

测量结果 $e\_i$ 的概率由 **Born 规则** 给出：

$$
p(e_i = 0) = \langle\psi_i|P_0|\psi_i\rangle,\quad
p(e_i = 1) = \langle\psi_i|P_1|\psi_i\rangle
$$

- 当 $\gamma\_i = \theta\_i$（Eve 选对基）：$p(e\_i = b\_i) = 1$，结果确定
- 当 $\gamma\_i \neq \theta\_i$（Eve 选错基）：$p(e\_i=0) = p(e\_i=1) = 1/2$，结果完全随机

**代码对应**：`np.random.randint(0, 2)` 模拟了"测量基不匹配时结果各 50% 概率"这一量子效应，本质是 Born 规则中投影模平方 $\vert\langle\phi\_j\vert\psi\_i\rangle\vert^2$ 的离散采样。

测量后量子态坍缩到 $P\_{e\_i}$ 对应的本征态 $\vert\phi\_i\rangle$，Eve 将此坍缩态转发给 Bob。Eve 无法复制未知量子态——这是**不可克隆定理**（No-cloning Theorem）的直接推论。

---

### 7.3 Bob 测量：基比对与结果筛选

```python
# 核心代码
bob_bases = self.bob.generate_bases(n)     # Bob 随机选测量基 β_i
bob_bits = self.bob.measure(...)            # 测量

# Alice & Bob 公开基（不公开比特），只保留基一致的位置
match = alice_bases == bob_bases
alice_sifted = alice_bits[match]
bob_sifted = bob_bits[match]
```

**物理图像**：
- 若 $\beta\_i = \theta\_i$（基一致）：测量结果确定，$\tilde{b}\_i = b\_i$
- 若 $\beta\_i \neq \theta\_i$（基不一致）：$\tilde{b}\_i$ 以 50% 概率为 0 或 1

**基比对**（Basis Sifting）是 BB84 的关键后处理步骤。Bob 通过经典信道公开自己的测量基序列 $\mathbf{\beta}$（**不公开测量结果**）。双方丢弃 $\theta\_i \neq \beta\_i$ 的位置，保留 $\theta\_i = \beta\_i$ 的位作为 sifted key：

$$
\mathbf{k}_A = \{b_i\}_{\{i: \theta_i = \beta_i\}},\quad
\mathbf{k}_B = \{\tilde{b}_i\}_{\{i: \theta_i = \beta_i\}}
$$

由于 $\theta\_i, \beta\_i$ 独立随机，$P(\theta\_i = \beta\_i) = 1/2$，sifted key 长度约为 $n/2$。

---

### 7.4 QBER 计算：Eve 存在的检测

```python
# 从 sifted key 中随机抽样比对
n_sample = int(len(alice_sifted) * sample_fraction)
indices = np.random.choice(len(alice_sifted), n_sample, replace=False)
n_errors = np.sum(alice_sifted[indices] != bob_sifted[indices])
qber = n_errors / n_sample
```

**物理图像**：考虑 Alice 和 Bob 基一致（即 $i \in S$）的位置，Eve 截获-重发攻击引入的 QBER 为：

$$
\begin{aligned}
\text{QBER} &= \mathbb{P}(\tilde{b}_i \neq b_i \mid \theta_i = \beta_i) \\
&= \mathbb{P}(\gamma_i \neq \theta_i) \times \mathbb{P}(\tilde{b}_i \neq b_i \mid \gamma_i \neq \theta_i, \theta_i = \beta_i) \\
&= \frac{1}{2} \times \frac{1}{2} = \frac{1}{4} = 25\%
\end{aligned}
$$

**安全性阈值**：若检测到 QBER $> 11\%$，双方可确信存在窃听者并丢弃密钥。11% 来自信息论分析——当误码率超过此值时，Eve 可能获取足够信息量。

---

### 7.5 核心物理原理总结

| 代码行 | 物理原理 | 狄拉克符号表达 |
|--------|---------|---------------|
| `alice.generate_bases(n)` | 共轭基编码 | $\theta\_i \in \{Z, X\}$ |
| `eve_bases != alice_bases` | 测量坍缩 + Born 规则 | $p(e\_i) = \vert\langle e\_i\vert \psi\_i\rangle\vert^2$ |
| `np.random.randint(0, 2)` | 非共轭基测量随机性 | $\vert\langle 0\vert+\rangle\vert^2 = \vert\langle 1\vert+\rangle\vert^2 = 1/2$ |
| `alice_bases == bob_bases` | 基比对（Sifting） | $S = \{i \mid \theta\_i = \beta\_i\}$ |
| `n_errors / n_sample` | QBER = 25% 检测 Eve | $\text{QBER} = 1/2 \times 1/2 = 1/4$ |

