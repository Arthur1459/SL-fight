import pygame as pg
import vars as vr
import config as cf


class detector:
    def __init__(self, coord_modifier, name, size):
        self.instance = 'detector'
        self.name = name
        self.state, self.blocked = False, False
        self.coord = [0, 0]
        self.modifier = coord_modifier
        self.size = self.setSize(size)
        self.hitbox = self.setHitbox()
        self.visuals = [pg.transform.scale(pg.image.load("ressources/visuals/others/detector.png"), self.size),
                        pg.transform.scale(pg.image.load("ressources/visuals/others/detector2.png"), self.size)]
        self.visual = self.visuals[0]
        self.collide_with = 'nothing'
        self.data = {'colliding': self.collide_with, 'origins': None, 'damage': 0, 'repulsion': 0, 'freeze': False}

    def setHitbox(self):
        if abs(self.modifier[0]) > abs(self.modifier[1]):
            hitbox = [[self.coord[0], self.coord[1] - self.size[1]//2], [self.coord[0], self.coord[1] + self.size[1]//2]]
            return hitbox
        else:
            hitbox = [[self.coord[0] - self.size[0]//2, self.coord[1]], [self.coord[0] + self.size[0]//2, self.coord[1]]]
            return hitbox

    def setSize(self, size):
        if abs(self.modifier[0]) > abs(self.modifier[1]):
            return [1, size[1]//2]
        else:
            return [size[0]//2, 1]

    def coord_draw(self):
        return self.hitbox[0]

    def is_colliding(self, hitbox_ext):
        width_self = self.hitbox[1][0] - self.hitbox[0][0]
        height_self = self.hitbox[1][1] - self.hitbox[0][1]
        width_ext = hitbox_ext[1][0] - hitbox_ext[0][0]
        height_ext = hitbox_ext[1][1] - hitbox_ext[0][1]
        if self.hitbox[0][0] <= hitbox_ext[0][0] + width_ext \
            and self.hitbox[0][0] + width_self >= hitbox_ext[0][0] \
            and self.hitbox[0][1] <= hitbox_ext[0][1] + height_ext \
            and self.hitbox[0][1] + height_self >= hitbox_ext[0][1]:
            return True
        else:
            return False

    def update(self, new_coord):

        self.coord[0] = new_coord[0] + self.modifier[0]
        self.coord[1] = new_coord[1] + self.modifier[1]
        self.hitbox = self.setHitbox()

        self.data['damage'] = 0
        self.data['repulsion'] = 0
        self.data['num'] = None
        self.data['instance'] = None

        self.state = False
        self.blocked = False
        self.visual = self.visuals[0]
        self.collide_with = 'nothing'

        for key in vr.solids.keys():
            if vr.solids[key].name != self.name:
                if self.is_colliding([vr.solids[key].topleft, vr.solids[key].downright]):
                    self.state = True
                    self.visual = self.visuals[1]
                    self.collide_with = vr.solids[key].name
                    self.data['colliding'] = 'solid'
                    self.data['num'] = vr.solids[key].num
                    self.data['instance'] = vr.solids[key].instance
                    self.blocked = True

        for key in vr.events.keys():
            if cf.attacks_type[vr.events[key].get().name] and vr.events[key].get().sender != self.name:  # means it's an attack
                if self.is_colliding(vr.events[key].get().hitbox):
                    self.state = True
                    self.collide_with = vr.events[key].get().name
                    try:
                        self.data['damage'] = vr.events[key].get().damage
                        self.data['repulsion'] = vr.events[key].get().repulsion
                        self.data['num'] = vr.events[key].get().num
                        self.data['instance'] = vr.events[key].get().instance
                        self.data['colliding'] = cf.attacks_type[self.collide_with]
                    except:
                        pass

        return

    def get(self):
        return self
