import numpy
import weave

a = numpy.zeros((10, 6))

# Perform the time step
expr = "a[1:3, 2:-1] = 1"
weave.blitz(expr)

print a

