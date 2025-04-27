import lib.stddraw as stddraw
from lib.color import Color
from point import Point
import numpy as np
from collections import deque  # bağlantı kontrolü için kullanılacak


def draw_tetromino_preview(tetromino, offset_x, offset_y):
    matrix = tetromino.get_min_bounded_tile_matrix()
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            tile = matrix[row][col]
            if tile is not None:
                x = offset_x + col
                y = offset_y - row
                tile.draw(Point(x, y))
class GameGrid:
   def __init__(self, grid_h, grid_w):
      self.grid_height = grid_h
      self.grid_width = grid_w
      self.tile_matrix = np.full((grid_h, grid_w), None)
      self.current_tetromino = None
      self.game_over = False
      self.empty_cell_color = Color(42, 69, 99)
      self.line_color = Color(0, 100, 200)
      self.boundary_color = Color(0, 100, 200)
      self.line_thickness = 0.002
      self.box_thickness = 10 * self.line_thickness
      self.score = 0  # 🔥 Yeni: skor değişkeni

   def display(self, next_tetromino=None, held_tetromino=None, level=1):
    stddraw.clear(self.empty_cell_color)
    self.draw_grid()

    if self.current_tetromino is not None:
        ghost = self.current_tetromino.get_ghost_copy(self)
        ghost.draw(ghost=True)
        self.current_tetromino.draw()

    self.draw_boundaries()
    self.draw_score()

    grid_w = self.grid_width
    grid_h = self.grid_height

    # 🔴 Sağ panel arka planı (kırmızı)
    stddraw.setPenColor(Color(255, 0, 0))  # kırmızı panel
    stddraw.filledRectangle(grid_w, 0, 6, grid_h)

    # 🟢 Yazılar - beyaz
    stddraw.setPenColor(Color(255, 255, 255))
    stddraw.setFontSize(14)
    panel_x = self.grid_width + 2
    stddraw.text(panel_x, self.grid_height - 2, "Next:")
    if next_tetromino:
        draw_tetromino_preview(next_tetromino, panel_x - 1, self.grid_height - 5)

    stddraw.text(panel_x, self.grid_height - 8, "Hold:")
    if held_tetromino:
        draw_tetromino_preview(held_tetromino, panel_x - 1, self.grid_height - 11)

    # 🔽 Tuş açıklamaları
    stddraw.setFontSize(12)
    stddraw.text(grid_w + 2.5, 3, "P: Pause/Resume")
    stddraw.text(grid_w + 2.5, 2, "R: Restart")
    stddraw.text(grid_w + 2.5, 1, "F: Faster")

    # 🔼 Seviye göster
    stddraw.setFontSize(14)
    stddraw.text(grid_w + 2.5, 6, f"Level: {level}")

    stddraw.show(250)

   def draw_grid(self):
      for row in range(self.grid_height):
         for col in range(self.grid_width):
            if self.tile_matrix[row][col] is not None:
               self.tile_matrix[row][col].draw(Point(col, row))
      stddraw.setPenColor(self.line_color)
      stddraw.setPenRadius(self.line_thickness)
      start_x, end_x = -0.5, self.grid_width - 0.5
      start_y, end_y = -0.5, self.grid_height - 0.5
      for x in np.arange(start_x + 1, end_x, 1):
         stddraw.line(x, start_y, x, end_y)
      for y in np.arange(start_y + 1, end_y, 1):
         stddraw.line(start_x, y, end_x, y)
      stddraw.setPenRadius()

   def draw_boundaries(self):
    stddraw.setPenColor(self.boundary_color)
    stddraw.setPenRadius(self.box_thickness)
    
    # ✅ Sadece oyun gridini değil, tüm ekranı kapsayan bir kutu çiz
    total_width = self.grid_width + 6  # sağ panel dahil
    stddraw.rectangle(-0.5, -0.5, total_width, self.grid_height)
    
    stddraw.setPenRadius()

   def draw_score(self):
      stddraw.setPenColor(Color(255, 255, 255))
      stddraw.setFontSize(18)
      stddraw.text(1, self.grid_height - 1, f"Score: {self.score}")

   def is_occupied(self, row, col):
      if not self.is_inside(row, col):
         return False
      return self.tile_matrix[row][col] is not None

   def is_inside(self, row, col):
      return 0 <= row < self.grid_height and 0 <= col < self.grid_width

   def update_grid(self, tiles_to_lock, blc_position):
      self.current_tetromino = None
      n_rows, n_cols = len(tiles_to_lock), len(tiles_to_lock[0])
      for col in range(n_cols):
         for row in range(n_rows):
            if tiles_to_lock[row][col] is not None:
               pos = Point()
               pos.x = blc_position.x + col
               pos.y = blc_position.y + (n_rows - 1) - row
               if self.is_inside(pos.y, pos.x):
                  self.tile_matrix[pos.y][pos.x] = tiles_to_lock[row][col]
               else:
                  self.game_over = True

      self.merge_tiles()
      self.clear_full_rows()
      self.remove_free_tiles()  # 🔥 Yeni: serbest (bağsız) tile'ları temizle

      return self.game_over

   def merge_tiles(self):
      for col in range(self.grid_width):
         row = 0
         while row < self.grid_height - 1:
            current = self.tile_matrix[row][col]
            above = self.tile_matrix[row + 1][col]
            if current and above and current.number == above.number:
               current.number *= 2
               self.score += current.number  # 🔥 Skora ekle
               self.tile_matrix[row + 1][col] = None
               for r in range(row + 1, self.grid_height - 1):
                  self.tile_matrix[r][col] = self.tile_matrix[r + 1][col]
                  self.tile_matrix[r + 1][col] = None
               continue
            row += 1

   def clear_full_rows(self):
      row = 0
      while row < self.grid_height:
         full = True
         for col in range(self.grid_width):
            if self.tile_matrix[row][col] is None:
               full = False
               break
         if full:
            for c in range(self.grid_width):
               self.score += self.tile_matrix[row][c].number  # 🔥 Skora ekle
            for r in range(row, self.grid_height - 1):
               for c in range(self.grid_width):
                  self.tile_matrix[r][c] = self.tile_matrix[r + 1][c]
            for c in range(self.grid_width):
               self.tile_matrix[self.grid_height - 1][c] = None
            continue
         row += 1

   # 🔻 Yeni: Serbest (bağlantısız) tile'ları sil ve skora ekle
   def remove_free_tiles(self):
      visited = np.full((self.grid_height, self.grid_width), False)
      connected = np.full((self.grid_height, self.grid_width), False)

      # BFS ile tüm bağlı olanları bul (yani aşağıya bağlantılı olanlar)
      for col in range(self.grid_width):
         if self.tile_matrix[0][col] is not None:
            queue = deque()
            queue.append((0, col))
            connected[0][col] = True
            while queue:
               r, c = queue.popleft()
               for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                  nr, nc = r + dr, c + dc
                  if self.is_inside(nr, nc) and self.tile_matrix[nr][nc] is not None and not connected[nr][nc]:
                     connected[nr][nc] = True
                     queue.append((nr, nc))

      # bağlı olmayan tile'ları sil ve skora ekle
      for r in range(self.grid_height):
         for c in range(self.grid_width):
            if self.tile_matrix[r][c] is not None and not connected[r][c]:
               self.score += self.tile_matrix[r][c].number
               self.tile_matrix[r][c] = None



