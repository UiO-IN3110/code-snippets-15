CC=gcc

all: C OMP OMP_ALT
C:
	$(CC) diffusion.c -o diffusion.o -lm -O3 -march=native
OMP:
	$(CC) diffusion_omp.c -o diffusion_omp.o -lm -O3 -fopenmp -march=native
OMP_ALT:
	$(CC) diffusion_omp_alt.c -o diffusion_omp_alt.o -lm -O3 -fopenmp -march=native
clean:
	rm diffusion.o diffusion_omp.o diffusion_omp_alt.o
