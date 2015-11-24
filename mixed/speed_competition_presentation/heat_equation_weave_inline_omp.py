import numpy as np
from scipy import weave

def solve(t0, t1, dt, n, m, u_initial, f, nu, verbose=False):
    """
    Function which, using weave.inline, solves the heat equation for a substance 
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
    code = r"""
    double *temp, *u_init = u;          /*set a pointer to u for later use*/
    int th_id, nthreads;
    int i, j, it, m_start, m_end;
    #pragma omp parallel private(th_id, nthreads, it, i, j, m_start, m_end)
    {
        th_id = omp_get_thread_num();
        nthreads = omp_get_num_threads();
        m_start = (m-2)*th_id/nthreads + 1;
        m_end = (m-2)*(th_id+1)/nthreads + 1;
        /*printf("Thread #%d/%d starting: [%d, %d)\n", th_id+1, nthreads, m_start, m_end);*/

        for (it = 1; it < Nt+1; it++) {
            for (i=m_start; i < m_end; i++) {
                for (j=1; j < n-1; j++) {
                    u_new[i*n + j] = u[i*n + j] + dt*(nu*(u[(i-1)*n + j] 
                                   + u[i*n + j-1] - 4*u[i*n + j] + u[i*n + j+1] 
                                   + u[(i+1)*n + j]) + f[i*n + j]);
                }
            }

            #pragma omp barrier
            /*swap pointers*/
            if (th_id == 0) {
                temp = u;
                u = u_new;
                u_new = temp;

                if (verbosity && it % (Nt/100) == 0) {  /*update progress 100 times*/
                    /*use stderr since it's unbuffered*/
                    fprintf(stderr, "\rt = %6.0f (%3.0f%%)", t0 + it*dt, it*1E2/Nt);
                }
            }
            #pragma omp barrier
        }
    }

    if (verbosity) {    /*print newline*/
        printf("\n");
    }

    /*since we're writing back and forth between two arrays, u and u_new,
    and we want the results in u regardless of the number of time steps,
    if u doesn't point to the same location in memory as u_res, 
    then we must copy the contents of back u_new to u_res */
    if (u_init != u) {  /*u_init points to the original u*/
        if (verbosity) {
            printf("Copying back to correct array\n");
        }
        memcpy(u_init, u, sizeof(double)*m*n);
    }
    """
    runtime = 0.
    verbosity = 1 if verbose else 0
    weave.inline(code, 
                 arg_names=['u', 'u_new', 'f', 'nu', 'm', 'n',
                            'dt', 'Nt', 't0', 't1', 'verbosity', 'runtime'],
                 headers=['<math.h>',   #for round 
                          '<stdio.h>',  #for printing
                          '<string.h>', #for memcpy
                          '<omp.h>'],   #for OpenMP
                 extra_compile_args=['-O3',             #optimize loops
                                     '-w',              #surpress warnings
                                     '-fopenmp',        #enable OpenMP
                                     '-march=native'    #optimize for processor
                                    ],
                libraries=['gomp']
                )
    return u, t

if __name__ == '__main__':
    t0 = 0      #start time
    t1 = 1000   #end time
    dt = 0.1    #size of time step
    n = 50      #spatial resolution in y-dimension (x-dimension in plot)
    m = 100     #spatial resolution in x-dimension (y-dimension in plot)
    nu = 1      #constant determining the rate the heat spreads at

    dim = (m, n)
    f = np.ones(dim)                #source term
    u_initial = np.zeros(dim)       #initial condition

    import time
    pre = time.time()
    u, t = solve(t0, t1, dt, n, m, u_initial, f, nu)
    post = time.time()
    print "u_max = %.15E   @ t=%g" % (u.max(), t)
    print "The computation took %g s" % (post - pre)

    import matplotlib.pyplot as plt
    plt.imshow(u, cmap = 'gist_gray')
    plt.colorbar()
    plt.savefig("plot_5_2_weave_inline.pdf")
    plt.savefig("plot_5_2_weave_inline.png")
    #plt.show()