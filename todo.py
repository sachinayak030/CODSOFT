import tkinter as tk
from tkinter import messagebox
import json
import os

class TodoListApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Todo List App")
        self.geometry("600x400")
        self.configure(bg="azure3")
        self.tasks = []
        self.data_file = "todo_data.json"
        self.create_widgets()
        self.load_tasks()

    def create_widgets(self):
        self.task_entry = tk.Entry(self, width=50)
        self.task_entry.pack(pady=10)
        self.add_button = tk.Button(self, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=10)

        self.tasks_frame = tk.Frame(self, bg="#ffffff", bd=2, relief="solid", highlightbackground="dodger blue", highlightcolor="dodger blue", highlightthickness=2)
        self.tasks_frame.pack(pady=10, padx=20, fill='both', expand=True)

        # Table Headers
        self.headers_frame = tk.Frame(self.tasks_frame, bg="slateGray1", bd=1, relief="solid", highlightbackground="dodger blue", highlightcolor="dodger blue", highlightthickness=2)
        self.headers_frame.pack(fill='x')
        tk.Label(self.headers_frame, text="Task", font=("Times New Roman 20 bold", 12, "bold"), fg="medium purple", bg="slateGray1").pack(side='left', padx=20, expand=True)
        tk.Label(self.headers_frame, text="Completed", font=("Times New Roman 20 bold", 12, "bold"), fg="medium purple", bg="slateGray1").pack(side='left', padx=20, expand=True)
        tk.Label(self.headers_frame, text="Update", font=("Times New Roman 20 bold", 12, "bold"), fg="medium purple", bg="slateGray1").pack(side='left', padx=20, expand=True)

    def load_tasks(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                self.tasks = json.load(file)
                self.update_ui()

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks.append({"task": task, "completed": False})
            self.update_ui()
            self.save_tasks()
            self.task_entry.delete(0, 'end')

    def update_ui(self):
        for widget in self.tasks_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget != self.headers_frame:
                widget.destroy()

        for task in self.tasks:
            task_frame = tk.Frame(self.tasks_frame, bg="white", bd=1, relief="solid", highlightbackground="dodger blue", highlightcolor="dodger blue", highlightthickness=2)
            task_frame.pack(fill='x', pady=5)

            task_label = tk.Label(task_frame, text=task["task"], bg="white")
            task_label.pack(side='left', padx=20, expand=True)

            if task["completed"]:
                complete_label = tk.Label(task_frame, text="✔", fg="green", bg="#ffffff")
                complete_label.pack(side='left', padx=20, expand=True)
            else:
                complete_label = tk.Label(task_frame, text="", bg="#ffffff")
                complete_label.pack(side='left', padx=20, expand=True)

            actions_frame = tk.Frame(task_frame, bg="#ffffff")
            actions_frame.pack(side='left', padx=5, expand=True)
            if not task["completed"]:
                mark_button = tk.Button(actions_frame, text="Done", command=lambda t=task: self.mark_task_done(t))
                mark_button.pack(side='left')
            delete_button = tk.Button(actions_frame, text="Delete", command=lambda t=task: self.delete_task(t))
            delete_button.pack(side='left')

    def mark_task_done(self, task):
        task["completed"] = True
        self.update_ui()
        self.save_tasks()

    def delete_task(self, task):
        self.tasks.remove(task)
        self.update_ui()
        self.save_tasks()

    def save_tasks(self):
        with open(self.data_file, 'w') as file:
            json.dump(self.tasks, file)

if __name__ == "__main__":
    app = TodoListApp()
    app.mainloop()
