import pygame
import random
import json
import os
import math

pygame.init()

# ============================================================
# SETTINGS
# ============================================================

WIDTH = 1100
HEIGHT = 700
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sword Adventure")

clock = pygame.time.Clock()

FONT = pygame.font.SysFont("arial", 24)
SMALL = pygame.font.SysFont("arial", 17)
BIG = pygame.font.SysFont("arial", 48)
HUGE = pygame.font.SysFont("arial", 62)

SAVE_FILE = "sword_save.json"


# ============================================================
# COLORS
# ============================================================

WHITE = (245, 245, 245)
BLACK = (15, 15, 15)

RED = (220, 60, 60)
DARK_RED = (120, 20, 20)

GREEN = (50, 200, 80)
DARK_GREEN = (30, 110, 50)

BLUE = (60, 130, 230)
DARK_BLUE = (25, 55, 120)

GOLD = (240, 190, 40)

GRAY = (120, 120, 120)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (55, 55, 55)

BROWN = (125, 75, 35)

PURPLE = (150, 60, 200)

ORANGE = (245, 120, 30)

CYAN = (100, 220, 255)

YELLOW = (255, 235, 80)

PINK = (235, 80, 180)


# ============================================================
# CHARACTERS
# ============================================================

characters = {

    "Knight": {

        "hp_bonus": 40,
        "speed_bonus": -0.5,
        "color": LIGHT_GRAY,

        "abilities": {

            "Z": {
                "name": "Shield Rush",
                "cooldown": 4 * FPS
            },

            "X": {
                "name": "Ground Slam",
                "cooldown": 6 * FPS
            },

            "C": {
                "name": "Berserk",
                "cooldown": 10 * FPS
            }
        }
    },

    "Ranger": {

        "hp_bonus": 0,
        "speed_bonus": 1.0,
        "color": GREEN,

        "abilities": {

            "Z": {
                "name": "Triple Shot",
                "cooldown": 3 * FPS
            },

            "X": {
                "name": "Dash",
                "cooldown": 4 * FPS
            },

            "C": {
                "name": "Arrow Storm",
                "cooldown": 10 * FPS
            }
        }
    },

    "Mage": {

        "hp_bonus": -10,
        "speed_bonus": 0,
        "color": PURPLE,

        "abilities": {

            "Z": {
                "name": "Fireball",
                "cooldown": 3 * FPS
            },

            "X": {
                "name": "Freeze Blast",
                "cooldown": 5 * FPS
            },

            "C": {
                "name": "Lightning Nova",
                "cooldown": 9 * FPS
            }
        }
    },

    "Shadow": {

        "hp_bonus": -20,
        "speed_bonus": 1.5,
        "color": DARK_GRAY,

        "abilities": {

            "Z": {
                "name": "Teleport Strike",
                "cooldown": 3 * FPS
            },

            "X": {
                "name": "Vanish",
                "cooldown": 6 * FPS
            },

            "C": {
                "name": "Spin Attack",
                "cooldown": 8 * FPS
            }
        }
    }
}


# ============================================================
# SWORDS
# ============================================================

weapons = {

    "Wood Sword": {
        "damage": 15,
        "price": 0
    },

    "Iron Sword": {
        "damage": 25,
        "price": 150
    },

    "Knight Sword": {
        "damage": 40,
        "price": 450
    },

    "Fire Sword": {
        "damage": 65,
        "price": 1100
    },

    "Demon Sword": {
        "damage": 95,
        "price": 2300
    },

    "Dragon Blade": {
        "damage": 140,
        "price": 5000
    }
}


# ============================================================
# BOWS
# ============================================================

bows = {

    "Wood Bow": {
        "damage": 10,
        "speed": 9,
        "price": 0
    },

    "Hunter Bow": {
        "damage": 22,
        "speed": 10,
        "price": 250
    },

    "Fire Bow": {
        "damage": 42,
        "speed": 11,
        "price": 950
    },

    "Demon Bow": {
        "damage": 65,
        "speed": 12,
        "price": 2200
    },

    "Dragon Bow": {
        "damage": 90,
        "speed": 14,
        "price": 4200
    }
}


# ============================================================
# ARMOR
# ============================================================

armors = {

    "Cloth Armor": {
        "defense": 0,
        "price": 0
    },

    "Leather Armor": {
        "defense": 3,
        "price": 120
    },

    "Iron Armor": {
        "defense": 7,
        "price": 350
    },

    "Knight Armor": {
        "defense": 13,
        "price": 850
    },

    "Demon Armor": {
        "defense": 20,
        "price": 1900
    },

    "Dragon Armor": {
        "defense": 30,
        "price": 4500
    }
}


# ============================================================
# ARROWS
# ============================================================

arrow_types = {

    "regular": {

        "price": 0,
        "damage_bonus": 0,
        "speed_bonus": 0,

        "homing": False,

        "burn_damage": 0,
        "burn_time": 0,

        "explosion_radius": 0,

        "lightning_radius": 0,

        "description": "Normal arrow"
    },


    "lightning": {

        "price": 1200,
        "damage_bonus": 15,
        "speed_bonus": 3,

        "homing": False,

        "burn_damage": 0,
        "burn_time": 0,

        "explosion_radius": 0,

        "lightning_radius": 170,

        "description": "Chain lightning"
    },


    "exploding": {

        "price": 1800,
        "damage_bonus": 10,
        "speed_bonus": -1,

        "homing": False,

        "burn_damage": 0,
        "burn_time": 0,

        "explosion_radius": 135,

        "lightning_radius": 0,

        "description": "Explosion damage"
    },


    "homing": {

        "price": 2400,
        "damage_bonus": 20,
        "speed_bonus": 0,

        "homing": True,

        "burn_damage": 0,
        "burn_time": 0,

        "explosion_radius": 0,

        "lightning_radius": 0,

        "description": "Tracks enemies"
    },


    "fire": {

        "price": 3000,
        "damage_bonus": 18,
        "speed_bonus": 1,

        "homing": False,

        "burn_damage": 5,
        "burn_time": 240,

        "explosion_radius": 0,

        "lightning_radius": 0,

        "description": "Burn damage"
    },


    "super": {

        "price": 8000,
        "damage_bonus": 55,
        "speed_bonus": 3,

        "homing": True,

        "burn_damage": 8,
        "burn_time": 300,

        "explosion_radius": 190,

        "lightning_radius": 220,

        "description": "Homing + explosion + fire + lightning"
    }
}


# ============================================================
# UTILITIES
# ============================================================

utilities = {

    "Ender Pearl": {

        "price": 700,
        "type": "teleport"
    },

    "Iron Hammer": {

        "price": 900,
        "type": "hammer",

        "damage": 80,
        "range": 150
    },

    "Demon Hammer": {

        "price": 2200,
        "type": "hammer",

        "damage": 140,
        "range": 180
    },

    "Dragon Hammer": {

        "price": 4800,
        "type": "hammer",

        "damage": 220,
        "range": 220
    }
}


# ============================================================
# LEVELS
# ============================================================

levels = {

    1: {

        "name": "Green Plains",

        "background": (45, 110, 55),

        "enemy_hp": 45,
        "enemy_damage": 7,
        "enemy_count": 5,

        "ranged_chance": 0.15,

        "boss_name": "Goblin King",

        "boss_hp": 220,
        "boss_damage": 14
    },


    2: {

        "name": "Dark Forest",

        "background": (28, 70, 38),

        "enemy_hp": 70,
        "enemy_damage": 10,
        "enemy_count": 6,

        "ranged_chance": 0.25,

        "boss_name": "Forest Troll",

        "boss_hp": 350,
        "boss_damage": 18
    },


    3: {

        "name": "Frozen Fortress",

        "background": (65, 105, 140),

        "enemy_hp": 100,
        "enemy_damage": 13,
        "enemy_count": 7,

        "ranged_chance": 0.35,

        "boss_name": "Ice Knight",

        "boss_hp": 500,
        "boss_damage": 22
    },


    4: {

        "name": "Volcano",

        "background": (100, 42, 24),

        "enemy_hp": 140,
        "enemy_damage": 18,
        "enemy_count": 8,

        "ranged_chance": 0.42,

        "boss_name": "Fire Demon",

        "boss_hp": 750,
        "boss_damage": 28
    },


    5: {

        "name": "Dragon Temple",

        "background": (55, 30, 70),

        "enemy_hp": 190,
        "enemy_damage": 24,
        "enemy_count": 10,

        "ranged_chance": 0.50,

        "boss_name": "Ancient Dragon",

        "boss_hp": 1200,
        "boss_damage": 35
    }
}


# ============================================================
# PLAYER DATA
# ============================================================

default_data = {

    "gold": 300,

    "xp": 0,

    "player_level": 1,

    "max_hp": 100,

    "character": "Knight",

    "weapon": "Wood Sword",

    "bow": "Wood Bow",

    "armor": "Cloth Armor",

    "weapon_mode": "sword",

    "arrow_type": "regular",

    "utility": "",

    "owned_weapons": [
        "Wood Sword"
    ],

    "owned_bows": [
        "Wood Bow"
    ],

    "owned_armors": [
        "Cloth Armor"
    ],

    "owned_arrows": [
        "regular"
    ],

    "owned_utilities": [],

    "potions": 3,

    "unlocked_level": 1
}

player_data = {}


# ============================================================
# SAVE SYSTEM
# ============================================================

def fresh_data():

    result = {}

    for key, value in default_data.items():

        if isinstance(value, list):

            result[key] = value.copy()

        else:

            result[key] = value

    return result


def save_game():

    with open(
        SAVE_FILE,
        "w"
    ) as file:

        json.dump(
            player_data,
            file,
            indent=4
        )


def load_game():

    global player_data

    player_data = fresh_data()

    if not os.path.exists(
        SAVE_FILE
    ):

        return

    try:

        with open(
            SAVE_FILE,
            "r"
        ) as file:

            saved = json.load(
                file
            )

        player_data.update(
            saved
        )


        player_data.setdefault(
            "character",
            "Knight"
        )

        player_data.setdefault(
            "owned_arrows",
            ["regular"]
        )

        player_data.setdefault(
            "owned_utilities",
            []
        )

        player_data.setdefault(
            "utility",
            ""
        )

    except:

        player_data = fresh_data()


# ============================================================
# TEXT
# ============================================================

