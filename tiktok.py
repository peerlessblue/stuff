import random
import time
import collections
import matplotlib.pyplot as plt
import multiprocessing

def adj_min(arg):
    arg = [x for x in arg if x is not None]
    if arg:
        return min(arg)
    else:
        return 1000
        
def adj_max(arg):
    arg = [x for x in arg if x is not None]
    if arg:
        return max(arg)
    else:
        return -1

def list_game(choice_function):
    # create an empty list of length 20
    lst = [None] * 20
    count = 0
    
    while True:
        # generate a random integer between 1 and 999
        num = random.randint(1, 999)
        
        # find an empty index where the number can be inserted
        empty_indices = [i for i, x in enumerate(lst) if x is None]
        valid_indices = [i for i in empty_indices if (i == 0 or adj_max(lst[:i]) <= num) and (adj_min(lst[i:]) >= num or i == len(lst)-1)]
        if not valid_indices:
            break
        
        # choose a random index from the valid indices and insert the number
        index = choice_function(valid_indices, num)
        lst[index] = num
        count += 1
        
    return count

def fools_game(*_):
    return list_game(lambda x,_: random.choice(x))

def smart_game(*_):
    return list_game(lambda x,y: min(x, key=lambda z:abs((z+0.5)*50-y)))

def main():
    random_results = []
    solid_results = []
    trials = 100000

    #run trials for both options, time results
    start_t = time.perf_counter()
    with multiprocessing.Pool() as pool:
        random_results = tuple(pool.imap_unordered(fools_game, range(trials),chunksize=trials//multiprocessing.cpu_count()))
        solid_results = tuple(pool.imap_unordered(smart_game, range(trials),chunksize=trials//multiprocessing.cpu_count()))
    end_t = time.perf_counter()
    print(f"{trials} trials done in {((end_t-start_t)*1000000/trials):.2f} ns per iteration")

    #collect results into dicts for analysis
    random_counter = collections.Counter(random_results)
    solid_counter = collections.Counter(solid_results)
    print(random_counter, solid_counter, sep ="\n")

    #plot results using matplotlib
    fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)
    for ax in axs: ax.set_xticks(range(20))
    axs[0].hist(random_results, bins = len(random_counter))
    axs[1].hist(solid_results, bins = len(solid_counter))
    plt.show()

if __name__ == "__main__":
    main()

# initial:  100000 trials done in 211.39 ns per iteration
# mp:       100000 trials done in 160.98 ns per iteration
# mp tuple: 100000 trials done in 139.34 ns per iteration
# mp chunk: 100000 trials done in  52.62 ns per iteration