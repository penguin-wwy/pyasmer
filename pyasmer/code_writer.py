from pyasmer.code_view import CodeViewer
from pyasmer.asm_instruction import AsmInstruction, AsmElement


class CodeWriter(CodeViewer):

    def __init__(self, co):
        super(CodeWriter, self).__init__(co)

    def insert_inst(self, index, inst_name, oparg=0):
        self._inst_list.insert(index, AsmInstruction(inst_name, oparg))
        for item in filter(lambda x: x[0] > index, self._jabs_map.items()):
            for inst in item[1]:
                inst.oparg += 1
        # TODO: relation jump

    def call_function(self, index, retval: AsmElement | None, function: AsmElement, *args: AsmElement):
        self.insert_inst(index, *function.load_inst)
        for i in range(1, len(args) + 1):
            self.insert_inst(index + i, *args[-i].load_inst)
        self.insert_inst(index + len(args) + 1, 'CALL_FUNCTION', len(args))
        self.insert_inst(index + len(args) + 2, retval.store_inst if retval else 'POP_TOP')
