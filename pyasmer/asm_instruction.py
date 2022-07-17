import enum
from typing import Optional

from pyasmer.op_help import is_abs_jump, to_inst_name

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

    def gen_load_inst(self, cw, index):
        cw.insert_inst(index, *self.load_inst)
        return index + 1

    def gen_store_inst(self, cw, index):
        cw.insert_inst(index, *self.store_inst)
        return index + 1


class AsmLocalVarElem(AsmElement):

    def __init__(self, varname):
        super(AsmLocalVarElem, self).__init__(varname, AsmElemType.ASM_VARIABLE)


class AsmConstVarElem(AsmElement):

    def __init__(self, cnt_val):
        super(AsmConstVarElem, self).__init__(cnt_val, AsmElemType.ASM_CONST)


class AsmGlobalVarElem(AsmElement):

    def __init__(self, global_name):
        super(AsmGlobalVarElem, self).__init__(global_name, AsmElemType.ASM_GLOBAL)


class AsmAttrVarElem(AsmElement):

    def __init__(self, owner: AsmElement, attr_name):
        super(AsmAttrVarElem, self).__init__(attr_name, AsmElemType.ASM_ATTR)
        self._owner = owner

    def gen_load_inst(self, cw, index):
        self._owner.gen_load_inst(cw, index)
        cw.insert_inst(index + 1, *self.load_inst)
        return index + 2


asm_local_var = AsmLocalVarElem
asm_const_var = AsmConstVarElem
asm_global_var = AsmGlobalVarElem
asm_attr_var = AsmAttrVarElem


class AsmInstruction:
    def __init__(self, offset, inst_op, oparg):
        self.inst_name = to_inst_name(inst_op)
        self.inst_op = inst_op
        self.oparg = oparg
        self.offset = offset

    def __iter__(self):
        return iter((self.offset, self.inst_op, self.oparg))

    def __str__(self):
        return f"({self.offset}, {self.inst_name}, {self.oparg})"

    def promote(self, cls, *args):
        self.__class__ = cls
        cls.promote_by(*([self] + list(args)))


class JumpInstruction(AsmInstruction):
    def __init__(self, offset, inst_op, oparg):
        super(JumpInstruction, self).__init__(offset, inst_op, oparg)
        self._jump_target: Optional[AsmInstruction] = None
        self._hax_next = not is_abs_jump(self.inst_name)

    @property
    def jump_target(self):
        return self._jump_target.offset

    @classmethod
    def promote_by(cls, inst: 'JumpInstruction', target: AsmInstruction):
        inst._hax_next = not is_abs_jump(inst.inst_name)
        inst._jump_target = target
        return inst
