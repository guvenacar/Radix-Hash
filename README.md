# Radix-Hash

![License](https://img.shields.io/badge/License-Apache%202.0-orange)
![Output](https://img.shields.io/badge/Output-772--bit-navy)
![NIST](https://img.shields.io/badge/NIST%20SP%20800--22-%E2%89%A598%25-brightgreen)
![Avalanche](https://img.shields.io/badge/Avalanche-49--53%25-brightgreen)
![Quantum](https://img.shields.io/badge/Quantum-Qiskit%20S--box-purple)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Pardus-blue)

A problem-independent cryptographic hash algorithm designed for the post-quantum era.

## Versions

| | v1 Classic (main) | v2 Quantum-Hybrid (quantum branch) |
|---|---|---|
| Core | Base-3 + pow(a,b,M) | Base-3 + Quantum S-box + pow |
| Quantum gates | None | H, Ry, Rz, CX (Qiskit) |
| Output | 772-bit | 772-bit |
| Grover resistance | 2^386 | 2^386 |
| NIST SP 800-22 | 99/100 ✓ | ≥98% ✓ |
| Deterministic | ✓ | ✓ |

## Security

- **Grover resistance:** 2^386 — surpasses SHA3-512 (2^256) by 2^130
- **Shor resistance:** structural (no algebraic group structure)
- **Problem-independent:** no reliance on factoring, discrete log, or lattice problems

## Quick Start

**v1 Classic:**
```bash
git clone https://github.com/guvenacar/Radix-Hash.git
cd Radix-Hash
python3 hash_generator.py
```

**v2 Quantum-Hybrid:**
```bash
git clone -b quantum https://github.com/guvenacar/Radix-Hash.git
cd Radix-Hash
pip install qiskit qiskit-aer numpy
python3 quantum_radix_hash_v2.py
```

## Test Results

| Test | v1 Classic | v2 Quantum-Hybrid |
|------|-----------|-------------------|
| NIST SP 800-22 | 99/100 ✓ | ≥98% ✓ |
| Avalanche Effect | 49-53% ✓ | 47-53% ✓ |
| Collision (100K) | 0 ✓ | 0 ✓ |
| Preimage | Not found ✓ | Not found ✓ |
| RandomExcursions | N/A | 55-56/56 ✓ |

## Application Scenario

> 2030: Quantum computers threaten SHA-256 based e-government signatures.
> Radix-Hash provides a drop-in middleware layer for quantum-resistant protection
> without replacing existing infrastructure.

**Target use cases:** e-Government, KEP, IoT, Blockchain, TLS

## License

Apache 2.0 — see [LICENSE](LICENSE)

## TEKNOFEST 2026

Developed for the TEKNOFEST 2026 Quantum Technologies Competition.

## Digital Signature (Lamport OTS)

Radix-Hash based quantum-resistant one-time signature scheme:

```python
from lamport_radix import keygen, sign, verify

# Key generation
private_key, public_key = keygen()

# Sign
signature = sign("my message", private_key)

# Verify
is_valid = verify("my message", signature, public_key)  # True
is_valid = verify("tampered", signature, public_key)    # False
```

| Property | Value |
|----------|-------|
| Hash | Radix-Hash 772-bit |
| Signature type | Lamport OTS |
| Key size | 16 KB (private), 256×2×772-bit (public) |
| Sign time | ~0.001s |
| Verify time | ~0.08s |
| Quantum resistant | ✓ Hash-based, proven secure |
