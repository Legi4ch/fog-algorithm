# fog-algorithm

### Туман - стеганографический алгоритм для _относительно безопасного_ хранения сид фраз в незащищенных местах, таких как: Гугл и прочие диски, почта, распечатки на бумаге и т.д.

> Приведенный ниже способ не является алгоритмом шифрования. Это возможность хранить сид-фразу относительно безопасно и не запоминать ее. Используйте на свой страх и риск.

Полученный по алгоритму набор слов можно распечатать на бумаге, закинуть на почту и т.д. 
Вам не потребуется программа для восстановления фразы, если вы понимаете, как работает алгоритм и помните пин-код.
Получить ключ по пин-коду можно даже в табличке excel или вообще на бумажке.


#### Описание работы алгоритма.

Пин-код используемый в этом примере - 12345.

Сид фраза из 12 слов, которую мы собираемся положить в публичном месте после замешивания в туман.
Для наглядности будем использовать цифры вместо слов.
1 2 3 4 5 6 7 8 9 10 11 12

Генерировать первичный туман лучше всего случайно.
Рекомендую использовать библиотеку bip39gen (_Python_).
<https://github.com/massmux/bip39gen>

#### Создаем первичный туман из случайных слов
`
unique permit behind cradle flash end accuse soap verb fitness maximum pupil elder wait thing cradle pilot alpha giraffe wage siege below artefact chicken name improve random clarify teach chunk zone tip middle close truck token kiwi two riot orient group skirt loud mass version guard rail plate palace vessel eager zebra blood scissors high napkin teach match crime glimpse monitor food mention fit clog summer march chalk staff kick transfer nut brisk ahead effort cart owner exact mushroom afford icon review lobster course fat garage busy spin shop grow luggage need couple side bachelor energy symptom naive ribbon sing way turkey ripple state teach admit tribe trouble entire people fabric either cool canoe
`

##### Первичный ключ
Образуется склеиванием пин-кода с самим собой до получения длины равной кол-ву слов в сид фразе.
В этом пример длина пин-кода 5 символов. Поэтому мы _добиваем_ еще 7 символов из начала пин-кода к его концу.
Таким образом первичный ключ тумана 123451234512, всего 12 символов.

##### Генерируем ключ тумана

Первичный ключ выглядит так. __S__ это сдвиг, его расчитаем позже, когда получим все значения.
| 0  | 1  |  2 | 3  | 4  |  5 | 6  | 7  | 8  | 9  | 10 | 11 | S |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|  1 | 2  | 3  | 4  | 5  | 1  | 2  |3  | 4  | 5  | 1  | 2 | 

Теперь, каждую цифру первичного ключа имеющую нечетный индекс складываем с индексом умноженным на 10.
Каждую цифру первичного ключа имеющую четный индекс возводим в квадрат.

Получаем такой вид ключа тумана.
| 0  | 1  |  2 | 3  | 4  |  5 | 6  | 7  | 8  | 9  | 10 | 11 | S |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|  1 | 2  | 3  | 4  | 5  | 1  | 2  |3  | 4  | 5  | 1  | 2 | 
|  1 | 12  | 9  | 34  | 25  | 51  | 4  | 73  | 16  | 95  | 1  | 112 | 

Теперь надо вычислить сдвиг ключа. Он получается вычислением остатка от деления суммы всех цифр ключа на длину ключа.

В нашем случае 1 + 12 +9 + 34 + 25 + 51 + 4 + 73 + 16 + 95 + 1 + 112 = 433. Остаток деления 433 % 12 = 1.

Мы получили ключ тумана и сдвиг.

#### Создание публичного тумана
_Для генерации тумана лучше использовать программу, ибо делать это руками будет достаточно неудобно)_
После генерации первичного тумана из случайных слов (выше), записываем нашу сид фразу в туман таким образом:
1. Преобразуем первичный туман в список (_для Pyhon_)
2. Берем последний символ ключа тумана (_обратный цикл_). Его индекс 12, а значение 112.
3. Берем из сид фразы слово стоящее под номером 12 и добавляем его в туман с индексом 113 (112 + 1 сдвиг).
4. Туман увеличивается на одно слово, а старые индексы смещаются.
5. Повторяем шаги 3-4 до перебора всей длины ключа.
6. Таким образом, полученный список увеличится на 12 слов.
7. Преобразуем список в строку и полученный набор слов можно распечать, сохранить на компьютере и т.д.



#### Итоговый туман, после полного прохода
`
unique permit 1 11 behind cradle 7 flash end accuse soap 3 verb fitness 2 maximum pupil elder wait thing cradle 9 pilot alpha giraffe wage siege below artefact 5 chicken name improve random clarify teach chunk zone 4 tip middle close truck token kiwi two riot orient group skirt loud mass version guard rail plate palace 6 vessel eager zebra blood scissors high napkin teach match crime glimpse monitor food mention fit clog summer march chalk staff kick transfer nut 8 brisk ahead effort cart owner exact mushroom afford icon review lobster course fat garage busy spin shop grow luggage need couple side bachelor 10 energy symptom naive ribbon sing way turkey ripple state teach admit tribe trouble entire people fabric either cool 12 canoe
`

#### Восстановление сид фразы из тумана достаточно просто выполнить без компьютера
Теперь цикл уже прямой.
1. Создаем пустой список для записи слов из тумана.
2. Преобразуем строку тумана в список (_для Python_)
3. Создаем снова ключ тумана по пин-коду
4. Берем нулевой индекс ключа. Это 1.
5. Добавляем слово из туманного списка с индексом 1 + 1 (сдвиг) в список слов. Это первое слово из сид фразы.
6. Из туманного списка удаляется элемент с индексом 1. Туман слов укорачивается, индексы смещаются.
7. Шаги 3-5 повторяются до перебора всей длины ключа.

Как видно, все операции по расчету ключа из пин-кода несложно сделать вручную или например в excel.
Также можно восстановить фразу с бумажного листка, просто вычеркивая найденные по ключу и сдвигу слова и считая индекс от нуля каждый раз для следующего слова.

#### Несколько слов о безопасности

__Это не криптографический алгоритм и не способ шифрования инофрмации!!! Это алгоритм стеганографии!!!__

В работе алгоритма нет никаких криптографических методов. Это способ скрыть информацию в другой информации. Суть данного способа в том, что правильный порядок слов и их место в конечном тексте
находятся в неизвестных местах, среди других слов. Сами слова ключевой фразы все равно присутсвуют в получаемом тексте.

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


