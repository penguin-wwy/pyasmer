import sys
from types import ModuleType

from pyasmer.asm_helper import asm_viewer
from pyasmer.code_view import CodeViewer


@asm_viewer
def named_module(name):
    if not isinstance(name, str):
        raise
    mod = sys.modules[name]
    if not isinstance(mod, ModuleType):
        raise
    return mod


def test_match_sys_modules():
    cv: CodeViewer = named_module.viewer
    sys_modules = [x for x in cv.find_snippet_by_expression("sys.modules", global_vars=["sys"])]
    assert len(sys_modules) == 1
    assert sys_modules[0] == (6, 7)

    sys_modules_name = [x for x in cv.find_snippet_by_expression("sys.modules[name]",
                                                                 local_vars=['name'], global_vars=["sys"])]
    assert len(sys_modules_name) == 1
    assert sys_modules_name[0] == (6, 9)


@asm_viewer
def binary_ops(a, b):
    return [a + b, a - b, a * b, a / b, a + b]


def test_match_binary_op():
    cv: CodeViewer = binary_ops.viewer
    binary_add = [x for x in cv.find_snippet_by_expression("a + b", local_vars=["a", "b"])]
    assert len(binary_add) == 2
    assert binary_add == [(0, 2), (12, 14)]
