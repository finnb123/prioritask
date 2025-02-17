import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import pickle
import os
import shutil
from classes.task import Task
import datetime
from funcs.computation import findPriority

#password imports
from passlib.hash import argon2
import sqlite3


global tasks
global pastTasks
global userName
global taskFileName
global completedFileName

def clearScreen():
    '''Clears all widgets from the screen'''
    for widget in root.winfo_children():
        widget.destroy()

def refresh():
    '''Clears the screen and loads the main menu'''
    clearScreen()
    loadMain()

def removeTask(task, view):
    '''Marks a task or subtask as complete
    task: Task or Subtask to mark
    view: Current app view. 0 - Main, 
                            1 - Detailed Task View
                            2 - Past tasks view'''
    global tasks
    global completedTasks
    # taskFileName = username + "Tasks.file"
    # completedFileName = username + "Completed.file"

    task.markComplete()
    if task not in completedTasks and type(task)==Task:
        for subtask in task.subtasks: subtask.markComplete()
        completedTasks.append(task)
    with open(taskFileName, "wb") as taskFile:
        pickle.dump(tasks, taskFile)
    with open(completedFileName, "wb") as taskFile:
        pickle.dump(completedTasks, taskFile)
    if view == 0:
        refresh()
    if view == 1:
        showDetailedTaskView(task.parent)
    if view == 2:
        pastTasks()

def draw_rounded_rectangle(canvas, x, y, width, height, corner_radius, task, index=0, taskType=0, view=0, **kwargs):
    '''
    Draws a rounded rectangle to display task information.
    '''
    global imageReferences
    # Create rounded corners
    canvas.create_arc(x, y, x + corner_radius * 2, y + corner_radius * 2, start=90, extent=90, fill=kwargs['fill'], outline="")
    canvas.create_arc(x + width - corner_radius * 2, y, x + width, y + corner_radius * 2, start=0, extent=90, fill=kwargs['fill'], outline="")
    canvas.create_arc(x, y + height - corner_radius * 2, x + corner_radius * 2, y + height, start=180, extent=90, fill=kwargs['fill'], outline="")
    canvas.create_arc(x + width - corner_radius * 2, y + height - corner_radius * 2, x + width, y + height, start=270, extent=90, fill=kwargs['fill'], outline="")

    # Create 2 rectangles to fill the space
    canvas.create_rectangle(x + corner_radius, y, x + width - corner_radius, y + height, fill=kwargs['fill'], outline="")
    canvas.create_rectangle(x, y+corner_radius, x + width, y + height - corner_radius, fill=kwargs['fill'], outline="")

    # Create text representing task information
    canvas.create_text(x+corner_radius/2, y+corner_radius/2, text=task.name, font='roboto 12 normal', fill="#FFFAF1", anchor="nw")
    if taskType==0:canvas.create_text(width-corner_radius/2, height-corner_radius/2, text=f"Due {task.dueDate}", font='roboto 12 normal', fill="#FFFAF1", anchor="se")
    if taskType==0:canvas.create_text(x+width-corner_radius, y+corner_radius, text=index, font='roboto 12 normal')

    # Create clickable image to remove task
    minusPicOriginal = Image.open('img/minus.png')
    desired_size = (30, 30)
    resizedMinus = minusPicOriginal.resize(desired_size, Image.Resampling.LANCZOS)
    minusButtonPic = ImageTk.PhotoImage(resizedMinus)
    ## Stop garbage collection of image
    if taskType==0:imageReferences[task.taskID] = minusButtonPic
    else:imageReferences[task.id] = minusButtonPic
    if not task.completed:
        button = tk.Button(canvas, image=minusButtonPic, command=lambda: removeTask(task, view), bd=0, bg=kwargs['fill'], activebackground=kwargs['fill'])
        button.image = minusButtonPic
        button.place(x=x+width-(corner_radius/2), y=height/2, anchor='e')
    
