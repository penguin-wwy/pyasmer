from typing import Optional, Dict, List, Set

from pyasmer.code_view import CodeViewer, HELP_MODULE
from pyasmer.asm_instruction import AsmInstruction, AsmElement, asm_attr_var, asm_const_var, JumpInstruction
from pyasmer.op_help import to_inst_op, jump_oparg


class CodeWriter(CodeViewer):

    def __init__(self, co):
        super(CodeWriter, self).__init__(co)
        self._insert_position = 0
        self._inc_stack_size = 0
        self._insert_map: Dict[int, List[AsmInstruction]] = dict()
        self._delete_set: Set[int] = set()

    def update_position(self, *, offset=0, index=0):
        if offset > 0:
            self._insert_position = self.offset_to_index(offset)
        else:
            assert index >= 0
            self._insert_position = index

    def update_offset(self):
        # TODO
        for i in range(len(self._inst_list)):
            self._inst_list[i].offset = i * 2

    @staticmethod
    def offset_to_index(offset):
        return offset // 2

    def _gen_inst(self, inst: AsmInstruction):
        offset, inst_op, oparg_value = inst
        if isinstance(inst, JumpInstruction):
            return inst_op, jump_oparg(offset, inst_op, inst.jump_target)
        for attr_name in CodeViewer.ATTR_NAMES:
            if getattr(HELP_MODULE, f"has_{attr_name}")(inst_op):
                attr_map = getattr(self, f"_{attr_name}_map")
                if oparg_value not in attr_map:
                    attr_map[oparg_value] = len(attr_map)
                return inst_op, attr_map[oparg_value]
        return inst_op, oparg_value

    def gen_code(self):
        new_inst_list = []
        insert_index_list = [x for x in sorted(self._insert_map.keys())]
        origin_seek = 0
        for insert_index in insert_index_list:
            for origin_inst in filter(lambda x: x not in self._delete_set, range(origin_seek, insert_index)):
                new_inst_list.append(self._inst_list[origin_inst])
            new_inst_list.extend(self._insert_map[insert_index])
            origin_seek = insert_index
        assert origin_seek < len(self._inst_list)
        for origin_inst in filter(lambda x: x not in self._delete_set, range(origin_seek, len(self._inst_list))):
            new_inst_list.append(self._inst_list[origin_inst])

        self._inst_list = new_inst_list
        self._insert_position = 0
        self._insert_map.clear()
        self._delete_set.clear()
        self.update_offset()

        import pyasmer._pyasmer
        code_bytes = []
        for item in map(lambda x: self._gen_inst(x), self._inst_list):
            code_bytes.extend(item)
        stack_size = self._inc_stack_size + self._code_obj.co_stacksize \
            if self._inc_stack_size else self._code_obj.co_stacksize
        self._inc_stack_size = 0
        return pyasmer._pyasmer.reset_code_object(self._code_obj,
                                                  code_bytes=bytes(code_bytes),
                                                  consts_array=self._const_map.to_seq_if_inc(),
                                                  names_array=self._name_map.to_seq_if_inc(),
                                                  varnames_array=self._local_map.to_seq_if_inc(),
                                                  stack_size=stack_size)

    def insert_inst(self, inst_name, oparg=0):
        if self._insert_position not in self._insert_map:
            self._insert_map[self._insert_position] = []
        self._insert_map[self._insert_position].append(AsmInstruction(-1, to_inst_op(inst_name), oparg))
        # TODO: pass oparg
        # return opcode.stack_effect(HELP_MODULE.to_inst_op(inst_name))

    def delete_inst(self, *, offset=None, index=None, total=1):
        if offset is not None:
            delete_from = self.offset_to_index(offset)
        elif index is not None:
            delete_from = index
        else:
            raise AssertionError("Invalid input for delete inst")
        for i in range(total):
            self._delete_set.add(delete_from + i)

    def call_function(self, retval: Optional[AsmElement], function: AsmElement, *args: AsmElement):
        function.gen_load_inst(self)
        for arg in reversed(args):
            arg.gen_load_inst(self)
        self.insert_inst('CALL_FUNCTION', len(args))
        if retval:
            retval.gen_store_inst(self)
        else:
            self.insert_inst('POP_TOP')
        self._inc_stack_size = max(len(args) + 1, self._inc_stack_size)

    def load_attribute(self, dest: Optional[AsmElement], owner: AsmElement, attr_name: AsmElement):
        owner.gen_load_inst(self)
        assert isinstance(attr_name, asm_attr_var)
        attr_name.gen_load_inst(self)
        if dest:
            dest.gen_store_inst(self)
        self._inc_stack_size = max(1, self._inc_stack_size)

    def return_value(self, retval: Optional[AsmElement]):
        if not retval:
            retval = asm_const_var(None)
        retval.gen_load_inst(self)
        self.insert_inst('RETURN_VALUE')
        self._inc_stack_size = max(1, self._inc_stack_size)
