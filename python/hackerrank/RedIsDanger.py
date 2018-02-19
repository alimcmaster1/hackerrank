import time
import math
import sys
from functools import lru_cache
import matplotlib.pyplot as plt


class TreePairs():
    def __init__(self, value=None, valueTop=None, valueBottom=None, nodeHeight=0):
        self.value = value
        self.valueTop = valueTop
        self.valueBottom = valueBottom
        self.nodeHeight = nodeHeight


def RedIsDanger(capacity_array):

    def computeCombinations(size):

        count_size = 1
        sys.setrecursionlimit(50000)
        tree_init_pairs = TreePairs("Head Node", TreePairs("G", nodeHeight=1), TreePairs("R", nodeHeight=1))

        @lru_cache(maxsize=10000)
        def recursive_func(count, item, count_size):
            if item.value is None:
                return 0
            elif item.value is "G":
                item.valueTop = TreePairs("G", nodeHeight=item.nodeHeight+1)
                item.valueBottom = TreePairs("R", nodeHeight=item.nodeHeight+1)
            elif item.value is "R":
                item.valueTop = TreePairs("G", nodeHeight=item.nodeHeight+1)
                item.valueBottom = TreePairs()

            if item.nodeHeight == size:
                return count + 1

            return recursive_func(count, item.valueTop, count_size) + recursive_func(count, item.valueBottom, count_size)

        count = recursive_func(0, tree_init_pairs.valueTop, count_size)

        counttwo = recursive_func(0, tree_init_pairs.valueBottom, count_size)

        return count + counttwo

        print(recursive_func.cache_info())

    output = []
    times = []
    for item in capacity_array:
        start = time.process_time()
        output.append(int(math.pow(computeCombinations(item), 2)))
        elapsed_time = time.process_time() - start
        times.append(elapsed_time)

    plt.plot(capacity_array, times)
    plt.ylabel("time (s)")
    plt.xlabel("input")
    plt.title("Red is Danger Binomial Tree")
    plt.grid(True)
    plt.savefig("myplt.png")
    plt.show()
    return output
RedIsDanger(range(2,10,2))