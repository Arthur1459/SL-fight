# Bah wtf y a pas d' import...

class Block:
    def __init__(self, pt1, pt2, name, num):
        self.instance = 'solid'
        self.name = name
        self.num = num
        self.topleft = [pt1[0], pt1[1]]
        self.downright = [pt2[0], pt2[1]]
        self.hitbox = [self.topleft, self.downright]

        return

    def resetPos(self, pt1, pt2):
        self.topleft = [pt1[0], pt1[1]]
        self.downright = [pt2[0], pt2[1]]
        self.hitbox = [self.topleft, self.downright]
