##Opening remarks
Some of these implementations don't qualify for the competition as they don't include any Python code, but I left them in for comparison. This applies to

  - pure C (`diffusion.c`)
  - OpenMP (`diffusion_omp.c`)
  - OpenMP alt. (`diffusion_omp_alt.c`)

##How to run the benchmark
```
python run_benchmark.py
```

##Results

|implementation            |  abs. time  | rel. time|
|--------------------------|-------------|----------|
|weave blitz               |      1.297  |      5.11|
|weave inline              |      1.787  |      7.04|
|weave inline OpenMP       |      0.795  |      3.13|
|weave inline OpenMP alt.  |      0.764  |      3.01|
|pure C                    |      0.871  |      3.43|
|OpenMP                    |      0.263  |      1.04|
|OpenMP alt.               |      0.254  |      1.00|

##System
These tests were run on a system with a Intel Core i7 2600K processor running at 4.5 GHz and 4 DIMMs of 4 GB Kingston DDR3 ValueRAM running at 1333 MHz.
