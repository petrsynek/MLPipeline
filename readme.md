# MLPipeline 

This is simple project which mocks a workflow of machine-learning pipeline. Project is implemented in python 3.9 although I guess anything 3.7+ should be fine.

Project was created based on assignment in _assignment.md_ file. At beginning, I worked with structure of _.yaml_ as defined in assignment, however everything in the original yaml is list which is probably flawed. For purposes of tests and ease of pipeline assembly I switched to slightly more normal implementation later. Still, there are residuals of original implementation - components are still lists, and whole thing is just begging to be OrderedDict. 

I imagined pipeline as orchestrator of individual runners (tasks) which perform operations on datasets. As multiple task can run concurrently on the data I have implemented it as asynchronous scheduler. The abstract flow of the pipeline and alternative approaches are described lower.

This is realy like minimal version of the app. possible next steps what should be done are described in _To do (/nice to have)_ section
### Description

- App should take pipeline flow from .yaml file and inputs from command line.
- Check, if the declaration is correct, validate if it can finish.
- Execute and return results

### Guide

Before you start install requirements

```
pip install -r requirements.txt
```

Run pipeline principle demonstrator:
```
python async_pipeline_principle.py
```

Run client with assignment defined yaml:
```
python pipeline_cli.py --file pipeline_assignment.yaml --inputs document_id=D0 page_num=0 -b
```

Run client with simplified yaml:
```
python --file pipeline.yaml --inputs document_id=D0 page_num=0
```

Run unittests:
```
python -m unittest discover Tests
```

Run integration test:
```
python integration_test.py
```

### Files:

- **MLPipeline** - pipeline module
  - **consumable** - definition of data container
  - **pipeline** - definition of service class for pipeline
  - **pipeline_builder** - well... pipeline builder
  - **pipeline_task** - definition of abstract task method and task factory
  - **pipeline_runners** - definition of specific tasks - runners
  - **utils** - various utilities created for the project
- **Tests** - tests module
  - **tests** - some basic unittests
  - **utils** - fake pipeline constructor
- **async_pipeline_principle**.**py** - executable which demonstrate a simplified version of async pipeline run
- **pipeline_cli**.**py** - main executable as defined in requirements
- **requirements.txt** - requirements for project
- **.yaml** files - one as defined in the assignment with everything as list, other in ordinary human form
- **assignment.md** - assigment for the project

### Flow of execution

1. check tasks, if any of them have all required inputs defined (published),
2. mark task with valid inputs as running, execute it, publish outputs, move task to finished
3. check if global desired outputs are collected
4. repeat until the desired outputs are collected or no more tasks could be run

### Implementation options

- **synchronous** - as described in flow, will be just perfect to check if the pipeline is finite (executions will be faked)
- **asynchronous** - run all task with valid inputs, on-event of output generation check if precondition is met for other tasks (preferable if task duration ~< scheduler tick ) - *won't implement*
- **scheduled** - run all task with available inputs asynchronously by the scheduler, easy to solve situation if task freezes or times out (preferable if task duration > scheduler tick)

Will implement the scheduled version... sound more feasible for ML tasks.

### Vision

- tasks, pipelines - tables in a relational DB as foreign keys will come handy
- consumables - entries in no-sql DB/MQ

Overseer (pipeline runner in our case) - server which will start specific task services and execute pipeline
Worker (task in our case) - microservice which will be assigned to execute task

### Done

+ pipeline and methods
+ abstract task runner and methods
+ consumable model
+ pipeline builder
+ fake runner which checks validity of pipeline
+ client
+ implement basic flow
+ fix pipeline builder for normal style yaml (not only lists in yaml)
+ implement async
+ implement basic tests
+ implement generic graph tests (integration tests)

### To do (/nice to have):
- extend unittests coverage...
- exceptions fired when looking if all keys are present should be more specific
  - implement in is_subset_of to return missing keys
  - fix in calls
- for failed fake run print list of module:missing input
- clear the pipeline tasks that do not lead to desired output (backtrack from outputs to the inputs)
- implement task execution canceling, expiration, restart (async tasks running in the loop are accessible trough asyncio.Task.all_tasks())
- pipeline for integration tests is designed to converge, maybe add complex failing pipeline?

### Assignment Q/A:

- Inputs are defined in one place of assignment as list of strings while at same time being dict of strings (e.g. from command line, different outputs to **specific** output names)
- Pipeline definition of input yaml in project assignment is not well-made.