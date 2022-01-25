import pygame
import pymunk
import random
import sys
import os
import sqlite3

pygame.init()
display = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()
space = pymunk.Space()

space.gravity = 0, 100
clearer = []
salt_clearer = []
FPS = 60

all_sprites = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()

con = sqlite3.connect("saltorsug.sqlite3")
cur = con.cursor()
result = cur.execute("""SELECT * FROM parametrs""").fetchall()

ochki = 0
count = result[0][1]
open_lev = [True, False, False, False, False]
slavar_max = {1: [], 2: [], 3: [], 4: [], 5: []}


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Salt():
    def __init__(self, bool, collision_number=None):
        self.ball_rad = 3
        self.body = pymunk.Body()
        if bool is True:
            self.body.position = 500 + random.randint(0, 50), 50
        else:
            self.body.position = 500 + random.randint(0, 50), 550
        self.shape = pymunk.Circle(self.body, self.ball_rad)
        self.shape.elasticity = 0.1
        self.shape.friction = 0.3
        self.shape.density = 1
        self.shape.color = (255, 0, 0)
        space.add(self.body, self.shape)
        salt_clearer.append((self.body, self.shape))
        self.shape.collision_type = collision_number

    def draw(self):
        x, y = self.body.position
        pygame.draw.circle(display, (255, 255, 255), (int(x), int(y)), 3)

    def draw_red(self):
        x, y = self.body.position
        pygame.draw.circle(display, (255, 0, 0), (int(x), int(y)), 3)

    def colliding(self, arbiter, space, date):
        self.shape.collision_type = 112
        global count
        count -= 1


class Cup():
    def __init__(self, x, y, bool, collision_number=None):
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.xx, self.yy = x, y
        self.bool = bool
        self.shape = pymunk.Segment(self.body, (self.xx, self.yy), (self.xx + 40, self.yy), 10)
        self.shape.elasticity = 3
        self.shape.friction = 1.0
        image = load_image("cup1.png")
        if bool is False:
            sprite.image = pygame.transform.scale(pygame.transform.flip(image, False, True), (75, 50))
            sprite.rect = sprite.image.get_rect()
            all_sprites.add(sprite)
        if bool is True:
            sprite.image = pygame.transform.scale(image, (75, 50))
            sprite.rect = sprite.image.get_rect()
            self.segment_shape = pymunk.Segment(space.static_body, (self.xx - 20, self.yy + 45),
                                                (self.xx + 80, self.yy + 45), 20)
            self.segment_shape.friction = 0
            space.add(self.segment_shape)
            all_sprites.add(sprite)
        space.add(self.body, self.shape)

        if collision_number:
            self.shape.collision_type = collision_number

    def draw(self):
        if self.bool is True:
            pygame.draw.line(display, (255, 255, 255), (self.xx - 20, self.yy + 45), (self.xx + 80, self.yy + 45),
                             width=40)
            sprite.rect.x = self.xx - 4
            sprite.rect.y = self.yy - 20
            all_sprites.draw(display)
            all_sprites.update()
        if self.bool is False:
            sprite.rect.x = self.xx - 4
            sprite.rect.y = self.yy - 30
            all_sprites.draw(display)
            all_sprites.update()

    def dellor(self):
        all_sprites.remove(sprite)
        if bool is True:
            space.remove(self.segment_shape)
        space.remove(self.body, self.shape)


def terminate():
    pygame.quit()
    sys.exit()


