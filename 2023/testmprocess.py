import time

from utils import Utilities


def run_process(name, sleep_time):
    print("Running %s, sleeping %s" % (name, sleep_time))
    time.sleep(sleep_time)
    print("Done process %s" % name)
    return sleep_time


if __name__ == '__main__':
    args = [("A", 2), ("B", 5), ("C", 4), ("D", 8)]
    r = [(run_process, a) for a in args]
    print(r[0][1])
    res = Utilities.run_parallel_processes(r)
    print(res)