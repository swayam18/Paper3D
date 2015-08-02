from utilities import makeUnionFind
from tree import parseArrayIntoTree, parseEdgeArrayIntoTree
from unionfind import UnionFind
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

    (child1, child2) = (self.crossOver(parent1,parent2),self.crossOver(parent1,parent2))
    self.mutate(child1)
    self.mutate(child2)
    return child1, child2

  def crossOver(self,a, b):
    N = len(self.graph.nodes)
    set1 = set(a)
    set2 = set(b)
    child = set.intersection(set1,set2)
    f = set.union(set1,set2) - child
    uf = makeUnionFind(child, N)

    edge_list = list(f)
    random.shuffle(edge_list)
    for edge in edge_list:
        if not uf.connected(edge[0],edge[1]):
            uf.union(edge[0],edge[1])
            child.add(edge)
        if len(child) == N-1: 
            return list(child)

    for i in xrange(N):
        for j in xrange(N):
            if i != j and not uf.connected(i,j) and i in self.graph.nodes[j].children:
                print "added new edge"
                uf.union(i,j)
                child.add((i,j) if i < j else (j,i))
    return list(child)

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
      r = self.dfs_search_for_path(list_of_edges,i,j)
      rm = random.choice(r)
      list_of_edges.remove(rm)
      # insert in list_of_edges
      list_of_edges.append((i,j))
    return list_of_edges

  def paths_intersection(self,array):
    tn = parseEdgeArrayIntoTree(self.graph.nodes, array)
    tn.unfold()
    intersects = tn.checkIntersection()
    p = []
    for i,j in intersects:
      r = self.dfs_search_for_path(array,i,j)
      p.append(tuple(r))
    return p

  def dfs_search_for_path(self,list_of_edges, i,j):
    list_of_edges = list_of_edges[:]
    return self._dfs_with_path(list_of_edges, i, j, [])

  def _dfs_with_path(self, list_of_edges, cur, goal, path):
    children_edges = [edge for edge in list_of_edges if (cur in edge)]
    if len(children_edges) == 0: return None
    for child_edge in children_edges:
      if goal in child_edge:
        return path + [(cur,goal) if cur < goal else (goal,cur)] 
        break
      else:
        next = child_edge[1] if child_edge[0] == cur else child_edge[0]
        list_of_edges.remove(child_edge)
        res = self._dfs_with_path(list_of_edges, next, goal, path + [(cur,next) if cur < next else (next,cur)])
        if res != None:
          return res

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
    tn = parseEdgeArrayIntoTree(self.graph.nodes, array)
    tn.unfold()
    intersects = tn.checkIntersection()
    return len(array) - len(tn.checkIntersection())
