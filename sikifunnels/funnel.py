from typing import List


class FunnelPipelineError(Exception):
    """Raised when the input value is too small"""
    pass


class Funnel:
    """Single funnel to filter on a list of objects"""
    def __init__(self, model_class):
        self.model_class = model_class

    def filter(self, l: List["self.model_class"]) -> List["self.model_class"]:
        raise NotImplementedError


class FunnelPipeline(list):
    """Funnel list"""
    def __init__(self, funnels: List[Funnel] = [], *args, **kwargs):
        self.funnels = funnels
        if self.__pipeline_is_valid():
            super(FunnelPipeline, self).__init__(funnels)
        else:
            raise FunnelPipelineError("All funnels should have the same "
                                      "Model Class!")

    def __funnel_is_valid(self, funnel: Funnel) -> None:
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

    def insert(self, index: int, funnel: Funnel) -> None:
        """
        Add a funnel to the pipeline
        :param index: position index in pipeline
        :param funnel: funnel
        :return: None
        """

        if self.__funnel_is_valid(funnel):
            super(FunnelPipeline, self).insert(index, funnel)
        else:
            raise FunnelPipelineError("This funnel Model Class is different "
                                      "than the others already in the "
                                      "pipeline!")

    def append(self, funnel: Funnel) -> None:
        """
        Add funnel at the end of the pipeline
        :param funnel:
        :return: None
        """

        if self.__funnel_is_valid(funnel):
            super(FunnelPipeline, self).append(funnel)
        else:
            raise FunnelPipelineError("This funnel Model Class is different "
                                      "than the others already in the "
                                      "pipeline!")

    def pop(self, index: int = -1) -> Funnel:
        """
        Remove a funnel at specified index
        :param index: index in pipeline
        :return: removed funnel
        """
        super(FunnelPipeline, self).pop(index)

    def run(self, input_list: List) -> List:
        """
        Run the whole pipeline
        :param input_list: model instances list
        :return: filtered model instances list
        """

        if len(self) == 0:
            raise FunnelPipelineError("No funnel in pipeline!")
        else:
            ret = self[0].filter(input_list)
            for funnel in self[1:]:
                ret = funnel.filter(ret)
        return ret
