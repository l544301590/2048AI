from pygame import sprite
from pygame import font
from pygame.locals import *
import pygame
import random as rd
import ai


WINDOW = {
    "WIDTH": 400,
    "HEIGHT": 500
}
PANEL_A = {
    "WIDTH": 400,
    "HEIGHT": 100
}
PANEL_B = {
    "WIDTH": 400,
    "HEIGHT": 400,
    "COLOR": (158, 158, 158)
}
BLOCK = {
    "A": 90,
    "MARGIN": 8,
    "COLOR": [             # index   number
        (84, 84, 84),   # 0       nothing
        (255, 255, 255),   # 1       2
        (255, 255, 128),   # 2       4
        (255, 255, 0),     # 3       8
        (255, 220, 128),   # 4       16
        (255, 220, 0),     # 5       32
        (255, 190, 0),     # 6       64
        (255, 160, 0),     # 7       128
        (255, 130, 0),     # 8       256
        (255, 100, 0),     # 9       512
        (255, 70, 0),      # 10      1024
        (255, 40, 0),      # 11      2048
        (255, 10, 0),      # 12      4096
    ]
}


class Grid:

    def __init__(self, data=None):
        if data:
            self.data = data
        else:
            self.data = [[0 for j in range(4)] for i in range(4)]

    def gen_next(self):
        vacancy = []
        for i in range(4):
            for j in range(4):
                if self.data[i][j] == 0:
                    vacancy.append((i, j))
        if not vacancy:
            return False
        i, j = rd.sample(vacancy, 1)[0]
        self.data[i][j] = 1
        return True

    def clone(self):
        new_data = [[0 for j in range(4)] for i in range(4)]
        for i in range(4):
            for j in range(4):
                new_data[i][j] = self.data[i][j]
        return Grid(new_data)

    def get_up_grid(self):
        new_grid = self.clone()
        new_grid.up()
        return new_grid

    def get_down_grid(self):
        new_grid = self.clone()
        new_grid.down()
        return new_grid

    def get_left_grid(self):
        new_grid = self.clone()
        new_grid.left()
        return new_grid

    def get_right_grid(self):
        new_grid = self.clone()
        new_grid.right()
        return new_grid

    def up(self):
        for col in range(4):
            aux, pos = [], 0
            for i in range(4):
                if self.data[i][col] != 0:
                    aux.append(self.data[i][col])
                self.data[i][col] = 0
            aux.append(0)
            i = 0
            while i < len(aux) - 1:
                if aux[i] == aux[i + 1]:
                    self.data[pos][col] = aux[i] + 1
                    i += 2
                elif aux[i] != aux[i + 1]:
                    self.data[pos][col] = aux[i]
                    i += 1
                pos += 1

    def down(self):
        for col in range(4):
            aux, pos = [], 3
            for i in range(3, -1, -1):
                if self.data[i][col] != 0:
                    aux.append(self.data[i][col])
                self.data[i][col] = 0
            aux.append(0)
            i = 0
            while i < len(aux) - 1:
                if aux[i] == aux[i + 1]:
                    self.data[pos][col] = aux[i] + 1
                    i += 2
                elif aux[i] != aux[i + 1]:
                    self.data[pos][col] = aux[i]
                    i += 1
                pos -= 1

    def left(self):
        for row in range(4):
            aux, pos = [], 0
            for i in range(4):
                if self.data[row][i] != 0:
                    aux.append(self.data[row][i])
                self.data[row][i] = 0
            aux.append(0)
            i = 0
            while i < len(aux) - 1:
                if aux[i] == aux[i + 1]:
                    self.data[row][pos] = aux[i] + 1
                    i += 2
                elif aux[i] != aux[i + 1]:
                    self.data[row][pos] = aux[i]
                    i += 1
                pos += 1

    def right(self):
        for row in range(4):
            aux, pos = [], 3
            for i in range(3, -1, -1):
                if self.data[row][i] != 0:
                    aux.append(self.data[row][i])
                self.data[row][i] = 0
            aux.append(0)
            i = 0
            while i < len(aux) - 1:
                if aux[i] == aux[i + 1]:
                    self.data[row][pos] = aux[i] + 1
                    i += 2
                elif aux[i] != aux[i + 1]:
                    self.data[row][pos] = aux[i]
                    i += 1
                pos -= 1

    def draw(self, panel):
        for i in range(4):
            for j in range(4):
                if self.data[i][j]:
                    # block surface
                    block_surface = pygame.Surface((BLOCK["A"], BLOCK["A"]))
                    block_surface.fill(BLOCK["COLOR"][self.data[i][j]])
                    # text surface
                    f = pygame.font.SysFont("freesansbold.ttf", 50)
                    fw, fh = f.size(str(2 ** self.data[i][j]))
                    text_surface = f.render(str(2 ** self.data[i][j]), True, (0, 0, 0))
                    # blit together
                    block_surface.blit(text_surface, ((BLOCK["A"] - fw) / 2, (BLOCK["A"] - fh) / 2))
                    block_pos = (
                            j*BLOCK["A"]+(j+1)*BLOCK["MARGIN"],
                            i*BLOCK["A"]+(i+1)*BLOCK["MARGIN"]
                    )
                    panel.blit(block_surface, block_pos)


if __name__ == '__main__':

    pygame.init()

    # init screen
    screen = pygame.display.set_mode((WINDOW["WIDTH"], WINDOW["HEIGHT"]))

    # init panel a
    panel_a = pygame.Surface((PANEL_A["WIDTH"], PANEL_A["HEIGHT"]))

    # init panel b
    panel_b = pygame.Surface((PANEL_B["WIDTH"], PANEL_B["HEIGHT"]))
    panel_b.fill(PANEL_B["COLOR"])
    for i in range(4):
        x = BLOCK["MARGIN"] + i * (BLOCK["A"] + BLOCK["MARGIN"])
        for j in range(4):
            y = BLOCK["MARGIN"] + j * (BLOCK["A"] + BLOCK["MARGIN"])
            pygame.draw.rect(panel_b, BLOCK["COLOR"][0], (x, y, BLOCK["A"], BLOCK["A"]))
    panel_b_copy = panel_b.copy()

    # init grid
    grid = Grid()
    grid.gen_next()

    AI = ai.Minimax(3)

    # main loop
    while True:

        panel_b.blit(panel_b_copy, (0, 0))  # erase all

        # handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                # if event.key == K_UP:
                #     grid.up()
                # elif event.key == K_DOWN:
                #     grid.down()
                # elif event.key == K_LEFT:
                #     grid.left()
                # elif event.key == K_RIGHT:
                #     grid.right()
                # else:
                #     break
                if event.key == K_SPACE:
                    dec = AI.decision(grid)
                    if dec == 0:
                        grid.up()
                    elif dec == 1:
                        grid.down()
                    elif dec == 2:
                        grid.left()
                    elif dec == 3:
                        grid.right()
                if not grid.gen_next():
                    exit()

        # draw new things
        grid.draw(panel_b)
        screen.blit(panel_a, (0, 0))
        screen.blit(panel_b, (0, PANEL_A["HEIGHT"]))

        pygame.display.flip()