def draw_text(
    message,
    x,
    y,
    font=FONT,
    color=WHITE
):

    image = font.render(
        str(message),
        True,
        color
    )

    screen.blit(
        image,
        (
            x,
            y
        )
    )


def draw_center(
    message,
    y,
    font=FONT,
    color=WHITE
):

    image = font.render(
        str(message),
        True,
        color
    )

    x = (
        WIDTH // 2
        -
        image.get_width() // 2
    )

    screen.blit(
        image,
        (
            x,
            y
        )
    )


# ============================================================
# BUTTON
# ============================================================

class Button:

    def __init__(
        self,
        x,
        y,
        width,
        height,
        label
    ):

        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        self.label = label


    def draw(self):

        mouse = pygame.mouse.get_pos()

        if self.rect.collidepoint(
            mouse
        ):

            color = (
                90,
                90,
                125
            )

        else:

            color = (
                55,
                55,
                80
            )


        pygame.draw.rect(
            screen,
            color,
            self.rect,
            border_radius=8
        )

        pygame.draw.rect(
            screen,
            WHITE,
            self.rect,
            2,
            border_radius=8
        )


        image = SMALL.render(
            self.label,
            True,
            WHITE
        )


        screen.blit(
            image,
            image.get_rect(
                center=self.rect.center
            )
        )


    def clicked(
        self,
        event
    ):

        return (
            event.type
            ==
            pygame.MOUSEBUTTONDOWN
            and
            event.button
            ==
            1
            and
            self.rect.collidepoint(
                event.pos
            )
        )


# ============================================================
# EFFECTS
# ============================================================

class Explosion:

    def __init__(
        self,
        x,
        y,
        radius
    ):

        self.x = x
        self.y = y

        self.radius = radius

        self.timer = 20


    def update(self):

        self.timer -= 1


    def draw(self):

        progress = (
            20
            -
            self.timer
        ) / 20


        radius = max(
            5,
            int(
                self.radius
                *
                progress
            )
        )


        pygame.draw.circle(
            screen,
            ORANGE,
            (
                int(
                    self.x
                ),
                int(
                    self.y
                )
            ),
            radius,
            4
        )


        pygame.draw.circle(
            screen,
            YELLOW,
            (
                int(
                    self.x
                ),
                int(
                    self.y
                )
            ),
            max(
                3,
                radius // 2
            ),
            2
        )


class LightningEffect:

    def __init__(
        self,
        start,
        end
    ):

        self.start = start

        self.end = end

        self.timer = 10


    def update(self):

        self.timer -= 1


    def draw(self):

        points = [
            self.start
        ]


        for i in range(
            1,
            6
        ):

            ratio = (
                i / 6
            )


            x = (
                self.start[0]
                +
                (
                    self.end[0]
                    -
                    self.start[0]
                )
                *
                ratio
            )


            y = (
                self.start[1]
                +
                (
                    self.end[1]
                    -
                    self.start[1]
                )
                *
                ratio
            )


            x += random.randint(
                -10,
                10
            )

            y += random.randint(
                -10,
                10
            )


            points.append(
                (
                    int(
                        x
                    ),
                    int(
                        y
                    )
                )
            )


        points.append(
            self.end
        )


        pygame.draw.lines(
            screen,
            CYAN,
            False,
            points,
            4
        )


        pygame.draw.lines(
            screen,
            WHITE,
            False,
            points,
            1
        )


# ============================================================
# PROJECTILE
# ============================================================

class Projectile:

    def __init__(
        self,
        x,
        y,
        target_x,
        target_y,
        damage,
        speed,
        projectile_type,
        enemy=False
    ):

        self.x = float(
            x
        )

        self.y = float(
            y
        )

        self.damage = damage

        self.speed = speed

        self.projectile_type = (
            projectile_type
        )

        self.enemy = enemy


        angle = math.atan2(
            target_y - y,
            target_x - x
        )


        self.dx = (
            math.cos(
                angle
            )
            *
            speed
        )


        self.dy = (
            math.sin(
                angle
            )
            *
            speed
        )


        self.rect = pygame.Rect(
            int(
                x
            ),
            int(
                y
            ),
            14,
            14
        )


    def find_target(
        self,
        enemies,
        boss
    ):

        targets = [

            enemy

            for enemy in enemies

            if enemy.hp > 0
        ]


        if (
            boss
            and
            boss.hp > 0
        ):

            targets.append(
                boss
            )


        if not targets:

            return None


        return min(

            targets,

            key=lambda target:

            math.dist(
                self.rect.center,
                target.rect.center
            )
        )


    def update(
        self,
        enemies,
        boss
    ):

        if not self.enemy:

            arrow = arrow_types.get(
                self.projectile_type
            )


            if (
                arrow
                and
                arrow[
                    "homing"
                ]
            ):

                target = self.find_target(
                    enemies,
                    boss
                )


                if target:

                    dx = (
                        target.rect.centerx
                        -
                        self.rect.centerx
                    )


                    dy = (
                        target.rect.centery
                        -
                        self.rect.centery
                    )


                    distance = max(
                        1,
                        math.hypot(
                            dx,
                            dy
                        )
                    )


                    desired_dx = (
                        dx
                        /
                        distance
                        *
                        self.speed
                    )


                    desired_dy = (
                        dy
                        /
                        distance
                        *
                        self.speed
                    )


                    self.dx = (
                        self.dx
                        *
                        0.82
                        +
                        desired_dx
                        *
                        0.18
                    )


                    self.dy = (
                        self.dy
                        *
                        0.82
                        +
                        desired_dy
                        *
                        0.18
                    )


                    current_speed = max(
                        0.01,
                        math.hypot(
                            self.dx,
                            self.dy
                        )
                    )


                    self.dx = (
                        self.dx
                        /
                        current_speed
                        *
                        self.speed
                    )


                    self.dy = (
                        self.dy
                        /
                        current_speed
                        *
                        self.speed
                    )


        self.x += (
            self.dx
        )

        self.y += (
            self.dy
        )


        self.rect.x = int(
            self.x
        )

        self.rect.y = int(
            self.y
        )


    def draw(self):

        colors = {

            "regular":
                LIGHT_GRAY,

            "lightning":
                CYAN,

            "exploding":
                ORANGE,

            "homing":
                PURPLE,

            "fire":
                RED,

            "super":
                GOLD,

            "enemy":
                PURPLE,

            "ice":
                CYAN,

            "fireball":
                ORANGE,

            "dragon_fire":
                RED
        }


        color = colors.get(
            self.projectile_type,
            PURPLE
        )


        pygame.draw.line(
            screen,
            color,
            self.rect.center,
            (
                self.rect.centerx
                -
                int(
                    self.dx
                    *
                    2
                ),

                self.rect.centery
                -
                int(
                    self.dy
                    *
                    2
                )
            ),
            5
        )


        pygame.draw.circle(
            screen,
            color,
            self.rect.center,
            5
        )


    def off_screen(self):

        return (
            self.x < -50
            or
            self.x > WIDTH + 50
            or
            self.y < -50
            or
            self.y > HEIGHT + 50
        )


# ============================================================
# ENEMY
# ============================================================

