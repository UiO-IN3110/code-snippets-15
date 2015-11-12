#encoding=utf-8
import numpy as np
from weave import inline
import matplotlib.pylab as mpl

def heat_equation(t0, t1, dt, n, m, u, f, nu):

	# Used as a placeholder
	u_new = np.zeros((n, m))

	code = """

		int stop = t1/dt;

		// Timestep loop
		for(t0; t0 < stop; t0++)
		{
			int i, j;
			for(i = 1; i < n - 1; i++)
			{
				for(j = 1; j < m - 1; j++)
				{
					U_NEW2(i,j) = U2(i, j) + dt*(nu*U2(i-1,j) + nu*U2(i,j-1) - 4*nu*U2(i,j) + nu*U2(i,j+1) + nu*U2(i+1,j) + F2(i,j));
				}
			}

			// Update U2 with the values from this run.
			// This can probably be done with  pointer swap also
			for(i = 1; i < n - 1; i++)
			{
				for(j = 1; j < m - 1; j++)
				{
					U2(i, j) = U_NEW2(i, j);
				}
			}
		}
		"""

	inline(code, ['t0', 't1', 'dt', 'n', 'm', 'u', 'f', 'nu', 'u_new'])
	return u

t0 = 0;
t1 = 1000;
dt = 0.1;
n = 50;
m = 100;
u = np.zeros((n, m), dtype = 'double')
f = np.ones((n, m), dtype = 'double')
nu = 1;

res = heat_equation(t0, t1, dt, n, m, u, f, nu)

img = mpl.imshow(res, cmap=mpl.cm.gray)
mpl.colorbar(img)
mpl.show()