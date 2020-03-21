# EvoGuess

## Подготовка
Установка пакетов
```
pip3 install numpy
pip3 install pebble
pip3 install python-sat
pip3 install mpi4py (для MPI)
```

## Запуск
```
python3 main.py <instance> <function>
```

## MPI Запуск
```
mpiexec -n node_count python3 mpi_main.py <instance> <function>
```

## Обязательные Аргументы
* **instance**
    - *e0* – E0
    - *a5* – A5/1
    - *asg72* – ASG 72/76
    - *asg96* – ASG 96/112
    - *asg192* – ASG 192/200
    - *gr0* – Grain v0
    - *gr1* – Grain v1
    - *tr* – Trivium
    - *biv* – Bivium
    - *tr64* – Trivium 64/75
    - *tr96* – Trivium 96/100
    - *pr5_2* – Present 5/2KP
    - *pr6_1* – Present 6/1KP
    - *pr6_2* – Present 6/2KP
    - *bvi:n_k* – BubbleVsInsert (**только gad**) (аргументы: n чисел по k бит)
    - *bvs:n_k* – BubbleVsSelection (**только gad**) (аргументы: n чисел по k бит)
    - *md4:n_k* – MD4 (аргументы: n шагов, k бит)

* **function** – Оценочная функциия
    - *gad* – Guess-and-Determine
    - *ibs* – Inverse Backdoor Sets
    
## Необязательные Аргументы
* -t – Кол-во потоков (по-умолчанию: 1)
* -d – Описание для запуска (запишется в отдельный файл)
* -wt – Ограничение времени поиска: hh:mm:ss (по-умолчанию: 24:00:00)
* -v – Verbosity для debug [0-3] (по-умолчанию: 3)
* -i – Использовать инкрементальность при решении (по-умолчанию: нет)
* -dall – Отладка для всех нод (по-умолчанию: нет)

* -n – выборка для метода Монте-Карло (по-умолчанию: 1000)
* -tl – Ограничение времен на подзадачу (**только ibs**, по-умолчанию: 5 сек)
* -s – SAT-solver для решения, см. **Solvers** (по-умолчанию: g3)
* -pr - SAT-solver для Unit Propagation, см. **Solvers** (по-умолчанию: = -s)

* -a – Алгоритм для оптимизации, см. **Алгоритмы** (по-умолчанию: 1+1)
* -st – Стагнаций до рестарта (по-умолчанию: 300)

## Solvers (python-sat library)
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

## Алгоритмы
* *m+l* – Эволюционная стратегия (m + l)
* *m,l* – Эволюционная стратегия (m, l)
* *m^l* – Генетический алгоритм: Элитизм (m элит из l особей)

## Примеры
Поиск с использованием эволюционной стратегии (1+2) на 36 потоках функцией Guess-and-Determine, SAT-solver Glucose 3, выборка для метода Монте-Карло 500,
```shell script
python3 main.py bvs:7_4 gad -t 36 -wt 12:00:00 -d "bvs 7x4 run" -v 3 -n 500 -s g3 -a 1+2
```