import pygame
import random
import os
import sys
# import PIL


def load_image(name, colorkey=None):
    fullname = os.path.join('data1', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board_d = [[0] * height for _ in range(width)]
        self.relief = [[0] * height for _ in range(width)]
        self.left = 0
        self.top = 0
        self.cell_size = 30

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color(0, 128, 0), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                    self.cell_size), 1)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size


class Menu:
    def __init__(self):
        anim_s = ['hoi_1.png', 'hoi_2.png', 'hoi_3.png', 'hoi_4.png', 'hoi_5.png', 'hoi_6.png']
        anim_num = 0
        pygame.init()
        size = 1200, 720
        self.screen = pygame.display.set_mode(size)
        clock = pygame.time.Clock()
        ticks = 0
        speed = 0
        running = True
        while running:
            clock.tick(100)
            ticks += random.randint(1, 3)
            if ticks >= speed:
                speed = 10
                image = load_image(anim_s[anim_num])
                ticks = 0
                anim_num += 1
                if anim_num == 6:
                    running = False
                image = pygame.transform.scale(image, (1200, 720))
                self.screen.blit(image, (0, 0))
                pygame.display.flip()
        size = 500, 700
        self.screen = pygame.display.set_mode(size)
        # fon = load_image('menu_fon.png')
        # fon = pygame.transform.scale(fon, (500, 700))
        start_button = load_image('start_button.png')
        start_button = pygame.transform.scale(start_button, (350, 40))
        self.screen.blit(start_button, (75, 10))
        const_but = load_image('start_button.png')
        const_but = pygame.transform.scale(const_but, (350, 40))
        self.screen.blit(const_but, (75, 85))
        pygame.display.flip()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if 425 > pos[0] > 75 and 10 < pos[1] < 50:
                        Game()
                    elif 425 > pos[0] > 75 and 85 < pos[1] < 125:
                        Constructor()
                        Constructor().main()


class Constructor(Board):
    def __init__(self):
        super().__init__(30, 18)
        self.divisions = pygame.sprite.Group()
        self.relief_sprite = pygame.sprite.Group()
        self.choose = 0

    def main(self):
        pygame.init()
        size = 1200, 720
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.set_view(0, 40, 40)

        pygame.display.flip()

        running = True
        while running:
            self.screen.fill((0, 0, 0))
            start_button = load_image('division.png')
            start_button = pygame.transform.scale(start_button, (40, 40))
            self.screen.blit(start_button, (0, 0))
            start_button = load_image('government.png')
            start_button = pygame.transform.scale(start_button, (40, 40))
            self.screen.blit(start_button, (80, 0))
            start_button = load_image('yellow.png')
            start_button = pygame.transform.scale(start_button, (40, 40))
            self.screen.blit(start_button, (160, 0))
            start_button = load_image('blue.png')
            start_button = pygame.transform.scale(start_button, (40, 40))
            self.screen.blit(start_button, (240, 0))
            start_button = load_image('red.png')
            start_button = pygame.transform.scale(start_button, (40, 40))
            self.screen.blit(start_button, (320, 0))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    n = 0
                    s = 'hoi_save'
                    while os.path.isfile(s):
                        s = 'hoi_save'
                        n += 1
                        s += str(n)
                    s += ".txt"
                    print(s)
                    with open(s, "w") as f:
                        for sprite in self.divisions:
                            f.write(str(sprite.x) + ' ' + str(sprite.y) + ' ' + str(sprite.rel) + '\n')
                        f.write('relief\n')
                        for sprite in self.relief_sprite:
                            f.write(str(sprite.x) + ' ' + str(sprite.y) + ' ' + str(sprite.rel) + '\n')
                        f.close()
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.get_click(event.pos)
            self.render(self.screen)
            self.relief_sprite.draw(self.screen)
            self.divisions.draw(self.screen)
            pygame.display.flip()
        pygame.quit()
        Menu()

    def on_click(self, cell):
        x, y = cell[0], cell[1]
        if self.choose == 0:
            if self.board_d[x][y] == 0:
                self.board_d[x][y] = 1
                if self.relief[x][y] != 0 and self.relief[x][y] != 1:
                    Infantry_division(x, y, self.relief[x][y], self.divisions)
            else:
                self.board_d[x][y] = 0
        else:
            if self.choose != 1:
                Relief(x, y, self.choose, self.relief_sprite)
            if self.choose == self.relief[x][y]:
                self.relief[x][y] = 0
                for sprite in self.relief_sprite:
                    sprite.get_event(x, y)
            elif self.choose == 1:
                if self.relief[x][y] != 0:
                    for sprite in self.relief_sprite:
                        sprite.get_event(x, y)
                    Relief(x, y, str(self.choose) + str(self.relief[x][y]), self.relief_sprite)
                    self.relief[x][y] = 1
            elif self.choose == 2:
                self.relief[x][y] = 2
            elif self.choose == 3:
                self.relief[x][y] = 3
            elif self.choose == 4:
                self.relief[x][y] = 4

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            if mouse_pos[0] < 40:
                self.choose = 0
            elif 80 < mouse_pos[0] < 120:
                self.choose = 1
            elif 160 < mouse_pos[0] < 200:
                self.choose = 2
            elif 240 < mouse_pos[0] < 280:
                self.choose = 3
            elif 320 < mouse_pos[0] < 360:
                self.choose = 4
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)


