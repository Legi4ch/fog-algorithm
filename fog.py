# fog-algorithm
import bip39gen as bip

class Fog():
    
    def __init__(self):
        pass

    
    def glue_key(self, pin:str, seed_len:int) -> str:
        """ формируем предварительный ключ длиной seed_len - 1 из символов pin """
        if len(pin) >= seed_len:
            return pin[0:seed_len]
        else:
            key = ''
            while len(key) < seed_len:
                key = key + pin        
            return key[0:seed_len-1]     
        

    def __make_key(self, key:str) -> list:
        """ 
            Формируем итоговый ключ длиной seed_len - 1 из символов 
            предварительного ключа. Последний символ - остаток от деления всей суммы ключа на длину ключа      
        """
        result_key = []
        key_sum = 0
        for i in range(0, len(key)):
            k = int(key[i])
            if (i % 2 == 0):
                result_key.append(k+i)
                key_sum = key_sum + (k+i)
            else:
                result_key.append(k*i)
                key_sum = key_sum + (k*i)
        cs = key_sum % len(key)
        result_key.append(cs)
        return result_key
    
    
    def make_key(self, key:str) -> list:
        """ 
            Формируем итоговый ключ длиной seed_len - 1 из символов 
            предварительного ключа. Последний символ - остаток от деления всей суммы ключа на длину ключа      
        """
        result_key = []
        key_sum = 0
        for i in range(0, len(key)):
            k = int(key[i])
            el = 0
            el = k+i*10 if i % 2 == 0 else k**2
            if el in result_key:
                result_key.append(el*2)
                key_sum = key_sum + (el*2)
            else:
                result_key.append(el)
                key_sum = key_sum + (el)
            
        cs = key_sum % len(key)
        result_key.append(cs)
        return result_key    
                
       
    
    def random_fog(self, key:list) -> list:
        words_count =  sorted(key)[-1] + 5 # создаем список на 20 слов длиннее самого большого значения ключа
        fog = bip.random_as_string(words_count, separator=" ", lang="en")
        return fog.split()

    
           
    def make_fog(self, fog:list, seed_len:int, key:list, phrase:str) -> list:
        """ создаем туман """
        _fog = fog.copy()
        seed = phrase.split()
        for word, k in enumerate(range(seed_len, 0, -1)):
            _fog.insert(int(key[k-1]), seed[k-1])
        return _fog      

    
    def restore(self, fog:str, seed_len:int, key:list) -> str:
        """ извлекаем из тумана слова в нужном порядке """
        _seed = []
        _fog = fog.split()
        for i in (range(0,seed_len)):
            k = int(key[i])
            _seed.append(_fog[k])
            _fog.pop(k)    
        return ' '.join(_seed) 
    
    
    def list_to_str(self, fog:list) -> str:
         return ' '.join(fog)    
        

if __name__ == "__main__":
    
    pin = '123456'
    seed_len = 12
    phrase = '''1 2 3 4 5 6 7 8 9 10 11 12'''

    # инициализация объекта и создание ключа по пин-коду
    fog = Fog()
    glue_key = fog.glue_key(pin, seed_len)
    key = fog.make_key(glue_key)
    print (key)
    
    # замешивание тумана
    words_list = fog.random_fog(key) 
    result = fog.make_fog(words_list, seed_len, key, phrase)    
    print (result)
    
    
    # восстановление фразы из тумана
    words = fog.list_to_str(result)
    
    restored = fog.restore(words, seed_len, key)
    print(restored)
