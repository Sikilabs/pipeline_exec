import unittest
from pipeline_exec.pipeline import Pipe, Pipeline, PipelineExecError


class MyTestFunnelPlusOne(Pipe):
    def filter(self, l):
        return [i + 1 for i in l]


class MyTestFunnelPlusTwo(Pipe):
    def filter(self, l):
        return [i + 2 for i in l]


class MyTestFunnelMinusOne(Pipe):
    def filter(self, l):
        return [i - 1 for i in l]


class MyTestFunnelConcatA(Pipe):
    def filter(self, l):
        return [i + "A" for i in l]


class TestFunnel(unittest.TestCase):
    def setUp(self) -> None:
        self.funnel = Pipe(int)
        self.funnel_plus_one = MyTestFunnelPlusOne(int)

    def test_filter_exception(self):
        self.assertRaises(NotImplementedError, self.funnel.filter, [1, 1, 1])

    def test_filter(self):
        self.assertEqual(self.funnel_plus_one.filter([1, 1, 1]), [2, 2, 2])


class TestFunnelPipeline(unittest.TestCase):
    def setUp(self) -> None:
        self.funnel_plus_one = MyTestFunnelPlusOne(int)
        self.funnel_plus_two = MyTestFunnelPlusTwo(int)
        self.funnel_minus_one = MyTestFunnelMinusOne(int)
        self.funnel_concat_A = MyTestFunnelConcatA(str)

    def test_create(self):
        self.assertRaises(PipelineExecError, Pipeline,
                          [self.funnel_plus_one,
                           self.funnel_concat_A])
        pipeline = Pipeline([self.funnel_plus_one, self.funnel_plus_two])
        self.assertListEqual(pipeline,
                             [self.funnel_plus_one, self.funnel_plus_two])

    def test_append(self):
        pipeline = Pipeline()
        pipeline.append(self.funnel_plus_two)
        pipeline.append(self.funnel_plus_one)
        self.assertListEqual(pipeline,
                             [self.funnel_plus_two, self.funnel_plus_one])
        self.assertRaises(PipelineExecError, pipeline.append,
                          self.funnel_concat_A)

    def test_insert(self):
        pipeline = Pipeline([self.funnel_plus_two, self.funnel_plus_one])
        self.assertRaises(PipelineExecError, pipeline.insert, 1,
                          self.funnel_concat_A)
        pipeline.insert(1, self.funnel_minus_one)
        self.assertListEqual(pipeline,
                             [self.funnel_plus_two, self.funnel_minus_one,
                              self.funnel_plus_one])

    def test_pop(self):
        pipeline = Pipeline([self.funnel_plus_two, self.funnel_minus_one,
                                   self.funnel_plus_one])
        pipeline.pop(1)
        self.assertEqual(pipeline,
                         [self.funnel_plus_two, self.funnel_plus_one])
        pipeline.pop()
        self.assertEqual(pipeline, [self.funnel_plus_two])

    def test_run(self):
        pipeline_1 = Pipeline(
            [self.funnel_plus_two, self.funnel_minus_one,
             self.funnel_plus_one])
        self.assertEqual(pipeline_1.run([1, 1, 1]), [3, 3, 3])
        pipeline_2 = Pipeline(
            [self.funnel_plus_two, self.funnel_minus_one,
             self.funnel_minus_one])
        self.assertEqual(pipeline_2.run([1, 1, 1]), [1, 1, 1])
        pipeline_2 = Pipeline([self.funnel_concat_A])
        self.assertEqual(pipeline_2.run(['Z', 'Z', 'Z']), ['ZA', 'ZA', 'ZA'])
