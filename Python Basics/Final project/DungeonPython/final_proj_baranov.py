import pygame
from pygame.sprite import Sprite
import sys
import random


class DungeonAndPythons:
    """Manage a game"""

    def __init__(self) -> None:
        """
        Initialize a game. Creating Hero and Monster
        And other parameters
        """
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Dungeon'n'Pythons")
        self.fpsClock = pygame.time.Clock()
        self.hero_class = 'warrior'

        self.hero = Hero(self, self.hero_class)
        self.monster = Monster(self)
        self.bottles = pygame.sprite.Group()
        self.arrows = pygame.sprite.Group()

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        self.font_stats = pygame.font.SysFont(None, 24)
        self.font_help = pygame.font.SysFont(None, 14)

        #  Make the play button
        self.play_button = Button(self, "Play ('p')")

        #  Make difficulty buttons
        self.easy_button = DifficultyButton(self, "Easy", "topright")
        self.medium_button = DifficultyButton(self, "Medium", "midright")
        self.hard_button = DifficultyButton(self, "Hard", "bottomright")

        # Hero buttons
        self.warrior_button = HeroButton(self, "Warrior", "midleft")
        self.archer_button = HeroButton(self, "Archer", "bottomleft")

        self.game_active = False

    def _create_bottles(self):
        """
            Creates and places bottles which could be collected
            by the hero. Bottles affect hp, damage and defense parameters
        """
        for color in {'red', 'yellow', 'blue'}:
            for _ in range(3):
                bottle = Bottle(self, color)
                max_x = self.screen.get_rect().width - bottle.rect.width
                max_y = self.screen.get_rect().height - bottle.rect.height

                bottle.rect.x = random.randint(0, max_x)
                bottle.rect.y = random.randint(0, max_y)

                #  start each new alien near random place of the screen
                while bottle.rect.colliderect(self.hero) \
                        or bottle.rect.colliderect(self.monster) \
                        or pygame.sprite.spritecollideany(bottle, self.bottles):
                    bottle.rect.x = random.randint(0, max_x)
                    bottle.rect.y = random.randint(0, max_y)

                self.bottles.add(bottle)

    def _start_game(self):
        """
           Initialize the basic game parameters
           Cleans the screen from previous game session
        """
        self.settings.initialize_dynamic_settings()
        self.game_active = True
        self.bottles.empty()
        self.arrows.empty()
        self._create_bottles()
        self.hero = Hero(self, self.hero_class)
        self.monster = Monster(self)
        pygame.mouse.set_visible(False)
        self.run_game()

    def run_game(self):
        """
            Manages main loop for the game
        """
        while True:
            # 60 fps lock
            self.fpsClock.tick(60)
            self._check_events()
            if self.game_active:
                self.hero.update()
                self.monster.update(self)
                self.arrows.update()
                self._update_arrows()
                hp_check = self._check_hp()
                if hp_check is None:
                    pass
                else:
                    self.game_active = False
                    pygame.mouse.set_visible(True)
            self.update_screen()

    def _check_events(self):
        """
            Respond to key presses and mouse events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        """
            Process mouse clicks on buttons
        """
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if not self.game_active:
            if button_clicked:
                self._start_game()
            elif self.easy_button.rect.collidepoint(mouse_pos):
                self.settings.difficulty = "easy"
            elif self.medium_button.rect.collidepoint(mouse_pos):
                self.settings.difficulty = "medium"
            elif self.hard_button.rect.collidepoint(mouse_pos):
                self.settings.difficulty = "hard"
            elif self.warrior_button.rect.collidepoint(mouse_pos):
                self.hero_class = 'warrior'
            elif self.archer_button.rect.collidepoint(mouse_pos):
                self.hero_class = 'archer'

    def _check_keydown_events(self, event):
        """
            Process keyboard keys interaction
        """
        if not self.game_active and event.key == pygame.K_p:
            self._start_game()
        elif event.key == pygame.K_RIGHT:
            self.hero.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.hero.moving_left = True
        elif event.key == pygame.K_UP:
            self.hero.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.hero.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self.hero.attack(self.monster)
            if self.hero_class == 'archer':
                self._fire_arrow()
        elif event.key == pygame.K_LCTRL:
            self.hero.defense()
        elif event.key == pygame.K_h:
            # health bottle
            self.hero.use_bottle('red')
        elif event.key == pygame.K_a:
            # damage blue
            self.hero.use_bottle('blue')
        elif event.key == pygame.K_d:
            # defense yellow
            self.hero.use_bottle('yellow')

    def _check_keyup_events(self, event):
        """
            Process finish of pressing keyboard keys
        """
        if event.key == pygame.K_RIGHT:
            self.hero.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.hero.moving_left = False
        elif event.key == pygame.K_UP:
            self.hero.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.hero.moving_down = False
        elif event.key == pygame.K_SPACE:
            self.hero.attack_finished()
        elif event.key == pygame.K_LCTRL:
            self.hero.defense_finished()

    def update_screen(self):
        """
            Update images on the screen, and flip to the new screen.
        """
        self.screen.fill(self.settings.bg_color)
        self.hero.blitme()
        self.monster.blitme()

        # checks hp of hero/monsters to display message
        self._check_hp()

        self._check_hero()
        self._check_monster()
        self._render_help()
        for arrow in self.arrows.sprites():
            arrow.draw_arrow()

        self.bottles.draw(self.screen)
        self.hero.check_bottle_col(self)
        self.hero.draw_hero_bottles(self)

        #  Draw buttons if game is inactive
        if not self.game_active:
            self.play_button.draw_button()
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()
            self.warrior_button.draw_button()
            self.archer_button.draw_button()

        #  Make the most recently drawn screen visible.
        pygame.display.flip()

    def _check_hp(self):
        """
            Checks the remaining hero/monster HP
            If <=0, game finishes
        """
        self.message = ''
        if self.settings.monster_hp <= 0:
            self.message = 'YOU WON!'
            self.monster.image = self.monster.lost_image
        elif self.settings.hero_hp <= 0:
            self.message = 'YOU LOST...'
            self.hero.image = self.hero.lost_image
        if self.message:
            self.final_message = self.font.render(self.message, True,
                                                  self.text_color, self.settings.bg_color)
            self.message_rect = self.final_message.get_rect()
            self.message_rect.center = self.screen.get_rect().center
            self.message_rect.y += 50
            self.screen.blit(self.final_message, self.message_rect)
            return True
        return None

    def _check_hero(self):
        """
            Check and display hero current stats
        """
        text = 'HERO '
        text += f'HP:{self.settings.hero_hp} '
        text += f'Damage:{self.settings.hero_damage} '
        text += f'Defense:{self.settings.hero_defense} '

        message = self.font_stats.render(text, True,
                                         self.text_color, self.settings.bg_color)
        message_rect = message.get_rect()
        message_rect.bottomleft = self.screen.get_rect().bottomleft
        self.screen.blit(message, message_rect)

    def _check_monster(self):
        """
            Check and display monster current stats
        """
        text = 'MONSTER '
        text += f'HP:{self.settings.monster_hp} '
        text += f'Damage:{self.settings.monster_damage} '
        # text += f'Defense: {self.settings}\n'

        message = self.font_stats.render(text, True,
                                         self.text_color, self.settings.bg_color)
        message_rect = message.get_rect()
        message_rect.bottomright = self.screen.get_rect().bottomright
        self.screen.blit(message, message_rect)

    def _render_help(self):
        """
            Renders help for control keys
        """
        help_text = [
            '(SPACE) for attack',
            '(LCtrl) for defense',
            '(H) for health (red) bottle',
            '(D) for defense (yellow) bottle',
            '(A) for damage (blue) bottle',
            '(Q) for exit'
        ]
        count = 0
        for line in help_text:
            message = self.font_help.render(line, True,
                                            self.text_color, self.settings.bg_color)
            message_rect = message.get_rect()
            message_rect.topleft = self.screen.get_rect().topleft
            message_rect.y += 31 + count * 14
            count += 1
            self.screen.blit(message, message_rect)

    def _fire_arrow(self):
        """
            Creates new arrow and add it to the group
        """
        if len(self.arrows) < self.settings.arrows_allowed:
            new_arrow = Arrow(self)
            self.arrows.add(new_arrow)

    def _update_arrows(self):
        """
            Update position and delete old arrows
        """
        self.arrows.update()

        for arrow in self.arrows.copy():
            if arrow.rect.right > self.screen.get_rect().right:
                self.arrows.remove(arrow)

        self._check_bullet_monster_collision()

    def _check_bullet_monster_collision(self):
        """
            Check collision between any arrow and monster
            Does damage to the monster and deletes arrow
        """
        if pygame.sprite.spritecollideany(self.monster, self.arrows):
            collisions = pygame.sprite.spritecollide(self.monster, self.arrows, True)
            self.arrows.remove(collisions.pop())
            self.monster.settings.monster_hp -= self.hero.settings.hero_damage
            if self.monster.settings.monster_hp < 0:
                self.monster.settings.monster_hp = 0


class Hero(Sprite):
    """Hero class"""

    def __init__(self, dnp_game, hero_class='warrior') -> None:
        """
            Initialize base parameters for the hero
        """
        super().__init__()
        self.screen = dnp_game.screen
        self.screen_rect = dnp_game.screen.get_rect()
        self.settings = dnp_game.settings

        #  Load the hero image and get its rect.
        if hero_class == 'warrior':
            self.basic_image = pygame.image.load('images/hero.png')
            self.image = self.basic_image
            self.attack_image = pygame.image.load('images/hero_attacks.png')
            self.defense_image = pygame.image.load('images/hero_defend.png')
            self.lost_image = pygame.image.load('images/hero_lost.png')
        elif hero_class == 'archer':
            self.basic_image = pygame.image.load('images/archer.png')
            self.image = self.basic_image
            self.attack_image = pygame.image.load('images/archer_attacks.png')
            self.defense_image = pygame.image.load('images/archer_defend.png')
            self.lost_image = pygame.image.load('images/archer_lost.png')

        # self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()

        #  Start new hero at the left of the screen
        self.rect.midleft = self.screen_rect.midleft

        #  Store a decimal value for the hero's speed
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # movement and defending flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.defending = False

        # hero inventory bottles
        self.hero_bottles = pygame.sprite.Group()
        self.bottles_max = 3
        self.hero_class = hero_class

    def blitme(self):
        """
            Draw the hero at its current location.
        """
        self.screen.blit(self.image, self.rect)

    def update(self):
        """
            Update the hero's position based on movement flags.
        """
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.hero_speed
        elif self.moving_left and self.rect.left > 0:
            self.x -= self.settings.hero_speed
        elif self.moving_up and self.rect.top > 0:
            self.y -= self.settings.hero_speed
        elif self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.hero_speed

        #  Update rect
        self.rect.x = self.x
        self.rect.y = self.y

    def attack(self, monster):
        """
            When monster's sprite is collided
            Does damage to the monster if hero is warrior
            Else just changes the hero image
        """
        # change image
        self.image = self.attack_image
        if self.hero_class == 'warrior':
            # check if the monster nearby, calculate damage
            if self.rect.colliderect(monster) and monster.settings.monster_hp > 0:
                monster.settings.monster_hp -= self.settings.hero_damage
            if monster.settings.monster_hp < 0:
                monster.settings.monster_hp = 0

    def attack_finished(self):
        """
            Finishes attack
            Return basic image
        """
        self.image = self.basic_image

    def defense(self):
        """
            Set defending flag
            And changes image
        """
        self.image = self.defense_image
        # only when defending defense points are applicable
        self.defending = True

    def defense_finished(self):
        """
            Back to the normal image and False flag
            when the defense is finished
        """
        self.image = self.basic_image
        self.defending = False

    def check_bottle_col(self, dnp_game):
        """
            Checks if hero collided with any bottle
            Adds it to the hero inventory if it doesn't surpass max capacity
        """
        if len(self.hero_bottles) < self.bottles_max \
                and pygame.sprite.spritecollideany(self, dnp_game.bottles):
            collisions = pygame.sprite.spritecollide(self, dnp_game.bottles, True)
            bottle_color = collisions.pop().color

            hero_bottle = Bottle(self, bottle_color, size=(20, 30))
            self.hero_bottles.add(hero_bottle)
            self.draw_hero_bottles(dnp_game)

    def draw_hero_bottles(self, dnp_game):
        """
            Draws hero inventory bottles
        """
        count = 1
        for bottle in self.hero_bottles:
            bottle.rect.top = dnp_game.screen.get_rect().top
            bottle.rect.x = 3 + (count * bottle.rect.width + 1)
            count += 1
        self.hero_bottles.draw(dnp_game.screen)

    def use_bottle(self, color):
        """
            If specific bottle used
            It affects some parameters
            Afterward bottle is removed from screen
        """
        for bottle in self.hero_bottles:
            if bottle.color == color:
                if color == 'red':
                    self.settings.hero_hp += self.settings.hp_effect
                elif color == 'blue':
                    self.settings.hero_damage += self.settings.damage_effect
                elif color == 'yellow':
                    self.settings.hero_defense += self.settings.defense_effect
                self.hero_bottles.remove(bottle)
                break


class Monster(Sprite):
    def __init__(self, dnp_game) -> None:
        """
            Initialize monster basic parameters
        """
        super().__init__()
        self.screen = dnp_game.screen
        self.screen_rect = dnp_game.screen.get_rect()
        self.settings = dnp_game.settings

        #  Load the image and get its rect.
        self.basic_image = pygame.image.load('images/snake.png')
        self.image = self.basic_image
        self.attack_image = pygame.image.load('images/snake_attacks.png')
        self.lost_image = pygame.image.load('images/snake_lost.png')
        self.attacking = False

        # self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()

        #  Start each new monster at the right of the screen
        self.rect.midright = self.screen_rect.midright

        #  Store a decimal value for the monster's speed
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def attack(self, hero):
        """
            Monster attack method
            It can only attack with the specific damage
        """
        self.image = self.attack_image
        # calculate damage
        if hero.settings.hero_hp <= 0:
            return
        if hero.defending:
            if hero.settings.hero_defense < self.settings.monster_damage:
                hero.settings.hero_hp -= (self.settings.monster_damage - hero.settings.hero_defense)
        else:
            hero.settings.hero_hp -= self.settings.monster_damage
        if hero.settings.hero_hp < 0:
            hero.settings.hero_hp = 0

    def attack_finished(self):
        """
            Return to the basic image when attack finishes
        """
        self.image = self.basic_image

    def update(self, dnp_game):
        """
            Updates monster positions
            Makes it move in direction of the hero
            with the specific speed
        """
        hero_x = dnp_game.hero.rect.x
        hero_y = dnp_game.hero.rect.y
        mnst_speed = dnp_game.settings.monster_speed

        # check case when hero is near
        # attack!
        if self.rect.colliderect(dnp_game.hero):
            self.attack(dnp_game.hero)
            # screen update
            dnp_game.update_screen()
            pygame.time.delay(200)
            self.attack_finished()
        else:
            if self.x < hero_x:
                self.x += mnst_speed
            elif self.x > hero_x:
                self.x -= mnst_speed
            if self.y < hero_y:
                self.y += mnst_speed
            elif self.y > hero_y:
                self.y -= mnst_speed

        #  Update rect
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """
            Draw the monster at its current location.
        """
        self.screen.blit(self.image, self.rect)


class Settings:
    """
        Game settings class
        Mainly to eliminate "magic numbers"
    """

    def __init__(self) -> None:
        # None will be set in dynamic settings
        self.monster_speed = None
        self.monster_damage = None
        self.hero_defense = None
        self.hero_damage = None
        self.monster_hp = None
        self.hero_hp = None
        self.hero_speed = None
        # game settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.difficulty = "easy"
        # inventory settings
        self.max_inv = 3
        # bottle settings
        self.hp_effect = 20
        self.damage_effect = 5
        self.defense_effect = 5
        # arrow settings
        self.arrow_width = 15
        self.arrow_height = 3
        self.arrow_color = (60, 60, 60)
        self.arrows_allowed = 3
        self.arrow_speed = 3.0
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """
            Dynamic settings for different difficulty
            And also refreshes HP for hero/monster for the new session
        """
        # hero settings
        self.hero_speed = 4
        self.hero_hp = 100
        # monster settings
        self.monster_hp = 100

        """change settings according to the difficulty"""
        if self.difficulty == "easy":
            self.hero_damage = 10
            self.hero_defense = 5
            self.monster_damage = 3
            self.monster_speed = 1
        elif self.difficulty == "medium":
            self.hero_damage = 7
            self.hero_defense = 3
            self.monster_damage = 5
            self.monster_speed = 1.5
        elif self.difficulty == "hard":
            self.hero_damage = 5
            self.hero_defense = 2
            self.monster_damage = 7
            self.monster_speed = 2


class Bottle(Sprite):
    """
        Bottles that could be collected
        Placed on the game field or in the inventory
        Affect different hero parameters
    """

    def __init__(self, dnp_game, color_name='red', size=(40, 60)) -> None:
        """
            initializes a bottle of a color with a size
        """
        super().__init__()
        self.screen = dnp_game.screen
        self.settings = dnp_game.settings
        self.color = color_name

        self.image = pygame.image.load(f'images/{color_name}_bottle.png')
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()


class Button:
    """
        Clickable buttons class
    """

    def __init__(self, dnp_game, msg):
        """
            initialize attributes for button
        """
        self.screen = dnp_game.screen
        self.screen_rect = self.screen.get_rect()

        #  Set the dimensions and properties of the button
        self.width, self.height = 200, 50
        self.button_color = (0, 0, 0)
        self.text_color = (192, 192, 192)
        self.font = pygame.font.SysFont(None, 48)

        #  Build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        #  The button message
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """
            Turn msg into a rendered image and center text on the button
        """
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """
            Draw a blank button and then draw message
        """
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


class DifficultyButton(Button):
    """Class for the specific button for the difficulty"""

    def __init__(self, dnp_game, msg, location):
        super().__init__(dnp_game, msg)
        if location == "topright":
            self.rect.topright = self.screen_rect.topright
        elif location == "midright":
            self.rect.midright = self.screen_rect.midright
        elif location == "bottomright":
            self.rect.bottomright = self.screen_rect.bottomright
            # by the stats font up
            self.rect.y -= 24
        self._prep_msg(msg)


class HeroButton(Button):
    """Specific hero class choice button"""

    def __init__(self, dnp_game, msg, location):
        super().__init__(dnp_game, msg)
        if location == 'midleft':
            self.rect.midleft = self.screen_rect.midleft
        elif location == 'bottomleft':
            self.rect.bottomleft = self.screen_rect.bottomleft
            # by the stats font up
            self.rect.y -= 24
        self._prep_msg(msg)


class Arrow(Sprite):
    """
        Manages arrow object at the archer current position
        For archer hero class only
    """

    def __init__(self, dnp_game):
        """
            Initialize the arrow and sets basic parameters
        """
        super().__init__()
        self.screen = dnp_game.screen
        self.settings = dnp_game.settings
        # self.color = self.settings.arrow_color
        self.image = pygame.image.load('images/arrow.png')
        self.rect = self.image.get_rect()

        # create an arrow rect at (0, 0) and set correct position
        self.rect = pygame.Rect(0, 0, self.settings.arrow_width,
                                self.settings.arrow_height)
        self.rect.midleft = dnp_game.hero.rect.midright
        self.rect.y -= 15

        #  Store arrow's position
        self.x = float(self.rect.x)

    def update(self):
        """
            Move arrow right to the screen edge
        """
        #  Update the decimal postition
        self.x += self.settings.arrow_speed

        #  Update the rect
        self.rect.x = self.x

    def draw_arrow(self):
        """
            Draws the arrow to the screen
        """
        # pygame.draw.rect(self.screen, self.color, self.rect)
        self.screen.blit(self.image, self.rect)


if __name__ == '__main__':
    #  Make a game instance, and run the game.
    dnp = DungeonAndPythons()
    dnp.run_game()
