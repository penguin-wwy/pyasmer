from collections import namedtuple

from pyasmer.asm_helper import asm_writer
from pyasmer.code_writer import CodeWriter

User = namedtuple('User', ['name', 'sex', 'age'])

"""
  2           0 LOAD_FAST                1 (name)
              2 LOAD_FAST                0 (user)
              4 STORE_ATTR               0 (name)

  3           6 LOAD_FAST                0 (user)
              8 LOAD_ATTR                0 (name)
             10 RETURN_VALUE
"""
@asm_writer  # noqa: E302
def delete_store_attr(user: User, name):
    user.name = name
    return user.name


def test_insert_user_attr():
    user = User(name='bob', sex='unknown', age=-1)
    cw: CodeWriter = delete_store_attr.writer
    cw.delete_inst(offset=0, total=3)
    cw.gen_code()
    assert delete_store_attr(user, 'fake bob') == 'bob'