def showDetailedTaskView(task):
    '''Show a detailed view of task containing task information and subtasks'''
    clearScreen()
    # Text representations of basic task info
    taskLabel = tk.Label(root, text=task.name, font=('roboto', 24, 'bold'), foreground='#03DAC6', borderwidth=0, background="#121212")
    taskLabel.place(anchor="n", relx=0.5, rely=0.05)
    if task.description != "":
        descriptText = task.description
    else: descriptText = "No Description."
    descriptLabel = tk.Label(root, text=descriptText, font=('roboto', 12, 'normal'), foreground='#03DAC6', borderwidth=0, background="#121212")
    descriptLabel.place(anchor="n", relx=0.5, rely=0.15)

    dueDateString = task.dueDate 
    dueDateElements = dueDateString.split("-")
    dueDate = datetime.date(int(dueDateElements[0]), int(dueDateElements[1]), int(dueDateElements[2]))
    today = datetime.date.today()
    daysLeft = (dueDate-today).days
    if daysLeft == 0: 
        dueLabel = tk.Label(root, text="Due Today.", font=('roboto', 12, 'normal'), foreground='#CF6679', borderwidth=0, background="#121212")
    elif daysLeft < 0: 
        dueLabel = tk.Label(root, text="Overdue.", font=('roboto', 12, 'normal'), foreground='#CF6679', borderwidth=0, background="#121212")
    elif daysLeft==1:
        dueLabel = tk.Label(root, text="Due Tomorrow.", font=('roboto', 12, 'normal'), foreground='#03DAC6', borderwidth=0, background="#121212")
    else:
        dueLabel = tk.Label(root, text=f"Due in {daysLeft} Days.", font=('roboto', 12, 'normal'), foreground='#03DAC6', borderwidth=0, background="#121212")
    dueLabel.place(anchor="n", relx=0.5, rely=0.115)

    # Find task's subtask not marked completed and display them
    if not task.completed:
        subtasksRemaining = []
        for subtask in task.subtasks:
            if not subtask.completed: subtasksRemaining.append(subtask)
        if len(subtasksRemaining)>=1:
            subtasksLabel = tk.Label(root, text="SubTasks", font=('roboto', 20, 'bold'), foreground='#03DAC6', borderwidth=0, background="#121212")
            subtasksLabel.place(anchor="n", relx=0.5, rely=0.2)
        for subtask in subtasksRemaining:
            if not subtask.completed:
                canvas = tk.Canvas(root, width=300, height=50, bg="#121212", highlightthickness=0)
                canvas.place(anchor='n', relx = 0.5, rely = 0.25+(subtasksRemaining.index(subtask)*0.08))
                draw_rounded_rectangle(canvas, 0, 0, 300, 50, 20, subtask, task.subtasks.index(subtask)+1, fill="#3700B3", taskType=1, view=1)
    # Handle displaying of subtasks in completed task view (show all)
    elif task.completed:
        if len(task.subtasks)>=1:
            subtasksLabel = tk.Label(root, text="SubTasks", font=('roboto', 20, 'bold'), foreground='#03DAC6', borderwidth=0, background="#121212")
            subtasksLabel.place(anchor="n", relx=0.5, rely=0.2)
        for subtask in task.subtasks:
            canvas = tk.Canvas(root, width=300, height=50, bg="#121212", highlightthickness=0)
            canvas.place(anchor='n', relx = 0.5, rely = 0.25+(task.subtasks.index(subtask)*0.08))
            draw_rounded_rectangle(canvas, 0, 0, 300, 50, 20, subtask, task.subtasks.index(subtask)+1, fill="#3700B3", taskType=1, view=1)


    # UI back button
    exitPicOriginal = Image.open('img/backArrowB.png')
    desired_size = (50, 50)
    resizedexit = exitPicOriginal.resize(desired_size, Image.Resampling.LANCZOS)
    exitButtonPic = ImageTk.PhotoImage(resizedexit)
    if task.completed == True:
        exitButton = tk.Button(root, image=exitButtonPic, command= pastTasks, bd=0, bg="#121212", activebackground="#121212")
    else:
        exitButton = tk.Button(root, image=exitButtonPic, command= refresh, bd=0, bg="#121212", activebackground="#121212")
    exitButton.image = exitButtonPic
    exitButton.place(anchor="n", relx=0.25, rely=0.75)
    
