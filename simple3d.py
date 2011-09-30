import csv
import math

class Simple3d :
   "3d object representation & manipulation"
   def __init__(self, path=None, name=None) :
      self.name = name
      self.path = path
      self.edge = []
      self.face = []
      self.vertex = []
   
   def debug(self) :
      "print the object data"
      print( "name:", self.name )
      print( "path:", self.path )
      print( "edge:" )
      for e in self.edge :
         print( e[0], e[1] )
      print( "face:" )
      for f in self.face :
         print( f[0], f[1], f[2] )
      print( "vertex:" )
      for v in self.vertex :
         print( v[0], v[1], v[2] )
      
   def read_vertices(self, vfile) :
      "read the list of x,y,z values from objname.vertices"
      reader = csv.reader(open(vfile, 'r'), delimiter=',')
      for row in reader :
         self.append_vertex( float(row[0]), float(row[1]), float(row[2]) )
   
   def read_edges(self, efile) :
      "read the list of edges from objname.edges"
      reader = csv.reader(open(efile, 'r'), delimiter=',')
      for row in reader :
         self.append_edge( int(row[0]), int(row[1]) )
   
   def read_faces(self, ffile) :
      "read the list of faces from objname.faces"
      reader = csv.reader(open(ffile, 'r'), delimiter=',')
      for row in reader :
         self.append_face( int(row[0]), int(row[1]), int(row[2]) )
   
   def load_object(self, path, name) :
      "read object data from 3 related files"
      self.path = path
      self.name = name
      if path == None or len(path) == 0 :
         fname = name
      else :
         fname = path + name if path[-1] == '/' else path + '/' + name
      # open path/name.vertices
      self.read_vertices(fname + ".vertices")
      # open path/name.edges
      self.read_edges(fname + ".edges")
      # open path/name.faces
      self.read_faces(fname + ".faces")
      
   def store_object(self, path, name) :
      "write object data to 3 related files"
      self.path = path
      self.name = name
      if path == None or len(path) == 0 :
         fname = name
      else :
         fname = path + name if path[-1] == '/' else path + '/' + name
      # open path/name.vertices
      self.write_vertices(fname + ".vertices")
      # open path/name.edges
      self.write_edges(fname + ".edges")
      # open path/name.faces
      self.write_faces(fname + ".faces")
      
   def write_vertices(self, vfile) :
      "write the list of x,y,z values to objname.vertices"
      writer = csv.writer(open(vfile, 'wb'), delimiter=',')
      for v in self.vertex :
         writer.writerow(v)
   
   def write_edges(self, efile) :
      "write the list of edges to objname.edges"
      writer = csv.writer(open(efile, 'wb'), delimiter=',')
      for e in self.edge :
         writer.writerow(e)
   
   def write_faces(self, ffile) :
      "write the list of faces to objname.faces"
      writer = csv.writer(open(ffile, 'wb'), delimiter=',')
      for f in self.face :
         writer.writerow(f)
   
   def append_vertex(self, x, y, z) :
      "add a 3D point to the object"
      self.vertex.append([x, y, z])

   def append_edge(self, v1, v2) :
      "add a pair of indices into the vertex list"
      self.edge.append([v1, v2])

   def append_face(self, v1, v2, v3) :
      "only triangles are currently supported"
      self.face.append([v1, v2, v3])

   def connect_last(self) :
      "add an edge betwen the 2 most-recently added vertices"
      self.append_edge(len(self.vertex)-2, len(self.vertex)-1)
      
   def rotX(self, angle) :
      "rotate object angle radians about the X axis"
      c = math.cos(angle)
      s = math.sin(angle)
      newV = []
      for v in self.vertex :        
         newY = v[1]*c - v[2]*s
         newZ = v[1]*s + v[2]*c
         newV.append([v[0], newY, newZ])
      self.vertex = newV
         
   def rotY(self, angle) :
      "rotate object angle radians about the Y axis"
      c = math.cos(angle)
      s = math.sin(angle)
      newV = []
      for v in self.vertex :        
         newX = v[0]*c - v[2]*s
         newZ = v[0]*s + v[2]*c
         newV.append([newX, v[1], newZ])
      self.vertex = newV
         
   def rotZ(self, angle) :
      "rotate object angle radians about the Z axis"
      c = math.cos(angle)
      s = math.sin(angle)
      newV = []
      for v in self.vertex :        
         newX = v[0]*c - v[1]*s
         newY = v[0]*s + v[1]*c
         newV.append([newX, newY, v[2]])
      self.vertex = newV
         
   def move(self, vector) :
      "displace object by vector"
      newV = []
      for v in self.vertex :        
         newX = v[0] + vector[0]
         newY = v[1] + vector[1]
         newZ = v[2] + vector[2]
         newV.append([newX, newY, newZ])
      self.vertex = newV
   
   def extrude_linear(self, p0, p1, num_new_pts) :
      "add vertices to object by 'extruding' along a line"
      # to do: faces
      dx = float(p1[0] - p0[0])/num_new_pts
      dy = float(p1[1] - p0[1])/num_new_pts
      dz = float(p1[2] - p0[2])/num_new_pts
      for i in range(num_new_pts+1) :
         self.append_vertex( i*dx + p0[0], i*dy + p0[1], i*dz + p0[2] )
         if (i > 0) :
            self.connect_last()
			
   def copy_vertices(self, first, last, vector, scale) :
	   "copy a set of vertices, displaced by a vector & scaled"
	   for i in range(first,last+1) :
		   newPt = self.vertex[i]
		   newX = (newPt[0] + vector[0])*scale
		   newY = (newPt[1] + vector[1])*scale
		   newZ = (newPt[2] + vector[2])*scale
		   self.append_vertex(newX, newY, newZ)
		
   def copy_edges(self, first, last, offset) :
      "replicate a set of edges, offsetting @ vertex index"
      for i in range(first,last+1) :
         e = self.edge[i]
         self.append_edge(e[0]+offset, e[1]+offset)
      
if __name__ == '__main__' :
   print( 'object ./ttt' )
   o = Simple3d()
   o.load_object('objects', 'test')
   o.debug()
   print( 'extrude 0,0,0 to 2,2,2 in 3' )
   o = Simple3d()
   o.extrude_linear( (0,0,0), (2.0,2.0,2.0), 3 )
   o.debug()
   print( 'extrude 0,0,0 to -2,-2,-2 in 3' )
   o.extrude_linear( (0,0,0), (-2.0,-2.0,-2.0), 3 )
   o.debug()
   # save number of vertices so far
   nv = len(o.vertex)
   print( 'copy vertices 0 through 3 displacing (2.0,0.0,0.0) scaling 1.2' )
   o.copy_vertices(0,3,(2.0,0.0,0.0), 1.2)
   print( 'copy edges 0 through 2, offset by (#vertices)' )
   o.copy_edges(0,2,nv)
   o.debug()
   o.store_object('objects', 'tst2')
