/*
 * Interfacing python code with c code
 *
 * Copyright (c) 2018 Peace Lee <iipeace5@gmail.com>
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 2 of the License, or (at your option)
 * any later version.
 *
 */

#include <Python.h>

static PyObject *
guider_getpid(PyObject *self, PyObject *args)
{
    const char *name;

    if (!PyArg_ParseTuple(args, "s", &name))
    {
        return NULL;
    }

    printf("called getpid with %s!\n", name);

    //Py_RETURN_NONE;
    //return Py_BuildValue("s", "Hello, Python extensions!!");
    return Py_BuildValue("i", getpid());
}

static PyMethodDef guiderMethods[] = {
    {"getpid", guider_getpid, METH_VARARGS, "interface for getpid"},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initguider(void)
{
    (void) Py_InitModule("guider", guiderMethods);
}
