import operator
from typing import Optional

from pyasmer.code_view import CodeViewer, HELP_MODULE
from pyasmer.asm_instruction import AsmInstruction, AsmElement, asm_attr_var, asm_const_var, JumpInstruction
from pyasmer.op_help import to_inst_op, jump_oparg


class CodeWriter(CodeViewer):

    def __init__(self, co):
        super(CodeWriter, self).__init__(co)
        self._inc_stack_size = 0

    def _gen_inst(self, inst: AsmInstruction):
        offset, inst_op, oparg_value = inst
        if isinstance(inst, JumpInstruction):
            return inst_op, jump_oparg(offset, inst_op, inst.jump_target)
        for attr_name in CodeViewer.ATTR_NAMES:
            if getattr(HELP_MODULE, f"has_{attr_name}")(inst_op):
                if attr_name == "local" and oparg_value not in self._local_map:
                    raise NameError("TODO append variable")
                attr_map = getattr(self, f"_{attr_name}_map")
                if oparg_value not in attr_map:
                    attr_map[oparg_value] = len(attr_map)
                return inst_op, attr_map[oparg_value]
        return inst_op, oparg_value

    def gen_code(self):
        self.update_offset()
        import pyasmer._pyasmer
        code_bytes = []
        for item in map(lambda x: self._gen_inst(x), self._inst_list):
            code_bytes.extend(item)
        name_array = [x[0] for x in sorted(self._name_map.items(), key=operator.itemgetter(1))]
        const_array = [x[0] for x in sorted(self._const_map.items(), key=operator.itemgetter(1))]
        stack_size = self._inc_stack_size + self._code_obj.co_stacksize \
            if self._inc_stack_size else self._code_obj.co_stacksize
        self._inc_stack_size = 0
        return pyasmer._pyasmer.reset_code_object(self._code_obj,
                                                  code_bytes=bytes(code_bytes),
                                                  consts_array=tuple(const_array),
                                                  names_array=tuple(name_array),
                                                  stack_size=stack_size)

    def insert_inst(self, index, inst_name, oparg=0):
        # TODO: pass offset
        self._inst_list.insert(index, AsmInstruction(index * 2, to_inst_op(inst_name), oparg))
        # TODO: pass oparg
        # return opcode.stack_effect(HELP_MODULE.to_inst_op(inst_name))

    def call_function(self, index, retval: Optional[AsmElement], function: AsmElement, *args: AsmElement):
        next_index = function.gen_load_inst(self, index)
        for arg in reversed(args):
            next_index = arg.gen_load_inst(self, next_index)
        self.insert_inst(next_index, 'CALL_FUNCTION', len(args))
        next_index += 1
        if retval:
            next_index = retval.gen_store_inst(self, next_index)
        else:
            self.insert_inst(index + len(args) + 2, 'POP_TOP')
            next_index += 1
        self._inc_stack_size = max(len(args) + 1, self._inc_stack_size)
        return next_index

    def load_attribute(self, index, dest: Optional[AsmElement], owner: AsmElement, attr_name: AsmElement):
        next_index = owner.gen_load_inst(self, index)
        assert isinstance(attr_name, asm_attr_var)
        next_index = attr_name.gen_load_inst(self, next_index)
        if dest:
            dest.gen_store_inst(self, next_index)
        self._inc_stack_size = max(1, self._inc_stack_size)
        return next_index + 1

    def return_value(self, index, retval: Optional[AsmElement]):
        if not retval:
            retval = asm_const_var(None)
        next_index = retval.gen_load_inst(self, index)
        self.insert_inst(next_index, 'RETURN_VALUE')
        self._inc_stack_size = max(1, self._inc_stack_size)
        return next_index + 1
