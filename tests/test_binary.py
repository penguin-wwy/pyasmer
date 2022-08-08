from typing import List

from pyasmer.asm_helper import asm_writer
from pyasmer.asm_instruction import asm_global_var, asm_fast_var
from pyasmer.code_writer import CodeWriter


@asm_writer
def sequence_add(a: List, b: List):
    return a, b


def test_sequence_add():
    cw: CodeWriter = sequence_add.writer
    snippet = cw.find_snippet_by_expression('a, b', local_vars=['a', 'b'])
    snippet = next(snippet)
    cw.update_position(index=snippet[1] + 1)
    cw.binary_op(None, asm_fast_var('a'), asm_fast_var('b'), "+")
    cw.gen_code()
    assert sequence_add([1], [2]) == [1, 2]


NUMBER = 10


@asm_writer
def global_operator(a):
    a += 1
    return a


def test_global_operator():
    cw: CodeWriter = global_operator.writer
    cw.binary_op(asm_fast_var('a'), asm_fast_var('a'), asm_global_var('NUMBER'), '*')
    cw.gen_code()
    assert global_operator(1) == 11
