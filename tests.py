from main import *
from funcs.computation import findPriority
from classes.task import Task
from classes.subtask import Subtask

def testFindPriority():
    print("\t---Testing Find Priority---")
    print("Creating Task 1: Due 2023-12-12")
    task1 = Task("Task1", dueDate="2023-12-12", taskID=1, workload=5)
    print("Creating Task 2: Due 2023-12-11")
    task2 = Task("Task2", dueDate="2023-12-11", taskID=2, workload=5)
    tasklist = [task1, task2]
    print("Prioritizing. Expected order: Task2, Task1. Result:")
    prioritizedList = findPriority(tasklist)
    for task in prioritizedList:
        print(task.name)
    print("")
    print("Attempting prioritization using non-Task type object. Expected result: 1 (error). Result:")
    tasklist.append("Not a task!")
    print(findPriority(tasklist))
    print("")
    print("Attempting prioritization using empty list. Expected result: []. Result:")
    print(findPriority([]))

testFindPriority()