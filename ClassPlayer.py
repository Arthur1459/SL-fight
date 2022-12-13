import ClassProjectiles
import ressources as rs
import config as cf
import vars as vr
import ClassDetectors
import ClassSolid
import pygame.transform
import ClassMelee
import ClassEvent as Event


class Player:
    # --- Init --- #
    def __init__(self, name, player_n, coord):
        self.instance = 'player'
        self.name = name
        self.player_n = player_n
        self.coord = [coord[0], coord[1]]
        self.speed, self.orient, self.attack_orient, self.last_orient = [0, 0], [1.0, 0.0], 'side', 0
        self.state = 'stand'
        self.last_time = vr.time
        self.start_phase, self.len_phase, self.current_phase, self.attack_time = vr.time, 0, 0, 0
        self.visual = (rs.hero_visuals[self.name])[self.state][0]
        self.size = self.visual.get_size()
        self.hitbox = [[self.coord[0] - self.getwidth_hitbox() // 2, self.coord[0] - self.getheight_hitbox() // 2], [self.coord[0] + self.getwidth_hitbox() // 2, self.coord[0] + self.getheight_hitbox() // 2]]
        self.inputs = cf.players_inputs[player_n]
        self.detectors, self.already_taken = self.initDetectors(), []
        self.skills, self.mass = cf.heroes_skills[self.name], cf.heroes_skills[self.name]['mass']
        self.current_walljumps, self.current_doublejumps, self.current_attack_base, self.jump_time, self.up_remember = 0, 0, 0, 0, False
        self.num, self.last_time = vr.solid_num, vr.time
        vr.solids[self.num] = ClassSolid.Block(self.hitbox[0], self.hitbox[1], self.name, self.num)
        vr.solid_num += 1
        return

    def getx(self):  # return the coord visualised
        return self.coord[0] - self.getwidth_hitbox() // 2

    def gety(self):
        return self.coord[1] - self.getheight_hitbox() // 2

    def getwidth_hitbox(self):
        return self.size[0]

    def getheight_hitbox(self):
        return self.size[1]

    def getsize_visual(self):
        return self.visual.get_size()

    def getcoord_visual(self):
        size = self.getsize_visual()
        x = self.getx() - (size[0] - self.getwidth_hitbox())/2
        y = self.gety() - (size[1] - self.getheight_hitbox())/2
        return [x, y]

    def getHealth(self):
        return self.skills['health']

    def getCoordHealthBar(self):
        return [[self.getx(), self.gety() - 10], [self.getx(), self.gety() - 10]]

    def initDetectors(self):
        detectors = [ClassDetectors.detector([self.getwidth_hitbox() // 2, 0], self.name, cf.size_player),
                     ClassDetectors.detector([0, self.getheight_hitbox() // 2], self.name, cf.size_player),
                     ClassDetectors.detector([-self.getwidth_hitbox() // 2, 0], self.name, cf.size_player),
                     ClassDetectors.detector([0, -self.getheight_hitbox() // 2], self.name, cf.size_player),
                     ClassDetectors.detector([self.getwidth_hitbox() // 2.3, 0], self.name, cf.size_player),
                     ClassDetectors.detector([0, self.getheight_hitbox() // 2.3], self.name, cf.size_player),
                     ClassDetectors.detector([-self.getwidth_hitbox() // 2.3, 0], self.name, cf.size_player),
                     ClassDetectors.detector([0, -self.getheight_hitbox() // 2.3], self.name, cf.size_player)]
        return detectors

    def get_state(self):
        states = []
        if vr.inputs[self.inputs['attack_1']] and self.current_attack_base <= 0:
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
        if self.detectors[1].state is True: # c koi ça mael ???? wtf
            states.append('right')
        if self.detectors[1].state is False and self.attack_time <= 0:
            states.append('jump')
        elif self.speed[0] != 0 and self.attack_time <= 0:
            states.append('walk')
        elif self.attack_time <= 0:
            states.append('stand')
        return  # mdrrr en plus tu return rien Trololol

    def updateDetectors(self):
        for detector in self.detectors:
            detector.update(self.coord)
        return True

    def updatevisual(self):
        try:
            if self.state == 'attack_1':  # if visuals depends on the up/down orientation
                self.len_phase = len((rs.hero_visuals[self.name])[self.state][self.attack_orient])
                if self.current_phase >= self.len_phase:
                    self.current_phase = 0
                elif vr.time - self.start_phase > 200:
                    self.current_phase += 1
                    self.start_phase = vr.time

                if self.orient[0] >= 0:
                    self.visual = (rs.hero_visuals[self.name])[self.state][self.attack_orient][self.current_phase]

                else:
                    self.visual = pygame.transform.flip((rs.hero_visuals[self.name])[self.state][self.attack_orient][self.current_phase], True, False)

            elif self.state == 'walk' and self.attack_time <= 0:  # if the visuals depends only of the right/left orientation
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

            elif self.attack_time <= 0:  # if visuals don't depend on the orientation
                if self.orient[0] >= 0:
                    self.visual = (rs.hero_visuals[self.name])[self.state][0]
                else:
                    self.visual = pygame.transform.flip((rs.hero_visuals[self.name])[self.state][0], True, False)

        except:
            print("ERROR : Missing hero visual")

    def updatepos(self):
        if self.attack_time <= 0:
            # --- orientation --- #
            self.orient[1] = 0.0
            self.orient[0] = self.last_orient
            if vr.inputs[self.inputs['right']]:
                self.orient[0] = 1.0
                self.last_orient = 1.0
                self.orient[1] = 0.0
            elif vr.inputs[self.inputs['left']]:
                self.orient[0] = -1.0
                self.last_orient = -1.0
                self.orient[1] = 0.0
            if vr.inputs[self.inputs['up']]:
                self.orient[1] = -1.0
                if not (vr.inputs[self.inputs['right']] or vr.inputs[self.inputs['left']]):
                    self.orient[0] = 0.0
                    self.last_orient = 0.0
            elif vr.inputs[self.inputs['down']] and self.isInTheAir():
                self.orient[1] = 1.0
                if not (vr.inputs[self.inputs['right']] or vr.inputs[self.inputs['left']]):
                    self.orient[0] = 0.0
                    self.last_orient = 0.0
            elif vr.inputs[self.inputs['down']]:
                self.orient[1] = 0.5
        elif self.orient[0] == 0.0 and not self.isInTheAir():
            self.orient[0] = 1.0

        # --- new coord / hitbox --- #
        self.coord[0], self.coord[1] = self.coord[0] + self.speed[0], self.coord[1] + self.speed[1]
        self.hitbox = [[self.coord[0] - self.getwidth_hitbox() // 2, self.coord[1] - self.getheight_hitbox() // 2], [self.coord[0] + self.getwidth_hitbox() // 2, self.coord[1] + self.getheight_hitbox() // 2]]

        # --- verification --- #
        if not(0 < self.getx() < cf.screenx) or not(0 < self.gety() < cf.screeny):  # out of screen
            print("\nERROR Coordinate of", self.name, "unexpected.\n")
            self.coord = [200, 200]

        # --- update solid hitbox --- #
        vr.solids[self.num] = ClassSolid.Block(self.hitbox[0], self.hitbox[1], self.name, self.num)
        return

    def attack(self, attack, type_attack):
        self.current_phase = -1
        if type_attack == 'base':
            if self.current_attack_base <= 0:
                self.current_attack_base = self.skills[attack]['reload'] * 1000  # reloading time
                self.state = attack
                if cf.attacks_type[self.skills[attack]['name']] == 'projectile':
                    object_tmp = ClassProjectiles.projectile(self.name, self.skills[attack]['name'], self.skills[attack]['damage'], self.coord, [self.skills[attack]['speed'] * self.orient[0], self.skills[attack]['speed'] * self.orient[1]], self.skills[attack]['rng'], self.skills[attack]['duration'], self.skills[attack]['size'], self.skills[attack]['special'], vr.event_num)
                    vr.events[str(vr.event_num)] = Event.NewEvent(object_tmp, self.skills[attack]['killable'])
                    vr.event_num += 1
                    print("New Projectile attack :", vr.event_num)
                elif cf.attacks_type[self.skills[attack]['name']] == 'melee':
                    self.attack_time = self.skills[attack]['duration']*1000  # time of the attack
                    object_tmp = ClassMelee.melee(self.name, self.skills[attack]['name'], self.skills[attack]['damage'] + self.getAttackModifier(attack), self.coord, [0, 0], self.skills[attack]['duration'], self.skills[attack]['size'][self.attack_orient], self.skills[attack]['special'], vr.event_num, self.orient)
                    vr.events[str(vr.event_num)] = Event.NewEvent(object_tmp, self.skills[attack]['killable'])
                    vr.event_num += 1
                    print("New Melee attack :", vr.event_num)
        elif type_attack == 'special':
            print("ERROR SPECIAL ATTACK NOT IMPLEMENTED YET.")
        return

    def setAttackOrient(self):
        self.attack_orient = 'side'
        if vr.inputs[self.inputs['down']] and self.isInTheAir():
            self.attack_orient = 'down'
        elif vr.inputs[self.inputs['up']]:
            self.attack_orient = 'up'
        return

    def getAttackModifier(self, attack):
        if self.attack_orient == 'down':
            return self.skills[attack]['damage']
        else:
            return 0

    # ------ UPDATE ----- #
    def update(self):
        # -- Events interaction -- #
        for detector in self.detectors:
            if detector.data['colliding'] == 'projectile' or detector.data['colliding'] == 'melee':  # Detectors have already checked who was the sender
                if str(detector.data['num']) in vr.events.keys() and not(str(detector.data['num']) in self.already_taken):
                    self.skills['health'][0] += -detector.data['damage']
                    print(self.name, "hit by", str(detector.data['instance']), " Life : ", self.skills['health'][0], "/", self.skills['health'][1])
                    if self.instance in vr.events[str(detector.data['num'])].killable_by:
                        del vr.events[str(detector.data['num'])]
                    self.already_taken.append(str(detector.data['num']))
                    if len(self.already_taken) > 1000:  # not essential (opti ?)
                        self.already_taken = [self.already_taken[i] for i in range(len(self.already_taken) - 20, len(self.already_taken) - 1)]
                if self.skills['health'][0] <= 0:
                    self.state = 'dead'
                    return

        # -- reloading -- #
        if self.current_attack_base > 0:
            self.current_attack_base += self.last_time - vr.time
        if self.attack_time > 0:
            self.attack_time = self.attack_time - (vr.time - self.last_time)

        # -- Gravity -- #
        if self.detectors[1].blocked is False and self.speed[1] < cf.max_vspeed:
            self.speed[1] += cf.g*self.mass
        elif self.detectors[1].blocked is True and self.speed[1] > 0:
            self.speed[1] = 0
            if self.detectors[5].blocked is True:
                self.speed[1] = -2

        if -self.skills['acceleration']//2 <= self.speed[0] <= self.skills['acceleration']//2 and self.speed[0] != 0:
            self.speed[0] = 0
        if self.speed[0] < 0 and vr.inputs[self.inputs['left']] is False:
            self.speed[0] += self.skills['acceleration']//2
        if self.speed[0] > 0 and vr.inputs[self.inputs['right']] is False:
            self.speed[0] += -self.skills['acceleration']//2

        # -- Inputs -- #
        if self.detectors[1].blocked is True:
            self.current_walljumps, self.current_doublejumps = 0, 0

        # a faire -> V  air / ground
        if self.attack_time <= 0 or self.detectors[1].blocked is False:   # if he is not attacking or in the air

            # Wall jumps
            if vr.inputs[self.inputs['up']] and vr.inputs[self.inputs['right']] and self.detectors[0].blocked is True and self.current_walljumps < self.skills['walljump'][2]:
                self.speed = [-self.skills['walljump'][0], -self.skills['walljump'][1]]
                self.current_walljumps += 1
            if vr.inputs[self.inputs['up']] and vr.inputs[self.inputs['left']] and self.detectors[2].blocked is True and self.current_walljumps < self.skills['walljump'][2]:
                self.speed = [self.skills['walljump'][0], -self.skills['walljump'][1]]
                self.current_walljumps += 1

            # Side
            if vr.inputs[self.inputs['right']] and not self.detectors[0].blocked:   # go right
                if self.isInTheAir():
                    if self.speed[0] <= self.skills['maxspeed'][1]:
                        self.speed[0] += self.skills['acceleration']
                    if self.speed[0] > self.skills['maxspeed'][1]:
                        self.speed[0] += int(-(cf.air_resistance/self.mass + 1))

                else:
                    if self.speed[0] < self.skills['maxspeed'][0]:
                        self.speed[0] += self.skills['acceleration']
            if vr.inputs[self.inputs['left']] and not self.detectors[2].blocked:  # go left
                if self.isInTheAir():
                    if self.speed[0] >= -self.skills['maxspeed'][1]:
                        self.speed[0] += -self.skills['acceleration']
                    if self.speed[0] < -self.skills['maxspeed'][1]:
                        self.speed[0] += int(cf.air_resistance/self.mass + 1)
                else:
                    if self.speed[0] > -self.skills['maxspeed'][0]:
                        self.speed[0] += -self.skills['acceleration']

            # Jumps
            if (vr.inputs[self.inputs['up']] and not self.up_remember) and (self.detectors[1].blocked is True or (self.current_doublejumps < self.skills['doublejump'] and vr.time - self.jump_time > (cf.jump_duration * 1000))):
                self.speed[1] = -self.skills['jump']
                self.jump_time = vr.time
                if self.detectors[1].blocked is False:
                    self.current_doublejumps += 1

            # Down
            elif (vr.inputs[self.inputs['down']]) and (self.detectors[1].blocked is False) and (self.speed[1] >= -self.skills['maxspeed'][1]//2):
                if self.speed[1] < self.skills['jump']*self.skills['down_smash']:
                    self.speed[1] += self.skills['jump']*self.skills['down_smash']  # Modifier speed vertical when down
                    if self.speed[1] > cf.max_vspeed:
                        self.speed[1] = cf.max_vspeed
            elif vr.inputs[self.inputs['down']] and self.detectors[1].blocked:
                self.speed[1] = 0

            self.up_remember = vr.inputs[self.inputs['up']]

        # -- verification -- #
        if self.detectors[0].blocked is True:
            if self.speed[0] > 0:
                self.speed[0] = 0
            if self.detectors[4].blocked is True:
                self.coord[0] += -2
        if self.detectors[2].blocked is True:
            if self.speed[0] < 0:
                self.speed[0] = 0
            if self.detectors[6].blocked is True:
                self.coord[0] += 2
        if self.detectors[3].blocked is True:
            if self.speed[1] < 0:
                self.speed[1] = 0
            if self.detectors[7].blocked is True:
                self.coord[1] += 2
        if self.detectors[1].blocked is True:
            if self.speed[1] > 0:
                self.speed[1] = 0
            if self.detectors[5].blocked is True:
                self.coord[1] += -4

        # -- animations -- #
        if self.detectors[1].blocked is False and self.attack_time <= 0:
            self.state = 'jump'
        elif self.speed[0] != 0 and self.attack_time <= 0:
            self.state = 'walk'
        elif self.attack_time <= 0:
            self.state = 'stand'

        self.updatepos()
        self.updateDetectors()

        if vr.inputs[self.inputs['attack_1']] and self.attack_time <= 0:
            self.setAttackOrient()
            self.attack('attack_1', 'base')

        self.updatevisual()

        self.last_time = vr.time

    def get(self):
        return self

    def isInTheAir(self):
        if self.detectors[1].blocked is True:
            return False
        else:
            return True
