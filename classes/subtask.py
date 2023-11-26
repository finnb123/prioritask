class Subtask:
    def __init__(self, id, name:str, completed=False):
        self._id = id
        self._name = name
        self._completed = completed
    
    # Getters
    @property
    def id(self): return self._id
    @property
    def name(self): return self._name
    @property
    def completed(self): return self._completed

    # Setters
    @id.setter
    def name(self, newName): self._name = newName

    def markComplete(self):
        self._completed = True