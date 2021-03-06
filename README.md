# pipeline-exec

##  Status
### unstable ![](https://github.com/Sikilabs/pipeline_exec/workflows/tests/badge.svg?branch=develop)
### stable ![](https://github.com/Sikilabs/pipeline_exec/workflows/tests/badge.svg?branch=master)
### Pypi [![PyPI version](https://badge.fury.io/py/pipeline-exec.svg)](https://badge.fury.io/py/pipeline-exec)

## About
*pipeline-exec* is an execution Pipeline to apply to an Object Collection. It's like a group of functions to run against 
a list of objects on a sequential manner. The original goal behind this project was to implement a framework to help 
create a funnel pipeline for Django model instances. We're sure there can be many more uses. 

## Installation
Just run:
```
  pip install -U pipeline-exec
```

## Usage
You need to create a pipeline and add a few Pipes to it:

```python
from pipeline_exec.pipeline import Pipe, Pipeline

# creating our funnels
class MyTestPipePlusOne(Pipe):
    def run(self, l):
        return [i + 1 for i in l]


class MyTestPipePlusTwo(Pipe):
    def run(self, l):
        return [i + 2 for i in l]


class MyTestPipeMinusOne(Pipe):
    def run(self, l):
        return [i - 1 for i in l]

# creating our pipeline
pipeline = Pipeline([MyTestPipePlusOne(), MyTestPipePlusTwo(), MyTestPipeMinusOne()])

# run the pipeline
pipeline.run([1, 1, 1]) # returns [3, 3, 3]
```

## Contribute
For now, it's very straight forward. Everyone is welcome to contribute. All pull requests are against the develop branch.
Unit tests and the flake8 linter run at every push.
Thanks in advance for your contribution :)
