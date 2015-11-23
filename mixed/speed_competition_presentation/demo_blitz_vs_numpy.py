import numpy as np
from scipy import weave

# 4 point average.
expr = "u[1:-1, 1:-1] = (u[0:-2, 1:-1] + u[2:, 1:-1] + "\
                "u[1:-1,0:-2] + u[1:-1, 2:])*0.25"

u = np.zeros((5, 5)); u[0,:] = 100
exec(expr)
print "NumPy:"; print u; print

u = np.zeros((5, 5)); u[0,:] = 100
weave.blitz(expr)
print "Blitz:"; print u