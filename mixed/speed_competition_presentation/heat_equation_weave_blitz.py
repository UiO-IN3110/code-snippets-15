import numpy as np
import sys
from scipy import weave

def solve(t0, t1, dt, n, m, u_initial, f, nu, verbose=False):
    """
    Function which, using weave.blitz, solves the heat equation for a substance 
    with a specific viscosity across a 2D domain with a time-independent heat 
    source and the boundary condition u=0 at all boundaries.

    Parameters
    ----------
    t0 : float
        Start time for simulation.
    t1 : float
        End time for simulation. (If t1-t0 isn't a multiple of dt, 
        the end time is set to t0 + the nearest multiple of dt)
    dt : float
        The size of the time step
    n : int
        The spatial resolution in the y-dimension (x-dimension in plot)
    m : int
        The spatial resolution in the x-dimension (y-dimension in plot)
    u_initial : 2D-array
        The initial temperature distribution of the domain
    f : 2D-array
        The time-independent heat source
    nu : float
        The viscosity ("floatiness") of the substance, which determines 
        how fast heat spreads in the system.

    Returns
    -------
    u : 2D-array
        The temperature distribution of the domain at the end time.
    t : float
        The end time of the simulation. (If t1-t0 isn't a multiple of dt, 
        this is set to t0 + the nearest multiple of dt)
    """
    u = u_initial
    u_new = u_initial.copy()    
    Nt = int(round((t1 - t0) / float(dt)))      #number of time points
    t = t0 + Nt*dt                              #end time
    for it in xrange(1, Nt+1):
        formula="u_new[1:m-1,1:n-1] = u[1:m-1,1:n-1] + dt*(nu*(u[0:m-2,1:n-1]" \
                                    "+ u[1:m-1,0:n-2] - 4*u[1:m-1,1:n-1]" \
                                    "+ u[1:m-1,2:n] + u[2:m,1:n-1])" \
                                    "+ f[1:m-1,1:n-1])"
        weave.blitz(formula, 
                    check_size=0,    #improves speed significantly
                    extra_compile_args=['-O3',             #optimize loops
                                        '-w',              #surpress warnings
                                        '-march=native'    #optimize for processor
                                       ]
                    )

        #swap pointers
        u_new, u = u, u_new
        if verbose and it % (Nt/100) == 0: 
            sys.stdout.write("\rt = %6.0f (%3.0f%%)" % (t0 + it*dt, it*1E2/Nt))
            sys.stdout.flush()
    if verbose:
        print
    return u, t

if __name__ == '__main__':
    t0 = 0      #start time
    t1 = 1000   #end time
    dt = 0.1    #time step
    n = 50      #spatial resolution in y-dimension (x-dimension in plot)
    m = 100     #spatial resolution in x-dimension (y-dimension in plot)
    nu = 1      #constant determining the rate the heat spreads at

    dim = (m, n)
    f = np.ones(dim)                #source term
    u_initial = np.zeros(dim)       #initial condition

    import time
    pre = time.clock()
    u, t = solve(t0, t1, dt, n, m, u_initial, f, nu)
    post = time.clock()
    print "u_max = %.15E   @ t=%g" % (u.max(), t)
    print "The computation took %g s" % (post - pre)

    import matplotlib.pyplot as plt
    plt.imshow(u, cmap = 'gist_gray')
    plt.colorbar()
    plt.savefig("plot_5_2_weave_blitz.pdf")
    plt.savefig("plot_5_2_weave_blitz.png")
    #plt.show()