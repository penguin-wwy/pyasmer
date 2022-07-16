import opcode


def has_const(inst_op):
    return inst_op in opcode.hasconst


def has_name(inst_op):
    return inst_op in opcode.hasname


def has_local(inst_op):
    return inst_op in opcode.haslocal


def has_jabs(inst_op):
    return inst_op in opcode.hasjabs


def to_inst_name(inst_op):
    return opcode.opname[inst_op]


def to_inst_op(inst_name):
    return opcode.opmap[inst_name]