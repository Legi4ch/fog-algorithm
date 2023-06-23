# fog-algorithm

### Алгоритм Туман для _относительно безопасного_ публичного хранения сид фраз в открытых и небезопасных местах, таких как: Гугл диск и прочие диски, почта, в том числе и распечатки на бумаге и т.д.

> Приведенный ниже способ не является алгоритмом шифрования. Это возможность хранить сид-фразу относительно безопасно и не запоминать ее. Используйте на свой страх и риск.

Полученный по алгоритму набор слов можно распечатать на бумаге, закинуть на почту и т.д. 
Вам не потребуется программа для восстановления фразы, если вы понимаете, как работает алгоритм и помните пин-код.


#### Описание работы алгоритма.

Пин-код используемый в этом примере - 123456.

Сид фраза из 12 слов, которую мы собираемся положить в публичном месте после замешивания в туман.
Для наглядности будем использовать цифры вместо слов.
1 2 3 4 5 6 7 8 9 10 11 12

Генерировать первичный туман лучше всего случано.
Рекомендую использовать библиотеку bip39gen (_Python_).
<https://github.com/massmux/bip39gen>

`
['chuckle', 'thought', 'knee', 'flip', 'harvest', 'comic', 'mutual', 'cost', 'film', 'increase', 'balcony', 'weapon', 'market', 'oven', 'dwarf', 'attitude', 'affair', 'lend', 'renew', 'tennis', 'coyote', 'ecology', 'taxi', 'claim', 'business', 'genius', 'recycle', 'protect', 'wire', 'waste', 'feel', 'ocean', 'sugar', 'amount', 'circle', 'road', 'sense', 'daughter', 'morning', 'minute', 'purse', 'virtual', 'dash', 'battle', 'airport', 'tribe', 'frog', 'cousin', 'reunion', 'solid', 'fruit', 'permit', 'future', 'gauge', 'victory', 'dice', 'bag', 'shadow', 'rich', 'ugly', 'track', 'discover', 'ensure', 'always', 'risk', 'pattern', 'random', 'slot', 'inner', 'question', 'regular', 'draft', 'you', 'term', 'news', 'humble', 'culture', 'curve', 'vehicle', 'settle', 'brass', 'occur', 'crucial', 'cherry', 'vast', 'bench', 'resource', 'siren', 'brick', 'picnic', 'certain', 'town', 'fabric', 'judge', 'twenty', 'odor', 'title', 'lend', 'unable', 'blouse']
`
#### Ключ тумана

##### Первичный ключ
Обюразуется склеиванием пин-кода с самим собой до получения длины равной кол-ву слов в сид фразе минус 1. Ниже будет ясно почему меньше на единицу.
В этом пример длина пин-кода 6 символов. Поэтому мы _добиваем_ еще 5 символов из начала пин-кода к его концу.
Таким образом первичный ключ тумана 12345612345, всего 11 символов.

##### Генерируем ключ тумана

Первичный ключ выглядит так. __К__ это контрольный символ, его расчитаем позже.
| 0  | 1  |  2 | 3  | 4  |  5 | 6  | 7  | 8  | 9  | 10  | К |
|---|---|---|---|---|---|---|---|---|---|---|---|
|  1 | 2  | 3  | 4  | 5  | 6  | 1  | 2  | 3  | 4  | 5  |  |

Теперь, каждый цифру первичного ключа имеющую четный индекс складываем с индексом.
Каждую цифру первичного ключа имеющую нечетный индекс возводим в квадрат.

Получаем такой вид ключа тумана.
| 0  | 1  |  2 | 3  | 4  |  5 | 6  | 7  | 8  | 9  | 10  | К |
|---|---|---|---|---|---|---|---|---|---|---|---|
|  1 | 2  | 3  | 4  | 5  | 6  | 1  | 2  | 3  | 4  | 5  |  |
|  1 | 4  |5  | 16  | 9  | 36  | 7  | 4  | 11  | 16  |15  |  |

Контрольный символ вычисляется как остаток от деления суммы всех цифр ключа на кол-во цифр в ключе.
В нашем случае 1+4+5+16+9+36+7+4+11+16+15 = 124. Остаток деления 124 % 11 = 3

Мы получили ключ тумана.
| 0  | 1  |  2 | 3  | 4  |  5 | 6  | 7  | 8  | 9  | 10  | К |
|---|---|---|---|---|---|---|---|---|---|---|---|
|  1 | 2  | 3  | 4  | 5  | 6  | 1  | 2  | 3  | 4  | 5  |  |
|  1 | 4  |5  | 16  | 9  | 36  | 7  | 4  | 11  | 16  |15  | 3 |


#### Создание публичного тумана
_Для генерации тумана лучше использовать программу, ибо делать это руками будет достаточно неудобно)_
После генерации первичного тумана из случайных слов (выше), записываем нашу сид фразу в туман таким образом:
1. Преобразуем первичный туман в список (_для Pyhon_)
2. Берем последний символ ключа тумана (_обратный цикл_). Его индекс 11, а значение 3.
3. Берем из сид фразы слово стоящее под номер 11 и добавляем (_insert_) его в список с индексом 3.
4. Список увеличивается на одно слово, а старые индексы смещаются.
5. Повторяем с предыдущим символом из ключа (10,15) и увеличенным списком.
6. Таким образом, полученный список увеличится на 12 слов.
7. Преобразуем список в строку и полученный набор слов можно распечать, сохранить на компьютере и т.д.



#### Итоговый туман, после 12 проходов
`
['chuckle', '1', 'thought', 'knee', '12', '2', '8', '3', 'flip', 'harvest', '7', 'comic', '5', 'mutual', 'cost', 'film', 'increase', '9', 'balcony', '4', 'weapon', 'market', 'oven', '11', '10', 'dwarf', 'attitude', 'affair', 'lend', 'renew', 'tennis', 'coyote', 'ecology', 'taxi', 'claim', 'business', 'genius', 'recycle', 'protect', 'wire', 'waste', '6', 'feel', 'ocean', 'sugar', 'amount', 'circle', 'road', 'sense', 'daughter', 'morning', 'minute', 'purse', 'virtual', 'dash', 'battle', 'airport', 'tribe', 'frog', 'cousin', 'reunion', 'solid', 'fruit', 'permit', 'future', 'gauge', 'victory', 'dice', 'bag', 'shadow', 'rich', 'ugly', 'track', 'discover', 'ensure', 'always', 'risk', 'pattern', 'random', 'slot', 'inner', 'question', 'regular', 'draft', 'you', 'term', 'news', 'humble', 'culture', 'curve', 'vehicle', 'settle', 'brass', 'occur', 'crucial', 'cherry', 'vast', 'bench', 'resource', 'siren', 'brick', 'picnic', 'certain', 'town', 'fabric', 'judge', 'twenty', 'odor', 'title', 'lend', 'unable', 'blouse']
`

#### Восстановление сид фразы из тумана достаточно просто выполнить без компьютера
Теперь цикл уже прямой.
1. Создаем пустой список для записи слов из тумана.
2. Преобразуем строку тумана в список (_для Python_)
3. Создаем снова ключ тумана по пин-коду
4. Берем нулевой индекс ключа. Это 1.
5. Добавляем слово из туманного списка с индексом 1 всписок для слов. Это первое слово из сид фразы.
6. Из туманного списка удаляется элемент с индексом 1. Список укорачивается.
7. Шаги 3-5 повторяются до перебора всей длины ключа.

