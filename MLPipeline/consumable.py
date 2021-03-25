class Consumable:
    """Container which acts as carrier of the inputs/outputs (model for DB)"""

    def __init__(self, name: str, content: str, parent_task_name: str = ''):
        self.content = content
        self.name = name
        self.parent_task_name = parent_task_name

    @property
    def full_name(self) -> str:
        """returns Consumable name along with name of task that spawned it in format task_name.consumable_name"""
        if self.parent_task_name:
            return f"{self.parent_task_name}.{self.name}"
        else:
            return self.name
