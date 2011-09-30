
# some readability consts for the View3d class:
# screen & viewport
left = 0
top = 1
right = 2
bottom = 3
# world
xmin = 0
xmax = 1
ymin = 2
ymax = 3
zmin = 4
zmax = 5
# eye
x = 0
y = 1
z = 2
      
class View3d :
   "methods related to displaying 3d objects"
   
   def __init__(self, screen, viewport, world, eye, distance) :
      # screen coords (left, top, right, bottom)
      self.screen = screen
      # "viewport" coords (l, t, r, b)
      self.viewport = viewport
      # world bounding box (xmin, xmax, ymin, ymax, zmin, zmax)
      self.world = world
      # world coordinates of the "viewer's eye" (x, y, z)
      self.eye = eye
      # z distance between the viewer's eye and the "viewport"
      self.distance = distance
      self.debug()
      
   def debug(self) :
      print( "screen:", self.screen )
      print( "viewport:", self.viewport )
      print( "world:", self.world )
      print( "eye:", self.eye )
      print( "distance:", self.distance )
      print( "w2v((1,1,1)):", self.w2v((1,1,1)) )
      print( "v2s((1,1)):", self.v2s((1,1)) )
      
   def w2v(self, point3) :
      "project a 3d point onto the 2d viewport"
      factor = (1.0 * self.distance)/(point3[z] - self.eye[z])
      vpX = point3[x] * factor
      vpY = point3[y] * factor
      return (vpX, vpY)
        
   def v2s(self, point2) :
      "convert from viewport coords to screen coords"
      relativeX = (point2[x] - self.viewport[left]) / (self.viewport[right] - self.viewport[left])
      screenX = self.screen[left] + relativeX * (self.screen[right] - self.screen[left])
      relativeY = (point2[y] - self.viewport[top]) / (self.viewport[bottom] - self.viewport[top])
      screenY = self.screen[top] + relativeY * (self.screen[bottom] - self.screen[top])      
      return (screenX, screenY)
      
      
      
