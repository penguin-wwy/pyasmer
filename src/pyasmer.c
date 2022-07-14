#include "Python.h"
#include "clinic/pyasmer.c.h"

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

Reload module.
[clinic start generated code]*/

static PyObject *
_pyasmer_reset_code_object_impl(PyObject *module, PyObject *code,
                                PyObject *code_bytes, PyObject *consts_array,
                                PyObject *names_array)
/*[clinic end generated code: output=bef5b7900ea8754a input=8a856b4132d13bfb]*/
{
    assert(PyCode_Check(code));
    PyCodeObject *co = (PyCodeObject *) code;
    PyObject *old_obj = NULL;
    if (code_bytes != Py_None) {
        old_obj = co->co_code;
        co->co_code = Py_NewRef(code_bytes);
        Py_DECREF(old_obj);
    }
    if (consts_array != Py_None) {
        old_obj = co->co_consts;
        co->co_consts = Py_NewRef(consts_array);
        Py_DECREF(old_obj);
    }
    if (names_array != Py_None) {
        old_obj = co->co_names;
        co->co_names = Py_NewRef(names_array);
        Py_DECREF(old_obj);
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
