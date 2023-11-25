import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
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
    
    addTaskView = tk.Frame(root)
    addTaskView.pack(fill="both", expand=True)

    testLabel = tk.Label(addTaskView, text="Create a Task", font=('roboto', 12, 'bold'), foreground='#121212')
    testLabel.pack()

    nameField = tk.Entry(addTaskView)
    nameField.pack()
    descriptionField = tk.Entry(addTaskView)
    descriptionField.pack()
    workloadInt = tk.Scale(addTaskView, from_=0, to=200, orient='horizontal')
    workloadInt.pack()

    savePicOriginal = Image.open('img/tickB.png')
    desired_size = (50, 50)
    resizedSave = savePicOriginal.resize(desired_size, Image.ANTIALIAS)
    saveButtonPic = ImageTk.PhotoImage(resizedSave)
    saveButton = tk.Button(root, image=saveButtonPic, command=lambda: saveTask(nameField.get(), descriptionField.get(), workloadInt.get()), bd=0, bg="#121212", activebackground="#121212")
    saveButton.image = saveButtonPic
    saveButton.pack()


    exitPicOriginal = Image.open('img/backArrowB.png')
    desired_size = (50, 50)
    resizedexit = exitPicOriginal.resize(desired_size, Image.ANTIALIAS)
    exitButtonPic = ImageTk.PhotoImage(resizedexit)
    exitButton = tk.Button(root, image=exitButtonPic, command=refresh, bd=0, bg="#121212", activebackground="#121212")
    exitButton.image = exitButtonPic
    exitButton.pack()

def saveTask(name, description, workload):
    global tasks
    print("Saving task")
    print(name)
    if len(tasks) > 0:
        newID = tasks[-1].taskID + 1
    else:
        newID = 1
    newTask = Task(name=name, taskID=newID, description=description, workload=workload)
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
        taskNameLabel = tk.Label(root, text=task.name, font=('roboto', 12, 'bold'), foreground='#121212')
        taskNameLabel.pack()
    print(len(tasks))

    plusPicOriginal = Image.open('img/plusB.png')

    desired_size = (50, 50)
    resized_image = plusPicOriginal.resize(desired_size, Image.ANTIALIAS)

    plusButtonPic = ImageTk.PhotoImage(resized_image)

    plusButton = tk.Button(root, image=plusButtonPic, command=showAddTaskView, bd=0, bg="#121212", activebackground="#121212")
    plusButton.image = plusButtonPic
    plusButton.pack()

root = tk.Tk()
root.title("PrioriTask")
root.configure(bg="#121212")
root.geometry("1280x720")

tasks = []
loadMain()

root.mainloop()
