"""BB84 协议流程完整性测试。"""

import numpy as np
from bb84_sim import BB84Protocol
from bb84_sim.alice import Alice
from bb84_sim.bob import Bob
from bb84_sim.eve import Eve
from bb84_sim import utils


class TestAlice:
    def test_generate_bits_length(self):
        alice = Alice()
        bits = alice.generate_bits(100)
        assert len(bits) == 100
        assert bits.dtype == int

    def test_generate_bits_values(self):
        alice = Alice()
        bits = alice.generate_bits(1000)
        assert set(bits).issubset({0, 1}), "比特只能为 0 或 1"

    def test_generate_bases_values(self):
        alice = Alice()
        bases = alice.generate_bases(100)
        assert set(bases).issubset({"Z", "X"}), "基只能为 'Z' 或 'X'"

    def test_sift_key_matching(self):
        """验证筛选只保留基一致的位。"""
        alice = Alice()
        bits = np.array([0, 1, 0, 1])
        alice_bases = np.array(["Z", "X", "Z", "X"])
        bob_bases = np.array(["Z", "Z", "X", "X"])
        sifted = alice.sift_key(bits, alice_bases, bob_bases)
        # 位置 0 (Z==Z) 和位置 3 (X==X) 保留 → [0, 1]
        assert np.array_equal(sifted, [0, 1])


class TestBob:
    def test_measure_matching_basis(self):
        """基一致时测量结果应确定。"""
        bob = Bob()
        bits = np.array([0, 1, 1, 0])
        alice_bases = np.array(["Z", "X", "Z", "X"])
        bob_bases = np.array(["Z", "X", "Z", "X"])
        result = bob.measure(bits, alice_bases, bob_bases)
        assert np.array_equal(result, bits), "基一致时测量结果应与原始比特一致"

    def test_measure_mismatch_basis(self):
        """基不一致时测量结果应为 0 或 1（正常执行不抛异常）。"""
        bob = Bob()
        bits = np.array([0, 1, 1, 0])
        alice_bases = np.array(["Z", "X", "Z", "X"])
        bob_bases = np.array(["X", "Z", "X", "Z"])
        result = bob.measure(bits, alice_bases, bob_bases)
        assert set(result).issubset({0, 1})


class TestEve:
    def test_intercept_resend_output_length(self):
        eve = Eve()
        bits = np.array([0, 1, 0, 1, 1, 0])
        bases = np.array(["Z", "X", "Z", "X", "Z", "X"])
        intercepted, intercepted_bases = eve.intercept_resend(bits, bases)
        assert len(intercepted) == len(bits)
        assert len(intercepted_bases) == len(bases)

    def test_intercept_resend_values(self):
        eve = Eve()
        bits = np.array([0, 1, 0, 1])
        bases = np.array(["Z", "X", "Z", "X"])
        intercepted, intercepted_bases = eve.intercept_resend(bits, bases)
        assert set(intercepted).issubset({0, 1})
        assert set(intercepted_bases).issubset({"Z", "X"})


class TestUtils:
    def test_sift_keys(self):
        alice_bits = np.array([0, 1, 0, 1])
        bob_bits = np.array([0, 1, 1, 0])
        alice_bases = np.array(["Z", "X", "Z", "X"])
        bob_bases = np.array(["Z", "Z", "X", "X"])
        a_sifted, b_sifted = utils.sift_keys(
            alice_bits, bob_bits, alice_bases, bob_bases
        )
        # 位置 0 (Z==Z) → [0,0]; 位置 3 (X==X) → [1,0]
        assert np.array_equal(a_sifted, [0, 1])
        assert np.array_equal(b_sifted, [0, 0])

    def test_compute_qber_identical_keys(self):
        """相同密钥的 QBER 应为 0。"""
        key = np.array([0, 1, 0, 1, 1, 0, 1, 0, 0, 1])
        qber, errors, n = utils.compute_qber(key, key, sample_fraction=1.0)
        assert qber == 0.0
        assert errors == 0


class TestProtocol:
    def test_run_returns_dict(self):
        protocol = BB84Protocol(seed=42)
        result = protocol.run(n_qubits=100, eve_present=False)
        required_keys = {"qber", "n_errors", "n_sample", "sifted_len",
                         "alice_sifted", "bob_sifted", "eve_present"}
        assert required_keys.issubset(result.keys())

    def test_eve_present_flag(self):
        protocol = BB84Protocol(seed=42)
        r1 = protocol.run(n_qubits=100, eve_present=False)
        r2 = protocol.run(n_qubits=100, eve_present=True)
        assert r1["eve_present"] is False
        assert r2["eve_present"] is True

    def test_alice_bob_sifted_same_length(self):
        protocol = BB84Protocol(seed=42)
        result = protocol.run(n_qubits=1000, eve_present=False)
        assert len(result["alice_sifted"]) == len(result["bob_sifted"])
