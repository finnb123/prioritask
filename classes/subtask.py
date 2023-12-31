class Subtask:
    def __init__(self, id, name:str, parent, completed=False):
        self._id = id
        self._name = name
        self._completed = completed
        self._parent = parent
    
    # Getters
    @property
    def id(self): return self._id
    @property
    def name(self): return self._name
    @property
    def completed(self): return self._completed
    @property
    def parent(self): return self._parent

    # Setters
    @name.setter
    def name(self, newName): self._name = newName
    @id.setter
    def id(self, newID): self._id = newID
    @parent.setter
    def parent(self, newParent): self._parent = newParent

    def markComplete(self):
        self._completed = True