import pygame
import random

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# SHAPE FORMATS

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

# index 0 - 6 represent shape


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c

    return grid


def convert_shape_format(piece):
    positions = []
    shape_format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(shape_format):
        row = list(line)
        for j, col in enumerate(row):
            if col == '0':
                positions.append((piece.x + j - 2, piece.y + i - 4))

    return positions


def valid_space(piece, grid):
    valid_positions = set()
    for y in range(20):
        for x in range(10):
            if grid[y][x] == (0, 0, 0):
                valid_positions.add((x, y))

    piece_positions = convert_shape_format(piece)

    for pos in piece_positions:
        if pos not in valid_positions and pos[1] > -1:
            return False

    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


def get_shape():
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    pass


def draw_grid_lines(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * block_size), (sx + play_width, sy + i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * block_size, sy), (sx + j * block_size, sy + play_height))


def clear_rows(grid, locked_positions):
    row_clear_start = None
    num_rows_to_clear = 0

    for row in range(len(grid)):
        row_needs_clearing = True
        for col in range(len(grid[row])):
            if grid[row][col] == (0, 0, 0):
                row_needs_clearing = False
                break

        if row_needs_clearing:
            if row_clear_start is None:
                row_clear_start = row
            num_rows_to_clear += 1

    if num_rows_to_clear == 0:
        return locked_positions

    for row_to_clear in range(row_clear_start, row_clear_start + num_rows_to_clear):
        for col in range(len(grid[row_to_clear])):
            grid[row_to_clear][col] = (0, 0, 0)
            del locked_positions[(col, row_to_clear)]

    updated_locked_positions = {}
    for key, val in locked_positions.items():
        x = key[0]
        y = key[1]
        new_y_loc = key[1] + num_rows_to_clear

        if new_y_loc <= row_clear_start + num_rows_to_clear:
            grid[new_y_loc][x] = val
            grid[y][x] = grid[y - 1][x]
            updated_locked_positions[(x, new_y_loc)] = val
        else:
            updated_locked_positions[(x, y)] = val

    locked_positions = updated_locked_positions
    return locked_positions


def draw_next_piece(piece: Piece, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Piece:', True, (255, 255, 255))

    sx = top_left_x + play_width + 60
    sy = top_left_y + play_height // 20
    piece_format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(piece_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                x_pos_block = sx + j * block_size
                y_pos_block = sy + i * block_size
                pygame.draw.rect(surface, piece.color, (x_pos_block, y_pos_block, block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 25))


def draw_window(surface, grid):
    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', True, (255, 255, 255))

    center_at_top_dimens = (top_left_x + play_width/2 - (label.get_width()/2), 30)
    surface.blit(label, center_at_top_dimens)

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)  # drawing pieces on grid

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)    # Outer border
    draw_grid_lines(surface, grid)


def color_piece_on_grid(shape_positions, current_piece, grid):
    for i in range(len(shape_positions)):
        x, y = shape_positions[i]
        if y > -1:
            grid[y][x] = current_piece.color

    return shape_positions


def update_locked_positions(current_piece, current_shape_positions, locked_positions):
    for pos in current_shape_positions:
        pos_key = (pos[0], pos[1])
        locked_positions[pos_key] = current_piece.color


def handle_down_pressed():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        return 0.08
    else:
        return 0.75


def main(main_window):
    locked_positions = {}
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.75

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1

            # checks if current piece has moved down past the bottom of the grid or moved into another piece, if so, so move it back up and trigger next piece to begin moving down
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not valid_space(current_piece, grid):
                        current_piece.rotation -= 1

        fall_speed = handle_down_pressed()
        shape_positions = convert_shape_format(current_piece)
        color_piece_on_grid(shape_positions, current_piece, grid)

        if change_piece:
            update_locked_positions(current_piece, shape_positions, locked_positions)
            locked_positions = clear_rows(grid, locked_positions)
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

        draw_window(main_window, grid)
        draw_next_piece(next_piece, main_window)
        pygame.display.update()
        if check_lost(locked_positions):
            run = False

    pygame.display.quit()


def main_menu(main_window):
    main(main_window)


window = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("Tetris")
main_menu(window)  # start game
