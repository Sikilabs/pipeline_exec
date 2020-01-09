from typing import List


class PipelineExecError(Exception):
    """Base Error"""
    pass


class Pipe:
    """Single Pipe to process a list of objects"""
    def __init__(self, model_class):
        self.model_class = model_class

    def run(self, l: List["self.model_class"]) -> List["self.model_class"]:
        raise NotImplementedError


class Pipeline(list):
    """Pipe list"""
    def __init__(self, pipes: List[Pipe] = [], *args, **kwargs):
        self.pipes = pipes
        if self.__pipeline_is_valid():
            super(Pipeline, self).__init__(pipes)
        else:
            raise PipelineExecError("All pipes should have the same "
                                      "Model Class!")

    def __pipe_is_valid(self, pipe: Pipe) -> None:
        """
        Validate if pipe can be part of pipeline
        A pipe is valid only if its model_class is the same as the other
        pipes in the list unless the list is empty
        :param pipe: Pipe
        :return: None
        """

        if self:
            return self[0].model_class == pipe.model_class
        else:
            return True

    def __pipeline_is_valid(self) -> None:
        """
        Validate the pipeline
        confirm that the pipeline is empty or that all pipes have the same
        model_class
        :return:
        """

        return len(set([f.model_class for f in self.pipes])) in [0, 1]

    def insert(self, index: int, pipe: Pipe) -> None:
        """
        Add a pipe to the pipeline
        :param index: position index in pipeline
        :param pipe: pipe
        :return: None
        """

        if self.__pipe_is_valid(pipe):
            super(Pipeline, self).insert(index, pipe)
        else:
            raise PipelineExecError("This pipe Model Class is different "
                                    "than the others already in the "
                                    "pipeline!")

    def append(self, pipe: Pipe) -> None:
        """
        Add pipe at the end of the pipeline
        :param pipe:
        :return: None
        """

        if self.__pipe_is_valid(pipe):
            super(Pipeline, self).append(pipe)
        else:
            raise PipelineExecError("This pipe Model Class is different "
                                    "than the others already in the "
                                    "pipeline!")

    def pop(self, index: int = -1) -> Pipe:
        """
        Remove a pipe at specified index
        :param index: index in pipeline
        :return: removed pipe
        """
        super(Pipeline, self).pop(index)

    def run(self, input_list: List) -> List:
        """
        Run the whole pipeline
        :param input_list: model instances list
        :return: runed model instances list
        """

        if len(self) == 0:
            raise PipelineExecError("No pipe in pipeline!")
        else:
            ret = self[0].run(input_list)
            for pipe in self[1:]:
                ret = pipe.run(ret)
        return ret
