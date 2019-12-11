# sikifunnels

## About
Sikifunnel is a Funnel Pipeline to apply to  an Object Collection. It's like a
group of fonction to run on a list of objects.

## Installation
Just run:
```
  pip install -U sikifunnels
```
## Usage
You need to create a pipeline and add a few funnels to it:

```python
from sikifunnels.funnel import Funnel, FunnelPipeline

# creating our funnels
class MyTestFunnelPlusOne(Funnel):
    def filter(self, l):
        return [i + 1 for i in l]


class MyTestFunnelPlusTwo(Funnel):
    def filter(self, l):
        return [i + 2 for i in l]


class MyTestFunnelMinusOne(Funnel):
    def filter(self, l):
        return [i - 1 for i in l]

# creating our pipeline
pipeline = FunnelPipeline([MyTestFunnelPlusOne(), MyTestFunnelPlusTwo(), MyTestFunnelMinusOne()])

# run the pipeline
pipeline.run([1, 1, 1]) # returns [3, 3, 3]
```

## Contribute
