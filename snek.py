import pygame
import random

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARKGRAY = (150, 150, 150)
RED = (200, 50, 50)
BLUE = (50, 50, 200)
GREEN = (50, 180, 50)

tile_size = 30
top_bar_height = 50

def show_text(msg, x, y, color, size):
    fontobj = pygame.font.SysFont("freesans", size)
    msgobj = fontobj.render(msg, False, color)
    screen.blit(msgobj, (x, y))

class Tile:
    def __init__(self, mine, x, y):
        self.clicked = False
        self.mine = mine
        self.x = x
        self.y = y
        self.neighbor_mines = 0
        self.flagged = False

    def clicked_on(self):
        self.clicked = True

MENU_WIDTH, MENU_HEIGHT = 800, 600
screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
pygame.display.set_caption("Minesweeper")

clock = pygame.time.Clock()

grid_sizes = [10, 20, 30]
current_size_idx = 0
selected_grid_size = grid_sizes[current_size_idx]

game_state = "MENU"
board = []
flags_placed = 0
max_flags = 0
start_ticks = 0
board_initialized = False
final_time = 0

def create_empty_board(size):
    global flags_placed, board_initialized
    flags_placed = 0
    board_initialized = False
    new_board = []
    for row in range(size):
        row_tiles = []
        for col in range(size):
            row_tiles.append(Tile(False, col, row))
        new_board.append(row_tiles)
    return new_board

def populate_board(size, safe_row, safe_col):
    global max_flags, start_ticks, board_initialized
    start_ticks = pygame.time.get_ticks()
    
    total_mines = 0
    for row in range(size):
        for col in range(size):
            if abs(row - safe_row) <= 1 and abs(col - safe_col) <= 1:
                board[row][col].mine = False
            else:
                ismine = random.random() < 0.15
                board[row][col].mine = ismine
                if ismine:
                    total_mines += 1
                    
    max_flags = total_mines
    
    for row in range(size):
        for col in range(size):
            if not board[row][col].mine:
                count = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < size and 0 <= nc < size:
                            if board[nr][nc].mine:
                                count += 1
                board[row][col].neighbor_mines = count
                
    board_initialized = True

def reveal_tile(r, c):
    t = board[r][c]
    if t.clicked or t.flagged:
        return
    t.clicked_on()
    if t.neighbor_mines == 0 and not t.mine:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < selected_grid_size and 0 <= nc < selected_grid_size:
                    if not board[nr][nc].clicked:
                        reveal_tile(nr, nc)

def check_win_condition():
    for row in board:
        for t in row:
            if not t.mine and not t.clicked:
                return False
    return True