class Ssam(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('ssam1.png')
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Go(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('go.png')
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Star(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('1.png')
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


def win_level(num, winnn=True):
    display.fill(pygame.Color('white'))
    font = pygame.font.Font(None, 120)
    animation_set = [load_image(f"{i}.png") for i in range(1, 8)]
    animation_set2 = [load_image(f"1{i}.png") for i in range(1, 4)]
    global slavar_max
    fffff = 0
    if winnn is False:
        intro_text = font.render(f'Вы не прошли уровень', True, pygame.Color('#FABA2C'))
        intro_text_x = 500 - intro_text.get_width() // 2
        intro_text_y = 20
        display.blit(intro_text, (intro_text_x, intro_text_y))
    else:
        intro_text = font.render(f'Уровень {num} пройден', True, pygame.Color('#FABA2C'))
        intro_text_x = 500 - intro_text.get_width() // 2
        intro_text_y = 30
        display.blit(intro_text, (intro_text_x, intro_text_y))
    global ochki
    font = pygame.font.Font(None, 70)
    ochki_text = font.render(f'1 звезда', True, pygame.Color('#FABA2C'))
    ochki_text_x = 0
    ochki_text_y = 0
    rolkk = 0
    if ochki > 90:
        ochki_text = font.render(f'3 звезды', True, pygame.Color('#FABA2C'))
        ochki_text_x = 500 - ochki_text.get_width() // 2
        ochki_text_y = 330
        display.blit(ochki_text, (ochki_text_x, ochki_text_y))
        rolkk = 3
        if winnn is True:
            slavar_max[num].append(rolkk)
    elif ochki in range(45, 90):
        ochki_text = font.render(f'2 звезды', True, pygame.Color('#FABA2C'))
        ochki_text_x = 500 - ochki_text.get_width() // 2
        ochki_text_y = 330
        rolkk = 2
        if winnn is True:
            slavar_max[num].append(rolkk)
        display.blit(ochki_text, (ochki_text_x, ochki_text_y))
    elif ochki <= 44:
        ochki_text = font.render(f'1 звезда', True, pygame.Color('#FABA2C'))
        ochki_text_x = 500 - ochki_text.get_width() // 2
        ochki_text_y = 330
        rolkk = 1
        if winnn is True:
            slavar_max[num].append(rolkk)
        display.blit(ochki_text, (ochki_text_x, ochki_text_y))
    while True:
        display.fill(pygame.Color('white'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] in range(620, 880) and event.pos[1] in range(480, 561):
                    if num == 1:
                        game1()
                    elif num == 2:
                        game2()
                    elif num == 3:
                        game3()
                    elif num == 4:
                        game4()
                    elif num == 5:
                        game5()
                elif event.pos[0] in range(120, 380) and event.pos[1] in range(480, 561):
                    level_room()
        pygame.draw.rect(display, pygame.Color('#012428'), (620, 480, 260, 80))
        pygame.draw.rect(display, pygame.Color('#012428'), (120, 480, 260, 80))
        font = pygame.font.Font(None, 70)
        button_text = font.render('Заново', True, pygame.Color('#FABA2C'))
        button_text_x = 660
        button_text_y = 500
        button1_text = font.render('Уровни', True, pygame.Color('#FABA2C'))
        button1_text_x = 155
        button1_text_y = 500
        display.blit(intro_text, (intro_text_x, intro_text_y))
        display.blit(button_text, (button_text_x, button_text_y))
        display.blit(button1_text, (button1_text_x, button1_text_y))

        if winnn is True:
            if rolkk == 3:
                display.blit(animation_set[fffff // 12], (250, 150))
                display.blit(animation_set[fffff // 12], (450, 150))
                display.blit(animation_set[fffff // 12], (650, 150))
                display.blit(ochki_text, (ochki_text_x, ochki_text_y))
                fffff += 1
                if fffff == 60:
                    fffff = 0
            if rolkk == 2:
                display.blit(animation_set[fffff // 12], (350, 150))
                display.blit(animation_set[fffff // 12], (550, 150))
                display.blit(ochki_text, (ochki_text_x, ochki_text_y))
                fffff += 1
                if fffff == 60:
                    fffff = 0
            if rolkk == 1:
                display.blit(animation_set[fffff // 12], (450, 150))
                display.blit(ochki_text, (ochki_text_x, ochki_text_y))
                fffff += 1
                if fffff == 60:
                    fffff = 0
        else:
            display.blit(animation_set2[fffff // 1], (253, 80))
            fffff += 1
            if fffff == 3:
                fffff = 0
        all_sprites.draw(display)
        pygame.display.flip()
        print(slavar_max)
        if winnn is False:
            clock.tick(5)
        else:
            clock.tick(100)


def start_screen():
    font = pygame.font.Font(None, 120)
    intro_text = font.render('Salt or Sugar', True, pygame.Color('#FABA2C'))
    intro_text_x = 500 - intro_text.get_width() // 2
    intro_text_y = 50
    font = pygame.font.Font(None, 70)
    button_txt = ['Играть', 'Правила']
    display.fill(pygame.Color('#099A9F'))
    display.blit(intro_text, (intro_text_x, intro_text_y))
    pygame.draw.rect(display, pygame.Color('#012428'), (370, 180, 260, 80))
    pygame.draw.rect(display, pygame.Color('#012428'), (370, 280, 260, 80))
    text_coor = -100
    for i in button_txt:
        text_coor += 100
        button1_txt = font.render(i, True, pygame.Color('#FABA2C'))
        button1_txt_x = 500 - button1_txt.get_width() // 2
        button1_txt_y = 200 + text_coor
        display.blit(button1_txt, (button1_txt_x, button1_txt_y))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] in range(370, 631) and event.pos[1] in range(180, 261):
                    level_room()
                elif event.pos[0] in range(370, 631) and event.pos[1] in range(280, 361):
                    rules()
        pygame.display.flip()
        clock.tick(FPS)


def level_room():
    display.fill(pygame.Color('#099A9F'))
    lst = []
    font = pygame.font.Font(None, 120)
    intro_text = font.render('Уровни', True, pygame.Color('#FABA2C'))
    intro_text_x = 500 - intro_text.get_width() // 2
    intro_text_y = 30
    display.blit(intro_text, (intro_text_x, intro_text_y))
    pygame.draw.rect(display, pygame.Color('#012428'), (25, 500, 180, 80))
    font = pygame.font.Font(None, 50)
    intro_text = font.render('В меню', True, pygame.Color('#FABA2C'))
    intro_text_x = 110 - intro_text.get_width() // 2
    intro_text_y = 525
    display.blit(intro_text, (intro_text_x, intro_text_y))
    global open_lev, slavar_max
    for i in range(5):
        pygame.draw.rect(display, pygame.Color('#012428'), (25 + i * 200, 180, 150, 80))
        if open_lev[i] is False:
            ssam = Ssam(60 + 200 * i, 180)
            lst.append(ssam)
            all_sprites.add(ssam)
        if open_lev[i] is True and len(slavar_max[i + 1]) == 0:
            go = Go(60 + 200 * i, 180)
            lst.append(go)
            all_sprites.add(go)
        if open_lev[i] is True and len(slavar_max[i + 1]) > 0:
            for g in range(max(slavar_max[i + 1])):
                star = Star(55 + 200 * i + 30 * g, 200)
                lst.append(star)
                all_sprites.add(star)
        font = pygame.font.Font(None, 60)
        intro_text = font.render(f'00{i + 1}', True, pygame.Color('#FABA2C'))
        intro_text_x = 100 - intro_text.get_width() // 2 + i * 200
        intro_text_y = 270
        display.blit(intro_text, (intro_text_x, intro_text_y))
    flag = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] in range(25, 176) and event.pos[1] in range(180, 261) and open_lev[0] is True:
                    for i in lst:
                        all_sprites.remove(i)
                    game1()
                if event.pos[0] in range(225, 376) and event.pos[1] in range(180, 261) and open_lev[1] is True:
                    for i in lst:
                        all_sprites.remove(i)
                    game2()
                if event.pos[0] in range(425, 576) and event.pos[1] in range(180, 261) and open_lev[2] is True:
                    for i in lst:
                        all_sprites.remove(i)
                    game3()
                if event.pos[0] in range(625, 776) and event.pos[1] in range(180, 261) and open_lev[3] is True:
                    for i in lst:
                        all_sprites.remove(i)
                    game4()
                if event.pos[0] in range(825, 976) and event.pos[1] in range(180, 261) and open_lev[4] is True:
                    for i in lst:
                        all_sprites.remove(i)
                    game5()
                if event.pos[0] in range(25, 206) and event.pos[1] in range(500, 581):
                    for i in lst:
                        all_sprites.remove(i)
                    start_screen()
                if event.pos[0] in range(370, 630) and event.pos[1] in range(380, 461) and flag is True:
                    end()
        if len(slavar_max[1]) > 0 and len(slavar_max[2]) > 0 and len(slavar_max[3]) > 0 and \
                len(slavar_max[4]) > 0 and len(slavar_max[5]) > 0:
            flag = True
            pygame.draw.rect(display, pygame.Color('#012428'), (370, 380, 260, 80))
            font = pygame.font.Font(None, 60)
            intro_text = font.render('Завершить', True, pygame.Color('#FABA2C'))
            intro_text_x = 390
            intro_text_y = 400
            display.blit(intro_text, (intro_text_x, intro_text_y))
        all_sprites.draw(display)
        pygame.display.flip()
        clock.tick(FPS)


def end():
    display.fill(pygame.Color('#099A9F'))
    allstar = 0
    for i in range(1, 6):
        allstar += max(slavar_max[i])
    lst = [
        '   Вы успешно прошли стажировку и поэтому были приняты',
        'на работу в качестве младшего официанта.',
        f' Если Вам интересны ваши результаты то вот они: {allstar}/15 звезд']
    text_coor = -120
    for i in lst:
        text_coor += 50
        font = pygame.font.Font(None, 45)
        rul = font.render(f'{i}', True, pygame.Color('#FABA2C'))
        rul_x = 30
        rul_y = 200 + text_coor
        display.blit(rul, (rul_x, rul_y))
    font = pygame.font.Font(None, 120)
    intro_text = font.render('ПОЗДРАВЛЯЕМ', True, pygame.Color('#FABA2C'))
    intro_text_x = 500 - intro_text.get_width() // 2
    intro_text_y = 30
    font = pygame.font.Font(None, 70)
    button_text = font.render('Конец', True, pygame.Color('#FABA2C'))
    button_text_x = 800 - button_text.get_width() // 2
    button_text_y = 500

    display.blit(intro_text, (intro_text_x, intro_text_y))
    pygame.draw.rect(display, pygame.Color('#012428'), (670, 480, 260, 80))
    display.blit(button_text, (button_text_x, button_text_y))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] in range(670, 931) and event.pos[1] in range(480, 561):
                    terminate()
        pygame.display.flip()
        clock.tick(FPS)


def rules():
    display.fill(pygame.Color('#099A9F'))
    lst = [
        '   Вы проходите стажировку в новой и очень крутой кофейне',
        'и почему-то именно вас клиенты постояно просят добавить',
        'сахарку в их кофе.', '    Ваша же задача выполнить просьбу клиента. А именно,',
        'вам необходимо путем рисования обьектов направить',
        'сахар в кружку клиента', '    Количество объектов и время игры ограниченно. Для',
        'рисования объектов используйте мышку']
    text_coor = -120
    for i in lst:
        text_coor += 50
        font = pygame.font.Font(None, 45)
        rul = font.render(f'{i}', True, pygame.Color('#FABA2C'))
        rul_x = 30
        rul_y = 200 + text_coor
        display.blit(rul, (rul_x, rul_y))
    font = pygame.font.Font(None, 120)
    intro_text = font.render('Правила', True, pygame.Color('#FABA2C'))
    intro_text_x = 500 - intro_text.get_width() // 2
    intro_text_y = 30
    font = pygame.font.Font(None, 70)
    button_text = font.render('Играть', True, pygame.Color('#FABA2C'))
    button_text_x = 890 - intro_text.get_width() // 2
    button_text_y = 500

    display.blit(intro_text, (intro_text_x, intro_text_y))
    pygame.draw.rect(display, pygame.Color('#012428'), (670, 480, 260, 80))
    display.blit(button_text, (button_text_x, button_text_y))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] in range(670, 931) and event.pos[1] in range(480, 561):
                    level_room()
        pygame.display.flip()
        clock.tick(FPS)


def game1():
    global count, ochki
    import time
    winflag = True
    mana = result[0][2]
    start_time, end_time = time.time(), 30
    lst, sps = [], []
    ticks_to_next_spawn, col = 10, 2
    ball = Salt(True, collision_number=2)
    sps.append(ball)
    cup = Cup(result[0][3], result[0][4], True, collision_number=1)
    drawing = False
    current_time = int(time.time() - start_time)
    count = result[0][1]
    while count > 0:
        if current_time is end_time:
            winflag = False
            break
        current_time = int(time.time() - start_time)
        display.fill(pygame.Color('#FFAA00'))
        font = pygame.font.Font(None, 70)
        time_text = font.render(f"00:{30 - current_time}", True, pygame.Color('#4671D5'))
        time_text_x = 800
        time_text_y = 50
        display.blit(time_text, (time_text_x, time_text_y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False
            if event.type == pygame.MOUSEMOTION:
                if drawing and mana > 0:
                    mana -= 1
                    curcleee = pymunk.Segment(space.static_body, (event.pos), (event.pos[0] - 1, event.pos[1] - 1), 8)
                    lst.append(event.pos)
                    curcleee.friction = 1.0
                    clearer.append(curcleee)
                    space.add(curcleee)
        font = pygame.font.Font(None, 30)
        mana_text = font.render(f"Количество объектов:{mana}", True, pygame.Color('#4671D5'))
        mana_text_x = 80
        mana_text_y = 50
        display.blit(mana_text, (mana_text_x, mana_text_y))
        ticks_to_next_spawn -= 1
        if ticks_to_next_spawn <= 0:
            ticks_to_next_spawn = 20
            col += 1
            ball = Salt(True, collision_number=col)
            sps.append(ball)

        font = pygame.font.Font(None, 30)
        text = font.render(f"{count}", True, pygame.Color('#4671D5'))
        text_x = result[0][3] + 10
        text_y = result[0][4]

        touch = [(space.add_collision_handler(1, i + 2), sps[i]) for i in range(len(sps))]
        for i, g in touch:
            i.separate = g.colliding
        for i in lst:
            pygame.draw.circle(display, pygame.Color('#4671D5'), i, 8)
        for i in sps:
            if i.shape.collision_type != 112:
                i.draw()
        cup.draw()
        display.blit(text, (text_x, text_y))

        pygame.display.update()
        clock.tick(FPS)
        space.step(1 / FPS)
    global open_lev
    if count <= 0:
        open_lev[1] = True
    cup.dellor()
    count = 20
    for i in clearer:
        space.remove(i)
    clearer.clear()
    for i in salt_clearer:
        space.remove(i[0], i[1])
    salt_clearer.clear()
    touch = []
    lst, sps = [], []
    ochki = (30 - current_time) * 2 + mana
    if winflag is False:
        win_level(1, False)
    else:
        win_level(1, True)


def game2():
    global count
    import time
    winflag = True
    mana = result[1][2]
    start_time, end_time = time.time(), 30
    lst, sps = [], []
    ticks_to_next_spawn, col = 10, 2
    ball = Salt(True, collision_number=2)
    sps.append(ball)
    cup = Cup(result[1][3], result[1][4], True, collision_number=1)
    drawing = False
    count = result[1][1]
    current_time = int(time.time() - start_time)
    while count > 0:
        if current_time is end_time:
            winflag = False
            break
        current_time = int(time.time() - start_time)
        display.fill(pygame.Color('#FFAA00'))
        font = pygame.font.Font(None, 70)
        time_text = font.render(f"00:{30 - current_time}", True, pygame.Color('#4671D5'))
        time_text_x = 800
        time_text_y = 50
        display.blit(time_text, (time_text_x, time_text_y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False
            if event.type == pygame.MOUSEMOTION:
                if drawing and mana > 0:
                    mana -= 1
                    curcleee = pymunk.Segment(space.static_body, (event.pos), (event.pos[0] - 1, event.pos[1] - 1), 8)
                    lst.append(event.pos)
                    curcleee.friction = 1.0
                    clearer.append(curcleee)
                    space.add(curcleee)
        font = pygame.font.Font(None, 30)
        mana_text = font.render(f"Количество объектов:{mana}", True, pygame.Color('#4671D5'))
        mana_text_x = 80
        mana_text_y = 50
        display.blit(mana_text, (mana_text_x, mana_text_y))
        ticks_to_next_spawn -= 1
        if ticks_to_next_spawn <= 0:
            ticks_to_next_spawn = 20
            col += 1
            ball = Salt(True, collision_number=col)
            sps.append(ball)

        font = pygame.font.Font(None, 30)
        text = font.render(f"{count}", True, pygame.Color('#4671D5'))
        text_x = result[1][3] + 10
        text_y = result[1][4]

        touch = [(space.add_collision_handler(1, i + 2), sps[i]) for i in range(len(sps))]
        for i, g in touch:
            i.separate = g.colliding
        for i in lst:
            pygame.draw.circle(display, pygame.Color('#4671D5'), i, 8)
        for i in sps:
            if i.shape.collision_type != 112:
                i.draw()
        cup.draw()
        display.blit(text, (text_x, text_y))

        pygame.display.update()
        clock.tick(FPS)
        space.step(1 / FPS)
    global open_lev
    if count <= 0:
        open_lev[2] = True
    cup.dellor()
    count = 20
    for i in clearer:
        space.remove(i)
    clearer.clear()
    for i in salt_clearer:
        space.remove(i[0], i[1])
    salt_clearer.clear()
    touch = []
    lst, sps = [], []
    global ochki
    ochki = (30 - current_time) * 2 + mana
    if winflag is False:
        win_level(2, False)
    else:
        win_level(2, True)


def game3():
    global count, ochki
    import time
    winflag = True
    mana = result[2][2]
    start_time, end_time = time.time(), 45
    lst, sps = [], []
    ticks_to_next_spawn, col = 10, 2
    ball = Salt(True, collision_number=2)
    sps.append(ball)
    cup = Cup(result[2][3], result[2][4], True, collision_number=1)
    drawing = False
    current_time = int(time.time() - start_time)
    segment_shape1 = pymunk.Segment(space.static_body, (0, 250), (160, 250), 20)
    segment_shape1.friction = 0
    space.add(segment_shape1)
    segment_shape2 = pymunk.Segment(space.static_body, (260, 250), (1000, 250), 20)
    segment_shape2.friction = 0
    space.add(segment_shape2)
    segment_shape3 = pymunk.Segment(space.static_body, (500, 400), (1000, 400), 20)
    segment_shape3.friction = 0
    space.add(segment_shape3)
    segment_shape4 = pymunk.Segment(space.static_body, (0, 400), (400, 400), 20)
    segment_shape4.friction = 0
    space.add(segment_shape4)
    count = result[2][1]
    while count > 0:
        if current_time is end_time:
            winflag = False
            break
        current_time = int(time.time() - start_time)
        display.fill(pygame.Color('#FFAA00'))
        font = pygame.font.Font(None, 70)
        time_text = font.render(f"00:{45 - current_time}", True, pygame.Color('#4671D5'))
        time_text_x = 800
        time_text_y = 50
        display.blit(time_text, (time_text_x, time_text_y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False
            if event.type == pygame.MOUSEMOTION:
                if drawing and mana > 0:
                    mana -= 1
                    curcleee = pymunk.Segment(space.static_body, (event.pos), (event.pos[0] - 1, event.pos[1] - 1), 8)
                    lst.append(event.pos)
                    clearer.append(curcleee)
                    space.add(curcleee)
        pygame.draw.line(display, (255, 255, 255), (0 - 12, 250), (160 + 7, 250), width=40)
        pygame.draw.line(display, (255, 255, 255), (260 - 12, 250), (1000 + 7, 250), width=40)
        pygame.draw.line(display, (255, 255, 255), (500 - 12, 400), (1000 + 7, 400), width=40)
        pygame.draw.line(display, (255, 255, 255), (0 - 12, 400), (400 + 7, 400), width=40)
        font = pygame.font.Font(None, 30)
        mana_text = font.render(f"Количество объектов:{mana}", True, pygame.Color('#4671D5'))
        mana_text_x = 80
        mana_text_y = 50
        display.blit(mana_text, (mana_text_x, mana_text_y))
        ticks_to_next_spawn -= 1
        if ticks_to_next_spawn <= 0:
            ticks_to_next_spawn = 15
            col += 1
            ball = Salt(True, collision_number=col)
            sps.append(ball)

        font = pygame.font.Font(None, 30)
        text = font.render(f"{count}", True, pygame.Color('#4671D5'))
        text_x = result[2][3] + 10
        text_y = result[2][4]

        touch = [(space.add_collision_handler(1, i + 2), sps[i]) for i in range(len(sps))]
        for i, g in touch:
            i.separate = g.colliding
        for i in lst:
            pygame.draw.circle(display, pygame.Color('#4671D5'), i, 8)
        for i in sps:
            if i.shape.collision_type != 112:
                i.draw()
        cup.draw()
        display.blit(text, (text_x, text_y))
        pygame.display.update()
        clock.tick(FPS)
        space.step(1 / FPS)

    global open_lev
    if count <= 0:
        open_lev[3] = True
    cup.dellor()
    count = 20
    for i in clearer:
        space.remove(i)
    clearer.clear()
    for i in salt_clearer:
        space.remove(i[0], i[1])
    salt_clearer.clear()
    space.remove(segment_shape1)
    space.remove(segment_shape2)
    space.remove(segment_shape3)
    space.remove(segment_shape4)
    touch = []
    lst, sps = [], []
    ochki = (45 - current_time) * 2 + mana
    if winflag is False:
        win_level(3, False)
    else:
        win_level(3, True)


def game4():
    global count, ochki
    import time
    winflag = True
    space.gravity = 0, -100
    mana = result[3][2]
    start_time, end_time = time.time(), 50
    lst, sps = [], []
    ticks_to_next_spawn, col = 10, 2
    ball = Salt(False, collision_number=2)
    sps.append(ball)
    cup = Cup(result[3][3], result[3][4], False, collision_number=1)
    drawing = False
    current_time = int(time.time() - start_time)
    count = result[3][1]
    while count > 0:
        if current_time is end_time:
            winflag = False
            break
        current_time = int(time.time() - start_time)
        display.fill(pygame.Color('#FFAA00'))
        font = pygame.font.Font(None, 70)
        time_text = font.render(f"00:{50 - current_time}", True, pygame.Color('#4671D5'))
        time_text_x = 800
        time_text_y = 450
        display.blit(time_text, (time_text_x, time_text_y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False
            if event.type == pygame.MOUSEMOTION:
                if drawing and mana > 0:
                    mana -= 1
                    curcleee = pymunk.Segment(space.static_body, (event.pos), (event.pos[0] - 1, event.pos[1] - 1), 8)
                    lst.append(event.pos)
                    curcleee.friction = 1.0
                    clearer.append(curcleee)
                    space.add(curcleee)
        font = pygame.font.Font(None, 30)
        mana_text = font.render(f"Количество объектов:{mana}", True, pygame.Color('#4671D5'))
        mana_text_x = 80
        mana_text_y = 450
        display.blit(mana_text, (mana_text_x, mana_text_y))
        ticks_to_next_spawn -= 1
        if ticks_to_next_spawn <= 0:
            ticks_to_next_spawn = 20
            col += 1
            ball = Salt(False, collision_number=col)
            sps.append(ball)

        font = pygame.font.Font(None, 30)
        text = font.render(f"{count}", True, pygame.Color('#4671D5'))
        text_x = result[3][3] + 10
        text_y = result[3][4] - 10

        touch = [(space.add_collision_handler(1, i + 2), sps[i]) for i in range(len(sps))]
        for i, g in touch:
            i.separate = g.colliding
        for i in lst:
            pygame.draw.circle(display, pygame.Color('#4671D5'), i, 8)
        for i in sps:
            if i.shape.collision_type != 112:
                i.draw()
        cup.draw()
        display.blit(text, (text_x, text_y))

        pygame.display.update()
        clock.tick(FPS)
        space.step(1 / FPS)
    global open_lev
    if count <= 0:
        open_lev[4] = True
    cup.dellor()
    count = 20
    for i in clearer:
        space.remove(i)
    clearer.clear()
    for i in salt_clearer:
        space.remove(i[0], i[1])
    salt_clearer.clear()
    touch = []
    lst, sps = [], []
    ochki = (50 - current_time) * 2 + mana
    space.gravity = 0, 100
    if winflag is False:
        win_level(4, False)
    else:
        win_level(4, True)


def game5():
    global count, ochki
    import time
    winflag = True
    space.gravity = 0, -100
    mana = result[4][2]
    start_time, end_time = time.time(), 50
    lst, sps = [], []
    ticks_to_next_spawn, col = 10, 2
    ball = Salt(False, collision_number=2)
    sps.append(ball)
    cup = Cup(result[4][3], result[4][4], False, collision_number=1)
    drawing = False
    current_time = int(time.time() - start_time)
    count = result[4][1]
    xxx = -250
    segmenlst, delseg = [], []
    for i in range(0, 6):
        xxx += 200
        segment_shape1 = pymunk.Segment(space.static_body, (xxx, 250), (xxx + 100, 250), 20)
        segment_shape1.friction = 0
        segmenlst.append((xxx, 250, xxx + 100, 250))
        delseg.append(segment_shape1)
        space.add(segment_shape1)
    xxx = -150
    for i in range(0, 5):
        xxx += 200
        segment_shape1 = pymunk.Segment(space.static_body, (xxx, 350), (xxx + 100, 350), 20)
        segment_shape1.friction = 0
        segmenlst.append((xxx, 350, xxx + 100, 350))
        delseg.append(segment_shape1)
        space.add(segment_shape1)
    while count > 0:
        if current_time is end_time:
            winflag = False
            break
        current_time = int(time.time() - start_time)
        display.fill(pygame.Color('#FFAA00'))
        font = pygame.font.Font(None, 70)
        time_text = font.render(f"00:{50 - current_time}", True, pygame.Color('#4671D5'))
        time_text_x = 800
        time_text_y = 450
        display.blit(time_text, (time_text_x, time_text_y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False
            if event.type == pygame.MOUSEMOTION:
                if drawing and mana > 0:
                    mana -= 1
                    curcleee = pymunk.Segment(space.static_body, (event.pos), (event.pos[0] - 1, event.pos[1] - 1), 8)
                    lst.append(event.pos)
                    curcleee.friction = 1.0
                    clearer.append(curcleee)
                    space.add(curcleee)
        font = pygame.font.Font(None, 30)
        mana_text = font.render(f"Количество объектов:{mana}", True, pygame.Color('#4671D5'))
        mana_text_x = 80
        mana_text_y = 450
        display.blit(mana_text, (mana_text_x, mana_text_y))
        ticks_to_next_spawn -= 1
        if ticks_to_next_spawn <= 0:
            ticks_to_next_spawn = 20
            col += 1
            ball = Salt(False, collision_number=col)
            sps.append(ball)
        font = pygame.font.Font(None, 30)
        text = font.render(f"{count}", True, pygame.Color('#4671D5'))
        text_x = result[4][3] + 10
        text_y = result[4][4] - 10

        touch = [(space.add_collision_handler(1, i + 2), sps[i]) for i in range(len(sps))]
        for i, g in touch:
            i.separate = g.colliding
        for i in lst:
            pygame.draw.circle(display, pygame.Color('#4671D5'), i, 8)
        for i in segmenlst:
            pygame.draw.line(display, (255, 255, 255), (i[0] - 12, i[1]), (i[2] + 7, i[3]), width=40)

        for i in sps:
            if i.shape.collision_type != 112:
                i.draw()

        cup.draw()
        display.blit(text, (text_x, text_y))

        pygame.display.update()
        clock.tick(FPS)
        space.step(1 / FPS)
    cup.dellor()
    count = 20
    for i in clearer:
        space.remove(i)
    clearer.clear()
    for i in salt_clearer:
        space.remove(i[0], i[1])
    salt_clearer.clear()
    touch = []
    lst, sps = [], []
    ochki = (50 - current_time) * 2 + mana
    space.gravity = 0, 100
    for i in delseg:
        space.remove(i)
    if winflag is False:
        win_level(5, False)
    else:
        win_level(5, True)


start_screen()
pygame.quit()
