import operator
import sys
from types import CodeType
from typing import List, Any, Callable

from pyasmer import op_help
from pyasmer.asm_instruction import AsmInstruction, JumpInstruction
from pyasmer.op_help import has_jabs, has_jrel, jump_target
from pyasmer.structure import IncDict, DefaultDict

SELF_MODULE = sys.modules[__name__]
HELP_MODULE = op_help


def _inst_chunks(code_array: bytes):
    for i in range(0, len(code_array), 2):
        yield i, code_array[i:i + 2]


class CodeViewer:

    ATTR_NAMES = ("name", "const", "local")

    def __init__(self, co):
        # Extract functions from methods.
        if hasattr(co, '__func__'):
            co = co.__func__
        # Extract compiled code objects from...
        if hasattr(co, '__code__'):  # ...a function, or
            co = co.__code__
        elif hasattr(co, 'gi_code'):  # ...a generator object, or
            co = co.gi_code
        elif hasattr(co, 'ag_code'):  # ...an asynchronous generator object, or
            co = co.ag_code
        elif hasattr(co, 'cr_code'):  # ...a coroutine.
            co = co.cr_code
        assert isinstance(co, CodeType)
        self._code_obj: CodeType = co
        self._inst_list: List[AsmInstruction] = []
        self._name_map: IncDict[str, int] = IncDict().init_by_seq(self._code_obj.co_names)
        self._const_map: IncDict[Any, int] = IncDict().init_by_seq(self._code_obj.co_consts)
        self._local_map: IncDict[str, int] = IncDict().init_by_seq(self._code_obj.co_varnames)
        self.parse_code()

    def get_name(self, index):
        return self._code_obj.co_names[index]

    def get_const(self, index):
        return self._code_obj.co_consts[index]

    def get_local(self, index):
        return self._code_obj.co_varnames[index]

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

    def parse_code(self):
        for offset, (inst_op, oparg) in _inst_chunks(self._code_obj.co_code):
            self._inst_list.append(self._parse_inst(offset, inst_op, oparg))
        self._parse_jump()

    def __call__(self, *args, **kwargs):
        return self

    def __str__(self):
        return "\n".join(str(x) for x in self._inst_list)

    def __iter__(self):
        return iter(self._inst_list)

    def find_inst_by_offset(self, offset):
        if self._inst_list[offset // 2].offset == offset:
            return self._inst_list[offset // 2]
        else:
            raise AssertionError("Offset error")

    def find_index_by_inst_name(self, *inst_names):
        inst_names = set(inst_names)
        for i in range(len(self._inst_list)):
            if self._inst_list[i].inst_name in inst_names:
                yield i

    def find_snippet_by_expression(self, source_code: str, *, local_vars=None, global_vars=None):
        if local_vars is None:
            local_vars = []
        if global_vars is None:
            global_vars = []
        match_code = compile(source_code, '<exp>', 'eval')
        match_viewer = CodeViewer(match_code)
        match_len = len(match_viewer._inst_list) - 1  # TODO

        asm_inst: AsmInstruction
        for asm_inst in filter(lambda inst: inst.inst_name == "LOAD_NAME", match_viewer):
            if asm_inst.oparg.value in local_vars:
                getattr(asm_inst, '_update')(inst_name="LOAD_FAST")
            elif asm_inst.oparg.value in global_vars:
                getattr(asm_inst, '_update')(inst_name="LOAD_GLOBAL")

        def match_one(match_inst: AsmInstruction, do: Callable):
            for pos in filter(lambda x: self._inst_list[x].oparg == match_inst.oparg,
                              self.find_index_by_inst_name(match_inst.inst_name)):
                do(pos)

        result: DefaultDict[int, List] = DefaultDict.create(lambda: [])
        match_one(match_viewer._inst_list[0], lambda p: result[p].append(p))

        def append_next(pos):
            if pos - 1 in result:
                result[pos] = result[pos - 1]
                result[pos].append(pos)
                del result[pos - 1]
        for asm_inst in match_viewer._inst_list[1:match_len]:
            match_one(asm_inst, append_next)

        for item in sorted(result.items(), key=operator.itemgetter(0)):
            if len(item[1]) == match_len:
                yield item[1][0], item[1][-1]
