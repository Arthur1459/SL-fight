class NewEvent:
    def __init__(self, object, killableby):
        self.object = object
        self.killable_by = killableby  # List of instance which stop the event when touch
        self.state = 'alive'

    def update(self):
        self.object.update()
        try:
            collide = []
            for detector in self.object.detectors:
                collide.append(detector.data['name'])
            for colliding in collide:
                if colliding in self.killable_by:
                    self.state = 'dead'
                    return
        except:
            pass
        return

    def get(self):
        return self.object.get()
