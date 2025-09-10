# utils/balance_transforms.py

def half_xor_then_append_not(bits: str) -> str:
    """
    bits uzunluğu even olmalı (bizde 772). İşlem:
      - bits'i iki eşit yarıya ayır: A | B
      - C = A XOR B  (uzunluk = len(A))
      - output = C || NOT(C)  (uzunluk = 2 * len(C) = len(bits))
    Böylece blok başına kesin %50/50 0/1 dengesi sağlanır.
    """
    n = len(bits)
    if n % 2 != 0:
        raise ValueError("half_xor_then_append_not requires even-length bit strings")

    half = n // 2
    A = bits[:half]
    B = bits[half:]

    # XOR A and B
    C_list = []
    for a, b in zip(A, B):
        # xor: '0' xor '0' -> '0', '0' xor '1' -> '1', etc.
        C_list.append('1' if (a != b) else '0')
    C = ''.join(C_list)

    # NOT(C)
    notC = ''.join('1' if c == '0' else '0' for c in C)

    return C + notC

def interleave_with_not(bits):
    """
    bits: '0' ve '1' karakterlerinden oluşan string veya liste
    dönüş: yine string ('0','1')
    """
    interleaved = []
    for b in bits:
        bi = int(b)                  # karakter → int
        interleaved.append(str(bi))  # orijinal
        interleaved.append(str(1 - bi))  # NOT
    return "".join(interleaved)

def xor_not_reverse_dynamic_count(bits):
    if not isinstance(bits, str):
        bits = "".join(bits)

    N = len(bits)
    mid = N // 2
    A = bits[:mid]
    B = bits[mid:]

    # XOR
    xor_len = min(len(A), len(B))
    X = [str(int(A[i]) ^ int(B[i])) for i in range(xor_len)]

    # NOT ve reverse
    X_not_rev = ['1' if ch == '0' else '0' for ch in X][::-1]

    # Counts = XOR sonucu içindeki 0/1 blok uzunlukları
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

    # Interleave
    out = []
    pos_X = 0
    pos_rev = 0
    for c in counts:
        # XOR dizisinden c bit
        out.extend(X[pos_X:pos_X+c])
        pos_X += c
        # Reverse-NOT dizisinden c bit
        out.extend(X_not_rev[pos_rev:pos_rev+c])
        pos_rev += c

    return "".join(out)




# küçük yardımcı kontrol fonksiyonu
def counts(bits: str):
    return bits.count('0'), bits.count('1')
