import pygame.transform, pygame.time
import ressources as rs
import ClassDetectors
import vars as vr


class special_skill:
    def __init__(self, sender, type, damage, coordi, speedi, duration, width, effects, num):
        self.sender = sender
        self.type = type
        self.damage = damage
        self.duration = duration * 1000
        self.start_time = vr.time
        self.speed = speedi
        self.coord = [coordi[0], coordi[1]]
        self.width = width
        self.hitbox = [[self.coord[0] - self.width // 2, self.coord[1] - self.width // 2],
                       [self.coord[0] + self.width // 2, self.coord[1] + self.width // 2]]
        self.visual = pygame.transform.scale(rs.special[self.type], [width, width])
        self.effects = effects
        self.bounce, self.explode, self.repulsion = False, False, 0
        self.initEffects()

        if self.bounce or self.explode:
            self.detectors = self.initDetectors()
        else:
            self.detectors = []
        self.num = num
        return

    def getx(self):  # return the coord visualised
        return self.coord[0] - self.width // 2

    def gety(self):
        return self.coord[1] - self.width // 2

    def initEffects(self):
        try:
            if self.effects['bounce'] is True:
                self.bounce = True
            try:
                if self.effects['explode'] is True:
                    self.explode = True
            except:
                pass
        except:
            pass

    def initDetectors(self):
        detectors = [ClassDetectors.detector([self.width//2, 0], self.sender, [self.width, self.width]),
                     ClassDetectors.detector([0, self.width//2], self.sender, [self.width, self.width]),
                     ClassDetectors.detector([-self.width//2, 0], self.sender, [self.width, self.width]),
                     ClassDetectors.detector([0, -self.width//2], self.sender, [self.width, self.width])]
        return detectors

    def update(self):

        if self.explode:
            if self.detectors[0].state or self.detectors[2].state or self.detectors[1].state or self.detectors[3].state:
                # make explosion
                pass

        if self.bounce:

            if (self.detectors[0].state or self.detectors[2].state) and (self.detectors[0].collide_with == 'wall' or self.detectors[2].collide_with == 'wall'):
                self.speed[0] = -self.speed[0]
            if (self.detectors[1].state or self.detectors[3].state) and (self.detectors[1].collide_with == 'wall' or self.detectors[3].collide_with == 'wall'):
                self.speed[1] = -self.speed[1]

        self.coord[0], self.coord[1] = self.coord[0] + self.speed[0], self.coord[1] + self.speed[1]
        self.hitbox = [[self.coord[0] - self.width // 2, self.coord[1] - self.width // 2],
                       [self.coord[0] + self.width // 2, self.coord[1] + self.width // 2]]

        if self.detectors:
            for detector in self.detectors:
                detector.update(self.coord)

        #vr.events[str(self.num)] = self
