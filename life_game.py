import pygame
import random
import time

WIDTH, HEIGHT = 800, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The life game - designed by nyck")

pygame.font.init()
font = pygame.font.SysFont('Arial Rounded', 40)

clock = pygame.Clock()

class Cell():
    def __init__(self, col: int, row: int) -> None:
        """ una cellula, caratterizzata dalle dimensioni e coordinate. il parametro alive è impostato randomicamente """
        self.width, self. height = 10, 10
        self.col, self.row = col, row
        self.x, self.y = 200 + self.col * self.width, 200 + self.row * self.height

        self.rect = pygame.Rect(self.x,  self.y, self.width, self.height)

        self.alive = random.choice([True, False])
        self.color = 'yellow' if self.alive else 'black'
        self.neighbors: int

    def update_color(self):
        """ associa il colore della cellula al proprio stato """
        self.color = 'yellow' if self.alive else 'black'

    def update_state(self):
        """ aggiorna lo stato della cellula in base al numero di vicini che essa ha """
        if self.alive and (self.neighbors < 2 or self.neighbors > 3):
            self.alive = False
        elif not self.alive and self.neighbors == 3:
            self.alive = True
        self.update_color()
    
    def kill(self):
        self.alive = False
    
    def create(self):
        self.alive = True

    def get_neighbors(self, cells: list):
        """ ottiene il numero di vicini che la cellula ha """
        self.neighbors = 0
        # Iteriamo sui vicini (-1, 0, 1) sia per la riga che per la colonna
        for i in range(-1, 2):
            for j in range(-1, 2):
                # Saltiamo la cellula stessa
                if i == 0 and j == 0:
                    continue
                # Calcoliamo la posizione del vicino
                neighbor_row = self.row + i
                neighbor_col = self.col + j
                # Verifichiamo che il vicino sia all'interno della griglia
                if 0 <= neighbor_row < len(cells) and 0 <= neighbor_col < len(cells):
                    if cells[neighbor_row][neighbor_col].alive:
                        self.neighbors += 1

    def draw(self):
        """ disegna la cellula """
        pygame.draw.rect(win, self.color, self.rect)

n = 40
cells = [[Cell(col, row) for col in range(n)] for row in range(n)]

def draw_your_patter(run:bool):
    if run:
        for row in cells:
                for cell in row:
                    cell.kill()

    while run:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]: 
            run = False
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if pygame.mouse.get_pressed()[0]:  # get_pressed()[0] restituisce True se il tasto sinistro è premuto
            for row in cells:
                for cell in row:
                    if cell.rect.collidepoint(mouse_x, mouse_y):
                        cell.create()

        pygame.draw.rect(win, 'white', (195, 195, 410, 410), 5, border_radius= 5)
        for row in cells:
            for cell in row:
                cell.update_color()
                cell.draw()
        info_text = font.render('Draw the cells you want to create.\nPress space when you are done!', 1, 'white')
        win.blit(info_text, ((WIDTH - info_text.get_width())//2, 25))
        pygame.display.update()

def game_loop():
    """ il loop principale del gioco """
    gen = 0
    save = True
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        win.fill('black')

        for row in cells:
            for cell in row:
                cell.get_neighbors(cells)

        for row in cells:
            for cell in row:
                cell.update_state()
                cell.draw()

        pygame.draw.rect(win, 'white', (195, 195, 410, 410), 5, border_radius= 5)
        gen_text = font.render(f'Generation: {gen}', 1, 'white')
        win.blit(gen_text, (25, 25))
        pygame.display.update()

        gen += 1
        time.sleep(1)

draw_your_patter(False)
game_loop()