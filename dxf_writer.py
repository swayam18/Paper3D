from dxfwrite import DXFEngine as dxf
from utilities import close_enough


# color index
# 0 for black
# 1 for red
# 2 for yellow
# 3 for green
# 5 for blue

class DXFWriter:
  def __init__(self, vertices, filename = "test.dxf", col1 = 0, col2 = 1, col3 = 1):
    self.drawing = dxf.drawing(filename)
    self.vertices = vertices
    self.cutting_color = col1
    self.folding_color1 = col2
    self.folding_color2 = col3
    self.all_edges = set()
    self.fold_edges = set()
    self.cut_edges = set()

  def generate_from_vertices(self):
    paths = [[x for x in range(y,y+3)] for y in range(0,len(self.vertices),3)]
    for path in paths:
      v1 = tuple(self.vertices[path[0]] + [0])
      v2 = tuple(self.vertices[path[1]] + [0])
      v3 = tuple(self.vertices[path[2]] + [0])
      
      for edge in ((v1,v2), (v2,v3), (v3,v1)):
        connected = False
        for old_edge in self.all_edges:
          if close_enough(edge, old_edge) or close_enough(edge[::-1], old_edge):
            self.fold_edges.add(edge)
            connected = True
            break
          
        if not connected:
          self.all_edges.add(edge)
    
    self.cut_edges = self.all_edges - self.fold_edges
    
    
  def generate_lines(self):
    for cut_edge in self.cut_edges:
      self.drawing.add(dxf.line(cut_edge[0][:2], cut_edge[1][:2], color=self.cutting_color))
    for fold_edge in self.fold_edges:
      self.drawing.add(dxf.line(fold_edge[0][:2], fold_edge[1][:2], color=self.folding_color1))


  def generate_file(self):
    self.generate_from_vertices()
    self.generate_lines()
    self.drawing.save()


