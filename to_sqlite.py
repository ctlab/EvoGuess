import re
import sqlite3

from os import listdir
from os.path import join

path = "output/_main_logs/sgen/6_900_100/2020.10.10_20:34:59-2020.10.11_08:35:01"

db_path = join(path, 'backdoors.db')
connection = sqlite3.connect(db_path)

cursor = connection.cursor()
cursor.execute('''create table backdoors (backdoor text, payload text)''')

# 1.95 гб
bd_dir = join(path, 'backdoors')
for bd in listdir(bd_dir):
    with open(join(bd_dir, bd), 'r') as f:
        lines = f.readlines()
        bd_key = lines[0][:-1].split(': ')[1]
        count = int(lines[1].split('(')[1].split(')')[0])

        cases = []
        for i in range(count):
            cases.append(lines[2 + i])

        time = float(lines[count + 2].split(': ')[1])
        value = float(lines[count + 3].split(': ')[1])

        print(bd_key, count, time, value)
        cases = [(bd_key, case, time, value) for case in cases]
        cursor.executemany('''insert into backdoors values (?, ?)''', cases)
        connection.commit()
