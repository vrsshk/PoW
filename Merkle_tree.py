from hash import hash_1

class MerkleTree:
    def __init__(self, transactions):
        self.transactions = transactions
        # Список Хешей, из которых будет строиться дерево
        self.list_hashes = [hash_1(self.convert_to_bits(tx)) for tx in transactions]
        # Строим дерево пока есть из чего строить
        self.root = self.build_tree(self.list_hashes) if transactions else None

    def convert_to_bits(self, data):
        return ''.join(f'{b:08b}' for b in data.encode('utf-8'))

    # Рекурсивное построение дерева Меркла
    def build_tree(self, hashes):
        # Если в списке остался только 1 элемент, он и будет корнем
        if len(hashes) == 1:
            return hashes[0]

        new_level = []  # Поднимаемся на 1 уровень в ветке
        # Пробегаемся по хешам, попарно соединяя их
        for i in range(0, len(hashes), 2):
            left = hashes[i]
            # Для правого проверяем, есть ли он. Если его нет, дублируем левый
            right = hashes[i + 1] if i + 1 < len(hashes) else left
            # Далее комбинируем их (последовательно соединяем и берем хеш длинной 256)
            combined = self.convert_to_bits(left) + self.convert_to_bits(right)
            new_level.append(hash_1(combined))

        return self.build_tree(new_level)

    # Функция, которая возвращает корень
    def get_root(self):
        return self.root

    # Функция, которая проверяет, принадлежит ли транзакция этому дереву (True/False)💫 (рекурсивно)
    def verify_transaction(self, transaction: str) -> bool:
        if not self.root:
            return False

        target_hash = hash_1(self.convert_to_bits(transaction))
        # Проверяем, есть ли такая транзакция в списке хешей
        if target_hash not in self.list_hashes:
            return False
        # Далее находим доказательство того, что хеш принадлежит дереву
        proof = self.get_proof(target_hash)
        current = target_hash

        for direction, sibling in proof:
            if direction == 'left':
                combined = self.convert_to_bits(sibling) + self.convert_to_bits(current)
            else:
                combined = self.convert_to_bits(current) + self.convert_to_bits(sibling)
            current = hash_1(combined)

        return current == self.root

    def get_proof(self, hash_data):
        proof = []
        current_level = self.list_hashes.copy()
        index = current_level.index(hash_data)
        # Тут мы поднимаемся от нижнего уровня (листа) к верхнему (корню)
        while len(current_level) > 1:
            next_level = []
            new_index = -1

            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i + 1] if i + 1 < len(current_level) else left
                combined = self.convert_to_bits(left) + self.convert_to_bits(right)
                # Формируем РОДИТЕЛЬСКИЙ УЗЕЛ
                parent = hash_1(combined)
                next_level.append(parent)
                # Далее необходимо определить позицию родительского узла
                if i == index or i + 1 == index:
                    new_index = len(next_level) - 1

            if index % 2 == 0:
                sibling_index = index + 1 if index + 1 < len(current_level) else index
                proof.append(('right', current_level[sibling_index]))
            else:
                proof.append(('left', current_level[index - 1]))

            current_level = next_level
            index = new_index

        return proof


transactions = [
    "Подписанная транзакция 1",
    "Подписанная транзакция 2",
    "Подписанная транзакция 3",
    "Подписанная транзакция 4",
    "Безверженко Игорь"  # Транзакция с именем
]

tree = MerkleTree(transactions)
print("Корень Меркла:", tree.get_root())

# Проверка транзакции с именем
tx = "Безверженко Игорь"
print(f"Транзакция '{tx}' валидна:", tree.verify_transaction(tx))
