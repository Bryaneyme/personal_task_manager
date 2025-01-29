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
	x.	Error Notifications:
	•	x If I try to add an empty task, a popup error message appears, preventing the task from being added.
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
        self.completed_tasks = []
        self.pending_tasks = []
        self.tasks = []
        self.load_tasks(is_completed=True)
        self.load_tasks(is_completed=False)
        self.setup_ui_2()
        self.setWindowTitle("Task manager")
        self.setMinimumSize(QtCore.QSize(1080, 720))
        # self.setup_connections()
        self.populate_tasks()

        # connect
        self.btn_add_task.clicked.connect(self.add_task)
        self.le_input_field.returnPressed.connect(self.add_task)

        self.lw_pending.itemClicked.connect(self.set_focus_to_card)
        self.lw_pending.installEventFilter(self)
        self.lw_pending.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)

        self.lw_completed.itemClicked.connect(self.set_focus_to_card)
        self.lw_completed.installEventFilter(self)
        self.lw_completed.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)

        # testing

    def load_tasks(self, all_tasks: bool = True, is_completed: bool = False):
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

        if not is_completed:
            self.pending_tasks = [Task.from_dict(item) for item in content if
                                  Task.from_dict(item).is_completed is False]
            print(f"uncompleted: {self.pending_tasks}")
        if is_completed:
            self.completed_tasks = [Task.from_dict(item) for item in content if
                                    Task.from_dict(item).is_completed is True]
            print(f"completed: {self.completed_tasks}")

        self.tasks = self.pending_tasks + self.completed_tasks
        print(f"all: {self.tasks}")

    def setup_ui_2(self):
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(16, 0, 16, 0)

        # ---------------------------TOP NAVIGATION BAR---------------------------#
        self.qframe_navigation_bar = QtWidgets.QFrame()
        self.qframe_navigation_bar.setFixedHeight(80)

        # horizontal layout
        self.layout_navigation_bar = QtWidgets.QHBoxLayout(self.qframe_navigation_bar)
        self.layout_navigation_bar.setContentsMargins(0, 0, 0, 0)

        # QLabel for title
        self.qlabel_title = QtWidgets.QLabel("Task Manager")
        self.qlabel_title.setStyleSheet("""
        QLabel {
        font-size: 24px;
        font-weight: 700;
        color: #E0E0E0;
        }
        """)

        # QPushButton to add task
        self.btn_add_task = QtWidgets.QPushButton("+")
        self.btn_add_task.setFixedSize(40, 40)
        self.btn_add_task.setStyleSheet("""
        QPushButton {
        background-color: #BB86FC;
        border-radius: 20px;
        font-size: 24px;
        text-align: center;
        color: #E0E0E0 
        }
        """)

        # add widgets to sub-layout
        self.layout_navigation_bar.addWidget(self.qlabel_title)
        self.layout_navigation_bar.addWidget(self.btn_add_task)

        # ---------------------------TASK INPUT SECTION---------------------------#
        self.le_input_field = QtWidgets.QLineEdit()
        self.le_input_field.setFixedHeight(40)
        self.le_input_field.setPlaceholderText("Enter new task...")
        self.le_input_field.setStyleSheet("""
        QLineEdit {
        border-radius: 8px;
        padding: 8px;
        font-size: 16px;
        font-weight 400;
        color: #E0E0E0;
        background-color: #1E1E1E
        }
        """)

        # ---------------------------TASK-HEADERS-SECTION---------------------------#
        self.qframe_list_headers = QtWidgets.QFrame()
        self.qframe_list_headers.setStyleSheet("""
        QFrame {
        font-size: 18px;
        font-weight: 700;
        margin-top: 24px;
        color: #E0E0E0 
        }
        """)

        # horizontal layout
        self.layout_list_headers = QtWidgets.QHBoxLayout(self.qframe_list_headers)
        self.layout_list_headers.setContentsMargins(0, 0, 0, 0)

        # QLabel for tasks
        self.text_header_pending = QtWidgets.QLabel("Pending tasks")
        self.text_header_pending.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.text_header_completed = QtWidgets.QLabel("Completed Tasks")
        self.text_header_completed.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # add widgets to sub-layout
        self.layout_list_headers.addWidget(self.text_header_pending)
        self.layout_list_headers.addWidget(self.text_header_completed)
        # ---------------------------TASK LIST SECTION---------------------------#
        self.qframe_list_widgets = QtWidgets.QFrame()

        # horizontal layout
        self.layout_list_widgets = QtWidgets.QHBoxLayout(self.qframe_list_widgets)
        self.layout_list_widgets.setContentsMargins(0, 0, 0, 0)

        # QListWidget for pending tasks
        self.lw_pending = QtWidgets.QListWidget()
        self.lw_pending.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        self.lw_pending.setObjectName("lw_pending")
        self.lw_pending.setStyleSheet("""
        QListWidget {
        background-color: #121212;
        border: 0px solid;
        }2
        QListWidget::item {
        margin-bottom: 10px;
        }
        QListWidget::item:selected {
        #background-color: rgba(0, 0, 0, 0)
        }
        """)

        # QListWidget for completed tasks
        self.lw_completed = QtWidgets.QListWidget()
        self.lw_completed.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        self.lw_completed.setObjectName("lw_completed")
        self.lw_completed.setStyleSheet("""
        QListWidget {
        background-color: #121212;
        border: 0px solid;
        }
        QListWidget::item:selected {
        background-color: rgba(0, 0, 0, 0)
        }
        """)

        # add widgets to sub-layout
        self.layout_list_widgets.addWidget(self.lw_pending)
        self.layout_list_widgets.addWidget(self.lw_completed)

        # ---------------------------Add widgets to main-layout---------------------------
        self.layout.addWidget(self.qframe_navigation_bar)
        self.layout.addWidget(self.le_input_field)
        self.layout.addWidget(self.qframe_list_headers)
        self.layout.addWidget(self.qframe_list_widgets)

    def setup_task_card(self, title: str, is_completed: bool = False, selected: bool = False):
        self.qframe_task_card = QtWidgets.QFrame()
        # self.qframe_task_card.setFixedHeight(60)  # Need to expand according to size change. 100% of container
        self.qframe_task_card.setContentsMargins(0, 0, 0, 0)
        self.qframe_task_card.setStyleSheet("""
        QFrame {
        color: #E0E0E0;
        border-radius: 12px;
        background-color: #1E1E1E;
        border: 2px solid #333333;
        }
        """)

        if selected:
            self.qframe_task_card.setStyleSheet("""
            QFrame {
            color: #E0E0E0;
            border-radius: 12px;
            background-color: #2A2A2A;
            border: 2px solid #BB86FC;
            }
            """)

        self.layout_task_card = QtWidgets.QHBoxLayout(self.qframe_task_card)

        # QLabel card title
        self.qlabel_task_card_title = QtWidgets.QLabel(title)
        self.qlabel_task_card_title.setMaximumWidth(420)
        self.qlabel_task_card_title.setWordWrap(True)
        self.qlabel_task_card_title.setStyleSheet("""
        QLabel {
        font-size: 16px;
        font-weight: 500;
        border: 0px solid rgba(0, 0, 0, 0);
        }
        """)

        # QPushButton mark as complete
        self.btn_change_completion_status = QtWidgets.QPushButton("DONE" if is_completed is False else "UN-DONE")
        self.btn_change_completion_status.setFixedSize(75, 30)
        if is_completed is False:
            self.btn_change_completion_status.setStyleSheet("""
            QPushButton {
            background-color: #4CAF50;
            border: 1px solid #66BB6A;
            border-radius: 15px;
            color: #FFFFFF;
            }
            QPushButton::hover {
            background-color: #388E3C;
            }
            """)

        elif is_completed is True:
            self.btn_change_completion_status.setStyleSheet("""
            QPushButton {
            background-color: rgba(0, 0, 0, 0);
            border: 1px solid #66BB6A;
            border-radius: 15px;
            color: #4CAF50;
            }
            QPushButton::hover {
            background-color: #2A2A2A;
            }
            """)
        self.btn_change_completion_status.clicked.connect(self.change_completion_status)

        # QPushButton edit task title
        self.btn_edit_task = QtWidgets.QPushButton("EDIT")
        self.btn_edit_task.setFixedSize(75, 30)
        self.btn_edit_task.setStyleSheet("""
        QPushButton {
        background-color: #FFC107;
        border: 1px solid #FFCA28;
        border-radius: 15px;
        color: #FFFFFF;
        }
        QPushButton::hover {
        background-color: #FFB300;
        }
        """)

        # QPushButton delete task
        self.btn_delete_task = QtWidgets.QPushButton("DELETE")
        self.btn_delete_task.setFixedSize(75, 30)
        self.btn_delete_task.setStyleSheet("""
        QPushButton {
        background-color: #D32F2F;
        border: 1px solid #FF5252;
        border-radius: 15px;
        color: #FFFFFF
        }
        QPushButton::hover {
        background-color: #B71C1C;
        }
        """)

        self.btn_delete_task.clicked.connect(self.delete_task)

        # add widgets to sub-layout
        self.layout_task_card.addWidget(self.qlabel_task_card_title)
        self.layout_task_card.addWidget(self.btn_change_completion_status)
        self.layout_task_card.addWidget(self.btn_edit_task)
        self.layout_task_card.addWidget(self.btn_delete_task)

        return self.qframe_task_card

    def setup_connections(self):
        self.btn_change_completion_status.clicked.connect(self.change_completion_status)

        logging.info("Connections completed")
        return True

    def populate_tasks(self):
        for task in self.pending_tasks:
            self._to_lw_item(task, self.lw_pending)

        for task in self.completed_tasks:
            self._to_lw_item(task, self.lw_completed)

        # if not self.tasks:
        #     self._show_no_tasks(True)

        logging.info("LIST WIDGET - Tasks populated")

        return True

    def set_focus_to_card(self, lw_item: QListWidgetItem):
        # reset previous items selected
        self.reset_focus_to_cards(lw_item.listWidget())

        # for each item selected: change their appearance
        for item in lw_item.listWidget().selectedItems():
            item_data = item.data(QtCore.Qt.ItemDataRole.UserRole)
            item.listWidget().setItemWidget(item, self.setup_task_card(item_data.title, item_data.is_completed, True))
            print(item_data.title)

    def reset_focus_to_cards(self, list_widget: QtWidgets.QListWidget):
        for index in range(list_widget.count()):
            item = list_widget.item(index)
            item_class_object = item.data(QtCore.Qt.ItemDataRole.UserRole)
            list_widget.setItemWidget(item,
                                      self.setup_task_card(item_class_object.title, item_class_object.is_completed))

    def change_completion_status(self):
        # get which lw has focus
        if self.lw_pending.hasFocus():
            list_widget_a = self.lw_pending
            list_widget_b = self.lw_completed
            change_completion_status_to = True
        elif self.lw_completed.hasFocus():
            list_widget_a = self.lw_completed
            list_widget_b = self.lw_pending
            change_completion_status_to = False
        else:
            logging.warning("Completion status change - failed")
            return False

        lw_items = list_widget_a.selectedItems()

        for item in lw_items:
            class_item: Task = item.data(QtCore.Qt.ItemDataRole.UserRole)

            # delete item from list A
            row = list_widget_a.row(item)
            list_widget_a.takeItem(row)
            logging.info(f"Deleted item from {list_widget_a.objectName()}")

            # change completion status
            logging.debug(f"class item is_completed: {class_item.is_completed}")
            class_item.change_completion_status(change_completion_status_to)
            logging.debug(f"class item is_completed: {class_item.is_completed}")

            # add item to list B
            list_widget_b.insertItem(0, item)
            logging.info(f"Added: {class_item.title} to {list_widget_b.objectName()}")

            # apply card to lw_item
            list_widget_b.setItemWidget(item, self.setup_task_card(class_item.title, class_item.is_completed))

        self.save_tasks()
        return True

    def add_task(self):
        task = Task(self.le_input_field.text())
        task_titles = [task.title for task in self.tasks]
        if task.title in task_titles:
            logging.warning("Cannot have two tasks with the same title.")
            # come back: error
            self._show_le_error(True, "Cannot have two tasks with the same title")
            self.le_input_field.setText("")
            return False
        if not task.check_task_title_length():
            logging.warning("Task title must not be empty")
            # come back: error
            self._show_le_error(True, "Task title must not be empty")
            return False

        self._show_le_error(False)

        self.tasks.append(task)

        lw_task = self._to_lw_item(task, self.lw_pending)
        self.lw_pending.addItem(lw_task)
        self.lw_pending.setItemWidget(lw_task, self.setup_task_card(task.title, task.is_completed))

        # self._show_no_tasks(False)
        self.le_input_field.setText("")
        self.save_tasks()

        logging.info("Added task")

        return True

    def delete_task(self):
        print("deelete task function")
        if self.lw_pending.hasFocus():
            list_widget = self.lw_pending
            class_object_list = [task.data(QtCore.Qt.UserRole) for task in list_widget.selectedItems()]
        elif self.lw_completed.hasFocus():
            list_widget = self.lw_completed
            class_object_list = [task.data(QtCore.Qt.UserRole) for task in list_widget.selectedItems()]
        else:
            return False

        list_widget_item_list = list_widget.selectedItems()

        # remove task from app tasks list
        for class_object in class_object_list:
            print(class_object.title)
            self.tasks.remove(class_object)
            logging.info(f"Removed {class_object.title} - self.tasks")

        # remove task from list widget
        for list_widget_item in list_widget_item_list:
            row = list_widget.row(list_widget_item)
            list_widget.takeItem(row)
            logging.info(f"Removed {list_widget_item.text()} - list widget")

        self.save_tasks()
        logging.info("Deleted task")

        # if not self.tasks:
        #     self._show_no_tasks(True)

        return True

    def save_tasks(self):
        # take tasks attribute info | convert to dict | overwrite json file
        task_dict_list = [Task.to_dict(task_object) for task_object in self.tasks]

        with open(JSON_FILE_PATH, 'w') as json_file:
            json.dump(task_dict_list, json_file, indent=4)
            logging.info("JSON - Tasks saved")

        return True

    def eventFilter(self, watched, event: QKeyEvent):
        """
        Change keybindings in-app
        Args:
            watched: QObject being focused on
            event: What is happening? Key being pressed? Mouse being clicked?

        Returns: True if specific action has been detected. Otherwise, hands the actions to widgets.

        """
        if watched in [self.lw_pending, self.lw_completed]:
            watched: QtWidgets.QListWidget
            if event.type() == QtCore.QEvent.KeyPress:
                if event.key() == QtCore.Qt.Key_Backspace:
                    self.delete_task()
                    return True
                # if event.key() == QtCore.Qt.Key.Key_Return:
                #     self.change_completion_status()
                #     return True
            if event.type() == QtCore.QEvent.Type.FocusOut:
                print('focus out')
                self.reset_focus_to_cards(watched)
                watched.clearFocus()
                return True

        return super().eventFilter(watched, event)

    def _show_le_error(self, show: bool, error_reason: str = ""):
        if show:
            self.le_input_field.setPlaceholderText(error_reason)
            self.le_input_field.setStyleSheet("""
                QLineEdit {
                border-radius: 8px;
                padding: 8px;
                font-size: 16px;
                font-weight 400;
                color: #757575;
                background-color: #1E1E1E;
                border: 1px solid #FF5252;
                }
                """)
        if not show:
            self.le_input_field.setPlaceholderText("Enter the task name here")
            self.le_input_field.setStyleSheet("""
                QLineEdit {
                border-radius: 8px;
                padding: 8px;
                font-size: 16px;
                font-weight 400;
                color: #E0E0E0;
                background-color: #1E1E1E
                }
                """)

    def _to_lw_item(self, task: Task, task_list: QtWidgets.QListWidget) -> QtWidgets.QListWidgetItem:
        lw_item = QtWidgets.QListWidgetItem()
        lw_item.setData(QtCore.Qt.UserRole, task)
        task_list.addItem(lw_item)

        task_card = self.setup_task_card(task.title, task.is_completed)
        task_list.setItemWidget(lw_item, task_card)

        lw_item.setSizeHint(QtCore.QSize(600, 76))

        return lw_item

    def _convert_selected_items_to_class_object_list(self, is_completed: bool) -> list[Task]:
        if not is_completed:
            pending_selected_tasks = self.lw_pending.selectedItems()
            return [task.data(QtCore.Qt.UserRole) for task in pending_selected_tasks]

        completed_selected_tasks = self.lw_completed.selectedItems()
        return [task.data(QtCore.Qt.UserRole) for task in completed_selected_tasks]

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
    win.setStyleSheet("""
    background-color: #121212;
    font-family: 'Roboto';
    """)
    win.show()
    app.exec()
    pass
