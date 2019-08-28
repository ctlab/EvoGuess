import sys
import subprocess


def parse_out(out):
    i = 0
    lines = out.split('\n')

    while i < len(lines) and not lines[i].startswith("i CPU time"):
        i += 1
    t = float(lines[i].split(':')[1])
    i += 1

    while i < len(lines) and not lines[i].startswith("i "):
        i += 1
    st = lines[i].split(' ')[1]
    i += 1

    s = ''
    c = ''
    if st == 'SATISFIABLE':
        s = lines[i]
    elif st == 'PRESATELITED':
        while i < len(lines):
            c += lines[i] + '\n'
            i += 1

    return t, st, s, c


if len(sys.argv) < 3:
    print "USAGE: rokk.py <simplify?> <timelimit?> [tl]"
    exit(1)

simplify = sys.argv[1] != '0'
timelimit = sys.argv[2] != '0'

if timelimit and len(sys.argv) < 4:
    raise Exception("timelimit util only work with tl")

tl = None
if len(sys.argv) >= 4:
    tl = int(sys.argv[3])

elite_path = './rokk/binary/SatELite_release'
solver_path = './rokk/binary/rokk_static'


def get_args():
    if timelimit:
        l_args = ["timelimit", "-t%d" % tl, solver_path]
    else:
        l_args = [solver_path]
        if tl is not None:
            l_args.append('-cpu-lim=%d' % tl)

    return l_args


if not simplify:
    p = subprocess.Popen(get_args(), stdin=sys.stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate()
    if len(err) != 0 and not err.startswith("timelimit"):
        raise Exception(err)

    time, status, solution, _ = parse_out(output)
    print "%f\n%s\n%s\n" % (time, status, solution)
    exit(0)

p = subprocess.Popen([elite_path], stdin=sys.stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, err = p.communicate()
if len(err) != 0:
    raise Exception(err)

elite_time, status, solution, cnf = parse_out(output)
if status == 'SATISFIABLE' or status == 'UNSATISFIABLE':
    print "%f p\n%s\n%s\n" % (elite_time, status, solution)
elif cnf != '':
    p = subprocess.Popen(get_args(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate(cnf)
    if len(err) != 0 and not err.startswith("timelimit"):
        raise Exception(err)

    time, status, solution, _ = parse_out(output)
    print "%f\n%s\n%s\n" % (time + elite_time, status, solution)
else:
    raise Exception("cnf not specified")
