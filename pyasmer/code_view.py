import sys
from types import CodeType
from typing import List, Dict

from pyasmer import op_help
from pyasmer.asm_instruction import AsmInstruction, JumpInstruction
from pyasmer.op_help import has_jabs, has_jrel, jump_target

SELF_MODULE = sys.modules[__name__]
HELP_MODULE = op_help


def _inst_chunks(code_array: bytes):
    for i in range(0, len(code_array), 2):
        yield i, code_array[i:i + 2]


class CodeViewer:

    ATTR_NAMES = ("name", "const", "local")

    def __init__(self, co):
        self._code_obj: CodeType = co
        self._inst_list: List[AsmInstruction] = []
        self._name_map: Dict
        self._const_map: Dict
        self._local_map: Dict

    def get_name(self, index):
        return self._code_obj.co_names[index]

    def get_const(self, index):
        return self._code_obj.co_consts[index]

    def get_local(self, index):
        return self._code_obj.co_varnames[index]

    def find_inst_by_offset(self, offset):
        if self._inst_list[offset // 2].offset == offset:
            return self._inst_list[offset // 2]
        else:
            raise AssertionError("Offset error")

    def find_index_by_inst_name(self, inst_name):
        for i in range(len(self._inst_list)):
            if self._inst_list[i].inst_name == inst_name:
                yield i

    def _parse_jump(self):
        for inst in self._inst_list:
            if has_jabs(inst.inst_op) or has_jrel(inst.inst_op):
                offset = jump_target(*inst)
                target = self.find_inst_by_offset(offset)
                inst.promote(JumpInstruction, target)

    def _parse_inst(self, offset, inst_op, oparg) -> AsmInstruction:
        for attr_name in CodeViewer.ATTR_NAMES:
            if getattr(HELP_MODULE, f"has_{attr_name}")(inst_op):
                return AsmInstruction(offset, inst_op, getattr(self, f"get_{attr_name}")(oparg))
        return AsmInstruction(offset, inst_op, oparg)

    def _parse_code(self):
        self._name_map = {self.get_name(i): i for i in range(len(self._code_obj.co_names))}
        self._const_map = {self.get_const(i): i for i in range(len(self._code_obj.co_consts))}
        self._local_map = {self.get_local(i): i for i in range(len(self._code_obj.co_varnames))}
        for offset, (inst_op, oparg) in _inst_chunks(self._code_obj.co_code):
            self._inst_list.append(self._parse_inst(offset, inst_op, oparg))
        self._parse_jump()

    def __call__(self, *args, **kwargs):
        self._parse_code()
        return self

    def __str__(self):
        return "\n".join(str(x) for x in self._inst_list)
