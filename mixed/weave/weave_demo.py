import numpy
import weave

a = numpy.zeros((10, 6))

expr = "a[1:3, 2:-1] = 1"
weave.blitz(expr)

print a

