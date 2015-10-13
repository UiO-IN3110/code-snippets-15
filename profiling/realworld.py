from dolfin import *
import cProfile


def main():

    mesh = UnitSquareMesh(100, 100)

    V = FunctionSpace(mesh, "CG", 2)

    class SinExpr(Expression):
        def eval(self, value, x):
            value[0] = sin(x[0])
    expr = SinExpr()

    #expr = Expression("sin(x[0])")

    interpolate(expr, V)


if __name__=="__main__":
    prof = cProfile.Profile()
    prof.runcall(main)
    prof.dump_stats("realworld.profile")

