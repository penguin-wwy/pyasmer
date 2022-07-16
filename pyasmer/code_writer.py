import operator

from pyasmer.code_view import CodeViewer, HELP_MODULE
from pyasmer.asm_instruction import AsmInstruction, AsmElement


class CodeWriter(CodeViewer):

    def __init__(self, co):
        super(CodeWriter, self).__init__(co)
        self._inc_stack_size = 0

    def gen_code(self):
        import pyasmer._pyasmer
        code_bytes = []
        for item in map(lambda x: self._gen_inst(x.inst_op, x.oparg), self._inst_list):
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
        self._inst_list.insert(index, AsmInstruction(inst_name, oparg))
        for item in filter(lambda x: x[0] > index, self._jabs_map.items()):
            for inst in item[1]:
                # TODO: relation jump
                inst.oparg += 1

        # TODO: pass oparg
        # return opcode.stack_effect(HELP_MODULE.to_inst_op(inst_name))

    def call_function(self, index, retval: AsmElement | None, function: AsmElement, *args: AsmElement):
        self.insert_inst(index, *function.load_inst)
        for i in range(1, len(args) + 1):
            self.insert_inst(index + i, *args[-i].load_inst)
        self.insert_inst(index + len(args) + 1, 'CALL_FUNCTION', len(args))
        self.insert_inst(index + len(args) + 2, *retval.store_inst if retval else 'POP_TOP')
        self._inc_stack_size = max(len(args) + 1, self._inc_stack_size)
