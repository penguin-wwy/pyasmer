import dis

from pyasmer.asm_helper import asm_writer
from pyasmer.asm_instruction import asm_const_var


@asm_writer
def insert_return_const(flag):
    if flag:
        return 0
    else:
        return 1


def test_insert_return_const():
    cw = insert_return_const.writer
    cw.return_value(2, asm_const_var(1))
    cw.gen_code()
    print(dis.dis(insert_return_const.function))
    assert insert_return_const(0) == 1
    assert insert_return_const(1) == 1
