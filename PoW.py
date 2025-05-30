from prng import prng
import datetime
from hash import hash_1


# Создание заголовка блока и PoW
def create_block_header(merkle_root):
    size_bytes = int(prng(1)[0][:32], 2).to_bytes(4, 'big')

    # Генерируем хеш предыдущего блока (256 бит)
    # Берем первые 256 бит из ГПСЧ
    prev_hash = prng(1)[0][:256]

    # Генерируем дату и время
    now = datetime.datetime.now()
    # Формируем метку времени из 4 байт:
    # [час (0-23), день (1-31), месяц (1-12), год % 100 (00-99)]
    timestamp_bytes = bytes([
        now.hour,
        now.day,
        now.month,
        now.year % 100
    ])
    # Собираем готовую конструкцию
    header = {
        "size": size_bytes,  # 4 байта - произвольный размер
        "prev_hash": prev_hash,  # 256 бит - хеш предыдущего блока
        "merkle_root": merkle_root,  # 256 бит - корень Меркла
        "timestamp": timestamp_bytes,  # 4 байта - метка времени
        "nonce": 0  # 4 байта - счетчик для PoW (инициализируем 0)
    }

    return header


def mine_block(header: dict) -> tuple:
    """Алгоритм Proof-of-Work для поиска валидного nonce."""
    # Переделываем все в байты
    prev_hash_bytes = int(header["prev_hash"], 2).to_bytes(32, 'big')
    merkle_root_bytes = int(header["merkle_root"], 2).to_bytes(32, 'big')
    # Собираем все компоненты, кроме nonce
    base_header = (
            header["size"] +  # 4 байта
            prev_hash_bytes +  # 32 байта
            merkle_root_bytes +  # 32 байта
            header["timestamp"]  # 4 байта
    )
    """Теперь перебираем nonce"""
    for nonce in range(0, 2 ** 32):
        # Снова переходим в байты
        nonce_bytes = nonce.to_bytes(4, 'big') # big - правильный порядок байт
        # Делаем полный заголовок
        full_header = base_header + nonce_bytes
        # После этого для дальнейших операций переделываем полный заголовок в биты
        header_bits = ''.join(f'{b:08b}' for b in full_header)
        block_hash = hash_1(header_bits)

        # Ищем хеш, который начинается с "00000"
        if block_hash.startswith('00000'):
            print(f"Успех! Найден nonce: {nonce}")
            print(f"Хеш блока: {block_hash}")
            return nonce, block_hash

    # Если решение не найдено после полного перебора
    print("Не удалось найти подходящий nonce")
    return None, None



