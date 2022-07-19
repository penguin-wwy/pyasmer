## Pyasmer

### En
Pyasmer is a python bytecode manipulation library.
It can be used to modify existing code object(e.g. `func.__code__`), directly in binary form.

Pyasmer helps developers to perform some dynamic stubbing, proxy, instruction generation, in existing python code.

Using it requires you to have some knowledge of Python bytecode and the CPython VM execution mechanism, 
which you can get from the official documentation:
[https://docs.python.org/3/library/dis.html](https://docs.python.org/3/library/dis.html).
Pyasmer will also provide some easy-to-use interfaces that are less difficult to use.

Fox example:
```python
import sys

from pyasmer.asm_instruction import asm_global_var, asm_fast_var
from pyasmer.code_writer import CodeWriter

if __name__ == '__main__':
    _frozen_importlib = sys.modules['_frozen_importlib']
    # The _find_and_load_unlocked function will be called when import module
    _find_and_load_unlocked = getattr(_frozen_importlib, '_find_and_load_unlocked')
    cw = CodeWriter(_find_and_load_unlocked.__code__)()
    # Add a print statement to the beginning of the _find_and_load_unlocked function 
    # to print out the name of the module which to be imported
    #
    # The insertion position is at the beginning of the function(0 instruction)
    cw.update_position(offset=0)
    # None: Ignore return value
    # asm_global_var('print'): called function is print
    # asm_fast_var('name'): local variable `name` pass to print
    cw.call_function(None, asm_global_var('print'), asm_fast_var('name'))
    cw.gen_code()
    # Execute the import command
    import ast
```

The output shows that there are two modules that are imported in the process.
```shell
output:
    ast
    _ast
```

For more information on how to use it, please refer to the tests directory.


### 中文
Pyasmer是一个Python字节码编辑库。它可以用来修改现有的二进制代码(例如, `func.__code__`)。

Pyasmer可以帮助开发者在python代码中执行一些动态地在已有代码中插桩、代理、指令生成，

使用它需要你具备一定的Python字节码和CPython虚拟机执行机制，你可以从官方文档获取这些知识：
[https://docs.python.org/3/library/dis.html](https://docs.python.org/3/library/dis.html)。
Pyasmer也会提供一些易于使用的接口，降低使用难度。

举个例子：
```python
import sys

from pyasmer.asm_instruction import asm_global_var, asm_fast_var
from pyasmer.code_writer import CodeWriter

if __name__ == '__main__':
    _frozen_importlib = sys.modules['_frozen_importlib']
    # _find_and_load_unlocked函数会在import模块的时候被调用
    _find_and_load_unlocked = getattr(_frozen_importlib, '_find_and_load_unlocked')
    cw = CodeWriter(_find_and_load_unlocked.__code__)()
    # 在_find_and_load_unlocked函数开头添加一个print，将要被import的模块名称打印出来
    #
    # 更新插入位置到函数开头(第0条指令)
    cw.update_position(offset=0)
    # None: 忽略返回值
    # asm_global_var('print'): 调用的函数为print
    # asm_fast_var('name'): 将局部变量`name`传给print
    cw.call_function(None, asm_global_var('print'), asm_fast_var('name'))
    cw.gen_code()
    # 执行import命令
    import ast
```

输出显示有两个模块在import命令过程中被引用。
```shell
output:
    ast
    _ast
```

更多的使用方法可以参考tests目录。
