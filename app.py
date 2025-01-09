"""
Acceptance Criteria (ACs)

Core Functionality
	x.	x Add Tasks:
	•	x I can add a task by typing its title into a text field and clicking an “Add Task” button.
	•	x (NEEDS GUI) If the task title is empty, I see an error message.
	x.	x View Tasks:
	•	x I can view all my tasks in a scrollable list on the main screen.
	•	x Each task displays its title and status (completed or not).
	x.	x Mark Tasks as Completed:
	•	x I can mark tasks as completed by selecting them and clicking a “Mark as Completed” button.
	•	x Completed tasks appear visually distinct (e.g., grayed out or with a strike-through).
	x.	x Delete Tasks:
	•	x I can delete tasks by selecting them and clicking a “Delete Task” button.
	x.	x Persist Data:
	•	x All tasks are saved to a file (JSON format) so that I can access them the next time I open the app.
GUI Requirements
	x.	x User-Friendly Layout:
	•	x The app uses a clean vertical layout with the following sections:
	•	x A text field for entering task titles.
	•	x Buttons for adding, marking as completed, and deleting tasks.
	•	x A scrollable list of tasks.
	x.	Real-Time Updates:
	•	x The list of tasks updates in real time whenever I add, delete, or modify a task.
Error Handling
	8.	Error Notifications:
	•	x If I try to add an empty task, a popup error message appears, preventing the task from being added.
	•	If I try to delete or mark a task without selecting one, I see a warning message.
Edge Cases
	x.	Handle Empty States:
	•	x If there are no tasks, the task list should display a friendly message (e.g., “No tasks yet!”).
	•	x I cannot mark or delete tasks when the list is empty.
	x.	Prevent Duplicates:
	•	x If I try to add a task with the same title as an existing one, I see a message indicating that duplicate tasks are not allowed.
Stretch Goals
	1.	Filter Tasks:
	•	I can filter the task list to show only completed or pending tasks.
	2.	Edit Tasks:
	•	I can edit the title of an existing task.
"""
from PySide6.QtWidgets import QListWidgetItem

"""
Acceptance Criteria (ACs)

Core Functionality
	1.	Add Tasks:
	•	I can add a task by typing its title into a text field and clicking an “Add Task” button.
	•	If the task title is empty, I see an error message.
	2.	View Tasks:
	•	I can view all my tasks in a scrollable list on the main screen.
	•	Each task displays its title and status (completed or not).
	3.	Mark Tasks as Completed:
	•	I can mark tasks as completed by selecting them and clicking a “Mark as Completed” button.
	•	Completed tasks appear visually distinct (e.g., grayed out or with a strike-through).
	4.	Delete Tasks:
	•	I can delete tasks by selecting them and clicking a “Delete Task” button.
	5.	Persist Data:
	•	All tasks are saved to a file (JSON format) so that I can access them the next time I open the app.
GUI Requirements
	6.	User-Friendly Layout:
	•	The app uses a clean vertical layout with the following sections:
	•	A text field for entering task titles.
	•	Buttons for adding, marking as completed, and deleting tasks.
	•	A scrollable list of tasks.
	7.	Real-Time Updates:
	•	The list of tasks updates in real time whenever I add, delete, or modify a task.
Error Handling
	8.	Error Notifications:
	•	If I try to add an empty task, a popup error message appears, preventing the task from being added.
	•	If I try to delete or mark a task without selecting one, I see a warning message.
Edge Cases
	9.	Handle Empty States:
	•	If there are no tasks, the task list should display a friendly message (e.g., “No tasks yet!”).
	•	I cannot mark or delete tasks when the list is empty.
	10.	Prevent Duplicates:
	•	If I try to add a task with the same title as an existing one, I see a message indicating that duplicate tasks are not allowed.
Stretch Goals
	1.	Filter Tasks:
	•	I can filter the task list to show only completed or pending tasks.
	2.	Edit Tasks:
	•	I can edit the title of an existing task.
"""

import json
import logging
from pathlib import Path

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtGui import QKeyEvent

from task import Task

