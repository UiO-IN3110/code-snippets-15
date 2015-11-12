from scipy import weave

code = r"""
i++;
printf("Inside i = %d\n", i);
"""
i = 1
weave.inline(code, arg_names=['i'])
print "Outside i = %d" % i