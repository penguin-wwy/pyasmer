from collections import namedtuple

from pyasmer.asm_helper import asm_writer
from pyasmer.asm_instruction import asm_local_var
from pyasmer.code_writer import CodeWriter

User = namedtuple('User', ['name', 'sex', 'age'])


@asm_writer
def insert_user_attr(user: User):
    return None


def test_insert_user_attr():
    user = User(name='bob', sex='unknown', age=-1)
    cw: CodeWriter = insert_user_attr.writer
    cw.load_attribute(1, None, asm_local_var('user'), attr_name='name')
    cw.gen_code()
    assert insert_user_attr(user) == 'bob'
