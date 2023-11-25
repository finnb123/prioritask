import datetime
from classes.task import Task

def findPriority(tasks:list[Task]):
    prioritizedList = []

    for task in tasks:
        workLoad = task.workload
        workLeft = 1 #work left to be added
        dueDateString = task.dueDate #due date to be added
        dueDateElements = dueDateString.split("-")
        dueDate = datetime.date(int(dueDateElements[0]), int(dueDateElements[1]), int(dueDateElements[2]))
        today = datetime.date.today()
        daysLeft = (dueDate-today).days

        currentWorkLoad = workLoad * workLeft
        task.priority = currentWorkLoad - daysLeft
        prioritizedList.append(task)

    prioritizedList.sort(key = lambda x: x.priority, reverse = True)
    return prioritizedList



#Uses date due, workload, work left
# Workload x Workleft = Current Workload
# CurrentWorkload - Days left = PriorityPoints
# More Priority points = higher on list
#   [5,1,-2,-17] 
