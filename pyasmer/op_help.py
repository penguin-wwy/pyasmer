import opcode
from sys import version_info as VERSION_INFO


def has_const(inst_op):
    return inst_op in opcode.hasconst


def has_name(inst_op):
    return inst_op in opcode.hasname


def has_local(inst_op):
    return inst_op in opcode.haslocal


def has_jabs(inst_op):
    return inst_op in opcode.hasjabs


def has_jrel(inst_op):
    return inst_op in opcode.hasjrel


def jump_target(offset, inst_op, oparg):
    if has_jabs(inst_op):
        return (oparg * 2) if VERSION_INFO > (3, 10) else oparg
    if has_jrel(inst_op):
        return offset + 2 + ((oparg * 2) if VERSION_INFO > (3, 10) else oparg)


def jump_oparg(inst_offset, inst_op, target_offset):
    if has_jabs(inst_op):
        return (target_offset // 2) if VERSION_INFO > (3, 10) else target_offset
    if has_jrel(inst_op):
        return (target_offset - 2 - inst_offset) // (2 if VERSION_INFO > (3, 10) else 1)


def is_abs_jump(inst_name):
    return inst_name == "JUMP_ABSOLUTE" or inst_name == "JUMP_FORWARD"


def to_inst_name(inst_op):
    return opcode.opname[inst_op]


def to_inst_op(inst_name):
    return opcode.opmap[inst_name]
