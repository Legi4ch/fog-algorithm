# fog-algorithm
import bip39gen as bip
import random


class Fog:
    _primary_key: list
    _xor_key: list
    _shifts: list
    _xor_control_sum: int
    seed_len: int
    pin: str
    _rand_min = 10
    _rand_max = 50

    def __init__(self, _pin: str, _seed_len: int):
        self.seed_len = _seed_len
        self._pin = self._glue_pin(_pin)
        self._set_primary_key()
        self._set_xor_key()
        self._set_shifts()

    def _glue_pin(self, _pin: str):
        split_pin = _pin.split()
        result_list = []
        while len(result_list) < self.seed_len:
            result_list.extend(split_pin)
        return result_list[:self.seed_len]

    def _set_primary_key(self):
        """
            Формируем первичный ключ из пин-кода ключа.
        """
        result_key = []
        key_sum = 0
        key = self._pin

        for idx in range(0, len(key)):
            el = int(key[idx]) + (idx+1)*10 if idx % 2 > 0 else int(key[idx]) ** 2
            result_key.append(el)
            key_sum = key_sum + el

        self._primary_key = result_key

    def _set_xor_key(self):
        """
            Формируем xor ключ из первичного ключа.
        """
        result_key = []
        key_sum = 0
        for idx in range(0, len(self._primary_key)):
            xor = self._primary_key[idx] ^ (idx+1)
            result_key.append(xor)
            key_sum = key_sum + xor

        self._xor_control_sum = key_sum % len(self._primary_key)
        self._xor_key = result_key

    def _set_shifts(self):
        """
            Формируем итоговый сдвиг каждого слова. Каждое значение сдвига уникально!
        """
        result_key = []
        full_set = set()
        for idx in range(0, len(self._xor_key)):
            i = self._xor_key[idx] if self._xor_key[idx] < 1000 else int(str(self._xor_key[idx])[:3]) + (idx+1)
            el = i - self._xor_control_sum if idx % 2 > 0 else i + self._xor_control_sum
            el = -el if el < 0 else el
            while el in full_set:
                el = el + 1
            full_set.add(el)
            result_key.append(el)
        self._shifts = result_key

    def get_pin(self) -> list:
        return self._pin

    def get_primary_key(self) -> list:
        return self._primary_key

    def get_xor_key(self) -> list:
        return self._xor_key

    def get_shifts(self) -> list:
        return self._shifts

    def get_xor_control_sum(self) -> int:
        return self._xor_control_sum

    def get_seed_len(self) -> int:
        return self.seed_len

    def _random_fog(self) -> list:
        words_count = max(self._shifts) + random.randint(self._rand_min,
                                                         self._rand_max)
        _fog = bip.random_as_string(words_count, separator=" ", lang="en")
        return _fog.split()

    def get_fog(self, _phrase: str) -> list:
        """ создаем туман """
        _fog = self._random_fog()
        seed = _phrase.split()
        for word, k in enumerate(range(self.seed_len, 0, -1)):
            _fog.insert(self._shifts[k-1], seed[k - 1])
        return _fog

    def restore(self, _fog: str) -> str:
        """ извлекаем из тумана слова в нужном порядке """
        _seed = []
        _fog = _fog.split()
        for i in (range(0, self.seed_len)):
            k = self._shifts[i]
            _seed.append(_fog[k])
            _fog.pop(k)
        return ' '.join(_seed)

    @staticmethod
    def list_to_str(lst: list) -> str:
        return ' '.join(lst)


if __name__ == "__main__":
    pin = '1 2 3 4 5'
    phrase = '''1 2 3 4 5 6 7 8 9 10 11 12'''
    seed_len = len(phrase.split())
    fog = Fog(pin, 12)

    # замешивание тумана
    result = fog.get_fog(phrase)
    print("Fog: ", fog.list_to_str(result))
    print("Total words in fog: ", len(result))

    print("Pin: ", fog.get_pin())
    print("Key: ", fog.get_primary_key())
    print("XOR: ", fog.get_xor_key())
    print("Shifts: ", fog.get_shifts())
    print("XOR control sum: ", fog.get_xor_control_sum())

    # восстановление фразы из тумана
    words = fog.list_to_str(result)
    print("Restored phrase: ", fog.restore(words))