def addSubtaskField(subtaskFields):
    '''Add a Field for a new subtask to the addTaskView'''
    newField = tk.Entry(root, borderwidth=0, background="#4c4c4c", foreground="#FFFFFF", font=('roboto', 16, 'normal'))
    newField.place(anchor='n', relx=0.5, rely=(0.6 + (len(subtaskFields)*0.05)))
    subtaskFields.append(newField)

def showAddTaskView():
    '''Show view to create a new Task to list'''
    clearScreen()
    subtaskFields = [] # Keep track of how many subtaskFields have been added
    # View Title
    addTaskLabel = tk.Label(root, text="Create a Task", font=('roboto', 24, 'bold'), foreground='#03DAC6', borderwidth=0, background="#121212")
    addTaskLabel.place(anchor="n", relx=0.5, rely=0.05)
    # Titles and fields for user input
    # Task Name input
    titleLabel = tk.Label(root, text="Title", font=('roboto', 12, 'normal'), foreground='#03DAC6', borderwidth=0, background="#121212")
    titleLabel.place(anchor="s", relx=0.5, rely=0.2)
    nameField = tk.Entry(root, borderwidth=0, background="#4c4c4c", foreground="#FFFFFF", font=('roboto', 16, 'normal'))
    nameField.place(anchor="n", relx=0.5, rely=0.2)
    # Task Description input
    descriptionLabel = tk.Label(root, text="Description (Optional)", font=('roboto', 12, 'normal'), foreground='#03DAC6', borderwidth=0, background="#121212")
    descriptionLabel.place(anchor="s", relx=0.5, rely=0.3)
    descriptionField = tk.Entry(root, borderwidth=0, background="#4c4c4c", foreground="#FFFFFF", font=('roboto', 16, 'normal'))
    descriptionField.place(anchor="n", relx=0.5, rely=0.3)
    # Task due date input
    dateLabel = tk.Label(root, text="Due Date (YYYY-MM-DD)", font=('roboto', 12, 'normal'), foreground='#03DAC6', borderwidth=0, background="#121212")
    dateLabel.place(anchor="s", relx=0.5, rely=0.4)
    dateField = tk.Entry(root, borderwidth=0, background="#4c4c4c", foreground="#FFFFFF", font=('roboto', 16, 'normal'))
    dateField.place(anchor="n", relx=0.5, rely=0.4)
    currentDate = datetime.date.today()
    dateField.insert(-1, currentDate)
    # Task effort level input
    effortLabel = tk.Label(root, text="How big does this task feel?", font=('roboto', 12, 'normal'), foreground='#03DAC6', borderwidth=0, background="#121212")
    effortLabel.place(anchor="s", relx=0.5, rely=0.5)
    sliderStyle = ttk.Style()
    sliderStyle.configure('TScale', background='#121212', slidercolor="#03DAC6")
    workloadInt = ttk.Scale(root, from_=0, to=10, orient='horizontal', style='TScale')
    workloadInt.place(anchor="n", relx=0.5, rely=0.5, relwidth=0.25)

    # User input for task subtasks
    subtasksLabel = tk.Label(root, text="SubTasks", font=('roboto', 18, 'normal'), foreground='#03DAC6', borderwidth=0, background="#121212")
    subtasksLabel.place(anchor='n', relx=0.5, rely=0.55)
    # Button to allow user to add subtasks as they please
    addPicOriginal = Image.open('img/plusB.png')
    desired_size = (20, 20)
    resizedAdd = addPicOriginal.resize(desired_size, Image.Resampling.LANCZOS)
    addButtonPic = ImageTk.PhotoImage(resizedAdd)
    addButton = tk.Button(root, image=addButtonPic, command=lambda: 
                           addSubtaskField(subtaskFields), 
                           bd=0, bg="#121212", activebackground="#121212")
    addButton.image = addButtonPic
    addButton.place(anchor="n", relx=0.555, rely=0.56)

    # UI Elements
    # Save task
    savePicOriginal = Image.open('img/tickB.png')
    desired_size = (50, 50)
    resizedSave = savePicOriginal.resize(desired_size, Image.Resampling.LANCZOS)
    saveButtonPic = ImageTk.PhotoImage(resizedSave)
    saveButton = tk.Button(root, image=saveButtonPic, command=lambda: 
                           saveTask(nameField.get(), descriptionField.get(), workloadInt.get(), dateField.get(), subtaskFields), 
                           bd=0, bg="#121212", activebackground="#121212")
    saveButton.image = saveButtonPic
    saveButton.place(anchor="n", relx=0.75, rely=0.75)
    # Cancel / Return to main menu
    exitPicOriginal = Image.open('img/backArrowB.png')
    desired_size = (50, 50)
    resizedexit = exitPicOriginal.resize(desired_size, Image.Resampling.LANCZOS)
    exitButtonPic = ImageTk.PhotoImage(resizedexit)
    exitButton = tk.Button(root, image=exitButtonPic, command=refresh, bd=0, bg="#121212", activebackground="#121212")
    exitButton.image = exitButtonPic
    exitButton.place(anchor="n", relx=0.25, rely=0.75)

