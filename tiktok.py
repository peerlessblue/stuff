import random
import time
import collections
import matplotlib.pyplot as plt
import multiprocessing

def get_range(lst,num):
	for sub in lst:
		if sub[0] <= num <= sub[1]:
			return sub[2]
	return []

def insert_range(lst,num,index):
	i = 0
	while index > lst[i][2][-1]:
		i += 1
	if len(lst[i][2]) == 1:
		lst.pop(i)
	elif index == lst[i][2][0]:
		lst[i] = [num,lst[i][1],range(index+1,lst[i][2][-1]+1)]
	elif index == lst[i][2][-1]:
		lst[i] = [lst[i][0],num,range(lst[i][2][0],index)]
	else:
		lst.insert(i,[lst[i][0],num,range(lst[i][2][0],index)])
		lst[i+1] = [num,lst[i+1][1],range(index+1,lst[i+1][2][-1]+1)]

def list_game(choice_function):
	# create an empty list of length 20
	list_size = 20
	count = 0
	indices = [[0,1000,range(list_size)]]
	valid_indices = indices[0][2]
	num = random.randint(1, 999)
	while valid_indices:
		# choose an index from the valid indices and insert the number
		index = choice_function(valid_indices, num)
		insert_range(indices,num,index)
		count += 1

		# generate a new random integer between 1 and 999
		num = random.randint(1, 999)

		# find an empty index where the number can be inserted
		valid_indices = get_range(indices,num)

	return count

def fools_game(*_):
	return list_game(lambda x,_: random.choice(x))

def smart_game(*_):
	return list_game(lambda x,y: min(x, key=lambda z:abs((z+0.5)*50-y)))

def main():
	random_results = []
	solid_results = []
	trials = 100000
	multipro = True

	#run trials for both options, time results
	start_t = time.perf_counter()
	if multipro:
		with multiprocessing.Pool() as pool:
			random_results = tuple(pool.imap_unordered(fools_game, range(trials),chunksize=trials//multiprocessing.cpu_count()))
			solid_results = tuple(pool.imap_unordered(smart_game, range(trials),chunksize=trials//multiprocessing.cpu_count()))
	else:
		for i in range(trials):
			random_results += [fools_game()]
			solid_results += [smart_game()]
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
# mp chunk: 100000 trials done in 52.62 ns per iteration
# rm comp:  100000 trials done in 45.21 ns per iteration
# new adj:  100000 trials done in 33.08 ns per iteration
# rewrite:	100000 trials done in 28.97 ns per iteration
# w/ multi: 100000 trials done in 17.82 ns per iteration