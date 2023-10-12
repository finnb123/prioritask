import tkinter as tk

def showAddTaskView():
    print("showing addtaskview")
    addTaskView.pack(fill="both", expand=True)

def hideAddTaskView():
    print("hiding addtaskview")
    addTaskView.pack_forget()

def plusPress():
    print("+ Button Pressed")
    showAddTaskView()

root = tk.Tk()
root.title("PrioriTask")
root.geometry("1280x720")

plusButton = tk.Button(root, text="+", command=plusPress)
plusButton.pack()

addTaskView = tk.Frame(root, bg="black")
testLabel = tk.Label(addTaskView, text="Test")
testLabel.pack()
taskViewExit = tk.Button(addTaskView, text="exit", command=hideAddTaskView)
taskViewExit.pack()



root.mainloop()