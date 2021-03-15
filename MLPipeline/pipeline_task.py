import inspect
import random
import time
from typing import List, Tuple

from MLPipeline.consumable import Consumable


class AbstractTask:
    """abstract class for all runners which are defined in pipeline_runners"""

    def __init__(
            self,
            name: str,
            input_consumables: List[str] = None,
            output_consumables: List[str] = None,
    ):

        if not input_consumables:
            self.input_consumables = []
        else:
            self.input_consumables = input_consumables

        if not output_consumables:
            self.output_consumables = []
        else:
            self.output_consumables = output_consumables

        self.name = name
        self.generated_outputs = []

    def execute(self, input_consumables: List[Consumable]):
        raise Exception("Executing of AbstractTask is not what you should do! Overload the execute method fist!")

    def fake_execute(self, input_consumables: List[Consumable]) -> List[Consumable]:
        """performs fake execution of the task"""
        task_result = []
        for output in self.output_consumables:
            new_content = f"{[c.full_name for c in input_consumables]}" \
                          f"->" \
                          f"{self.name}" \
                          f"->" \
                          f"{self.name}.{output}"
            task_result.append(Consumable(output, new_content, self.name))
        return task_result

    def dummy_executor(self, inputs: List[Consumable], key: str, duration: Tuple[int, int] = (1, 5)) -> None:
        """This is just dummy executor which i am gonna use in runners to make my work easier"""
        print(f'Starting execution of {self.name}')
        time.sleep(random.randint(*duration))
        result_should_be = ''.join([f"{i.content}" for i in inputs]) + f'-{key}'
        for i, consumable_name in enumerate(self.output_consumables):
            generated = Consumable(
                consumable_name,
                result_should_be + str(i),
                self.name
            )
            self.generated_outputs.append(generated)
        print(f'Ending execution of  {self.name}')


class TaskFactory:
    """factory for runners"""

    def __init__(self):
        import MLPipeline.pipeline_runners
        self.known_runners = {}

        # scan pipeline_runners for class objects which inherit from AbstractTask and add them to the dict
        for runner_name, runner_class in inspect.getmembers(MLPipeline.pipeline_runners, inspect.isclass):
            if issubclass(runner_class, AbstractTask):
                self.known_runners[runner_name] = runner_class

    def spawn_task(self, name, runner, inputs, outputs):
        if runner not in self.known_runners:
            raise UnknownRunnerError(runner)
        return self.known_runners[runner](name, inputs, outputs)


class DuplicateConsumableException(Exception):

    def __init__(self, consumable: Consumable, task: AbstractTask):
        super().__init__(f"ConsumableBox with name {consumable.name} already defined on task {task.name}")


class UnknownRunnerError(Exception):

    def __init__(self, runner_name: str):
        super().__init__(f"Runner with name {runner_name} not in DB!")