def saveTask(name:str, description:str="", workload:int=0, dueDate:str="", subtaskFields=[]):
    '''Create a new Task object with given information, add to list, and save to tasks.file'''
    global tasks
    # Dynamically create array of subtasks from subtaskFields
    subtasks = []
    for field in subtaskFields:
        subTaskName = field.get()
        if subTaskName != "": subtasks.append(subTaskName)
    # Allocate ID to task based on last assigned ID - If any exists
    if len(tasks) > 0:
        newID = tasks[-1].taskID + 1
    else:
        newID = 1
    # Create new Task object from supplied information and append to global list of tasks
    
    
    #Checks if date is valid, if it is save it and go to main screen, else show error and remain on task screen
    try:
            dueDateElements = dueDate.split("-")
            dueDateTest = datetime.date(int(dueDateElements[0]), int(dueDateElements[1]), int(dueDateElements[2]))
            newTask = Task(name=name, taskID=newID, description=description, workload=workload, dueDate=dueDate, subtasks=subtasks)
            tasks.append(newTask)
            # Save all tasks to storage
            # taskFileName = username + "Tasks.file"
            with open(taskFileName, "wb") as taskFile:
                pickle.dump(tasks, taskFile)
    except:
        messagebox.showerror('Date Error', 'Incorrect Date Format.')
        return 1
    
    refresh()

def pastTasks():
    '''Load view of past tasks'''
    clearScreen()
    titleLabel = tk.Label(root, text="Past Tasks",  font=('roboto', 44, 'bold'), foreground='#BB86FC', borderwidth=0, background="#121212")
    titleLabel.place(anchor="n", relx=0.5, rely=0.02)
    #Button to show current tasks
    exitPicOriginal = Image.open('img/backArrowB.png')
    desired_size = (50, 50)
    resizedexit = exitPicOriginal.resize(desired_size, Image.Resampling.LANCZOS)
    exitButtonPic = ImageTk.PhotoImage(resizedexit)
    exitButton = tk.Button(root, image=exitButtonPic, command=refresh, bd=0, bg="#121212", activebackground="#121212")
    exitButton.image = exitButtonPic
    exitButton.place(anchor="n", relx=0.25, rely=0.75)

    #Load past tasks from storage if any exist
    global completedTasks

    #Sort tasks in order of youngest to oldest
    completedTasks.sort(key=lambda x: x.dueDate, reverse = True)

    #Display list of tasks, only 5 currently
    for task in completedTasks:
        color="#018786"
        canvas = tk.Canvas(root, width=300, height=100, bg="#121212", highlightthickness=0)
        canvas.place(anchor='n', relx = 0.5, rely = ((completedTasks.index(task)+1)/6)+0.01)
        draw_rounded_rectangle(canvas, 0, 0, 300, 100, 20, task, completedTasks.index(task)+1, fill=color, view=2)
        canvas.bind('<Button>', func=lambda event, t=task: showDetailedTaskView(t))