class Enemy:

    def __init__(
        self,
        x,
        y,
        hp,
        damage,
        level,
        ranged=False,
        boss=False,
        boss_name=""
    ):

        self.x = float(
            x
        )

        self.y = float(
            y
        )

        self.level = level

        self.ranged = ranged

        self.boss = boss

        self.boss_name = (
            boss_name
        )


        if boss:

            width = 82
            height = 90

        else:

            width = 45
            height = 55


        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )


        self.max_hp = hp

        self.hp = hp

        self.damage = damage


        if boss:

            self.speed = 1.4

        else:

            self.speed = (
                1.1
                +
                level
                *
                0.08
            )


        self.attack_timer = 0

        self.shoot_timer = random.randint(
            50,
            100
        )

        self.special_timer = 180


        self.burn_timer = 0

        self.burn_damage = 0

        self.burn_tick = 30


        self.freeze_timer = 0


    def apply_burn(
        self,
        damage,
        duration
    ):

        self.burn_damage = max(
            self.burn_damage,
            damage
        )

        self.burn_timer = max(
            self.burn_timer,
            duration
        )


    def update_burn(
        self
    ):

        if self.burn_timer <= 0:

            return


        self.burn_timer -= 1

        self.burn_tick -= 1


        if self.burn_tick <= 0:

            self.hp -= (
                self.burn_damage
            )

            self.burn_tick = 30


    def update(
        self,
        player,
        walls,
        projectiles
    ):

        self.update_burn()


        if self.freeze_timer > 0:

            self.freeze_timer -= 1

            current_speed = (
                self.speed
                *
                0.35
            )

        else:

            current_speed = (
                self.speed
            )


        if (
            player.invisible_timer
            >
            0
        ):

            return


        dx = (
            player.rect.centerx
            -
            self.rect.centerx
        )


        dy = (
            player.rect.centery
            -
            self.rect.centery
        )


        distance = max(
            1,
            math.hypot(
                dx,
                dy
            )
        )


        move_x = 0

        move_y = 0


        if self.ranged:

            if distance > 280:

                move_x = (
                    dx
                    /
                    distance
                    *
                    current_speed
                )

                move_y = (
                    dy
                    /
                    distance
                    *
                    current_speed
                )

            elif distance < 170:

                move_x = (
                    -dx
                    /
                    distance
                    *
                    current_speed
                )

                move_y = (
                    -dy
                    /
                    distance
                    *
                    current_speed
                )


        else:

            if distance > 55:

                move_x = (
                    dx
                    /
                    distance
                    *
                    current_speed
                )

                move_y = (
                    dy
                    /
                    distance
                    *
                    current_speed
                )


        old_x = (
            self.x
        )

        self.x += (
            move_x
        )

        self.rect.x = int(
            self.x
        )


        for wall in walls:

            if self.rect.colliderect(
                wall
            ):

                self.x = (
                    old_x
                )

                self.rect.x = int(
                    self.x
                )

                break


        old_y = (
            self.y
        )

        self.y += (
            move_y
        )

        self.rect.y = int(
            self.y
        )


        for wall in walls:

            if self.rect.colliderect(
                wall
            ):

                self.y = (
                    old_y
                )

                self.rect.y = int(
                    self.y
                )

                break


        if self.attack_timer > 0:

            self.attack_timer -= 1


        if self.shoot_timer > 0:

            self.shoot_timer -= 1


        if self.special_timer > 0:

            self.special_timer -= 1


        distance = math.dist(
            self.rect.center,
            player.rect.center
        )


        if self.ranged:

            if (
                distance < 480
                and
                self.shoot_timer <= 0
            ):

                projectiles.append(

                    Projectile(
                        self.rect.centerx,
                        self.rect.centery,

                        player.rect.centerx,
                        player.rect.centery,

                        self.damage,

                        6,

                        "enemy",

                        True
                    )
                )


                self.shoot_timer = 85


        else:

            if (
                distance < 60
                and
                self.attack_timer <= 0
            ):

                defense = armors[
                    player_data[
                        "armor"
                    ]
                ]["defense"]


                player.hp -= max(
                    1,
                    self.damage
                    -
                    defense
                )


                self.attack_timer = 50


    # ========================================================
    # BOSS ABILITIES
    # ========================================================

    def boss_ability(
        self,
        player,
        enemies,
        projectiles
    ):

        if not self.boss:

            return


        if self.special_timer > 0:

            return


        # GOBLIN KING

        if self.level == 1:

            for i in range(
                2
            ):

                enemies.append(

                    Enemy(
                        self.rect.x
                        +
                        random.randint(
                            -100,
                            100
                        ),

                        self.rect.y
                        +
                        random.randint(
                            -100,
                            100
                        ),

                        35,

                        6,

                        1
                    )
                )


            self.special_timer = (
                5
                *
                FPS
            )


        # FOREST TROLL

        elif self.level == 2:

            if math.dist(
                self.rect.center,
                player.rect.center
            ) < 190:

                defense = armors[
                    player_data[
                        "armor"
                    ]
                ]["defense"]


                player.hp -= max(
                    1,
                    32
                    -
                    defense
                )


            self.special_timer = (
                4
                *
                FPS
            )


        # ICE KNIGHT

        elif self.level == 3:

            projectiles.append(

                Projectile(
                    self.rect.centerx,
                    self.rect.centery,

                    player.rect.centerx,
                    player.rect.centery,

                    20,

                    7,

                    "ice",

                    True
                )
            )


            self.special_timer = (
                2
                *
                FPS
            )


        # FIRE DEMON

        elif self.level == 4:

            base_angle = math.atan2(

                player.rect.centery
                -
                self.rect.centery,

                player.rect.centerx
                -
                self.rect.centerx
            )


            for offset in [

                -0.28,
                0,
                0.28

            ]:

                angle = (
                    base_angle
                    +
                    offset
                )


                projectiles.append(

                    Projectile(
                        self.rect.centerx,
                        self.rect.centery,

                        self.rect.centerx
                        +
                        math.cos(
                            angle
                        )
                        *
                        600,

                        self.rect.centery
                        +
                        math.sin(
                            angle
                        )
                        *
                        600,

                        24,

                        7,

                        "fireball",

                        True
                    )
                )


            self.special_timer = (
                3
                *
                FPS
            )


        # ANCIENT DRAGON

        elif self.level == 5:

            attack = random.choice(
                [
                    "fire",
                    "charge",
                    "summon"
                ]
            )


            if attack == "fire":

                base_angle = math.atan2(

                    player.rect.centery
                    -
                    self.rect.centery,

                    player.rect.centerx
                    -
                    self.rect.centerx
                )


                for offset in [

                    -0.55,
                    -0.28,
                    0,
                    0.28,
                    0.55

                ]:

                    angle = (
                        base_angle
                        +
                        offset
                    )


                    projectiles.append(

                        Projectile(
                            self.rect.centerx,
                            self.rect.centery,

                            self.rect.centerx
                            +
                            math.cos(
                                angle
                            )
                            *
                            700,

                            self.rect.centery
                            +
                            math.sin(
                                angle
                            )
                            *
                            700,

                            30,

                            8,

                            "dragon_fire",

                            True
                        )
                    )


            elif attack == "charge":

                dx = (
                    player.rect.centerx
                    -
                    self.rect.centerx
                )


                dy = (
                    player.rect.centery
                    -
                    self.rect.centery
                )


                distance = max(
                    1,
                    math.hypot(
                        dx,
                        dy
                    )
                )


                self.x += (
                    dx
                    /
                    distance
                    *
                    130
                )


                self.y += (
                    dy
                    /
                    distance
                    *
                    130
                )


                self.rect.x = int(
                    self.x
                )

                self.rect.y = int(
                    self.y
                )


                if self.rect.colliderect(
                    player.rect
                ):

                    player.hp -= 38


            else:

                for i in range(
                    3
                ):

                    enemies.append(

                        Enemy(
                            self.rect.x
                            +
                            random.randint(
                                -120,
                                120
                            ),

                            self.rect.y
                            +
                            random.randint(
                                -120,
                                120
                            ),

                            90,

                            15,

                            5,

                            ranged=random.choice(
                                [
                                    True,
                                    False
                                ]
                            )
                        )
                    )


            self.special_timer = (
                3
                *
                FPS
            )


    # ========================================================
    # DRAW ENEMY
    # ========================================================

    def draw(
        self
    ):

        if self.boss:

            body_color = DARK_RED

            head_color = RED

        elif self.ranged:

            body_color = PURPLE

            head_color = (
                80,
                200,
                90
            )

        else:

            body_color = DARK_GREEN

            head_color = (
                80,
                200,
                80
            )


        if (
            self.boss
            and
            self.level == 5
        ):

            pygame.draw.ellipse(
                screen,
                body_color,
                self.rect
            )

        else:

            pygame.draw.rect(
                screen,
                body_color,
                self.rect,
                border_radius=8
            )


        head_radius = (
            22
            if self.boss
            else
            12
        )


        pygame.draw.circle(
            screen,
            head_color,
            (
                self.rect.centerx,
                self.rect.y + 8
            ),
            head_radius
        )


        pygame.draw.circle(
            screen,
            RED,
            (
                self.rect.centerx - 5,
                self.rect.y + 7
            ),
            2
        )


        pygame.draw.circle(
            screen,
            RED,
            (
                self.rect.centerx + 5,
                self.rect.y + 7
            ),
            2
        )


        if (
            self.boss
            and
            self.level != 5
        ):

            pygame.draw.polygon(
                screen,
                GOLD,
                [
                    (
                        self.rect.centerx - 20,
                        self.rect.y - 8
                    ),

                    (
                        self.rect.centerx - 10,
                        self.rect.y - 25
                    ),

                    (
                        self.rect.centerx,
                        self.rect.y - 8
                    ),

                    (
                        self.rect.centerx + 10,
                        self.rect.y - 25
                    ),

                    (
                        self.rect.centerx + 20,
                        self.rect.y - 8
                    )
                ]
            )


        if self.ranged:

            pygame.draw.arc(
                screen,
                BROWN,
                (
                    self.rect.x - 7,
                    self.rect.y + 15,
                    30,
                    38
                ),
                -1.5,
                1.5,
                4
            )


        if self.burn_timer > 0:

            pygame.draw.circle(
                screen,
                ORANGE,
                (
                    self.rect.centerx,
                    self.rect.y - 5
                ),
                9
            )

            pygame.draw.circle(
                screen,
                YELLOW,
                (
                    self.rect.centerx,
                    self.rect.y - 8
                ),
                5
            )


        if self.freeze_timer > 0:

            pygame.draw.circle(
                screen,
                CYAN,
                self.rect.center,
                max(
                    20,
                    self.rect.width // 2
                ),
                2
            )


        pygame.draw.rect(
            screen,
            DARK_RED,
            (
                self.rect.x,
                self.rect.y - 12,
                self.rect.width,
                7
            )
        )


        hp_width = int(
            self.rect.width
            *
            max(
                0,
                self.hp
            )
            /
            self.max_hp
        )


        pygame.draw.rect(
            screen,
            GREEN,
            (
                self.rect.x,
                self.rect.y - 12,
                hp_width,
                7
            )
        )


# ============================================================
# PLAYER
# ============================================================

