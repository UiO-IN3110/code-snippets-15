import time
import cProfile


def delay1():
    time.sleep(1)

def delay2():
    time.sleep(2)

def delay3():
    time.sleep(3)


def main():
    delay1()
    delay2()
    delay3()


if __name__ == "__main__":

    #cProfile.run("main()")

    prof = cProfile.Profile()
    prof.runcall(main)
    prof.dump_stats("dump.profile")
