import numpy as np
from timeit import Timer
import math

def timer(*funcs):
    # find the maximum function name length
    if len(funcs) > 1:
        maxlen = max(*[len(func) for func in funcs])
    elif len(funcs) == 1:
        maxlen = len(funcs[0])
    else:
        return

    # run each function 10000 times and print statistics
    times = []
    print "--"
    for func in funcs:
        timerfunc = Timer("%s()" % func, "from __main__ import %s" % func)
        runtime = timerfunc.repeat(repeat=10000, number=1)
        mtime = np.mean(runtime)
        stime = np.std(runtime)
        dfunc = func + (" " * (maxlen - len(func) + 1))
        print "%s: %.6f +/- %.6f seconds" % (dfunc, mtime, stime)

def numpy_arange():
    l = np.arange(1000)
def py_range():
    l = range(1000)
def py_xrange():
    l = list(xrange(1000))
def main():
    timer("numpy_arange","py_range","py_xrange")


if __name__ == "__main__":
    main()