class Player:

    def __init__(
        self
    ):

        character_data = characters[
            player_data[
                "character"
            ]
        ]


        self.x = 100

        self.y = 350


        self.rect = pygame.Rect(
            self.x,
            self.y,
            44,
            58
        )


        self.speed = (
            5
            +
            character_data[
                "speed_bonus"
            ]
        )


        self.max_hp = (
            player_data[
                "max_hp"
            ]
            +
            character_data[
                "hp_bonus"
            ]
        )


        self.max_hp = max(
            50,
            self.max_hp
        )


        self.hp = (
            self.max_hp
        )


        self.facing = 1


        self.attack_cooldown = 0

        self.bow_cooldown = 0

        self.utility_cooldown = 0


        self.swing_timer = 0

        self.swing_length = 12


        self.hammer_timer = 0


        self.slow_timer = 0


        self.ability_z_cooldown = 0

        self.ability_x_cooldown = 0

        self.ability_c_cooldown = 0


        self.berserk_timer = 0

        self.invisible_timer = 0


    # ========================================================
    # PLAYER UPDATE
    # ========================================================

    def update(
        self,
        walls
    ):

        keys = pygame.key.get_pressed()


        if self.slow_timer > 0:

            movement_speed = (
                self.speed
                /
                2
            )

            self.slow_timer -= 1

        else:

            movement_speed = (
                self.speed
            )


        dx = 0

        dy = 0


        if keys[
            pygame.K_a
        ]:

            dx = (
                -movement_speed
            )

            self.facing = -1


        if keys[
            pygame.K_d
        ]:

            dx = (
                movement_speed
            )

            self.facing = 1


        if keys[
            pygame.K_w
        ]:

            dy = (
                -movement_speed
            )


        if keys[
            pygame.K_s
        ]:

            dy = (
                movement_speed
            )


        old_x = (
            self.x
        )


        self.x += (
            dx
        )


        self.rect.x = int(
            self.x
        )


        for wall in walls:

            if self.rect.colliderect(
                wall
            ):

                self.x = (
                    old_x
                )

                self.rect.x = int(
                    self.x
                )

                break


        old_y = (
            self.y
        )


        self.y += (
            dy
        )


        self.rect.y = int(
            self.y
        )


        for wall in walls:

            if self.rect.colliderect(
                wall
            ):

                self.y = (
                    old_y
                )

                self.rect.y = int(
                    self.y
                )

                break


        self.x = max(
            0,
            min(
                WIDTH
                -
                self.rect.width,
                self.x
            )
        )


        self.y = max(
            100,
            min(
                HEIGHT
                -
                self.rect.height,
                self.y
            )
        )


        self.rect.x = int(
            self.x
        )

        self.rect.y = int(
            self.y
        )


        if self.attack_cooldown > 0:

            self.attack_cooldown -= 1


        if self.bow_cooldown > 0:

            self.bow_cooldown -= 1


        if self.utility_cooldown > 0:

            self.utility_cooldown -= 1


        if self.swing_timer > 0:

            self.swing_timer -= 1


        if self.hammer_timer > 0:

            self.hammer_timer -= 1


        if self.ability_z_cooldown > 0:

            self.ability_z_cooldown -= 1


        if self.ability_x_cooldown > 0:

            self.ability_x_cooldown -= 1


        if self.ability_c_cooldown > 0:

            self.ability_c_cooldown -= 1


        if self.berserk_timer > 0:

            self.berserk_timer -= 1


        if self.invisible_timer > 0:

            self.invisible_timer -= 1


    # ========================================================
    # SWORD
    # ========================================================

    def sword_attack(
        self,
        enemies,
        boss
    ):

        if self.attack_cooldown > 0:

            return


        self.attack_cooldown = 22


        self.swing_timer = (
            self.swing_length
        )


        if self.facing == 1:

            hitbox = pygame.Rect(
                self.rect.right,
                self.rect.y - 10,
                85,
                80
            )

        else:

            hitbox = pygame.Rect(
                self.rect.left - 85,
                self.rect.y - 10,
                85,
                80
            )


        damage = weapons[
            player_data[
                "weapon"
            ]
        ]["damage"]


        if self.berserk_timer > 0:

            damage *= 2


        for enemy in enemies:

            if hitbox.colliderect(
                enemy.rect
            ):

                enemy.hp -= (
                    damage
                )


        if (
            boss
            and
            hitbox.colliderect(
                boss.rect
            )
        ):

            boss.hp -= (
                damage
            )


    # ========================================================
    # BOW
    # ========================================================

    def shoot(
        self,
        projectiles
    ):

        if self.bow_cooldown > 0:

            return


        arrow_name = (
            player_data[
                "arrow_type"
            ]
        )


        arrow = arrow_types[
            arrow_name
        ]


        bow = bows[
            player_data[
                "bow"
            ]
        ]


        damage = (
            bow[
                "damage"
            ]
            +
            arrow[
                "damage_bonus"
            ]
        )


        speed = max(
            3,
            bow[
                "speed"
            ]
            +
            arrow[
                "speed_bonus"
            ]
        )


        if arrow_name == "super":

            self.bow_cooldown = 42

        else:

            self.bow_cooldown = 28


        projectiles.append(

            Projectile(
                self.rect.centerx,
                self.rect.centery,

                self.rect.centerx
                +
                self.facing
                *
                700,

                self.rect.centery,

                damage,

                speed,

                arrow_name
            )
        )


    # ========================================================
    # UTILITY
    # ========================================================

    def teleport(
        self,
        walls
    ):

        if self.utility_cooldown > 0:

            return


        old_x = (
            self.x
        )


        self.x += (
            self.facing
            *
            220
        )


        self.x = max(
            0,
            min(
                WIDTH
                -
                self.rect.width,
                self.x
            )
        )


        self.rect.x = int(
            self.x
        )


        for wall in walls:

            if self.rect.colliderect(
                wall
            ):

                self.x = (
                    old_x
                )

                self.rect.x = int(
                    self.x
                )

                return


        self.utility_cooldown = 120


    def hammer(
        self,
        enemies,
        boss,
        explosions
    ):

        if self.utility_cooldown > 0:

            return


        utility_name = (
            player_data[
                "utility"
            ]
        )


        if utility_name not in utilities:

            return


        utility_data = utilities[
            utility_name
        ]


        if utility_data[
            "type"
        ] != "hammer":

            return


        self.utility_cooldown = 90


        self.hammer_timer = 20


        radius = (
            utility_data[
                "range"
            ]
        )


        damage = (
            utility_data[
                "damage"
            ]
        )


        explosions.append(

            Explosion(
                self.rect.centerx,
                self.rect.centery,
                radius
            )
        )


        for enemy in enemies:

            if math.dist(
                self.rect.center,
                enemy.rect.center
            ) <= radius:

                enemy.hp -= damage


        if (
            boss
            and
            math.dist(
                self.rect.center,
                boss.rect.center
            ) <= radius
        ):

            boss.hp -= damage


    # ========================================================
    # CHARACTER ABILITIES
    # ========================================================

    def use_ability(
        self,
        key,
        enemies,
        boss,
        projectiles,
        explosions,
        lightning_effects,
        walls
    ):

        character_name = (
            player_data[
                "character"
            ]
        )


        character = characters[
            character_name
        ]


        # ====================================================
        # Z
        # ====================================================

        if key == "Z":

            if self.ability_z_cooldown > 0:

                return


            self.ability_z_cooldown = (

                character[
                    "abilities"
                ][
                    "Z"
                ][
                    "cooldown"
                ]
            )


            # KNIGHT - SHIELD RUSH

            if character_name == "Knight":

                old_x = (
                    self.x
                )


                self.x += (
                    self.facing
                    *
                    150
                )


                self.x = max(
                    0,
                    min(
                        WIDTH
                        -
                        self.rect.width,
                        self.x
                    )
                )


                self.rect.x = int(
                    self.x
                )


                for wall in walls:

                    if self.rect.colliderect(
                        wall
                    ):

                        self.x = (
                            old_x
                        )

                        self.rect.x = int(
                            self.x
                        )

                        break


                for enemy in enemies:

                    if math.dist(
                        self.rect.center,
                        enemy.rect.center
                    ) < 130:

                        enemy.hp -= 50


                if (
                    boss
                    and
                    math.dist(
                        self.rect.center,
                        boss.rect.center
                    ) < 130
                ):

                    boss.hp -= 50


            # RANGER - TRIPLE SHOT

            elif character_name == "Ranger":

                bow = bows[
                    player_data[
                        "bow"
                    ]
                ]


                arrow_name = (
                    player_data[
                        "arrow_type"
                    ]
                )


                arrow = arrow_types[
                    arrow_name
                ]


                damage = (
                    bow[
                        "damage"
                    ]
                    +
                    arrow[
                        "damage_bonus"
                    ]
                )


                speed = max(
                    3,
                    bow[
                        "speed"
                    ]
                    +
                    arrow[
                        "speed_bonus"
                    ]
                )


                base_angle = (
                    0
                    if self.facing == 1
                    else math.pi
                )


                for offset in [

                    -0.20,
                    0,
                    0.20

                ]:

                    angle = (
                        base_angle
                        +
                        offset
                    )


                    projectiles.append(

                        Projectile(
                            self.rect.centerx,
                            self.rect.centery,

                            self.rect.centerx
                            +
                            math.cos(
                                angle
                            )
                            *
                            700,

                            self.rect.centery
                            +
                            math.sin(
                                angle
                            )
                            *
                            700,

                            damage,

                            speed,

                            arrow_name
                        )
                    )


            # MAGE - FIREBALL

            elif character_name == "Mage":

                projectiles.append(

                    Projectile(
                        self.rect.centerx,
                        self.rect.centery,

                        self.rect.centerx
                        +
                        self.facing
                        *
                        700,

                        self.rect.centery,

                        75,

                        8,

                        "fire"
                    )
                )


            # SHADOW - TELEPORT STRIKE

            elif character_name == "Shadow":

                targets = [

                    enemy

                    for enemy in enemies

                    if enemy.hp > 0
                ]


                if (
                    boss
                    and
                    boss.hp > 0
                ):

                    targets.append(
                        boss
                    )


                if targets:

                    target = min(

                        targets,

                        key=lambda e:

                        math.dist(
                            self.rect.center,
                            e.rect.center
                        )
                    )


                    self.x = (
                        target.rect.x
                        -
                        60
                    )


                    self.y = (
                        target.rect.y
                    )


                    self.x = max(
                        0,
                        min(
                            WIDTH
                            -
                            self.rect.width,
                            self.x
                        )
                    )


                    self.y = max(
                        100,
                        min(
                            HEIGHT
                            -
                            self.rect.height,
                            self.y
                        )
                    )


                    self.rect.x = int(
                        self.x
                    )

                    self.rect.y = int(
                        self.y
                    )


                    target.hp -= 90


        # ====================================================
        # X
        # ====================================================

        elif key == "X":

            if self.ability_x_cooldown > 0:

                return


            self.ability_x_cooldown = (

                character[
                    "abilities"
                ][
                    "X"
                ][
                    "cooldown"
                ]
            )


            # KNIGHT - GROUND SLAM

            if character_name == "Knight":

                radius = 190


                explosions.append(

                    Explosion(
                        self.rect.centerx,
                        self.rect.centery,
                        radius
                    )
                )


                for enemy in enemies:

                    if math.dist(
                        self.rect.center,
                        enemy.rect.center
                    ) <= radius:

                        enemy.hp -= 75


                if (
                    boss
                    and
                    math.dist(
                        self.rect.center,
                        boss.rect.center
                    ) <= radius
                ):

                    boss.hp -= 75


            # RANGER - DASH

            elif character_name == "Ranger":

                old_x = (
                    self.x
                )


                self.x += (
                    self.facing
                    *
                    240
                )


                self.x = max(
                    0,
                    min(
                        WIDTH
                        -
                        self.rect.width,
                        self.x
                    )
                )


                self.rect.x = int(
                    self.x
                )


                for wall in walls:

                    if self.rect.colliderect(
                        wall
                    ):

                        self.x = (
                            old_x
                        )

                        self.rect.x = int(
                            self.x
                        )

                        break


            # MAGE - FREEZE BLAST

            elif character_name == "Mage":

                radius = 210


                explosions.append(

                    Explosion(
                        self.rect.centerx,
                        self.rect.centery,
                        radius
                    )
                )


                for enemy in enemies:

                    if math.dist(
                        self.rect.center,
                        enemy.rect.center
                    ) <= radius:

                        enemy.hp -= 35

                        enemy.freeze_timer = (
                            4
                            *
                            FPS
                        )


                if (
                    boss
                    and
                    math.dist(
                        self.rect.center,
                        boss.rect.center
                    ) <= radius
                ):

                    boss.hp -= 35

                    boss.freeze_timer = (
                        2
                        *
                        FPS
                    )


            # SHADOW - VANISH

            elif character_name == "Shadow":

                self.invisible_timer = (
                    3
                    *
                    FPS
                )


        # ====================================================
        # C
        # ====================================================

        elif key == "C":

            if self.ability_c_cooldown > 0:

                return


            self.ability_c_cooldown = (

                character[
                    "abilities"
                ][
                    "C"
                ][
                    "cooldown"
                ]
            )


            # KNIGHT - BERSERK

            if character_name == "Knight":

                self.berserk_timer = (
                    5
                    *
                    FPS
                )


            # RANGER - ARROW STORM

            elif character_name == "Ranger":

                arrow_name = (
                    player_data[
                        "arrow_type"
                    ]
                )


                arrow = arrow_types[
                    arrow_name
                ]


                bow = bows[
                    player_data[
                        "bow"
                    ]
                ]


                damage = (
                    bow[
                        "damage"
                    ]
                    +
                    arrow[
                        "damage_bonus"
                    ]
                )


                speed = max(
                    4,
                    bow[
                        "speed"
                    ]
                )


                targets = [

                    enemy

                    for enemy in enemies

                    if enemy.hp > 0
                ]


                if boss:

                    targets.append(
                        boss
                    )


                for target in targets:

                    for i in range(
                        3
                    ):

                        start_x = (
                            target.rect.centerx
                            +
                            random.randint(
                                -100,
                                100
                            )
                        )


                        start_y = (
                            target.rect.centery
                            -
                            300
                            -
                            random.randint(
                                0,
                                80
                            )
                        )


                        projectiles.append(

                            Projectile(
                                start_x,
                                start_y,

                                target.rect.centerx,
                                target.rect.centery,

                                damage,

                                speed,

                                arrow_name
                            )
                        )


            # MAGE - LIGHTNING NOVA

            elif character_name == "Mage":

                radius = 280


                targets = []


                for enemy in enemies:

                    if math.dist(
                        self.rect.center,
                        enemy.rect.center
                    ) <= radius:

                        targets.append(
                            enemy
                        )


                if (
                    boss
                    and
                    math.dist(
                        self.rect.center,
                        boss.rect.center
                    ) <= radius
                ):

                    targets.append(
                        boss
                    )


                for target in targets:

                    target.hp -= 90


                    lightning_effects.append(

                        LightningEffect(
                            self.rect.center,
                            target.rect.center
                        )
                    )


            # SHADOW - SPIN ATTACK

            elif character_name == "Shadow":

                radius = 170


                explosions.append(

                    Explosion(
                        self.rect.centerx,
                        self.rect.centery,
                        radius
                    )
                )


                for enemy in enemies:

                    if math.dist(
                        self.rect.center,
                        enemy.rect.center
                    ) <= radius:

                        enemy.hp -= 110


                if (
                    boss
                    and
                    math.dist(
                        self.rect.center,
                        boss.rect.center
                    ) <= radius
                ):

                    boss.hp -= 110


    # ========================================================
    # DRAW PLAYER
    # ========================================================

    def draw_body(
        self
    ):

        character_name = (
            player_data[
                "character"
            ]
        )


        character_color = (
            characters[
                character_name
            ][
                "color"
            ]
        )


        armor_name = (
            player_data[
                "armor"
            ]
        )


        if "Dragon" in armor_name:

            armor_color = RED

        elif "Demon" in armor_name:

            armor_color = PURPLE

        elif "Knight" in armor_name:

            armor_color = LIGHT_GRAY

        elif "Iron" in armor_name:

            armor_color = GRAY

        elif "Leather" in armor_name:

            armor_color = BROWN

        else:

            armor_color = (
                character_color
            )


        alpha_mode = (
            self.invisible_timer
            >
            0
        )


        if alpha_mode:

            body_color = (
                90,
                90,
                90
            )

        else:

            body_color = (
                armor_color
            )


        pygame.draw.rect(
            screen,
            DARK_BLUE,
            (
                self.rect.x + 7,
                self.rect.y + 42,
                12,
                16
            )
        )


        pygame.draw.rect(
            screen,
            DARK_BLUE,
            (
                self.rect.x + 26,
                self.rect.y + 42,
                12,
                16
            )
        )


        pygame.draw.rect(
            screen,
            body_color,
            (
                self.rect.x + 5,
                self.rect.y + 15,
                34,
                32
            ),
            border_radius=5
        )


        pygame.draw.circle(
            screen,
            (
                235,
                195,
                155
            ),
            (
                self.rect.centerx,
                self.rect.y + 10
            ),
            13
        )


        pygame.draw.circle(
            screen,
            BLACK,
            (
                self.rect.centerx - 5,
                self.rect.y + 8
            ),
            2
        )


        pygame.draw.circle(
            screen,
            BLACK,
            (
                self.rect.centerx + 5,
                self.rect.y + 8
            ),
            2
        )


        # KNIGHT HELMET

        if character_name == "Knight":

            pygame.draw.arc(
                screen,
                LIGHT_GRAY,
                (
                    self.rect.centerx - 14,
                    self.rect.y - 3,
                    28,
                    22
                ),
                math.pi,
                2 * math.pi,
                5
            )


        # RANGER HOOD

        elif character_name == "Ranger":

            pygame.draw.arc(
                screen,
                GREEN,
                (
                    self.rect.centerx - 15,
                    self.rect.y - 4,
                    30,
                    25
                ),
                math.pi,
                2 * math.pi,
                6
            )


        # MAGE HAT

        elif character_name == "Mage":

            pygame.draw.polygon(
                screen,
                PURPLE,
                [
                    (
                        self.rect.centerx,
                        self.rect.y - 25
                    ),

                    (
                        self.rect.centerx - 17,
                        self.rect.y + 3
                    ),

                    (
                        self.rect.centerx + 17,
                        self.rect.y + 3
                    )
                ]
            )


        # SHADOW MASK

        elif character_name == "Shadow":

            pygame.draw.rect(
                screen,
                DARK_GRAY,
                (
                    self.rect.centerx - 13,
                    self.rect.y,
                    26,
                    9
                )
            )


    def draw_sword(
        self
    ):

        center_x = (
            self.rect.centerx
        )

        center_y = (
            self.rect.centery
        )


        if self.swing_timer > 0:

            progress = (
                self.swing_length
                -
                self.swing_timer
            ) / self.swing_length


            if self.facing == 1:

                angle = (
                    -1.2
                    +
                    progress
                    *
                    2.4
                )

            else:

                angle = (
                    math.pi
                    +
                    1.2
                    -
                    progress
                    *
                    2.4
                )

        else:

            if self.facing == 1:

                angle = -0.3

            else:

                angle = (
                    math.pi
                    +
                    0.3
                )


        sword_length = 52


        handle_x = (
            center_x
            +
            math.cos(
                angle
            )
            *
            13
        )


        handle_y = (
            center_y
            +
            math.sin(
                angle
            )
            *
            13
        )


        end_x = (
            center_x
            +
            math.cos(
                angle
            )
            *
            sword_length
        )


        end_y = (
            center_y
            +
            math.sin(
                angle
            )
            *
            sword_length
        )


        pygame.draw.line(
            screen,
            GOLD,
            (
                center_x,
                center_y
            ),
            (
                handle_x,
                handle_y
            ),
            8
        )


        pygame.draw.line(
            screen,
            LIGHT_GRAY,
            (
                handle_x,
                handle_y
            ),
            (
                end_x,
                end_y
            ),
            7
        )


        if self.berserk_timer > 0:

            pygame.draw.circle(
                screen,
                RED,
                (
                    int(
                        end_x
                    ),
                    int(
                        end_y
                    )
                ),
                8,
                2
            )


    def draw_bow(
        self
    ):

        if self.facing == 1:

            bow_rect = pygame.Rect(
                self.rect.right - 5,
                self.rect.centery - 25,
                28,
                50
            )

        else:

            bow_rect = pygame.Rect(
                self.rect.left - 23,
                self.rect.centery - 25,
                28,
                50
            )


        pygame.draw.arc(
            screen,
            BROWN,
            bow_rect,
            -1.5,
            1.5,
            4
        )


        pygame.draw.line(
            screen,
            WHITE,
            (
                bow_rect.centerx,
                bow_rect.top
            ),
            (
                bow_rect.centerx,
                bow_rect.bottom
            ),
            2
        )


    def draw_hammer(
        self
    ):

        if self.hammer_timer <= 0:

            return


        end_x = (
            self.rect.centerx
            +
            self.facing
            *
            55
        )


        end_y = (
            self.rect.centery
            -
            30
        )


        pygame.draw.line(
            screen,
            BROWN,
            self.rect.center,
            (
                end_x,
                end_y
            ),
            8
        )


        pygame.draw.rect(
            screen,
            DARK_GRAY,
            (
                end_x - 18,
                end_y - 15,
                36,
                30
            )
        )


    def draw(
        self
    ):

        self.draw_body()


        if (
            player_data[
                "weapon_mode"
            ]
            ==
            "sword"
        ):

            self.draw_sword()

        else:

            self.draw_bow()


        self.draw_hammer()


