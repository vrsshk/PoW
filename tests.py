import unittest
from hash import hash_1
from schnorr import *
from prng import prng

class TestHash256(unittest.TestCase):
    def test_1(self):
        hex_msg = "323130393837363534333231303938373635343332313039383736353433323130393837363534333231303938373635343332313039383736353433323130"
        M_1 = ''.join(f'{int(hex_msg[i:i+2], 16):08b}' for i in range(0, len(hex_msg), 2))
        H_1 = "00557be5e584fd52a449b16b0251d05d27f94ab76cbaa6da890b59d8ef1e159d"
        result_hex = f'{int(hash_1(M_1), 2):064x}'
        self.assertEqual(result_hex.lower(), H_1.lower())

    def test_2(self):
        hex_msg = "fbe2e5f0eee3c820fbeafaebef20fffbf0e1e0f0f520e0ed20e8ece0ebe5f0f2f120fff0eeec20f120faf2fee5e2202ce8f6f3ede220e8e6eee1e8f0f2d1202ce8f0f2e5e220e5d1"
        M_2 = ''.join(f'{int(hex_msg[i:i+2], 16):08b}' for i in range(0, len(hex_msg), 2))
        H_2 = "508f7e553c06501d749a66fc28c6cac0b005746d97537fa85d9e40904efed29d"
        result_hex = f'{int(hash_1(M_2), 2):064x}'
        self.assertEqual(result_hex.lower(), H_2.lower())

class TestSchnorrSignature(unittest.TestCase):
    def test_signature_verification(self):
        bits = prng(2)
        x = int(bits[0], 2) % q
        r = int(bits[1], 2) % q

        message = "Привет от Ворощук Анны"
        signature, public_key = sign(message, x, r)
        self.assertTrue(verify(message, public_key, signature))

    def test_modified_message_should_fail(self):
        bits = prng(2)
        x = int(bits[0], 2) % q
        r = int(bits[1], 2) % q

        message = "Привет от Ворощук Анны"
        modified_message = "Привет от Иванова Ивана"

        signature, public_key = sign(message, x, r)
        self.assertFalse(verify(modified_message, public_key, signature))

if __name__ == '__main__':
    unittest.main()
