import pygame.transform, pygame.time
import ressources as rs
import config as cf
import vars as vr

class melee:
    def __init__(self, sender, type, damage, coordi, speedi, duration, dimension, special, num, orient):
        self.instance = 'melee'
        self.sender = sender
        self.type = type
        self.damage = damage
        self.duration = duration * 1000
        self.start_time = vr.time
        self.speed = speedi
        self.orient = [orient[0], orient[1]]
        self.coord = [coordi[0] + cf.size_player[0] // (4 / 3) * self.orient[0],
                      coordi[1] + cf.size_player[1] // (4 / 3) * self.orient[1]]
        if self.orient[1] != 0:
            self.dimension = [dimension[1], dimension[0]]
        else:
            self.dimension = [dimension[0], dimension[1]]
        self.hitbox = [[self.coord[0] - self.dimension[0] // 2, self.coord[1] - self.dimension[1] // 2],
                       [self.coord[0] + self.dimension[0] // 2, self.coord[1] + self.dimension[1] // 2]]
        self.visual = pygame.transform.scale(rs.melee[self.type],
                                             [min(dimension[0], dimension[1]), min(dimension[0], dimension[1])])
        self.special = special
        self.explode, self.repulsion = False, 0
        self.initSpecial()
        self.num = num
        return

    def getx(self):  # return the coord visualised
        return self.coord[0] - self.dimension[0] // 2

    def gety(self):
        return self.coord[1] - self.dimension[1] // 2

    def initSpecial(self):
        try:
            if self.special['explode'] is True:
                self.explode = True
        except:
            pass

    def update(self):

        if self.explode:
            # make explosion
            pass

        self.coord[0], self.coord[1] = vr.players[self.sender].coord[0] + cf.size_player[0] // (4 / 3) * self.orient[0], vr.players[self.sender].coord[1] + cf.size_player[1] // (4 / 3) * self.orient[1]
        self.hitbox = [[self.coord[0] - self.dimension[0] // 2, self.coord[1] - self.dimension[1] // 2],
                       [self.coord[0] + self.dimension[0] // 2, self.coord[1] + self.dimension[1] // 2]]

    def get(self):
        return self
