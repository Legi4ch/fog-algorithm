# fog-algorithm

### Туман - стеганографический алгоритм для хранения сид фраз в незащищенных местах, таких как: Гугл и прочие диски, почта, распечатки на бумаге и т.д.

> Приведенный ниже способ не является алгоритмом шифрования в полном смысле термина.
> Алгоритм меняет порядок слов в сид фразе и скрывает исходные слова в массиве других слов используемых для формирования сид фраз. Отсюда и название алгоритма - Туман.


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


Теперь у нас есть сдвиг для каждого слова из сид фразы. Обратите внимание, что в 11 индексе установлено сдвиг 22. В расчете он получается равным 21,
но 21 уже есть в индексе 3. Поэтому для индекса 11 полученный результат был увеличен на единицу? чтобы стать уникальным для данного набора сдвигов.

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

__Обратите внимание, что используемый для получения этого тумана пин-код: 1 2 3 4 5 - очень простой!__

#### Пример тумана с использованием пин-кода 10 67 13 43 99 181. Тут уже 1039 слов! Всегда используйте сложные пин-коды!

`
random sail toddler goddess dirt cute velvet agent region acid solution exit satoshi honey system endorse picture hamster differ borrow wasp nasty price cargo cool slender fitness zero gaze shaft caution fence clerk unlock more visa swear jaguar century autumn draw milk bind inner sea matrix buzz dad sketch advance current prosper lobster safe amazing achieve nasty wave pilot super please win struggle catch proof panel domain globe danger evoke library access immense girl best until glance drip dignity price exclude 2 goose young 4 call word useless pumpkin grant exile short mango gasp normal hip frozen bonus cute young include forum dress enhance repeat 1 7 rude toward spray unfold roof erase three diet minimum leg choose room tell story fall later feed outside wealth olympic true into where job peasant shell 10 license carpet parrot blade illness neutral anger castle follow ordinary impact coyote catalog clown essay million result notable shift hill reform 8 steak canoe anchor say labor surround sting execute cricket fee age wire attack 9 supply measure oyster turkey skirt column 3 talk lemon stairs print athlete usage tuition cotton blur guitar hip lady boat merry release catalog point unfair vault subway envelope foam pause invest awful renew length capable junk chase ten bleak warm degree satisfy cliff seek awful type able voice beyond oyster over extra lobster movie emerge grace stem actual cube cube tattoo crater front include junior program jazz strong tortoise salmon bicycle about width captain image wrap shrug 6 scrub wealth grocery acquire menu renew cabbage rookie argue latin exhibit special predict kingdom turn cross news rapid rebuild van never real eternal nurse fade source elephant process swarm rail horror sadness oval actress deal congress ketchup accuse double dinosaur purpose fabric once lottery rebuild measure 12 tooth exhibit humble now oil brand beyond inside logic pause heart lake ask scout later one broken urge elder middle lunar fiscal afraid shuffle mean region extra blush history rotate stereo liar frame case wink fee fit rough clarify leaf stem axis first able train clever danger nasty ignore kit tool already awkward gravity pistol script task radar piano woman trust luggage mango steel degree fatigue version tent story fever gaze venue heavy home sudden surface board midnight palace group shadow unfold velvet absurd civil frequent moon bubble always cover cruise venue claim health stadium speak clump sign security midnight dice suspect fever strategy genuine right pepper exchange correct nurse auction noble permit vacant plate between beef other glance junior infant december wish impulse uncover era become follow vintage hobby measure flip symptom monitor shrimp junior agent sad siren bullet camera treat patch property brand pledge trend bless trouble into hint thing hard situate glow goose also group topple fade coconut august route valve warm gym pet smoke silk plate flip consider pen expand neck stamp course youth actual fish boss spray almost raw lottery sing spirit build arch strike deny still waste tent gown coil soul radio drip certain prefer cloud among monster puzzle cloud pet provide exchange rifle immune room endless quarter begin turtle apology mask clip screen bullet carbon tip curtain unique nerve pause lawn diary gate acquire witness bomb patrol student arm sad deer moral fragile spirit document rich twice panda attitude popular fold main relief gap pool cricket skirt stem tent device cross fancy jump above empower debris educate enemy repeat dial mutual powder door unique radio boat nominee unfair sphere youth curious quit eagle analyst teach bullet nephew actress color photo surge fault crop rude basic attitude train bacon oblige upper soldier warrior giraffe write soft farm digital visit crime all urban narrow now merit coil tuition analyst joy black panther local turn session grass van total portion agree honey pelican roast morning snack cover clinic van middle hurry spare clay arrive bamboo gasp retire pill assume rate myth soul drill lucky chapter pave energy purchase boss proof already negative member acquire rail warfare monster easily order talent marine twist retire squeeze rally upper armed path turn tourist sand term spare identify forget staff hazard aunt outdoor romance clean marble dignity course winner worry you state amount depart pipe melody elevator chalk school ring amount until bunker snow destroy fossil shadow calm obscure legend midnight girl help fat elegant tennis addict order ride decrease enact gun next spawn absorb huge festival term icon exact farm cradle fox repair describe manual teach cage hurt tiger relax wreck borrow royal pupil foil space scrub yard exclude mixed lend confirm penalty hammer embark camera great type dismiss push rather few purity scare slam laundry meat horse lazy test stuff burden sight waste soft either high cricket dirt another speed spider image horror van orchard hover used goat zero verb feel cream lucky spoon gauge museum miracle project length great seven wasp develop critic title kind field beauty lunch fabric sound amount public pupil public patrol boost consider twice tank retreat addict claim prevent side already color corn another forget oyster cruise adjust also fragile advance check bubble balcony describe casual mammal warrior fire poverty athlete clerk sure wedding attract one pause defense antique basket already north arrow balcony tribe elephant paddle carbon just video hunt ocean admit mention alcohol good upper spell wall bird absurd mesh giggle wagon attitude ignore visual lock pool wall hedgehog clinic quarter clip fresh color embody rebel cabin pen life tattoo anchor vicious upgrade bar say knee wild often error figure price fee obey huge dilemma coffee timber despair detail cable between invest strike sense purpose february barrel host patient attitude note slim margin setup broccoli cattle bless napkin shoe below dwarf dog electric search warrior journey mirror pony middle cook key sign chest assist idle daughter grow science cushion lecture initial lecture happy various sorry kingdom entire twelve forest polar wet error lyrics open dry ankle three hollow action layer usual family bird retire cupboard reject general capable edit monkey supreme bench roast kick hospital worth slogan today replace 5 pair cook text dynamic fame approve risk toddler truck depend 11 pig good fat raven hurry explain want maid sea hungry despair purse pony pizza sausage jar lock proud tell dash quality whale immune express twenty portion speed decade clay group time winner noise include
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


