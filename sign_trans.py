from prng import prng
from schnorr import sign, p, q, a
import base64

def sign_transactions(transactions):
    # Генерируем секретный ключ
    x = int((prng(1)[0][:256]), 2)
    # Если ключ равен 0, меняем его
    if x == 0:
        x = 1

    signatures = []
    public_keys = []

    for tx_bits in transactions:
        tx_str = bits_to_text(tx_bits) # Делаем, чтобы работать со строкой
        # Генерация уникального нонса для каждой подписи
        r_val = int(prng(1)[0][:256], 2) % q
        if r_val == 0:
            r_val = 1

        # Создание подписи
        signature, P = sign(tx_str, x, r_val)
        signatures.append(signature)
        public_keys.append(P)

    return signatures, public_keys, x

def bits_to_text(bits):
    """Безопасное преобразование битов в строку через Base64"""
    byte_array = bytearray()
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) == 8:
            byte_array.append(int(byte, 2))
    return base64.b64encode(bytes(byte_array)).decode('ascii')

def text_to_bits(text):
    """Обратное преобразование строки в биты"""
    byte_array = base64.b64decode(text.encode('ascii'))
    return ''.join(f'{b:08b}' for b in byte_array)
