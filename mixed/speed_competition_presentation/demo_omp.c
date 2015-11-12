#include <omp.h>
#include <stdio.h>

int main() {
    int th_id, nthreads;
    #pragma omp parallel private(th_id, nthreads)
    {
        th_id = omp_get_thread_num();
        nthreads = omp_get_num_threads();
        printf("Thread #%d/%d says: Hello, world!\n", th_id + 1, nthreads);
    }
    return 0;
}