import pygame.display

# --- Constant --- #
nb_fps = 60
size_player = [48, 86]
g = 1
air_resistance = 1
jump_duration = 0.3

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
hero_try_skills = {'acceleration': 4, 'maxspeed': [18, 16], 'jump': 18, 'down_smash': 1.3, 'walljump': [18, 18, 2], 'doublejump': 1, 'health': [100, 100], 'mass': 1.3, 'attack_1': {'name': 'kick', 'damage': 10, 'killable': [], 'reload': 0.4, 'duration': 0.2, 'size': [size_player[0]/(2/3), size_player[1]/4], 'special': {}}}

arcane_mage_skills = {'acceleration': 2, 'maxspeed': [14, 20], 'jump': 14, 'down_smash': 1.2, 'walljump': [14, 14, 1], 'doublejump': 2, 'health': [100, 100], 'mass': 0.3, 'attack_1': {'name': 'spell', 'damage': 20, 'killable': ['player'], 'reload': 1, 'duration': 5, 'speed': 5, 'rng': 1, 'size': 42, 'special': {'bounce': True, 'explode': False}}}

chevalier = {'acceleration': 3, 'maxspeed': [15, 10], 'jump': 16, 'down_smash': 1.2, 'walljump': [18, 12, 1], 'doublejump': 1, 'health': [100, 100], 'mass': 0.8, 'attack_1': {'name': 'spell', 'damage': 5, 'killable': ['player', 'wall'], 'reload': 0.3, 'duration': 2, 'speed': 16, 'rng': 1, 'size': 16, 'special': {'bounce': False, 'explode': False}}}


tit2_skills = {'acceleration': 5, 'maxspeed': [16, 12], 'jump': 22, 'down_smash': 1.5, 'walljump': [14, 20, 2], 'doublejump': 1, 'health': [100, 100], 'mass': 1.3, 'attack_1': {'name': 'kick', 'damage': 10, 'killable': [], 'reload': 0.8, 'duration':  0.4, 'size': {'side': [size_player[0]/(2/3), size_player[0]/2], 'down': [size_player[0]//(2/3), size_player[0]], 'up': [size_player[0]//(2/3), size_player[0]]}, 'special': {}}}

heroes_skills = {'hero_try': hero_try_skills, 'arcane_mage': arcane_mage_skills, 'tit2': tit2_skills, 'chevalier': chevalier}

attacks_type = {'kick': 'melee', 'spell': 'projectile'}

max_vspeed = 32  # vertical speed
max_hspeed = 32  # horizontal speed
# --- Game --- #
arena = 'arena_1'
