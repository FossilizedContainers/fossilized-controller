from math import *

n = 1
# times = [1000000, 60000000, 3600000000, 86400000000, 2628000000000, 31540000000000, 3154000000000000]
times = [1000000, 60000000]

for t in times:
    while n * log(n, 2) < t:
        n += 1

print("n :", n - 1)
