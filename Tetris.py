import pygame
import sys
import random

# -------------------- Configuration --------------------
CELL_SIZE = 30
COLS = 10
ROWS = 20
SIDE_PANEL_WIDTH = 200
WIDTH = COLS * CELL_SIZE + SIDE_PANEL_WIDTH * 2  
HEIGHT = ROWS * CELL_SIZE
FPS = 60
BG_COLOR = (0, 0, 0)
GRID_LINE_COLOR = (50, 50, 50)
EMPTY_CELL_COLOR = (0, 0, 0)
SCORES = {1: 100, 2: 300, 3: 500, 4: 800}

# -------------------- Piece Class --------------------
class Piece:
    def __init__(self, shape, color):
        self.shape = shape
        self.rotation = 0
        self.x = COLS // 2 - len(shape[0][0]) // 2
        self.y = 0  
        self.color = color

    def get_current_rotation(self):
        return self.shape[self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)

# -------------------- Grid Functions --------------------
def create_grid(rows, cols, empty_color):
    return [[empty_color for _ in range(cols)] for _ in range(rows)]

def draw_grid(surface, grid):
    for r, row in enumerate(grid):
        for c, color in enumerate(row):
            rect = pygame.Rect(c * CELL_SIZE + SIDE_PANEL_WIDTH, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, GRID_LINE_COLOR, rect, 1)

# -------------------- Drawing Pieces --------------------
def draw_piece(surface, piece, offset_x=0, offset_y=0):
    shape = piece.get_current_rotation()
    for r, row in enumerate(shape):
        for c, val in enumerate(row):
            if val and piece.y + r >= 0:  
                rect = pygame.Rect(
                    offset_x + (piece.x + c) * CELL_SIZE,
                    offset_y + (piece.y + r) * CELL_SIZE,
                    CELL_SIZE, CELL_SIZE
                )
                pygame.draw.rect(surface, piece.color, rect)
                pygame.draw.rect(surface, GRID_LINE_COLOR, rect, 1)

def draw_next_piece(surface, piece, offset_x, offset_y):
    shape = piece.get_current_rotation()
    for r, row in enumerate(shape):
        for c, val in enumerate(row):
            if val:
                rect = pygame.Rect(
                    offset_x + c * CELL_SIZE,
                    offset_y + r * CELL_SIZE,
                    CELL_SIZE, CELL_SIZE
                )
                pygame.draw.rect(surface, piece.color, rect)
                pygame.draw.rect(surface, GRID_LINE_COLOR, rect, 1)

# -------------------- Collision / Movement --------------------
def valid_position(piece, grid, adj_x=0, adj_y=0, rotation=None):
    shape = piece.shape[rotation if rotation is not None else piece.rotation]
    for r, row in enumerate(shape):
        for c, val in enumerate(row):
            if val:
                new_x = piece.x + c + adj_x
                new_y = piece.y + r + adj_y
                if new_x < 0 or new_x >= COLS or new_y >= ROWS:
                    return False
                if new_y >= 0 and grid[new_y][new_x] != EMPTY_CELL_COLOR:
                    return False
    return True

def check_collision(piece, grid, adj_x=0, adj_y=0, rotation=None):
    return not valid_position(piece, grid, adj_x, adj_y, rotation)

def lock_piece(piece, grid):
    for r, row in enumerate(piece.get_current_rotation()):
        for c, val in enumerate(row):
            if val:
                y = piece.y + r
                x = piece.x + c
                if y < 0:
                    return True  # Game over
                grid[y][x] = piece.color
    return False

def clear_rows(grid):
    full_rows = [r for r in range(len(grid)) if all(cell != EMPTY_CELL_COLOR for cell in grid[r])]
    for r in full_rows:
        del grid[r]
        grid.insert(0, [EMPTY_CELL_COLOR for _ in range(COLS)])
    return len(full_rows)

