from typing import List


class PipelineExecError(Exception):
    """Raised when the input value is too small"""
    pass


class Pipe:
    """Single Pipe to process a list of objects"""
    def __init__(self, model_class):
        self.model_class = model_class

    def run(self, l: List["self.model_class"]) -> List["self.model_class"]:
        raise NotImplementedError


class Pipeline(list):
    """Funnel list"""
    def __init__(self, funnels: List[Pipe] = [], *args, **kwargs):
        self.funnels = funnels
        if self.__pipeline_is_valid():
            super(Pipeline, self).__init__(funnels)
        else:
            raise PipelineExecError("All funnels should have the same "
                                      "Model Class!")

    def __pipe_is_valid(self, funnel: Pipe) -> None:
        """
        Validate if funnel can be part of pipeline
        A funnel is valid only if its model_class is the same as the other
        funnels in the list unless the list is empty
        :param funnel: Funnel
        :return: None
        """

        if self:
            return self[0].model_class == funnel.model_class
        else:
            return True

    def __pipeline_is_valid(self) -> None:
        """
        Validate the pipeline
        confirm that the pipeline is empty or that all funnels have the same
        model_class
        :return:
        """

        return len(set([f.model_class for f in self.funnels])) in [0, 1]

    def insert(self, index: int, funnel: Pipe) -> None:
        """
        Add a funnel to the pipeline
        :param index: position index in pipeline
        :param funnel: funnel
        :return: None
        """

        if self.__pipe_is_valid(funnel):
            super(Pipeline, self).insert(index, funnel)
        else:
            raise PipelineExecError("This funnel Model Class is different "
                                      "than the others already in the "
                                      "pipeline!")

    def append(self, funnel: Pipe) -> None:
        """
        Add funnel at the end of the pipeline
        :param funnel:
        :return: None
        """

        if self.__pipe_is_valid(funnel):
            super(Pipeline, self).append(funnel)
        else:
            raise PipelineExecError("This funnel Model Class is different "
                                      "than the others already in the "
                                      "pipeline!")

    def pop(self, index: int = -1) -> Pipe:
        """
        Remove a funnel at specified index
        :param index: index in pipeline
        :return: removed funnel
        """
        super(Pipeline, self).pop(index)

    def run(self, input_list: List) -> List:
        """
        Run the whole pipeline
        :param input_list: model instances list
        :return: runed model instances list
        """

        if len(self) == 0:
            raise PipelineExecError("No funnel in pipeline!")
        else:
            ret = self[0].run(input_list)
            for pipe in self[1:]:
                ret = pipe.run(ret)
        return ret
