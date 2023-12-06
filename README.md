# fog-algorithm

### Туман - стеганографический алгоритм для _относительно безопасного_ хранения сид фраз в незащищенных местах, таких как: Гугл и прочие диски, почта, распечатки на бумаге и т.д.

> Приведенный ниже способ не является алгоритмом шифрования. Это возможность хранить сид-фразу относительно безопасно и не запоминать ее. Используйте на свой страх и риск.

Полученный по алгоритму набор слов можно сохранить на облачном диске, закинуть на почту и т.д. 
По туману слов применяя алгоритм написанный на любом удобном языке, можно восстановить сид фразу зная пин-код.


#### Описание работы алгоритма.

Пин-код используемый в этом примере - 1 2 3 4 5. Обратите внимание, пин-код это не число, это последовательность чисел!

Сид фраза, которую мы собираемся положить в публичном месте после замешивания в туман, состоит из 12 слов.
Для наглядности в примере работы алгоритма будем использовать цифры вместо настоящих слов.
1 2 3 4 5 6 7 8 9 10 11 12

Генерировать первичный туман лучше всего случайно.
Рекомендую использовать библиотеку bip39gen (_Python_).
<https://github.com/massmux/bip39gen>

#### Создаем первичный туман из случайных слов с помощью bip39gen

```python
import bip39gen as bip
import random
def random_fog() -> list:
  words_count = 300
  fog = bip.random_as_string(words_count, separator=" ", lang="en")
  return fog.split()
print(random_fog())
```


##### Исходный ключ
Образуется склеиванием пин-кода с самим собой до получения длины равной кол-ву слов в сид фразе.
В этом пример длина пин-кода 5 чисел. Поэтому мы _добиваем_ еще 7 чисел из начала пин-кода к его концу.

Таким образом исходный ключ тумана 1 2 3 4 5 1 2 3 4 5 1 2, всего получается 12 чисел, для фразы из 12 слов.

##### Первичный ключ
Для получения первичного ключа надо проделать операцию с каждым элементом исходного ключа:

каждую цифру исходного ключа имеющую нечетный индекс складываем с индексом умноженным на 10.

каждую цифру исходного ключа имеющую четный индекс возводим в квадрат.

##### XOR ключ
Для получения XOR ключа надо произвести xor операцию: индекс первичного ключа (считать от 1) xor значение первичного ключа от этого индекса.

В MS Excel эта операция назвается БИТ.ИСКЛИЛИ(A;B)

##### Контрольное число XOR ключа
Это число понадобится на последнем шаге. Вычисляется как остаток от деления суммы всех элементов XOR ключа на кол-во его элементов.

##### Ключ сдвига
Это последний шаг подготовки, который выполняется так:

1. Если текущее значение элемента в XOR ключе больше 1000, то от значения в XOR  ключе берутся только первые три цифры и к ним прибавляется текущий индекс цикла (считать от 1)
   Если значение в XOR ключе меньше 1000, то оно остается как есть.

2. Для четного индекса XOR ключа берется его значение полученное на шаге 1 и складывается с контрольным XOR числом.
   Для нечетного индекса XOR ключа берется его значение полученное на шаге 1 и из него вычитается контрольное XOR число.

3. Если итоговое значение получилось с отрицательным знаком, то меняем знак на положительный.
   
4. Если полученное значение уже содержится в сдвигах, увеличиваем его на 1 до тех пор пока он не станет уникальным.


Все преобразования показаны в таблице. Контрольное число XOR ключа в данном случае равно 11.

|   Индекс	    |   1	|   2	|   3	|   4	|   5	|   6	|   7	|   8	|   9	|   10	|   11	|   12	|
|---	        |---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|---	|
|Пин-код        |   1 	|   2	|   3	|   4	|   5	|   1	|   2	|   3	|   4	|   5	|   1	|   2	|
|Первичный ключ |   1	|  22	|   9	|   44	|   25	|   61	|   4	|   83	|   16	|   105	|   1	|   122	|
|XOR         	|   0   |  20 	|  10 	|   40	|   28	|   59	|   3	|   91	|   25	|   99	|   10	|  118 	|
|Сдвиг  	    |   11	|  9 	|  21 	|   29	|   39	|   48	|   14	|   80	|   36	|   88	|   22	|  107 	|

Вы также можете провести эксперименты с разными значениями пин-кода в с помощью файла keys_calculator.xlsx 


