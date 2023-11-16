import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from task import Task
import pickle
import os

def showAddTaskView():
    print("showing addtaskview")
    addTaskView.pack(fill="both", expand=True)

def hideAddTaskView():
    print("hiding addtaskview")
    addTaskView.pack_forget()
    loadMain()

def plusPress():
    print("+ Button Pressed")
    showAddTaskView()

def commitText():
    print(nameField.get("1.0",'end-1c'))
    if len(tasks)>0:
        newID = tasks[-1].id()+1
    else:
        newID = 1
    newTask = Task(name = nameField.get("1.0",'end-1c'), taskID=newID, description=descriptionField.get("1.0",'end-1c'), workload=workloadInt.get())
    tasks.append(newTask)
    with open("tasks.file", "wb") as taskFile:
        pickle.dump(tasks, taskFile)
    taskFile.close()

def refresh():
    root.delete(all)

def loadMain():
    if os.path.exists("tasks.file"):
        with open("tasks.file", "rb") as taskFile:
            tasks = pickle.load(taskFile)
    else:
        tasks = []
    plusButton = tk.Button(root, text="+", command=plusPress).pack()
    for task in tasks:
        taskNameLabel = tk.Label(root, text=task.name)
        taskNameLabel.pack()
### --- SETUP --- ###
root = tk.Tk()
root.title("PrioriTask")
root.geometry("1280x720")
tasks = []
loadMain()



### --- MAIN WINDOW --- ###




### --- ADD TASK VIEW --- ###
addTaskView = tk.Frame(root, bg="black")
testLabel = tk.Label(addTaskView, text="Create a Task")
testLabel.pack()

nameField = tk.Text(addTaskView, height=2, width=50)
nameField.pack()
descriptionField = tk.Text(addTaskView, height=3, width=50)
descriptionField.pack()
workloadInt = tk.Scale(addTaskView, from_=0, to=200, orient='horizontal')
workloadInt.pack()

commitButton = tk.Button(addTaskView, text="commit", command=commitText)
commitButton.pack()
taskViewExit = tk.Button(addTaskView, text="exit", command=hideAddTaskView).pack()


### --- MAIN --- ###
root.mainloop()