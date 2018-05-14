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

#define _GNU_SOURCE  
#include <unistd.h>
#include <sys/syscall.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/ptrace.h>
#include <linux/perf_event.h>
#include <sys/prctl.h>
#include <sys/mman.h>
#include <sys/resource.h>
#include <sched.h>
#include <inttypes.h>
#include <Python.h>

static PyObject *
guider_check(PyObject *self, PyObject *args)
{
    Py_RETURN_NONE;
}

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
    void *ret;
    int prot, flags, fd;
    unsigned long addr, length, offset;

    if (!PyArg_ParseTuple(args, "lliiil", &addr, &length, &prot, &flags, &fd, &offset))
    {
        return NULL;
    }

    ret = mmap((void *)addr, length, prot, flags, fd, offset);

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

    ret = munmap((void *)addr, length);

    return Py_BuildValue("i", ret);
}

/*
 * int mincore(void *addr, size_t length, unsigned char *vec);
 */
static PyObject *
guider_mincore(PyObject *self, PyObject *args)
{
    int ret, page;
    char *vec;
    unsigned long addr, length, tsize;
    PyObject * result;

    if (!PyArg_ParseTuple(args, "ll", &addr, &length))
    {
        return NULL;
    }

    page = getpagesize();
    tsize = (length + page - 1) / page;

    vec = (char *)calloc(1, tsize);
    if (vec == NULL)
        Py_RETURN_NONE;

    ret = mincore((void *)addr, length, vec);
    if (ret < 0)
        Py_RETURN_NONE;

    result = Py_BuildValue("s#", vec, tsize);

    free(vec);

    return result;
}

/*
 * int getrlimit(int resource, struct rlimit *rlim);
 */
static PyObject *
guider_getrlimit(PyObject *self, PyObject *args)
{
    int resource, ret;
    struct rlimit rlim;

    if (!PyArg_ParseTuple(args, "i", &resource))
    {
        return NULL;
    }

    ret = getrlimit(resource, &rlim);

    return Py_BuildValue("i", rlim.rlim_cur);
}

/*
 * int sched_setscheduler(pid_t pid, int policy,
 *     const struct sched_param *param);
 */
static PyObject *
guider_sched_setscheduler(PyObject *self, PyObject *args)
{
    int pid, policy, ret;
    struct sched_param param;

    if (!PyArg_ParseTuple(args, "iii", &pid, &policy, &param.sched_priority))
    {
        return NULL;
    }

    ret = sched_setscheduler(pid, policy, &param);

    return Py_BuildValue("i", ret);
}

/* int perf_event_open(struct perf_event_attr *attr,
 *     pid_t pid, int cpu, int group_fd, unsigned long flags);
 */
static PyObject *
guider_perf_event_open(PyObject *self, PyObject *args)
{
    int fd, type, pid, cpu, group_fd;
    long config, flags;
    struct perf_event_attr pea;

    if (!PyArg_ParseTuple(args, "iliiil", &type, &config, &pid, &cpu, &group_fd, &flags))
    {
        return NULL;
    }

    memset(&pea, 0, sizeof(struct perf_event_attr));
    pea.type = type;
    pea.size = sizeof(struct perf_event_attr);
    pea.config = config;
    pea.disabled = 1;
    //pea.exclude_user = 1;
    //pea.exclude_kernel = 1;
    //pea.exclude_hv = 1;
    //pea.exclude_idle = 1;

    fd = syscall(__NR_perf_event_open, &pea, pid, cpu, group_fd, flags);

    if (fd > 0)
    {
        ioctl(fd, PERF_EVENT_IOC_RESET, 0);
        ioctl(fd, PERF_EVENT_IOC_ENABLE, 0);
    }

    return Py_BuildValue("i", fd);
}

/*
 * int setpriority(int which, int who, int prio);
 */
static PyObject *
guider_setpriority(PyObject *self, PyObject *args)
{
    int which, who, prio, ret;

    if (!PyArg_ParseTuple(args, "iii", &which, &who, &prio))
    {
        return NULL;
    }

    ret = setpriority(which, who, prio);
    if (ret < 0) {
        return NULL;
    } else {
        return Py_BuildValue("i", ret);
    }
}

