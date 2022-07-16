from collections import namedtuple

from pyasmer.code_writer import CodeWriter


FunctionAndWriter = namedtuple('FunctionAndWriter', ['function', 'writer'])


class AsmWriter(FunctionAndWriter):

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)


def asm_writer(func):
    cw = CodeWriter(func.__code__)()
    return AsmWriter(func, cw)
