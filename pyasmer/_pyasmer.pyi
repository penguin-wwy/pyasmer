from types import CodeType
from typing import Tuple


def reset_code_object(code: CodeType, *,
                      code_bytes: bytes = None,
                      consts_array: Tuple = None,
                      names_array: Tuple = None,
                      varnames_array: Tuple = None,
                      stack_size: int = 0):
    ...
