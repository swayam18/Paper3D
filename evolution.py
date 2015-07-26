from tree import parseArrayIntoTree
import random

class TreeWorld:
  def __init__(self, graph, arrays):
    self.graph = graph
    self.arrays = arrays
    self.mutation_p = 0.1

  def evaluate(self):
    fitness = [0] * len(self.arrays)
    for i,array in enumerate(self.arrays):
       fitness[i] = self.evaluate_array(array)
    return fitness

  # Generates till max fiteness is reached
  def generateFittest(self,maxGenerations=None, numPairs=None):
    best = []
    bestFitness = 0
    if maxGenerations == None:
      maxGenerations = 100

    if numPairs == None:
      numPairs = len(self.arrays)

    for k in xrange(maxGenerations):
      print "Generation: ", k
      print "Evaluating..."
      fitness = self.evaluate()
      print "Best Fitness:", max(fitness)
      for i,array in enumerate(self.arrays):
        if fitness[i] == len(array):
          return array
        if fitness[i] > bestFitness:
          bestFitness = fitness[i]
          best = array
      print "Creating New Generation..."
      self.nextGeneration(fitness,numPairs)
      print
    return best

  # creates the next generation of arrays
  def nextGeneration(self,fitness,numPairs):
    next_arrays = []
    for i in range(numPairs):
      next_arrays+= self.generate(fitness)

    self.arrays = next_arrays

  def generate(self, fitness):
    i = self.selectRandom(fitness)
    fitness = fitness[:]
    fitness[i] = 0 # make it impossible for i to be selected again
    j = self.selectRandom(fitness)
    parent1 = self.arrays[i][:]
    parent2 = self.arrays[j][:]

    (child1, child2) = self.crossOver(parent1,parent2)
    self.mutate(child1)
    self.mutate(child2)
    return [child1, child2]

  def crossOver(self,a, b):
    i = min(a.index(-1), b.index(-1))
    j = max(a.index(-1), b.index(-1))

    c = range(0,i)+range(j+1,len(a))
    k = random.choice(c)
    c = a[:k] + b[k:]
    d = b[:k] + a[k:]
    return c,d

  def mutate(self, a):
    roll = random.random()
    if roll > self.mutation_p:
      return
    i = random.randint(0,len(a)-1)
    if a[i] == -1:
      return
    node = self.graph.nodes[i]
    k = random.choice(list(node.children))
    a[i] = k

  def selectRandom(self,fitness):
    total = sum(fitness)
    number = random.random() * total
    for i,f in enumerate(fitness):
      if number < f:
        return i
      number -= f

  # fitness is the number of non intersecting triangles
  def evaluate_array(self, array):
    # consistency check
    for i,j in enumerate(array):
      # if the triangles aren't neighbours, discard this mutant
      if j != -1:
        node_i = self.graph.nodes[i]
        node_j = self.graph.nodes[j]
        if self.graph.connected(node_i,node_j) == -1:
          return 0
    tn = parseArrayIntoTree(self.graph.nodes, array)
    tn.unfold()
    intersects = tn.checkIntersection()
    return len(array) - len(tn.checkIntersection())
