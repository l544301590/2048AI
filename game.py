from pygame import sprite
from pygame import font
import pygame

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


def graphic_pos(row, col):
    return row * BLOCK["A"], col * BLOCK["A"]


class Box(sprite.Sprite):

    def __init__(self, row, col, ind):
        sprite.Sprite.__init__(self)

        self.ind = ind
        self.row = row
        self.col = col

        self.image = self._gen_image()
        self.rect = (
            self.col * BLOCK["A"], self.row * BLOCK["A"],  # x, y,
            BLOCK["A"], BLOCK["A"]                         # w, h
        )
        self.des_rect = self.rect
        self.des_ind = 0
        self.v_x = 0  # speed of x
        self.v_y = 0  # speed of y
        self.v_a = 0  # speed of image alpha

    def _gen_image(self):
        # block surface
        block_surface = pygame.Surface((BLOCK["A"], BLOCK["A"]))
        block_surface.fill(pygame.Color(BLOCK["COLOR"]))

        # text surface
        f = font.SysFont("freesansbold.ttf", 50)
        fw, fh = f.size(str(2**self.ind))
        text_surface = f.render(
            str(2**self.ind),   # text
            True,               # antialias
            (BLOCK["A"]-fw)/2,  # text pos x
            (BLOCK["A"]-fh)/2   # text pos y
        )

        # blit text onto block surface
        block_surface.blit(text_surface, (0, 0))
        return block_surface

    def transform(self, row, col, ind, faded):
        # set final destination
        self.row = row
        self.col = col
        self.des_rect = (col*BLOCK["A"], row*BLOCK["A"], BLOCK["A"], BLOCK["A"])
        self.des_ind = ind

        # modify each parameter
        self.v_x = (self.des_rect[0] - self.rect[0]) / 8
        self.v_y = (self.des_rect[1] - self.rect[1]) / 8
        if faded:
            self.v_a = -50

    def update(self):
        x, y, w, h = self.rect
        X, Y, W, H = self.des_rect
        if (self.v_x > 0 and X >= x) or \
                (self.v_x < 0 and X <= x) or \
                (self.v_y > 0 and Y >= y) or \
                (self.v_y < 0 and Y <= y):
            self.v_x, self.v_y, self.v_a = 0, 0, 0
            self.rect = self.des_rect
            self.ind = self.des_ind
            self.remove()
            del self
            return

        x += self.v_x
        y += self.v_y

        self.image.set_alpha(self.image.get_alpha() + self.v_a)

        self.rect = x, y, w, h


class Grid(sprite.Group):

    def __init__(self):
        sprite.Group.__init__(self)
        self.spritedict = {}  # graphically

    def up(self):
        aux = [[] for i in range(4)]
        for block in self.spritedict:
            aux[block.col].append(block)
        for ali in aux:
            sorted(ali, key=lambda b: b.row, reverse=False)
        for ali in aux:
            des_row, i = 0, 0
            while True:
                if i == len(ali) - 1:
                    ali[i].transform(des_row, ali[i].col, ali[i].ind, False)
                    break
                if ali[i].ind == ali[i+1].ind:
                    ali[i].transform(des_row, ali[i].col, ali[i].ind+1, False)
                    ali[i+1].transform(des_row, ali[i+1].col, ali[i+1].ind, True)
                    des_row += 1
                    ali.remove(ali[i+1])
                i += 1

    def down(self):
        aux = [[] for i in range(4)]
        for block in self.spritedict:
            aux[block.col].append(block)
        for ali in aux:
            sorted(ali, key=lambda b: b.row, reverse=True)
        for ali in aux:
            des_row, i = len(ali)-1, 0
            while True:
                if i == len(ali) - 1:
                    ali[i].transform(des_row, ali[i].col, ali[i].ind, False)
                    break
                if ali[i].ind == ali[i+1].ind:
                    ali[i].transform(des_row, ali[i].col, ali[i].ind+1, False)
                    ali[i+1].transform(des_row, ali[i+1].col, ali[i+1].ind, True)
                    des_row -= 1
                    ali.remove(ali[i+1])
                i += 1

    def left(self):
        aux = [[] for i in range(4)]
        for block in self.spritedict:
            aux[block.row].append(block)
        for ali in aux:
            sorted(ali, key=lambda b: b.col, reverse=False)
        for ali in aux:
            des_col, i = 0, 0
            while True:
                if i == len(ali) - 1:
                    ali[i].transform(ali[i].row, des_col, ali[i].ind, False)
                    break
                if ali[i].ind == ali[i+1].ind:
                    ali[i].transform(ali[i].row, des_col, ali[i].ind+1, False)
                    ali[i+1].transform(ali[i].row, des_col, ali[i+1].ind, True)
                    des_col += 1
                    ali.remove(ali[i+1])
                i += 1

    def right(self):
        aux = [[] for i in range(4)]
        for block in self.spritedict:
            aux[block.row].append(block)
        for ali in aux:
            sorted(ali, key=lambda b: b.col, reverse=True)
        for ali in aux:
            des_col, i = len(ali)-1, 0
            while True:
                if i == len(ali) - 1:
                    ali[i].transform(ali[i].row, des_col, ali[i].ind, False)
                    break
                if ali[i].ind == ali[i+1].ind:
                    ali[i].transform(ali[i].row, des_col, ali[i].ind+1, False)
                    ali[i+1].transform(ali[i].row, des_col, ali[i+1].ind, True)
                    des_col -= 1
                    ali.remove(ali[i+1])
                i += 1


# if __name__ == '__main__':
#     pygame.init()
#
#     screen = pygame.display.set_mode((WINDOW["A"], WINDOW["A"]))
#
#     # init panel b
#     panel_b = pygame.Surface((PANEL_B["WIDTH"], PANEL_B["HEIGHT"]))
#     panel_b.fill(PANEL_B["COLOR"])
#     for i in range(4):
#         x = BLOCK["MARGIN"] + i * (BLOCK["A"] + BLOCK["MARGIN"])
#         for j in range(4):
#             y = BLOCK["MARGIN"] + j * (BLOCK["A"] + BLOCK["MARGIN"])
#             pygame.draw.rect(panel_b, x, y)
#
#     grid = Grid()
#     grid.gen_next()
#     grid.update()
#     grid.draw(panel_b)
#
#     while True:
#         # clear all
#         panel_b.blit(main_bg, (0, 0))
#
#         # handle events
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 exit()
#             if event.type == KEYDOWN:
#                 if event.key == K_UP:
#                     grid.up()
#                 elif event.key == K_DOWN:
#                     grid.down()
#                 elif event.key == K_LEFT:
#                     grid.left()
#                 elif event.key == K_RIGHT:
#                     grid.right()
#                 else:
#                     break
#                 grid.gen_next()
#
#         # modify the reference variable
#         grid.update()
#         grid.draw(panel_b)
#
#         # modify the pixels
#         screen.blit(panel_b, (M_PANEL_MARGIN, M_PANEL_MARGIN))
#
#         # render all
#         pygame.display.flip()