def login(enteredUsername, enteredPassword, view = 0):
    try:
        connection = sqlite3.connect('sql.db')
        cursor = connection.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", [enteredUsername])
        result = cursor.fetchone()
        if result != [] and result != None:
            passwordHash = result[0]            
        cursor.close()
    
    except sqlite3.Error as error:
        print("Error occurred - ", error)

    finally:
        if connection:
            connection.close()
            print("SQLite Connection Closed")

    #Might be vulnerable to time based attack; look at in future
    if result != [] and result != None and argon2.verify(enteredPassword, passwordHash):
        global username 
        global taskFileName
        global completedFileName
        username = enteredUsername
        try:
            os.mkdir("tasksFolder/" + username)     #create user folder to contain past and present task files
        except:
            print("")   
        taskFileName =  "tasksFolder/" + username + "/" + "tasks.file"  
        completedFileName = "tasksFolder/" + username + "/" + "completed.file"
        if view == 0:
            messagebox.showinfo(title="Login Successful!", message = "Logged in")
            refresh()  
        if view == 1:
              deleteAccount()
    else:
        messagebox.showinfo(title="Login Unsuccessful!", message = "Login Failed; Invalid user ID or password")
    
def createAccount(enteredUsername, enteredPassword):
    #Create account in SQLite database. Stores passwords using argon2 hashing
    connection = sqlite3.connect("sql.db")
    cursor = connection.cursor()
    try: 
        if len(enteredPassword) < 10 or len(enteredPassword) > 128:
            messagebox.showinfo(title="Creation Unsuccessful!", message = "Account Creation Unsuccessful\nPassword Guidelines\n10<, <128, ")     
        else:
            hash = argon2.hash(enteredPassword)
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (enteredUsername,hash))
            messagebox.showinfo(title="Creation Successful!", message = "Account Creation Successful")
    except:
        messagebox.showinfo(title="Creation Unsuccessful!", message = "Account Creation Unsuccessful\nPassword Guidelines\n10 < , < 128")
    connection.commit()
    connection.close()

