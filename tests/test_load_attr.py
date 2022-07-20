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
    cw.update_position(index=return_value_index[0])
    cw.load_attribute(None, asm_fast_var('user'), asm_attr_var('name'))
    cw.gen_code()
    assert insert_user_attr(user) == 'bob'


"""
transform to:
  2           0 LOAD_FAST                0 (user)
              2 LOAD_ATTR                0 (name)
              4 STORE_FAST               1 (result)

  3           6 LOAD_FAST                1 (result)
              8 RETURN_VALUE
"""
@asm_writer
def load_attr_to_local_variable(user: User):
    user.name
    return None


def test_load_attr_to_local_variable():
    user = User(name='bob', sex='unknown', age=-1)
    cw: CodeWriter = load_attr_to_local_variable.writer
    return_value_index = [x for x in cw.find_index_by_inst_name('RETURN_VALUE')]
    assert len(return_value_index) == 1
    cw.update_position(offset=4)
    result = asm_fast_var('result')
    result.gen_store_inst(cw)
    result.gen_load_inst(cw)
    cw.delete_inst(offset=4, total=2)  # delete origin instructions
    cw.gen_code()
    assert load_attr_to_local_variable(user) == 'bob'

