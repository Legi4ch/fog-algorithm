# fog-algorithm
import bip39gen as bip

class Fog():
    
    def __init__(self):
        pass
    
    
    def generate_key(self, pin:str, seed_len:int) -> str:
        """ формируем ключ длиной seed_len из символов pin """
        if len(pin) >= seed_len:
            return pin[0:seed_len]
        else:
            key = ''
            while len(key) < seed_len:
                key = key + pin        
            return key[0:seed_len]

    def random_fog(self, words_count:int) -> list:
        _fog = bip.random_as_string(words_count, separator=" ", lang="en")
        return _fog.split()
        
    def make_fog(self, fog:list, seed_len:int, key:str, phrase:str) -> list:
        """ создаем туман """
        _fog = fog.copy()
        _seed = phrase.split()
        for word, k in enumerate(range(seed_len, 0, -1)):
            _fog.insert(int(key[k-1]),_seed[k-1])
        return _fog      

    
    def restore(self, fog:str, seed_len:int, key:str) -> str:
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
    
    pin = '1511706'
    seed_len = 12
    words_count = 100
    phrase = '''collection reputation clash haunt flesh reptile desire word tumble chance wood glove'''
    
    fog = Fog()
    key = fog.generate_key(pin, seed_len)
    words_list = fog.random_fog(words_count)
    result = fog.make_fog(words_list, seed_len, key, phrase)

    
    # получаем открытую строку
    fog_str = fog.list_to_str(result)
    print ("Fog: ", fog_str)
    
    restored = fog.restore(fog_str, seed_len, key)
    print ("Restored seed:" , restored) 
