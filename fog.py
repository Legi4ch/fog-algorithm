# fog-algorithm
import bip39gen as bip
import random


class Fog:
    _key: list
    _shift: int
    seed_len: int
    pin: str

    def __init__(self, pin: str, seed_len: int):
        self.seed_len = seed_len
        self.pin = pin
        self._set_key(pin, seed_len)

    def _glue_pin(self) -> str:
        """ формируем предварительный ключ длиной seed_len из символов pin """
        if len(self.pin) >= self.seed_len:
            return self.pin[0:self.seed_len]
        else:
            key = ''
            while len(key) < self.seed_len:
                key = key + self.pin
            return key[0:self.seed_len]

    def _set_key(self, _pin: str, _seed_len: int):
        """
            Формируем итоговый ключ из символов предварительного ключа.
        """
        result_key = []
        key_sum = 0
        key = self._glue_pin()

        for i in range(0, len(key)):
            el = int(key[i]) + i * 10 if i % 2 > 0 else int(key[i]) ** 2
            result_key.append(el)
            key_sum = key_sum + el

        cs = key_sum % len(key)
        self._key = result_key
        self._shift = cs

    def get_key(self) -> list:
        return self._key

    def get_shift(self) -> int:
        return self._shift

    def get_seed_len(self) -> int:
        return self.seed_len

    def _random_fog(self) -> list:
        words_count = sorted(self._key)[-1] + random.randint(self._shift,
                                                             self._shift * 2)  # создаем список > max значения в ключе
        _fog = bip.random_as_string(words_count, separator=" ", lang="en")
        return _fog.split()

    def get_fog(self, _phrase: str) -> list:
        """ создаем туман """
        _fog = self._random_fog()
        seed = _phrase.split()
        for word, k in enumerate(range(self.seed_len, 0, -1)):
            _fog.insert(int(self._key[k - 1] + self._shift), seed[k - 1])
        return _fog

    def restore(self, _fog: str) -> str:
        """ извлекаем из тумана слова в нужном порядке """
        _seed = []
        _fog = _fog.split()
        for i in (range(0, self.seed_len)):
            k = int(self._key[i] + self._shift)
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
    print("Key: ", fog.get_key())

    # замешивание тумана
    result = fog.get_fog(phrase)
    print("Fog: ", fog.list_to_str(result))

    print("Shift: ", fog.get_shift())

    # восстановление фразы из тумана
    words = fog.list_to_str(result)
    print("Restored: ", fog.restore(words))
