import random
import collections
import matplotlib.pyplot as plt

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

def main():
    random_results = []
    solid_results = []
    for i in range(100000):
        random_results += [list_game(lambda x,_: random.choice(x))]
        solid_results += [list_game(lambda x,y: min(x, key=lambda z:abs((z+0.5)*50-y)))]
    random_counter = collections.Counter(random_results)
    solid_counter = collections.Counter(solid_results)
    print(random_counter, solid_counter, sep ="\n")
    fig, axs = plt.subplots(1, tight_layout=True)
    axs.set_xticks(range(20))
    axs.hist(solid_results, bins = len(solid_counter))
    plt.show()

if __name__ == "__main__":
    main()