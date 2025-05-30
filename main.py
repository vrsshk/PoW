from PoW import create_block_header, mine_block
from five_trans import generate_data
from sign_trans import sign_transactions
from Merkle_tree import MerkleTree
from schnorr import verify
from utils import bits_to_text, save_report



def main():
    print("=" * 50)
    print("Генерация транзакций")
    print("=" * 50)
    transactions = generate_data(4)

    print("\n" + "=" * 50)
    print("Подпись транзакций")
    print("=" * 50)
    signatures, public_keys, secret_key = sign_transactions(transactions)

    # Проверка подписей
    for i, tx_bits in enumerate(transactions):
        tx_str = bits_to_text(tx_bits)
        is_valid = verify(tx_str, public_keys[i], signatures[i])
        print(f"Транзакция {i + 1} {'валидна' if is_valid else 'НЕВАЛИДНА'}")

    print("\n" + "=" * 50)
    print("Построение дерева Меркла")
    print("=" * 50)
    tree = MerkleTree(transactions)
    merkle_root = tree.get_root()
    print(f"Корень Меркла: {merkle_root}")

    print("\n" + "=" * 50)
    print("Создание блока и PoW")
    print("=" * 50)
    header = create_block_header(merkle_root)
    nonce, block_hash = mine_block(header)

    if nonce is not None:
        header["nonce"] = nonce
        print("\nРезультаты:")
        print(f"Размер блока: {header['size'].hex()}")
        print(f"Хеш предыдущего блока: {hex(int(header['prev_hash'], 2))[2:]}")
        print(f"Корень Меркла: {merkle_root}")
        print(f"Метка времени: {list(header['timestamp'])}")
        print(f"Nonce: {nonce}")
        print(f"Хеш блока: {block_hash}")

        # Сохранение отчета
        save_report(
            header=header,
            transactions=transactions,
            signatures=signatures,
            public_keys=public_keys,
            secret_key=secret_key,
            merkle_root=merkle_root,
            block_hash=block_hash
        )
    else:
        print("Не удалось найти подходящий nonce")


if __name__ == "__main__":
    main()