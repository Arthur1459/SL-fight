import pygame.display

# --- Constant --- #
nb_fps = 50
size_player = [48, 86]
g = 1

# --- Pygame --- #
pygame.display.init()
screenDimension = [1280, 720]
screenx, screeny = screenDimension[0], screenDimension[1]
screenxmid, screenymid = screenx//2, screeny//2
backcolor = pygame.Color('NavyBlue')
backs = ['ressources/visuals/backgrounds/back1.png']

# --- Players --- #
players_inputs = {'1': {'right': "RIGHT", 'left': "LEFT", 'up': "UP", 'down': "DOWN", 'attack_1': "L", 'attack2': "F"}, '2': {'right': "D", 'left': "Q", 'up': "Z", 'down': "S", 'attack_1': "G"}}
# Format :
# attack_1 :
# 'projectile' : [type, damage, reloading, speed, duration, width, special]
# 'melee' = [type, damage, reloading, duration, dimension, special]
# special
hero_try_skills = {'acceleration': 4, 'maxspeed': 18, 'jump': 18, 'walljump': [18, 18, 2], 'doublejump': 1, 'health': [100, 100], 'attack_1': ['kick', 10, 0.4, 0.2, [size_player[0]//(2/3), size_player[1]//4], {}]}

arcane_mage_skills = {'acceleration': 2,'maxspeed': 18, 'jump': 14, 'walljump': [14, 14, 1], 'doublejump': 2, 'health': [150, 200], 'attack_1': ['spell', 20, 1, 6, 4, 48, {'bounce': True, 'explode': False}]}

tit2_skills = {'acceleration': 5, 'maxspeed': 16, 'jump': 20, 'walljump': [14, 20, 2], 'doublejump': 1, 'health': [100, 100], 'attack_1': ['kick', 10, 0.8, 0.4, {'side': [size_player[0]//(2/3), size_player[0]//3], 'down': [size_player[0]//(2/3), size_player[0]*5/4], 'up': [size_player[0]*1.2, size_player[0]//3]}, {}],'special': {}}

heroes_skills = {'hero_try': hero_try_skills, 'arcane_mage': arcane_mage_skills, 'tit2': tit2_skills}

attacks_type = {'kick': 'melee', 'spell': 'projectile'}

max_vspeed = 20  # vertical speed
max_hspeed = 16  # horizontal speed

# --- Game --- #
arena = 'arena_1'
