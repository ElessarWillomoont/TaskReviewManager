import json
import os
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox, simpledialog

# Path to the JSON file
DATA_FILE = "task_data.json"

# Check if the JSON file exists. If not, prompt the user to create a new one or exit.
def check_data_file():
    if not os.path.exists(DATA_FILE):
        response = messagebox.askyesno("File Not Found", "task_data.json not found. Do you want to create a new file?\nSelect 'No' to exit the application.")
        if response:
            with open(DATA_FILE, 'w') as file:
                json.dump({}, file)
            messagebox.showinfo("File Created", "A new task_data.json file has been created.")
        else:
            messagebox.showerror("Exiting", "The application cannot run without the data file. Now exiting.")
            exit()

# Load the JSON data from the file
def load_data():
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

# Save the JSON data to the file
def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Get today's date
today_date = datetime.now().strftime("%Y-%m-%d")

# Review intervals (in days, weeks, and months)
intervals = {
    "1 day later": timedelta(days=1),
    "3 days later": timedelta(days=3),
    "1 week later": timedelta(weeks=1),
    "2 weeks later": timedelta(weeks=2),
    "1 month later": timedelta(days=30),
    "3 months later": timedelta(days=90),
    "6 months later": timedelta(days=180),
}

# Calculate the review dates based on the starting date
def calculate_review_dates(start_date):
    return {name: (start_date + interval).strftime("%Y-%m-%d") for name, interval in intervals.items()}