# ============================================================
# CHEST
# ============================================================

class Chest:

    def __init__(
        self,
        x,
        y
    ):

        self.rect = pygame.Rect(
            x,
            y,
            42,
            32
        )

        self.opened = False


    def draw(
        self
    ):

        if self.opened:

            pygame.draw.rect(
                screen,
                DARK_GRAY,
                self.rect
            )

        else:

            pygame.draw.rect(
                screen,
                BROWN,
                self.rect,
                border_radius=5
            )


            pygame.draw.line(
                screen,
                GOLD,
                (
                    self.rect.x,
                    self.rect.centery
                ),
                (
                    self.rect.right,
                    self.rect.centery
                ),
                3
            )


            pygame.draw.rect(
                screen,
                GOLD,
                (
                    self.rect.centerx - 4,
                    self.rect.centery - 3,
                    8,
                    10
                )
            )


    def open(
        self,
        player
    ):

        if self.opened:

            return ""


        nearby = self.rect.inflate(
            55,
            55
        )


        if not nearby.colliderect(
            player.rect
        ):

            return ""


        self.opened = True


        if random.random() < 0.7:

            amount = random.randint(
                30,
                100
            )


            player_data[
                "gold"
            ] += amount


            return (
                f"+{amount} gold!"
            )

        else:

            player_data[
                "potions"
            ] += 1


            return (
                "Found a potion!"
            )


