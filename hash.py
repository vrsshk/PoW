from transform import *

def hash(M: str) -> str:
    """
    Реализация хэш-функции с длиной хэш-кода 256 бит.
    M — сообщение в виде битовой строки (str из '0' и '1')
    возвращает 256-битный хэш в виде строки из 0 и 1
    """
    h = IV
    N = '0' * 512
    Sigma = '0' * 512

    # Этап 2 — обработка полных 512-битных блоков
    while len(M) >= 512:
        m = M[-512:]
        M = M[:-512]
        h = g_N(h, m, N)
        N = add_mod512(N, int_to_bits(512))
        Sigma = add_mod512(Sigma, m)

    # Этап 3 — обработка последнего (неполного) блока
    m = '0' * (511 - len(M)) + '1' + M
    h = g_N(h, m, N)
    N = add_mod512(N, int_to_bits(len(M)))
    Sigma = add_mod512(Sigma, m)


    h = g_N(h, N, '0' * 512)
    h = g_N(h, Sigma, '0' * 512)

    return h[:256]