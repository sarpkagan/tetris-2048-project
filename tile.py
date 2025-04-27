import lib.stddraw as stddraw  # used for drawing the tiles to display them
from lib.color import Color  # used for coloring the tiles
import random  # for assigning random numbers to tiles

# A class for modeling numbered tiles as in 2048
class Tile:
   # Class variables shared among all Tile objects
   boundary_thickness = 0.004
   font_family, font_size = "Arial", 14

   # A constructor that creates a tile with 2 or 4 as the number on it
   def __init__(self):
      # set the number on this tile (90% 2, 10% 4)
      self.number = 4 if random.random() < 0.1 else 2
      # set the colors of this tile
      self.background_color = Color(151, 178, 199)
      self.foreground_color = Color(0, 100, 200)
      self.box_color = Color(0, 100, 200)

   # A method for drawing this tile at a given position with a given length
   def draw(self, position, length=1, ghost=False):
    if ghost:
        ghost_color = Color(200, 200, 200)  # gri
        stddraw.setPenColor(ghost_color)
        stddraw.filledSquare(position.x, position.y, length / 2)
        stddraw.setPenColor(Color(150, 150, 150))  # kenarlık
        stddraw.setPenRadius(Tile.boundary_thickness)
        stddraw.square(position.x, position.y, length / 2)
        stddraw.setPenRadius()
    else:
        stddraw.setPenColor(self.background_color)
        stddraw.filledSquare(position.x, position.y, length / 2)
        stddraw.setPenColor(self.box_color)
        stddraw.setPenRadius(Tile.boundary_thickness)
        stddraw.square(position.x, position.y, length / 2)
        stddraw.setPenRadius()
        stddraw.setPenColor(self.foreground_color)
        stddraw.setFontFamily(Tile.font_family)
        stddraw.setFontSize(Tile.font_size)
        stddraw.text(position.x, position.y, str(self.number))