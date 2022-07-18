from pyasmer.asm_helper import asm_writer
from pyasmer.asm_instruction import asm_global_var, asm_fast_var
from pyasmer.code_writer import CodeWriter


@asm_writer
def insert_print_result(inputs):
    result = len(inputs)
    return result


def test_insert_print_result(capsys):
    origin_stack_size = insert_print_result.function.__code__.co_stacksize
    cw: CodeWriter = insert_print_result.writer
    store_fast_index = [x for x in cw.find_index_by_inst_name('STORE_FAST')]
    assert len(store_fast_index) == 1
    next_index = store_fast_index[0] + 1
    cw.call_function(next_index, None, asm_global_var('print'), asm_fast_var('result'))
    cw.gen_code()
    insert_print_result([])
    captured = capsys.readouterr()
    assert captured.out == '0\n'
    assert origin_stack_size + 2 == insert_print_result.function.__code__.co_stacksize


@asm_writer
def insert_sum_call(inputs):
    result = None
    return result


def test_insert_sum_call():
    origin_stack_size = insert_sum_call.function.__code__.co_stacksize
    cw: CodeWriter = insert_sum_call.writer
    store_fast_index = [x for x in cw.find_index_by_inst_name('STORE_FAST')]
    assert len(store_fast_index) == 1
    next_index = store_fast_index[0] + 1
    cw.call_function(next_index, asm_fast_var('result'), asm_global_var('sum'), asm_fast_var('inputs'))
    cw.gen_code()
    assert insert_sum_call([1, 2, 3]) == 6
    assert origin_stack_size + 2 == insert_sum_call.function.__code__.co_stacksize
