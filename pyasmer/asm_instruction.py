import enum
import sys
from typing import Optional

from pyasmer.op_help import is_abs_jump, to_inst_name, to_inst_op

_SELF_MODULE = sys.modules[__name__]

_ELEM_LOAD = [None, 'LOAD_FAST', 'LOAD_CONST', 'LOAD_NAME', 'LOAD_GLOBAL', 'LOAD_ATTR']
_ELEM_STORE = [None, 'STORE_FAST', '', 'STORE_NAME', 'STORE_GLOBAL', 'STORE_ATTR']


class _AsmElemTypeMeta(enum.EnumMeta):

    def __getitem__(self, item):
        if item not in self._member_map_:
            return self._member_map_['ASM_DEFAULT']
        return self._member_map_[item]


class AsmElemType(enum.IntEnum, metaclass=_AsmElemTypeMeta):
    ASM_DEFAULT = 0
    ASM_FAST = 1
    ASM_CONST = 2
    ASM_NAME = 3
    ASM_GLOBAL = 4
    ASM_ATTR = 5

    def load(self):
        return _ELEM_LOAD[self.value]

    def store(self):
        return _ELEM_STORE[self.value]

    def contribute(self, *args, **kwargs):
        return getattr(_SELF_MODULE, f"{self.name.lower()}_var")(*args, **kwargs)


class AsmElement:

    def __init__(self, value, val_tp: AsmElemType):
        self._value = value
        self._val_tp = val_tp

    @property
    def value(self):
        return self._value

    @property
    def load_inst(self):
        return self._val_tp.load(), self._value

    @property
    def store_inst(self):
        return self._val_tp.store(), self._value

    def gen_load_inst(self, cw):
        cw.insert_inst(*self.load_inst)

    def gen_store_inst(self, cw):
        cw.insert_inst(*self.store_inst)

    def __eq__(self, other):
        if isinstance(other, AsmElement):
            return self._value == other._value
        else:
            return self._value == other


class AsmFastVarElem(AsmElement):

    def __init__(self, varname):
        super(AsmFastVarElem, self).__init__(varname, AsmElemType.ASM_FAST)


class AsmConstVarElem(AsmElement):

    def __init__(self, cnt_val):
        super(AsmConstVarElem, self).__init__(cnt_val, AsmElemType.ASM_CONST)


class AsmNameVarElem(AsmElement):

    def __init__(self, name_str):
        super(AsmNameVarElem, self).__init__(name_str, AsmElemType.ASM_NAME)


class AsmGlobalVarElem(AsmElement):

    def __init__(self, global_name):
        super(AsmGlobalVarElem, self).__init__(global_name, AsmElemType.ASM_GLOBAL)


class AsmAttrVarElem(AsmElement):

    def __init__(self, attr_name):
        super(AsmAttrVarElem, self).__init__(attr_name, AsmElemType.ASM_ATTR)


asm_default_var = lambda o: AsmElement(o, AsmElemType.ASM_DEFAULT)
asm_fast_var = AsmFastVarElem
asm_const_var = AsmConstVarElem
asm_name_var = AsmNameVarElem
asm_global_var = AsmGlobalVarElem
asm_attr_var = AsmAttrVarElem


def _get_suffix_type(inst_name: str) -> AsmElemType:
    return AsmElemType[f"ASM_{inst_name.split('_')[-1]}"]


class AsmInstruction:
    def __init__(self, offset, inst_op, oparg):
        self.inst_name = to_inst_name(inst_op)
        self.inst_op = inst_op
        self.oparg = _get_suffix_type(self.inst_name).contribute(oparg) if not isinstance(oparg, AsmElement) else oparg
        self.offset = offset

    def __iter__(self):
        return iter((self.offset, self.inst_op, self.oparg.value))

    def __str__(self):
        return f"({self.offset}, {self.inst_name}, {self.oparg})"

    def _update(self, *, inst_name=None, inst_op=None, oparg=None, offset=None):
        assert not inst_name or not inst_op or to_inst_name(inst_op) == inst_name
        if inst_name:
            self.inst_name = inst_name
            self.inst_op = to_inst_op(inst_name)
        if inst_op:
            self.inst_op = inst_op
            self.inst_name = to_inst_name(inst_op)
        if oparg:
            self.oparg = _get_suffix_type(self.inst_name).contribute(oparg) \
                if not isinstance(oparg, AsmElement) else oparg
        if offset:
            self.offset = offset

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
