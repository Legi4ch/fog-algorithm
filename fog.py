# fog-algorithm
import bip39gen as bip
import random


class Fog():

    _key:list
    _shift:int
    _seed_len:int


    def __init__(self, pin:str, seed_len:int):
        self._set_key(pin, seed_len)
        self._seed_len = seed_len
        

    def _glue_pin(self, pin: str, seed_len: int) -> str:
        """ формируем предварительный ключ длиной seed_len из символов pin """
        if len(pin) >= seed_len:
            return pin[0:seed_len]
        else:
            key = ''
            while len(key) < seed_len:
                key = key + pin
            return key[0:seed_len]

        
    def _set_key(self, pin: str, seed_len: int):
        """
            Формируем итоговый ключ из символов предварительного ключа. 
        """
        result_key = []
        key_sum = 0
        key = self._glue_pin(pin, seed_len)
        
        for i in range(0, len(key)):
            el = int(key[i]) + i * 10 if i % 2 > 0 else int(key[i]) ** 2
            result_key.append(el)
            key_sum = key_sum + (el)
        
        cs = key_sum % len(key)
        self._key = result_key
        self._shift = cs
        

    def get_key(self) -> list:
        return self._key


    def get_shift(self) -> int:
        return self._shift


    def get_seed_len(self) -> int:
        return self._seed_len
    

    def _random_fog(self) -> list:
        words_count = sorted(self._key)[-1] + random.randint(self._shift, self._shift*2)# создаем список > max значения в ключе
        fog = bip.random_as_string(words_count, separator=" ", lang="en")
        return fog.split()
    

    def get_fog(self, phrase: str) -> list:
        """ создаем туман """
        fog = self._random_fog()
        seed = phrase.split()
        for word, k in enumerate(range(self._seed_len, 0, -1)):
            fog.insert(int(self._key[k - 1] + self._shift ), seed[k - 1])
        return fog

    
    def restore(self, fog: str) -> str:
        """ извлекаем из тумана слова в нужном порядке """
        _seed = []
        _fog = fog.split()
        for i in (range(0, self._seed_len)):
            k = int(self._key[i] + self._shift)
            _seed.append(_fog[k])
            _fog.pop(k)
        return ' '.join(_seed)
    

    def list_to_str(self, lst: list) -> str:
        return ' '.join(lst)


if __name__ == "__main__":
    
    pin = '12345'
    seed_len = 12
    phrase = '''1 2 3 4 5 6 7 8 9 10 11 12'''

    fog = Fog(pin, seed_len)
    print("Key: ",fog.get_key())

    # замешивание тумана
    result = fog.get_fog(phrase)
    print("Fog: ", fog.list_to_str(result))

    # восстановление фразы из тумана
    words = fog.list_to_str(result)
    print("Restored: ", fog.restore(words))
