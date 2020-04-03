# MAGic MAchine Learning Tools (MagMaLT)

## Simple Machine Learning pipeline tools for Major Atmospheric Gamma Imaging Cherenkov Telescopes

The pipelines support following types of steps:

- Data loaders
- Transformers (preprocessing)
  - Scaling
  - Filters (Same syntax as in MARS)
- Models
- Transforms (postprocessing - e.g. reverse scaling, unbias)
- Metrics (Keras, etc.)
- Reports
- Data writter

All steps must implement fit/transform paradigm used in scikit-learn.

## Stages

A pipeline has three distinct stages:

### Initialization

In this stage the `initialize` method of all steps is called and prepare steps for execution.
The following operations should be performed here:

- Initialization of all parameters that need to be persisted, for a given step in the context
- For models - create model
- Features needed for a given step are appended to the dataset's `features`

### Exection

This stage executes `run` method of all steps.
Thus the `run` method should contain the main logic for each step.

### Finalization

This is the final stage of the execution. Steps should finalize their operation.
This stage executes `finalize` method for each step. This stage is **optional**.
Examples of some operations that should be performed in this stage:

- Perists models to a file
- Write training statistics history to a file

## Steps

Step is a part of the pipeline that has to be executed

### General
