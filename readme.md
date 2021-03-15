### Files:

- **MLPipeline** - pipeline module
  - **consumable** - definition of data container
  - **pipeline** - definition of service class for pipeline
  - **pipeline_builder** - well... pipeline builder
  - **pipeline_task** - definition of abstract task method and task factory
  - **pipeline_runners** - definition of specific tasks - runners
  - **utils** - various utilities created for the project

- **async_pipeline_principle**.**py** - executable which demonstrate a simplified version of async pipeline run
- **pipeline_cli**.**py** - main executable as defined in requirements
- **requirements.txt** - requirements for project, no, I am not going to implement yaml parser, sorry guys
- **.yaml** files - one as defined in the assignment with everything as list 'sigh', other in ordinary human form 

### Description

- App should take pipeline flow from .yaml file and inputs from command line.
- Check, if the declaration is correct, validate if it can finish.
- Execute and return results

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

### To do:

- implement generic graph tests
- exceptions fired when looking if all keys are present should be more specific
  - implement in is_subset_of to return missing keys
  - fix in calls
- for failed fake run print list of module:missing input
- clear the pipeline tasks that do not lead to desired output (backtrack from outputs to the inputs)

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


### Assignment Q/A:

- Inputs are defined in one place of assignment as list of strings while at same time being dict of strings (e.g. from command line, different outputs to **specific** output names)
- Pipeline definition of input yaml in project assignment is crap. Everything is list, even if it is obviously dict. Implementation of code which mends this, cost me seconds of my life which won't come back. I almost dropped this fun project, because you know... who does this?
- I used 3rd party library which is yaml for yaml parsing, I am not going to reinvent the wheel.
- Making my own pipeline was fun, but you know that it is bad idea, don't you? There are like a bazillion of project which, if not perfectly fitting, you can fork. 