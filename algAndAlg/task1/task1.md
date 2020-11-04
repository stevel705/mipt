# Задание 1: параллельное вычисление префиксов «произведения»

## Как мы будем описывать схемы из функциональных элементов

Схема — это ациклический орграф, в котором каждая вершина является либо входом, либо функциональным элементом; некоторые вершины также могут дополнительно быть помечены как выходные. Схему нужно вывести в стандартный поток вывода в виде последовательности строк, каждая из которых имеет либо вид

```
GATE <номер вершины> <AND|OR|NOT> <номера вершин, выходы которых поданы на элемент>
```

или

```
OUTPUT <порядковый номер выхода> <номера вершины граф схемы, с которой снимается выходное значение>
```

Вершины нумеруются, начиная с нулевой. Если схема реализует функцию (или набор функций) от n n n переменных, то вершины с наименьшими n n n номерами считаются входами, и им не должны приписываться функциональные элементы. Номера вершин схемы должны образовывать непрерывный интервал натуральных чисел. Выходы схемы имеют порядковые номера, начинающиеся с нулевого и также образующие непрерывный интервал натуральных чисел.

Пример описания схемы, имеющей два входа и один выход, в котором реализуется операция XOR от двух переменных (функция XOR реализована в вершине с номером 5):


```
GATE 2 AND 0 1
GATE 3 OR 0 1
GATE 4 NOT 2
GATE 5 AND 3 4
OUTPUT 0 5
```

## Описание задания

На лекции для построения схемы логарифмической глубины для сложения чисел в двоичной записи мы использовали схему «параллельный префикс»: быстрое одновременное вычисление всех выражений вида a1∘a2∘⋯∘ak  (k=1,2,…,n)a_1\circ a_2\circ\dots\circ a_k\,\,(k=1,2,\dots,n)a1​∘a2​∘⋯∘ak​(k=1,2,…,n) для бинарной ассоциативной операции ∘\circ∘ и произвольных a1,…,ana_1,\dots,a_na1​,…,an​. Вам предлагается реализовать такую схему, где в качестве ∘\circ∘ выступает дизъюнкция ∨\lor∨. Соответственно, в качестве функциональных элементов допускается использовать только двухвходовую дизъюнкцию (OR). Входы схемы с номерами 0,1,…,n−10,1,\dots,n-10,1,…,n−1 соответствуют значениям a1,…,ana_1,\dots,a_na1​,…,an​, а выходы схемы с номерами 0,1,…,n−10,1,\dots,n-10,1,…,n−1 соответствуют выражениям a1, a1∨a2, a1∨a2∨a3, …a_1,\,a_1\lor a_2,\,a_1\lor a_2\lor a_3,\,\dotsa1​,a1​∨a2​,a1​∨a2​∨a3​,…

## Ограничения на размер и глубину

Глубина схемы (максимум количества функциональных элементов на пути от входной до выходной вершины) должна быть не больше ⌈log⁡2n⌉\lceil\log_2n\rceil⌈log2​n⌉, а число элементов — не должно превосходить размера схемы, разобранной в лекции.

Формат выходных данных такой же, как и в примере выше для XOR. Входные данные — единственное число n, 2≤n≤200n,\,2\le n\le 200n,2≤n≤200.

### Sample Input 1: 
```
2 
```
### Sample Output 1: 
```
GATE 2 OR 0 1
OUTPUT 0 0
OUTPUT 1 2
```

### Sample Input 2: 
```
3
```
### Sample Output 3: 
```
GATE 3 OR 0 1
GATE 4 OR 1 2
GATE 5 OR 0 4
OUTPUT 0 0
OUTPUT 1 3
OUTPUT 2 5
```