Теперь у нас есть сдвиг для каждого слова из сид фразы. Обратите внимание, что в 11 индексе установлено сдвиг 22. В расчете он полчуается равным 21,
но 21 уже есть в индексе 3. Поэтому для индекса 11 полученный результат был увеличен на единицу.

#### Создание публичного тумана
_Для генерации тумана лучше использовать программу, ибо делать это руками будет достаточно неудобно)_
После генерации первичного тумана из случайных слов (выше), записываем нашу сид фразу в туман таким образом:
1. Преобразуем первичный туман в список (_для Pyhon_)
2. Берем последний символ ключа тумана (_обратный цикл_). Его индекс 12, а значение сдвига 107.
3. Берем из сид фразы слово стоящее под номером 12 и добавляем его в туман с индексом 107.
4. Туман увеличивается на одно слово, а индексы тумана смещаются на единицу.
5. Повторяем шаги 3-4 до перебора всей длины ключа.
6. Таким образом, полученный список увеличится на 12 слов.
7. К первичному туману необходимо добавить некоторое случайное дополнительное кол-во слов, чтобы общее их число было больше чем максимальный сдвиг.
8. Преобразуем список в строку и полученный набор слов можно распечать, сохранить на компьютере и т.д.



#### Туман, после полного прохода по все фразе
`
flight enough elbow custom certain pioneer air miracle damp 2 dragon 1 identify casino 
audit fiction 7 kidney awful drift reward boost twelve 3 all 11 retreat way kite forget 
glory direct 4 ask mixed spoil wrong away chief muscle twin 9 just 5 melody fault clean 
problem tip antenna tube lazy used 6 guide survey write dolphin wreck extend mean keen 
wine rain category high day drink cake bulk verb barrel canyon solar wire grant quote 
first taste stable grid tribe sugar swing exchange news swear 8 venue direct tank obey 
draw run debris rebuild claim 10 defy hotel south night flash panda syrup left pet jacket 
cat cheap assist weapon cup silk wasp oil normal super 12 initial gauge such burden reform 
adapt hard style fall affair actual chalk draft twist hire wrist icon work notable frost 
idle chaos zoo logic scatter giggle panel strong screen match grow obtain
`

#### Восстановление сид фразы из тумана выполняется в обратном порядке
Теперь цикл уже прямой.
1. Создаем пустой список для записи слов из тумана.
2. Преобразуем строку тумана в список (_для Python_)
3. Создаем все ключи по пин-коду
4. Берем нулевой индекс ключа. Это 11.
5. Добавляем слово из туманного списка с индексом 1 в список слов подготовленный на шаге 1. Это первое слово из сид фразы.
6. Из туманного списка удаляется найденный на шаге 5 элемент. Туман слов укорачивается, индексы смещаются.
7. Шаги 3-5 повторяются до перебора всей длины ключа.


#### Несколько слов о безопасности

__Это не криптографический алгоритм и не способ шифрования инофрмации!!! Это алгоритм стеганографии!!!__

В работе алгоритма нет никаких криптографических методов. Это способ скрыть информацию в другой информации. Суть данного способа в том, что правильный порядок слов и их место в конечном тексте
находятся в неизвестных местах, среди других слов. Сами слова ключевой фразы все равно присутствуют в получаемом тексте.

Смысл алгоритма туман - получить способ восстанавливать забытую, либо утерянную ключевую фразу из относительно безопасного места хранения в тумане, без применения каких-либо программ вообще.

В качестве дополнительного способа защиты можно увеличить ключевую фразу, которую вы хотите спрятать, за счет добавления слов в ее начало, середину, конец и т.д.

Например:

фразу truck token kiwi two riot orient group skirt loud mass version guard, можно изменить так:

start truck token kiwi two riot orient middle group skirt loud mass version guard finish

Мы добавляем start, middle, finish к сид фразе и увеличиваем таким образом  ее длину с 12 до 15 слов. Их разброс по тексту изменится соответственно.

__Никогда не генерируйте и не публикуйте разные версии тумана с одним пин-кодом!!!__

Это серьезно снижает безопасность способа, так как обладая даже двумя вариантами текста, можно будет легко вычислить какие слова не меняют свой порядок в нем.
Разумеется в этом случае все еще остается неизвестным правильный порядок слов, но данный факт не должен вас обнадеживать.

__Пин-код должен соответствовать всем требованиям безопасности. Не указывайте свой день рождения, дни рождения детей, жен и прочие даты. 
Не указывайте в качестве пин-кода свой номер телефона или номер автомобиля.__


