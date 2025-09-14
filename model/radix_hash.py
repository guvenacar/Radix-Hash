#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Core functions of the 772-bit QTHash algorithm.
This module is designed to be imported by the NIST test script.
"""
import sys
import os

# M value: the power of 3 closest to 772-bit length.
# 3**486 ≈ 770 bits, closest to the 772-bit target.
M = 3 ** 486

def text_to_bits(s: str) -> str:
    """Convert text to UTF-8 and return a bit string."""
    return ''.join(f"{b:08b}" for b in s.encode("utf-8"))

def pad_bits(bits: str, size=772) -> str:
    """Pad the bit string to be a multiple of 772."""
    if len(bits) % size == 0:
        return bits
    return bits + "0" * (size - len(bits) % size)

def chunks(bits: str, size=772):
    """Split a bit string into 772-bit chunks."""
    return [bits[i:i+size] for i in range(0, len(bits), size)]

def bits_to_base3_int(bits: str) -> int:
    """Convert bit string into a base-3 integer."""
    n = 0
    for bit in bits:
        n = n * 3 + (1 if bit == "0" else 2)
    return n

def normalize_bits(bits: str, target_length=771) -> str:
    """Normalize bit string to 772 bits."""
    if len(bits) == target_length:
        return bits + "1"
    return bits

def _hash_block_internal(bits: str) -> str:
    """
    Process a single 772-bit block and return a hexadecimal string.
    Do not call this directly from outside.
    """
    n = bits_to_base3_int(bits)
    hexstr = format(n, "x")
    vals = [int(ch, 16) + 2 for ch in hexstr]

    total = 2
    term = 0
    i = 0
    while i < len(vals) - 1:
        a, b = vals[i], vals[i+1]
        term = (term + pow(a, b, M)) % M
        total = (total * term) % M
        i += 2

    if i < len(vals):
        last = vals[i]
        term = pow(last, 3, M)
        total = (total + term) % M

    # Normalize output
    if total.bit_length() < 771:
        total = 2 * M - total
    elif total.bit_length() == 771:
        total += 1

    return format(total, "x")

from utils.balance_transforms import xor_not_reverse_dynamic_count

def process_block(input_data: str) -> str:
    """
    Function called by the main test script.
    Accepts text input, computes hash, returns 772-bit string.
    Multi-block inputs are XORed together.
    Scrambling: XOR + NOT + reverse + dynamic count interleave.
    """
    BITS_PER_BLOCK = 772

    bits = pad_bits(text_to_bits(input_data), BITS_PER_BLOCK)
    bit_chunks = chunks(bits, BITS_PER_BLOCK)

    final_hash_int = 0

    for chunk in bit_chunks:
        normalized_chunk = normalize_bits(chunk)
        scrambled_chunk = xor_not_reverse_dynamic_count(normalized_chunk)
        hex_hash = _hash_block_internal(scrambled_chunk)
        final_hash_int ^= int(hex_hash, 16)

    final_hash_int &= ((1 << BITS_PER_BLOCK) - 1)
    return bin(final_hash_int)[2:].zfill(BITS_PER_BLOCK)