def loginPage(view = 0):
    clearScreen()
    '''Load View of Login Page'''
    titleLabel = tk.Label(root, text="PrioriTask", font=('roboto', 44, 'bold'), foreground='#BB86FC', borderwidth=0, background="#121212")
    titleLabel.place(anchor="n", relx=0.5, rely=0.02)

    #Username Field
    usernameLabel = tk.Label(root, text="Username", font=('roboto', 12, 'normal'), foreground='#03DAC6', borderwidth=0, background="#121212")
    usernameEntry = tk.Entry(root, borderwidth=0, background="#4c4c4c", foreground="#FFFFFF", font=('roboto', 16, 'normal'))
    usernameEntry.place(anchor="n", relx=0.5, rely=0.2)
    usernameLabel.place(anchor="s", relx=0.5, rely=0.2)

    #Password Field
    passwordLabel = tk.Label(root, text="Password", font=('roboto', 12, 'normal'), foreground='#03DAC6', borderwidth=0, background="#121212")
    passwordEntry = tk.Entry(root, borderwidth=0, background="#4c4c4c", foreground="#FFFFFF", show="*", font=('roboto', 16, 'normal'))
    passwordEntry.place(anchor="n", relx=0.5, rely=0.3)
    passwordLabel.place(anchor="s", relx=0.5, rely=0.3)
    
    if view == 0: #if coming from initial login page
        #Login Button
        loginButton = tk.Button(root, text="Login", background="#4c4c4c", foreground="#FFFFFF", font=('roboto', 16, 'normal'), command=lambda: login(str(usernameEntry.get()).lower(), str(passwordEntry.get())))
        loginButton.place(anchor="n", relx=0.5, rely=.375)
        #Create Account
        createAccountButton = tk.Button(root, text="Create Account", background="#4c4c4c", foreground="#FFFFFF", font=('roboto', 16, 'normal'), command=lambda: createAccount(str(usernameEntry.get()).lower(), str(passwordEntry.get())))
        createAccountButton.place(anchor="n", relx=0.5, rely=.45)

    if view == 1: #if coming from account page delete account
        authenticateButton = tk.Button(root, text="Authenticate", background="#4c4c4c", foreground="#FFFFFF", font=('roboto', 16, 'normal'), command=lambda: login( str(usernameEntry.get()).lower(), str(passwordEntry.get()), 1))
        authenticateButton.place(anchor="n", relx=0.5, rely=.375)

def accountPage():
    clearScreen()
    '''Load View of Account Page'''
    titleLabel = tk.Label(root, text=username, font=('roboto', 44, 'bold'), foreground='#BB86FC', borderwidth=0, background="#121212")
    titleLabel.place(anchor="n", relx=0.5, rely=0.02)    

    deleteAccountButton = tk.Button(root, text="Delete Account", background="#4c4c4c", foreground="#FFFFFF", font=('roboto', 16, 'normal'), command=lambda: loginPage(1))
    deleteAccountButton.place(anchor="n", relx=0.5, rely=.2)   

def deleteAccount():
    try:
        if os.path.exists("tasksFolder/"+username):
            shutil.rmtree("tasksFolder/" + username)
        connection = sqlite3.connect("sql.db")
        cursor = connection.cursor()
        query = "DELETE FROM users WHERE username = ?"
        args = (username,)
        cursor.execute(query, args)
        connection.commit()
        connection.close()
        messagebox.showinfo(title="Deletion Successful!", message = "Account Deletion Successful")
        loginPage()
    except:
        messagebox.showinfo(title="Deletion Unsuccessful!", message = "Account Deletion Unsuccessful")

