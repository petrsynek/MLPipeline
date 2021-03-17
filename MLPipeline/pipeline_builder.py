from typing import List

import yaml

from MLPipeline.consumable import Consumable
from MLPipeline.pipeline import Pipeline
from MLPipeline.pipeline_task import TaskFactory
from MLPipeline.utils import is_subset_of


def list_of_dicts_to_dict(my_list: List[dict]) -> dict:
    """Voodoo magic which fixes weirdly defined yaml in assignment. In principle this should be easy,
     but if someone can't define dict in yaml, who knows what else will be there so I am double checking. """

    return {list(item.keys())[0]: item[list(item.keys())[0]]
            for item in my_list if type(item) is dict and len(list(item.keys())) == 1}


class PipelineParsingError(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class Builder:
    """Class for instantiating the pipeline:

    flow:
    1. instantiate
    2. load_yml
    3. pass_command_line_inputs
    4. build_pipeline to get Pipeline
    """

    def __init__(self):
        self.parsed_yaml = {}
        self.command_line_inputs = {}

    def load_yaml(self, filename: str) -> None:
        with open(filename) as yaml_file:
            self.parsed_yaml = yaml.load(yaml_file, Loader=yaml.FullLoader)

    def pass_command_line_inputs(self, command_line_inputs: dict) -> None:
        self.command_line_inputs.update(command_line_inputs)

    def build_pipeline(self, bad_yaml=False, verbose=True) -> Pipeline:
        """Definition of pipeline structure comes here...
        Implementing for one pipeline per yaml, could be easily extended.
        """

        if verbose:
            print("Building pipeline...")

        # check of the base level definition
        # if you made original yaml and you read this - look here https://en.wikipedia.org/wiki/YAML
        if self.parsed_yaml.get('pipeline'):
            if bad_yaml:
                pipeline_content = list_of_dicts_to_dict(self.parsed_yaml['pipeline'])
            else:
                pipeline_content = self.parsed_yaml['pipeline']
        else:
            raise PipelineParsingError("Missing pipeline definition.")

        if not is_subset_of(
                ['name', 'inputs', 'outputs', 'components'],
                list(pipeline_content.keys())
        ):
            raise PipelineParsingError("Pipeline missing key attributes.")

        pipeline = Pipeline(pipeline_content['name'])
        # now we have the pipeline lets start to feed it
        task_factory_instance = TaskFactory()
        for component in pipeline_content['components']:

            if len(component) != 1:
                raise PipelineParsingError(
                    "Component root should be list of dicts of length one with its component.name as a key!"
                )
            else:
                c_name = list(component.keys())[0]

            if bad_yaml:
                component_dict = list_of_dicts_to_dict(component[c_name])
            else:
                component_dict = component[c_name]
            # checking if task contain all required sections
            if not is_subset_of(['runner', 'inputs', 'outputs'], list(component_dict.keys())):
                raise PipelineParsingError(f'Component {c_name} missing one of the key arguments!')

            task_from_component = task_factory_instance.spawn_task(c_name, **component_dict)
            pipeline.add_task(task_from_component)

        # check if all pipeline inputs are declared on command line and add them one by one
        for pipeline_input in pipeline_content['inputs']:
            if pipeline_input in self.command_line_inputs:
                consumable_from_input = Consumable(pipeline_input, self.command_line_inputs[pipeline_input])
                pipeline.add_input(consumable_from_input)
            else:
                raise PipelineParsingError(
                    f"Pipeline declared input {pipeline_input} not found in command line inputs!")

        # this could be done in one shove, but there should be in principle CRUD
        # this way it would be easy to extend in future :)
        for pipeline_output in pipeline_content['outputs']:
            if pipeline_output not in pipeline.expected_outputs:
                pipeline.add_output(pipeline_output)

        return pipeline
