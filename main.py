import tkinter as tk
from tkinter import *
from tkinter import simpledialog
from classes.task import Task
import pickle
import os


def clearScreen():
    for widget in root.winfo_children():
        widget.destroy()

def refresh():
    clearScreen()
    loadMain()

def showAddTaskView():
    clearScreen()
    print("showing addtaskview")
    addTaskView = Frame(root, bg="black")
    testLabel = Label(addTaskView, text="Create a Task")
    testLabel.pack()

    nameField = Entry(addTaskView)
    nameField.pack()
    descriptionField = Entry(addTaskView)
    descriptionField.pack()
    workloadInt = Scale(addTaskView, from_=0, to=200, orient='horizontal')
    workloadInt.pack()

    commitButton = Button(addTaskView, text="Save Task", 
        command=lambda: saveTask(nameField.get(), descriptionField.get(), workloadInt.get()))
    commitButton.pack()

    taskViewExit = Button(addTaskView, text="exit", command=refresh).pack()
    addTaskView.pack(fill="both", expand=True)


def saveTask(name, description, workload):
    global tasks
    print("Saving task")
    print(name)
    if len(tasks)>0:
        newID = tasks[-1].taskID+1
    else:
        newID = 1
    newTask = Task(name = name, taskID=newID, description=description, workload=workload)
    tasks.append(newTask)
    print(len(tasks))
    with open("tasks.file", "wb") as taskFile:
        pickle.dump(tasks, taskFile)

def loadMain():
    global tasks
    if os.path.exists("tasks.file"):
        with open("tasks.file", "rb") as taskFile:
            tasks = pickle.load(taskFile)
    else:
        tasks = []
    for task in tasks:
        taskNameLabel = Label(root, text=task.name)
        taskNameLabel.pack()
    print(len(tasks))
    testLabel = Label(root, text=str(tasks)).pack()
    plusButton = tk.Button(root, text="+", command=showAddTaskView).pack()



### --- SETUP --- ###
root = tk.Tk()
root.title("PrioriTask")
root.configure(bg="light cyan")
root.geometry("1280x720")
tasks=[]
loadMain()



### --- MAIN WINDOW --- ###




### --- ADD TASK VIEW --- ###



### --- MAIN --- ###
root.mainloop()