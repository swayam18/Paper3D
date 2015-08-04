from dxfwrite import DXFEngine as dxf
from utilities import *
import copy

# color index
# 0 for black
# 1 for red
# 2 for yellow
# 3 for green
# 5 for blue

class DXFWriter:
  def __init__(self, n, ds,  filename = "test", col1 = 0, col2 = 1, col3 = 1):
    
    self.n = n
    self.ds = ds
    self.drawings = [dxf.drawing(filename + str(i) + ".dxf") for i in range(len(self.ds))]
    self.cutting_color = col1
    self.folding_color1 = col2
    self.folding_color2 = col3
    self.fold_edges = [[] for i in range(len(self.ds))]
    self.cut_edges = [[] for i in range(len(self.ds))]
    self.edge = []

    self.combined_d = {}
    for d in self.ds:
      self.combined_d.update(d)

    self.all_edges = {k: self.combined_d[k].node.edge_to_nodes for k in xrange(n) }
    self.edge_numbering = None


  def generate_from_vertices2(self,i):
    d = self.ds[i]
    all_fold_edges = {i: [None]*3 for i in d}
    all_edges = {k: d[k].node.edge_to_nodes for k in d }
    all_cut_edges = {k: d[k].node.edge_to_nodes for k in d }
    # print "all_edges", all_edges
    print "CUTEDGE", i, all_cut_edges
    
    discovered = set()
    for k in d:
      tn = d[k]
      parent_idx = tn.node.index
      
      for child,edge in tn.children:  # fold edges
        child_idx = child.node.index
        edge_val = (child_idx, parent_idx) if child_idx < parent_idx else (parent_idx, child_idx)

        if edge_val not in discovered:
          if edge_val in all_edges[parent_idx]:
            parent_pos = all_edges[parent_idx].index(edge_val)
            all_fold_edges[parent_idx][parent_pos] = edge_val
            all_cut_edges[parent_idx][parent_pos] = None

          if edge_val in all_edges[child_idx]:
            child_pos = all_edges[child_idx].index(edge_val)
            all_fold_edges[child_idx][child_pos] = edge_val
            all_cut_edges[child_idx][child_pos] = None

          discovered.add(edge_val)


    # print "edge_numbering", edge_numbering
    self.fold_edges[i] = all_fold_edges
    self.cut_edges[i] = all_cut_edges
    
    
    
    
  def draw_lines(self, i):
    drawn = set()
    d = self.ds[i]
    all_fold_edges = self.fold_edges[i]
    all_cut_edges = self.cut_edges[i]
    edge_numbering = self.edge_numbering
    for k in d:
      v1, v2, v3 = d[k].transformed_vertices
      v1 = tuple(v1)
      v2 = tuple(v2)
      v3 = tuple(v3)
      cut_edges = all_cut_edges[k]
      fold_edges = all_fold_edges[k]
      
      for j, edge in enumerate([(v1,v2), (v2,v3), (v3,v1)]) and edge not in drawn:
        if cut_edges[j] != None and edge not in drawn:  
          self.drawings[i].add(dxf.line(edge[0][:2], edge[1][:2], color=self.cutting_color))
          drawn.add(edge)

        elif fold_edges[j] != None and edge not in drawn:
          self.drawings[i].add(dxf.line(edge[0][:2], edge[1][:2], color=self.folding_color1))
          drawn.add(edge)

  def draw_numbers(self, i):
    drawn = set()
    d = self.ds[i]
    all_fold_edges = self.fold_edges[i]
    all_cut_edges = self.cut_edges[i]
    edge_numbering = self.edge_numbering
    for k in d:
      v1, v2, v3 = d[k].transformed_vertices
      v1 = tuple(v1)
      v2 = tuple(v2)
      v3 = tuple(v3)
      cut_edges = all_cut_edges[k]
      fold_edges = all_fold_edges[k]
      
      for j, edge in enumerate([(v1,v2), (v2,v3), (v3,v1)]):
        if edge_numbering[k][j] != None:
          midpoint = ( (edge[0][0] + edge[1][0])/2 , (edge[0][1] + edge[1][1])/2 )
          n = getNormalBetween2DVertices(edge[0],edge[1])
          multiplier = 1.5
          pt = (midpoint[0] - n[0] * multiplier, midpoint[1] - n[1] * multiplier)
          self.drawings[i].add(dxf.text(edge_numbering[k][j], insert=pt))

  def generate_edge_numbering(self):
    edge_numbering = {i: [None]*3 for i in self.combined_d}
    discovered = set()
    k = 0
    for i in range(len(self.ds)):
      for j in self.cut_edges[i]:
        for edge_id, edge_val in enumerate(self.cut_edges[i][j]):
          if edge_val != None and edge_val not in discovered:
            parent_idx, child_idx = edge_val
            parent_pos = self.all_edges[parent_idx].index(edge_val)
            edge_numbering[parent_idx][parent_pos] = k

            child_pos = self.all_edges[child_idx].index(edge_val)
            edge_numbering[child_idx][child_pos] = k
            discovered.add(edge_val)
            k += 1

    self.edge_numbering = edge_numbering

  def generate_file(self):
    for i in range(len(self.ds)):
      self.generate_from_vertices2(i)
      self.draw_lines(i)

    self.generate_edge_numbering()

    for i in range(len(self.drawings)):
      self.draw_numbers(i)
      self.drawings[i].save()


