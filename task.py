"""
Contains the app's main logic
"""
import logging

# noinspection PyUnresolvedReferences
import logging_config


class Task:
    def __init__(self, title: str, is_completed: bool = False):
        self.title = title.strip().capitalize()
        self.is_completed = is_completed

    def change_completion_status(self, status: bool):
        self.is_completed = status
        logging.info("Marked as completed")

    def to_dict(self):
        """
        Converts Task instances to dictionaries
        Returns: Dictionary with title and is_completed keys

        """
        return {
            "title": self.title,
            "is_completed": self.is_completed
        }

    @staticmethod
    def from_dict(data: dict):
        """
        Converts dictionary data to Task class instance with title and completion status
        Args:
            data: list containing dictionaries

        Returns: Task instance

        """
        return Task(
            title=data.get("title"),
            is_completed=data.get("is_completed")
        )

    def check_task_title_length(self):
        if len(self.title.strip()) == 0:
            return False
        return True


if __name__ == "__main__":
    pass
