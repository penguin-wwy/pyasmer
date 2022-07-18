from pyasmer.asm_instruction import AsmElemType


def test_asm_elem_type():
    assert AsmElemType["ASM_GLOBAL"] == AsmElemType.ASM_GLOBAL
    assert AsmElemType["ASM_FUNCTION"] == AsmElemType.ASM_DEFAULT