# ============================================================
# MAP
# ============================================================

def create_map(
    level
):

    walls = [

        pygame.Rect(
            250,
            180,
            220,
            35
        ),

        pygame.Rect(
            620,
            470,
            260,
            35
        )
    ]


    if level >= 2:

        walls.append(

            pygame.Rect(
                500,
                280,
                35,
                180
            )
        )


    if level >= 3:

        walls.append(

            pygame.Rect(
                800,
                150,
                40,
                180
            )
        )


    if level >= 4:

        walls.append(

            pygame.Rect(
                160,
                500,
                250,
                30
            )
        )


    if level >= 5:

        walls.append(

            pygame.Rect(
                430,
                570,
                280,
                30
            )
        )


    return walls


def draw_walls(
    walls,
    level
):

    colors = {

        1:
            BROWN,

        2:
            DARK_GREEN,

        3:
            LIGHT_GRAY,

        4:
            DARK_RED,

        5:
            PURPLE
    }


    color = colors[
        level
    ]


    for wall in walls:

        pygame.draw.rect(
            screen,
            color,
            wall,
            border_radius=4
        )


        pygame.draw.rect(
            screen,
            BLACK,
            wall,
            2,
            border_radius=4
        )


# ============================================================
# XP
# ============================================================

def check_level_up(
):

    while True:

        needed = (
            player_data[
                "player_level"
            ]
            *
            100
        )


        if (
            player_data[
                "xp"
            ]
            <
            needed
        ):

            break


        player_data[
            "xp"
        ] -= needed


        player_data[
            "player_level"
        ] += 1


        player_data[
            "max_hp"
        ] += 15


# ============================================================
# ARROW HIT
# ============================================================

def apply_arrow_hit(
    projectile,
    target,
    enemies,
    boss,
    explosions,
    lightning_effects
):

    arrow = arrow_types[
        projectile.projectile_type
    ]


    target.hp -= (
        projectile.damage
    )


    # FIRE

    if arrow[
        "burn_damage"
    ] > 0:

        target.apply_burn(
            arrow[
                "burn_damage"
            ],
            arrow[
                "burn_time"
            ]
        )


    # EXPLOSION

    radius = arrow[
        "explosion_radius"
    ]


    if radius > 0:

        explosions.append(

            Explosion(
                projectile.rect.centerx,
                projectile.rect.centery,
                radius
            )
        )


        targets = list(
            enemies
        )


        if boss:

            targets.append(
                boss
            )


        for other in targets:

            if other is target:

                continue


            if math.dist(
                projectile.rect.center,
                other.rect.center
            ) <= radius:

                other.hp -= max(
                    1,
                    projectile.damage
                    //
                    2
                )


                if arrow[
                    "burn_damage"
                ] > 0:

                    other.apply_burn(
                        arrow[
                            "burn_damage"
                        ],
                        arrow[
                            "burn_time"
                        ]
                    )


    # LIGHTNING

    lightning_radius = arrow[
        "lightning_radius"
    ]


    if lightning_radius > 0:

        nearby = []


        targets = list(
            enemies
        )


        if boss:

            targets.append(
                boss
            )


        for other in targets:

            if other is target:

                continue


            if math.dist(
                target.rect.center,
                other.rect.center
            ) <= lightning_radius:

                nearby.append(
                    other
                )


        nearby.sort(

            key=lambda other:

            math.dist(
                target.rect.center,
                other.rect.center
            )
        )


        for other in nearby[:3]:

            other.hp -= max(
                1,
                projectile.damage
                //
                2
            )


            lightning_effects.append(

                LightningEffect(
                    target.rect.center,
                    other.rect.center
                )
            )


            if arrow[
                "burn_damage"
            ] > 0:

                other.apply_burn(
                    arrow[
                        "burn_damage"
                    ],
                    arrow[
                        "burn_time"
                    ]
                )


# ============================================================
# SAFE WALL IMPACT
# ============================================================

def arrow_hit_wall(
    projectile,
    enemies,
    boss,
    explosions,
    lightning_effects
):

    if projectile.enemy:

        return


    if (
        projectile.projectile_type
        not in arrow_types
    ):

        return


    arrow = arrow_types[
        projectile.projectile_type
    ]


    impact = (
        projectile.rect.centerx,
        projectile.rect.centery
    )


    # EXPLOSION

    radius = arrow[
        "explosion_radius"
    ]


    if radius > 0:

        explosions.append(

            Explosion(
                impact[0],
                impact[1],
                radius
            )
        )


        targets = list(
            enemies
        )


        if boss:

            targets.append(
                boss
            )


        for target in targets:

            if target.hp <= 0:

                continue


            if math.dist(
                impact,
                target.rect.center
            ) <= radius:

                target.hp -= max(
                    1,
                    projectile.damage
                    //
                    2
                )


                if arrow[
                    "burn_damage"
                ] > 0:

                    target.apply_burn(
                        arrow[
                            "burn_damage"
                        ],
                        arrow[
                            "burn_time"
                        ]
                    )


    # LIGHTNING

    lightning_radius = arrow[
        "lightning_radius"
    ]


    if lightning_radius > 0:

        targets = [

            enemy

            for enemy in enemies

            if enemy.hp > 0
        ]


        if (
            boss
            and
            boss.hp > 0
        ):

            targets.append(
                boss
            )


        targets.sort(

            key=lambda target:

            math.dist(
                impact,
                target.rect.center
            )
        )


        count = 0


        for target in targets:

            if math.dist(
                impact,
                target.rect.center
            ) <= lightning_radius:

                target.hp -= max(
                    1,
                    projectile.damage
                    //
                    2
                )


                lightning_effects.append(

                    LightningEffect(
                        impact,
                        target.rect.center
                    )
                )


                if arrow[
                    "burn_damage"
                ] > 0:

                    target.apply_burn(
                        arrow[
                            "burn_damage"
                        ],
                        arrow[
                            "burn_time"
                        ]
                    )


                count += 1


                if count >= 3:

                    break


# ============================================================
# COOLDOWN TEXT
# ============================================================

def cooldown_text(
    value
):

    if value <= 0:

        return "READY"


    return (
        f"{value / FPS:.1f}s"
    )


# ============================================================
# HUD
# ============================================================

def draw_hud(
    player,
    level
):

    # HP BAR

    pygame.draw.rect(
        screen,
        DARK_RED,
        (
            20,
            20,
            250,
            25
        )
    )


    hp_width = int(
        250
        *
        max(
            0,
            player.hp
        )
        /
        player.max_hp
    )


    pygame.draw.rect(
        screen,
        GREEN,
        (
            20,
            20,
            hp_width,
            25
        )
    )


    draw_text(
        f"HP {max(0, player.hp)}/{player.max_hp}",
        25,
        20,
        SMALL
    )


    needed = (
        player_data[
            "player_level"
        ]
        *
        100
    )


    draw_text(
        f"Lv {player_data['player_level']}",
        300,
        18,
        SMALL
    )


    draw_text(
        f"XP {player_data['xp']}/{needed}",
        300,
        40,
        SMALL
    )


    draw_text(
        f"Gold {player_data['gold']}",
        415,
        18,
        SMALL,
        GOLD
    )


    draw_text(
        f"Potions {player_data['potions']} [H]",
        415,
        40,
        SMALL
    )


    draw_text(
        f"Mode {player_data['weapon_mode']}",
        590,
        18,
        SMALL,
        GOLD
    )


    draw_text(
        f"Arrow {player_data['arrow_type'].title()}",
        590,
        40,
        SMALL
    )


    draw_text(
        f"Stage {level}",
        960,
        18,
        SMALL
    )


    # ABILITIES

    character_name = (
        player_data[
            "character"
        ]
    )


    character = characters[
        character_name
    ]


    draw_text(
        character_name,
        20,
        70,
        SMALL,
        GOLD
    )


    draw_text(
        (
            f"Z {character['abilities']['Z']['name']}: "
            f"{cooldown_text(player.ability_z_cooldown)}"
        ),
        20,
        92,
        SMALL
    )


    draw_text(
        (
            f"X {character['abilities']['X']['name']}: "
            f"{cooldown_text(player.ability_x_cooldown)}"
        ),
        20,
        114,
        SMALL
    )


    draw_text(
        (
            f"C {character['abilities']['C']['name']}: "
            f"{cooldown_text(player.ability_c_cooldown)}"
        ),
        20,
        136,
        SMALL
    )


    if player.berserk_timer > 0:

        draw_text(
            "BERSERK!",
            400,
            75,
            SMALL,
            RED
        )


    if player.invisible_timer > 0:

        draw_text(
            "INVISIBLE",
            400,
            75,
            SMALL,
            PURPLE
        )


# ============================================================
# BUY ITEM
# ============================================================

def buy_item(
    name,
    dictionary,
    owned_key,
    equipped_key
):

    if name in player_data[
        owned_key
    ]:

        player_data[
            equipped_key
        ] = name


        return


    price = dictionary[
        name
    ]["price"]


    if (
        player_data[
            "gold"
        ]
        >=
        price
    ):

        player_data[
            "gold"
        ] -= price


        player_data[
            owned_key
        ].append(
            name
        )


        player_data[
            equipped_key
        ] = name


# ============================================================
# SHOP
# ============================================================

