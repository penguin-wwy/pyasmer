import dis

import fib
from pyasmer.code_view import CodeViewer

if __name__ == '__main__':
    cv = CodeViewer(fib.fib.__code__)()
    print(cv)
    print("====================================")
    cv.insert_inst(0, 'LOAD_GLOBAL', 'print')
    cv.insert_inst(1, 'LOAD_FAST', 'num')
    cv.insert_inst(2, 'CALL_FUNCTION', 1)
    cv.insert_inst(3, 'POP_TOP')
    print(cv)
    cv.gen_code()
    print(dis.dis(fib.fib))
    print(fib.fib(4))
