import pygame
import asyncio
from online_net import open_game_connection
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
BIG = pygame.font.SysFont("arial", 46)
HUGE = pygame.font.SysFont("arial", 60)

SAVE_FILE = "sword_save.json"

GROUND_TOP = 150

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
LIGHT_GRAY = (205, 205, 205)
DARK_GRAY = (55, 55, 55)

BROWN = (125, 75, 35)
DARK_BROWN = (80, 50, 30)

PURPLE = (150, 60, 200)

ORANGE = (245, 120, 30)
CYAN = (100, 220, 255)
YELLOW = (255, 235, 80)

PINK = (230, 90, 170)


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
        "speed_bonus": 1,
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
# WEAPONS
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
        "description": "Area explosion"
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
        "name": "Enchanted Forest",
        "biome": "forest",
        "world_width": 4300,

        "background": (60, 120, 70),

        "enemy_hp": 45,
        "enemy_damage": 7,

        "boss_name": "Goblin King",
        "boss_hp": 300,
        "boss_damage": 14
    },

    2: {
        "name": "Haunted Woods",
        "biome": "dark_forest",
        "world_width": 4800,

        "background": (35, 65, 45),

        "enemy_hp": 75,
        "enemy_damage": 10,

        "boss_name": "Forest Troll",
        "boss_hp": 450,
        "boss_damage": 18
    },

    3: {
        "name": "Frozen Mountains",
        "biome": "snow",
        "world_width": 5200,

        "background": (100, 145, 180),

        "enemy_hp": 110,
        "enemy_damage": 14,

        "boss_name": "Ice Knight",
        "boss_hp": 650,
        "boss_damage": 23
    },

    4: {
        "name": "Volcanic Wasteland",
        "biome": "volcano",
        "world_width": 5700,

        "background": (90, 42, 28),

        "enemy_hp": 155,
        "enemy_damage": 18,

        "boss_name": "Fire Demon",
        "boss_hp": 900,
        "boss_damage": 28
    },

    5: {
        "name": "Dragon Kingdom",
        "biome": "dragon",
        "world_width": 6300,

        "background": (55, 35, 75),

        "enemy_hp": 210,
        "enemy_damage": 25,

        "boss_name": "Ancient Dragon",
        "boss_hp": 1500,
        "boss_damage": 36
    }
}


# ============================================================
# SAVE DATA
# ============================================================

