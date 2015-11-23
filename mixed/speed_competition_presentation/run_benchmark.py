import numpy as np
import sys, time, re
from subprocess import Popen, PIPE

param_sets = [
#             [0, 10, 0.1, 50, 100, 0, 1, 1.0],
             [0, 1000, 0.1, 50, 100, 0, 1, 1.0],    #5.1
             [0, 5000, 0.1, 100, 200, 0, 1, 1.0]    #speed challenge
             ]
implementations = [
#{'name': 'pure Python',   'dtype':list,         'file': 'heat_equation'},
#{'name': 'NumPy',         'dtype':np.ndarray,   'file': 'heat_equation_numpy'},
{'name': 'weave blitz',   'dtype':np.ndarray,   'file': 'heat_equation_weave_blitz'},
{'name': 'weave inline',  'dtype':np.ndarray,   'file': 'heat_equation_weave_inline'},
{'name': 'weave inline OpenMP',  'dtype':np.ndarray,   'file': 'heat_equation_weave_inline_omp'},
{'name': 'weave inline OpenMP alt.',  'dtype':np.ndarray,   'file': 'heat_equation_weave_inline_omp_alt'},
{'name': 'pure C',          'makeflag': 'C',        'cmd': './diffusion.o'},
{'name': 'OpenMP',          'makeflag': 'OMP',      'cmd': './diffusion_omp.o'},
{'name': 'OpenMP alt.',     'makeflag': 'OMP_ALT',  'cmd': './diffusion_omp_alt.o'}
]
repetitions = 5
perf_data = np.zeros((len(implementations), len(param_sets), repetitions))

for i in xrange(len(implementations)):
    imp = implementations[i]
    print "\nBenchmarking %s" % imp['name']
    if not 'makeflag' in imp:
        import_str = "from %s import solve" % imp['file']
        exec(import_str)
        for j in xrange(len(param_sets)):
            param_set = param_sets[j]
            print "  Running parameter set #%d" % (j+1)
            t0 = param_set[0]
            t1 = param_set[1]
            dt = param_set[2]
            n = param_set[3]
            m = param_set[4]
            u_const = param_set[5]
            f_const = param_set[6]
            nu = param_set[7]

            for rep in xrange(repetitions):
                if imp['dtype'] == list:
                    u = [[u_const for y in xrange(n)] for x in xrange(m)]
                    f = [[f_const for y in xrange(n)] for x in xrange(m)]
                else:
                    u = np.full((m,n), u_const, dtype=np.float64)
                    f = np.full((m,n), f_const, dtype=np.float64)

                pre = time.time()
                solve(t0, t1, dt, n, m, u, f, nu)
                post = time.time()
                perf_data[i, j, rep] = post - pre

    else:
        filename = imp['cmd'][2:].split()[0]
        try:
            f = open(filename, 'r')
            f.close()
        except IOError:
            print "Compiling %s ..." % imp['name']
            args = ['make', imp['makeflag']]
            p = Popen(args)
            p.communicate()

        for j in xrange(len(param_sets)):
            print "  Running parameter set #%d" % (j+1)
            param_set = param_sets[j]
            args = imp['cmd'].split()
            param_set = [str(param) for param in param_set]
            args.extend(param_set)
            
            for rep in xrange(repetitions):
                p = Popen(args, stdout=PIPE)
                output, err = p.communicate()
                match = re.findall("The computation took (\S+)", output)
                time = float(match[0])
                perf_data[i, j, rep] = time

for i in xrange(len(param_sets)):
    print "\nResults for parameter set #%d:" % (i+1), param_sets[i]
    print "%-25s  %10s  %10s" % ("implementation", "abs. time", "rel. time")
    print "-"*49
    for j in xrange(len(implementations)):
        time = perf_data[j,i].min()
        comp = perf_data[:,i].min() #use min value as index point
        print "%-25s  %10.3f  %10.2f" % (implementations[j]['name'], 
                                        time, time/comp)
    print
