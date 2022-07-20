/*[clinic input]
preserve
[clinic start generated code]*/

PyDoc_STRVAR(_pyasmer_reset_code_object__doc__,
"reset_code_object($module, code, /, *, code_bytes=None,\n"
"                  consts_array=None, names_array=None,\n"
"                  varnames_array=None, stack_size=0)\n"
"--\n"
"\n"
"Reload module.");

#define _PYASMER_RESET_CODE_OBJECT_METHODDEF    \
    {"reset_code_object", (PyCFunction)_pyasmer_reset_code_object, METH_FASTCALL, _pyasmer_reset_code_object__doc__},

static PyObject *
_pyasmer_reset_code_object_impl(PyObject *module, PyObject *code,
                                PyObject *code_bytes, PyObject *consts_array,
                                PyObject *names_array,
                                PyObject *varnames_array, int stack_size);

static PyObject *
_pyasmer_reset_code_object(PyObject *module, PyObject **args, Py_ssize_t nargs, PyObject *kwnames)
{
    PyObject *return_value = NULL;
    static const char * const _keywords[] = {"", "code_bytes", "consts_array", "names_array", "varnames_array", "stack_size", NULL};
    static _PyArg_Parser _parser = {"O|$OOOOi:reset_code_object", _keywords, 0};
    PyObject *code;
    PyObject *code_bytes = Py_None;
    PyObject *consts_array = Py_None;
    PyObject *names_array = Py_None;
    PyObject *varnames_array = Py_None;
    int stack_size = 0;

    if (!_PyArg_ParseStack(args, nargs, kwnames, &_parser,
                           &code, &code_bytes, &consts_array, &names_array, &varnames_array, &stack_size)) {
        goto exit;
    }
    return_value = _pyasmer_reset_code_object_impl(module, code, code_bytes, consts_array, names_array, varnames_array, stack_size);

exit:
    return return_value;
}
/*[clinic end generated code: output=ab68cadbf65207e9 input=a9049054013a1b77]*/
