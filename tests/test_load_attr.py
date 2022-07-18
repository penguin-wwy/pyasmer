from collections import namedtuple

from pyasmer.asm_helper import asm_writer
from pyasmer.asm_instruction import asm_fast_var, asm_attr_var
from pyasmer.code_writer import CodeWriter

User = namedtuple('User', ['name', 'sex', 'age'])


@asm_writer
def insert_user_attr(user: User):
    return None


def test_insert_user_attr():
    user = User(name='bob', sex='unknown', age=-1)
    cw: CodeWriter = insert_user_attr.writer
    return_value_index = [x for x in cw.find_index_by_inst_name('RETURN_VALUE')]
    assert len(return_value_index) == 1
    cw.load_attribute(return_value_index[0], None, asm_fast_var('user'), asm_attr_var('name'))
    cw.gen_code()
    assert insert_user_attr(user) == 'bob'
