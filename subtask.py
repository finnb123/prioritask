class Subtask:
    def __init__(self, id, name:str, completed=False):
        self.id = id
        self.name = name
        self.completed = completed
    
    # Getters
    @property
    def id(self): return self.id
    @property
    def name(self): return self.name
    @property
    def completed(self): return self.completed

    # Setters
    @id.setter
    def name(self, newName): self.name = newName

    def markComplete(self):
        self.completed = True