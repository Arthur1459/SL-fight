import pygame as pg
import config as cf

# --- Fct scale image --- #
def scale(target, size):
    if size[0] <= size[1]:
        return [target[0], size[1]*target[0]/size[0]]
    else:
        return [target[0]*target[1]/size[1], size[1]]

# -- heroes -- #
hero_try = {'stand': [pg.transform.scale(pg.image.load('ressources/visuals/heroes/herotry/herotry.png'), cf.size_player)], 'jump': [pg.transform.scale(pg.image.load('ressources/visuals/heroes/herotry/jump.png'), cf.size_player)], 'walk': [pg.transform.scale(pg.image.load('ressources/visuals/heroes/herotry/walk_1.png'), cf.size_player), pg.transform.scale(pg.image.load('ressources/visuals/heroes/herotry/walk_2.png'), cf.size_player)]}
arcane_mage = {'stand': [pg.transform.scale(pg.image.load('ressources/visuals/heroes/arcane_mage/stand.png'), cf.size_player)], 'jump': [pg.transform.scale(pg.image.load('ressources/visuals/heroes/arcane_mage/stand.png'), cf.size_player)], 'walk': [pg.transform.scale(pg.image.load('ressources/visuals/heroes/arcane_mage/stand.png'), cf.size_player), pg.transform.scale(pg.image.load('ressources/visuals/heroes/arcane_mage/stand.png'), cf.size_player)]}
chevalier = {'stand': [pg.transform.scale(pg.image.load('ressources/visuals/heroes/arcane_mage/stand.png'), cf.size_player)], 'jump': [pg.transform.scale(pg.image.load('ressources/visuals/heroes/arcane_mage/stand.png'), cf.size_player)], 'walk': [pg.transform.scale(pg.image.load('ressources/visuals/heroes/arcane_mage/stand.png'), cf.size_player), pg.transform.scale(pg.image.load('ressources/visuals/heroes/arcane_mage/stand.png'), cf.size_player)]}
tit2 = {'stand': [pg.transform.scale(pg.image.load('ressources/visuals/heroes/tit2/tit2.png'), cf.size_player)], 'jump': [pg.image.load('ressources/visuals/heroes/tit2/jump.png')], 'walk': [pg.image.load('ressources/visuals/heroes/tit2/walk_1.png'), pg.image.load('ressources/visuals/heroes/tit2/walk_2.png')], 'attack_1': {'side': [pg.image.load('ressources/visuals/heroes/tit2/hit_2.png'), pg.image.load('ressources/visuals/heroes/tit2/hit_1.png')], 'down': [pg.image.load('ressources/visuals/heroes/tit2/hit_down.png')], 'up': [pg.image.load('ressources/visuals/heroes/tit2/up_hit1.png'), pg.image.load('ressources/visuals/heroes/tit2/up_hit2.png')]}}

hero_visuals = {'hero_try': hero_try, 'arcane_mage': arcane_mage, 'tit2': tit2, 'chevalier': chevalier}

# --- to remove (maybe) --- #
# for hero_key in hero_visuals.keys():
#     for key in hero_visuals[hero_key].keys():
#         if isinstance(hero_visuals[hero_key][key], list):
#             for num in range(len(hero_visuals[hero_key][key])):
#                 hero_visuals[hero_key][key][num] = pg.transform.scale(hero_visuals[hero_key][key][num], scale(cf.size_player, hero_visuals[hero_key][key][num].get_size()))
#         elif isinstance(hero_visuals[hero_key][key], dict):
#             for spe_key in hero_visuals[hero_key][key].keys():
#                 for num in range(len(hero_visuals[hero_key][key][spe_key])):
#                     hero_visuals[hero_key][key][spe_key][num] = pg.transform.scale(hero_visuals[hero_key][key][spe_key][num], scale(cf.size_player, hero_visuals[hero_key][key][spe_key][num].get_size()))


# -- Projectiles -- #
projectiles = {'spell': pg.image.load('ressources/visuals/projectiles/spell.png')}
special = {'spec_tit': pg.image.load('ressources/visuals/melee/kick.png')}
melee = {'kick': pg.image.load('ressources/visuals/melee/kick.png')}


# -- GUI -- #
backs = {'back1': pg.image.load('ressources/visuals/backgrounds/back1.png')}

# -- Arena -- #
arena_1_blocks = [[[0, 0], [40, cf.screeny]], [[(cf.screenx - 40), 0], [cf.screenx, cf.screeny]], [[0, (cf.screeny - 135)], [cf.screenx, cf.screeny]], [[0, 0], [cf.screenx, 40]], [[740, 500], [880, 585]], [[740, 300], [880, 400]]]
arena_blocks = {'arena_1': arena_1_blocks}

