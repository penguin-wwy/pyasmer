import opcode
import operator
import sys
from types import CodeType
from typing import List, Dict

import _pyasmer

SELF_MODULE = sys.modules[__name__]


def _has_const(inst_op):
    return inst_op in opcode.hasconst


def _has_name(inst_op):
    return inst_op in opcode.hasname


def _has_local(inst_op):
    return inst_op in opcode.haslocal


def _has_jabs(inst_op):
    return inst_op in opcode.hasjabs


def _inst_name(inst_op):
    return opcode.opname[inst_op]


def _inst_op(inst_name):
    return opcode.opmap[inst_name]


def _inst_chunks(code_array: bytes):
    for i in range(0, len(code_array), 2):
        yield code_array[i:i + 2]


class AsmInstruction:
    def __init__(self, inst_op, oparg):
        self.inst_op = inst_op
        self.oparg = oparg

    def __str__(self):
        return f"({self.inst_op}, {self.oparg})"


class CodeViewer:

    ATTR_NAMES = ("name", "const", "local")

    def __init__(self, co):
        self._code_obj: CodeType = co
        self._inst_list: List = []
        self._jabs_map: Dict = {}
        self._name_map: Dict
        self._const_map: Dict
        self._local_map: Dict

    def jabs_map_or_default(self, k) -> List:
        if k not in self._jabs_map:
            self._jabs_map[k] = []
        return self._jabs_map[k]

    def get_name(self, index):
        return self._code_obj.co_names[index]

    def get_const(self, index):
        return self._code_obj.co_consts[index]

    def get_local(self, index):
        return self._code_obj.co_varnames[index]

    def _parse_inst(self, inst_op, oparg) -> AsmInstruction:
        for attr_name in CodeViewer.ATTR_NAMES:
            if getattr(SELF_MODULE, f"_has_{attr_name}")(inst_op):
                return AsmInstruction(_inst_name(inst_op), getattr(self, f"get_{attr_name}")(oparg))
        result = AsmInstruction(_inst_name(inst_op), oparg)
        if _has_jabs(inst_op):
            # Note: 3.10 jump
            self.jabs_map_or_default(oparg).append(result)
        return result

    def _parse_code(self):
        self._name_map = {self.get_name(i): i for i in range(len(self._code_obj.co_names))}
        self._const_map = {self.get_const(i): i for i in range(len(self._code_obj.co_consts))}
        self._local_map = {self.get_local(i): i for i in range(len(self._code_obj.co_varnames))}
        for inst_op, oparg in _inst_chunks(self._code_obj.co_code):
            self._inst_list.append(self._parse_inst(inst_op, oparg))

    def insert_inst(self, index, inst_name, oparg=0):
        self._inst_list.insert(index, AsmInstruction(inst_name, oparg))
        for item in filter(lambda x: x[0] > index, self._jabs_map.items()):
            for inst in item[1]:
                inst.oparg += 1
        # TODO: relation jump

    def _gen_inst(self, inst_name, oparg):
        inst_op = _inst_op(inst_name)
        for attr_name in CodeViewer.ATTR_NAMES:
            if getattr(SELF_MODULE, f"_has_{attr_name}")(inst_op):
                if attr_name == "local" and oparg not in self._local_map:
                    raise NameError("TODO append variable")
                attr_map = getattr(self, f"_{attr_name}_map")
                if oparg not in attr_map:
                    attr_map[oparg] = len(attr_map)
                return inst_op, attr_map[oparg]
        return inst_op, oparg

    def gen_code(self):
        code_bytes = []
        for item in map(lambda x: self._gen_inst(x.inst_op, x.oparg), self._inst_list):
            code_bytes.extend(item)
        name_array = [x[0] for x in sorted(self._name_map.items(), key=operator.itemgetter(1))]
        const_array = [x[0] for x in sorted(self._const_map.items(), key=operator.itemgetter(1))]
        return _pyasmer.reset_code_object(self._code_obj, code_bytes=bytes(code_bytes), consts_array=tuple(const_array), names_array=tuple(name_array))

    def __call__(self, *args, **kwargs):
        self._parse_code()
        return self

    def __str__(self):
        return "\n".join(str(x) for x in self._inst_list)
