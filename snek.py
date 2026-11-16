import pygame
import random

# init pygame
pygame.init()

# color definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARKGRAY = (150, 150, 150)
RED = (200, 50, 50)
BLUE = (50, 50, 200)
GREEN = (50, 180, 50)

# setup constants
TILE_SIZE = 30
TOP_BAR_HEIGHT = 50
MENU_WIDTH, MENU_HEIGHT = 800, 600

# setup display
screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
pygame.display.set_caption("Minesweeper")
clock = pygame.time.Clock()

# game variables
grid_sizes = [10, 20, 30]
current_size_idx = 0
selected_grid_size = grid_sizes[current_size_idx]

gameState = "MENU"
board = []
flagsPlaced = 0
maxFlags = 0
startTicks = 0
finalTime = 0

# tile class
class Tile:
    def __init__(self, mine, x, y):
        self.clicked = False
        self.mine = mine
        self.x = x
        self.y = y
        self.neighborMines = 0
        self.flagged = False

    def clicked_on(self):
        self.clicked = True

# render text
def show_text(msg, x, y, color, size):
    fontobj = pygame.font.Font(None, size)
    msgobj = fontobj.render(msg, False, color)
    screen.blit(msgobj, (x, y))

# create board
def create_board(size):
    global flagsPlaced, maxFlags, startTicks
    startTicks = pygame.time.get_ticks()
    flagsPlaced = 0
    
    newBoard = []
    totalMines = 0
    
    # row loop
    for row in range(size):
        rowTiles = []
        # col loop
        for col in range(size):
            ismine = random.random() < 0.15
            t = Tile(ismine, col, row)
            if ismine:
                totalMines += 1
            rowTiles.append(t)
        newBoard.append(rowTiles)
        
    maxFlags = totalMines
    
    # neighbor loop
    for row in range(size):
        # inner row loop
        for col in range(size):
            if not newBoard[row][col].mine:
                count = 0
                # offset loops
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < size and 0 <= nc < size:
                            if newBoard[nr][nc].mine:
                                count += 1
                newBoard[row][col].neighborMines = count
                
    return newBoard

# reveal tile
def reveal_tile(r, c):
    t = board[r][c]
    if t.clicked or t.flagged:
        return
    t.clicked_on()
    if t.neighborMines == 0 and not t.mine:
        # recursive loops
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < selected_grid_size and 0 <= nc < selected_grid_size:
                    if not board[nr][nc].clicked:
                        reveal_tile(nr, nc)

# check win
def check_win_condition():
    # win loop
    for row in board:
        for t in row:
            if not t.mine and not t.clicked:
                return False
    return True

# draw menu
def draw_menu():
    show_text("Select Grid Size", 260, 120, BLACK, 54)
    show_text(str(selected_grid_size) + " x " + str(selected_grid_size), 310, 315, BLACK, 54)
    
    pygame.draw.rect(screen, GRAY, (200, 300, 80, 80))
    pygame.draw.rect(screen, GRAY, (520, 300, 80, 80))
    show_text("-", 230, 315, BLACK, 54)
    show_text("+", 548, 315, BLACK, 54)
    
    pygame.draw.rect(screen, DARKGRAY, (300, 420, 200, 60)) 
    show_text("START", 340, 432, WHITE, 52)

# game over screen
def draw_game_over():
    show_text("GAME OVER", 280, 120, RED, 54)
    
    pygame.draw.rect(screen, DARKGRAY, (250, 350, 300, 70))
    show_text("PLAY AGAIN", 290, 370, WHITE, 42)
    
    pygame.draw.rect(screen, DARKGRAY, (250, 450, 300, 70))
    show_text("MAIN MENU", 290, 470, WHITE, 42)

# win screen
def draw_win():
    show_text("YOU WIN!", 300, 100, GREEN, 54)
    show_text("Time: " + str(finalTime) + " seconds", 310, 180, BLACK, 32)
    
    pygame.draw.rect(screen, DARKGRAY, (250, 350, 300, 70))
    show_text("PLAY AGAIN", 290, 370, WHITE, 42)
    
    pygame.draw.rect(screen, DARKGRAY, (250, 450, 300, 70))
    show_text("MAIN MENU", 290, 470, WHITE, 42)

