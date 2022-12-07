import pygame as pg
import config as cf

# -- heroes -- #
hero_try = {'stand': [pg.transform.scale(pg.image.load('ressources/visuals/heroes/herotry/herotry.png'), cf.size_player)], 'jump': [pg.transform.scale(pg.image.load('ressources/visuals/heroes/herotry/jump.png'), cf.size_player)], 'walk': [pg.transform.scale(pg.image.load('ressources/visuals/heroes/herotry/walk_1.png'), cf.size_player), pg.transform.scale(pg.image.load('ressources/visuals/heroes/herotry/walk_2.png'), cf.size_player)]}
arcane_mage = {'stand': [pg.transform.scale(pg.image.load('ressources/visuals/heroes/arcane_mage/stand.png'), cf.size_player)], 'jump': [pg.transform.scale(pg.image.load('ressources/visuals/heroes/arcane_mage/stand.png'), cf.size_player)], 'walk': [pg.transform.scale(pg.image.load('ressources/visuals/heroes/arcane_mage/stand.png'), cf.size_player), pg.transform.scale(pg.image.load('ressources/visuals/heroes/arcane_mage/stand.png'), cf.size_player)]}
tit2 = {'stand': [pg.transform.scale(pg.image.load('ressources/visuals/heroes/tit2/tit2.png'), cf.size_player)], 'jump': [pg.transform.scale(pg.image.load('ressources/visuals/heroes/tit2/jump.png'), cf.size_player)], 'walk': [pg.transform.scale(pg.image.load('ressources/visuals/heroes/tit2/walk_1.png'), cf.size_player), pg.transform.scale(pg.image.load('ressources/visuals/heroes/tit2/walk_2.png'), cf.size_player)], 'attack_1': {'side': [pg.transform.scale(pg.image.load('ressources/visuals/heroes/tit2/hit_2.png'), cf.size_player), pg.transform.scale(pg.image.load('ressources/visuals/heroes/tit2/hit_1.png'), cf.size_player)], 'down': [pg.transform.scale(pg.image.load('ressources/visuals/heroes/tit2/hit_down.png'), cf.size_player)], 'up': [pg.transform.scale(pg.image.load('ressources/visuals/heroes/tit2/hit_1.png'), cf.size_player)]}}

hero_visuals = {'hero_try': hero_try, 'arcane_mage': arcane_mage, 'tit2': tit2}

# -- Projectiles -- #
projectiles = {'spell': pg.image.load('ressources/visuals/projectiles/spell.png')}
special = {'spec_tit': pg.image.load('ressources/visuals/melee/kick.png')}
melee = {'kick': pg.image.load('ressources/visuals/melee/kick.png')}


# -- GUI -- #
backs = {'back1': pg.image.load('ressources/visuals/backgrounds/back1.png')}

# -- Arena -- #
arena_1_blocks = [[[0, 0], [40, cf.screeny]], [[(cf.screenx - 40), 0], [cf.screenx, cf.screeny]], [[0, (cf.screeny - 120)], [cf.screenx, cf.screeny]], [[0, 0], [cf.screenx, 40]], [[740, 500], [880, 600]], [[740, 300], [880, 400]]]
arena_blocks = {'arena_1': arena_1_blocks}
