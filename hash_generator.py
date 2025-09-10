#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple script to hash an input string using Radix-Hash.
"""
from model.radix_hash import process_block

def main():
    text = input("Enter text to hash: ")
    hash_bits = process_block(text)
    print(f"\nInput text: {text}")
    print(f"772-bit hash: {hash_bits}")
    print(f"Hex hash: {hex(int(hash_bits,2))[2:]}")

if __name__ == "__main__":
    main()
