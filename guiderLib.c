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

/*
 * int prctl(int option, unsigned long arg2, unsigned long arg3,
 *      unsigned long arg4, unsigned long arg5);
 */
static PyObject *
guider_prctl(PyObject *self, PyObject *args)
{
    int option, ret;
    unsigned long arg2, arg3, arg4, arg5;

    if (!PyArg_ParseTuple(args, "islll", &option, &arg2, &arg3, &arg4, &arg5))
    {
        return NULL;
    }

    ret = prctl(option, arg2, arg3, arg4, arg5);

    return Py_BuildValue("i", ret);
}

/*
 * void *mmap(void *addr, size_t length, int prot, int flags,
 *     int fd, off_t offset);
 */
static PyObject *
guider_mmap(PyObject *self, PyObject *args)
{
    int prot, flags, fd;
    unsigned long addr, length, offset, ret;

    if (!PyArg_ParseTuple(args, "lliiil", &addr, &length, &prot, &flags, &fd, &offset))
    {
        return NULL;
    }

    ret = mmap(addr, length, prot, flags, fd, offset);

    return Py_BuildValue("l", ret);
}

/*
 * int munmap(void *addr, size_t length);
 */
static PyObject *
guider_munmap(PyObject *self, PyObject *args)
{
    int ret;
    unsigned long addr, length;

    if (!PyArg_ParseTuple(args, "ll", &addr, &length))
    {
        return NULL;
    }

    ret = munmap(addr, length);

    return Py_BuildValue("i", ret);
}

/*
 * int mincore(void *addr, size_t length, unsigned char *vec);
 */
static PyObject *
guider_mincore(PyObject *self, PyObject *args)
{
    int ret;
    char *vec;
    unsigned long addr, length;

    if (!PyArg_ParseTuple(args, "lls#", &addr, &length, &vec))
    {
        return NULL;
    }

    ret = mincore(addr, length, vec);

    return Py_BuildValue("i", ret);
}

static PyMethodDef guiderMethods[] = {
    {"prctl", guider_prctl, METH_VARARGS, "prctl()"},
    {"mmap", guider_mmap, METH_VARARGS, "mmap()"},
    {"munmap", guider_munmap, METH_VARARGS, "munmap()"},
    {"mincore", guider_mincore, METH_VARARGS, "mincore()"},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initguider(void)
{
    (void) Py_InitModule("guider", guiderMethods);
}
