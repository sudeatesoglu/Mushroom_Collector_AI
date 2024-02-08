import pygame
import random
import os


class Character:
    """
    Represents the game characters.
    """

    def __init__(self, image_path, initial_position):
        """
        Initialize a Character object with an image and initial position.

        Args:
            image_path (str): path to the image file.
            initial_position (tuple): initial position of the character (x, y).
        """
        self.image = pygame.image.load(image_path)  # Load image from file
        self.position = self.image.get_rect(topleft=initial_position)  # Set position


class Info:
    """
    Manages displaying game information.
    """

    @staticmethod
    def game_over_message(screen):
        """
        Display the game over message on the screen.

        Args:
            screen (pygame.Surface): game screen surface.
        """
        font = pygame.font.Font(None, 70)

        text = font.render("Game Over", True, pygame.Color("gray"))
        text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))

        screen.blit(text, text_rect)  # Draw text on screen

    @staticmethod
    def draw_score(screen, collected_count, poisonous_count):
        """
        Draw the score on the screen.

        Args:
            screen (pygame.Surface): game screen surface.
            collected_count (int): number of collected mushrooms.
            poisonous_count (int): number of poisonous mushrooms collected.
        """
        font = pygame.font.Font(None, 45)

        text = font.render(f"Count: {collected_count} Poisonous: {poisonous_count}",
                           True, pygame.Color("purple"))
        text_rect = text.get_rect(topright=(690, 15))

        pygame.draw.rect(screen, pygame.Color("lightblue"), text_rect)
        screen.blit(text, text_rect)


class Game:
    """
    Manages the game logic.
    """

    def __init__(self):
        """
        Initialize the game.
        """
        pygame.init()  # Initialize Pygame
        self.screen = pygame.display.set_mode((700, 550))  # Create game screen
        pygame.display.set_caption("Mushroom Collector")  # Set window title
        self.clock = pygame.time.Clock()  # Create clock object
        self.dt = 0  # Delta time for frame rate independence
        self.fps = 60  # Frames per second
        self.run = True  # Flag to control game loop
        self.collected_count = 0
        self.poisonous_count = 0
        self.initial_fall_speed = 150
        self.fall_speed_increment = 1
        self.basket = Character(os.path.join('assets', 'collection_basket.png'),
                                (self.screen.get_width() / 2 - 66, 430))

        self.characters = [
            Character(os.path.join('assets', 'mushroom.png'),
                      (random.randint(0, self.screen.get_width() - self.basket.position.width),
                       -self.basket.position.height)),

            Character(os.path.join('assets', 'poisonous_mushroom.png'),
                      (random.randint(0, self.screen.get_width() - self.basket.position.width),
                       -self.basket.position.height)),

            Character(os.path.join('assets', 'mushroom2.png'),
                      (random.randint(0, self.screen.get_width() - self.basket.position.width),
                       -self.basket.position.height))
        ]

        self.sounds = {
            "mushroom_collected": pygame.mixer.Sound(os.path.join('assets', 'mushrooms_collected.wav')),
            "poisonous_warning": pygame.mixer.Sound(os.path.join('assets', 'poisonous_warning.wav')),
            "game_over": pygame.mixer.Sound(os.path.join('assets', 'game_over.wav'))
        }

    def produce_character(self, character):
        """
        Produce a new character if it goes out of the screen.

        Args:
            character (Character): character object to produce.
        """
        if character.position.y > self.screen.get_height():
            character.position.topleft = pygame.Vector2(
                random.randint(0, self.screen.get_width() - character.position.width),
                -character.position.height)

    def handle_collision(self, character):
        """
        Handle collision between characters.

        Args:
            character (Character): character involved in the collision.
        """
        if self.basket.position.colliderect(character.position):
            if character.image == self.characters[0].image:
                self.collected_count += 1
                self.sounds["mushroom_collected"].play()
                if self.collected_count % 5 == 0:
                    self.fall_speed_increment += 10
            elif character.image == self.characters[2].image:
                self.collected_count += 1
                self.sounds["mushroom_collected"].play()
                if self.collected_count % 5 == 0:
                    self.fall_speed_increment += 10
            elif character.image == self.characters[1].image:
                self.poisonous_count += 1
                self.sounds["poisonous_warning"].play()
                if self.poisonous_count == 5:
                    self.sounds["game_over"].play()
            character.position.topleft = pygame.Vector2(
                random.randint(0, self.screen.get_width() - character.position.width),
                -character.position.height)

    def run_game(self):
        """
        Run the main game loop.
        """
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.basket.position.x -= 300 * self.dt
            elif keys[pygame.K_RIGHT]:
                self.basket.position.x += 300 * self.dt

            for char in self.characters:
                char.position.y += (self.initial_fall_speed + self.fall_speed_increment * (self.collected_count // 5)) * self.dt
                self.handle_collision(char)
                self.produce_character(char)

            if self.poisonous_count == 5:
                Info.game_over_message(self.screen)
                pygame.display.update()
                pygame.time.delay(3000)
                self.run = False

            self.screen.fill(pygame.Color("lightgreen"))
            self.screen.blit(self.basket.image, self.basket.position)
            for char in self.characters:
                self.screen.blit(char.image, char.position)

            Info.draw_score(self.screen, self.collected_count, self.poisonous_count)

            pygame.display.flip()
            self.dt = self.clock.tick(self.fps) / 1000
            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run_game()