###
###
###
###
###
###
###
###
###


class Game(Board):
    def __init__(self):
        super().__init__(33, 18)
        self.divisions = pygame.sprite.Group()
        self.relief_sprite = pygame.sprite.Group()
        with open('hoi_save.txt', 'r') as f:
            text = f.read().split('\n')
            flag = True
            for i in text:
                if i == 'relief':
                    flag = False
                elif flag:
                    i = list(map(int, i.split(' ')))
                    ind = Infantry_division(i[0], i[1], i[2], self.divisions)
                    if ind.country == 1:
                        self.board_d[i[0]][i[1]] = 1
                    elif ind.country == 2:
                        self.board_d[i[0]][i[1]] = 2
                    elif ind.country == 3:
                        self.board_d[i[0]][i[1]] = 3
                else:
                    if i != '':
                        i = list(map(int, i.split(' ')))
                        if len(str(i[2])) > 1:
                            i[2] = str(i[2])
                            self.relief[i[0]][i[1]] = i[2][0]
                        else:
                            self.relief[i[0]][i[1]] = i[2]
                        Relief(i[0], i[1], i[2], self.relief_sprite)
        self.y = 0
        self.b = 0
        self.r = 0
        for sprite in self.relief_sprite:
            if sprite.rel == 2:
                self.y += 1
            elif sprite.rel == 3:
                self.b += 1
            elif sprite.rel == 4:
                self.r += 1
        self.limit_y = self.y * 0,8
        self.limit_b = self.b * 0.8
        self.limit_r = self.r * 0.8
        self.screen_1 = None
        self.day = None
        self.month_num = None
        self.time = None
        self.year = None
        self.month = None
        self.start = None
        self.main()

    def main(self):
        self.day = 1
        self.month_num = 0
        self.year = 1936
        self.time = 'December, 1936, day 1'
        self.start = False

        size = 1200, 720
        pygame.init()
        self.screen_1 = pygame.display.set_mode(size)
        self.set_view(0, 40, 40)
        pygame.display.flip()
        clock = pygame.time.Clock()
        ticks = 0
        speed = 10

        running = True
        while running:
            self.screen_1.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     self.gametime()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.start = not self.start
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    ev_pos = event.pos
                    self.get_click(ev_pos)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    Menu()
            if ticks >= speed:
                if self.start:
                    self.gametime()
                    for division in self.divisions:
                        ret = division.update(self.board_d, self.relief)
                        if ret:
                            self.board_d[ret[0]][ret[1]] = 0
                            self.board_d[ret[3]][ret[4]] = ret[2]
                            n = self.relief[ret[0]][ret[1]]
                            if n != division.country + 1:
                                if n == 2:
                                    self.y -= 1
                                elif n == 3:
                                    self.b -= 1
                                elif n == 4:
                                    self.r -= 1
                            if self.relief[ret[3]][ret[4]] == 0:
                                if ret[2] + 1 == 2:
                                    self.y += 1
                                if ret[2] + 1 == 3:
                                    self.b += 1
                                if ret[2] + 1 == 4:
                                    self.r += 1
                            self.relief[ret[0]][ret[1]] = ret[2] + 1
                            for sprite in self.relief_sprite:
                                sprite.get_event(ret[3], ret[4])
                            Relief(ret[3], ret[4], ret[2] + 1, self.relief_sprite)
                            if self.limit_y[1] > self.y:
                                for sprite in self.relief_sprite:
                                    if sprite.rel == 2:
                                        self.relief[sprite.x][sprite.y] = 0
                                        sprite.kill()
                            if self.limit_b > self.b:
                                for sprite in self.relief_sprite:
                                    if sprite.rel == 3:
                                        self.relief[sprite.x][sprite.y] = sprite.country + 1
                                        sprite.kill()
                            if self.limit_r > self.r:
                                for sprite in self.relief_sprite:
                                    if sprite.rel == 4:
                                        self.relief[sprite.x][sprite.y] = 0
                                        sprite.kill()
                                    print('r')
                ticks = 0
            clock.tick(100)
            ticks += 1
            self.relief_sprite.draw(self.screen_1)
            self.divisions.draw(self.screen_1)
            self.render(self.screen_1)
            pygame.display.set_caption(self.time)
            pygame.display.flip()
        pygame.quit()

    def on_click(self, cell):
        x, y = cell[0], cell[1]

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)

    def gametime(self):
        self.month = ['January', 'February', 'March', 'April', 'May', 'June', 'Jul', 'August',
                      'September', 'October', 'November', 'December']
        self.day += 1
        if self.day == 32:
            self.day = 1
            self.month_num += 1
        if self.day == 31 and self.month[self.month_num] not in ['December', 'February', 'May', 'June',
                                                                 'Jul', 'September']:
            self.day = 1
            self.month_num += 1
        if self.month_num == 12:
            self.month_num = 0
            self.year += 1
        self.time = '   ' + self.month[self.month_num] + ', ' + str(self.year) + ', ' + str(self.day)


