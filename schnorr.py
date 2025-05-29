from hash import hash 
from prng import prng
from transform import int_to_bits, str_to_bits
from sympy import isprime

# Параметры из ГОСТ Р 34.10-94
p = int("EE8172AE8996608FB69359B89EB82A69854510E2977A4D63BC97322CE5DC3386EA0A12B343E9190F23177539845839786BB0C345D165976EF2195EC9B1C379E3", 16)

q = int("98915E7EC8265EDFCDA31E88F24809DDB064BDC7285DD50D7289F0AC6F49DD2D", 16)

a = int("9E96031500C8774A869582D4AFDE2127AFAD2538B4B6270A6F7C8837B50D50F206755984A49E509304D648BE2AB5AAB18EBE2CD46AC3D8495B142AA6CE23E21C", 16)

# Подпись Шнорра (key-prefixed)
def sign(message: str, x: int, r: int) -> tuple:
    R = pow(a, r, p)
    P = pow(a, x, p) # открытый ключ

    h_input = int_to_bits(R) + int_to_bits(P) + str_to_bits(message)
    e = int(hash(h_input), 2) % q
    s = (r + e * x) % q

    return (R, s), P

# Проверка подписи
def verify(message: str, P: int, signature: tuple) -> bool:
    R, s = signature

    h_input = int_to_bits(R) + int_to_bits(P) + str_to_bits(message)
    e = int(hash(h_input), 2) % q

    left = pow(a, s, p)
    right = (R * pow(P, e, p)) % p

    return left == right