# draw board
def draw_playing(windowWidth):
    # board loop
    for row in board:
        for t in row:
            rect = pygame.Rect(t.x * TILE_SIZE, t.y * TILE_SIZE + TOP_BAR_HEIGHT, TILE_SIZE, TILE_SIZE)
            if t.clicked:
                if t.mine:
                    pygame.draw.rect(screen, RED, rect)
                else:
                    pygame.draw.rect(screen, WHITE, rect)
                    if t.neighborMines > 0:
                        show_text(str(t.neighborMines), rect.x + 10, rect.y + 6, BLACK, 24)
            else:
                if t.flagged:
                    pygame.draw.rect(screen, BLUE, rect)
                else:
                    pygame.draw.rect(screen, GRAY, rect)
            
            pygame.draw.rect(screen, BLACK, rect, 1)

    pygame.draw.rect(screen, GRAY, (0, 0, windowWidth, TOP_BAR_HEIGHT))
    pygame.draw.line(screen, BLACK, (0, TOP_BAR_HEIGHT), (windowWidth, TOP_BAR_HEIGHT), 2)

    elapsedTime = (pygame.time.get_ticks() - startTicks) // 1000

    hudText = f"{selected_grid_size}x{selected_grid_size} Flags: {flagsPlaced}/{maxFlags} Time: {elapsedTime}s"
    show_text(hudText, 10, 16, BLACK, 18)

    restart_btn = pygame.Rect(windowWidth - 115, 10, 50, 30)
    menu_btn = pygame.Rect(windowWidth - 60, 10, 50, 30)
    
    pygame.draw.rect(screen, DARKGRAY, restart_btn)
    pygame.draw.rect(screen, DARKGRAY, menu_btn)

    show_text("restart", restart_btn.x + 14, restart_btn.y + 8, WHITE, 16)
    show_text("menu", menu_btn.x + 10, menu_btn.y + 8, WHITE, 16)

# main loop
run = True
while run:
    screen.fill(WHITE)
    
    gridPixelWidth = selected_grid_size * TILE_SIZE
    windowWidth = gridPixelWidth
    windowHeight = gridPixelWidth + TOP_BAR_HEIGHT

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            
            if gameState == "MENU":
                if 200 <= mx <= 280 and 300 <= my <= 380:
                    current_size_idx = (current_size_idx - 1) % len(grid_sizes)
                    selected_grid_size = grid_sizes[current_size_idx]
                elif 520 <= mx <= 600 and 300 <= my <= 380:
                    current_size_idx = (current_size_idx + 1) % len(grid_sizes)
                    selected_grid_size = grid_sizes[current_size_idx]
                elif 300 <= mx <= 500 and 420 <= my <= 480:
                    gameState = "PLAYING"
                    screen = pygame.display.set_mode((windowWidth, windowHeight))
                    pygame.display.set_caption("Minesweeper")
                    board = create_board(selected_grid_size)

            elif gameState in ("GAMEOVER", "WIN"):
                if 250 <= mx <= 550 and 350 <= my <= 420:
                    gameState = "PLAYING"
                    screen = pygame.display.set_mode((windowWidth, windowHeight))
                    pygame.display.set_caption("Minesweeper")
                    board = create_board(selected_grid_size)
                elif 250 <= mx <= 550 and 450 <= my <= 520:
                    gameState = "MENU"
                    screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
                    pygame.display.set_caption("Minesweeper")

            elif gameState == "PLAYING":
                if my < TOP_BAR_HEIGHT:
                    restart_btn = pygame.Rect(windowWidth - 115, 10, 50, 30)
                    menu_btn = pygame.Rect(windowWidth - 60, 10, 50, 30)
                    
                    if restart_btn.collidepoint(mx, my):
                        board = create_board(selected_grid_size)
                        gameState = "PLAYING"
                    elif menu_btn.collidepoint(mx, my):
                        gameState = "MENU"
                        screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
                        pygame.display.set_caption("Minesweeper")
                elif my >= TOP_BAR_HEIGHT:
                    col = mx // TILE_SIZE
                    row = (my - TOP_BAR_HEIGHT) // TILE_SIZE
                    if 0 <= row < selected_grid_size and 0 <= col < selected_grid_size:
                        t = board[row][col]
                        if event.button == 1 and not t.flagged:
                            if t.mine:
                                t.clicked_on()
                                gameState = "GAMEOVER"
                                screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
                                pygame.display.set_caption("Minesweeper")
                            else:
                                reveal_tile(row, col)
                                if check_win_condition():
                                    finalTime = (pygame.time.get_ticks() - startTicks) // 1000
                                    gameState = "WIN"
                                    screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
                                    pygame.display.set_caption("Minesweeper")
                                
                        elif event.button == 3:
                            if not t.clicked:
                                if t.flagged:
                                    t.flagged = False
                                    flagsPlaced -= 1
                                else:
                                    if flagsPlaced < maxFlags:
                                        t.flagged = True
                                        flagsPlaced += 1

    if gameState == "MENU":
        draw_menu()
    elif gameState == "GAMEOVER":
        draw_game_over()
    elif gameState == "WIN":
        draw_win()
    elif gameState == "PLAYING":
        draw_playing(windowWidth)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()