class Infantry_division(pygame.sprite.Sprite):
    def __init__(self, x, y, rel, *group):
        super().__init__(*group)
        if rel == 2:
            self.image = pygame.transform.scale(load_image('division_y.png'), (40, 40))
            self.rect = self.image.get_rect()
            self.country = 1
        if rel == 3:
            self.image = pygame.transform.scale(load_image('division_b.png'), (40, 40))
            self.rect = self.image.get_rect()
            self.country = 2
        if rel == 4:
            self.image = pygame.transform.scale(load_image('division_r.png'), (40, 40))
            self.rect = self.image.get_rect()
            self.country = 3
        # if rel == 2:
        #     self.image = pygame.transform.scale(load_image('division.png'), (40, 40))
        #     self.rect = self.image.get_rect()
        self.rect.x = x * 40
        self.rect.y = y * 40 + 40
        self.x = x
        self.y = y
        self.rel = rel
        self.hp = 100
        self.at = 100
        self.org = 30
        self.attack = False
        self.go = False
        self.pynct = 0
        self.S = 0

    def update(self, board, relief):
        dxdy = [(self.x, self.y - 1), (self.x, self.y + 1), (self.x - 1, self.y), (self.x + 1, self.y)]
        if not self.go and not self.attack:
            for xy in dxdy:
                if xy[0] > 0 and xy[1] > 0:
                    if board[xy[0]][xy[1]] != self.country and board[xy[0]][xy[1]] != 0:
                        if random.randint(1, 2) == 1:
                            print('Error')
                            # self.attack = True
                    else:
                        if relief[xy[0]][xy[1]] != self.rel:
                            if random.randrange(1, 6) == 1:
                                self.pynct = (xy[0], xy[1])
                                self.go = True
                                break
                        elif relief[xy[0]][xy[1]] == self.rel:
                            if random.randrange(1, 6) == 1:
                                self.pynct = (xy[0], xy[1])
                                self.go = True
                                print('nice2')
                                break
        if self.go:
            if self.pynct != 0:
                if board[self.pynct[0]][self.pynct[1]] != 0:
                    self.go = False
                    self.S = 0
                    self.pynct = 0
            self.S += 5
            if self.S == 100:
                self.go = False
                self.S = 0
                n = [self.x, self.y, self.country, self.pynct[0], self.pynct[1]]
                self.x = self.pynct[0]
                self.y = self.pynct[1]
                self.rect.x = self.x * 40
                self.rect.y = self.y * 40 + 40
                self.pynct = 0
                return n


class Relief(pygame.sprite.Sprite):
    def __init__(self, x, y, rel, *group):
        super().__init__(*group)
        if isinstance(rel, str):
            if rel[1] == '2':
                self.image = pygame.transform.scale(load_image('government_y.png'), (40, 40))
                self.rect = self.image.get_rect()
                print(123)
            elif rel[1] == '3':
                self.image = pygame.transform.scale(load_image('government_b.png'), (40, 40))
                self.rect = self.image.get_rect()
            elif rel[1] == '4':
                self.image = pygame.transform.scale(load_image('government_r.png'), (40, 40))
                self.rect = self.image.get_rect()
            else:
                print(1234)
                print(rel)
                self.kill()
        if rel == 2:
            self.image = pygame.transform.scale(load_image('yellow.png'), (40, 40))
            self.rect = self.image.get_rect()
        if rel == 3:
            self.image = pygame.transform.scale(load_image('blue.png'), (40, 40))
            self.rect = self.image.get_rect()
        if rel == 4:
            self.image = pygame.transform.scale(load_image('red.png'), (40, 40))
            self.rect = self.image.get_rect()
        self.rect.x = x * 40
        self.rect.y = y * 40 + 40
        self.x = x
        self.y = y
        self.rel = rel

    def get_event(self, x, y):
        if self.x == x and self.y == y:
            self.kill()


if __name__ == '__main__':
    Menu()
