from hash import hash_1

def prng(count: int):
    """
    Генератор псевдослучайных чисел.
    count - нужное количество псевдослучайных чисел
    Возвращает список из count элементов - битовых строк длины 256 бит.
    """
    # 512-битная строка из фамилии и имени
    name = "Ворощук Анна"
    bits = ''.join(f'{b:08b}' for b in name.encode('utf-8'))

    if len(bits) < 512:
        bits = bits.zfill(512)
    else:
        bits = bits[:512]

    # Нулевой цикл - получаем h0
    h0 = hash_1(bits)

    random_numbers = []

    # 3. Циклы i = 1..count
    for i in range(1, count + 1):
        # Формируем вход: h0 (256 бит) + i в 256 бит
        i_bits = f'{i:0256b}'
        input_bits = h0 + i_bits
        h_i = hash_1(input_bits)
        random_numbers.append(h_i)

    return random_numbers
