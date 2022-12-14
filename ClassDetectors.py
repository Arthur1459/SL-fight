import pygame as pg
import vars as vr
import config as cf


class detector:
    def __init__(self, coord_modifier, name, size):
        self.name = name
        self.state = False
        self.coord = [0, 0]
        self.size = size
        self.modifier = coord_modifier
        self.hitbox, self.size = self.setHitbox()
        self.visuals = [pg.transform.scale(pg.image.load("ressources/visuals/others/detector.png"), self.size),
                        pg.transform.scale(pg.image.load("ressources/visuals/others/detector2.png"), self.size)]
        self.visual = self.visuals[0]
        self.collide_with = 'nothing'
        self.data = {'colliding': self.collide_with, 'origins': None, 'damage': 0, 'repulsion': 0, 'freeze': False}

    def setHitbox(self):
        if abs(self.modifier[0]) > abs(self.modifier[1]):
            hitbox = [[self.coord[0], self.coord[1] - self.size[1]//3], [self.coord[0], self.coord[1] + self.size[1]//3]]
            return hitbox, [1, self.size[1]//(3/2)]
        else:
            hitbox = [[self.coord[0] + self.size[0]//6, self.coord[1]], [self.coord[0] - self.size[0]//6, self.coord[1]]]
            return hitbox, [self.size[0]//3, 1]

    def coord_draw(self):
        return self.hitbox[0]

    def is_colliding(self, hitbox_ext):
        if hitbox_ext[0][0] < self.hitbox[0][0] < hitbox_ext[1][0] \
                and hitbox_ext[0][1] < self.hitbox[0][1] < hitbox_ext[1][1] \
                or hitbox_ext[0][0] < self.hitbox[0][0] < hitbox_ext[1][0] \
                and hitbox_ext[0][1] < self.hitbox[1][1] < hitbox_ext[1][1] \
                or hitbox_ext[0][0] < self.hitbox[1][0] < hitbox_ext[1][0] \
                and hitbox_ext[0][1] < self.hitbox[0][1] < hitbox_ext[1][1] \
                or hitbox_ext[0][0] < self.hitbox[1][0] < hitbox_ext[1][0] \
                and hitbox_ext[0][1] < self.hitbox[0][1] < hitbox_ext[1][1] \
                or ((hitbox_ext[0][0] < self.hitbox[0][0] and self.hitbox[1][0] < hitbox_ext[1][0]) and ((hitbox_ext[0][1] < self.hitbox[1][1] < hitbox_ext[1][1]) or (hitbox_ext[0][1] < self.hitbox[0][1] < hitbox_ext[1][1]) or self.hitbox[0][1] < hitbox_ext[0][1] <= hitbox_ext[1][1] < self.hitbox[1][1])) \
                or ((hitbox_ext[0][1] < self.hitbox[0][1] <= self.hitbox[1][1] < hitbox_ext[1][1]) and (hitbox_ext[0][0] < self.hitbox[0][0] < hitbox_ext[1][0] or hitbox_ext[0][0] < self.hitbox[1][0] < hitbox_ext[1][0] or self.hitbox[0][0] < hitbox_ext[0][0] <= hitbox_ext[1][0] < self.hitbox[1][0])):
            return True
        else:
            return False

    def update(self, new_coord):

        self.coord[0] = new_coord[0] + self.modifier[0]
        self.coord[1] = new_coord[1] + self.modifier[1]
        self.hitbox = self.setHitbox()[0]

        self.state = False
        self.visual = self.visuals[0]
        self.collide_with = 'nothing'

        for key in vr.solids.keys():
            if vr.solids[key].name != self.name:
                if self.is_colliding([vr.solids[key].topleft, vr.solids[key].downright]):
                    self.state = True
                    self.visual = self.visuals[1]
                    self.collide_with = vr.solids[key].name

        self.data['damage'] = 0
        self.data['repulsion'] = 0
        self.data['num'] = None

        for key in vr.events.keys():
            if cf.attacks_type[vr.events[key].type] and vr.events[key].sender != self.name:  # means it's an attack
                if self.is_colliding(vr.events[key].hitbox):  # Why this test doesn't work ?
                    self.state = True
                    self.collide_with = cf.attacks_type[vr.events[key].type]
                    self.collide_with = cf.attacks_type[vr.events[key].type]
                    self.data['damage'] = vr.events[key].damage
                    self.data['repulsion'] = vr.events[key].repulsion
                    self.data['num'] = vr.events[key].num

        self.data['colliding'] = self.collide_with

        return