# -------------------- Game Over Screen --------------------
def show_game_over_screen(screen, score):
    font = pygame.font.SysFont("Arial", 36, bold=True)
    screen.fill((0, 0, 0))
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    restart_text = font.render("Press ENTER to play again", True, (200, 200, 200))
    quit_text = font.render("Press ESC to quit", True, (200, 200, 200))
    
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 1.5))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 1.3))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# -------------------- Title Screen --------------------
def show_title_screen(screen):
    font_big = pygame.font.SysFont("Courier New", 20, bold=True)
    font_small = pygame.font.SysFont("Arial", 24)

    ascii_title = [
        " ________           __                __           ",
        "/        |         /  |              /  |          ",
        "$$$$$$$$/______   _$$ |_     ______  $$/   _______ ",
        "   $$ | /      \\ / $$   |   /      \\ /  | /       |",
        "   $$ |/$$$$$$  |$$$$$$/   /$$$$$$  |$$ |/$$$$$$$/ ",
        "   $$ |$$    $$ |  $$ | __ $$ |  $$/ $$ |$$      \\ ",
        "   $$ |$$$$$$$$/   $$ |/  |$$ |      $$ | $$$$$$  |",
        "   $$ |$$       |  $$  $$/ $$ |      $$ |/     $$/ ",
        "   $$/  $$$$$$$/    $$$$/  $$/       $$/ $$$$$$$/  ",
        "                                                   ",
        "              Tetris by Elias Tovar                "
    ]

    screen.fill((0, 0, 0))

    y_offset = HEIGHT // 6
    for line in ascii_title:
        text_surface = font_big.render(line, True, (0, 255, 0))
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, y_offset))
        y_offset += 34  

    press_enter = font_small.render("Press ENTER to start", True, (200, 200, 200))
    press_esc = font_small.render("Press ESC to quit", True, (200, 200, 200))

    screen.blit(press_enter, (WIDTH // 2 - press_enter.get_width() // 2, y_offset + 20))
    screen.blit(press_esc, (WIDTH // 2 - press_esc.get_width() // 2, y_offset + 60))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


# -------------------- Main Function --------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris by Elias Tovar")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)

    grid = create_grid(ROWS, COLS, EMPTY_CELL_COLOR)
    level = 1
    lines_for_next_level = 10
    fall_time = 0
    fall_speed = max(30, 100 - (level - 1) * 10)
    score = 0
    lines_cleared = 0

    # ----- SHAPES -----
    I_SHAPE = [[[1,1,1,1]], [[1],[1],[1],[1]]]
    O_SHAPE = [[[1,1],[1,1]]]
    T_SHAPE = [[[0,1,0],[1,1,1]], [[1,0],[1,1],[1,0]], [[1,1,1],[0,1,0]], [[0,1],[1,1],[0,1]]]
    L_SHAPE = [[[1,0],[1,0],[1,1]], [[1,1,1],[1,0,0]], [[1,1],[0,1],[0,1]], [[0,0,1],[1,1,1]]]
    J_SHAPE = [[[0,1],[0,1],[1,1]], [[1,0,0],[1,1,1]], [[1,1],[1,0],[1,0]], [[1,1,1],[0,0,1]]]
    S_SHAPE = [[[0,1,1],[1,1,0]], [[1,0],[1,1],[0,1]]]
    Z_SHAPE = [[[1,1,0],[0,1,1]], [[0,1],[1,1],[1,0]]]

    SHAPES = [I_SHAPE,O_SHAPE,T_SHAPE,L_SHAPE,J_SHAPE,S_SHAPE,Z_SHAPE]
    COLORS = [(0,255,255),(255,255,0),(128,0,128),(255,165,0),(0,0,255),(0,255,0),(255,0,0)]

    # ----- Spawn first piece -----
    index = random.randrange(len(SHAPES))
    current_piece = Piece(SHAPES[index], COLORS[index])

    # ----- Spawn next piece -----
    index = random.randrange(len(SHAPES))
    next_piece = Piece(SHAPES[index], COLORS[index])

    # ----- Hold piece -----
    held_piece = None
    can_hold = True

    running = True
    while running:
        fall_time += clock.get_rawtime()
        clock.tick(FPS)

        # ----- Piece falling -----
        if fall_time > fall_speed:
            fall_time = 0
            if valid_position(current_piece, grid, adj_y=1):
                current_piece.y += 1
            else:
                lock_piece(current_piece, grid)
                cleared = clear_rows(grid)
                if cleared > 0:
                    score += SCORES.get(cleared, 0)
                    lines_cleared += cleared

                    if lines_cleared >= level * lines_for_next_level:
                        level += 1
                        fall_speed = max(30, 100 - (level - 1) * 10)

                # Spawn new piece
                current_piece = next_piece
                index = random.randrange(len(SHAPES))
                next_piece = Piece(SHAPES[index], COLORS[index])
                can_hold = True  # reset hold availability

                # Check for game over
                if not valid_position(current_piece, grid):
                    show_game_over_screen(screen, score)
                    return

        # ----- Event Handling -----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_LEFT:
                    if valid_position(current_piece, grid, adj_x=-1):
                        current_piece.x -= 1
                elif event.key == pygame.K_RIGHT:
                    if valid_position(current_piece, grid, adj_x=1):
                        current_piece.x += 1
                elif event.key == pygame.K_DOWN:
                    if valid_position(current_piece, grid, adj_y=1):
                        current_piece.y += 1
                elif event.key == pygame.K_UP:
                    old_rot = current_piece.rotation
                    current_piece.rotate()
                    if not valid_position(current_piece, grid):
                        current_piece.rotation = old_rot
                elif event.key == pygame.K_SPACE:
                    while valid_position(current_piece, grid, adj_y=1):
                        current_piece.y += 1

                    lock_piece(current_piece, grid)
                    cleared = clear_rows(grid)
                    if cleared > 0:
                        score += SCORES.get(cleared, 0)
                        lines_cleared += cleared

                        if lines_cleared >= level * lines_for_next_level:
                            level += 1
                            fall_speed = max(30, 100 - (level - 1) * 10)

                    # Spawn new piece
                    current_piece = next_piece
                    index = random.randrange(len(SHAPES))
                    next_piece = Piece(SHAPES[index], COLORS[index])
                    can_hold = True

                    # Check for game over immediately after spawning
                    if not valid_position(current_piece, grid):
                        show_game_over_screen(screen, score)
                        return
                elif event.key == pygame.K_c:  
                    if can_hold:
                        if held_piece is None:
                            held_piece = current_piece
                            current_piece = next_piece
                            index = random.randrange(len(SHAPES))
                            next_piece = Piece(SHAPES[index], COLORS[index])
                        else:
                            held_piece, current_piece = current_piece, held_piece
                            current_piece.x = COLS // 2 - len(current_piece.get_current_rotation()[0]) // 2
                            current_piece.y = 0
                        can_hold = False

        # ----- Drawing -----
        screen.fill(BG_COLOR)

        # draw left panel 
        pygame.draw.rect(screen, (30, 30, 30), (0, 0, SIDE_PANEL_WIDTH, HEIGHT))
        # draw grid
        draw_grid(screen, grid)
        draw_piece(screen, current_piece, offset_x=SIDE_PANEL_WIDTH)

        # draw right panel 
        pygame.draw.rect(screen, (30, 30, 30), (COLS * CELL_SIZE + SIDE_PANEL_WIDTH, 0, SIDE_PANEL_WIDTH, HEIGHT))
        
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        lines_text = font.render(f"Lines: {lines_cleared}", True, (255, 255, 255))
        level_text = font.render(f"Level: {level}", True, (255, 255, 255))
        next_text = font.render("Next:", True, (255, 255, 255))
        hold_text = font.render("Hold:", True, (255, 255, 255))

        screen.blit(score_text, (COLS * CELL_SIZE + SIDE_PANEL_WIDTH + 20, 50))
        screen.blit(lines_text, (COLS * CELL_SIZE + SIDE_PANEL_WIDTH + 20, 100))
        screen.blit(level_text, (COLS * CELL_SIZE + SIDE_PANEL_WIDTH + 20, 150))
        screen.blit(next_text, (COLS * CELL_SIZE + SIDE_PANEL_WIDTH + 20, 200))
        draw_next_piece(screen, next_piece, COLS * CELL_SIZE + SIDE_PANEL_WIDTH + 20, 230)

        screen.blit(hold_text, (20, 50))
        if held_piece:
            draw_next_piece(screen, held_piece, 20, 80)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    while True:
        show_title_screen(screen)
        main()
