from collections import namedtuple

from pyasmer.code_view import CodeViewer
from pyasmer.code_writer import CodeWriter


FunctionAndViewer = namedtuple('FunctionAndViewer', ['function', 'viewer'])
FunctionAndWriter = namedtuple('FunctionAndWriter', ['function', 'writer'])


class AsmViewer(FunctionAndViewer):

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)


def asm_viewer(func):
    cv = CodeViewer(func)
    return AsmViewer(func, cv)


class AsmWriter(FunctionAndWriter):

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)


def asm_writer(func):
    cw = CodeWriter(func)
    return AsmWriter(func, cw)
