from pyasmer.asm_instruction import AsmElement, AsmElemType
from pyasmer.code_writer import CodeWriter


def insert_print_result(inputs):
    result = len(inputs)
    return result


def test_insert_print_result(capsys):
    origin_stack_size = insert_print_result.__code__.co_stacksize
    cw = CodeWriter(insert_print_result.__code__)()
    cw.call_function(4,
                     None,
                     AsmElement('print', AsmElemType.ASM_GLOBAL),
                     AsmElement('result', AsmElemType.ASM_VARIABLE))
    cw.gen_code()
    insert_print_result([])
    captured = capsys.readouterr()
    assert captured.out == '0\n'
    assert origin_stack_size + 2 == insert_print_result.__code__.co_stacksize


def insert_sum_call(inputs):
    result = None
    return result


def test_insert_sum_call():
    origin_stack_size = insert_sum_call.__code__.co_stacksize
    cw = CodeWriter(insert_sum_call.__code__)()
    cw.call_function(2,
                     AsmElement('result', AsmElemType.ASM_VARIABLE),
                     AsmElement('sum', AsmElemType.ASM_GLOBAL),
                     AsmElement('inputs', AsmElemType.ASM_VARIABLE))
    cw.gen_code()
    assert insert_sum_call([1, 2, 3]) == 6
    assert origin_stack_size + 2 == insert_sum_call.__code__.co_stacksize
