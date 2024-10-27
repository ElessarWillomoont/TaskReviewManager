# Task Management System

A simple task management application built with Python and Tkinter. The application allows users to track daily tasks, set review reminders based on Ebbinghaus' forgetting curve, and manage task completion.

## Features

- **Task Addition**: Add tasks for today or any past date.
- **Review Scheduling**: Automatically schedule review dates for tasks based on a predefined schedule.
- **Task Completion**: Mark tasks as completed, with all unfinished tasks highlighted in red.
- **Data Storage**: All task data is stored in a JSON file (`task_data.json`).

## Getting Started

### Prerequisites

Make sure you have Python 3.7 or higher installed. You can check your version using:

python --version

### Installation

Clone the Repository:


git clone https://github.com/ElessarWillomoont/TaskReviewManager.git

cd TaskReviewManager

Install Required Libraries: The main dependency is tkinter, which usually comes pre-installed with Python. If needed, you can install additional dependencies using:


pip install pillow

Running the Application

To start the application, simply run:

python TRM.py

### Usage

Add Today's Task: Use the input field and click "Add Today's Task."

Review Tasks: All tasks to review are displayed in the list box. Unfinished tasks are highlighted in red.

Mark Task as Completed: Select a task from the list and click "Mark Selected Task as Completed."

Add Past Task: Click the "Add Past Task" button to add a task for a previous date.

# **Special: Idea by me, code by GPT 🤣**