# Paths
CUR_DIR = Path(__file__).parent
DATA_FILE_PATH = CUR_DIR / "data"
JSON_FILE_PATH = DATA_FILE_PATH / "tasks.json"


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.tasks = self.load_tasks()
        self.setup_ui()
        self.setWindowTitle("Task manager")
        self.setup_connections()
        self.populate_tasks()

    @staticmethod
    def load_tasks():
        """
        Creates list of Task objects
        Returns: list of task objects

        """
        try:
            with open(JSON_FILE_PATH, 'r') as json_file:
                content = json.load(json_file)
        except json.JSONDecodeError:
            with open(JSON_FILE_PATH, 'w') as json_file:
                json.dump([], json_file)
            return []

        return [Task.from_dict(item) for item in content]

    def setup_ui(self):
        # create widgets
        self.layout = QtWidgets.QVBoxLayout(self)

        self.le_task_title = QtWidgets.QLineEdit()
        self.le_task_title.setPlaceholderText("Enter the task name here")
        self.le_task_title.setStyleSheet("""
            color: rgba(60, 60, 60, 1);
            background-color: rgba(230, 230, 250, 1);
            border: 2px solid rgba(60, 60, 60, 1);
            """)

        self.btn_add_task = QtWidgets.QPushButton("Add task")
        self.btn_add_task.setStyleSheet("""
            QPushButton {
            color: rgba(60, 60, 60, 1);
            background-color: rgba(144, 238, 144, 1);
            border: 2px solid rgba(144, 238, 144, 1); 
            border-radius: 10px;
            font-family: 'Quicksand';
            font-weight: 600;
            font-size: 15px
            }
            QPushButton::hover {
            background-color: rgba(173, 216, 230, 1);
            border: 2px solid rgba(173, 216, 230, 1);
            }
            """)

        self.lw_task_list = QtWidgets.QListWidget()
        self.lw_task_list.setStyleSheet("""
            QListWidget {
            background-color: rgba(230, 230, 250, 1);
            border-radius: 10px
            }
            QListWidget::item {
            border: 2px solid rgba(0, 0, 0, 0);
            border-radius: 10px
            }
            QListWidget::item:selected {
            background-color: rgba(255, 228, 196, 1);
            border: 2px solid rgba(0, 0, 0, 0);
            }
            """)

        self._setup_qframe()

        self.btn_mark_as_completed = QtWidgets.QPushButton("Mark as completed")
        self.btn_mark_as_completed.setStyleSheet("""
            QPushButton {
            color: rgba(60, 60, 60, 1);
            background-color: rgba(255, 193, 7, 1);
            border: 2px solid rgba(255, 193, 7, 1); 
            border-radius: 10px;
            font-family: 'Quicksand';
            font-weight: 600;
            font-size: 15px
            }
            QPushButton::hover {
            background-color: rgba(173, 216, 230, 1);
            border: 2px solid rgba(173, 216, 230, 1);
            }
            """)

        self.btn_delete_task = QtWidgets.QPushButton("Delete task")
        self.btn_delete_task.setStyleSheet("""
            QPushButton {
            color: rgba(60, 60, 60, 1);
            background-color: rgba(244, 67, 54, 1);
            border: 2px solid rgba(244, 67, 54, 1); 
            border-radius: 10px;
            font-family: 'Quicksand';
            font-weight: 600;
            font-size: 15px
            }
            QPushButton::hover {
            background-color: rgba(173, 216, 230, 1);
            border: 2px solid rgba(173, 216, 230, 1);
            }
            """)

        # add widgets
        self.layout.addWidget(self.le_task_title)
        self.layout.addWidget(self.btn_add_task)
        self.layout.addWidget(self.lw_task_list)
        self.layout.addWidget(self.qframe_no_tasks);
        self.qframe_no_tasks.hide()
        self.layout.addWidget(self.btn_mark_as_completed)
        self.layout.addWidget(self.btn_delete_task)

        logging.info("UI completed")
        return True

    def setup_connections(self):
        self.btn_add_task.clicked.connect(self.add_task)
        self.le_task_title.returnPressed.connect(self.add_task)
        self.btn_mark_as_completed.clicked.connect(self.change_completion_status)
        self.btn_delete_task.clicked.connect(self.delete_task)
        self.lw_task_list.installEventFilter(self)

        logging.info("Connections completed")
        return True

    def populate_tasks(self):
        for task in self.tasks:
            lw_item_task = self._to_lw_item(task)
            if task.is_completed:
                self.lw_task_list.insertItem(len(self.tasks), lw_item_task)
                self._change_task_display(lw_item_task, True)
            else:
                print(False)
                self.lw_task_list.insertItem(0, lw_item_task)
                self._change_task_display(lw_item_task, False)

        if not self.tasks:
            self._show_no_tasks(True)

        logging.info("LIST WIDGET - Tasks populated")

        return True

    def change_completion_status(self):
        objects_selected_tasks = self._convert_selected_items_to_class_object_list()
        lw_items_selected_tasks = self.lw_task_list.selectedItems()
        index = 0

        for task in objects_selected_tasks:  # mark as completed internally
            if task.is_completed is False:
                task.change_completion_status(True)
                self._change_task_display(lw_items_selected_tasks[index], True)
            else:
                task.change_completion_status(False)
                self._change_task_display(lw_items_selected_tasks[index], False)
            index += 1

        self.save_tasks()

        return True

    def add_task(self):
        task_titles = [task.title for task in self.tasks]
        task = Task(self.le_task_title.text())
        if task.title in task_titles:
            logging.warning("Cannot have two tasks with the same title.")
            # come back: error
            self._show_le_error(True, "Cannot have two tasks with the same title")
            self.le_task_title.setText("")
            return False
        if not task.check_task_title_length():
            logging.warning("Task title must not be empty")
            # come back: error
            self._show_le_error(True, "Task title must not be empty")
            return False

        self._show_le_error(False)

        self.tasks.append(task)

        lw_task = self._to_lw_item(task)
        lw_task.setForeground(QtGui.QColor(60, 60, 60, 255))

        self.lw_task_list.insertItem(0, lw_task)

        self._show_no_tasks(False)
        self.le_task_title.setText("")
        self.save_tasks()

        logging.info("Added task")

        return True

    def delete_task(self):
        class_object_list = self._convert_selected_items_to_class_object_list()
        list_widget_item_list = self.lw_task_list.selectedItems()

        # remove task from app tasks list
        for class_object in class_object_list:
            self.tasks.remove(class_object)
            logging.info(f"Removed {class_object.title} - self.tasks")

        # remove task from list widget
        for list_widget_item in list_widget_item_list:
            row = self.lw_task_list.row(list_widget_item)
            self.lw_task_list.takeItem(row)
            logging.info(f"Removed {list_widget_item.text()} - list widget")

        self.save_tasks()
        logging.info("Deleted task")

        if not self.tasks:
            self._show_no_tasks(True)

        return True

    def save_tasks(self):
        # take tasks attribute info | convert to dict | overwrite json file
        task_object_list = self.tasks
        task_dict_list = [Task.to_dict(task_object) for task_object in task_object_list]

        with open(JSON_FILE_PATH, 'w') as json_file:
            json.dump(task_dict_list, json_file, indent=4)
            logging.info("JSON - Tasks saved")

        return True

    def eventFilter(self, watched: QtCore.QObject, event: QKeyEvent):
        """
        Change keybindings in-app
        Args:
            watched: QObject being focused on
            event: What is happening? Key being pressed? Mouse being clicked?

        Returns: True if specific action has been detected. Otherwise, hands the actions to widgets.

        """
        if watched == self.lw_task_list and event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Backspace:
                self.delete_task()
                return True
            if event.key() == QtCore.Qt.Key.Key_Return:
                self.change_completion_status()
                return True
        return super().eventFilter(watched, event)

    def _show_le_error(self, show: bool, error_reason: str = ""):
        if show:
            self.le_task_title.setPlaceholderText(error_reason)
            self.le_task_title.setStyleSheet("""
                color: rgba(60, 60, 60, 1);
                background-color: rgba(230, 230, 250, 1);
                border: 2px solid red;
                """)
        if not show:
            self.le_task_title.setPlaceholderText("Enter the task name here")
            self.le_task_title.setStyleSheet("""
                color: rgba(60, 60, 60, 1);
                background-color: rgba(230, 230, 250, 1);
                border: 2px solid rgba(60, 60, 60, 1);
                """)

    @staticmethod
    def _to_lw_item(task: Task) -> QtWidgets.QListWidgetItem:
        lw_item = QtWidgets.QListWidgetItem(task.title)
        lw_item.setData(QtCore.Qt.UserRole, task)
        return lw_item

    def _convert_selected_items_to_class_object_list(self) -> list[Task]:
        selected_tasks = self.lw_task_list.selectedItems()
        return [task.data(QtCore.Qt.UserRole) for task in selected_tasks]

    def _change_task_display(self, task: QListWidgetItem, complete: bool):
        # change font
        task.setFont(task.font())
        # change colour
        if complete:
            task.setForeground(QtGui.QColor(60, 60, 60, 100))
        else:
            task.setForeground(QtGui.QColor(60, 60, 60, 255))  # check if not overwritten by add task

        # send lw_item to bottom
        self.lw_task_list.takeItem(self.lw_task_list.row(task))  # take task item out of list
        len_completed_tasks = len([task for task in self.tasks if task.is_completed is False])
        self.lw_task_list.insertItem(len_completed_tasks if complete else 0,
                                     task)  # inserts item above completed tasks,
        # below uncompleted

        return True

    def _show_no_tasks(self, status: bool):
        if status:  # if True
            self.lw_task_list.hide()
            self.qframe_no_tasks.show()

        else:  # if False
            self.qframe_no_tasks.hide()
            self.lw_task_list.show()

    def _setup_qframe(self):
        # qframe
        self.qframe_no_tasks = QtWidgets.QFrame()
        self.qframe_no_tasks.setMinimumHeight(100)
        self.qframe_no_tasks.setStyleSheet("background-color: rgba(255, 223, 186, 1); border-radius: 10px")

        # qframe layout
        self.qframe_layout = QtWidgets.QVBoxLayout(self.qframe_no_tasks)
        label = QtWidgets.QLabel("No more tasks for you!!! Haha")
        self.qframe_layout.addWidget(label)

        # customize qlabel
        self.qframe_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("""
            font-family: 'Quicksand';
            color: rgba(255, 87, 34, 1);
            font-size: 16px;
            """)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    win = App()
    win.setStyleSheet("background-color: rgba(60, 60, 60, 1)")
    win.setMinimumSize(QtCore.QSize(100, 175))
    win.show()
    app.exec()
    pass
