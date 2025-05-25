from transform import (
    IV, C, S, P, L, X, E, g_N
)

def int_to_bits(n: int, length: int = 512) -> str:
    """Преобразует целое число в битовую строку длины `length`."""
    return f"{n:0{length}b}"

def add_mod512(a: str, b: str) -> str:
    """Сложение двух битовых строк по модулю 2^512."""
    return int_to_bits((int(a, 2) + int(b, 2)) % (1 << 512))

def hash256(message: bytes) -> str:
    """
    Реализация хэш-функции с длиной хэш-кода 256 бит.
    message — сообщение в байтах
    возвращает 256-битный хэш в виде строки из 0 и 1
    """
    h = IV
    N = '0' * 512
    Sigma = '0' * 512

    # Этап 2 — обработка полных блоков
    M = message
    while len(M) >= 64:
        m = ''.join(f'{byte:08b}' for byte in M[-64:])  # последний блок
        M = M[:-64]
        h = g_N(h, m, N)
        N = add_mod512(N, int_to_bits(512))
        Sigma = add_mod512(Sigma, m)

    # Этап 3 — финальный неполный блок
    message_bits = ''.join(f'{byte:08b}' for byte in M)
    pad_len = 512 - len(message_bits) - 1
    m = '0' * pad_len + '1' + message_bits
    h = g_N(h, m, N)
    N = add_mod512(N, int_to_bits(len(message_bits)))
    Sigma = add_mod512(Sigma, m)
    h = g_N(h, N, '0' * 512)
    h = g_N(h, Sigma, '0' * 512)

    # Возвращаем MSB_256(h)
    return h[:256]

if __name__ == "__main__":
    hex_msg = "323130393837363534333231303938373635343332313039383736353433323130393837363534333231303938373635343332313039383736353433323130"
    msg = bytes.fromhex(hex_msg)
    digest = hash256(msg)
    print(f"Хэш256: {digest}")
    print(hex(int(digest, 2))[2:].zfill(len(digest) // 4))
