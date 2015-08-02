from dxfwrite import DXFEngine as dxf
from utilities import *


# color index
# 0 for black
# 1 for red
# 2 for yellow
# 3 for green
# 5 for blue

class DXFWriter:
  def __init__(self, d,  filename = "test.dxf", col1 = 0, col2 = 1, col3 = 1):
    self.drawing = dxf.drawing(filename)
    self.d = d
    self.cutting_color = col1
    self.folding_color1 = col2
    self.folding_color2 = col3
    self.all_edges = set()
    self.fold_edges = set()
    self.cut_edges = []
    self.cut_edge_numbering = []


  def generate_from_vertices2(self):
    all_fold_edges = {i: [None]*3 for i in range(len(self.d))}
    all_edges = {k: self.d[k].node.edge_to_nodes for k in self.d }
    all_cut_edges = {k: self.d[k].node.edge_to_nodes for k in self.d }
    edge_numbering = {i: [None]*3 for i in range(len(self.d))}
    print "all_edges", all_edges
    
    discovered = set()
    for k in self.d:
      tn = self.d[k]
      parent_idx = tn.node.index
      
      for child,edge in tn.children:  # fold edges
        child_idx = child.node.index
        edge_val = (child_idx, parent_idx) if child_idx < parent_idx else (parent_idx, child_idx)

        if edge_val not in discovered:
          parent_pos = all_edges[parent_idx].index(edge_val)
          child_pos = all_edges[child_idx].index(edge_val)

          all_fold_edges[parent_idx][parent_pos] = edge_val
          all_cut_edges[parent_idx][parent_pos] = None

          all_fold_edges[child_idx][child_pos] = edge_val
          all_cut_edges[child_idx][child_pos] = None

          discovered.add(edge_val)
          

    print "all_fold_edges", all_fold_edges
    print "all_cut_edges", all_cut_edges
    i = 0
    discovered = set()
    for j in all_cut_edges:
      for edge_id, edge_val in enumerate(all_cut_edges[j]):
        if edge_val != None and edge_val not in discovered:
          parent_idx, child_idx = edge_val
          parent_pos = all_edges[parent_idx].index(edge_val)
          child_pos = all_edges[child_idx].index(edge_val)
          edge_numbering[parent_idx][parent_pos] = i
          edge_numbering[child_idx][child_pos] = i
          discovered.add(edge_val)
          i += 1


    
    print "edge_numbering", edge_numbering

    # self.all_edges = all_edges
    # self.fold_edges = all_fold_edges
    # self.cut_edges = all_cut_edges
    # self.edge_numbering = edge_numbering


    drawn = set()
    for k in self.d:
      v1, v2, v3 = self.d[k].transformed_vertices
      v1 = tuple(v1)
      v2 = tuple(v2)
      v3 = tuple(v3)
      cut_edges = all_cut_edges[k]
      fold_edges = all_fold_edges[k]
      
      for j, edge in enumerate([(v1,v2), (v2,v3), (v3,v1)]):
        if cut_edges[j] != None and edge not in drawn:  
          self.drawing.add(dxf.line(edge[0][:2], edge[1][:2], color=self.cutting_color))
          drawn.add(edge)

        elif fold_edges[j] != None and edge not in drawn:
          self.drawing.add(dxf.line(edge[0][:2], edge[1][:2], color=self.folding_color1))
          drawn.add(edge)


        if edge_numbering[k][j] != None:
          midpoint = ( (edge[0][0] + edge[1][0])/2 , (edge[0][1] + edge[1][1])/2 )
          n = getNormalBetween2DVertices(edge[0],edge[1])
          multiplier = 1.5
          pt = (midpoint[0] - n[0] * multiplier, midpoint[1] - n[1] * multiplier)
          self.drawing.add(dxf.text(edge_numbering[k][j], insert=pt))
    
    
  def generate_lines(self):
    for cut_edge in self.cut_edges:
      self.drawing.add(dxf.line(cut_edge[0][:2], cut_edge[1][:2], color=self.cutting_color))
    for fold_edge in self.fold_edges:
      self.drawing.add(dxf.line(fold_edge[0][:2], fold_edge[1][:2], color=self.folding_color1))

  def generate_edge_numbering(self):
    pass

  def generate_file(self):
    self.generate_from_vertices2()
    # self.generate_lines()
    self.drawing.save()


