import base64


def bits_to_text(bits):
    """Безопасное преобразование битов в строку через Base64"""
    byte_array = bytearray()
    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        if len(byte) == 8:
            byte_array.append(int(byte, 2))
    return base64.b64encode(bytes(byte_array)).decode('ascii')


def save_report(header, transactions, signatures, public_keys, secret_key, merkle_root, block_hash):
    """Сохранение полного отчета в файл"""
    with open('blockchain_report.txt', 'w') as f:
        f.write("=== ОТЧЕТ О СОЗДАНИИ БЛОКА ===\n\n")

        f.write("1. ПАРАМЕТРЫ ПОДПИСИ ШНОРРА:\n")
        f.write(f"Секретный ключ x: {hex(secret_key)}\n\n")

        f.write("2. ПОДПИСАННЫЕ ТРАНЗАКЦИИ:\n")
        for i, (tx_bits, sig, pub) in enumerate(zip(transactions, signatures, public_keys)):
            f.write(f"\nТранзакция {i + 1}:\n")
            f.write(f"Содержимое: {bits_to_text(tx_bits)[:100]}...\n")
            f.write(f"Подпись (R): {hex(sig[0])}\n")
            f.write(f"Подпись (s): {hex(sig[1])}\n")
            f.write(f"Публичный ключ: {hex(pub)}\n")

        f.write("\n3. ЗАГОЛОВОК БЛОКА:\n")
        f.write(f"Размер: {header['size'].hex()}\n")
        f.write(f"Хеш предыдущего блока: {hex(int(header['prev_hash'], 2))[2:]}\n")
        f.write(f"Корень Меркла: {merkle_root}\n")
        f.write(f"Метка времени: {list(header['timestamp'])}\n")
        f.write(f"Nonce: {header['nonce']}\n")
        f.write(f"Хеш блока: {block_hash}\n")