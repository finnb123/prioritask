def findPriority(tasks:list):
    prioritizedList = []

    for task in list:
        workLoad = task.workload
        workLeft = None #work left to be added
        dueDate = None #due date to be added

        currentWorkLoad = workLoad * workLeft

        task.priority = currentWorkLoad - dueDate
        prioritizedList.append(task)

    prioritizedList.sort(key = lambda x: x.priority, reverse = True)



#Uses date due, workload, work left
# Workload x Workleft = Current Workload
# CurrentWorkload - Days left = PriorityPoints
# More Priority points = higher on list
#   [5,1,-2,-17] 
