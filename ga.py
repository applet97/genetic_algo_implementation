import random

population = []
MIN_FITNESS = 2
MIN_POPULATION_SIZE = 10

INITIAL_POPULATION_SIZE = 1000 * 20
CHROMOSOME_SIZE = 40

def calc_fitness(chromosome):
	# fitness equals to number of bits in a chromosome
	fitness = 0
	for i in range(len(chromosome)):
		fitness = fitness + int(chromosome[i])
	return fitness


def get_max(generation_id):
	# we are interested in maximum level of fitness among all chromosomes in the generation
	ans = 0
	for chromosome in population[generation_id]:
		cur = calc_fitness(chromosome)
		if ans < cur:
			ans = cur
	return ans

def converged(generation_id):
	if len(population[generation_id]) <= MIN_POPULATION_SIZE: #if popilation size is extremely small, then it is converged
		return True

	cur = get_max(generation_id)
	cnt = 0
	for i in range(generation_id - 1, 0, -1):
		# if we did not get better result in last 10 generations, then it is converged
		cnt = cnt + 1
		if cnt == 10:
			break
		if get_max(i) < cur:
			return False
	
	return cnt >= 10


def mutate(generation_id):

	for chromosome in population[generation_id]:
		ri = random.randint(0, 1000) # probability of mutation if 0.001
		if ri == 0:
			ri = random.randint(0, len(chromosome) - 1)
			# we flip a random bit of the chromosome
			if chromosome[ri] == 0:
				chromosome[ri] = 1
			else:
				chromosome[ri] = 0


def selection(generation_id):
	selected = []
	unselected = []
	for chromosome in population[generation_id]:
		# we take chromosomes whose fitness is more than MIN_FITNESS

		if calc_fitness(chromosome) >= MIN_FITNESS:
			selected.append(chromosome)
		else:
			unselected.append(chromosome)
	return selected, unselected


def cross(a, b):
	ri = random.randint(0, len(a))
	c = []
	d = []
	# it is single point crossover
	# we separate head and tail of both a and b to get new chromosomes c and d

	for i in range(len(a)):
		if i > ri:
			c.append(a[i])
			d.append(b[i])
		else:
			c.append(b[i])
			d.append(a[i])
	return c, d

	

def crossover(selected):
	random.shuffle(selected)
	for i in range(len(selected)):
		if i % 2 == 1:
			girl, boy = cross(selected[i], selected[i - 1])
			# we replace old chromosomes with new two
			selected[i] = boy
			selected[i - 1] = girl
	return selected


def get_generation(generation_size, chromosome_size):
	generation = []
	# we generate random chromosomes of same length
	for i in range(generation_size):
		chromosome = []
		for j in range(chromosome_size):
			chromosome.append(random.randint(0, 1))
		generation.append(chromosome)

	return generation


def evolution(population):
	generation_id = 0

	# we start with random population

	initial_generation = get_generation(INITIAL_POPULATION_SIZE, CHROMOSOME_SIZE)
	population.append(initial_generation)

	# we store answer in maximum fitness
	max_fitness = get_max(generation_id)
	last_fitness = max_fitness

	while(True):

		print "Fitness: {}".format(last_fitness)

		if converged(generation_id):
			break

		# only selected chromosomes can be involved in crossover operation

		selected, unselected = selection(generation_id)
		selected = crossover(selected)
		population.append(selected)
		generation_id = generation_id + 1
		mutate(generation_id)
		cur_fitness = get_max(generation_id)
		last_fitness = cur_fitness
		
		if max_fitness < cur_fitness:
			max_fitness = cur_fitness


	return max_fitness

answer = evolution(population)

print "\nMaximum reached fitness: {}".format(answer)

