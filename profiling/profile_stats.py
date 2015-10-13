import pstats

p = pstats.Stats("dump.profile")

p.print_stats()

p.sort_stats("time")

p.print_stats(5)