run = True
while run:
    screen.fill(WHITE)
    
    grid_pixel_width = selected_grid_size * tile_size
    window_width = max(550, grid_pixel_width)
    window_height = grid_pixel_width + top_bar_height

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if game_state == "MENU":
                if 200 <= mx <= 280 and 300 <= my <= 380:
                    current_size_idx = (current_size_idx - 1) % len(grid_sizes)
                    selected_grid_size = grid_sizes[current_size_idx]
                elif 520 <= mx <= 600 and 300 <= my <= 380:
                    current_size_idx = (current_size_idx + 1) % len(grid_sizes)
                    selected_grid_size = grid_sizes[current_size_idx]
                elif 300 <= mx <= 500 and 420 <= my <= 480:
                    game_state = "PLAYING"
                    screen = pygame.display.set_mode((window_width, window_height))
                    pygame.display.set_caption("Minesweeper")
                    board = create_empty_board(selected_grid_size)

            elif game_state == "GAMEOVER" or game_state == "WIN":
                if 250 <= mx <= 550 and 350 <= my <= 420:
                    game_state = "PLAYING"
                    screen = pygame.display.set_mode((window_width, window_height))
                    pygame.display.set_caption("Minesweeper")
                    board = create_empty_board(selected_grid_size)
                elif 250 <= mx <= 550 and 450 <= my <= 520:
                    game_state = "MENU"
                    screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
                    pygame.display.set_caption("Minesweeper")

            elif game_state == "PLAYING":
                if my < top_bar_height:
                    if window_width - 150 <= mx <= window_width - 80 and 10 <= my <= 40:
                        board = create_empty_board(selected_grid_size)
                        game_state = "PLAYING"
                    elif window_width - 70 <= mx <= window_width - 10 and 10 <= my <= 40:
                        game_state = "MENU"
                        screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
                        pygame.display.set_caption("Minesweeper")
                elif my >= top_bar_height:
                    col = mx // tile_size
                    row = (my - top_bar_height) // tile_size
                    if 0 <= row < selected_grid_size and 0 <= col < selected_grid_size:
                        t = board[row][col]
                        if event.button == 1 and not t.flagged:
                            if not board_initialized:
                                populate_board(selected_grid_size, row, col)
                                t = board[row][col]
                            
                            if t.mine:
                                t.clicked_on()
                                game_state = "GAMEOVER"
                                screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
                                pygame.display.set_caption("Minesweeper")
                            else:
                                reveal_tile(row, col)
                                if check_win_condition():
                                    final_time = (pygame.time.get_ticks() - start_ticks) // 1000
                                    game_state = "WIN"
                                    screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
                                    pygame.display.set_caption("Minesweeper")
                                
                        elif event.button == 3 and board_initialized:
                            if not t.clicked:
                                if t.flagged:
                                    t.flagged = False
                                    flags_placed -= 1
                                else:
                                    if flags_placed < max_flags:
                                        t.flagged = True
                                        flags_placed += 1

    if game_state == "MENU":
        show_text("Select Grid Size", 260, 120, BLACK, 54)
        show_text(str(selected_grid_size) + " x " + str(selected_grid_size), 310, 315, BLACK, 54)
        
        pygame.draw.rect(screen, GRAY, (200, 300, 80, 80))
        pygame.draw.rect(screen, GRAY, (520, 300, 80, 80))
        show_text("-", 230, 315, BLACK, 54)
        show_text("+", 548, 315, BLACK, 54)
        
        pygame.draw.rect(screen, DARKGRAY, (300, 420, 200, 60)) 
        show_text("START", 340, 432, WHITE, 52)

    elif game_state == "GAMEOVER":
        show_text("GAME OVER", 280, 120, RED, 54)
        
        pygame.draw.rect(screen, DARKGRAY, (250, 350, 300, 70))
        show_text("PLAY AGAIN", 290, 370, WHITE, 42)
        
        pygame.draw.rect(screen, DARKGRAY, (250, 450, 300, 70))
        show_text("MAIN MENU", 290, 470, WHITE, 42)

    elif game_state == "WIN":
        show_text("YOU WIN!", 300, 100, GREEN, 54)
        show_text("Time: " + str(final_time) + " seconds", 310, 180, BLACK, 32)
        
        pygame.draw.rect(screen, DARKGRAY, (250, 350, 300, 70))
        show_text("PLAY AGAIN", 290, 370, WHITE, 42)
        
        pygame.draw.rect(screen, DARKGRAY, (250, 450, 300, 70))
        show_text("MAIN MENU", 290, 470, WHITE, 42)

    elif game_state == "PLAYING":
        for row in board:
            for t in row:
                rect = pygame.Rect(t.x * tile_size, t.y * tile_size + top_bar_height, tile_size, tile_size)
                if t.clicked:
                    if t.mine:
                        pygame.draw.rect(screen, RED, rect)
                    else:
                        pygame.draw.rect(screen, WHITE, rect)
                        if t.neighbor_mines > 0:
                            show_text(str(t.neighbor_mines), rect.x + 10, rect.y + 6, BLACK, 24)
                else:
                    if t.flagged:
                        pygame.draw.rect(screen, BLUE, rect)
                    else:
                        pygame.draw.rect(screen, GRAY, rect)
                
                pygame.draw.rect(screen, BLACK, rect, 1)

        pygame.draw.rect(screen, GRAY, (0, 0, window_width, top_bar_height))
        pygame.draw.line(screen, BLACK, (0, top_bar_height), (window_width, top_bar_height), 2)

        if board_initialized:
            elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000
        else:
            elapsed_time = 0

        hud_text = "Flags: " + str(flags_placed) + "/" + str(max_flags) + "  |  Size: " + str(selected_grid_size) + "x" + str(selected_grid_size) + "  |  Time: " + str(elapsed_time) + "s"
        show_text(hud_text, 15, 15, BLACK, 24)

        restart_btn = pygame.Rect(window_width - 150, 10, 65, 30)
        menu_btn = pygame.Rect(window_width - 75, 10, 65, 30)
        pygame.draw.rect(screen, DARKGRAY, restart_btn)
        pygame.draw.rect(screen, DARKGRAY, menu_btn)

        show_text("restart", restart_btn.x + 5, restart_btn.y + 6, WHITE, 24)
        show_text("menu", menu_btn.x + 10, menu_btn.y + 6, WHITE, 24)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()