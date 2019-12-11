import unittest
from sikifunnels.funnel import Funnel, FunnelPipeline, FunnelPipelineError


class MyTestFunnelPlusOne(Funnel):
    def filter(self, l):
        return [i + 1 for i in l]


class MyTestFunnelPlusTwo(Funnel):
    def filter(self, l):
        return [i + 2 for i in l]


class MyTestFunnelMinusOne(Funnel):
    def filter(self, l):
        return [i - 1 for i in l]


class MyTestFunnelConcatA(Funnel):
    def filter(self, l):
        return [i + "A" for i in l]


class TestFunnel(unittest.TestCase):
    def setUp(self) -> None:
        self.funnel = Funnel(int)
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
        self.assertRaises(FunnelPipelineError, FunnelPipeline,
                          [self.funnel_plus_one,
                           self.funnel_concat_A])
        pipeline = FunnelPipeline([self.funnel_plus_one, self.funnel_plus_two])
        self.assertListEqual(pipeline,
                             [self.funnel_plus_one, self.funnel_plus_two])

    def test_append(self):
        pipeline = FunnelPipeline()
        pipeline.append(self.funnel_plus_two)
        pipeline.append(self.funnel_plus_one)
        self.assertListEqual(pipeline,
                             [self.funnel_plus_two, self.funnel_plus_one])
        self.assertRaises(FunnelPipelineError, pipeline.append,
                          self.funnel_concat_A)

    def test_insert(self):
        pipeline = FunnelPipeline([self.funnel_plus_two, self.funnel_plus_one])
        self.assertRaises(FunnelPipelineError, pipeline.insert, 1,
                          self.funnel_concat_A)
        pipeline.insert(1, self.funnel_minus_one)
        self.assertListEqual(pipeline,
                             [self.funnel_plus_two, self.funnel_minus_one,
                              self.funnel_plus_one])

    def test_pop(self):
        pipeline = FunnelPipeline([self.funnel_plus_two, self.funnel_minus_one,
                                   self.funnel_plus_one])
        pipeline.pop(1)
        self.assertEqual(pipeline,
                         [self.funnel_plus_two, self.funnel_plus_one])
        pipeline.pop()
        self.assertEqual(pipeline, [self.funnel_plus_two])

    def test_run(self):
        pipeline_1 = FunnelPipeline(
            [self.funnel_plus_two, self.funnel_minus_one,
             self.funnel_plus_one])
        self.assertEqual(pipeline_1.run([1, 1, 1]), [3, 3, 3])
        pipeline_2 = FunnelPipeline(
            [self.funnel_plus_two, self.funnel_minus_one,
             self.funnel_minus_one])
        self.assertEqual(pipeline_2.run([1, 1, 1]), [1, 1, 1])
        pipeline_2 = FunnelPipeline([self.funnel_concat_A])
        self.assertEqual(pipeline_2.run(['Z', 'Z', 'Z']), ['ZA', 'ZA', 'ZA'])
