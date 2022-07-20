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
    {"reset_code_object", (PyCFunction)(void(*)(void))_pyasmer_reset_code_object, METH_FASTCALL|METH_KEYWORDS, _pyasmer_reset_code_object__doc__},

static PyObject *
_pyasmer_reset_code_object_impl(PyObject *module, PyObject *code,
                                PyObject *code_bytes, PyObject *consts_array,
                                PyObject *names_array,
                                PyObject *varnames_array, int stack_size);

static PyObject *
_pyasmer_reset_code_object(PyObject *module, PyObject *const *args, Py_ssize_t nargs, PyObject *kwnames)
{
    PyObject *return_value = NULL;
    static const char * const _keywords[] = {"", "code_bytes", "consts_array", "names_array", "varnames_array", "stack_size", NULL};
    static _PyArg_Parser _parser = {NULL, _keywords, "reset_code_object", 0};
    PyObject *argsbuf[6];
    Py_ssize_t noptargs = nargs + (kwnames ? PyTuple_GET_SIZE(kwnames) : 0) - 1;
    PyObject *code;
    PyObject *code_bytes = Py_None;
    PyObject *consts_array = Py_None;
    PyObject *names_array = Py_None;
    PyObject *varnames_array = Py_None;
    int stack_size = 0;

    args = _PyArg_UnpackKeywords(args, nargs, NULL, kwnames, &_parser, 1, 1, 0, argsbuf);
    if (!args) {
        goto exit;
    }
    code = args[0];
    if (!noptargs) {
        goto skip_optional_kwonly;
    }
    if (args[1]) {
        code_bytes = args[1];
        if (!--noptargs) {
            goto skip_optional_kwonly;
        }
    }
    if (args[2]) {
        consts_array = args[2];
        if (!--noptargs) {
            goto skip_optional_kwonly;
        }
    }
    if (args[3]) {
        names_array = args[3];
        if (!--noptargs) {
            goto skip_optional_kwonly;
        }
    }
    if (args[4]) {
        varnames_array = args[4];
        if (!--noptargs) {
            goto skip_optional_kwonly;
        }
    }
    if (PyFloat_Check(args[5])) {
        PyErr_SetString(PyExc_TypeError,
                        "integer argument expected, got float" );
        goto exit;
    }
    stack_size = _PyLong_AsInt(args[5]);
    if (stack_size == -1 && PyErr_Occurred()) {
        goto exit;
    }
skip_optional_kwonly:
    return_value = _pyasmer_reset_code_object_impl(module, code, code_bytes, consts_array, names_array, varnames_array, stack_size);

exit:
    return return_value;
}
/*[clinic end generated code: output=f82178785b8364d1 input=a9049054013a1b77]*/
