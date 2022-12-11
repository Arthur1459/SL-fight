class NewEvent:
    def __init__(self, object, killableby):
        self.object = object
        self.killable_by = killableby  # List of instance which stop the event when touch

    def update(self):
        self.object.update()
        return

    def get(self):
        return self.object.get()
