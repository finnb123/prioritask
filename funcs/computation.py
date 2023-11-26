import datetime
from classes.task import Task

def findPriority(tasks:list[Task]):
    prioritizedList = []

    for task in tasks:
        workLoad = task.workload
        workLeft = 1 
        if len(task.subtasks)>=1:
            subTasksCompleted = 0
            subTasksRemaining = 0
            for subtask in task.subtasks:
                if subtask.completed:
                    subTasksCompleted+=1
                else: subTasksRemaining+=1
            workLeft = subTasksRemaining/subTasksCompleted
            

        dueDateString = task.dueDate #due date to be added
        dueDateElements = dueDateString.split("-")
        dueDate = datetime.date(int(dueDateElements[0]), int(dueDateElements[1]), int(dueDateElements[2]))
        today = datetime.date.today()
        daysLeft = (dueDate-today).days

        currentWorkLoad = workLoad * workLeft
        task.priority = daysLeft - currentWorkLoad
        prioritizedList.append(task)

    prioritizedList.sort(key = lambda x: x.priority, reverse = False)
    return prioritizedList



#Uses date due, workload, work left
# Workload x Workleft = Current Workload
# CurrentWorkload - Days left = PriorityPoints
# More Priority points = higher on list
#   [5,1,-2,-17] 
