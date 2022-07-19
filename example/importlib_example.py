import sys

from pyasmer.asm_instruction import asm_global_var, asm_fast_var
from pyasmer.code_writer import CodeWriter

if __name__ == '__main__':
    _frozen_importlib = sys.modules['_frozen_importlib']
    _find_and_load_unlocked = getattr(_frozen_importlib, '_find_and_load_unlocked')
    cw = CodeWriter(_find_and_load_unlocked.__code__)()
    cw.update_position(offset=0)
    cw.call_function(None, asm_global_var('print'), asm_fast_var('name'))
    cw.gen_code()
    import ast  # noqa: F401, example code
    """
    output:
        ast
        _ast
    """
