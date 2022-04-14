import random

def rand_num_gen(num):
    start = 10**(num-1)
    end = (10**num) - 1
    random__num__1 = random.randint(start, end)
    random__num__2 = random.randint(start, end)
    return str(random__num__2) + str(random__num__1)

