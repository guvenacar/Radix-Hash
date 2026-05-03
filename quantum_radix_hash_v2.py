#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quantum-Hybrid Radix-Hash v2
============================
Kuantum S-box pow(a,b,M) girdilerine entegre edildi.
Klasik: pow(a, b, M)
Yeni:   pow(sbox[a], sbox[b], M)  ← kuantum devre tabanlı S-box

TEKNOFEST 2026
"""

import sys
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import Aer

sys.path.insert(0, '.')
from model.radix_hash import text_to_bits, pad_bits, chunks, normalize_bits
from utils.balance_transforms import xor_not_reverse_dynamic_count

M = 3 ** 486
BITS_PER_BLOCK = 772

# ── Kuantum S-box ──────────────────────────────────────────
def build_quantum_sbox(n_bits=4):
    """
    16 girdi için bijektif kuantum S-box üretir.
    H + Ry + Rz + CX kapıları, statevector tabanlı, deterministik.
    Bir kez çağrılır, önbelleğe alınır.
    """
    backend = Aer.get_backend('statevector_simulator')

    def raw(val):
        qc = QuantumCircuit(n_bits)
        for i in range(n_bits):
            if (val >> i) & 1:
                qc.x(i)
        for i in range(n_bits):
            qc.h(i)
            angle = (val * (i + 1) * np.pi) / 16
            qc.ry(angle, i)
            qc.rz(angle / (i + 1), i)
        for i in range(n_bits - 1):
            qc.cx(i, i + 1)
        sv = np.asarray(backend.run(qc).result().get_statevector())
        result = 0
        for i, amp in enumerate(sv):
            re = int(amp.real * (2**20)) & 0xFFFFF
            im = int(amp.imag * (2**20)) & 0xFFFFF
            result ^= ((re << 20) | im) << (i % 8)
        return abs(result)

    raw_vals = [raw(v) for v in range(16)]
    ranked = sorted(range(16), key=lambda i: raw_vals[i])
    sbox = [0] * 16
    for rank, orig in enumerate(ranked):
        sbox[orig] = rank + 2
    return sbox


# ── Kuantum S-box entegre çekirdek ─────────────────────────
def hash_block_quantum_sbox(bits: str, sbox: list) -> str:
    """
    pow(a, b, M) girdileri kuantum S-box'tan geçirilir.
    """
    n = 0
    for bit in bits:
        n = n * 3 + (1 if bit == "0" else 2)
    hexstr = format(n, "x")
    vals = [int(ch, 16) + 2 for ch in hexstr]
    vals_q = [sbox[v - 2] for v in vals]

    total = 2
    term = 0
    i = 0
    while i < len(vals_q) - 1:
        a, b = vals_q[i], vals_q[i + 1]
        term = (term + pow(a, b, M)) % M
        total = (total * term) % M
        i += 2
    if i < len(vals_q):
        term = pow(vals_q[i], 3, M)
        total = (total + term) % M
    if total.bit_length() < 771:
        total = 2 * M - total
    elif total.bit_length() == 771:
        total += 1
    return format(total, "x")


# ── Ana hash fonksiyonu ─────────────────────────────────────
_SBOX_CACHE = None

def quantum_radix_hash(input_data: str) -> str:
    """
    772-bit binary string döndürür.
    S-box ilk çağrıda oluşturulur, önbelleğe alınır.
    """
    global _SBOX_CACHE
    if _SBOX_CACHE is None:
        _SBOX_CACHE = build_quantum_sbox()

    bits = pad_bits(text_to_bits(input_data), BITS_PER_BLOCK)
    final = 0
    for chunk in chunks(bits, BITS_PER_BLOCK):
        scrambled = xor_not_reverse_dynamic_count(normalize_bits(chunk))
        h = hash_block_quantum_sbox(scrambled, _SBOX_CACHE)
        final ^= int(h, 16)
    final &= ((1 << BITS_PER_BLOCK) - 1)
    return bin(final)[2:].zfill(BITS_PER_BLOCK)


def quantum_radix_hash_hex(input_data: str) -> str:
    return format(int(quantum_radix_hash(input_data), 2), 'x').zfill(194)


if __name__ == "__main__":
    print("Kuantum S-box oluşturuluyor...")
    sbox = build_quantum_sbox()
    print(f"S-box: {sbox}\n")

    for text in ["Hello World", "Hello world", "a", "b", "TEKNOFEST2026"]:
        h = quantum_radix_hash(text)
        print(f"'{text}': {h[:48]}...")
