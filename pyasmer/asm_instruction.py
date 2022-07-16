import enum

_ELEM_LOAD = ['', 'LOAD_FAST', 'LOAD_CONST', 'LOAD_NAME', 'LOAD_GLOBAL', 'LOAD_ATTR']
_ELEM_STORE = ['', 'STORE_FAST', '', 'STORE_NAME', 'STORE_GLOBAL', 'STORE_ATTR']


class AsmElemType(enum.IntEnum):
    ASM_VARIABLE = 1
    ASM_CONST = 2
    ASM_NAME = 3
    ASM_GLOBAL = 4
    ASM_ATTR = 5

    def load(self):
        return _ELEM_LOAD[self.value]

    def store(self):
        return _ELEM_STORE[self.value]


class AsmElement:

    def __init__(self, value, val_tp: AsmElemType):
        self._value = value
        self._val_tp = val_tp

    @property
    def load_inst(self):
        return self._val_tp.load(), self._value

    @property
    def store_inst(self):
        return self._val_tp.store(), self._value


class AsmInstruction:
    def __init__(self, inst_op, oparg):
        self.inst_op = inst_op
        self.oparg = oparg

    def __str__(self):
        return f"({self.inst_op}, {self.oparg})"
