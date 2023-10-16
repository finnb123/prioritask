from subtask import Subtask;

class Task:
    def __init__(self, id, name, description="", workload=0, priority=0, subtasks = []):
        self.id = id
        self.name = name
        self.description = description
        self.workload = workload
        self.priority = priority
        self.subtasks = subtasks

    # Getters
    @property
    def id(self): return self.id
    @property
    def name(self): return self.name
    @property
    def description(self): return self.description
    @property
    def workload(self): return self.workload
    @property
    def priority(self): return self.priority
    @property
    def subtasks(self): return self.subtasks

    # Setters
    @name.setter
    def name(self, newName): self.name = newName
    @description.setter
    def description(self, newDesc): self.description = newDesc
    @priority.setter
    def priority(self, newPrio): self.priority = newPrio

    def addSubtask(self, newSub:Subtask):
        self.subtasks.append(newSub)
