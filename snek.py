import pygame
import random

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARKGRAY = (150, 150, 150)
RED = (200, 50, 50)
BLUE = (50, 50, 200)

tile_size = 30
top_bar_height = 50

def show_text(msg, x, y, color, size):
    fontobj = pygame.font.SysFont("freesans", size)
    msgobj = fontobj.render(msg, False, color)
    screen.blit(msgobj, (x, y))

class tile:
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

grid_sizes = [10, 25, 50]
current_size_idx = 0
selected_grid_size = grid_sizes[current_size_idx]

game_state = "MENU"
board = []
flags_placed = 0
max_flags = 10
start_ticks = 0

def create_board(size):
    global flags_placed, start_ticks
    flags_placed = 0
    start_ticks = pygame.time.get_ticks()
    
    board = []
    for row in range(size):
        row_tiles = []
        for col in range(size):
            ismine = random.random() < 0.15
            row_tiles.append(tile(ismine, col, row))
        board.append(row_tiles)
    
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
    return board

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
                    board = create_board(selected_grid_size)

            elif game_state == "GAMEOVER":
                if 250 <= mx <= 550 and 350 <= my <= 420:
                    game_state = "PLAYING"
                    screen = pygame.display.set_mode((window_width, window_height))
                    pygame.display.set_caption("Minesweeper")
                    board = create_board(selected_grid_size)
                elif 250 <= mx <= 550 and 450 <= my <= 520:
                    game_state = "MENU"
                    screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
                    pygame.display.set_caption("Minesweeper")

            elif game_state == "PLAYING":
                if my < top_bar_height:
                    if window_width - 150 <= mx <= window_width - 80 and 10 <= my <= 40:
                        board = create_board(selected_grid_size)
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
                            t.clicked_on()
                            if t.mine:
                                game_state = "GAMEOVER"
                                screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
                                pygame.display.set_caption("Minesweeper")
                            elif t.neighbor_mines == 0:
                                for dr in [-1, 0, 1]:
                                    for dc in [-1, 0, 1]:
                                        nr, nc = row + dr, col + dc
                                        if 0 <= nr < selected_grid_size and 0 <= nc < selected_grid_size:
                                            if not board[nr][nc].mine and not board[nr][nc].flagged:
                                                board[nr][nc].clicked_on()
                        elif event.button == 3:
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
        show_text("your first move may be a bomb. if you instantly lose, just try again", 100, 500, RED , 20)

    elif game_state == "GAMEOVER":
        show_text("GAME OVER", 280, 120, RED, 54)
        
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

        if game_state == "PLAYING":
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