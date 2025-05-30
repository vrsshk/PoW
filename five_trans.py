from prng import prng

def generate_data(count:int):
    """Генерируем содержимое файлов"""
    tmp = []
    count = count * 6.25
    random_data = prng(int(count))
    # Работаем над файлом с именем студента (если меньше -> прибовляем, если меньше -> убираем)
    name = "Безверженко Игорь"
    name_trans = ''.join(f'{b:08b}' for b in name.encode('utf-8'))
    if len(name_trans) < 1600:
        name_trans = "0"*(1600 - len(name_trans)) + name_trans # Добавляем в начало
    if len(name_trans) > 1600:
        name_trans = name_trans[:1600]

    random_data.append(name_trans)

    # Создаём масив, в котором храняться содержимое будующих файлов
    all_data = ""
    for i in random_data:
        all_data += "".join(i)
    data_list = []
    for i in range(0, len(all_data), 1600):
        data_list.append(all_data[i:i+1600])

    return data_list


# print(len(data_list[0]), len(data_list[1]), len(data_list[2]), len(data_list[3]), len(data_list[4]))
# print(len(all_data))


