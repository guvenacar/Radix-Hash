# Radix-Hash

Radix-Hash is a 772-bit Hash algorithm that introduces a completely different approach from classical hash algorithms. Its core principle is based on mathematical chaos and radix (base) conversion; it uses almost no traditional bit manipulations. Only a small, dynamic, and deterministic bit manipulation is applied, ensuring the unpredictability of the output.

## Features

* **High Uncertainty:** Knowing the hex value alone is insufficient to reverse the algorithm. The order of these values must also be known, making conventional attacks nearly impossible.

* **Minimal Bit Manipulation:** Only a small, dynamic combination of XOR + NOT + reverse + interleave is applied, providing high entropy and unpredictable results.

* **Radix Conversion Based:** Bits are converted to base-3, offering a completely new perspective for hash calculations. This approach creates a structure resistant to attacks without relying on conventional mathematical problems.

* **High NIST Test Success:** The algorithm passes NIST statistical tests with approximately 99% success.

* **Quantum Resistant:** The algorithm's structure ensures resistance against quantum computer attacks, as it does not rely on solvable mathematical problems.

## Usage

The `model/radix_hash.py` module contains the core hash functions.

```python
from model.radix_hash import process_block

input_text = "Hello world!"
hash_bits = process_block(input_text)
print(f"772-bit hash: {hash_bits}")
```

* Input text is converted to UTF-8 and processed in 772-bit blocks.
* Each block is normalized and scrambled dynamically.
* The final result is combined via XOR to produce a 772-bit hash.

## NIST Testing

The project provides `test/run_nist.sh` to generate NIST-compliant bit streams and run tests automatically.

* Tests validate the algorithm's randomness and unpredictability.
* Generated bit streams are stored in `results/nist_test_data.txt`.

## Project Structure

```
Radix-Hash/
├── controller/
├── model/
│   └── radix_hash.py
├── utils/
│   └── balance_transforms.py
├── view/
├── results/
│   └── nist_test_data.txt (auto-generated)
├── test/
│   └── run_nist.sh
├── requirements.txt
└── README.md

```

---

## Algorithm Details & NIST Testing

For full technical detail, see:

* [Detailed Algorithm Steps (Radix‑Hash Article)](Radix-Hash-Article.md)
* [NIST Statistical Test Report](NIST_Analysis_Report.txt)
* [Benchmark Results](radix_hash_benchmark_report.txt)

---

## Summary

Radix-Hash breaks away from classical hash paradigms, offering high security, NIST compliance, and quantum resistance through mathematical chaos and radix conversion methods. Knowing the values alone is insufficient; the order and scrambling steps must also be known. This makes the algorithm strong, unpredictable, and highly resistant to attacks.
