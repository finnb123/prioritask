import tkinter as tk

def buttonPress():
    print("Button Pressed")

root = tk.Tk()
root.title("PrioriTask")
root.geometry("1280x720")

button = tk.Button(root, text="Test", command=buttonPress)
button.pack()

addTaskView = tk.Frame(root)

root.mainloop()