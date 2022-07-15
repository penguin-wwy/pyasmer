import dis

import fib
from pyasmer.asm_instruction import AsmElement, AsmElemType
from pyasmer.code_writer import CodeWriter

if __name__ == '__main__':
    cw = CodeWriter(fib.fib.__code__)()
    print(cw)
    print(dis.dis(fib.fib))
    print("====================================")
    cw.call_function(0, None, AsmElement('print', AsmElemType.ASM_GLOBAL), AsmElement('num', AsmElemType.ASM_VARIABLE))
    print(cw)
    cw.gen_code()
    print(dis.dis(fib.fib))
    print(fib.fib(4))