static PyObject *
guider_perf_event_read(PyObject *self, PyObject *args)
{
    int fd, ret;
    long value = 0;

    if (!PyArg_ParseTuple(args, "i", &fd))
    {
        return NULL;
    }

    ret = read(fd, &value, sizeof(long));
    if (ret > 0) {
        ioctl(fd, PERF_EVENT_IOC_RESET, 0);
        return Py_BuildValue("l", value);
    } else {
        return NULL;
    }
}

/*
 * long ptrace(enum __ptrace_request request, pid_t pid,
 *	void *addr, void *data);
 */
static PyObject *
guider_ptrace(PyObject *self, PyObject *args)
{
    void *addr, *data;
    int request, pid;
    long ret;
    long value = 0;

    if (!PyArg_ParseTuple(args, "iill", &request, &pid, &addr, &data))
    {
        return NULL;
    }

    ret = ptrace(request, pid, addr, data);

    return Py_BuildValue("l", ret);
}

/*
 * int sched_setaffinity(pid_t pid, size_t cpusetsize,
 *      const cpu_set_t *mask);
 */
static PyObject *
guider_sched_setaffinity(PyObject *self, PyObject *args)
{
    cpu_set_t set;
    int pid, ret, i;
    long imask;

    if (!PyArg_ParseTuple(args, "il", &pid, &imask))
    {
        return NULL;
    }

    CPU_ZERO(&set);

    for (i = 0; i < sizeof(imask); i++) {
        if (imask & (1 << i))
            CPU_SET(i, &set);
    }

    ret = sched_setaffinity(pid, sizeof(set), &set);

    return Py_BuildValue("i", ret);
}

/*
 * int sched_getaffinity(pid_t pid, size_t cpusetsize,
 *      cpu_set_t *mask);
 */
static PyObject *
guider_sched_getaffinity(PyObject *self, PyObject *args)
{
    cpu_set_t mask;
    int pid, ret, nrcpus, i;
    long rmask = 0;

    if (!PyArg_ParseTuple(args, "i", &pid))
    {
        return NULL;
    }

    CPU_ZERO(&mask);

    ret = sched_getaffinity(pid, sizeof(cpu_set_t), &mask);
    if (ret < 0)
        return NULL;

    nrcpus = sysconf(_SC_NPROCESSORS_ONLN);
    for (i = 0; i < nrcpus; i++) {
        if (CPU_ISSET(i, &mask))
            rmask |= (1 << i);
    }

    return Py_BuildValue("l", rmask);
}

static PyMethodDef guiderMethods[] = {
    {"check", guider_check, METH_VARARGS, "check"},
    {"prctl", guider_prctl, METH_VARARGS, "prctl()"},
    {"getrlimit", guider_getrlimit, METH_VARARGS, "getrlimit()"},
    {"sched_setscheduler", guider_sched_setscheduler, METH_VARARGS, "sched_setscheduler()"},
    {"setpriority", guider_setpriority, METH_VARARGS, "setpriority()"},
    {"mmap", guider_mmap, METH_VARARGS, "mmap()"},
    {"munmap", guider_munmap, METH_VARARGS, "munmap()"},
    {"mincore", guider_mincore, METH_VARARGS, "mincore()"},
    {"ptrace", guider_ptrace, METH_VARARGS, "ptrace()"},
    {"sched_getaffinity", guider_sched_getaffinity, METH_VARARGS, "sched_getaffinity()"},
    {"sched_setaffinity", guider_sched_setaffinity, METH_VARARGS, "sched_setaffinity()"},
    {"perf_event_open", guider_perf_event_open, METH_VARARGS, "perf_event_open()"},
    {"perf_event_read", guider_perf_event_read, METH_VARARGS, "perf_event_read()"},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initguider(void)
{
    (void) Py_InitModule("guider", guiderMethods);
}
