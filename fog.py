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
        self.pin = _pin
        self._set_primary_key()
        self._set_xor_key()
        self._set_shifts()

    def _glue_pin(self) -> str:
        """ формируем предварительный ключ длиной seed_len из символов pin """
        if len(self.pin) >= self.seed_len:
            return self.pin[0:self.seed_len]
        else:
            key = ''
            while len(key) < self.seed_len:
                key = key + self.pin
            return key[0:self.seed_len]

    def _set_primary_key(self):
        """
            Формируем первичный ключ из пин-кода ключа.
        """
        result_key = []
        key_sum = 0
        key = self._glue_pin()

        for i in range(0, len(key)):
            el = int(key[i]) + ((i+1) * 10) if i % 2 > 0 else int(key[i]) ** 2
            result_key.append(el)
            key_sum = key_sum + el

        self._primary_key = result_key

    def _set_xor_key(self):
        """
            Формируем xor ключ из первичного ключа.
        """
        result_key = []
        key_sum = 0
        for i in range(0, len(self._primary_key)):
            xor = self._primary_key[i] ^ (i+1)
            result_key.append(xor)
            key_sum = key_sum + xor

        self._xor_control_sum = key_sum % len(self._primary_key)
        self._xor_key = result_key

    def _set_shifts(self):
        """
            Формируем итоговый сдвиг каждого слова
        """
        result_key = []
        for i in range(0, len(self._xor_key)):
            if i % 2 > 0:
                el = self._xor_key[i] + self._primary_key[i] - self._xor_control_sum
            else:
                el = self._xor_key[i] + self._primary_key[i] + self._xor_control_sum
            result_key.append(el)
        self._shifts = result_key

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
    pin = '12345'
    phrase = '''1 2 3 4 5 6 7 8 9 10 11 12'''
    seed_len = len(phrase.split())
    fog = Fog(pin, seed_len)

    # замешивание тумана
    result = fog.get_fog(phrase)
    print("Fog: ", fog.list_to_str(result))

    print("Key: ", fog.get_primary_key())
    print("XOR: ", fog.get_xor_key())
    print("Shifts: ", fog.get_shifts())
    print("XOR control sum: ", fog.get_xor_control_sum())

    # восстановление фразы из тумана
    words = fog.list_to_str(result)
    print("Restored phrase: ", fog.restore(words))
