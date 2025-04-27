import lib.stddraw as stddraw
from lib.picture import Picture
from lib.color import Color
import os
from game_grid import GameGrid
from point import Point
from tetromino import Tetromino
from game_grid import draw_tetromino_preview
import random
import time

def start():
    grid_h, grid_w = 20, 12
    canvas_h = 40 * grid_h
    canvas_w = 40 * (grid_w + 6)  # sağ panel için alan
    stddraw.setCanvasSize(canvas_w, canvas_h)
    stddraw.setXscale(-0.5, grid_w + 5.5)
    stddraw.setYscale(-0.5, grid_h - 0.5)

    Tetromino.grid_height = grid_h
    Tetromino.grid_width = grid_w
    grid = GameGrid(grid_h, grid_w)

    current_tetromino = create_tetromino()
    next_tetromino = create_tetromino()
    held_tetromino = None
    can_hold = True

    grid.current_tetromino = current_tetromino

    display_game_menu(grid_h, grid_w)

    fall_delay = 0.5
    level = 1
    last_time = time.time()
    paused = False

    while True:
        if stddraw.hasNextKeyTyped():
            key_typed = stddraw.nextKeyTyped()
            if key_typed == "left":
                current_tetromino.move("left", grid)
            elif key_typed == "right":
                current_tetromino.move("right", grid)
            elif key_typed == "down":
                current_tetromino.move("down", grid)
            elif key_typed == "space":
                while current_tetromino.move("down", grid):
                    pass
            elif key_typed == "up" or key_typed == "r":
                current_tetromino.rotate(grid)
            elif key_typed == "h" and can_hold:
                if held_tetromino is None:
                    held_tetromino = current_tetromino
                    current_tetromino = next_tetromino
                    next_tetromino = create_tetromino()
                else:
                    held_tetromino, current_tetromino = current_tetromino, held_tetromino
                    held_tetromino.bottom_left_cell.y = Tetromino.grid_height - 1
                can_hold = False
            elif key_typed == "p":  # Duraklat / Devam
                paused = not paused
                while paused:
                    stddraw.setFontSize(20)
                    stddraw.setPenColor(Color(255, 255, 0))
                    stddraw.text(grid_w + 2.5, 5, "PAUSED")
                    stddraw.show(100)
                    if stddraw.hasNextKeyTyped():
                        pause_key = stddraw.nextKeyTyped()
                        if pause_key == "p":
                            paused = False
                        elif pause_key == "r":
                            start()
                            return
                        elif pause_key == "f":
                            fall_delay *= 0.8
            elif key_typed == "f":  # Hız artır
                if level < 15:
                    level += 1
                    fall_delay = max(0.05, 0.5 * (0.9 ** level))
            elif key_typed == "r":  # Yeniden başlat
                start()
                return

            stddraw.clearKeysTyped()

        if time.time() - last_time >= fall_delay:
            success = current_tetromino.move("down", grid)
            if not success:
                tiles, pos = current_tetromino.get_min_bounded_tile_matrix(True)
                game_over = grid.update_grid(tiles, pos)

                for row in grid.tile_matrix:
                    for tile in row:
                        if tile is not None and tile.number == 2048:
                            display_win_screen(grid.score)
                            return

                if game_over:
                    display_game_over(grid.score)
                    return

                current_tetromino = next_tetromino
                next_tetromino = create_tetromino()
                grid.current_tetromino = current_tetromino
                can_hold = True

                if fall_delay > 0.1:
                    fall_delay *= 0.98

            # ✅ EKRANI GÜNCELLE (Next, Hold, Tuş Bilgileri dahil)
            grid.display(next_tetromino, held_tetromino, level)

            # 🔽 Sağ panel tuş açıklamaları
            stddraw.setFontSize(12)
            stddraw.setPenColor(Color(255, 255, 255))
            stddraw.text(grid_w + 2.5, 3, "P: Pause/Resume")
            stddraw.text(grid_w + 2.5, 2, "R: Restart")
            stddraw.text(grid_w + 2.5, 1, "F: Faster")

            
            last_time = time.time()





def create_tetromino():
   tetromino_types = ['I', 'O', 'Z', 'T', 'S', 'L', 'J']
   random_type = random.choice(tetromino_types)
   return Tetromino(random_type)


def display_game_menu(grid_height, grid_width):
   background_color = Color(42, 69, 99)
   button_color = Color(25, 255, 228)
   text_color = Color(31, 160, 239)
   stddraw.clear(background_color)
   current_dir = os.path.dirname(os.path.realpath(__file__))
   img_file = current_dir + "/images/menu_image.png"
   image_to_display = Picture(img_file)
   img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
   stddraw.picture(image_to_display, img_center_x, img_center_y)
   button_w, button_h = grid_width - 1.5, 2
   button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(25)
   stddraw.setPenColor(text_color)
   stddraw.text(img_center_x, 5, "Click Here to Start the Game")
   while True:
      stddraw.show(50)
      if stddraw.mousePressed():
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         if button_blc_x <= mouse_x <= button_blc_x + button_w and \
            button_blc_y <= mouse_y <= button_blc_y + button_h:
            break


def display_game_over(score):
   stddraw.clear(Color(0, 0, 0))
   stddraw.setPenColor(Color(255, 0, 0))
   stddraw.setFontSize(30)
   stddraw.text(6, 12, "GAME OVER")
   stddraw.setFontSize(20)
   stddraw.setPenColor(Color(255, 255, 255))
   stddraw.text(6, 10, f"Final Score: {score}")
   stddraw.text(6, 8, "Press any key to exit")
   stddraw.show()
   while not stddraw.hasNextKeyTyped():
      stddraw.show(100)


def display_win_screen(score):
   stddraw.clear(Color(0, 0, 0))
   stddraw.setPenColor(Color(0, 255, 0))
   stddraw.setFontSize(30)
   stddraw.text(6, 12, "YOU WIN!")
   stddraw.setFontSize(20)
   stddraw.setPenColor(Color(255, 255, 255))
   stddraw.text(6, 10, f"Final Score: {score}")
   stddraw.text(6, 8, "Press any key to exit")
   stddraw.show()
   while not stddraw.hasNextKeyTyped():
      stddraw.show(100)


if __name__ == '__main__':
   start()