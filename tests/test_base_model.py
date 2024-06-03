
import sys
import unittest
import sys
from self_utils.llm_util import LLM_Util

class TestBaseModel(unittest.TestCase):
    def test_model(self):
        llm = LLM_Util()
        r = llm.invoke([{"content": "你好，我是谁", "role": "user"}])
        for i in r:
            print(i)
            # print(i.choices[0].delta.content or "", end="")


    def test_yiled(self):
        def a():
            for i in range(10):
                yield i
        def d():
            res = a()
            print("res: ", res)
            yield from res
            print("res: ", res)

        for i in d():
            print(i)


