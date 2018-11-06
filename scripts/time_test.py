import numpy as np
import time

def foo1(a, b):
    return np.array(a)/b

def foo2(a, b):
    return np.true_divide(a, b)

time_start = int(round(time.time() * 1000))

a = np.random.rand(1000)
b = 2.4
for i in range(100000):
    foo2(a, b)

finishTime = int(round(time.time() * 1000))-time_start  # millsec
print('%i ms | %s' % (finishTime, time.strftime("%H:%M:%S", time.gmtime(int(finishTime/1000)))))