def shop(
):

    category = "arrow"


    while True:

        screen.fill(
            (
                25,
                20,
                40
            )
        )


        draw_center(
            "BLACKSMITH SHOP",
            20,
            BIG,
            GOLD
        )


        draw_text(
            f"Gold: {player_data['gold']}",
            20,
            80,
            FONT,
            GOLD
        )


        categories = [

            (
                "SWORDS",
                "sword"
            ),

            (
                "BOWS",
                "bow"
            ),

            (
                "ARMOR",
                "armor"
            ),

            (
                "ARROWS",
                "arrow"
            ),

            (
                "UTILITY",
                "utility"
            )
        ]


        tabs = []


        for i, (
            label,
            value
        ) in enumerate(
            categories
        ):

            button = Button(
                20
                +
                i
                *
                210,
                120,
                190,
                45,
                label
            )


            button.draw()


            tabs.append(
                (
                    button,
                    value
                )
            )


        if category == "sword":

            dictionary = weapons

            owned_key = (
                "owned_weapons"
            )

            equipped_key = (
                "weapon"
            )


        elif category == "bow":

            dictionary = bows

            owned_key = (
                "owned_bows"
            )

            equipped_key = (
                "bow"
            )


        elif category == "armor":

            dictionary = armors

            owned_key = (
                "owned_armors"
            )

            equipped_key = (
                "armor"
            )


        elif category == "arrow":

            dictionary = arrow_types

            owned_key = (
                "owned_arrows"
            )

            equipped_key = (
                "arrow_type"
            )


        else:

            dictionary = utilities

            owned_key = (
                "owned_utilities"
            )

            equipped_key = (
                "utility"
            )


        item_buttons = []


        y = 185


        for name, data in dictionary.items():

            if (
                name
                ==
                player_data[
                    equipped_key
                ]
            ):

                status = (
                    "EQUIPPED"
                )

            elif (
                name
                in
                player_data[
                    owned_key
                ]
            ):

                status = (
                    "EQUIP"
                )

            else:

                status = (
                    f"{data['price']}G"
                )


            if category == "sword":

                details = (
                    f"DMG {data['damage']}"
                )


            elif category == "bow":

                details = (
                    f"DMG {data['damage']} "
                    f"SPD {data['speed']}"
                )


            elif category == "armor":

                details = (
                    f"DEF {data['defense']}"
                )


            elif category == "arrow":

                details = (
                    data[
                        "description"
                    ]
                )


            else:

                if data[
                    "type"
                ] == "teleport":

                    details = (
                        "Teleport"
                    )

                else:

                    details = (
                        f"DMG {data['damage']} "
                        f"AOE {data['range']}"
                    )


            display_name = (

                name.title()
                +
                " Arrow"

                if category
                ==
                "arrow"

                else

                name
            )


            button = Button(
                175,
                y,
                750,
                55,
                (
                    f"{display_name} | "
                    f"{details} | "
                    f"{status}"
                )
            )


            button.draw()


            item_buttons.append(
                (
                    button,
                    name
                )
            )


            y += 65


        potion_button = Button(
            920,
            620,
            160,
            45,
            "POTION 50G"
        )


        potion_button.draw()


        draw_text(
            "ESC = Main Menu",
            20,
            665,
            SMALL
        )


        pygame.display.flip()


        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                save_game()

                pygame.quit()

                quit()


            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    save_game()

                    return


            for button, value in tabs:

                if button.clicked(
                    event
                ):

                    category = value


            for button, name in item_buttons:

                if button.clicked(
                    event
                ):

                    buy_item(
                        name,
                        dictionary,
                        owned_key,
                        equipped_key
                    )


            if potion_button.clicked(
                event
            ):

                if (
                    player_data[
                        "gold"
                    ]
                    >=
                    50
                ):

                    player_data[
                        "gold"
                    ] -= 50


                    player_data[
                        "potions"
                    ] += 1


        clock.tick(
            FPS
        )


# ============================================================
# CHARACTER SELECT
# ============================================================

def character_select(
):

    while True:

        screen.fill(
            (
                20,
                24,
                38
            )
        )


        draw_center(
            "SELECT CHARACTER",
            30,
            BIG,
            GOLD
        )


        buttons = []


        x_positions = [

            75,
            335,
            595,
            855
        ]


        for i, (
            name,
            data
        ) in enumerate(
            characters.items()
        ):

            x = (
                x_positions[
                    i
                ]
            )


            card = pygame.Rect(
                x,
                130,
                190,
                420
            )


            pygame.draw.rect(
                screen,
                (
                    45,
                    45,
                    65
                ),
                card,
                border_radius=12
            )


            pygame.draw.rect(
                screen,
                data[
                    "color"
                ],
                card,
                3,
                border_radius=12
            )


            draw_text(
                name,
                x + 50,
                150,
                FONT,
                GOLD
            )


            pygame.draw.circle(
                screen,
                data[
                    "color"
                ],
                (
                    x + 95,
                    220
                ),
                40
            )


            draw_text(
                (
                    f"HP bonus: "
                    f"{data['hp_bonus']:+}"
                ),
                x + 15,
                280,
                SMALL
            )


            draw_text(
                (
                    f"Speed: "
                    f"{data['speed_bonus']:+}"
                ),
                x + 15,
                305,
                SMALL
            )


            draw_text(
                "Abilities:",
                x + 15,
                345,
                SMALL,
                GOLD
            )


            draw_text(
                (
                    "Z "
                    +
                    data[
                        "abilities"
                    ][
                        "Z"
                    ][
                        "name"
                    ]
                ),
                x + 15,
                375,
                SMALL
            )


            draw_text(
                (
                    "X "
                    +
                    data[
                        "abilities"
                    ][
                        "X"
                    ][
                        "name"
                    ]
                ),
                x + 15,
                400,
                SMALL
            )


            draw_text(
                (
                    "C "
                    +
                    data[
                        "abilities"
                    ][
                        "C"
                    ][
                        "name"
                    ]
                ),
                x + 15,
                425,
                SMALL
            )


            select_button = Button(
                x + 20,
                485,
                150,
                45,
                (
                    "SELECTED"
                    if player_data[
                        "character"
                    ] == name
                    else
                    "SELECT"
                )
            )


            select_button.draw()


            buttons.append(
                (
                    select_button,
                    name
                )
            )


        draw_text(
            "ESC = Main Menu",
            20,
            665,
            SMALL
        )


        pygame.display.flip()


        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                save_game()

                pygame.quit()

                quit()


            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    save_game()

                    return


            for button, name in buttons:

                if button.clicked(
                    event
                ):

                    player_data[
                        "character"
                    ] = name


                    save_game()


        clock.tick(
            FPS
        )


# ============================================================
# PLAY LEVEL
# ============================================================

