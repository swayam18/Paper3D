from tree import parseArrayIntoTree, parseEdgeArrayIntoTree
import random

class TreeWorld:
  def __init__(self, graph, arrays):
    self.graph = graph
    self.arrays = arrays
    self.mutation_p = 1.0

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

    # (child1, child2) = self.crossOver(parent1,parent2)
    self.mutate(parent1)
    self.mutate(parent2)
    return [parent1, parent2]

  def crossOver(self,a, b):
    i = min(a.index(-1), b.index(-1))
    j = max(a.index(-1), b.index(-1))

    c = range(0,i)+range(j+1,len(a))
    k = random.choice(c)
    c = a[:k] + b[k:]
    d = b[:k] + a[k:]
    return c,d

  def mutate(self, list_of_edges):
    # see if we need to mutate
    roll = random.random()
    if roll > self.mutation_p:
      return list_of_edges
    i = random.randint(0,len(list_of_edges)-1)
    if list_of_edges[i] == -1:
      return list_of_edges
    
    # choose random node, and a random child
    random_node = self.graph.nodes[i]
    j = random.choice(list(random_node.children))
  
    # simple sort of (i,j)
    if i > j:
      temp = j
      j = i
      i = temp

    if (i, j) in list_of_edges:
      return list_of_edges
    else:
      print "Mutating!"
      # remove a random edge that was in the cycle.
      r = random.choice([i,j])

      l = [edge for edge in list_of_edges if (r in edge)]
      rm = random.choice(l)
      list_of_edges.remove(rm)
      # insert in list_of_edges
      list_of_edges.append((i,j))
      print r
      print list_of_edges
    return list_of_edges


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
    tn = parseArrayIntoTree(self.graph.nodes, array)
    tn.unfold()
    intersects = tn.checkIntersection()
    return len(array) - len(tn.checkIntersection())
