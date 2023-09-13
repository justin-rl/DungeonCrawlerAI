import math
import time
from matplotlib import pyplot as plt
import numpy as np

from Constants import NUM_ATTRIBUTES, MAX_ATTRIBUTE


POPULATION_SIZE = 1200
MUTATION_RATE = 0.08
ELITISM = 0.03
NUM_GENERATION = 100


class BabyPlayer:
    def __init__(self, attributes):
        self.attributes = attributes


class Population:
    population = None
    fitness_function = None
    population_fitness = None

    def __init__(self, fitness_function) -> None:
        self.population = np.random.random_integers(
            size=(POPULATION_SIZE, NUM_ATTRIBUTES),
            low=-MAX_ATTRIBUTE,
            high=MAX_ATTRIBUTE,
        )
        self.fitness_function = fitness_function

    def artificial_selection(self, plot=False):
        max_fitnesses = np.zeros(NUM_GENERATION)
        mean_fitnesses = np.zeros(NUM_GENERATION)
        nb_elites = math.ceil(POPULATION_SIZE * ELITISM)
        nb_bebe = POPULATION_SIZE - nb_elites

        for i in range(0, NUM_GENERATION):
            self.evaluate_fitness()
            max = np.max(self.population_fitness)
            max_fitnesses[i] = max
            mean_fitnesses[i] = np.mean(self.population_fitness)

            if max >= 10:
                break

            elites = self.find_elites(nb_elites)
            bebes = self.reproduce(nb_bebe, n_generation=i)
            self.population[:nb_elites][:] = elites
            self.population[nb_elites:][:] = bebes

        if plot:
            plt.figure("Artificial Selection")
            plt.plot(max_fitnesses)
            plt.plot(mean_fitnesses)
            plt.show()

        return self.find_elites(1)[0]

    def evaluate_fitness(self):
        self.population_fitness = list(
            map(self.fitness_function, map(BabyPlayer, self.population))
        )

    def find_elites(self, nb_elite):
        elites = np.argsort(self.population_fitness)[::-1]
        elites = np.array(list(map(lambda i: self.population[i], elites[:nb_elite])))
        return elites

    def reproduce(self, nb_bebe, n_generation):
        normalize_fit = (self.population_fitness - np.min(self.population_fitness)) / (
            np.max(self.population_fitness) - np.min(self.population_fitness)
        )
        percentage_fit = normalize_fit / np.sum(normalize_fit)
        next_gen = np.zeros((nb_bebe, NUM_ATTRIBUTES))
        parents_indices = np.random.choice(
            POPULATION_SIZE, size=(nb_bebe, 2), p=percentage_fit
        )
        for i, parents_idx in enumerate(parents_indices):
            papa = self.population[parents_idx[0]]
            maman = self.population[parents_idx[1]]
            bebe = maman
            split = np.random.randint(low=1, high=NUM_ATTRIBUTES - 1) 
            bebe[split:] = papa[split:]
            next_gen[i][:] = Population._mutate_bebe(bebe, multiply_factor=10 if n_generation < 20 else 5 if n_generation < 40 else 1)
        return next_gen

    def _mutate_bebe(bebe, multiply_factor=1):
        if np.random.randint(low=0, high=100) < MUTATION_RATE * multiply_factor * 100:
            idx = np.random.randint(0, NUM_ATTRIBUTES - 1)
            gene = int(bebe[idx])
            new_gene = None
            while new_gene is None:
                bit = np.random.randint(low=0, high=11)
                if bit == 11:
                    new_gene *= -1
                else:
                    t_gene = gene ^ (1 << bit)
                    if -MAX_ATTRIBUTE <= t_gene <= MAX_ATTRIBUTE:
                        new_gene = t_gene
            bebe[idx] = new_gene
        return bebe
