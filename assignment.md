# ML Pipeline Framework

## Motivation

In XXXXXXX we need to run a lot of experiments that are not restricted to a single machine learning model but rather to a whole plethora of models working together to solve a given task.
To be effective we need a framework for building computational graphs in which it would be easy to combine several machine learning models together with the common goal which, for example, in the main case for XXXXXXX is to extract information from documents.  Having a declarative way to specify complex computational graphs, or so-called pipelines,  would help XXXXXXX tremendously to try a lot of different things in order to find out what works best.

## Task Description

Your goal is to design and implement a simple executor of a purely declarative specification of what we can refer to as a computational graph. The computation graph / pipeline definition should be a YAML file with a global key - pipeline . 

**A pipeline must have 4 properties:**

- name  - a human-readable description for the pipeline.
- inputs  - a list of strings defining the inputs into the pipeline.
- outputs  - a list of strings defining the outputs of the pipeline.
- components  - a dictionary of individual executable components (e.g. a ML model)

Every executable component (which can be looked at as a service, or a piece of function) should have its own name, input/output parameters specification, and a reference to the actual executable. The reference should be used to instantiate the actual callable, which should receive the inputs and provide the outputs.
Some components need to be executed after another, in that order! This fact should be reflected by  _dependencies_ property of a component, which would be a list specifying what components must be executed prior to this one. Dependencies do not necessarily need to be explicit. If an input is an output of another component, the component providing the input should be automatically considered as a dependency. 
The input and output parameters of a component must have their own names, which can be used for reference. Two components may have the same outputs, but the combination of a component’s name, and the input/output name must be unique. A parameter to a component without clear reference to a component is considered a pipeline input (it must be defined
though in order for the pipeline to be valid!)

Finally, when a pipeline is executed its parameters must be required on the input, otherwise it cannot be started.
The “pipeline executor CLI” to be implemented, should require the pipeline description file (in YAML) and optionally (if the pipeline has an input) the values for the input parameters. The input names can be used as options (or any other way that is suitable) to specify their values on the command line.
When a pipeline is executed, the program should simulate the execution of individual components. An execution order of the components must naturally follow the dependencies defined implicitly or explicitly in the pipeline’s structure. An implementation of a component’s logic should be encapsulated and should generate random values for output parameters. Only when the input value is directly passed to the output its value is of course not randomly generated. Please, implement at least one component that does pass through a value from an input to an output. The component’s logic (other than what was mentioned) should be a “no-op” and only print out a “log message” about its execution: stating a timestamp (execution order), the name of the component, the reference for the executed logic ( _runner_ in the example below), the input and the output names with their values.

## Example

An example ( pipeline.yaml ) of a simple pipeline - no branching - where one component feeds the next can be found below:

```
pipeline:
    - name: "My pretty fancy ML pipeline."
    - inputs:
    	- document_id
    	- page_num
    - outputs:
    	- extractions
    - components:
        - image_preprocessing:
            - runner: ImagePreprocessor
            - inputs:
                - document_id
                - page_num
            - outputs:
                - page_id
        - image_ocr:
            - runner: OCRModel
            - inputs:
                - image_preprocessing.page_id
            - outputs:
                - page_id
        - extractor:
            - runner: ExtractionModel
            - inputs:
                - image_ocr.page_id
            - outputs:
                - extractions
```

When the pipeline is executed by running  _pipeline_cli.py_ (CLI tool to be implemented), it should require values for  document ID and  page number , since these are the pipeline’s inputs.

Execution of the CLI may look like this:

```
./pipeline_cli.py --file pipeline.yaml --inputs document_id=D0
page_num=0
0 : pipeline : inputs - document_id=D0, page_num=0
1 : image_preprocessing - ImagePreprocessor : inputs -
document_id=D0, page_num=0 : outputs - page_id=P
2 : image_ocr - OCRModel : inputs - page_id=P0 : outputs -
page_id=OP
3 : extractor - ExtractionModel : inputs - page_id=OP0 : outputs
- extractions=E
4 : pipeline : outputs - extractions=E
```

And could print out the following pipeline execution log:

## Before you start

You should consider the example as an inspiration (template). You should implement the core features that are specified above, but everything else is up to your ingenuity. Please write clean, documented, and tested Python 3 code with proper naming conventions. Try avoiding any use of 3rd party packages. No such thing should be necessary. Along with your solution, provide a specification of 2 configurations that demonstrate that the implementation works for a non-trivial case of pipelines which contain multiple computation branches and at least one of them contains merge of outputs of multiple components together.
The assignment is a bit open ended, but the beauty of it is in finding out what’s in it to solve. To give you a hint what should be covered: we will test the robustness of the solution by reconnecting the components, switching dependencies, mistyping a name or a reference to input and/or component here and there to see how the CLI is going to respond.

