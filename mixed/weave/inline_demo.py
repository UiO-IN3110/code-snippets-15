from weave import inline
import numpy as np

"""
Inline Macros
=============
When passing an array to ``inline`` they can be accessed using hefty pointer
arithmetic, or you can leave the pointer arithmetic to the macro ``inline``
makes.
For an array ``u`` in 2 dimensions ``inline``defines the macro ``U2(i,j)
(*((double*)(u_array->data + (i)*Su[0] + (j)*Su[1])))`` for easy and convenient
access.
"""

arrays = r"""
         printf("[");
          for(int x = 0; x < i; x++) {
            printf("[");
            for(int y = 0; y < j; y++) {
              printf("%d ", ARR2(x, y));
            }
            printf("]");
          }
          printf("]\n");
          """

arr = np.random.rand(3,3)
i, j = arr.shape

inline(arrays, ['i', 'j', 'arr'])
