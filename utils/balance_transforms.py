def half_xor_then_append_not(bits: str) -> str:
    """
    Bits length must be even (772 here). Operation:
    - Split bits into two halves: A | B
    - C = A XOR B  (length = len(A))
    - output = C || NOT(C)  (length = 2 * len(C) = len(bits))
    Ensures exact 50/50 0/1 balance per block.
    """
    n = len(bits)
    if n % 2 != 0:
        raise ValueError("half_xor_then_append_not requires even-length bit strings")

    half = n // 2
    A = bits[:half]
    B = bits[half:]

    C_list = ['1' if (a != b) else '0' for a, b in zip(A, B)]
    C = ''.join(C_list)

    notC = ''.join('1' if c == '0' else '0' for c in C)

    return C + notC

def interleave_with_not(bits):
    """
    bits: string or list of '0' and '1'
    returns: string ('0'/'1')
    """
    interleaved = []
    for b in bits:
        bi = int(b)
        interleaved.append(str(bi))
        interleaved.append(str(1 - bi))
    return "".join(interleaved)

def xor_not_reverse_dynamic_count(bits):
    if not isinstance(bits, str):
        bits = "".join(bits)

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

def counts(bits: str):
    """Helper function: returns number of 0s and 1s in a bit string."""
    return bits.count('0'), bits.count('1')