def loadMain():
    '''Load the main view containing prioritised list of tasks'''
    titleLabel = tk.Label(root, text="PrioriTask", font=('roboto', 44, 'bold'), foreground='#BB86FC', borderwidth=0, background="#121212")
    titleLabel.place(anchor="n", relx=0.5, rely=0.02)
    plusButtonOffset = 0.15
    global tasks
    global completedTasks

    if os.path.exists(taskFileName):
        with open(taskFileName, "rb") as taskFile:
            tasks = pickle.load(taskFile)
    else:
        tasks = []
    remainingTasks = []

    #Load completed tasks from storage if any exist
    if os.path.exists(completedFileName):
        with open(completedFileName, "rb") as taskFile:
            completedTasks = pickle.load(taskFile)
    else:
        completedTasks = []

    # Sort through tasks and determine which are yet to be completed
    for task in tasks:
        if not task.completed: remainingTasks.append(task)
    # Sort uncompleted tasks using priority algorithm
    tasks = findPriority(remainingTasks)
    # Add UI for task list if there are any tasks
    if len(tasks) >= 1:
        subTitleLabel = tk.Label(root, text="Here's what you should be working on now:", font=('roboto', 16, 'bold'), foreground='#6200BE', borderwidth=0, background="#121212")
        subTitleLabel.place(anchor="n", relx=0.5, rely=0.115)
        plusButtonOffset = (len(tasks)/6)+0.175
    for task in tasks:
        if tasks.index(task)<=3:
            if tasks.index(task)==0: color="#6200EE"
            else: color="#3700B3"
            canvas = tk.Canvas(root, width=300, height=100, bg="#121212", highlightthickness=0)
            canvas.place(anchor='n', relx = 0.5, rely = ((tasks.index(task)+1)/6)+0.01)
            draw_rounded_rectangle(canvas, 0, 0, 300, 100, 20, task, tasks.index(task)+1, fill=color)
            canvas.bind('<Button>', func=lambda event, t=task: showDetailedTaskView(t))
    print(len(tasks))

    # Plus button to add a new task to list
    plusPicOriginal = Image.open('img/plusB.png')
    desired_size = (50, 50)
    resized_image = plusPicOriginal.resize(desired_size, Image.Resampling.LANCZOS)
    plusButtonPic = ImageTk.PhotoImage(resized_image)
    plusButton = tk.Button(root, image=plusButtonPic, command=showAddTaskView, bd=0, bg="#121212", activebackground="#121212")
    plusButton.image = plusButtonPic
    plusButton.place(anchor='n', relx=0.5, rely=min(plusButtonOffset, 0.85))
    # Message to inform when there are more tasks than can be fit on screen
    if len(tasks)>4:
        footnoteLabel = tk.Label(root, text="Lower-priority tasks are displayed when higher-priority tasks are complete.", font=('roboto', 12, 'normal'), foreground='#6200BE', borderwidth=0, background="#121212")
        footnoteLabel.place(anchor="n", relx=0.5, rely=0.95)

    # Button to view Past Tasks
    pastPicOriginal = Image.open('img/pastTasksB.png')
    desired_size = (50, 50)
    resizedPast = pastPicOriginal.resize(desired_size, Image.Resampling.LANCZOS)
    pastButtonPic = ImageTk.PhotoImage(resizedPast)
    pastButton = tk.Button(root, image=pastButtonPic, command=pastTasks, bd=0, bg="#121212", activebackground="#121212")
    pastButton.image = pastButtonPic
    pastButton.place(anchor="n", relx=0.25, rely=0.75)
    
    # Refresh Button
    refreshPicOriginal = Image.open('img/refreshB.png')
    desired_size = (50, 50)
    resizedRefresh = refreshPicOriginal.resize(desired_size, Image.Resampling.LANCZOS)
    refreshButtonPic = ImageTk.PhotoImage(resizedRefresh)
    refreshButton = tk.Button(root, image=refreshButtonPic, command=refresh, bd=0, bg="#121212", activebackground="#121212")
    refreshButton.image = refreshButtonPic
    refreshButton.place(anchor="n", relx=0.75, rely=0.75)

    # Account Screen Button
    accountPicOriginal = Image.open('img/male-avatarB.png')
    desired_size = (50, 50)
    resizedAccount = accountPicOriginal.resize(desired_size, Image.Resampling.LANCZOS)
    accountButtonPic = ImageTk.PhotoImage(resizedAccount)
    accountButton = tk.Button(root, image=accountButtonPic, command=accountPage, bd=0, bg="#121212", activebackground="#121212")
    accountButton.image = accountButtonPic
    accountButton.place(anchor="n", relx=0.5, rely=0.75)

if __name__ == "__main__":
    #Create Database if doesn't exist
    path = 'sql.db'
    if not os.path.isfile(path):
        connection = sqlite3.connect("sql.db")
        connection.execute(''' CREATE TABLE users
                                (
                                    username        TEXT PRIMARY KEY    NOT NULL,
                                    password        TEXT                NOT NULL     
                                )
                        ''')
        print("SQLite DB Initialized")
        if connection:
            connection.close
            print("SQLite Connection Closed")


    root = tk.Tk()
    root.title("PrioriTask")
    root.configure(bg="#121212")
    root.geometry("1280x720")
    root.iconbitmap("img/plusB.ico")

    imageReferences = {}
    tasks = []
    loginPage()

    root.mainloop()