# Main GUI application class
class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Management System")
        self.data = load_data()
        self.selected_task = None  # Currently selected task
        self.selected_task_date = None  # Date of the selected task
        self.setup_gui()

    def setup_gui(self):
        # Create the main layout frame
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Display today's date
        tk.Label(self.frame, text=f"Today's Date: {today_date}").pack(anchor="w")

        # Display tasks that need to be reviewed today
        self.review_frame = tk.Frame(self.frame)
        self.review_frame.pack(fill="both", expand=True, pady=(10, 0))

        tk.Label(self.review_frame, text="Tasks to Review Today:", font=("Arial", 12, "bold")).pack(anchor="w")
        self.task_listbox = tk.Listbox(self.review_frame, height=10, selectmode=tk.SINGLE)
        self.task_listbox.pack(fill="both", expand=True)
        self.task_listbox.bind('<<ListboxSelect>>', self.on_task_select)  # Bind the select event

        # Load tasks that haven't been completed
        self.display_unfinished_tasks()

        # Button to mark selected tasks as completed
        self.complete_button = tk.Button(self.frame, text="Mark Selected Task as Completed", command=self.mark_as_complete)
        self.complete_button.pack(pady=(5, 10))

        # Input field to add new tasks
        self.new_task_entry = tk.Entry(self.frame, width=50)
        self.new_task_entry.pack(pady=(5, 5))
        self.add_button = tk.Button(self.frame, text="Add Today's Task", command=self.add_today_task)
        self.add_button.pack()

        # Button to add past tasks
        self.edit_past_button = tk.Button(self.frame, text="Add Past Task", command=self.add_past_task)
        self.edit_past_button.pack(pady=(10, 10))

    # Handle task selection from the listbox
    def on_task_select(self, event):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task_text = self.task_listbox.get(selected_index)
            if "(Unfinished" in task_text:  # Ensure it's an unfinished task
                try:
                    date_part, content_part = task_text.split(")", 1)
                    date_str = date_part.replace("(Unfinished", "").strip()
                    self.selected_task_date = date_str  # Save the selected date
                    self.selected_task = content_part.strip()  # Save the selected task content
                except ValueError:
                    print("Error parsing the task, could not extract date and content.")
            else:
                self.selected_task = task_text
                self.selected_task_date = today_date

            # Debugging information
            print(f"Selected task: {self.selected_task}")
            print(f"Task date: {self.selected_task_date}")

    # Mark the selected task as completed
    def mark_as_complete(self):
        if self.selected_task and self.selected_task_date:
            tasks = self.data.get(self.selected_task_date, {}).get("review_tasks", [])
            print(f"Attempting to mark task as completed: {self.selected_task} (Date: {self.selected_task_date})")  # Debugging information
            for task in tasks:
                if task["content"] == self.selected_task:
                    task["completed"] = True  # Mark the task as completed
                    print(f"Task found and marked as completed: {task['content']}")  # Debugging information
                    save_data(self.data)  # Save changes to the JSON file
                    self.update_task_listbox()  # Refresh the task list
                    messagebox.showinfo("Task Completed", "Task has been marked as completed!")
                    break
            else:
                print("Could not find the task to mark as completed.")  # Debugging information

    # Refresh the task listbox
    def update_task_listbox(self):
        self.display_unfinished_tasks()

    # Display unfinished tasks
    def display_unfinished_tasks(self):
        self.task_listbox.delete(0, tk.END)  # Clear the current list

        # Get today's date
        today = datetime.now().date()

        # Find all unfinished tasks from previous days
        unfinished_tasks = []
        for date, tasks in self.data.items():
            task_date = datetime.strptime(date, "%Y-%m-%d").date()
            if task_date < today:  # Only check tasks from previous days
                for task in tasks.get("review_tasks", []):
                    if not task.get("completed", False):
                        unfinished_tasks.append((date, task["content"]))

        # Sort unfinished tasks by date
        unfinished_tasks.sort(key=lambda x: x[0])

        # Display all unfinished tasks at the top and highlight them in red
        for date, content in unfinished_tasks:
            self.task_listbox.insert(tk.END, f"(Unfinished {date}) {content}")
            self.task_listbox.itemconfig(tk.END, {'bg': 'red'})

        # Display today's tasks that need to be reviewed
        today_tasks = self.data.get(today_date, {}).get("review_tasks", [])
        for task in today_tasks:
            self.task_listbox.insert(tk.END, task["content"])
            if not task.get("completed", False):
                self.task_listbox.itemconfig(tk.END, {'bg': 'red'})

    # Add a new task for today
    def add_today_task(self):
        new_task = self.new_task_entry.get().strip()
        if new_task:
            if today_date not in self.data:
                self.data[today_date] = {"work_done": [], "review_tasks": []}
            self.data[today_date]["work_done"].append(new_task)
            self.schedule_review(new_task)
            self.new_task_entry.delete(0, tk.END)
            save_data(self.data)
            messagebox.showinfo("Task Added", "Today's task has been added!")

    # Schedule review dates for a new task
    def schedule_review(self, task_content):
        start_date = datetime.strptime(today_date, "%Y-%m-%d")
        review_dates = calculate_review_dates(start_date)
        for date in review_dates.values():
            if date not in self.data:
                self.data[date] = {"work_done": [], "review_tasks": []}
            self.data[date]["review_tasks"].append({"content": task_content, "completed": False})

    # Add a task for a previous day
    def add_past_task(self):
        date_str = simpledialog.askstring("Add Past Task", "Enter the date for the task (format: YYYY-MM-DD):")
        if date_str:
            try:
                datetime.strptime(date_str, "%Y-%m-%d")  # Validate date format
                task_content = simpledialog.askstring("Add Past Task", f"Enter the task content for {date_str}:")
                if task_content:
                    if date_str not in self.data:
                        self.data[date_str] = {"work_done": [], "review_tasks": []}
                    self.data[date_str]["work_done"].append(task_content)
                    self.schedule_review_for_date(task_content, date_str)
                    save_data(self.data)
                    messagebox.showinfo("Task Added", f"Task for {date_str} has been added!")
            except ValueError:
                messagebox.showerror("Invalid Date Format", "Please enter the date in the correct format (YYYY-MM-DD).")

    # Schedule review dates for a task on a specific date
    def schedule_review_for_date(self, task_content, date_str):
        start_date = datetime.strptime(date_str, "%Y-%m-%d")
        review_dates = calculate_review_dates(start_date)
        for date in review_dates.values():
            if date not in self.data:
                self.data[date] = {"work_done": [], "review_tasks": []}
            self.data[date]["review_tasks"].append({"content": task_content, "completed": False})

# Create the application window
if __name__ == "__main__":
    check_data_file()  # Ensure the JSON file exists
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
