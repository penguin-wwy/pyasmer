#include "Python.h"
#if PY_MINOR_VERSION == 6
#include "clinic/v3_6.h"
#elif PY_MINOR_VERSION == 7
#include "clinic/v3_7.h"
#elif PY_MINOR_VERSION == 8
#include "clinic/v3_8.h"
#elif PY_MINOR_VERSION == 9
#include "clinic/v3_9.h"
#elif PY_MINOR_VERSION == 10
#include "clinic/v3_10.h"
#endif

/*[clinic input]
module _pyasmer
[clinic start generated code]*/
/*[clinic end generated code: output=da39a3ee5e6b4b0d input=987cc8b40a07d2de]*/

/*[clinic input]

_pyasmer.reset_code_object -> object

  code: object
  /
  *
  code_bytes: object = None
  consts_array: object = None
  names_array: object = None
  varnames_array: object = None
  stack_size: int = 0

Reload module.
[clinic start generated code]*/

static PyObject *
_pyasmer_reset_code_object_impl(PyObject *module, PyObject *code,
                                PyObject *code_bytes, PyObject *consts_array,
                                PyObject *names_array,
                                PyObject *varnames_array, int stack_size)
/*[clinic end generated code: output=6f60c4c0c645739d input=6f38925a6105b556]*/
{
    assert(PyCode_Check(code));
    PyCodeObject *co = (PyCodeObject *) code;
    PyObject *old_obj = NULL;
    if (code_bytes != Py_None) {
        old_obj = co->co_code;
        Py_INCREF(code_bytes);
        co->co_code = code_bytes;
        Py_DECREF(old_obj);
    }
    if (consts_array != Py_None) {
        old_obj = co->co_consts;
        Py_INCREF(consts_array);
        co->co_consts = consts_array;
        Py_DECREF(old_obj);
    }
    if (names_array != Py_None) {
        old_obj = co->co_names;
        Py_INCREF(names_array);
        co->co_names = names_array;
        Py_DECREF(old_obj);
    }
    if (varnames_array != Py_None) {
        old_obj = co->co_varnames;
        Py_INCREF(varnames_array);
        co->co_varnames = varnames_array;
        Py_DECREF(old_obj);
        Py_ssize_t size = PyTuple_Size(varnames_array);
        co->co_nlocals = Py_SAFE_DOWNCAST(size, Py_ssize_t, int);
    }
    if (stack_size) {
        co->co_stacksize = stack_size;
    }
    Py_INCREF(Py_None);
    return Py_None;
}

static PyMethodDef pyasmer_functions[] = {
        _PYASMER_RESET_CODE_OBJECT_METHODDEF
        {NULL, NULL, 0, NULL}
};

static struct PyModuleDef pyasmer_module = {
        PyModuleDef_HEAD_INIT,
        .m_name = "_pyasmer",
        .m_doc = "_pyasmer module.",
        .m_size = 0,
        .m_methods = pyasmer_functions
};

PyMODINIT_FUNC
PyInit__pyasmer(void)
{
    return PyModuleDef_Init(&pyasmer_module);
}