def play_level(
    level_number
):

    data = levels[
        level_number
    ]


    player = Player()


    walls = create_map(
        level_number
    )


    enemies = []


    for i in range(
        data[
            "enemy_count"
        ]
    ):

        enemies.append(

            Enemy(
                random.randint(
                    500,
                    1000
                ),

                random.randint(
                    160,
                    610
                ),

                data[
                    "enemy_hp"
                ],

                data[
                    "enemy_damage"
                ],

                level_number,

                ranged=(
                    random.random()
                    <
                    data[
                        "ranged_chance"
                    ]
                )
            )
        )


    chests = [

        Chest(
            random.randint(
                300,
                950
            ),
            random.randint(
                180,
                600
            )
        ),

        Chest(
            random.randint(
                300,
                950
            ),
            random.randint(
                180,
                600
            )
        )
    ]


    projectiles = []

    explosions = []

    lightning_effects = []


    boss = None

    boss_spawned = False


    message = ""

    message_timer = 0


    while True:

        clock.tick(
            FPS
        )


        # ====================================================
        # EVENTS
        # ====================================================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                save_game()

                pygame.quit()

                quit()


            if event.type != pygame.KEYDOWN:

                continue


            if event.key == pygame.K_ESCAPE:

                return "menu"


            # SWITCH WEAPON

            if event.key == pygame.K_q:

                if (
                    player_data[
                        "weapon_mode"
                    ]
                    ==
                    "sword"
                ):

                    player_data[
                        "weapon_mode"
                    ] = "bow"

                else:

                    player_data[
                        "weapon_mode"
                    ] = "sword"


            # ARROW HOTKEYS

            arrow_keys = {

                pygame.K_1:
                    "regular",

                pygame.K_2:
                    "lightning",

                pygame.K_3:
                    "exploding",

                pygame.K_4:
                    "homing",

                pygame.K_5:
                    "fire",

                pygame.K_6:
                    "super"
            }


            if event.key in arrow_keys:

                wanted = (
                    arrow_keys[
                        event.key
                    ]
                )


                if wanted in player_data[
                    "owned_arrows"
                ]:

                    player_data[
                        "arrow_type"
                    ] = wanted


            # NORMAL ATTACK

            if event.key == pygame.K_SPACE:

                if (
                    player_data[
                        "weapon_mode"
                    ]
                    ==
                    "sword"
                ):

                    player.sword_attack(
                        enemies,
                        boss
                    )

                else:

                    player.shoot(
                        projectiles
                    )


            # Z ABILITY

            if event.key == pygame.K_z:

                player.use_ability(
                    "Z",
                    enemies,
                    boss,
                    projectiles,
                    explosions,
                    lightning_effects,
                    walls
                )


            # X ABILITY

            if event.key == pygame.K_x:

                player.use_ability(
                    "X",
                    enemies,
                    boss,
                    projectiles,
                    explosions,
                    lightning_effects,
                    walls
                )


            # C ABILITY

            if event.key == pygame.K_c:

                player.use_ability(
                    "C",
                    enemies,
                    boss,
                    projectiles,
                    explosions,
                    lightning_effects,
                    walls
                )


            # POTION

            if event.key == pygame.K_h:

                if (
                    player_data[
                        "potions"
                    ]
                    >
                    0
                    and
                    player.hp
                    <
                    player.max_hp
                ):

                    player_data[
                        "potions"
                    ] -= 1


                    player.hp = min(
                        player.max_hp,
                        player.hp + 45
                    )


            # ENDER PEARL

            if event.key == pygame.K_r:

                if (
                    player_data[
                        "utility"
                    ]
                    ==
                    "Ender Pearl"
                ):

                    player.teleport(
                        walls
                    )


            # HAMMER

            if event.key == pygame.K_f:

                if (
                    "Hammer"
                    in
                    player_data[
                        "utility"
                    ]
                ):

                    player.hammer(
                        enemies,
                        boss,
                        explosions
                    )


            # CHEST

            if event.key == pygame.K_e:

                for chest in chests:

                    reward = chest.open(
                        player
                    )


                    if reward:

                        message = reward

                        message_timer = 120


        # ====================================================
        # PLAYER
        # ====================================================

        player.update(
            walls
        )


        # ====================================================
        # ENEMIES
        # ====================================================

        for enemy in enemies[:]:

            enemy.update(
                player,
                walls,
                projectiles
            )


            if enemy.hp <= 0:

                player_data[
                    "gold"
                ] += (
                    15
                    +
                    level_number
                    *
                    10
                )


                player_data[
                    "xp"
                ] += (
                    15
                    +
                    level_number
                    *
                    8
                )


                enemies.remove(
                    enemy
                )


                check_level_up()


        # ====================================================
        # BOSS SPAWN
        # ====================================================

        if (
            not enemies
            and
            not boss_spawned
        ):

            boss_spawned = True


            boss = Enemy(
                900,
                330,

                data[
                    "boss_hp"
                ],

                data[
                    "boss_damage"
                ],

                level_number,

                ranged=(
                    level_number
                    >=
                    3
                ),

                boss=True,

                boss_name=data[
                    "boss_name"
                ]
            )


            message = (
                "BOSS: "
                +
                data[
                    "boss_name"
                ]
            )


            message_timer = 180


        # ====================================================
        # BOSS
        # ====================================================

        if boss:

            boss.update(
                player,
                walls,
                projectiles
            )


            boss.boss_ability(
                player,
                enemies,
                projectiles
            )


        # ====================================================
        # PROJECTILES
        # ====================================================

        for projectile in projectiles[:]:

            projectile.update(
                enemies,
                boss
            )


            # ENEMY PROJECTILE

            if projectile.enemy:

                if projectile.rect.colliderect(
                    player.rect
                ):

                    defense = armors[
                        player_data[
                            "armor"
                        ]
                    ]["defense"]


                    player.hp -= max(
                        1,
                        projectile.damage
                        -
                        defense
                    )


                    if (
                        projectile.projectile_type
                        ==
                        "ice"
                    ):

                        player.slow_timer = (
                            3
                            *
                            FPS
                        )


                    if projectile in projectiles:

                        projectiles.remove(
                            projectile
                        )


                    continue


            # PLAYER PROJECTILE

            else:

                target = None


                for enemy in enemies:

                    if projectile.rect.colliderect(
                        enemy.rect
                    ):

                        target = enemy

                        break


                if (
                    target is None
                    and
                    boss
                    and
                    projectile.rect.colliderect(
                        boss.rect
                    )
                ):

                    target = boss


                if target:

                    if (
                        projectile.projectile_type
                        in
                        arrow_types
                    ):

                        apply_arrow_hit(
                            projectile,
                            target,
                            enemies,
                            boss,
                            explosions,
                            lightning_effects
                        )


                    else:

                        target.hp -= (
                            projectile.damage
                        )


                        if (
                            projectile.projectile_type
                            ==
                            "fire"
                        ):

                            target.apply_burn(
                                6,
                                240
                            )


                    if projectile in projectiles:

                        projectiles.remove(
                            projectile
                        )


                    continue


            # =================================================
            # WALL COLLISION
            # =================================================

            hit_wall = False


            for wall in walls:

                if projectile.rect.colliderect(
                    wall
                ):

                    hit_wall = True

                    break


            if hit_wall:

                arrow_hit_wall(
                    projectile,
                    enemies,
                    boss,
                    explosions,
                    lightning_effects
                )


                if projectile in projectiles:

                    projectiles.remove(
                        projectile
                    )


                continue


            if projectile.off_screen():

                if projectile in projectiles:

                    projectiles.remove(
                        projectile
                    )


        # ====================================================
        # DEAD ENEMIES FROM ABILITIES / FIRE
        # ====================================================

        for enemy in enemies[:]:

            if enemy.hp <= 0:

                player_data[
                    "gold"
                ] += (
                    15
                    +
                    level_number
                    *
                    10
                )


                player_data[
                    "xp"
                ] += (
                    15
                    +
                    level_number
                    *
                    8
                )


                enemies.remove(
                    enemy
                )


                check_level_up()


        # ====================================================
        # BOSS DEATH
        # ====================================================

        if (
            boss
            and
            boss.hp <= 0
        ):

            player_data[
                "gold"
            ] += (
                level_number
                *
                200
            )


            player_data[
                "xp"
            ] += (
                level_number
                *
                100
            )


            check_level_up()


            if (
                level_number
                ==
                player_data[
                    "unlocked_level"
                ]
                and
                level_number
                <
                len(
                    levels
                )
            ):

                player_data[
                    "unlocked_level"
                ] += 1


            save_game()


            return "win"


        # ====================================================
        # EFFECTS
        # ====================================================

        for explosion in explosions[:]:

            explosion.update()


            if explosion.timer <= 0:

                explosions.remove(
                    explosion
                )


        for effect in lightning_effects[:]:

            effect.update()


            if effect.timer <= 0:

                lightning_effects.remove(
                    effect
                )


        # ====================================================
        # PLAYER DEATH
        # ====================================================

        if player.hp <= 0:

            return "dead"


        # ====================================================
        # DRAW
        # ====================================================

        screen.fill(
            data[
                "background"
            ]
        )


        draw_walls(
            walls,
            level_number
        )


        for chest in chests:

            chest.draw()


        for enemy in enemies:

            enemy.draw()


        if boss:

            boss.draw()


            draw_center(
                data[
                    "boss_name"
                ],
                85,
                SMALL,
                RED
            )


        for projectile in projectiles:

            projectile.draw()


        for explosion in explosions:

            explosion.draw()


        for effect in lightning_effects:

            effect.draw()


        player.draw()


        draw_hud(
            player,
            level_number
        )


        draw_center(
            data[
                "name"
            ],
            60,
            FONT
        )


        draw_text(
            "WASD Move | SPACE Attack | Q Sword/Bow | Z X C Abilities",
            10,
            630,
            SMALL
        )


        draw_text(
            "1 Regular | 2 Lightning | 3 Exploding | 4 Homing | 5 Fire | 6 SUPER",
            10,
            652,
            SMALL
        )


        draw_text(
            "H Potion | E Chest | R Ender Pearl | F Hammer | ESC Exit",
            10,
            674,
            SMALL
        )


        if message_timer > 0:

            message_timer -= 1


            pygame.draw.rect(
                screen,
                BLACK,
                (
                    WIDTH // 2 - 220,
                    555,
                    440,
                    45
                ),
                border_radius=8
            )


            draw_center(
                message,
                565,
                SMALL,
                GOLD
            )


        pygame.display.flip()


# ============================================================
# RESULT SCREEN
# ============================================================

def result_screen(
    title,
    message
):

    button = Button(
        WIDTH // 2 - 150,
        450,
        300,
        60,
        "CONTINUE"
    )


    while True:

        screen.fill(
            (
                20,
                20,
                30
            )
        )


        draw_center(
            title,
            180,
            HUGE,
            GOLD
        )


        draw_center(
            message,
            290
        )


        button.draw()


        pygame.display.flip()


        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                save_game()

                pygame.quit()

                quit()


            if button.clicked(
                event
            ):

                return


        clock.tick(
            FPS
        )


# ============================================================
# LEVEL SELECT
# ============================================================

def level_select(
):

    while True:

        screen.fill(
            (
                20,
                35,
                50
            )
        )


        draw_center(
            "SELECT LEVEL",
            30,
            BIG,
            GOLD
        )


        buttons = []


        y = 120


        for number, data in levels.items():

            if (
                number
                <=
                player_data[
                    "unlocked_level"
                ]
            ):

                label = (
                    f"Level {number}: "
                    f"{data['name']} | "
                    f"Boss: {data['boss_name']}"
                )

            else:

                label = (
                    f"Level {number}: LOCKED"
                )


            button = Button(
                250,
                y,
                600,
                70,
                label
            )


            button.draw()


            buttons.append(
                (
                    button,
                    number
                )
            )


            y += 90


        draw_text(
            (
                "Character: "
                +
                player_data[
                    "character"
                ]
            ),
            20,
            625,
            SMALL,
            GOLD
        )


        draw_text(
            "ESC = Main Menu",
            20,
            660,
            SMALL
        )


        pygame.display.flip()


        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                save_game()

                pygame.quit()

                quit()


            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    return


            for button, number in buttons:

                if button.clicked(
                    event
                ):

                    if (
                        number
                        <=
                        player_data[
                            "unlocked_level"
                        ]
                    ):

                        result = play_level(
                            number
                        )


                        if result == "win":

                            result_screen(
                                "VICTORY!",
                                (
                                    "You defeated "
                                    +
                                    levels[
                                        number
                                    ][
                                        "boss_name"
                                    ]
                                    +
                                    "!"
                                )
                            )


                        elif result == "dead":

                            result_screen(
                                "YOU DIED",
                                "Upgrade your gear or try another character!"
                            )


        clock.tick(
            FPS
        )


# ============================================================
# MAIN MENU
# ============================================================

def main_menu(
):

    while True:

        screen.fill(
            (
                18,
                18,
                32
            )
        )


        draw_center(
            "SWORD ADVENTURE",
            65,
            HUGE,
            GOLD
        )


        play_button = Button(
            380,
            180,
            340,
            55,
            "PLAY"
        )


        character_button = Button(
            380,
            250,
            340,
            55,
            "CHARACTERS"
        )


        shop_button = Button(
            380,
            320,
            340,
            55,
            "SHOP"
        )


        save_button = Button(
            380,
            390,
            340,
            55,
            "SAVE GAME"
        )


        load_button = Button(
            380,
            460,
            340,
            55,
            "LOAD GAME"
        )


        quit_button = Button(
            380,
            530,
            340,
            55,
            "QUIT"
        )


        play_button.draw()

        character_button.draw()

        shop_button.draw()

        save_button.draw()

        load_button.draw()

        quit_button.draw()


        needed = (
            player_data[
                "player_level"
            ]
            *
            100
        )


        draw_center(
            (
                f"{player_data['character']} | "
                f"Lv {player_data['player_level']} | "
                f"XP {player_data['xp']}/{needed} | "
                f"Gold {player_data['gold']} | "
                f"Potions {player_data['potions']}"
            ),
            610,
            SMALL,
            WHITE
        )


        pygame.display.flip()


        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                save_game()

                pygame.quit()

                return


            if play_button.clicked(
                event
            ):

                level_select()


            elif character_button.clicked(
                event
            ):

                character_select()


            elif shop_button.clicked(
                event
            ):

                shop()


            elif save_button.clicked(
                event
            ):

                save_game()


                result_screen(
                    "SAVED",
                    "Your progress was saved."
                )


            elif load_button.clicked(
                event
            ):

                load_game()


                result_screen(
                    "LOADED",
                    "Your save was loaded."
                )


            elif quit_button.clicked(
                event
            ):

                save_game()

                pygame.quit()

                return


        clock.tick(
            FPS
        )


# ============================================================
# START GAME
# ============================================================

load_game()

main_menu()