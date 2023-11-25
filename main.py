import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import pickle
import os
from classes.task import Task
import datetime
from funcs.computation import findPriority

def clearScreen():
    for widget in root.winfo_children():
        widget.destroy()

def refresh():
    clearScreen()
    loadMain()

def showAddTaskView():
    clearScreen()
    print("showing addtaskview")
    
    addTaskLabel = tk.Label(root, text="Create a Task", font=('roboto', 24, 'normal'), foreground='#03DAC6', borderwidth=0, background="#121212")
    addTaskLabel.place(anchor="n", relx=0.5, rely=0.05)

    titleLabel = tk.Label(root, text="Title", font=('roboto', 12, 'normal'), foreground='#03DAC6', borderwidth=0, background="#121212")
    titleLabel.place(anchor="s", relx=0.5, rely=0.2)
    nameField = tk.Entry(root, borderwidth=0, background="#4c4c4c", foreground="#FFFFFF", font=('roboto', 16, 'normal'))
    nameField.place(anchor="n", relx=0.5, rely=0.2)
    descriptionLabel = tk.Label(root, text="Description (Optional)", font=('roboto', 12, 'normal'), foreground='#03DAC6', borderwidth=0, background="#121212")
    descriptionLabel.place(anchor="s", relx=0.5, rely=0.3)
    descriptionField = tk.Entry(root, borderwidth=0, background="#4c4c4c", foreground="#FFFFFF", font=('roboto', 16, 'normal'))
    descriptionField.place(anchor="n", relx=0.5, rely=0.3)
    dateLabel = tk.Label(root, text="Due Date (YYYY-MM-DD)", font=('roboto', 12, 'normal'), foreground='#03DAC6', borderwidth=0, background="#121212")
    dateLabel.place(anchor="s", relx=0.5, rely=0.4)
    dateField = tk.Entry(root, borderwidth=0, background="#4c4c4c", foreground="#FFFFFF", font=('roboto', 16, 'normal'))
    dateField.place(anchor="n", relx=0.5, rely=0.4)
    currentDate = datetime.date.today()
    dateField.insert(-1, currentDate)

    effortLabel = tk.Label(root, text="How big does this task feel?", font=('roboto', 12, 'normal'), foreground='#03DAC6', borderwidth=0, background="#121212")
    effortLabel.place(anchor="s", relx=0.5, rely=0.5)
    sliderStyle = ttk.Style()
    sliderStyle.configure('TScale', background='#121212', slidercolor="#03DAC6")
    workloadInt = ttk.Scale(root, from_=0, to=10, orient='horizontal', style='TScale')
    workloadInt.place(anchor="n", relx=0.5, rely=0.5, relwidth=0.25)

    savePicOriginal = Image.open('img/tickB.png')
    desired_size = (50, 50)
    resizedSave = savePicOriginal.resize(desired_size, Image.Resampling.LANCZOS)
    saveButtonPic = ImageTk.PhotoImage(resizedSave)
    saveButton = tk.Button(root, image=saveButtonPic, command=lambda: 
                           saveTask(nameField.get(), descriptionField.get(), workloadInt.get(), dateField.get()), 
                           bd=0, bg="#121212", activebackground="#121212")
    saveButton.image = saveButtonPic
    saveButton.place(anchor="n", relx=0.75, rely=0.75)


    exitPicOriginal = Image.open('img/backArrowB.png')
    desired_size = (50, 50)
    resizedexit = exitPicOriginal.resize(desired_size, Image.Resampling.LANCZOS)
    exitButtonPic = ImageTk.PhotoImage(resizedexit)
    exitButton = tk.Button(root, image=exitButtonPic, command=refresh, bd=0, bg="#121212", activebackground="#121212")
    exitButton.image = exitButtonPic
    exitButton.place(anchor="n", relx=0.25, rely=0.75)

def saveTask(name, description, workload, dueDate):
    global tasks
    print("Saving task")
    print(name)
    if len(tasks) > 0:
        newID = tasks[-1].taskID + 1
    else:
        newID = 1
    newTask = Task(name=name, taskID=newID, description=description, workload=workload, dueDate=dueDate)
    tasks.append(newTask)
    print(len(tasks))
    with open("tasks.file", "wb") as taskFile:
        pickle.dump(tasks, taskFile)
    refresh()

def loadMain():
    global tasks
    if os.path.exists("tasks.file"):
        with open("tasks.file", "rb") as taskFile:
            tasks = pickle.load(taskFile)
    else:
        tasks = []
    tasks = findPriority(tasks)
    for task in tasks:
        taskNameLabel = tk.Label(root, text=task.name, font=('roboto', 12, 'bold'), foreground='#121212')
        taskNameLabel.grid(column=2, row=tasks.index(task)+1)
    print(len(tasks))

    plusPicOriginal = Image.open('img/plusB.png')

    desired_size = (50, 50)
    resized_image = plusPicOriginal.resize(desired_size, Image.Resampling.LANCZOS)

    plusButtonPic = ImageTk.PhotoImage(resized_image)

    plusButton = tk.Button(root, image=plusButtonPic, command=showAddTaskView, bd=0, bg="#121212", activebackground="#121212")
    plusButton.image = plusButtonPic
    plusButton.grid(column=4, row=len(tasks)+1)

root = tk.Tk()
root.title("PrioriTask")
root.configure(bg="#121212")
root.geometry("1280x720")

tasks = []
loadMain()

root.mainloop()
