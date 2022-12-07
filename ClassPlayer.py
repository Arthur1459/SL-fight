import ClassProjectiles
import ressources as rs
import config as cf
import vars as vr
import ClassDetectors
import ClassSolid
import pygame.transform
import ClassMelee


class Player:
    def __init__(self, name, player_n, coord):
        self.name = name
        self.player_n = player_n
        self.coord = [coord[0], coord[1]]
        self.speed, self.orient, self.attack_orient = [0, 0], [1, 0], 'side'
        self.state = 'stand'
        self.last_time = vr.time
        self.start_phase, self.len_phase, self.current_phase, self.attack_time = vr.time, 0, 0, 0
        self.visual = (rs.hero_visuals[self.name])[self.state][0]
        self.size = self.visual.get_size()  # already with the size of a player
        self.hitbox = [[self.coord[0] - self.getwidth()//2, self.coord[0] - self.getheight()//2], [self.coord[0] + self.getwidth()//2, self.coord[0] + self.getheight()//2]]
        self.inputs = cf.players_inputs[player_n]
        self.detectors = self.initDetectors()
        self.skills = cf.heroes_skills[self.name]
        self.current_walljumps, self.current_doublejumps, self.current_attack_1 = 0, 0, 0
        self.num, self.last_time = vr.solid_num, vr.time
        vr.solids[self.num] = ClassSolid.Block(self.hitbox[0], self.hitbox[1], self.name, self.num)
        vr.solid_num += 1
        return

    def getx(self):  # return the coord visualised
        return self.coord[0] - self.getwidth()//2

    def gety(self):
        return self.coord[1] - self.getheight()//2

    def getwidth(self):
        return self.size[0]

    def getheight(self):
        return self.size[1]

    def getHealth(self):
        return self.skills['health']

    def getCoordHealthBar(self):
        return [[self.getx(), self.gety() - 10], [self.getx(), self.gety() - 10]]

    def initDetectors(self):
        detectors = [ClassDetectors.detector([self.getwidth() // 2, 0], self.name, cf.size_player),
                     ClassDetectors.detector([0, self.getheight() // 2], self.name, cf.size_player),
                     ClassDetectors.detector([-self.getwidth() // 2, 0], self.name, cf.size_player),
                     ClassDetectors.detector([0, -self.getheight() // 2], self.name, cf.size_player),
                     ClassDetectors.detector([self.getwidth() // 2.2, 0], self.name, cf.size_player),
                     ClassDetectors.detector([0, self.getheight() // 2.2], self.name, cf.size_player),
                     ClassDetectors.detector([-self.getwidth() // 2.2, 0], self.name, cf.size_player),
                     ClassDetectors.detector([0, -self.getheight() // 2.2], self.name, cf.size_player)]
        return detectors

    def get_state(self):
        states=[]
        if vr.inputs[self.inputs['attack_1']] and self.current_attack_1 <= 0:
            states.append('attack_1')
        if self.skills['health'][0] <= 0:
            states.append('dead')
        if self.detectors[0].state is True:
            states.append('right')
        if self.detectors[1].state is True:
            states.append('down')
        if self.detectors[2].state is True:
            states.append('left')
        if self.detectors[3].state is True:
            states.append('up')
        if self.detectors[1].state is True:
            states.append('right')
        if self.detectors[1].state is False and self.attack_time <= 0:
            states.append('jump')
        elif self.speed[0] != 0 and self.attack_time <= 0:
            states.append('walk')
        elif self.attack_time <= 0:
            states.append('stand')
        return

    def updateDetectors(self):
        for detector in self.detectors:
            detector.update(self.coord)
        return True

    def updatevisual(self):
        try:
            if self.state == 'attack_1':
                self.len_phase = len((rs.hero_visuals[self.name])[self.state][self.attack_orient])
                print(self.attack_orient)
                if vr.time - self.start_phase > 200:
                    self.current_phase += 1
                    self.start_phase = vr.time
                if self.current_phase >= self.len_phase:
                    self.current_phase = 0

                if self.orient[0] >= 0:
                    self.visual = (rs.hero_visuals[self.name])[self.state][self.attack_orient][self.current_phase]

                else:
                    self.visual = pygame.transform.flip((rs.hero_visuals[self.name])[self.state][self.attack_orient][self.current_phase], True, False)

            elif self.state == 'walk' and self.attack_time <= 0:
                self.len_phase = len((rs.hero_visuals[self.name])[self.state])
                if vr.time - self.start_phase > 200:
                    self.current_phase += 1
                    self.start_phase = vr.time
                if self.current_phase >= self.len_phase:
                    self.current_phase = 0

                if self.orient[0] >= 0:
                    self.visual = (rs.hero_visuals[self.name])[self.state][self.current_phase]

                else:
                    self.visual = pygame.transform.flip((rs.hero_visuals[self.name])[self.state][self.current_phase], True, False)

            elif self.attack_time <= 0:
                if self.orient[0] >= 0:
                    self.visual = (rs.hero_visuals[self.name])[self.state][0]
                else:
                    self.visual = pygame.transform.flip((rs.hero_visuals[self.name])[self.state][0], True, False)

        except:
            print("ERROR : Missing hero visual")

    def updatepos(self):
        if self.attack_time <= 0:
            if vr.inputs[self.inputs['right']]:
                self.orient[0] = 1
                self.orient[1] = 0
            if vr.inputs[self.inputs['left']]:
                self.orient[0] = -1
                self.orient[1] = 0
            if vr.inputs[self.inputs['up']]:
                self.orient[1] = -1
                if not(vr.inputs[self.inputs['right']] and vr.inputs[self.inputs['left']]):
                    self.orient[0] = 0
            if vr.inputs[self.inputs['down']]:
                self.orient[1] = 1

        self.coord[0], self.coord[1] = self.coord[0] + self.speed[0], self.coord[1] + self.speed[1]
        self.hitbox = [[self.coord[0] - self.getwidth()//2, self.coord[1] - self.getheight()//2], [self.coord[0] + self.getwidth()//2, self.coord[1] + self.getheight()//2]]
        if not(0 < self.getx() < cf.screenx) or not(0 < self.gety() < cf.screeny):
            print("\nERROR Coordinate of", self.name, "unexpected.\n")
            self.coord = [200, 200]
        vr.solids[self.num] = ClassSolid.Block(self.hitbox[0], self.hitbox[1], self.name, self.num)

    def attack(self):
        if vr.inputs[self.inputs['attack_1']] and self.current_attack_1 <= 0:
            self.current_attack_1 = self.skills['attack_1'][2]*1000  # reloading time
            self.state, self.attack_time = 'attack_1', self.skills['attack_1'][3]*1000  # time of the attack time (animations) -> to set
            # self.visual =  (rs.hero_visuals[self.name])[self.state][1]
            if cf.attacks_type[self.skills['attack_1'][0]] == 'projectile':
                self.state = 'attack_1'
                vr.events[str(vr.event_num)] = ClassProjectiles.projectile(self.name, self.skills['attack_1'][0], self.skills['attack_1'][1], self.coord, [self.skills['attack_1'][3] * self.orient[0], self.skills['attack_1'][3] * self.orient[1]], self.skills['attack_1'][4], self.skills['attack_1'][5], self.skills['attack_1'][6], vr.event_num)
                vr.event_num += 1
                print("New Projectile attack :", vr.event_num)
            if cf.attacks_type[self.skills['attack_1'][0]] == 'melee':
                self.state = 'attack_1'
                vr.events[str(vr.event_num)] = ClassMelee.melee(self.name, self.skills['attack_1'][0], self.skills['attack_1'][1], self.coord, [0,0], self.skills['attack_1'][3], self.skills['attack_1'][4][self.attack_orient], self.skills['attack_1'][5], vr.event_num, self.orient)
                vr.event_num += 1
                print("New Melee attack :", vr.event_num)

        return

    def update(self):

        # -- Events interaction -- #
        already_take = []
        for detector in self.detectors:
            if detector.data['colliding'] == 'projectile' or detector.data['colliding'] == 'melee':
                if str(detector.data['num']) in vr.events.keys() and not(str(detector.data['num']) in already_take):
                    self.skills['health'][0] += -detector.data['damage']
                    del vr.events[str(detector.data['num'])]
                    already_take.append(str(detector.data['num']))
                if self.skills['health'][0] <= 0:
                    self.state = 'dead'
                    return

        # -- reloading -- #
        if self.current_attack_1 > 0:
            self.current_attack_1 += self.last_time - vr.time
        if self.attack_time > 0:
            self.attack_time = self.attack_time - (vr.time - self.last_time)

        self.last_time = vr.time

        # -- Gravity -- #
        if self.detectors[1].state is False and self.speed[1] < cf.max_vspeed:
            self.speed[1] += cf.g
        elif self.detectors[1].state is True:
            self.speed[1] = 0
            if self.detectors[5].state is True:
                self.speed[1] = -2

        if -self.skills['acceleration'] < self.speed[0] < self.skills['acceleration'] and self.speed[0] != 0:
            self.speed[0] = 0
        elif self.speed[0] < 0 and vr.inputs[self.inputs['left']] is False:
            self.speed[0] += self.skills['acceleration']
        elif self.speed[0] > 0 and vr.inputs[self.inputs['right']] is False:
            self.speed[0] += -self.skills['acceleration']

        # -- Inputs -- #
        if self.detectors[1].state is True:
            self.current_walljumps, self.current_doublejumps = 0, 0


        # a faire -> V horizontale aérienne / terrestre
        if self.attack_time <= 0:
            if vr.inputs[self.inputs['up']] and vr.inputs[self.inputs['right']] and self.detectors[0].state is True and self.current_walljumps < self.skills['walljump'][2]:
                self.speed = [-self.skills['walljump'][0], -self.skills['walljump'][1]]
                self.current_walljumps += 1
            elif vr.inputs[self.inputs['up']] and vr.inputs[self.inputs['left']] and self.detectors[2].state is True and self.current_walljumps < self.skills['walljump'][2]:
                self.speed = [self.skills['walljump'][0], -self.skills['walljump'][1]]
                self.current_walljumps += 1

            elif vr.inputs[self.inputs['right']] and self.speed[0] < self.skills['maxspeed']:
                self.speed[0] += self.skills['acceleration']
            elif vr.inputs[self.inputs['left']] and self.speed[0] > -self.skills['maxspeed']:
                self.speed[0] += -self.skills['acceleration']

            elif vr.inputs[self.inputs['up']] and (self.detectors[1].state is True or (self.current_doublejumps < self.skills['doublejump'] and 0 < self.speed[1] < self.skills['maxspeed'])):
                self.speed[1] = -self.skills['jump']
                if self.detectors[1].state is False:
                    self.current_doublejumps += 1

            if (vr.inputs[self.inputs['down']]) and self.detectors[1].state is False:
                self.speed[1] = self.skills['jump']//1.5
                self.orient[0] = 0
                self.orient[1] = 1

        # -- verification -- #
        if self.detectors[0].state is True and self.speed[0] > 0:
            self.speed[0] = 0
            if self.detectors[4].state is True:
                self.speed[0] = -3
        if self.detectors[2].state is True and self.speed[0] < 0:
            self.speed[0] = 0
            if self.detectors[6].state is True:
                self.speed[0] = 3
        if self.detectors[3].state is True and self.speed[1] < 0:
            self.speed[1] = 0
            if self.detectors[7].state is True:
                self.speed[1] = 3

        # -- animations -- #
        if self.detectors[1].state is False and self.attack_time <= 0:
            self.state = 'jump'
        elif self.speed[0] != 0 and self.attack_time <= 0:
            self.state = 'walk'
        elif self.attack_time <= 0:
            self.state = 'stand'

        self.updatepos()
        self.updateDetectors()

        if vr.inputs[self.inputs['attack_1']] and self.attack_time <= 0:
            self.attack_orient = 'side'
            if abs(self.speed[0]) >= abs(self.speed[1]):
                self.attack_orient = 'side'
            elif self.speed[1] > 0:
                self.attack_orient = 'down'
            elif self.speed[1] < 0:
                self.attack_orient = 'up'
            self.attack()

        self.updatevisual()

        self.last_time = vr.time
