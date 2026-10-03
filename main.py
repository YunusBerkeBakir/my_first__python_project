
import pygame
import sys
import math

pygame.init()

# EKRAN
WIDTH, HEIGHT = 1575, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("my first project")

clock = pygame.time.Clock()

# RGB
SKY = (50, 100, 200)
GRASS = (90, 170, 70)
DARK_GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (35, 35, 35)
BROWN = (120, 75, 35)
LIGHT_BROWN = (170, 115, 65)
PINK = (230, 160, 165)
YELLOW = (255, 220, 80)

#yazılar
font = pygame.font.SysFont("arial", 32, bold=True)
small_font = pygame.font.SysFont("arial", 20)
big_font = pygame.font.SysFont("arial", 45, bold=True)

#koyunlar
sheep_list = []
jumping_sheep = None
sheep_count = 0

JUMP_DURATION = 1100


#koyun çizim
def draw_sheep(x, y):

    x = int(x)
    y = int(y)

    # Yün
    pygame.draw.circle(screen, WHITE, (x, y), 25)
    pygame.draw.circle(screen, WHITE, (x-17, y-12), 16)
    pygame.draw.circle(screen, WHITE, (x+5, y-19), 17)
    pygame.draw.circle(screen, WHITE, (x+19, y-8), 15)
    pygame.draw.circle(screen, WHITE, (x-15, y+12), 15)
    pygame.draw.circle(screen, WHITE, (x+8, y+15), 16)

    # Kafa
    pygame.draw.ellipse(
        screen, (205, 175, 150),
        (x+16, y-13, 34, 32)
    )

    # Kulak
    pygame.draw.ellipse(
        screen, PINK,
        (x+24, y-20, 13, 8)
    )

    # Göz
    pygame.draw.circle(
        screen, BLACK,
        (x+40, y-5), 3
    )

    # Burun
    pygame.draw.circle(
        screen, PINK,
        (x+49, y+6), 4
    )

    # Bacaklar
    pygame.draw.line(
        screen, BLACK,
        (x-12, y+22), (x-12, y+38), 4
    )

    pygame.draw.line(
        screen, BLACK,
        (x+10, y+22), (x+10, y+38), 4
    )


# arka plan
def draw_background():

    screen.fill(SKY)

    # güneş bize de tepeden bak
    pygame.draw.circle(screen, YELLOW, (900, 90), 50)

    # Bulutlar
    for x, y in [(150, 100), (550, 75), (780, 190)]:
        pygame.draw.circle(screen, WHITE, (x, y), 25)
        pygame.draw.circle(screen, WHITE, (x+30, y-10), 30)
        pygame.draw.circle(screen, WHITE, (x+60, y), 25)
        pygame.draw.rect(screen, WHITE, (x, y, 60, 25))

    # Çimen
    pygame.draw.rect(
        screen, GRASS,
        (0, 450, WIDTH, 150)
    )

    # Çimen detayları
    for x in range(0, WIDTH, 35):
        pygame.draw.line(
            screen, DARK_GREEN,
            (x, 450), (x-5, 440), 2
        )


# çit yapımı
def draw_fence():

    # direk
    for x in range(390, 590, 50):

        pygame.draw.rect(
            screen, BROWN,
            (x, 285, 18, 165),
            border_radius=4
        )

        # direk topuzları
        pygame.draw.polygon(
            screen, LIGHT_BROWN,
            [
                (x-3, 285),
                (x+9, 265),
                (x+21, 285)
            ]
        )

    #tahtalar
    pygame.draw.rect(
        screen, LIGHT_BROWN,
        (380, 315, 220, 22),
        border_radius=5
    )

    pygame.draw.rect(
        screen, LIGHT_BROWN,
        (380, 375, 220, 22),
        border_radius=5
    )

    #detay
    pygame.draw.line(
        screen, BROWN,
        (385, 325), (595, 325), 3
    )

    pygame.draw.line(
        screen, BROWN,
        (385, 385), (595, 385), 3
    )


# hedef konum
def get_sheep_position(index):

    column = index % 5
    row = index // 5

    x = 660 + column * 75
    y = 430 - row * 65

    return x, y


# oyun devam ettirme döngüsü
running = True

while running:

    clock.tick(60)

    current_time = pygame.time.get_ticks()

    # olaylar
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # SPACE: Yeni koyun oluştur
            if event.key == pygame.K_SPACE:

                if jumping_sheep is None:

                    sheep_count += 1

                    jumping_sheep = {
                        "start_time": current_time,
                        "index": sheep_count - 1
                    }

            # R: Sıfırla
            if event.key == pygame.K_r:

                sheep_list.clear()
                jumping_sheep = None
                sheep_count = 0

            # ESC: Çıkış
            if event.key == pygame.K_ESCAPE:
                running = False

    draw_background()

    draw_fence()

    # atlamış koyun
    for sheep in sheep_list:

        x, y = get_sheep_position(sheep)

        draw_sheep(x, y)

    # atlayan koyun
    if jumping_sheep is not None:

        elapsed = current_time - jumping_sheep["start_time"]

        progress = min(elapsed / JUMP_DURATION, 1)

        target_x, target_y = get_sheep_position(
            jumping_sheep["index"]
        )

        # Soldan sağa hareket
        x = 270 + (target_x - 270) * progress

        # Zıplama hareketi
        jump_height = 180 * 4 * progress * (1 - progress)

        y = 430 + (target_y - 430) * progress - jump_height

        draw_sheep(x, y)

        # Atlama başarılı
        if progress >= 1:

            sheep_list.append(jumping_sheep["index"])
            jumping_sheep = None

    else:

        # sonraki koyunun başlangıcı
        draw_sheep(270, 430)

    # sayaç
    pygame.draw.rect(
        screen, WHITE,
        (30, 25, 340, 115),
        border_radius=15
    )

    pygame.draw.rect(
        screen, BROWN,
        (30, 25, 340, 115),
        width=3,
        border_radius=15
    )

    title = small_font.render(
        "CITTEN ATLAYAN KOYUNLAR",
        True, BLACK
    )

    screen.blit(title, (55, 40))

    counter = big_font.render(
        str(sheep_count),
        True, DARK_GREEN
    )

    screen.blit(counter, (55, 65))

    # ALT BİLGİ
    info = small_font.render(
        "SPACE: Yeni koyun   |   R: Sifirla   |   ESC: Cikis",
        True, WHITE
    )

    screen.blit(info, (300, 550))

    pygame.display.flip()


pygame.quit()
sys.exit()
