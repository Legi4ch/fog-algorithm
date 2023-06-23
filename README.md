# fog-algorithm

### Алгоритм Туман, для публичного хранения сид фраз в открытых и небезопасных местах? таки как: Гугл диск и прочие диски, почта, в том числе и распечатки на бумаге и т.д.

Для создания тумана необходимо лишь придумать и запомнить пин-код из цифр. Полученный по алгоритму набор слов можно распечатать на бумаге, закинуть на почту и т.д. 
Вам не потребуется программа для восстановления фразы, если вы понимаете, как работает алгоритм и помните пин-код.


#### Описание работы алгоритма.

Пин-код в этом примере - 1511706

Сид фраза из 12 слов, которую мы собираемся положить в публичном месте после замешивания в туман:
``` python
['collection', 'reputation', 'clash', 'haunt', 'flesh', 'reptile', 'desire', 'word', 'tumble', 'chance', 'wood', 'glove']
```

Исходный набор слов, изначальный туман, без наших слов, либо с нашими словами, это не важно.

`
['soprano', 'reptile', 'professional', 'dominate', 'tumble', 'organisation', 'reputation', 'ready', 'combination', 'occupation', 'hostility', 'haunt', 'desire', 'combine', 'rebellion', 'flesh', 'galaxy', 'nuclear', 'improvement', 'reporter', 'integrated', 'charm', 'plug', 'talk', 'disaster', 'familiar', 'branch', 'provincial', 'manner', 'overwhelm', 'collection', 'glove', 'porter', 'senior', 'wood', 'morning', 'bench', 'clash', 'connection', 'clothes', 'word', 'dealer', 'kinship', 'contain', 'mayor', 'double', 'soprano', 'reptile', 'chance', 'professional', 'dominate', 'ostracize', 'announcement', 'tumble', 'organisation', 'trial', 'reputation', 'ready', 'combination', 'occupation', 'hostility', 'haunt', 'desire', 'combine', 'rebellion', 'flesh', 'galaxy', 'nuclear', 'improvement', 'reporter', 'integrated', 'charm', 'plug', 'talk', 'disaster', 'familiar', 'branch', 'provincial', 'manner', 'overwhelm', 'collection', 'glove', 'porter', 'senior', 'wood', 'morning', 'bench', 'clash', 'connection', 'clothes']
`
#### Ключ тумана
Длина ключа должна соответствовать кол-ву слов в сид фразе. В этом пример длина пин-кода 7 символов. Поэтому мы _добиваем_ еще 5 символов из начала пин-кода к его концу.
Таким образом ключ тумана 151170615117, всего 12 символов.

#### Создание публичного тумана
_Для генерации тумана лучше использовать программу, ибо делать это руками будет достаточно неудобно)_
После генерации облака из случайных слов (выше), записываем нашу сид фразу в туман таким образом:
1. Преобразуем облако слов в список (_для Pyhon_)
2. Берем последний символ ключа (_обратный цикл_). Его индекс 11, а значение 7.
3. Берем из сид фразы слово стоящее под номер 11 и добавляем (_insert_) его в список с индексом 7.
4. Список увеличивается на одно слово, а старые индексы смещаются.
5. Повторяем с предыдущим символом из ключа (10,1) и увеличенным списком.
6. Таким образом, полученный список увеличится на 12 слов.
7. Преобразуем список в строку и полученный набор слов можно распечать, сохранить на компьютере и т.д.

   
Для генерации начального списка слов, обязательно рекомендую использовать библиотеку bip39gen (_Python_).
<https://github.com/massmux/bip39gen>

#### Итоговый туман, после 12 проходов
`
['reptile', 'collection', 'clash', 'haunt', 'soprano', 'word', 'reputation', 'chance', 'wood', 'reptile', 'professional', 'flesh', 'desire', 'tumble', 'dominate', 'tumble', 'organisation', 'reputation', 'glove', 'ready', 'combination', 'occupation', 'hostility', 'haunt', 'desire', 'combine', 'rebellion', 'flesh', 'galaxy', 'nuclear', 'improvement', 'reporter', 'integrated', 'charm', 'plug', 'talk', 'disaster', 'familiar', 'branch', 'provincial', 'manner', 'overwhelm', 'collection', 'glove', 'porter', 'senior', 'wood', 'morning', 'bench', 'clash', 'connection', 'clothes', 'word', 'dealer', 'kinship', 'contain', 'mayor', 'double', 'soprano', 'reptile', 'chance', 'professional', 'dominate', 'ostracize', 'announcement', 'tumble', 'organisation', 'trial', 'reputation', 'ready', 'combination', 'occupation', 'hostility', 'haunt', 'desire', 'combine', 'rebellion', 'flesh', 'galaxy', 'nuclear', 'improvement', 'reporter', 'integrated', 'charm', 'plug', 'talk', 'disaster', 'familiar', 'branch', 'provincial', 'manner', 'overwhelm', 'collection', 'glove', 'porter', 'senior', 'wood', 'morning', 'bench', 'clash', 'connection', 'clothes']
`

#### Восстановление сид фразы из тумана достаточно просто выполнить без компьютера
Теперь цикл уже прямой.
1. Создаем пустой список для записи слов из тумана.
2. Преобразуем строку тумана в список (_для Python_)
3. Берем нулевой индекс ключа. Это 1.
4. Добавляем слово из туманного списка с индексом 1 всписок для слов. Это первое слово из сид фразы.
5. Из туманного списка удаляется элемент с индексом 1. Список укорачивается.
6. Шаги 3-5 повторяются до перебора всей длины ключа.

