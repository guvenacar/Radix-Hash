#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
772-bit Radix Hash debug aracı
Uzun metinleri dosyadan okuyarak her bloğu ayrı ayrı işler.
"""
import os

M = 3 ** 486  # 772-bit yakınında en uygun 3^k değeri

def text_to_bits(s: str) -> str:
    return ''.join(f"{b:08b}" for b in s.encode("utf-8"))

def pad_bits(bits: str, size=772) -> str:
    if len(bits) % size == 0:
        return bits
    return bits + "0" * (size - len(bits) % size)

def chunks(bits: str, size=772):
    return [bits[i:i+size] for i in range(0, len(bits), size)]

def bits_to_base3_int(bits: str) -> int:
    n = 0
    for bit in bits:
        n = n * 3 + (1 if bit == "0" else 2)
    return n

def _hash_block_internal(bits: str) -> str:
    n = bits_to_base3_int(bits)
    hexstr = format(n, "x")
    vals = [int(ch, 16) + 2 for ch in hexstr]

    total = 2
    term = 0
    i = 0
    while i < len(vals) - 1:
        a, b = vals[i], vals[i+1]
        term = pow(a, b, M)
        term = (2 * term) % M
        total = (total * term) % M
        i += 2

    if i < len(vals):
        last = vals[i]
        term = pow(last, 3, M)
        total = (total + term) % M

    if total.bit_length() < 771:
        total = 2 * M - total
    elif total.bit_length() == 771:
        total += 1

    return format(total, "x")

def xor_not_reverse_dynamic_count(bits):
    N = len(bits)
    mid = N // 2
    A = bits[:mid]
    B = bits[mid:]

    xor_len = min(len(A), len(B))
    X = [str(int(A[i]) ^ int(B[i])) for i in range(xor_len)]
    X_not_rev = ['1' if ch == '0' else '0' for ch in X][::-1]

    counts = []
    if X:
        prev = X[0]
        cnt = 1
        for ch in X[1:]:
            if ch == prev:
                cnt += 1
            else:
                counts.append(cnt)
                cnt = 1
                prev = ch
        counts.append(cnt)

    out = []
    pos_X = 0
    pos_rev = 0
    for c in counts:
        out.extend(X[pos_X:pos_X+c])
        pos_X += c
        out.extend(X_not_rev[pos_rev:pos_rev+c])
        pos_rev += c

    return "".join(out)

def process_file(filename: str):
    if not os.path.exists(filename):
        print(f"HATA: {filename} bulunamadı!")
        return

    with open(filename, "r", encoding="utf-8") as f:
        input_data = f.read()

    print("RADIX HASH - UZUN METİN İŞLEME (Python)")
    print("="*80)
    print(f"Dosya: {filename}")
    print(f"Metin uzunluğu: {len(input_data)} karakter")

    bits = pad_bits(text_to_bits(input_data), 772)
    bit_chunks = chunks(bits, 772)
    print(f"Toplam bit sayısı: {len(bits)}")
    print(f"İşlenecek blok sayısı: {len(bit_chunks)}")
    print("="*80)

    final_hash_int = 0
    for i, chunk in enumerate(bit_chunks, 1):
        scrambled = xor_not_reverse_dynamic_count(chunk)
        hex_hash = _hash_block_internal(scrambled)
        print(f"\n--- Blok {i} ---")
        print(f"Hex Hash: {hex_hash}")
        final_hash_int ^= int(hex_hash, 16)

    print("\n" + "-"*80)
    print("Tüm Blokların Birleştirilmiş (XOR) Hash'i:")
    print("-"*80)
    print(f"Hex Hash: {hex(final_hash_int)[2:]}")
    print("="*80)

if __name__ == "__main__":
    process_file("test_text.txt")
