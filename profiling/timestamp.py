import time

# Loop version
c1 = time.clock()
s = 0
for i in range(10000):
    s += i
c2 = time.clock()

print c2-c1


# Sum version
c1 = time.clock()
sum(range(10000))
c2 = time.clock()

print c2-c1


