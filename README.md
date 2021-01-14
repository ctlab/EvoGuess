# EvoGuess

## Подготовка

Установка пакетов

```
pip3 install numpy
pip3 install pebble
pip3 install python-sat
pip3 install mpi4py (для MPI)
```

## MPI Запуск

```
mpiexec -n node_count python3 -m mpi4py.futures main.py <instance>
```

## Обычный Запуск

```
python3 main2.py <instance>
```

## Обязательные Аргументы

* **instance**
    - *e0* – E0
    - *a5* – A5/1
    - *asg:sk_ks* – ASG (аргументы: sk вх. биты, ks вых. биты)
    - *gr:v* – Grain (аргументы: v версия)
    - *tr* – Trivium
    - *biv* – Bivium
    - *tr64* – Trivium 64/75
    - *tr96* – Trivium 96/100
    - *bvi:n_k* – BubbleVsInsert (**только gad**) (аргументы: n чисел по k бит)
    - *bvp:n_k* – BubbleVsPancake (**только gad**) (аргументы: n чисел по k бит)
    - *bvs:n_k* – BubbleVsSelection (**только gad**) (аргументы: n чисел по k бит)
    - *pvs:n_k* - PancakeVsSelection (**только gad**) (аргументы: n чисел по k бит)
    - *php:p_h* - PHP (**только gad**) (аргументы: p голубей, h клеток)
    - *qap:b* - QAP (**только gad**) (аргументы: b размерность)
    - *sgen:v_n_seed* - SGEN (**только gad**) (аргументы: v версия, n переменных, seed)
    - *domain:b* - Domain (**только gad**) (аргументы: b размерность)
    - *mphp:h_p* - Matrix PHP (**только gad**) (аргументы: h клеток, p голубей)

## Необязательные Аргументы

* -t – Кол-во потоков (**только в main2.py**) (по-умолчанию: 4)
* -v – Verbosity для debug [0-4] (по-умолчанию: 3)
* -o - Директория для логирования (по-умолчанию: main)
* -wt – Ограничение времени поиска: hh:mm:ss (по-умолчанию: 24:00:00)
* -a – Алгоритм для оптимизации, см. **Алгоритмы** (по-умолчанию: 1+1)
* -n - Функция выбора размера выборки, см. **Выборка** (по-умолчанию: 1000)

* -s – SAT-solver для решения, см. **Решатели** (по-умолчанию: g3)
* -m - Основная мера для проведения расчетов, см. **Мера** (по-умолчанию: props)

## Алгоритмы

* *!* – Tabu Search
* *m*+*l* – Эволюционная стратегия (m + l)
* *m*,*l* – Эволюционная стратегия (m, l)
* *m*^*l* – Генетический алгоритм: Элитизм (m элит из l особей)

## Выборка

* *n* – Постоянная выборка из n подзадач
* *mn:mx:step@epsilon*[d*delta*] – Динамическая выборка в зависимости от значения eps (mn минимальное значение, mx максимальное значение, step шаг выборки, epsilon, delta)

## Решатели (python-sat library)

* *cd*  – CaDiCaL (**только gad**)
* *g3*  – Glucose 3.0
* *g4*  – Glucose 4.1
* *lgl* – Lingeling (**только gad**)
* *mcb* – MapleLCMDistChronoBT
* *mcm* – MapleCM
* *mpl* – MapleSat
* *mc*  – Minicard 1.2
* *m22* – Minisat 2.2
* *mgh* – Minisat GitHub version

## Мера

* *time* – Время
* *confs* – Conflicts
* *props* – Propagations

## Примеры

Поиск с использованием эволюционной стратегии (1+2) на 36 потоках функцией Guess-and-Determine, SAT-solver Glucose 3,
выборка 500 подзадач,

```shell script
python3 main2.py bvs:7_4 -t 36 -wt 12:00:00 -v 3 -n 500 -s g3 -a 1+2
```

Поиск в режиме MPI с использованием генетического алгоритма Элитизм(2, 6) функцией Guess-and-Determine, SAT-solver Cadical,
динамическая выборка 100..500 подзадач с шагом 100 подзадач eps = 0.1, delta = 0.08,

```shell script
mpiexec -n node_count python3 -m mpi4py.futures main.py domain:8 -wt 12:00:00 -v 3 -n 100:500:100@0.1d0.08 -s cd -a 2^6
```