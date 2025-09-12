#hash_generator.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Readable Radix-Hash script for multiple inputs, including long text.
"""
from model.radix_hash import process_block
import textwrap

def print_hash(input_text: str, hash_bits: str):
    print("\n" + "-"*80)
    print("Input:")
    # Uzun metni daha okunaklı göstermek için 80 karakterlik satırlara böl
    for line in textwrap.wrap(input_text, width=80):
        print(line)
    print("\n772-bit hash:")
    print(hash_bits)
    print("\nHex hash:")
    print(hex(int(hash_bits,2))[2:])
    print("-"*80)

def main():
    # Kısa test girdileri
    test_inputs = [
        "Hello World",
        "Hello world",
        "a",
        "b",
        " ",
        "0",
        "1",
    ]

    # Uzun metin
    long_text = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam quis cursus libero. Etiam non erat neque. Nulla massa nisl, consequat nec mauris ac, hendrerit aliquet augue. Vestibulum elementum volutpat justo, ut ornare nisi imperdiet a. Mauris fringilla, nisi blandit sagittis finibus, justo nulla efficitur elit, vitae fringilla dolor ex a lectus. Proin pulvinar sem tellus, ac varius ipsum egestas vitae. Praesent non nunc purus. Donec blandit mi et eros dignissim, fringilla commodo eros rhoncus. Suspendisse facilisis interdum mauris, in congue arcu scelerisque nec. Suspendisse eu dolor ullamcorper, feugiat ligula ut, dapibus neque. Cras nunc est, rutrum sit amet viverra maximus, laoreet vitae urna. Aliquam egestas turpis consequat tempor elementum.

Cras maximus, turpis eu bibendum ultrices, sem metus porta nunc, nec feugiat risus metus et lacus. Suspendisse sed leo ac ligula elementum elementum. Proin iaculis cursus mauris, non lacinia tellus vulputate sit amet. Proin ac euismod orci. Donec ut nunc commodo, imperdiet diam vel, lobortis ante. Mauris venenatis mollis libero sed pharetra. Vivamus lacus magna, laoreet vitae luctus sit amet, gravida mattis risus.

Maecenas hendrerit pellentesque eros, non feugiat lectus pellentesque vitae. Quisque facilisis maximus accumsan. Mauris eu ex rutrum, ornare sem eget, volutpat lorem. Duis blandit aliquam mi id semper. Sed ultricies, ligula ac condimentum commodo, orci libero fermentum velit, id tincidunt mauris sapien in justo. Maecenas condimentum laoreet magna a facilisis. Maecenas sodales lorem eu orci finibus porta. Proin euismod, augue vitae malesuada pulvinar, risus felis lacinia metus, ac pellentesque lorem felis eu dolor. Nam sodales lacus quis ante imperdiet, eu efficitur nunc malesuada.

Nulla ante magna, pretium nec mollis sed, cursus ut turpis. Maecenas rhoncus non diam vel lobortis. Sed ultrices vehicula porta. Vivamus eget luctus ligula. Integer vestibulum ante a ante malesuada tempor. Phasellus vel luctus ante, id finibus nisi. Nam purus orci, pulvinar eget risus et, commodo vehicula eros. Aenean ut libero aliquam, laoreet lectus sit amet, aliquam lacus. Pellentesque dignissim eleifend sem vitae lacinia. Fusce sit amet molestie mi. Cras eget neque magna. Maecenas eget justo at lorem laoreet varius placerat ut lorem. Duis et sem ac magna semper convallis ac eu lectus. Pellentesque non scelerisque nisl, vitae mollis orci. Vestibulum accumsan blandit purus sit amet venenatis.
"""

    # Önce kısa test girdilerini hashle
    for text in test_inputs:
        hash_bits = process_block(text)
        print_hash(text, hash_bits)

    # En sonda uzun metni hashle
    hash_bits_long = process_block(long_text)
    print_hash(long_text, hash_bits_long)

if __name__ == "__main__":
    main()