default_data = {

    "player_name": "Player",
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
# SAVE FUNCTIONS
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
            "player_name",
            "Player"
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

        if (
            event.type != pygame.MOUSEBUTTONDOWN
            or
            event.button != 1
        ):
            return False

        # Browser builds can report mouse coordinates differently.
        # pygame.mouse.get_pos() gives the current position in the
        # game's logical canvas coordinates, which works more reliably
        # with pygbag / itch.io.
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            return True

        # Keep event.pos as a fallback for desktop builds.
        if hasattr(event, "pos"):
            return self.rect.collidepoint(event.pos)

        return False


# ============================================================
# CAMERA
# ============================================================

class Camera:

    def __init__(
        self,
        world_width
    ):

        self.x = 0

        self.world_width = (
            world_width
        )


    def update(
        self,
        player
    ):

        self.x = (
            player.rect.centerx
            -
            WIDTH // 2
        )

        self.x = max(
            0,
            min(
                self.x,
                self.world_width
                -
                WIDTH
            )
        )


    def sx(
        self,
        world_x
    ):

        return int(
            world_x
            -
            self.x
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


    def draw(
        self,
        camera
    ):

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
                camera.sx(
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
                camera.sx(
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


    def draw(
        self,
        camera
    ):

        start = (
            camera.sx(
                self.start[0]
            ),
            self.start[1]
        )

        end = (
            camera.sx(
                self.end[0]
            ),
            self.end[1]
        )

        points = [
            start
        ]

        for i in range(
            1,
            6
        ):

            ratio = i / 6

            x = (
                start[0]
                +
                (
                    end[0]
                    -
                    start[0]
                )
                *
                ratio
            )

            y = (
                start[1]
                +
                (
                    end[1]
                    -
                    start[1]
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
            end
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
            target_y
            -
            y,

            target_x
            -
            x
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


    def draw(
        self,
        camera
    ):

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

        cx = camera.sx(
            self.rect.centerx
        )

        cy = self.rect.centery

        pygame.draw.line(
            screen,
            color,
            (
                cx,
                cy
            ),
            (
                cx
                -
                int(
                    self.dx
                    *
                    2
                ),

                cy
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
            (
                cx,
                cy
            ),
            5
        )


    def off_world(
        self,
        world_width
    ):

        return (
            self.x < -100
            or
            self.x
            >
            world_width
            +
            100
            or
            self.y < 80
            or
            self.y
            >
            HEIGHT
            +
            100
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
        zone,
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

        self.zone = zone

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

        self.special_timer = (
            3
            *
            FPS
        )

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
        projectiles,
        active=True
    ):

        self.update_burn()

        if not active:

            return

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

        old_x = self.x

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

        old_y = self.y

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
                ][
                    "defense"
                ]

                player.hp -= max(
                    1,
                    self.damage
                    -
                    defense
                )

                self.attack_timer = 50


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

                        40,

                        7,

                        1,

                        99
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
            ) < 200:

                defense = armors[
                    player_data[
                        "armor"
                    ]
                ][
                    "defense"
                ]

                player.hp -= max(
                    1,
                    35
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

                    22,

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
                        700,

                        self.rect.centery
                        +
                        math.sin(
                            angle
                        )
                        *
                        700,

                        26,

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
                            800,

                            self.rect.centery
                            +
                            math.sin(
                                angle
                            )
                            *
                            800,

                            32,

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
                    150
                )

                self.y += (
                    dy
                    /
                    distance
                    *
                    150
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

                    player.hp -= 40

            else:

                for i in range(
                    3
                ):

                    enemies.append(

                        Enemy(
                            self.rect.x
                            +
                            random.randint(
                                -140,
                                140
                            ),

                            self.rect.y
                            +
                            random.randint(
                                -120,
                                120
                            ),

                            100,

                            17,

                            5,

                            99,

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


    def draw(
        self,
        camera
    ):

        x = camera.sx(
            self.rect.x
        )

        draw_rect = pygame.Rect(
            x,
            self.rect.y,
            self.rect.width,
            self.rect.height
        )

        if self.boss:

            body_color = (
                DARK_RED
            )

            head_color = (
                RED
            )

        elif self.ranged:

            body_color = (
                PURPLE
            )

            head_color = (
                80,
                200,
                90
            )

        else:

            body_color = (
                DARK_GREEN
            )

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
                draw_rect
            )

        else:

            pygame.draw.rect(
                screen,
                body_color,
                draw_rect,
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
                draw_rect.centerx,
                draw_rect.y
                +
                8
            ),
            head_radius
        )

        pygame.draw.circle(
            screen,
            RED,
            (
                draw_rect.centerx
                -
                5,
                draw_rect.y
                +
                7
            ),
            2
        )

        pygame.draw.circle(
            screen,
            RED,
            (
                draw_rect.centerx
                +
                5,
                draw_rect.y
                +
                7
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
                        draw_rect.centerx - 20,
                        draw_rect.y - 8
                    ),

                    (
                        draw_rect.centerx - 10,
                        draw_rect.y - 25
                    ),

                    (
                        draw_rect.centerx,
                        draw_rect.y - 8
                    ),

                    (
                        draw_rect.centerx + 10,
                        draw_rect.y - 25
                    ),

                    (
                        draw_rect.centerx + 20,
                        draw_rect.y - 8
                    )
                ]
            )

        if self.ranged:

            pygame.draw.arc(
                screen,
                BROWN,
                (
                    draw_rect.x - 7,
                    draw_rect.y + 15,
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
                    draw_rect.centerx,
                    draw_rect.y - 5
                ),
                9
            )

            pygame.draw.circle(
                screen,
                YELLOW,
                (
                    draw_rect.centerx,
                    draw_rect.y - 8
                ),
                5
            )

        if self.freeze_timer > 0:

            pygame.draw.circle(
                screen,
                CYAN,
                draw_rect.center,
                max(
                    20,
                    draw_rect.width // 2
                ),
                2
            )

        pygame.draw.rect(
            screen,
            DARK_RED,
            (
                draw_rect.x,
                draw_rect.y - 12,
                draw_rect.width,
                7
            )
        )

        hp_width = int(
            draw_rect.width
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
                draw_rect.x,
                draw_rect.y - 12,
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

        self.y = 380

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


    def update(
        self,
        walls,
        gates,
        world_width
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

        collision_objects = (
            walls
            +
            gates
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

        for wall in collision_objects:

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

        for wall in collision_objects:

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
                world_width
                -
                self.rect.width,
                self.x
            )
        )

        self.y = max(
            190,
            min(
                HEIGHT
                -
                self.rect.height
                -
                20,
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
        ][
            "damage"
        ]

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


    def teleport(
        self,
        collision_objects,
        world_width
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
                world_width
                -
                self.rect.width,
                self.x
            )
        )

        self.rect.x = int(
            self.x
        )

        for wall in collision_objects:

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

        name = player_data[
            "utility"
        ]

        if name not in utilities:

            return

        data = utilities[
            name
        ]

        if data[
            "type"
        ] != "hammer":

            return

        self.utility_cooldown = 90

        self.hammer_timer = 20

        radius = data[
            "range"
        ]

        damage = data[
            "damage"
        ]

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

                enemy.hp -= (
                    damage
                )

        if (
            boss
            and
            math.dist(
                self.rect.center,
                boss.rect.center
            ) <= radius
        ):

            boss.hp -= (
                damage
            )


    def use_ability(
        self,
        key,
        enemies,
        boss,
        projectiles,
        explosions,
        lightning_effects,
        collision_objects,
        world_width
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

            # KNIGHT SHIELD RUSH
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
                        world_width
                        -
                        self.rect.width,
                        self.x
                    )
                )

                self.rect.x = int(
                    self.x
                )

                for wall in collision_objects:

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


            # RANGER TRIPLE SHOT
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


            # MAGE FIREBALL
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


            # SHADOW TELEPORT STRIKE
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

                        key=lambda enemy:

                        math.dist(
                            self.rect.center,
                            enemy.rect.center
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

            # KNIGHT GROUND SLAM
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


            # RANGER DASH
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
                        world_width
                        -
                        self.rect.width,
                        self.x
                    )
                )

                self.rect.x = int(
                    self.x
                )

                for wall in collision_objects:

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


            # MAGE FREEZE BLAST
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


            # SHADOW VANISH
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

            # KNIGHT BERSERK
            if character_name == "Knight":

                self.berserk_timer = (
                    5
                    *
                    FPS
                )


            # RANGER ARROW STORM
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

                        projectiles.append(

                            Projectile(
                                target.rect.centerx
                                +
                                random.randint(
                                    -100,
                                    100
                                ),

                                target.rect.centery
                                -
                                300
                                -
                                random.randint(
                                    0,
                                    80
                                ),

                                target.rect.centerx,
                                target.rect.centery,

                                damage,

                                10,

                                arrow_name
                            )
                        )


            # MAGE LIGHTNING NOVA
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


            # SHADOW SPIN ATTACK
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


    def draw_body(
        self,
        camera
    ):

        x = camera.sx(
            self.rect.x
        )

        draw_rect = pygame.Rect(
            x,
            self.rect.y,
            self.rect.width,
            self.rect.height
        )

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

        if self.invisible_timer > 0:

            armor_color = (
                90,
                90,
                90
            )

        pygame.draw.rect(
            screen,
            DARK_BLUE,
            (
                draw_rect.x + 7,
                draw_rect.y + 42,
                12,
                16
            )
        )

        pygame.draw.rect(
            screen,
            DARK_BLUE,
            (
                draw_rect.x + 26,
                draw_rect.y + 42,
                12,
                16
            )
        )

        pygame.draw.rect(
            screen,
            armor_color,
            (
                draw_rect.x + 5,
                draw_rect.y + 15,
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
                draw_rect.centerx,
                draw_rect.y + 10
            ),
            13
        )

        pygame.draw.circle(
            screen,
            BLACK,
            (
                draw_rect.centerx - 5,
                draw_rect.y + 8
            ),
            2
        )

        pygame.draw.circle(
            screen,
            BLACK,
            (
                draw_rect.centerx + 5,
                draw_rect.y + 8
            ),
            2
        )

        if character_name == "Knight":

            pygame.draw.arc(
                screen,
                LIGHT_GRAY,
                (
                    draw_rect.centerx - 14,
                    draw_rect.y - 3,
                    28,
                    22
                ),
                math.pi,
                2 * math.pi,
                5
            )

        elif character_name == "Ranger":

            pygame.draw.arc(
                screen,
                GREEN,
                (
                    draw_rect.centerx - 15,
                    draw_rect.y - 4,
                    30,
                    25
                ),
                math.pi,
                2 * math.pi,
                6
            )

        elif character_name == "Mage":

            pygame.draw.polygon(
                screen,
                PURPLE,
                [
                    (
                        draw_rect.centerx,
                        draw_rect.y - 25
                    ),

                    (
                        draw_rect.centerx - 17,
                        draw_rect.y + 3
                    ),

                    (
                        draw_rect.centerx + 17,
                        draw_rect.y + 3
                    )
                ]
            )

        elif character_name == "Shadow":

            pygame.draw.rect(
                screen,
                DARK_GRAY,
                (
                    draw_rect.centerx - 13,
                    draw_rect.y,
                    26,
                    9
                )
            )

        return draw_rect


    def draw_sword(
        self,
        draw_rect
    ):

        center_x = (
            draw_rect.centerx
        )

        center_y = (
            draw_rect.centery
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
        self,
        draw_rect
    ):

        if self.facing == 1:

            bow_rect = pygame.Rect(
                draw_rect.right - 5,
                draw_rect.centery - 25,
                28,
                50
            )

        else:

            bow_rect = pygame.Rect(
                draw_rect.left - 23,
                draw_rect.centery - 25,
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
        self,
        draw_rect
    ):

        if self.hammer_timer <= 0:

            return

        end_x = (
            draw_rect.centerx
            +
            self.facing
            *
            55
        )

        end_y = (
            draw_rect.centery
            -
            30
        )

        pygame.draw.line(
            screen,
            BROWN,
            draw_rect.center,
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
        self,
        camera
    ):

        draw_rect = self.draw_body(
            camera
        )

        # Floating player name + health bar
        name_text = str(player_data.get("player_name", "Player"))[:14]
        name_surface = SMALL.render(name_text, True, WHITE)
        name_x = draw_rect.centerx - name_surface.get_width() // 2
        name_y = draw_rect.top - 34
        screen.blit(name_surface, (name_x, name_y))

        bar_w = 54
        bar_h = 7
        bar_x = draw_rect.centerx - bar_w // 2
        bar_y = draw_rect.top - 15

        pygame.draw.rect(screen, (45, 20, 20), (bar_x, bar_y, bar_w, bar_h))
        hp_ratio = max(0, min(1, self.hp / max(1, self.max_hp)))
        pygame.draw.rect(
            screen,
            GREEN,
            (bar_x, bar_y, int(bar_w * hp_ratio), bar_h)
        )
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_w, bar_h), 1)

        if (
            player_data[
                "weapon_mode"
            ]
            ==
            "sword"
        ):

            self.draw_sword(
                draw_rect
            )

        else:

            self.draw_bow(
                draw_rect
            )

        self.draw_hammer(
            draw_rect
        )


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
        self,
        camera
    ):

        x = camera.sx(
            self.rect.x
        )

        rect = pygame.Rect(
            x,
            self.rect.y,
            self.rect.width,
            self.rect.height
        )

        if self.opened:

            pygame.draw.rect(
                screen,
                DARK_GRAY,
                rect
            )

        else:

            pygame.draw.rect(
                screen,
                BROWN,
                rect,
                border_radius=5
            )

            pygame.draw.line(
                screen,
                GOLD,
                (
                    rect.x,
                    rect.centery
                ),
                (
                    rect.right,
                    rect.centery
                ),
                3
            )

            pygame.draw.rect(
                screen,
                GOLD,
                (
                    rect.centerx - 4,
                    rect.centery - 3,
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
# ADVENTURE WORLD
# ============================================================

class RiverCrossing:

    def __init__(self, x, bridge_y, width=120):
        self.x = x
        self.bridge_y = bridge_y
        self.width = width
        self.bridge_height = 120

    def collision_walls(self):
        top_height = max(0, self.bridge_y - self.bridge_height // 2 - GROUND_TOP)
        bottom_y = self.bridge_y + self.bridge_height // 2
        bottom_height = max(0, HEIGHT - bottom_y)
        return [
            pygame.Rect(self.x, GROUND_TOP, self.width, top_height),
            pygame.Rect(self.x, bottom_y, self.width, bottom_height)
        ]

    def draw(self, camera):
        sx = camera.sx(self.x)
        if sx < -self.width - 40 or sx > WIDTH + 40:
            return

        # Water
        pygame.draw.rect(
            screen,
            (45, 120, 185),
            (sx, GROUND_TOP, self.width, HEIGHT - GROUND_TOP)
        )

        # Moving-looking wave marks
        for y in range(GROUND_TOP + 18, HEIGHT, 34):
            offset = ((y // 34) % 2) * 18
            pygame.draw.line(
                screen,
                (105, 190, 235),
                (sx + 12 + offset, y),
                (sx + self.width - 15, y),
                2
            )

        # Wooden bridge
        bridge_top = self.bridge_y - self.bridge_height // 2
        pygame.draw.rect(
            screen,
            DARK_BROWN,
            (sx - 12, bridge_top - 8, self.width + 24, self.bridge_height + 16),
            border_radius=5
        )
        pygame.draw.rect(
            screen,
            BROWN,
            (sx - 7, bridge_top, self.width + 14, self.bridge_height),
            border_radius=4
        )

        for plank_y in range(bridge_top + 8, bridge_top + self.bridge_height, 18):
            pygame.draw.line(
                screen,
                (165, 115, 65),
                (sx - 4, plank_y),
                (sx + self.width + 4, plank_y),
                3
            )

        pygame.draw.line(screen, DARK_BROWN, (sx - 10, bridge_top), (sx - 10, bridge_top + self.bridge_height), 5)
        pygame.draw.line(screen, DARK_BROWN, (sx + self.width + 10, bridge_top), (sx + self.width + 10, bridge_top + self.bridge_height), 5)


class AdventureSign:

    def __init__(self, x, y, line1, line2=""):
        self.x = x
        self.y = y
        self.line1 = line1
        self.line2 = line2

    def draw(self, camera):
        sx = camera.sx(self.x)
        if sx < -160 or sx > WIDTH + 160:
            return

        pygame.draw.rect(screen, DARK_BROWN, (sx - 5, self.y, 10, 70))
        pygame.draw.rect(screen, BROWN, (sx - 76, self.y - 45, 152, 52), border_radius=4)
        pygame.draw.rect(screen, DARK_BROWN, (sx - 76, self.y - 45, 152, 52), 3, border_radius=4)
        draw_centered = SMALL.render(self.line1, True, WHITE)
        screen.blit(draw_centered, draw_centered.get_rect(center=(sx, self.y - 30)))
        if self.line2:
            second = SMALL.render(self.line2, True, GOLD)
            screen.blit(second, second.get_rect(center=(sx, self.y - 12)))


class HiddenPath:

    def __init__(self, points, name="Secret Trail"):
        # points are WORLD coordinates.  The normal road is broad and tan;
        # hidden treasure trails are deliberately narrow, dark and crooked.
        self.points = points
        self.name = name

    def draw(self, camera):
        screen_points = [(camera.sx(x), y) for x, y in self.points]

        xs = [p[0] for p in screen_points]
        if max(xs) < -180 or min(xs) > WIDTH + 180:
            return

        # Dark earth border makes the secret path very different from the
        # big main road.
        if len(screen_points) >= 2:
            pygame.draw.lines(
                screen,
                (64, 71, 45),
                False,
                screen_points,
                30
            )
            pygame.draw.lines(
                screen,
                (103, 88, 58),
                False,
                screen_points,
                20
            )
            pygame.draw.lines(
                screen,
                (133, 112, 72),
                False,
                screen_points,
                5
            )

        # Small moss/stone markers make it look like an old forgotten trail.
        for segment in range(len(screen_points) - 1):
            x1, y1 = screen_points[segment]
            x2, y2 = screen_points[segment + 1]
            for i in range(1, 6):
                t = i / 6
                px = int(x1 + (x2 - x1) * t)
                py = int(y1 + (y2 - y1) * t)
                pygame.draw.circle(screen, (92, 118, 67), (px, py), 4)
                pygame.draw.circle(screen, (170, 148, 95), (px + 5, py - 3), 2)

        # Bushes partly hide the entrance, so it feels secret without being
        # impossible to find.
        entrance_x, entrance_y = screen_points[0]
        for ox, oy in [(-14, -13), (9, -16), (-4, 12)]:
            pygame.draw.circle(screen, (30, 104, 49), (entrance_x + ox, entrance_y + oy), 11)
            pygame.draw.circle(screen, (45, 132, 61), (entrance_x + ox - 3, entrance_y + oy - 3), 5)

        # Treasure glow at the far end.
        end_x, end_y = screen_points[-1]
        pulse = 8 + int(3 * math.sin(pygame.time.get_ticks() / 180.0))
        pygame.draw.circle(screen, GOLD, (end_x, end_y), pulse, 2)


class EnemyCamp:

    def __init__(self, x, y, zone, name, reward):
        self.x = x
        self.y = y
        self.zone = zone
        self.name = name
        self.reward = reward
        self.rewarded = False

    def cleared(self, enemies):
        return not any(enemy.hp > 0 and enemy.zone == self.zone for enemy in enemies)

    def claim_reward(self, enemies):
        if not self.rewarded and self.cleared(enemies):
            self.rewarded = True
            return self.reward
        return 0

    def draw(self, camera, enemies):
        sx = camera.sx(self.x)
        if sx < -350 or sx > WIDTH + 180:
            return

        cleared = self.cleared(enemies)

        # Rough camp clearing
        pygame.draw.ellipse(screen, (92, 78, 58), (sx - 35, self.y + 70, 320, 145))

        # Two hostile tents
        tent_color = (100, 55, 45) if not cleared else (85, 85, 75)
        for tx, ty in [(sx, self.y + 40), (sx + 150, self.y + 65)]:
            pygame.draw.polygon(
                screen,
                tent_color,
                [(tx, ty + 85), (tx + 58, ty + 8), (tx + 118, ty + 85)]
            )
            pygame.draw.polygon(
                screen,
                BLACK,
                [(tx + 43, ty + 85), (tx + 59, ty + 48), (tx + 77, ty + 85)]
            )

        # Weapon rack
        rack_x = sx + 112
        pygame.draw.line(screen, DARK_BROWN, (rack_x, self.y + 105), (rack_x, self.y + 175), 5)
        pygame.draw.line(screen, DARK_BROWN, (rack_x + 42, self.y + 105), (rack_x + 42, self.y + 175), 5)
        pygame.draw.line(screen, DARK_BROWN, (rack_x - 5, self.y + 122), (rack_x + 47, self.y + 122), 5)
        pygame.draw.line(screen, LIGHT_GRAY, (rack_x + 6, self.y + 115), (rack_x + 30, self.y + 160), 3)
        pygame.draw.line(screen, LIGHT_GRAY, (rack_x + 36, self.y + 115), (rack_x + 14, self.y + 160), 3)

        # Campfire
        fire_x = sx + 130
        fire_y = self.y + 190
        pygame.draw.line(screen, DARK_BROWN, (fire_x - 18, fire_y), (fire_x + 18, fire_y + 13), 6)
        pygame.draw.line(screen, DARK_BROWN, (fire_x + 18, fire_y), (fire_x - 18, fire_y + 13), 6)
        if not cleared:
            pygame.draw.polygon(screen, ORANGE, [(fire_x, fire_y - 28), (fire_x - 13, fire_y + 4), (fire_x + 13, fire_y + 4)])
            pygame.draw.polygon(screen, YELLOW, [(fire_x, fire_y - 16), (fire_x - 7, fire_y + 2), (fire_x + 7, fire_y + 2)])

        label_color = GREEN if cleared else RED
        state = "CLEARED" if cleared else "ENEMY CAMP"
        draw_text(f"{self.name} - {state}", sx, self.y + 5, SMALL, label_color)


class BossFortress:

    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        self.width = 390

    def draw(self, camera):
        sx = camera.sx(self.x)
        if sx < -450 or sx > WIDTH + 100:
            return

        base_y = self.y

        # Outer stone wall
        pygame.draw.rect(screen, (72, 72, 78), (sx, base_y, self.width, 210), border_radius=5)
        pygame.draw.rect(screen, BLACK, (sx, base_y, self.width, 210), 4, border_radius=5)

        # Towers
        for tower_x in (sx - 35, sx + self.width - 45):
            pygame.draw.rect(screen, (62, 62, 68), (tower_x, base_y - 65, 90, 275))
            for battlement_x in range(tower_x, tower_x + 90, 30):
                pygame.draw.rect(screen, (62, 62, 68), (battlement_x, base_y - 84, 20, 28))
            pygame.draw.rect(screen, BLACK, (tower_x, base_y - 65, 90, 275), 3)

        # Battlements on main wall
        for bx in range(sx + 55, sx + self.width - 40, 42):
            pygame.draw.rect(screen, (82, 82, 88), (bx, base_y - 18, 24, 32))

        # Gate
        gate_w = 92
        gate_h = 125
        gate_x = sx + self.width // 2 - gate_w // 2
        gate_y = base_y + 85
        pygame.draw.rect(screen, DARK_BROWN, (gate_x, gate_y, gate_w, gate_h), border_radius=40)
        for bar_x in range(gate_x + 12, gate_x + gate_w - 5, 18):
            pygame.draw.line(screen, BLACK, (bar_x, gate_y + 10), (bar_x, gate_y + gate_h - 5), 4)

        # Flags
        for flag_x in (sx + 10, sx + self.width - 10):
            pygame.draw.line(screen, BLACK, (flag_x, base_y - 120), (flag_x, base_y - 55), 4)
            pygame.draw.polygon(screen, DARK_RED, [(flag_x, base_y - 118), (flag_x + 48, base_y - 100), (flag_x, base_y - 82)])

        draw_text(self.name, sx + 108, base_y + 30, SMALL, GOLD)


def path_y_at_x(world_width, world_x):
    """Return the centre Y of the winding adventure road."""
    p = world_x / max(1, world_width)

    if p < 0.16:
        return 410
    elif p < 0.27:
        t = (p - 0.16) / 0.11
        return int(410 - 145 * t)
    elif p < 0.42:
        return 265
    elif p < 0.54:
        t = (p - 0.42) / 0.12
        return int(265 + 245 * t)
    elif p < 0.69:
        return 510
    elif p < 0.80:
        t = (p - 0.69) / 0.11
        return int(510 - 175 * t)
    else:
        return 335


def get_road_segments(world_width):
    """Build many overlapping rectangles so the road visibly turns."""
    segments = []
    step = 90
    road_width = 235

    last_x = 0
    last_y = path_y_at_x(world_width, 0)

    for x in range(step, world_width + step, step):
        x2 = min(x, world_width)
        y2 = path_y_at_x(world_width, x2)

        left = last_x
        top = min(last_y, y2) - road_width // 2
        width = max(step + 40, x2 - last_x + 40)
        height = abs(y2 - last_y) + road_width

        segments.append(pygame.Rect(left, top, width, height))

        last_x = x2
        last_y = y2

    return segments


def create_adventure_world(level_number):

    data = levels[level_number]
    world_width = data["world_width"]

    walls = []
    river_walls = []
    enemies = []
    chests = []
    gates = []

    zone_centers = [
        int(world_width * 0.22),
        int(world_width * 0.47),
        int(world_width * 0.70)
    ]

    gate_positions = [
        int(world_width * 0.31),
        int(world_width * 0.58),
        int(world_width * 0.79)
    ]

    # Three useful camp types.
    camps = [
        RestCamp(
            int(world_width * 0.34),
            path_y_at_x(world_width, int(world_width * 0.34)) - 155,
            "Pine Watch Camp",
            "rest"
        ),
        RestCamp(
            int(world_width * 0.61),
            path_y_at_x(world_width, int(world_width * 0.61)) - 165,
            "Riverbend Trader",
            "merchant"
        ),
        RestCamp(
            int(world_width * 0.83),
            path_y_at_x(world_width, int(world_width * 0.83)) + 80,
            "Last Light Forge",
            "blacksmith"
        )
    ]

    # Real enemy camps attached to the three battle zones.
    enemy_camps = []
    for zone_id, center_x in enumerate(zone_centers):
        cy = path_y_at_x(world_width, center_x)
        camp_y = cy - 185 if zone_id % 2 == 0 else cy + 55
        camp_y = max(175, min(470, camp_y))
        enemy_camps.append(
            EnemyCamp(
                center_x - 110,
                camp_y,
                zone_id,
                ["Goblin Outpost", "Bandit War Camp", "Shadow Encampment"][zone_id],
                80 + level_number * 40 + zone_id * 35
            )
        )

    # Rivers force the player to use the bridges instead of walking through water.
    rivers = []
    for p in (0.405, 0.685):
        river_x = int(world_width * p)
        bridge_y = path_y_at_x(world_width, river_x)
        river = RiverCrossing(river_x, bridge_y, 115)
        rivers.append(river)
        river_walls.extend(river.collision_walls())

    # ========================================================
    # HIDDEN TREASURE ROADS
    # ========================================================
    # These are intentionally NOT straight copies of the main road.
    # They twist away through the forest and end in secret clearings.
    # There are FOUR hidden-road chests plus ONE normal roadside chest
    # later in this function = FIVE CHESTS TOTAL on every level.
    hidden_paths = []

    # Secret Trail 1: crooked trail that climbs away from the road, then
    # forks into a small treasure clearing with TWO chests.
    start1_x = int(world_width * 0.245)
    start1_y = path_y_at_x(world_width, start1_x)
    s1 = -1 if start1_y > 350 else 1

    trail1_points = [
        (start1_x, start1_y),
        (start1_x + 75, max(205, min(570, start1_y + s1 * 55))),
        (start1_x + 145, max(205, min(570, start1_y + s1 * 115))),
        (start1_x + 225, max(205, min(570, start1_y + s1 * 85))),
        (start1_x + 315, max(205, min(570, start1_y + s1 * 155)))
    ]
    hidden_paths.append(HiddenPath(trail1_points, "Forgotten Forest Trail"))

    chest1_x, chest1_y = trail1_points[-1]
    chests.append(Chest(chest1_x, chest1_y - 10))

    # Extra chest in a tiny side clearing beside Secret Trail 1.
    chest2_x = start1_x + 220
    chest2_y = max(210, min(565, start1_y + s1 * 175))
    hidden_paths.append(
        HiddenPath(
            [
                trail1_points[2],
                (start1_x + 180, chest2_y),
                (chest2_x, chest2_y)
            ],
            "Hidden Clearing"
        )
    )
    chests.append(Chest(chest2_x, chest2_y - 10))

    # Secret Trail 2: a longer zig-zag road after the third enemy camp.
    # It bends in the opposite direction so it does not look like Trail 1.
    start2_x = int(world_width * 0.735)
    start2_y = path_y_at_x(world_width, start2_x)
    s2 = 1 if start2_y < 430 else -1

    trail2_points = [
        (start2_x, start2_y),
        (start2_x + 65, max(205, min(570, start2_y + s2 * 60))),
        (start2_x + 130, max(205, min(570, start2_y + s2 * 20))),
        (start2_x + 205, max(205, min(570, start2_y + s2 * 120))),
        (start2_x + 285, max(205, min(570, start2_y + s2 * 85))),
        (start2_x + 355, max(205, min(570, start2_y + s2 * 150)))
    ]
    hidden_paths.append(HiddenPath(trail2_points, "Overgrown Treasure Trail"))

    chest4_x, chest4_y = trail2_points[-1]
    chests.append(Chest(chest4_x, chest4_y - 10))

    # Extra chest hidden behind a second little spur on Secret Trail 2.
    chest5_x = start2_x + 250
    chest5_y = max(210, min(565, start2_y - s2 * 125))
    hidden_paths.append(
        HiddenPath(
            [
                trail2_points[3],
                (start2_x + 225, chest5_y),
                (chest5_x, chest5_y)
            ],
            "Old Hunter Spur"
        )
    )
    chests.append(Chest(chest5_x, chest5_y - 10))

    # Trail signs around major bends and side areas.
    signs = [
        AdventureSign(int(world_width * 0.18), path_y_at_x(world_width, int(world_width * 0.18)) - 110, "OLD FOREST ROAD", "Camp ahead"),
        AdventureSign(int(world_width * 0.24), path_y_at_x(world_width, int(world_width * 0.24)) + 125, "BROKEN SIGN", "??? trail"),
        AdventureSign(int(world_width * 0.39), path_y_at_x(world_width, int(world_width * 0.39)) + 130, "BRIDGE", "Keep to the road"),
        AdventureSign(int(world_width * 0.60), path_y_at_x(world_width, int(world_width * 0.60)) - 120, "TRADER", "Supplies ->"),
        AdventureSign(int(world_width * 0.73), path_y_at_x(world_width, int(world_width * 0.73)) - 125, "OLD FOOTPATH", "Treasure?"),
        AdventureSign(int(world_width * 0.88), path_y_at_x(world_width, int(world_width * 0.88)) - 115, "FORTRESS", "Boss ahead!")
    ]

    # Enemies stay close to the road and their camp.
    for zone_id, center_x in enumerate(zone_centers):
        enemy_count = 4 + level_number + zone_id

        for i in range(enemy_count):
            enemy_x = center_x + random.randint(-330, 280)
            enemy_x = max(500, min(world_width - 700, enemy_x))
            road_y = path_y_at_x(world_width, enemy_x)
            enemy_y = road_y + random.randint(-90, 90)
            enemy_y = max(200, min(575, enemy_y))

            enemies.append(
                Enemy(
                    enemy_x,
                    enemy_y,
                    data["enemy_hp"] + zone_id * 12,
                    data["enemy_damage"] + zone_id * 2,
                    level_number,
                    zone_id,
                    ranged=(random.random() < (0.15 + level_number * 0.06))
                )
            )

    # Rocks, fallen logs and ruins beside the route.
    for x in range(650, world_width - 600, 620):
        road_y = path_y_at_x(world_width, x)
        side = random.choice([-1, 1])
        obstacle_y = road_y + side * random.randint(145, 190)
        obstacle_y = max(190, min(565, obstacle_y))

        if random.random() < 0.5:
            walls.append(pygame.Rect(x, obstacle_y, random.randint(75, 130), 32))
        else:
            walls.append(pygame.Rect(x, obstacle_y, 34, random.randint(65, 115)))

    # Chest #3: normal roadside treasure.  With the four hidden-road
    # chests above, this makes FIVE treasure chests in every level.
    for p, side in [(0.52, -1)]:
        chest_x = int(world_width * p)
        chest_y = path_y_at_x(world_width, chest_x) + side * 125
        chest_y = max(210, min(580, chest_y))
        chests.append(Chest(chest_x, chest_y))

    for gate_x in gate_positions:
        gates.append(pygame.Rect(gate_x, GROUND_TOP, 28, HEIGHT - GROUND_TOP))

    boss_x = world_width - 365
    boss_y = path_y_at_x(world_width, boss_x)

    fortress = BossFortress(
        world_width - 720,
        max(205, boss_y - 105),
        data["boss_name"] + " Fortress"
    )

    boss = Enemy(
        boss_x,
        boss_y,
        data["boss_hp"],
        data["boss_damage"],
        level_number,
        99,
        ranged=(level_number >= 3),
        boss=True,
        boss_name=data["boss_name"]
    )

    return (
        walls,
        river_walls,
        enemies,
        chests,
        gates,
        gate_positions,
        camps,
        enemy_camps,
        rivers,
        signs,
        hidden_paths,
        fortress,
        boss
    )


# ============================================================
# SCENERY
# ============================================================

def draw_tree(
    x,
    y,
    dark=False,
    snowy=False
):

    trunk_color = (
        DARK_BROWN
        if dark
        else BROWN
    )

    leaf_color = (
        (
            30,
            65,
            40
        )
        if dark
        else DARK_GREEN
    )

    pygame.draw.rect(
        screen,
        trunk_color,
        (
            x - 15,
            y,
            30,
            100
        )
    )

    pygame.draw.circle(
        screen,
        leaf_color,
        (
            x,
            y - 20
        ),
        50
    )

    pygame.draw.circle(
        screen,
        leaf_color,
        (
            x - 30,
            y
        ),
        35
    )

    pygame.draw.circle(
        screen,
        leaf_color,
        (
            x + 30,
            y
        ),
        35
    )

    if snowy:

        pygame.draw.arc(
            screen,
            WHITE,
            (
                x - 50,
                y - 70,
                100,
                55
            ),
            math.pi,
            2 * math.pi,
            8
        )


def draw_background(
    level_number,
    camera
):

    data = levels[
        level_number
    ]

    biome = data[
        "biome"
    ]

    screen.fill(
        data[
            "background"
        ]
    )

    if biome == "forest":
        ground = (55, 125, 60)
        path = (130, 100, 65)
        edge = (95, 78, 54)
    elif biome == "dark_forest":
        ground = (35, 70, 45)
        path = (80, 72, 58)
        edge = (57, 52, 45)
    elif biome == "snow":
        ground = (210, 225, 235)
        path = (165, 180, 190)
        edge = (135, 150, 160)
    elif biome == "volcano":
        ground = (75, 50, 45)
        path = (95, 60, 45)
        edge = (63, 42, 36)
    else:
        ground = (65, 50, 80)
        path = (95, 75, 90)
        edge = (67, 54, 70)

    pygame.draw.rect(
        screen,
        ground,
        (0, GROUND_TOP, WIDTH, HEIGHT - GROUND_TOP)
    )

    # Winding road. Drawing a darker border first makes it look much more
    # like an actual trail instead of one giant rectangle.
    for road in get_road_segments(data["world_width"]):
        sx = camera.sx(road.x)
        if sx > WIDTH + 250 or sx + road.width < -250:
            continue

        pygame.draw.rect(
            screen,
            edge,
            (
                sx - 8,
                road.y - 8,
                road.width + 16,
                road.height + 16
            ),
            border_radius=35
        )

        pygame.draw.rect(
            screen,
            path,
            (
                sx,
                road.y,
                road.width,
                road.height
            ),
            border_radius=30
        )

    # Crossroad / turn sign markers.
    marker_positions = [0.16, 0.27, 0.42, 0.54, 0.69, 0.80]
    for p in marker_positions:
        wx = int(data["world_width"] * p)
        sx = camera.sx(wx)
        wy = path_y_at_x(data["world_width"], wx)
        if -80 < sx < WIDTH + 80:
            pygame.draw.rect(screen, DARK_BROWN, (sx, wy - 65, 8, 70))
            pygame.draw.rect(screen, BROWN, (sx - 42, wy - 82, 92, 30), border_radius=4)
            pygame.draw.polygon(
                screen,
                GOLD,
                [
                    (sx + 50, wy - 67),
                    (sx + 34, wy - 78),
                    (sx + 34, wy - 56)
                ]
            )

    # Biome scenery
    if biome in ["forest", "dark_forest", "snow"]:
        for world_x in range(120, data["world_width"], 210):
            sx = camera.sx(world_x)
            if sx < -100 or sx > WIDTH + 100:
                continue

            road_y = path_y_at_x(data["world_width"], world_x)
            tree_y = 185 if (world_x // 210) % 2 == 0 else 545

            # Keep big trees away from the route centre.
            if abs(tree_y - road_y) < 145:
                tree_y = 190 if road_y > 390 else 535

            draw_tree(
                sx,
                tree_y,
                dark=(biome == "dark_forest"),
                snowy=(biome == "snow")
            )

    elif biome == "volcano":
        for world_x in range(300, data["world_width"], 600):
            sx = camera.sx(world_x)
            pygame.draw.polygon(
                screen,
                DARK_GRAY,
                [(sx - 80, 330), (sx, 190), (sx + 80, 330)]
            )
            pygame.draw.circle(screen, ORANGE, (sx, 335), 16)

    elif biome == "dragon":
        for world_x in range(350, data["world_width"], 700):
            sx = camera.sx(world_x)
            pygame.draw.rect(screen, DARK_GRAY, (sx, 220, 45, 160))
            pygame.draw.rect(screen, GRAY, (sx - 20, 210, 85, 25))


# ============================================================
# CAMPS
# ============================================================

class RestCamp:

    def __init__(self, x, y, name, camp_type="rest"):
        self.x = x
        self.y = y
        self.name = name
        self.camp_type = camp_type
        self.rect = pygame.Rect(x, y, 270, 195)

    def near_player(self, player):
        return self.rect.inflate(130, 105).colliderect(player.rect)

    def draw(self, camera):
        x = camera.sx(self.x)
        y = self.y

        if x < -340 or x > WIDTH + 120:
            return

        if self.camp_type == "merchant":
            cloth = (65, 105, 135)
            title_color = CYAN
        elif self.camp_type == "blacksmith":
            cloth = (110, 65, 55)
            title_color = ORANGE
        else:
            cloth = (145, 120, 78)
            title_color = GOLD

        # Ground clearing
        pygame.draw.ellipse(screen, (105, 88, 63), (x - 30, y + 90, 325, 115))

        # Large tent
        pygame.draw.polygon(
            screen,
            cloth,
            [(x, y + 125), (x + 72, y + 25), (x + 150, y + 125)]
        )
        pygame.draw.polygon(
            screen,
            DARK_BROWN,
            [(x + 52, y + 125), (x + 73, y + 70), (x + 96, y + 125)]
        )
        pygame.draw.line(screen, DARK_BROWN, (x + 72, y + 22), (x + 72, y + 135), 4)

        # Supply awning
        pygame.draw.polygon(
            screen,
            (110, 95, 70),
            [(x + 155, y + 80), (x + 205, y + 47), (x + 255, y + 80)]
        )
        pygame.draw.line(screen, DARK_BROWN, (x + 160, y + 80), (x + 160, y + 145), 4)
        pygame.draw.line(screen, DARK_BROWN, (x + 250, y + 80), (x + 250, y + 145), 4)

        # Crates
        for crate_x, crate_y in [(x + 165, y + 110), (x + 205, y + 116)]:
            pygame.draw.rect(screen, BROWN, (crate_x, crate_y, 38, 32))
            pygame.draw.line(screen, GOLD, (crate_x + 19, crate_y), (crate_x + 19, crate_y + 32), 3)

        # Barrel
        pygame.draw.ellipse(screen, DARK_BROWN, (x + 15, y + 137, 36, 42))
        pygame.draw.line(screen, GRAY, (x + 16, y + 151), (x + 50, y + 151), 3)
        pygame.draw.line(screen, GRAY, (x + 16, y + 166), (x + 50, y + 166), 3)

        # Campfire
        fire_x = x + 125
        fire_y = y + 163
        for ox, oy in [(-24, 5), (0, 12), (23, 5), (-14, 22), (14, 22)]:
            pygame.draw.circle(screen, GRAY, (fire_x + ox, fire_y + oy), 8)
        pygame.draw.line(screen, DARK_BROWN, (fire_x - 22, fire_y + 5), (fire_x + 22, fire_y + 25), 7)
        pygame.draw.line(screen, DARK_BROWN, (fire_x + 22, fire_y + 5), (fire_x - 22, fire_y + 25), 7)
        pygame.draw.polygon(screen, ORANGE, [(fire_x, fire_y - 35), (fire_x - 18, fire_y + 8), (fire_x + 18, fire_y + 8)])
        pygame.draw.polygon(screen, YELLOW, [(fire_x, fire_y - 20), (fire_x - 9, fire_y + 4), (fire_x + 9, fire_y + 4)])

        # Camp-specific prop
        if self.camp_type == "merchant":
            pygame.draw.circle(screen, GOLD, (x + 266, y + 122), 13)
            draw_text("$", x + 260, y + 112, SMALL, BLACK)
        elif self.camp_type == "blacksmith":
            pygame.draw.rect(screen, DARK_GRAY, (x + 245, y + 130, 50, 22), border_radius=4)
            pygame.draw.rect(screen, GRAY, (x + 257, y + 112, 26, 20), border_radius=3)
            pygame.draw.line(screen, ORANGE, (x + 265, y + 105), (x + 280, y + 90), 5)
        else:
            pygame.draw.line(screen, DARK_BROWN, (x + 265, y + 65), (x + 265, y + 120), 4)
            pygame.draw.circle(screen, YELLOW, (x + 265, y + 125), 9)

        label = {
            "rest": "REST CAMP",
            "merchant": "MERCHANT CAMP",
            "blacksmith": "BLACKSMITH CAMP"
        }.get(self.camp_type, "CAMP")

        draw_text(self.name, x, y - 12, SMALL, title_color)
        draw_text(label, x, y + 8, SMALL, WHITE)


async def camp_menu(player, camp):
    status = "Choose a camp service."

    while True:
        screen.fill((24, 28, 34))

        camp_title = {
            "rest": "REST & RESUPPLY",
            "merchant": "TRADER & SUPPLIES",
            "blacksmith": "FORGE & EQUIPMENT"
        }.get(camp.camp_type, "CAMP")

        draw_center(camp.name, 45, BIG, GOLD)
        draw_center(camp_title, 102, FONT, WHITE)

        pygame.draw.rect(screen, (48, 52, 62), (190, 145, 720, 430), border_radius=14)
        pygame.draw.rect(screen, GRAY, (190, 145, 720, 430), 2, border_radius=14)

        draw_text(f"HP: {player.hp}/{player.max_hp}", 250, 180, FONT)
        draw_text(f"Potions: {player_data['potions']}", 250, 217, FONT)
        draw_text(f"Gold: {player_data['gold']}", 250, 254, FONT, GOLD)

        if camp.camp_type == "merchant":
            draw_text("1  Buy 1 potion - 45 Gold", 250, 315, FONT)
            draw_text("2  Supply bundle: 3 potions - 120 Gold", 250, 357, FONT)
            draw_text("3  Open full shop", 250, 399, FONT)
            draw_text("4  Rest by fire - Restore all HP - 25 Gold", 250, 441, FONT)
            draw_text("5  Save game", 250, 483, FONT)

        elif camp.camp_type == "blacksmith":
            draw_text("1  Open equipment shop", 250, 315, FONT)
            draw_text("2  Repair & rest - Restore all HP - 20 Gold", 250, 357, FONT)
            draw_text("3  Buy 1 potion - 50 Gold", 250, 399, FONT)
            draw_text("4  Buy 3 potions - 130 Gold", 250, 441, FONT)
            draw_text("5  Save game", 250, 483, FONT)

        else:
            draw_text("1  Rest by the fire - Restore all HP - FREE", 250, 315, FONT)
            draw_text("2  Buy 1 potion - 50 Gold", 250, 357, FONT)
            draw_text("3  Supply bundle: 3 potions - 130 Gold", 250, 399, FONT)
            draw_text("4  Open full shop", 250, 441, FONT)
            draw_text("5  Save game", 250, 483, FONT)

        draw_text("ESC  Return to the adventure", 250, 525, FONT)
        draw_center(status, 610, SMALL, CYAN)

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game()
                pygame.quit()
                return

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_ESCAPE:
                return

            if camp.camp_type == "merchant":
                if event.key == pygame.K_1:
                    if player_data["gold"] >= 45:
                        player_data["gold"] -= 45
                        player_data["potions"] += 1
                        status = "Bought 1 potion."
                    else:
                        status = "Not enough gold."

                elif event.key == pygame.K_2:
                    if player_data["gold"] >= 120:
                        player_data["gold"] -= 120
                        player_data["potions"] += 3
                        status = "Supply bundle purchased: +3 potions."
                    else:
                        status = "Not enough gold."

                elif event.key == pygame.K_3:
                    await shop()
                    status = "Welcome back to the trader camp."

                elif event.key == pygame.K_4:
                    if player_data["gold"] >= 25:
                        player_data["gold"] -= 25
                        player.hp = player.max_hp
                        status = "You rested and restored all HP."
                    else:
                        status = "Not enough gold."

                elif event.key == pygame.K_5:
                    save_game()
                    status = "Game saved at camp."

            elif camp.camp_type == "blacksmith":
                if event.key == pygame.K_1:
                    await shop()
                    status = "Returned from the equipment shop."

                elif event.key == pygame.K_2:
                    if player_data["gold"] >= 20:
                        player_data["gold"] -= 20
                        player.hp = player.max_hp
                        status = "Armor repaired. HP fully restored."
                    else:
                        status = "Not enough gold."

                elif event.key == pygame.K_3:
                    if player_data["gold"] >= 50:
                        player_data["gold"] -= 50
                        player_data["potions"] += 1
                        status = "Bought 1 potion."
                    else:
                        status = "Not enough gold."

                elif event.key == pygame.K_4:
                    if player_data["gold"] >= 130:
                        player_data["gold"] -= 130
                        player_data["potions"] += 3
                        status = "Supply bundle purchased: +3 potions."
                    else:
                        status = "Not enough gold."

                elif event.key == pygame.K_5:
                    save_game()
                    status = "Game saved at the forge."

            else:
                if event.key == pygame.K_1:
                    player.hp = player.max_hp
                    status = "You rested by the fire. HP fully restored."

                elif event.key == pygame.K_2:
                    if player_data["gold"] >= 50:
                        player_data["gold"] -= 50
                        player_data["potions"] += 1
                        status = "Bought 1 potion."
                    else:
                        status = "Not enough gold."

                elif event.key == pygame.K_3:
                    if player_data["gold"] >= 130:
                        player_data["gold"] -= 130
                        player_data["potions"] += 3
                        status = "Supply bundle purchased: +3 potions."
                    else:
                        status = "Not enough gold."

                elif event.key == pygame.K_4:
                    await shop()
                    status = "Returned from the shop."

                elif event.key == pygame.K_5:
                    save_game()
                    status = "Game saved at camp."


# ============================================================
# GATES
# ============================================================

def get_closed_gates(
    gates,
    enemies
):

    closed = []

    for zone_index, gate in enumerate(
        gates
    ):

        alive_in_zone = any(

            enemy.hp > 0
            and
            enemy.zone
            ==
            zone_index

            for enemy in enemies
        )

        if alive_in_zone:

            closed.append(
                gate
            )

    return closed


def draw_gates(
    gates,
    enemies,
    camera
):

    for zone_index, gate in enumerate(
        gates
    ):

        alive_in_zone = any(

            enemy.hp > 0
            and
            enemy.zone
            ==
            zone_index

            for enemy in enemies
        )

        x = camera.sx(
            gate.x
        )

        if alive_in_zone:

            pygame.draw.rect(
                screen,
                DARK_RED,
                (
                    x,
                    gate.y,
                    gate.width,
                    gate.height
                )
            )

            pygame.draw.line(
                screen,
                GOLD,
                (
                    x,
                    gate.y
                ),
                (
                    x,
                    gate.bottom
                ),
                5
            )

        else:

            pygame.draw.line(
                screen,
                GREEN,
                (
                    x,
                    250
                ),
                (
                    x,
                    580
                ),
                3
            )


# ============================================================
# XP
# ============================================================

def check_level_up():

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
        ] -= (
            needed
        )

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

        targets = list(
            enemies
        )

        if boss:

            targets.append(
                boss
            )

        nearby = []

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
# SAFE WALL HIT
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
    level_number,
    world_width
):

    pygame.draw.rect(
        screen,
        (
            12,
            12,
            22
        ),
        (
            0,
            0,
            WIDTH,
            155
        )
    )

    # HP
    pygame.draw.rect(
        screen,
        DARK_RED,
        (
            20,
            18,
            240,
            24
        )
    )

    hp_width = int(
        240
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
            18,
            hp_width,
            24
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
        285,
        18,
        SMALL
    )

    draw_text(
        f"XP {player_data['xp']}/{needed}",
        285,
        42,
        SMALL
    )

    draw_text(
        f"Gold {player_data['gold']}",
        420,
        18,
        SMALL,
        GOLD
    )

    draw_text(
        f"Potions {player_data['potions']} [H]",
        420,
        42,
        SMALL
    )

    draw_text(
        f"Mode {player_data['weapon_mode']}",
        600,
        18,
        SMALL,
        GOLD
    )

    draw_text(
        f"Arrow {player_data['arrow_type'].title()}",
        600,
        42,
        SMALL
    )

    draw_text(
        f"Stage {level_number}",
        930,
        18,
        SMALL
    )

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
        94,
        SMALL
    )

    draw_text(
        (
            f"X {character['abilities']['X']['name']}: "
            f"{cooldown_text(player.ability_x_cooldown)}"
        ),
        20,
        116,
        SMALL
    )

    draw_text(
        (
            f"C {character['abilities']['C']['name']}: "
            f"{cooldown_text(player.ability_c_cooldown)}"
        ),
        20,
        138,
        SMALL
    )

    # Adventure progress
    progress = (
        player.x
        /
        world_width
    )

    pygame.draw.rect(
        screen,
        DARK_GRAY,
        (
            600,
            90,
            430,
            16
        )
    )

    pygame.draw.rect(
        screen,
        GOLD,
        (
            600,
            90,
            int(
                430
                *
                progress
            ),
            16
        )
    )

    draw_text(
        "Adventure Progress",
        600,
        112,
        SMALL
    )

    if player.berserk_timer > 0:

        draw_text(
            "BERSERK!",
            830,
            42,
            SMALL,
            RED
        )

    if player.invisible_timer > 0:

        draw_text(
            "INVISIBLE",
            830,
            42,
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
    ][
        "price"
    ]

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

async def shop():

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

                return

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
        await asyncio.sleep(0)

# ============================================================
# CHARACTER SELECT
# ============================================================

async def character_select():

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

            x = x_positions[
                i
            ]

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
                x + 48,
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

            button = Button(
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

            button.draw()

            buttons.append(
                (
                    button,
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

                return

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
        
        await asyncio.sleep(0)

# ============================================================
# PLAY LEVEL
# ============================================================

async def play_level(
    level_number
):

    data = levels[
        level_number
    ]

    world_width = data[
        "world_width"
    ]

    player = Player()

    camera = Camera(
        world_width
    )

    (
        walls,
        river_walls,
        enemies,
        chests,
        gates,
        gate_positions,
        camps,
        enemy_camps,
        rivers,
        signs,
        hidden_paths,
        fortress,
        boss
    ) = create_adventure_world(
        level_number
    )

    projectiles = []

    explosions = []

    lightning_effects = []

    message = (
        "Begin your adventure!"
    )

    message_timer = (
        2
        *
        FPS
    )

    boss_started = False

    boss_defeated = False

    while True:

        clock.tick(
            FPS
        )

        await asyncio.sleep(0)
        closed_gates = get_closed_gates(
            gates,
            enemies
        )

        collision_objects = (
            walls
            +
            river_walls
            +
            closed_gates
        )

        # ====================================================
        # EVENTS
        # ====================================================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                save_game()

                pygame.quit()

                return

            if event.type != pygame.KEYDOWN:

                continue

            if event.key == pygame.K_ESCAPE:

                return "menu"

            # SWITCH SWORD/BOW
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

            # ARROW KEYS
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

                wanted = arrow_keys[
                    event.key
                ]

                if wanted in player_data[
                    "owned_arrows"
                ]:

                    player_data[
                        "arrow_type"
                    ] = wanted

            # ATTACK
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

            # CHARACTER ABILITIES
            if event.key == pygame.K_z:

                player.use_ability(
                    "Z",
                    enemies,
                    boss,
                    projectiles,
                    explosions,
                    lightning_effects,
                    collision_objects,
                    world_width
                )

            if event.key == pygame.K_x:

                player.use_ability(
                    "X",
                    enemies,
                    boss,
                    projectiles,
                    explosions,
                    lightning_effects,
                    collision_objects,
                    world_width
                )

            if event.key == pygame.K_c:

                player.use_ability(
                    "C",
                    enemies,
                    boss,
                    projectiles,
                    explosions,
                    lightning_effects,
                    collision_objects,
                    world_width
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
                        player.hp
                        +
                        45
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
                        collision_objects,
                        world_width
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

            # CAMPS / CHESTS
            if event.key == pygame.K_e:

                used_camp = False

                for camp in camps:

                    if camp.near_player(
                        player
                    ):

                        await camp_menu(
                            player,
                            camp
                        )

                        message = "Rested and resupplied!"
                        message_timer = 2 * FPS
                        used_camp = True
                        break

                if not used_camp:

                    for chest in chests:

                        reward = chest.open(
                            player
                        )

                        if reward:

                            message = reward
                            message_timer = 2 * FPS
                            break

        # ====================================================
        # PLAYER
        # ====================================================

        player.update(
            walls + river_walls,
            closed_gates,
            world_width
        )

        camera.update(
            player
        )

        # ====================================================
        # GATE MESSAGES
        # ====================================================

        for zone_index, gate in enumerate(
            gates
        ):

            alive_in_zone = any(

                enemy.hp > 0
                and
                enemy.zone
                ==
                zone_index

                for enemy in enemies
            )

            if (
                alive_in_zone
                and
                abs(
                    player.rect.centerx
                    -
                    gate.centerx
                )
                <
                100
            ):

                message = (
                    "GATE LOCKED! Defeat the enemies!"
                )

                message_timer = 30

        # ====================================================
        # ENEMIES
        # ====================================================

        for enemy in enemies[:]:

            enemy_active = (
                abs(
                    enemy.rect.centerx
                    -
                    player.rect.centerx
                )
                <
                850
            )

            enemy.update(
                player,
                walls + river_walls,
                projectiles,
                enemy_active
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
        # ENEMY CAMP CLEAR REWARDS
        # ====================================================

        for enemy_camp in enemy_camps:

            camp_reward = enemy_camp.claim_reward(
                enemies
            )

            if camp_reward > 0:

                player_data[
                    "gold"
                ] += camp_reward

                message = (
                    enemy_camp.name
                    +
                    " cleared! +"
                    +
                    str(camp_reward)
                    +
                    " Gold"
                )

                message_timer = (
                    3
                    *
                    FPS
                )

        # ====================================================
        # BOSS
        # ====================================================

        boss_distance = (
            boss.rect.centerx
            -
            player.rect.centerx
        )

        if (
            boss_distance
            <
            800
            and
            not boss_started
        ):

            boss_started = True

            message = (
                "BOSS: "
                +
                data[
                    "boss_name"
                ]
            )

            message_timer = (
                3
                *
                FPS
            )

        if (
            boss_started
            and
            boss.hp > 0
        ):

            boss.update(
                player,
                walls + river_walls,
                projectiles,
                True
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

            # Enemy projectile
            if projectile.enemy:

                if projectile.rect.colliderect(
                    player.rect
                ):

                    defense = armors[
                        player_data[
                            "armor"
                        ]
                    ][
                        "defense"
                    ]

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

            # Player projectile
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
                    boss_started
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

            # Walls + closed gates
            hit_wall = False

            for wall in collision_objects:

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

            if projectile.off_world(
                world_width
            ):

                if projectile in projectiles:

                    projectiles.remove(
                        projectile
                    )

        # ====================================================
        # DEAD ENEMIES FROM FIRE / EXPLOSIONS
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
            boss_started
            and
            boss.hp <= 0
            and
            not boss_defeated
        ):

            boss_defeated = True

            player_data[
                "gold"
            ] += (
                level_number
                *
                250
            )

            player_data[
                "xp"
            ] += (
                level_number
                *
                120
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
        # DRAW WORLD
        # ====================================================

        draw_background(
            level_number,
            camera
        )

        # Rivers and bridges
        for river in rivers:
            river.draw(
                camera
            )

        # Hidden side trails
        for hidden_path in hidden_paths:
            hidden_path.draw(
                camera
            )

        # Trail signs
        for sign in signs:
            sign.draw(
                camera
            )

        # Boss fortress
        fortress.draw(
            camera
        )

        # Enemy camps
        for enemy_camp in enemy_camps:
            enemy_camp.draw(
                camera,
                enemies
            )

        # Real rest / merchant / blacksmith camps
        for camp in camps:

            camp.draw(
                camera
            )

            if camp.near_player(
                player
            ):

                draw_center(
                    "Press E to enter " + camp.camp_type + " camp",
                    535,
                    SMALL,
                    GOLD
                )

        # Walls
        for wall in walls:

            x = camera.sx(
                wall.x
            )

            if (
                x
                >
                -200
                and
                x
                <
                WIDTH
                +
                200
            ):

                pygame.draw.rect(
                    screen,
                    GRAY,
                    (
                        x,
                        wall.y,
                        wall.width,
                        wall.height
                    ),
                    border_radius=5
                )

                pygame.draw.rect(
                    screen,
                    BLACK,
                    (
                        x,
                        wall.y,
                        wall.width,
                        wall.height
                    ),
                    2,
                    border_radius=5
                )

        # Gates
        draw_gates(
            gates,
            enemies,
            camera
        )

        # Chests
        for chest in chests:

            chest.draw(
                camera
            )

        # Enemies
        for enemy in enemies:

            if (
                camera.sx(
                    enemy.rect.x
                )
                >
                -100
                and
                camera.sx(
                    enemy.rect.x
                )
                <
                WIDTH
                +
                100
            ):

                enemy.draw(
                    camera
                )

        # Boss
        if (
            boss_started
            or
            camera.sx(
                boss.rect.x
            )
            <
            WIDTH
        ):

            boss.draw(
                camera
            )

            if boss.hp > 0:

                draw_center(
                    data[
                        "boss_name"
                    ],
                    165,
                    SMALL,
                    RED
                )

        # Projectiles
        for projectile in projectiles:

            projectile.draw(
                camera
            )

        # Effects
        for explosion in explosions:

            explosion.draw(
                camera
            )

        for effect in lightning_effects:

            effect.draw(
                camera
            )

        # Player
        player.draw(
            camera
        )

        # HUD
        draw_hud(
            player,
            level_number,
            world_width
        )

        draw_center(
            data[
                "name"
            ],
            160,
            FONT,
            GOLD
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
            651,
            SMALL
        )

        draw_text(
            "H Potion | E Camp/Chest | R Pearl | F Hammer | N Next Level | ESC Exit",
            10,
            672,
            SMALL
        )

        if message_timer > 0:

            message_timer -= 1

            pygame.draw.rect(
                screen,
                BLACK,
                (
                    WIDTH // 2 - 260,
                    560,
                    520,
                    45
                ),
                border_radius=8
            )

            draw_center(
                message,
                570,
                SMALL,
                GOLD
            )

        pygame.display.flip()


# ============================================================
# RESULT SCREEN
# ============================================================

async def result_screen(
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

                return

            if button.clicked(
                event
            ):

                return

        clock.tick(
            FPS
        )

        await asyncio.sleep(0)
# ============================================================
# LEVEL SELECT
# ============================================================

async def level_select():

    while True:

        screen.fill(
            (
                20,
                35,
                50
            )
        )

        draw_center(
            "SELECT ADVENTURE",
            30,
            BIG,
            GOLD
        )

        buttons = []

        y = 115

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
                225,
                y,
                650,
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

                return

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

                        result = await play_level(
                            number
                        )

                        if result == "win":

                            await result_screen(
                                "VICTORY!",
                                (
                                    "You conquered "
                                    +
                                    levels[
                                        number
                                    ][
                                        "name"
                                    ]
                                    +
                                    "!"
                                )
                            )

                        elif result == "dead":

                            await result_screen(
                                "YOU DIED",
                                "Upgrade your gear or try another character!"
                            )

        clock.tick(
            FPS
        )

        await asyncio.sleep(0)
# ============================================================
# MAIN MENU
# ============================================================


async def player_name_screen(force=False):
    """Ask for a display name. Old saves called 'Player' get this once."""
    current = str(player_data.get("player_name", "Player"))
    if not force and current not in ("", "Player"):
        return

    typed = "" if current == "Player" else current[:14]

    while True:
        screen.fill((18, 18, 32))
        draw_center("CHOOSE YOUR PLAYER NAME", 115, BIG, GOLD)
        draw_center("This name appears above your character in LAN games.", 175, SMALL)

        box = pygame.Rect(330, 245, 440, 60)
        pygame.draw.rect(screen, (35, 35, 55), box)
        pygame.draw.rect(screen, GOLD, box, 3)

        shown = typed if typed else "Type your name..."
        color = WHITE if typed else GRAY
        name_surface = FONT.render(shown, True, color)
        screen.blit(name_surface, (box.x + 15, box.y + 16))

        draw_center("ENTER = confirm     ESC = cancel", 335, SMALL)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game()
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

                if event.key == pygame.K_RETURN:
                    clean = typed.strip()
                    if clean:
                        player_data["player_name"] = clean[:14]
                        save_game()
                        return

                elif event.key == pygame.K_BACKSPACE:
                    typed = typed[:-1]

                elif event.unicode and event.unicode.isprintable():
                    if len(typed) < 14:
                        typed += event.unicode

        clock.tick(FPS)
        await asyncio.sleep(0)


async def server_address_screen(title, default_value, help_text):
    typed = default_value
    while True:
        screen.fill((18, 18, 32))
        draw_center(title, 100, BIG, GOLD)
        draw_center(help_text, 165, SMALL)
        box = pygame.Rect(180, 235, 740, 60)
        pygame.draw.rect(screen, (35, 35, 55), box)
        pygame.draw.rect(screen, GOLD, box, 3)
        shown = typed[-70:]
        surf = SMALL.render(shown, True, WHITE)
        screen.blit(surf, (box.x + 12, box.y + 19))
        draw_center("ENTER = connect     ESC = back", 335, SMALL)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                if event.key == pygame.K_RETURN:
                    return typed.strip()
                if event.key == pygame.K_BACKSPACE:
                    typed = typed[:-1]
                elif event.unicode and event.unicode.isprintable() and len(typed) < 180:
                    typed += event.unicode
        clock.tick(FPS)
        await asyncio.sleep(0)


async def lan_ip_screen():
    address = await server_address_screen(
        "JOIN LAN SERVER",
        "ws://127.0.0.1:5050",
        "Same PC: ws://127.0.0.1:5050   Other PC: ws://LAN-IP:5050"
    )
    return address


async def online_server_screen():
    return await server_address_screen(
        "ONLINE SERVER",
        "wss://YOUR-SERVICE.onrender.com",
        "Paste your Render WebSocket address (wss://...onrender.com)"
    )


def draw_lan_remote_player(p, camera):
    """Draw another LAN player using the same character style as Sword Adventure."""
    sx = camera.sx(int(p["x"]))
    sy = int(p["y"])
    rect = pygame.Rect(sx, sy, 44, 58)

    if rect.right < -100 or rect.left > WIDTH + 100:
        return

    character_name = p.get("character", "Knight")
    if character_name not in characters:
        character_name = "Knight"

    body_color = characters[character_name]["color"]

    # Legs
    pygame.draw.rect(screen, DARK_BLUE, (rect.x + 7, rect.y + 42, 12, 16))
    pygame.draw.rect(screen, DARK_BLUE, (rect.x + 26, rect.y + 42, 12, 16))

    # Body
    pygame.draw.rect(
        screen, body_color,
        (rect.x + 5, rect.y + 15, 34, 32),
        border_radius=5
    )

    # Head
    pygame.draw.circle(screen, (235, 195, 155), (rect.centerx, rect.y + 10), 13)
    pygame.draw.circle(screen, BLACK, (rect.centerx - 5, rect.y + 8), 2)
    pygame.draw.circle(screen, BLACK, (rect.centerx + 5, rect.y + 8), 2)

    # Character head details
    if character_name == "Knight":
        pygame.draw.arc(
            screen, LIGHT_GRAY,
            (rect.centerx - 14, rect.y - 3, 28, 22),
            math.pi, 2 * math.pi, 5
        )
    elif character_name == "Ranger":
        pygame.draw.arc(
            screen, GREEN,
            (rect.centerx - 15, rect.y - 4, 30, 25),
            math.pi, 2 * math.pi, 6
        )
    elif character_name == "Mage":
        pygame.draw.polygon(
            screen, PURPLE,
            [
                (rect.centerx, rect.y - 25),
                (rect.centerx - 17, rect.y + 3),
                (rect.centerx + 17, rect.y + 3)
            ]
        )
    elif character_name == "Shadow":
        pygame.draw.rect(
            screen, DARK_GRAY,
            (rect.centerx - 13, rect.y, 26, 9)
        )

    # Simple equipped weapon so other players look like real characters.
    facing = int(p.get("facing", 1))
    weapon_mode = p.get("weapon_mode", "sword")

    if weapon_mode == "bow":
        if facing == 1:
            bow_rect = pygame.Rect(rect.right - 5, rect.centery - 25, 28, 50)
        else:
            bow_rect = pygame.Rect(rect.left - 23, rect.centery - 25, 28, 50)
        pygame.draw.arc(screen, BROWN, bow_rect, -1.5, 1.5, 4)
        pygame.draw.line(
            screen, WHITE,
            (bow_rect.centerx, bow_rect.top),
            (bow_rect.centerx, bow_rect.bottom), 2
        )
    else:
        angle = -0.3 if facing == 1 else math.pi + 0.3
        cx, cy = rect.centerx, rect.centery
        hx = cx + math.cos(angle) * 13
        hy = cy + math.sin(angle) * 13
        ex = cx + math.cos(angle) * 52
        ey = cy + math.sin(angle) * 52
        pygame.draw.line(screen, GOLD, (cx, cy), (hx, hy), 8)
        pygame.draw.line(screen, LIGHT_GRAY, (hx, hy), (ex, ey), 7)

    # Name + floating HP bar
    name = str(p.get("name", "Player"))[:14]
    name_surface = SMALL.render(name, True, WHITE)
    screen.blit(
        name_surface,
        (rect.centerx - name_surface.get_width() // 2, rect.top - 34)
    )

    bar_w = 54
    bar_h = 7
    bar_x = rect.centerx - bar_w // 2
    bar_y = rect.top - 15
    hp = max(0, int(p.get("hp", 100)))
    max_hp = max(1, int(p.get("max_hp", 100)))
    pygame.draw.rect(screen, (45, 20, 20), (bar_x, bar_y, bar_w, bar_h))
    pygame.draw.rect(
        screen, GREEN,
        (bar_x, bar_y, int(bar_w * min(1, hp / max_hp)), bar_h)
    )
    pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_w, bar_h), 1)


async def lan_game(host_ip):
    """Multiplayer adventure: works through WebSocket on desktop and browser."""
    try:
        reader, writer = await asyncio.wait_for(
            open_game_connection(host_ip, 5050),
            timeout=5
        )
    except Exception:
        end_time = pygame.time.get_ticks() + 2500
        while pygame.time.get_ticks() < end_time:
            screen.fill((18, 18, 32))
            draw_center("COULD NOT CONNECT", 220, BIG, RED)
            draw_center("Start server.py on the host, then try again.", 290, SMALL)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            await asyncio.sleep(0)
        return

    level_number = 1
    data = levels[level_number]
    world_width = data["world_width"]

    player = Player()
    camera = Camera(world_width)

    (
        walls,
        river_walls,
        enemies,
        chests,
        gates,
        gate_positions,
        camps,
        enemy_camps,
        rivers,
        signs,
        hidden_paths,
        fortress,
        boss
    ) = create_adventure_world(level_number)

    projectiles = []
    explosions = []
    lightning_effects = []

    message = "LAN Adventure started!"
    message_timer = 2 * FPS
    boss_started = False
    boss_defeated = False
    next_level_ready = False

    my_name = str(player_data.get("player_name", "Player"))[:14]
    my_character = player_data.get("character", "Knight")

    writer.write(f"HELLO|{my_name}|{my_character}\n".encode())
    await writer.drain()

    my_id = None
    others = {}

    async def send_state():
        try:
            writer.write(
                (
                    f"STATE|{level_number}|{player.x:.1f}|{player.y:.1f}|"
                    f"{int(player.hp)}|{int(player.max_hp)}|"
                    f"{player_data.get('character','Knight')}|{player.facing}|"
                    f"{player_data.get('weapon_mode','sword')}\n"
                ).encode()
            )
            await writer.drain()
            return True
        except Exception:
            return False

    async def receive_available():
        nonlocal my_id, others

        while True:
            try:
                line = await asyncio.wait_for(reader.readline(), timeout=0.001)
            except asyncio.TimeoutError:
                break
            except Exception:
                return False

            if not line:
                return False

            msg = line.decode(errors="ignore").strip().split("|")
            if not msg:
                continue

            if msg[0] == "WELCOME" and len(msg) >= 2:
                my_id = msg[1]

            elif msg[0] == "PLAYER" and len(msg) >= 11:
                pid = msg[1]
                if pid != my_id:
                    try:
                        others[pid] = {
                            "name": msg[2],
                            "level": int(msg[3]),
                            "x": float(msg[4]),
                            "y": float(msg[5]),
                            "hp": int(float(msg[6])),
                            "max_hp": int(float(msg[7])),
                            "character": msg[8],
                            "facing": int(msg[9]),
                            "weapon_mode": msg[10]
                        }
                    except ValueError:
                        pass

            elif msg[0] == "LEFT" and len(msg) >= 2:
                others.pop(msg[1], None)

        return True

    running = True
    last_send = 0

    while running:
        clock.tick(FPS)
        await asyncio.sleep(0)

        closed_gates = get_closed_gates(gates, enemies)

        collision_objects = (
            walls
            +
            river_walls
            +
            closed_gates
        )

        # ====================================================
        # EVENTS
        # ====================================================

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_ESCAPE:
                running = False
                continue

            # NEXT LEVEL AFTER DEFEATING THE BOSS
            if (
                event.key == pygame.K_n
                and
                boss_defeated
                and
                level_number < len(levels)
            ):
                level_number += 1
                data = levels[level_number]
                world_width = data["world_width"]

                (
                    walls,
                    river_walls,
                    enemies,
                    chests,
                    gates,
                    gate_positions,
                    camps,
                    enemy_camps,
                    rivers,
                    signs,
                    hidden_paths,
                    fortress,
                    boss
                ) = create_adventure_world(level_number)

                projectiles.clear()
                explosions.clear()
                lightning_effects.clear()

                boss_started = False
                boss_defeated = False
                next_level_ready = False

                player.x = 110
                player.y = float(path_y_at_x(world_width, 110))
                player.rect.x = int(player.x)
                player.rect.y = int(player.y)
                player.hp = player.max_hp

                camera = Camera(world_width)
                camera.update(player)

                message = (
                    "LEVEL "
                    + str(level_number)
                    + ": "
                    + data["name"]
                )
                message_timer = 4 * FPS
                continue

            # SWITCH SWORD/BOW
            if event.key == pygame.K_q:
                if player_data["weapon_mode"] == "sword":
                    player_data["weapon_mode"] = "bow"
                else:
                    player_data["weapon_mode"] = "sword"

            # ARROW TYPES
            arrow_keys = {
                pygame.K_1: "regular",
                pygame.K_2: "lightning",
                pygame.K_3: "exploding",
                pygame.K_4: "homing",
                pygame.K_5: "fire",
                pygame.K_6: "super"
            }

            if event.key in arrow_keys:
                wanted = arrow_keys[event.key]
                if wanted in player_data["owned_arrows"]:
                    player_data["arrow_type"] = wanted

            # ATTACK
            if event.key == pygame.K_SPACE:
                if player_data["weapon_mode"] == "sword":
                    player.sword_attack(enemies, boss)
                else:
                    player.shoot(projectiles)

            # CHARACTER ABILITIES
            if event.key == pygame.K_z:
                player.use_ability(
                    "Z",
                    enemies,
                    boss,
                    projectiles,
                    explosions,
                    lightning_effects,
                    collision_objects,
                    world_width
                )

            if event.key == pygame.K_x:
                player.use_ability(
                    "X",
                    enemies,
                    boss,
                    projectiles,
                    explosions,
                    lightning_effects,
                    collision_objects,
                    world_width
                )

            if event.key == pygame.K_c:
                player.use_ability(
                    "C",
                    enemies,
                    boss,
                    projectiles,
                    explosions,
                    lightning_effects,
                    collision_objects,
                    world_width
                )

            # POTION
            if event.key == pygame.K_h:
                if (
                    player_data["potions"] > 0
                    and
                    player.hp < player.max_hp
                ):
                    player_data["potions"] -= 1
                    player.hp = min(player.max_hp, player.hp + 45)

            # ENDER PEARL
            if event.key == pygame.K_r:
                if player_data["utility"] == "Ender Pearl":
                    player.teleport(collision_objects, world_width)

            # HAMMER
            if event.key == pygame.K_f:
                if "Hammer" in player_data["utility"]:
                    player.hammer(enemies, boss, explosions)

            # CAMPS / CHESTS
            if event.key == pygame.K_e:
                used_camp = False

                for camp in camps:
                    if camp.near_player(player):
                        await camp_menu(player, camp)
                        message = "Rested and resupplied!"
                        message_timer = 2 * FPS
                        used_camp = True
                        break

                if not used_camp:
                    for chest in chests:
                        reward = chest.open(player)
                        if reward:
                            message = reward
                            message_timer = 2 * FPS
                            break

        # ====================================================
        # PLAYER
        # ====================================================

        player.update(
            walls + river_walls,
            closed_gates,
            world_width
        )

        camera.update(player)

        # ====================================================
        # NETWORK
        # ====================================================

        now = pygame.time.get_ticks()

        if now - last_send >= 50:
            if not await send_state():
                running = False
            last_send = now

        if not await receive_available():
            running = False

        # ====================================================
        # GATE MESSAGES
        # ====================================================

        for zone_index, gate in enumerate(gates):
            alive_in_zone = any(
                enemy.hp > 0
                and
                enemy.zone == zone_index
                for enemy in enemies
            )

            if (
                alive_in_zone
                and
                abs(player.rect.centerx - gate.centerx) < 100
            ):
                message = "GATE LOCKED! Defeat the enemies!"
                message_timer = 30

        # ====================================================
        # ENEMIES
        # ====================================================

        for enemy in enemies[:]:
            enemy_active = (
                abs(enemy.rect.centerx - player.rect.centerx) < 850
            )

            enemy.update(
                player,
                walls + river_walls,
                projectiles,
                enemy_active
            )

            if enemy.hp <= 0:
                player_data["gold"] += 15 + level_number * 10
                player_data["xp"] += 15 + level_number * 8
                enemies.remove(enemy)
                check_level_up()

        # ====================================================
        # ENEMY CAMP CLEAR REWARDS
        # ====================================================

        for enemy_camp in enemy_camps:
            camp_reward = enemy_camp.claim_reward(enemies)

            if camp_reward > 0:
                player_data["gold"] += camp_reward
                message = (
                    enemy_camp.name
                    + " cleared! +"
                    + str(camp_reward)
                    + " Gold"
                )
                message_timer = 3 * FPS

        # ====================================================
        # BOSS
        # ====================================================

        boss_distance = boss.rect.centerx - player.rect.centerx

        if boss_distance < 800 and not boss_started:
            boss_started = True
            message = "BOSS: " + data["boss_name"]
            message_timer = 3 * FPS

        if boss_started and boss.hp > 0:
            boss.update(
                player,
                walls + river_walls,
                projectiles,
                True
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
            projectile.update(enemies, boss)

            # Enemy projectile
            if projectile.enemy:
                if projectile.rect.colliderect(player.rect):
                    defense = armors[player_data["armor"]]["defense"]

                    player.hp -= max(
                        1,
                        projectile.damage - defense
                    )

                    if projectile.projectile_type == "ice":
                        player.slow_timer = 3 * FPS

                    if projectile in projectiles:
                        projectiles.remove(projectile)

                    continue

            # Player projectile
            else:
                target = None

                for enemy in enemies:
                    if projectile.rect.colliderect(enemy.rect):
                        target = enemy
                        break

                if (
                    target is None
                    and
                    boss
                    and
                    boss_started
                    and
                    projectile.rect.colliderect(boss.rect)
                ):
                    target = boss

                if target:
                    if projectile.projectile_type in arrow_types:
                        apply_arrow_hit(
                            projectile,
                            target,
                            enemies,
                            boss,
                            explosions,
                            lightning_effects
                        )
                    else:
                        target.hp -= projectile.damage

                        if projectile.projectile_type == "fire":
                            target.apply_burn(6, 240)

                    if projectile in projectiles:
                        projectiles.remove(projectile)

                    continue

            # Walls + closed gates
            hit_wall = False

            for wall in collision_objects:
                if projectile.rect.colliderect(wall):
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
                    projectiles.remove(projectile)

                continue

            if projectile.off_world(world_width):
                if projectile in projectiles:
                    projectiles.remove(projectile)

        # ====================================================
        # DEAD ENEMIES FROM FIRE / EXPLOSIONS
        # ====================================================

        for enemy in enemies[:]:
            if enemy.hp <= 0:
                player_data["gold"] += 15 + level_number * 10
                player_data["xp"] += 15 + level_number * 8
                enemies.remove(enemy)
                check_level_up()

        # ====================================================
        # BOSS DEATH
        # ====================================================

        if (
            boss_started
            and
            boss.hp <= 0
            and
            not boss_defeated
        ):
            boss_defeated = True
            next_level_ready = level_number < len(levels)

            player_data["gold"] += level_number * 250
            player_data["xp"] += level_number * 120
            check_level_up()

            if (
                level_number == player_data["unlocked_level"]
                and
                level_number < len(levels)
            ):
                player_data["unlocked_level"] += 1

            save_game()
            boss.hp = 0

            if next_level_ready:
                message = (
                    data["boss_name"]
                    + " defeated! Press N for Level "
                    + str(level_number + 1)
                )
            else:
                message = (
                    data["boss_name"]
                    + " defeated! ALL 5 LAN LEVELS CLEARED!"
                )

            message_timer = 8 * FPS

        # ====================================================
        # EFFECTS
        # ====================================================

        for explosion in explosions[:]:
            explosion.update()
            if explosion.timer <= 0:
                explosions.remove(explosion)

        for effect in lightning_effects[:]:
            effect.update()
            if effect.timer <= 0:
                lightning_effects.remove(effect)

        # ====================================================
        # PLAYER DEATH / RESPAWN
        # ====================================================

        if player.hp <= 0:
            player.hp = player.max_hp
            player.x = 100
            player.y = 380
            player.rect.x = int(player.x)
            player.rect.y = int(player.y)
            message = "You were defeated! Respawned at the start."
            message_timer = 3 * FPS

        # ====================================================
        # DRAW WORLD
        # ====================================================

        draw_background(level_number, camera)

        for river in rivers:
            river.draw(camera)

        for hidden_path in hidden_paths:
            hidden_path.draw(camera)

        for sign in signs:
            sign.draw(camera)

        fortress.draw(camera)

        for enemy_camp in enemy_camps:
            enemy_camp.draw(camera, enemies)

        for camp in camps:
            camp.draw(camera)

            if camp.near_player(player):
                draw_center(
                    "Press E to enter " + camp.camp_type + " camp",
                    535,
                    SMALL,
                    GOLD
                )

        # Walls
        for wall in walls:
            x = camera.sx(wall.x)

            if -200 < x < WIDTH + 200:
                pygame.draw.rect(
                    screen,
                    GRAY,
                    (x, wall.y, wall.width, wall.height),
                    border_radius=5
                )

                pygame.draw.rect(
                    screen,
                    BLACK,
                    (x, wall.y, wall.width, wall.height),
                    2,
                    border_radius=5
                )

        # Gates
        draw_gates(gates, enemies, camera)

        # Chests
        for chest in chests:
            chest.draw(camera)

        # Enemies
        for enemy in enemies:
            if -100 < camera.sx(enemy.rect.x) < WIDTH + 100:
                enemy.draw(camera)

        # Boss
        if boss_started or camera.sx(boss.rect.x) < WIDTH:
            boss.draw(camera)

            if boss.hp > 0:
                draw_center(
                    data["boss_name"],
                    165,
                    SMALL,
                    RED
                )

        # Projectiles
        for projectile in projectiles:
            projectile.draw(camera)

        # Effects
        for explosion in explosions:
            explosion.draw(camera)

        for effect in lightning_effects:
            effect.draw(camera)

        # Other LAN players
        online_here = 1

        for p in others.values():
            if p.get("level") == level_number:
                draw_lan_remote_player(p, camera)
                online_here += 1

        # Local player
        player.draw(camera)

        # HUD
        draw_hud(
            player,
            level_number,
            world_width
        )

        draw_center(
            "MULTIPLAYER - " + data["name"],
            160,
            FONT,
            CYAN
        )

        draw_text(
            f"ONLINE: {online_here}   {host_ip}",
            790,
            118,
            SMALL,
            CYAN
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
            651,
            SMALL
        )

        draw_text(
            "H Potion | E Camp/Chest | R Ender Pearl | F Hammer | ESC Exit",
            10,
            672,
            SMALL
        )

        if message_timer > 0:
            message_timer -= 1

            pygame.draw.rect(
                screen,
                BLACK,
                (
                    WIDTH // 2 - 260,
                    560,
                    520,
                    45
                ),
                border_radius=8
            )

            draw_center(
                message,
                570,
                SMALL,
                GOLD
            )

        pygame.display.flip()

    try:
        writer.close()
        await writer.wait_closed()
    except Exception:
        pass


async def pvp_arena(host_ip, queue_mode):
    """LAN PvP V3: real arrows, class abilities, character selection, server-owned HP."""
    try:
        reader, writer = await asyncio.wait_for(
            open_game_connection(host_ip, 5050),
            timeout=5
        )
    except Exception:
        end_time = pygame.time.get_ticks() + 2200
        while pygame.time.get_ticks() < end_time:
            screen.fill((18, 18, 32))
            draw_center("COULD NOT CONNECT", 220, BIG, RED)
            draw_center("Make sure server.py is still running.", 290, SMALL)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            await asyncio.sleep(0)
        return

    my_name = str(player_data.get("player_name", "Player"))[:14]
    my_character = player_data.get("character", "Knight")
    writer.write(f"HELLO|{my_name}|{my_character}\n".encode())
    await writer.drain()

    my_id = None
    match_id = None
    my_team = None
    match_mode = None
    in_match = False
    won = None
    queue_count = 0
    others = {}
    pvp_projectiles = {}
    effects = []
    statuses = {}

    player = Player()
    player.hp = 100
    player.max_hp = 100
    player.x = 140
    player.y = 420
    player.rect.x = int(player.x)
    player.rect.y = int(player.y)

    arena_camera = Camera(WIDTH)
    arena_camera.x = 0

    writer.write(f"QUEUE|{queue_mode}\n".encode())
    await writer.drain()

    attack_cooldown_ms = 450
    last_attack_time = -9999
    ability_ready = {"Z": 0, "X": 0, "C": 0}

    def ability_cooldown_ms(key):
        info = characters[player_data["character"]]["abilities"][key]
        return int((info["cooldown"] / FPS) * 1000)

    def status_active(pid, name):
        return statuses.get(pid, {}).get(name, 0) > pygame.time.get_ticks()

    async def send_state():
        if not in_match:
            return
        try:
            writer.write(
                (
                    f"PVPSTATE|{player.x:.1f}|{player.y:.1f}|"
                    f"{player_data.get('character','Knight')}|"
                    f"{player.facing}|{player_data.get('weapon_mode','sword')}|"
                    f"{player_data.get('arrow_type','regular')}\n"
                ).encode()
            )
            await writer.drain()
        except Exception:
            pass

    async def receive_available():
        nonlocal my_id, match_id, my_team, match_mode
        nonlocal in_match, won, queue_count, others

        while True:
            try:
                line = await asyncio.wait_for(reader.readline(), timeout=0.001)
            except asyncio.TimeoutError:
                break
            except Exception:
                return False

            if not line:
                return False

            msg = line.decode(errors="ignore").strip().split("|")
            if not msg:
                continue

            if msg[0] == "WELCOME" and len(msg) >= 2:
                my_id = msg[1]

            elif msg[0] == "QUEUECOUNT" and len(msg) >= 3:
                if msg[1] == queue_mode:
                    try:
                        queue_count = int(msg[2])
                    except ValueError:
                        pass

            elif msg[0] == "MATCH" and len(msg) >= 6:
                match_mode = msg[1]
                match_id = msg[2]
                my_team = msg[3]
                try:
                    player.max_hp = int(float(msg[4]))
                    player.hp = int(float(msg[5]))
                except ValueError:
                    player.max_hp = 100
                    player.hp = 100

                in_match = True
                won = None
                others.clear()
                pvp_projectiles.clear()
                effects.clear()
                statuses.clear()
                ability_ready.update({"Z": 0, "X": 0, "C": 0})

                if my_team == "BLUE":
                    player.x = 135
                    player.facing = 1
                else:
                    player.x = WIDTH - 185
                    player.facing = -1

                player.y = 435
                player.rect.x = int(player.x)
                player.rect.y = int(player.y)

            elif msg[0] == "PVPPLAYER" and len(msg) >= 12:
                pid = msg[1]
                if pid != my_id:
                    try:
                        others[pid] = {
                            "name": msg[2],
                            "team": msg[3],
                            "x": float(msg[4]),
                            "y": float(msg[5]),
                            "hp": int(float(msg[6])),
                            "max_hp": int(float(msg[7])),
                            "character": msg[8],
                            "facing": int(msg[9]),
                            "weapon_mode": msg[10],
                            "arrow_type": msg[11]
                        }
                    except ValueError:
                        pass

            elif msg[0] == "PVPHP" and len(msg) >= 4:
                pid = msg[1]
                try:
                    hp = int(float(msg[2]))
                    max_hp = int(float(msg[3]))
                except ValueError:
                    continue

                if pid == my_id:
                    player.hp = hp
                    player.max_hp = max_hp
                elif pid in others:
                    others[pid]["hp"] = hp
                    others[pid]["max_hp"] = max_hp

            elif msg[0] == "FORCEPOS" and len(msg) >= 4:
                pid = msg[1]
                try:
                    nx = float(msg[2])
                    ny = float(msg[3])
                except ValueError:
                    continue
                if pid == my_id:
                    player.x = nx
                    player.y = ny
                    player.rect.x = int(nx)
                    player.rect.y = int(ny)
                elif pid in others:
                    others[pid]["x"] = nx
                    others[pid]["y"] = ny

            elif msg[0] == "STATUS" and len(msg) >= 4:
                pid = msg[1]
                status_name = msg[2]
                try:
                    duration_ms = int(msg[3])
                except ValueError:
                    duration_ms = 0
                statuses.setdefault(pid, {})[status_name] = pygame.time.get_ticks() + duration_ms

            elif msg[0] == "PVPPROJ" and len(msg) >= 2:
                action = msg[1]
                if action == "SPAWN" and len(msg) >= 10:
                    try:
                        proj_id = msg[2]
                        pvp_projectiles[proj_id] = {
                            "kind": msg[3],
                            "arrow_type": msg[4],
                            "x": float(msg[5]),
                            "y": float(msg[6]),
                            "vx": float(msg[7]),
                            "vy": float(msg[8]),
                            "team": msg[9]
                        }
                    except ValueError:
                        pass
                elif action == "UPDATE" and len(msg) >= 7:
                    proj_id = msg[2]
                    if proj_id in pvp_projectiles:
                        try:
                            pvp_projectiles[proj_id]["x"] = float(msg[3])
                            pvp_projectiles[proj_id]["y"] = float(msg[4])
                            pvp_projectiles[proj_id]["vx"] = float(msg[5])
                            pvp_projectiles[proj_id]["vy"] = float(msg[6])
                        except ValueError:
                            pass
                elif action == "REMOVE" and len(msg) >= 3:
                    pvp_projectiles.pop(msg[2], None)

            elif msg[0] == "PVPEFFECT" and len(msg) >= 7:
                try:
                    effects.append({
                        "type": msg[1],
                        "x1": float(msg[2]),
                        "y1": float(msg[3]),
                        "x2": float(msg[4]),
                        "y2": float(msg[5]),
                        "team": msg[6],
                        "life": 18
                    })
                except ValueError:
                    pass

            elif msg[0] == "RESULT" and len(msg) >= 2:
                won = (msg[1] == "WIN")
                in_match = False
                pvp_projectiles.clear()

            elif msg[0] == "PVPLEFT" and len(msg) >= 2:
                others.pop(msg[1], None)

        return True

    running = True
    last_send = 0

    while running:
        clock.tick(FPS)
        dt = max(0.001, clock.get_time() / 1000.0)
        await asyncio.sleep(0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_ESCAPE:
                if not in_match:
                    running = False
                continue

            if not in_match:
                continue

            if event.key == pygame.K_q:
                player_data["weapon_mode"] = (
                    "bow" if player_data["weapon_mode"] == "sword" else "sword"
                )

            if event.key == pygame.K_SPACE:
                now = pygame.time.get_ticks()
                if now - last_attack_time >= attack_cooldown_ms:
                    mode = player_data["weapon_mode"]
                    arrow_name = player_data.get("arrow_type", "regular")
                    try:
                        writer.write(f"PVPATTACK|{mode}|{arrow_name}\n".encode())
                        await writer.drain()
                        last_attack_time = now
                    except Exception:
                        pass

            ability_key = None
            if event.key == pygame.K_z:
                ability_key = "Z"
            elif event.key == pygame.K_x:
                ability_key = "X"
            elif event.key == pygame.K_c:
                ability_key = "C"

            if ability_key:
                now = pygame.time.get_ticks()
                if now >= ability_ready[ability_key]:
                    try:
                        writer.write(f"PVPABILITY|{ability_key}\n".encode())
                        await writer.drain()
                        ability_ready[ability_key] = now + ability_cooldown_ms(ability_key)
                    except Exception:
                        pass

        if in_match:
            keys = pygame.key.get_pressed()
            speed = player.speed
            if my_id and status_active(my_id, "SLOW"):
                speed *= 0.55

            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player.x -= speed
                player.facing = -1
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player.x += speed
                player.facing = 1
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player.y -= speed
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player.y += speed

            player.x = max(55, min(WIDTH - 105, player.x))
            player.y = max(275, min(HEIGHT - 115, player.y))
            player.rect.x = int(player.x)
            player.rect.y = int(player.y)

            now = pygame.time.get_ticks()
            if now - last_send >= 50:
                await send_state()
                last_send = now

        if not await receive_available():
            running = False

        # Smooth local projectile animation between server updates.
        for proj in pvp_projectiles.values():
            proj["x"] += proj["vx"] * dt
            proj["y"] += proj["vy"] * dt

        # ---------------- DRAW ----------------
        screen.fill((12, 14, 24))
        pygame.draw.rect(screen, (18, 21, 34), (0, 0, WIDTH, 175))
        draw_center("MULTIPLAYER PVP ARENA", 28, BIG, GOLD)

        if not in_match and won is None:
            needed = 2 if queue_mode == "1v1" else 4
            draw_center("QUEUE: " + queue_mode.upper(), 190, FONT, CYAN)
            draw_center(f"Waiting for players... {queue_count}/{needed}", 275, BIG, WHITE)
            draw_center("ESC = leave queue", 350, SMALL, GRAY)

        elif won is not None:
            panel = pygame.Rect(WIDTH // 2 - 260, 185, 520, 310)
            pygame.draw.rect(screen, (28, 32, 48), panel, border_radius=18)
            pygame.draw.rect(screen, GOLD if won else RED, panel, 4, border_radius=18)

            if won:
                draw_center("VICTORY!", 225, HUGE, GOLD)
                draw_center("You won the match.", 315, FONT, WHITE)
            else:
                draw_center("DEFEAT", 225, HUGE, RED)
                draw_center("Better luck next round.", 315, FONT, WHITE)

            draw_center("Press ESC to return to LAN PvP.", 395, SMALL, CYAN)

        else:
            arena = pygame.Rect(25, 190, WIDTH - 50, HEIGHT - 215)
            pygame.draw.rect(screen, (47, 56, 70), arena, border_radius=12)
            pygame.draw.rect(screen, (96, 82, 65), arena, 4, border_radius=12)

            pygame.draw.rect(screen, (45, 85, 115), (25, 190, 190, HEIGHT - 215))
            pygame.draw.rect(screen, (115, 52, 58), (WIDTH - 215, 190, 190, HEIGHT - 215))

            pygame.draw.rect(screen, (90, 75, 58), (WIDTH // 2 - 5, 190, 10, HEIGHT - 215))
            pygame.draw.circle(screen, (105, 90, 70), (WIDTH // 2, 445), 92, 5)
            pygame.draw.circle(screen, (66, 76, 90), (WIDTH // 2, 445), 58, 3)

            draw_text("BLUE SPAWN", 48, 208, SMALL, CYAN)
            draw_text("RED SPAWN", WIDTH - 175, 208, SMALL, RED)

            # Remote players
            for pid, p in others.items():
                draw_lan_remote_player(p, arena_camera)
                labels = []
                if status_active(pid, "SLOW"):
                    labels.append("FROZEN")
                if status_active(pid, "VANISH"):
                    labels.append("VANISH")
                if status_active(pid, "BERSERK"):
                    labels.append("BERSERK")
                if labels:
                    draw_text(" ".join(labels), int(p["x"]) - 2, int(p["y"]) - 38, SMALL, GOLD)

            # Local player
            player.draw(arena_camera)
            if my_id:
                local_labels = []
                if status_active(my_id, "SLOW"):
                    local_labels.append("FROZEN")
                if status_active(my_id, "VANISH"):
                    local_labels.append("VANISH")
                if status_active(my_id, "BERSERK"):
                    local_labels.append("BERSERK")
                if local_labels:
                    draw_text(" ".join(local_labels), int(player.x), int(player.y) - 42, SMALL, GOLD)

            # Real projectiles
            for proj in pvp_projectiles.values():
                x = int(proj["x"])
                y = int(proj["y"])
                kind = proj["kind"]
                arrow_name = proj["arrow_type"]

                if kind == "FIREBALL":
                    pygame.draw.circle(screen, ORANGE, (x, y), 11)
                    pygame.draw.circle(screen, YELLOW, (x, y), 5)
                else:
                    # Arrow shaft + arrow head.
                    direction = 1 if proj["vx"] >= 0 else -1
                    length = 24
                    pygame.draw.line(
                        screen, WHITE,
                        (x - direction * length, y),
                        (x + direction * 4, y),
                        3
                    )
                    pygame.draw.polygon(
                        screen,
                        GOLD,
                        [
                            (x + direction * 8, y),
                            (x - direction * 1, y - 6),
                            (x - direction * 1, y + 6)
                        ]
                    )

                    # Arrow-type visual marker.
                    if arrow_name == "fire":
                        pygame.draw.circle(screen, ORANGE, (x - direction * 9, y), 5)
                    elif arrow_name == "lightning":
                        pygame.draw.circle(screen, CYAN, (x, y), 5, 2)
                    elif arrow_name == "exploding":
                        pygame.draw.circle(screen, RED, (x, y), 6, 2)
                    elif arrow_name == "homing":
                        pygame.draw.circle(screen, GREEN, (x, y), 6, 2)
                    elif arrow_name == "super":
                        pygame.draw.circle(screen, PURPLE, (x, y), 8, 2)

            # Effects
            for eff in list(effects):
                if eff["type"] == "SWORD":
                    pygame.draw.line(
                        screen, GOLD,
                        (int(eff["x1"]), int(eff["y1"])),
                        (int(eff["x2"]), int(eff["y2"])),
                        max(2, eff["life"] // 3)
                    )
                elif eff["type"] in ("HIT", "SLAM", "NOVA", "SPIN"):
                    pygame.draw.circle(
                        screen, RED,
                        (int(eff["x2"]), int(eff["y2"])),
                        10 + (18 - eff["life"]),
                        3
                    )
                elif eff["type"] == "TELEPORT":
                    pygame.draw.circle(
                        screen, PURPLE,
                        (int(eff["x2"]), int(eff["y2"])),
                        18 + (18 - eff["life"]),
                        3
                    )
                elif eff["type"] == "LIGHTNING":
                    pygame.draw.line(
                        screen, CYAN,
                        (int(eff["x1"]), int(eff["y1"])),
                        (int(eff["x2"]), int(eff["y2"])),
                        5
                    )
                eff["life"] -= 1
                if eff["life"] <= 0:
                    effects.remove(eff)

            # Main HUD
            draw_text(
                f"{my_name}   {player_data['character']}   Team {my_team}   "
                f"HP {int(player.hp)}/{int(player.max_hp)}",
                24, 82, FONT, WHITE
            )
            draw_text(
                f"Mode: {player_data['weapon_mode']}   Arrow: {player_data.get('arrow_type','regular')}   "
                f"SPACE attack   Q switch weapon",
                24, 116, SMALL, GOLD
            )

            # Attack cooldown
            now = pygame.time.get_ticks()
            elapsed = max(0, now - last_attack_time)
            ready_ratio = min(1.0, elapsed / attack_cooldown_ms)
            bar_x, bar_y, bar_w, bar_h = WIDTH - 250, 103, 205, 16
            pygame.draw.rect(screen, (55, 55, 65), (bar_x, bar_y, bar_w, bar_h), border_radius=8)
            pygame.draw.rect(
                screen, (200, 200, 210),
                (bar_x, bar_y, int(bar_w * ready_ratio), bar_h),
                border_radius=8
            )
            draw_text(
                "ATTACK READY" if ready_ratio >= 1.0 else "COOLDOWN",
                bar_x + 40, bar_y - 23, SMALL,
                GOLD if ready_ratio >= 1.0 else GRAY
            )

            # Ability HUD
            char_data = characters[player_data["character"]]
            ability_y = 625
            for i, key in enumerate(("Z", "X", "C")):
                info = char_data["abilities"][key]
                remain = max(0, ability_ready[key] - now)
                label = f"{key}: {info['name']}"
                if remain > 0:
                    label += f" {remain / 1000:.1f}s"
                else:
                    label += " READY"
                draw_text(label, 35 + i * 350, ability_y, SMALL, GOLD if remain == 0 else GRAY)

        pygame.display.flip()

    try:
        writer.write(b"LEAVEQUEUE\n")
        await writer.drain()
    except Exception:
        pass

    try:
        writer.close()
        await writer.wait_closed()
    except Exception:
        pass


async def pvp_menu(host_ip):
    while True:
        screen.fill((18, 18, 32))
        draw_center("LAN PVP", 58, BIG, GOLD)
        draw_center(
            f"Character: {player_data.get('character','Knight')}   "
            f"Arrow: {player_data.get('arrow_type','regular')}",
            120,
            SMALL,
            CYAN
        )

        duel_button = Button(380, 190, 340, 55, "QUEUE 1v1 DUEL")
        team_button = Button(380, 265, 340, 55, "QUEUE 2v2")
        character_button = Button(380, 340, 340, 55, "CHANGE CHARACTER")
        back_button = Button(380, 415, 340, 55, "BACK")

        duel_button.draw()
        team_button.draw()
        character_button.draw()
        back_button.draw()

        char_data = characters[player_data.get("character", "Knight")]
        draw_center(
            "Abilities:  Z " + char_data["abilities"]["Z"]["name"]
            + "   |   X " + char_data["abilities"]["X"]["name"]
            + "   |   C " + char_data["abilities"]["C"]["name"],
            515,
            SMALL,
            GOLD
        )
        draw_center("Your equipped adventure arrow type is also used in PvP.", 550, SMALL)
        draw_center("1v1 = 2 players   |   2v2 = 4 players", 585, SMALL)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if duel_button.clicked(event):
                await pvp_arena(host_ip, "1v1")
            elif team_button.clicked(event):
                await pvp_arena(host_ip, "2v2")
            elif character_button.clicked(event):
                await character_select()
            elif back_button.clicked(event):
                return

        clock.tick(FPS)
        await asyncio.sleep(0)


async def lan_hub(host_ip):
    """LAN home screen. Connecting no longer drops you straight into a level."""
    while True:
        screen.fill((18, 18, 32))
        draw_center("LAN SERVER", 65, HUGE, GOLD)
        draw_center("Connected to " + host_ip, 135, SMALL, CYAN)

        adventure_button = Button(380, 205, 340, 55, "CO-OP ADVENTURE")
        pvp_button = Button(380, 280, 340, 55, "PVP ARENA")
        name_button = Button(380, 355, 340, 55, "CHANGE PLAYER NAME")
        back_button = Button(380, 430, 340, 55, "BACK TO GAME MENU")

        adventure_button.draw()
        pvp_button.draw()
        name_button.draw()
        back_button.draw()

        draw_center(
            "Choose what you want to do on the LAN server.",
            520,
            SMALL,
            WHITE
        )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if adventure_button.clicked(event):
                await lan_game(host_ip)
            elif pvp_button.clicked(event):
                await pvp_menu(host_ip)
            elif name_button.clicked(event):
                await player_name_screen(True)
            elif back_button.clicked(event):
                return

        clock.tick(FPS)
        await asyncio.sleep(0)


async def lan_menu():
    # Kept this function name so older menu code still works.
    while True:
        screen.fill((18, 18, 32))
        draw_center("MULTIPLAYER", 70, BIG, GOLD)
        local_button = Button(380, 175, 340, 55, "LAN / SAME COMPUTER")
        online_button = Button(380, 245, 340, 55, "ONLINE (RENDER)")
        name_button = Button(380, 315, 340, 55, "CHANGE PLAYER NAME")
        back_button = Button(380, 385, 340, 55, "BACK")
        local_button.draw(); online_button.draw(); name_button.draw(); back_button.draw()
        draw_center("Browser LAN now uses WebSocket too.", 485, SMALL, CYAN)
        draw_center("Render uses a secure wss:// address.", 515, SMALL, GOLD)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if local_button.clicked(event):
                address = await lan_ip_screen()
                if address:
                    await lan_hub(address)
            elif online_button.clicked(event):
                address = await online_server_screen()
                if address and "YOUR-SERVICE" not in address:
                    await lan_hub(address)
            elif name_button.clicked(event):
                await player_name_screen(True)
            elif back_button.clicked(event):
                return
        clock.tick(FPS)
        await asyncio.sleep(0)


async def main_menu():

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
            "PLAY ADVENTURE"
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

        lan_button = Button(
            380,
            390,
            340,
            55,
            "MULTIPLAYER"
        )

        save_button = Button(
            380,
            460,
            340,
            55,
            "SAVE GAME"
        )

        load_button = Button(
            380,
            530,
            340,
            55,
            "LOAD GAME"
        )

        quit_button = Button(
            380,
            600,
            340,
            55,
            "QUIT"
        )

        play_button.draw()

        character_button.draw()

        shop_button.draw()

        lan_button.draw()

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
            665,
            SMALL
        )

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                save_game()

                pygame.quit()

                return

            if play_button.clicked(event):
                await level_select()

            elif character_button.clicked(event):
                await character_select()

            elif shop_button.clicked(event):
                await shop()

            elif lan_button.clicked(event):
                await lan_menu()

            elif save_button.clicked(event):
                save_game()

            elif load_button.clicked(event):
                load_game()

            elif quit_button.clicked(event):
                save_game()
                pygame.quit()
                return

        clock.tick(FPS)
        await asyncio.sleep(0)


# ============================================================
# START GAME
# ============================================================

load_game()

async def start_game():
    await player_name_screen(False)
    await main_menu()

asyncio.run(start_game())
