#include <math.h>
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

double solve(double t0, double t1, double dt, int m, int n, double *u_init, 
             double *f, double nu) {
    double *temp;
    double *u = u_init;
    /*double u_other[m*n];*/
    double *u_other = malloc(sizeof(double)*m*n);
    double *u_new = u_other;
    memcpy(u_new, u_init, sizeof(double)*m*n);

    int Nt = (int) round((t1 - t0)/dt);
    double t = t0 + Nt*dt;

    int th_id, nthreads;
    int i, j, it, m_start, m_end;
    #pragma omp parallel private(th_id, nthreads, it, i, j, m_start, m_end)
    {
        th_id = omp_get_thread_num();
        nthreads = omp_get_num_threads();
        m_start = (m-2)*th_id/nthreads + 1;
        m_end = (m-2)*(th_id+1)/nthreads + 1;
        printf("Thread #%d/%d starting: [%d, %d)\n", th_id+1, nthreads, m_start, m_end);
        #pragma omp barrier

        for (it = 0; it < Nt; it++) {
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
            }
            #pragma omp barrier
        }
    }

    /*Since we're writing back and forth between two arrays, u_init and u_other,
    and we want the results in u_init regardless of the number of time steps,
    if u doesn't point to the same location in memory as u_init, 
    then we must copy the contents of back u_new to u_init */
    if (u != u_init) {
        /*printf("Copying back to correct array\n");*/
        memcpy(u_init, u, sizeof(double)*m*n);
    }
    free(u_other);
    return t;
}

int main(int argc, char *argv[]) {
    double pre, post;
    int i, j;

    double t0, t1, dt, nu, u_const, f_const;
    int m, n;
    if (argc == 9) {
        printf("Reading parameters from command line.\n");
        t0 = atof(argv[1]);
        t1 = atof(argv[2]);
        dt = atof(argv[3]);
        n = atoi(argv[4]);
        m = atoi(argv[5]);
        u_const = atof(argv[6]);
        f_const = atof(argv[7]);
        nu = atof(argv[8]);
        printf("Successfully read parameters from command line.\n");
    } else {
        printf("Using default parameters.\n");
        t0 = 0;
        t1 = 1000;
        dt = 0.1;
        n = 50;
        m = 100;
        u_const = 0;
        f_const = 1;
        nu = 1.0;
    }

    /*
    double u[m*n];
    double f[m*n];
    */
    double *u = malloc(sizeof(double)*m*n);
    double *f = malloc(sizeof(double)*m*n);

    for (i = 0; i < m; i++) {
        for (j = 0; j < n; j++) {
            u[i*n + j] = u_const;
            f[i*n + j] = f_const;
        }
    }
    
    pre = omp_get_wtime();
    double t = solve(t0, t1, dt, m, n, u, f, nu);
    post = omp_get_wtime();
    double u_max = 0;
    for (i = 0; i < m; i++) {
        for (j = 0; j < n; j++) {
            if (u[i*n + j] > u_max) u_max = u[i*n + j];
        }
    }
    printf("u_max = %.15E   @ t=%.2f\n", u_max, t);
    printf("The computation took %g s\n", (post - pre));

    /*
    char outfile[] = "C_output_data_omp.txt";
    printf("Writing data to %s\n", outfile);
    FILE *fp;
    fp = fopen(outfile, "w");
    for (i = 0; i < m; i++) {
        for (j = 0; j < n; j++) {
            fprintf(fp, "%.6g\t", u[i*n + j]);
        }
        fprintf(fp, "\n");
    }
    fclose(fp);
    */
    free(u);
    free(f);
    return 0;
}
