"""
Mushroom Collector game that AI plays

This project implements a simple game called Mushroom Collector using the NEAT (NeuroEvolution of Augmenting
Topologies) algorithm that creates artificial neural networks.
In this game, the player controls a basket to collect mushrooms falling. The goal is to collect mushrooms
avoiding poisonous ones.

The game consists of three main classes:
- Character: Represents the game characters, including the basket and mushrooms.
- Info: Manages displaying game information such as the score and game over message.
- Game: Manages the game logic including character movement, collision detection, and NEAT implementation.

NEAT is a method for evolving artificial neural networks with genetic algorithms and is used to evolve neural networks
to control the movement of the basket based on the position of the mushrooms in this game.

The project also includes a 'run' function to execute the NEAT algorithm for the Mushroom Collector game using
provided neat configuration file.
"""

import pygame
import random
import neat
import os


class Character:

    def __init__(self, image_path, initial_position):
        """
        Initialize the character.

        Args:
            image_path (str): path to the character's image.
            initial_position (tuple): initial position of the character (x, y).
        """
        self.image = pygame.image.load(image_path)
        self.position = self.image.get_rect(topleft=initial_position)


class Info:

    @staticmethod
    def game_over_message(screen):
        """ Display game over message on the screen.

        Args:
            screen (pygame.Surface): surface to render the message on.
        """
        font = pygame.font.Font(None, 70)

        text = font.render("Game Over", True, pygame.Color("gray"))
        text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))

        screen.blit(text, text_rect)

    @staticmethod
    def draw_score(screen, collected_count, poisonous_count):
        """ Draw the current score on the screen.

        Args:
            screen (pygame.Surface): surface to render the score on.
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

    def __init__(self):
        """ Initialize the game variables. """
        pygame.init()
        self.screen = pygame.display.set_mode((700, 550))
        pygame.display.set_caption("Mushroom Collector")
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.fps = 60
        self.run = True
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
        """ Produce a character when it goes out of the screen.

        Args:
            character (Character): character to produce.
        """
        if character.position.y > self.screen.get_height():
            character.position.topleft = pygame.Vector2(
                random.randint(0, self.screen.get_width() - character.position.width),
                -character.position.height)

    def handle_collision(self, character):
        """ Handle collision between the basket and characters.

        Args:
            character (Character): character involved in the collision.
        """
        if self.basket.position.colliderect(character.position):
            if character.image == self.characters[0].image:
                self.collected_count += 1
                self.sounds["mushroom_collected"].play()
                if self.collected_count % 5 == 0:
                    # Increase falling speed when mushroom is collected
                    self.fall_speed_increment += 10
            elif character.image == self.characters[2].image:
                self.collected_count += 1
                self.sounds["mushroom_collected"].play()
                if self.collected_count % 5 == 0:
                    # Increase falling speed when mushroom2 is collected
                    self.fall_speed_increment += 10
            elif character.image == self.characters[1].image:
                self.poisonous_count += 1
                self.sounds["poisonous_warning"].play()
                if self.poisonous_count == 5:
                    self.sounds["game_over"].play()
            character.position.topleft = pygame.Vector2(
                random.randint(0, self.screen.get_width() - character.position.width),
                -character.position.height)

    @staticmethod
    def run_game(genomes, config):
        """ Run the game using NEAT.

        Args:
            genomes (list): list of genomes provided by neat.
            config (neat.Config): neat configuration.
        """
        nets = []
        ge = []
        basket = Character(os.path.join('assets', 'collection_basket.png'), (300, 430))
        num_nets = 0

        for _, genome in genomes:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
            genome.fitness = 0
            ge.append(genome)
            num_nets += 1

        # Initialize game objects
        mushrooms = [
            Character(os.path.join('assets', 'mushroom.png'),
                      (random.randint(0, 700 - 132), random.randint(-550, -132))),
            Character(os.path.join('assets', 'poisonous_mushroom.png'),
                      (random.randint(0, 700 - 132), random.randint(-550, -132))),
            Character(os.path.join('assets', 'mushroom2.png'),
                      (random.randint(0, 700 - 132), random.randint(-550, -132)))
        ]

        pygame.init()
        screen = pygame.display.set_mode((700, 550))
        pygame.display.set_caption("Mushroom Collector")
        clock = pygame.time.Clock()
        run = True
        collected_count = 0
        poisonous_count = 0
        initial_fall_speed = 50
        fall_speed_increment = 1

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()

            # Move the basket according to the AI decisions
            output = nets[0].activate((basket.position.x, mushrooms[0].position.x, mushrooms[0].position.y))
            if output[0] < 0.5:
                basket.position.x -= 5  # Move left
            elif output[0] > 0.5:
                basket.position.x += 5  # Move right

            # Update game objects
            for mushroom in mushrooms:
                mushroom.position.y += initial_fall_speed * 0.01 * num_nets  # Adjust fall speed based on number of nets
                if mushroom.position.y > 550:
                    mushroom.position.y = random.randint(-550, -132)
                    mushroom.position.x = random.randint(0, 700 - 132)
                if basket.position.colliderect(mushroom.position):
                    ge[0].fitness += 1
                    if mushroom.image == mushrooms[0].image or mushroom.image == mushrooms[2].image:
                        collected_count += 1
                        if collected_count % 5 == 0:
                            fall_speed_increment += 10
                    else:
                        poisonous_count += 1
                        if poisonous_count == 5:
                            run = False

            # Draw game objects
            screen.fill(pygame.Color("lightgreen"))
            screen.blit(basket.image, basket.position)
            for mushroom in mushrooms:
                screen.blit(mushroom.image, mushroom.position)
            Info.draw_score(screen, collected_count, poisonous_count)

            pygame.display.flip()
            clock.tick(30)


def run(config_file):
    """ Run the algorithm.

    Args:
        config_file (str): path to the neat configuration file.
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(Game.run_game, 50)
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat-config.txt')
    run(config_path)
