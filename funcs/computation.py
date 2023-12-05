import datetime
from classes.task import Task

def findPriority(tasks:list[Task]):
    '''Sorts and returns a list of Task objects in order of calculated priority'''
    prioritizedList = []

    for task in tasks:
        if type(task) != Task: return 1
        workLoad = task.workload
        workLeft = 1 
        # Find percentage of subtasks complete if applicable
        if len(task.subtasks)>=1:
            subTasksCompleted = 0
            subTasksRemaining = 0
            for subtask in task.subtasks:
                if subtask.completed:
                    subTasksCompleted+=1
                else: subTasksRemaining+=1
            workLeft = subTasksRemaining/len(task.subtasks)
        # Find days left before due
        dueDateString = task.dueDate 
        dueDateElements = dueDateString.split("-")
        dueDate = datetime.date(int(dueDateElements[0]), int(dueDateElements[1]), int(dueDateElements[2]))
        today = datetime.date.today()
        daysLeft = (dueDate-today).days
        # Prioritize and append to list
        currentWorkLoad = workLoad * workLeft
        task.priority = daysLeft - currentWorkLoad
        prioritizedList.append(task)
    # Sort list based on priority value and return
    prioritizedList.sort(key = lambda x: x.priority, reverse = False)
    return prioritizedList
