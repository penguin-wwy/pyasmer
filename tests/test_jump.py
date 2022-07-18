from pyasmer.asm_helper import asm_writer
from pyasmer.asm_instruction import asm_const_var, asm_global_var, asm_fast_var
from pyasmer.code_writer import CodeWriter


@asm_writer
def insert_return_const(flag):
    if flag:
        return 0
    else:
        return 1


def test_insert_return_const():
    cw: CodeWriter = insert_return_const.writer
    cw.return_value(2, asm_const_var(1))
    cw.gen_code()
    assert insert_return_const(0) == 1
    assert insert_return_const(1) == 1


@asm_writer
def insert_print_element(array):
    """
    Test relation jump
    """
    ret_sum = 0
    for i in array:
        ret_sum += i
    return ret_sum


def test_insert_print_element(capsys):
    cw: CodeWriter = insert_print_element.writer
    for_iter_index = [x for x in cw.find_index_by_inst_name('FOR_ITER')]
    assert len(for_iter_index) == 1
    next_index = for_iter_index[0] + 2  # skip STORE_FAST
    cw.call_function(next_index, None, asm_global_var('print'), asm_fast_var('i'))
    cw.gen_code()
    insert_print_element([1, 2, 3])
    captured = capsys.readouterr()
    assert captured.out == '1\n2\n3\n'
