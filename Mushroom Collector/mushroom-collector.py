import pygame
import random

# Initializing
pygame.init()
screen = pygame.display.set_mode((700, 550))
pygame.display.set_caption("Mushroom Collector")

# Character Settings
char1 = pygame.image.load('assets\collection basket.png')
char2 = pygame.image.load('assets\mushroom.png')
char3 = pygame.image.load('assets\poisonous mushroom.png')
char4 = pygame.image.load('assets\mushroom2.png')
char1_pos = char1.get_rect()
char1_pos.topleft = pygame.Vector2(screen.get_width() / 2 - 66, 430)
char2_pos = char2.get_rect()
char2_pos.topleft = pygame.Vector2(random.randint(0, screen.get_width() - char2.get_width()), -char2.get_height())
char3_pos = char3.get_rect()
char3_pos.topleft = pygame.Vector2(random.randint(0, screen.get_width() - char3.get_width()), -char3.get_height())
collected_char3_count = 0
char4_pos = char4.get_rect()
char4_pos.topleft = pygame.Vector2(random.randint(0, screen.get_width() - char4.get_width()), -char4.get_height())
collected_chars_count = 0

# Sound Effects
sound1 = pygame.mixer.Sound('assets\mushrooms collected.wav')
sound2 = pygame.mixer.Sound('assets\poisonous warning.wav')
sound3 = pygame.mixer.Sound('assets\game over.wav')
# background sound
# pygame.mixer.music.load('background music.wav')
# pygame.mixer.music.play(-1, 0.0)

# Frame Rate Settings
clock = pygame.time.Clock()
dt = 0
fps = 60

# Game Variables
run = True
game_over = False


def game_is_over():
    font = pygame.font.Font(None, 70)
    text = font.render("Game Over", True, "Gray")
    text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
    screen.blit(text, text_rect)


def draw_score():
    font = pygame.font.Font(None, 45)

    text = font.render(f"count: {collected_chars_count} toxic: {collected_char3_count}", True, "Purple")
    text_rect = text.get_rect(topright=(690, 15))
    pygame.draw.rect(screen, "Light Blue", text_rect)

    screen.blit(text, text_rect)


def produce_mushroom(char, char_pos):
    if char_pos.y > screen.get_height():
        char_pos.topleft = pygame.Vector2(random.randint(0, screen.get_width() - char.get_width()), -char.get_height())


def collision(char, char_pos):

    global collected_chars_count, collected_char3_count

    if char1_pos.colliderect(char_pos) and (char == char2 or char == char4):
        collected_chars_count += 1
        char_pos.topleft = pygame.Vector2(random.randint(0, screen.get_width() - char.get_width()), -char.get_height())

        if collected_chars_count % 5 == 0:
            sound1.play()

    elif char1_pos.colliderect(char_pos) and char == char3:
        collected_char3_count += 1
        char_pos.topleft = pygame.Vector2(random.randint(0, screen.get_width() - char.get_width()), -char.get_height())
        sound2.play()

        if collected_char3_count == 5:
            sound3.play()


# Game Event
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        char1_pos.x -= 300 * dt
    elif key[pygame.K_RIGHT]:
        char1_pos.x += 300 * dt

    char2_pos.y += 250 * dt
    char3_pos.y += 250 * dt
    char4_pos.y += 250 * dt

    collision(char2, char2_pos)
    collision(char3, char3_pos)
    collision(char4, char4_pos)

    produce_mushroom(char2, char2_pos)
    produce_mushroom(char3, char3_pos)
    produce_mushroom(char4, char4_pos)

    if collected_char3_count == 5:
        game_is_over()
        pygame.display.update()
        pygame.time.delay(3000)
        run = False

    screen.fill("light green")
    screen.blit(char1, char1_pos)
    screen.blit(char2, char2_pos)
    screen.blit(char3, char3_pos)
    screen.blit(char4, char4_pos)

    draw_score()

    pygame.display.flip()
    dt = clock.tick(fps) / 1000
    pygame.display.update()

pygame.quit()
