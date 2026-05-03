#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quantum-Hybrid Radix Hash — Test Suite
=======================================
Avalanche, collision, preimage, entropi testleri.
"""

import sys, time, math, random, string, hashlib
sys.path.insert(0, '.')
from quantum_radix_hash import quantum_radix_hash

SEP = "=" * 60


def test_deterministik():
    print(f"\n{SEP}")
    print("1. DETERMİNİSTİK TEST")
    print(SEP)
    text = "TEKNOFEST2026"
    results = [quantum_radix_hash(text) for _ in range(5)]
    ok = len(set(results)) == 1
    print(f"5 kez aynı girdi → {'PASS ✓' if ok else 'FAIL ✗'}")
    return ok


def test_avalanche():
    print(f"\n{SEP}")
    print("2. AVALANCHE EFFECT")
    print(SEP)
    pairs = [
        ("Hello World", "Hello world"),
        ("a", "b"),
        ("0", "1"),
        ("test", "uest"),
        ("abc", "abd"),
    ]
    results = []
    for t1, t2 in pairs:
        h1 = quantum_radix_hash(t1)
        h2 = quantum_radix_hash(t2)
        diff = sum(c1 != c2 for c1, c2 in zip(h1, h2))
        pct = diff / 772 * 100
        ok = 45 <= pct <= 55
        results.append(ok)
        print(f"  '{t1}' vs '{t2}': {diff}/772 ({pct:.1f}%) {'✓' if ok else '✗'}")
    return all(results)


def test_collision(n=10000):
    print(f"\n{SEP}")
    print(f"3. COLLISION TEST ({n} girdi)")
    print(SEP)
    hashes = {}
    collisions = 0
    for i in range(n):
        text = str(i) + ''.join(random.choices(string.ascii_letters, k=4))
        h = quantum_radix_hash(text)
        if h in hashes:
            collisions += 1
            print(f"  COLLISION: '{text}' == '{hashes[h]}'")
        else:
            hashes[h] = text
    ok = collisions == 0
    print(f"  {n} girdi → {collisions} collision {'PASS ✓' if ok else 'FAIL ✗'}")
    return ok


def test_preimage(seconds=10):
    print(f"\n{SEP}")
    print(f"4. PREİMAGE DİRENCİ ({seconds} saniye)")
    print(SEP)
    target = quantum_radix_hash("secret")
    attempts = 0
    start = time.perf_counter()
    found = False
    while time.perf_counter() - start < seconds:
        guess = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        if quantum_radix_hash(guess) == target:
            print(f"  BULUNDU: '{guess}'")
            found = True
            break
        attempts += 1
    elapsed = time.perf_counter() - start
    print(f"  {attempts} deneme / {elapsed:.1f}sn → {'FAIL ✗' if found else 'PASS ✓'}")
    print(f"  Hız: {attempts/elapsed:.0f} deneme/sn")
    return not found


def test_entropi():
    print(f"\n{SEP}")
    print("5. ENTROPİ (SHA3-512 karşılaştırması)")
    print(SEP)

    def entropy(bits):
        n = len(bits)
        c0, c1 = bits.count('0'), bits.count('1')
        if c0 == 0 or c1 == 0:
            return 0.0
        p0, p1 = c0/n, c1/n
        return -p0*math.log2(p0) - p1*math.log2(p1)

    inputs = ["a", "Hello World", "123456", "TEKNOFEST2026", "x" * 100]
    print(f"  {'Girdi':<20} {'QR-Hash Entropi':>16} {'SHA3 Entropi':>14}")
    print(f"  {'-'*52}")
    for t in inputs:
        r = quantum_radix_hash(t)
        s = bin(int(hashlib.sha3_512(t.encode()).hexdigest(), 16))[2:].zfill(512)
        print(f"  {t[:20]:<20} {entropy(r):>16.6f} {entropy(s):>14.6f}")


if __name__ == "__main__":
    print("QUANTUM-HYBRID RADIX HASH — TEST SUITE")
    print("TEKNOFEST 2026")

    results = []
    results.append(test_deterministik())
    results.append(test_avalanche())
    results.append(test_collision(n=1000))  # hızlı test, n artırılabilir
    results.append(test_preimage(seconds=10))
    test_entropi()

    print(f"\n{SEP}")
    print("ÖZET")
    print(SEP)
    labels = ["Deterministik", "Avalanche", "Collision", "Preimage"]
    for label, ok in zip(labels, results):
        print(f"  {label:<15} {'PASS ✓' if ok else 'FAIL ✗'}")
    print(f"\n  {'Tümü geçti ✓' if all(results) else 'Bazı testler başarısız ✗'}")
