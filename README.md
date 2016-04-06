# guider
Are you struggle to improve system performance or to find root cause that makes system abnormal?
guider is made to measure system resource usage and to give user hints to improve system performance.
you can use this tool if only some ftrace options are enabled in linux kernel.

Requirement
=======

```
- linux kernel (>= 3.0)
- python (>= 2.7)
- root permission in shell
```

Kernel Configuration
=======

```
+ CONFIG_FTRACE
+ CONFIG_HAVE_DYNAMIC_FTRACE
+ CONFIG_HAVE_SYSCALL_TRACEPOINTS
+ CONFIG_STACKTRACE_SUPPORT
+ CONFIG_TRACE_IRQFLAGS_SUPPORT
+ CONFIG_USER_STACKTRACE_SUPPORT (optional)
```

Options
=======

* Don't use space between option and values
* Use comma(,) as delimiter for multiple values

```
-b[set_perCpuBuffer:kb]
-s[save_traceData:dir]
-o[set_outputFile:dir]
-r[record_repeatData:interval,count]

-e[enable_options:i(rq)|m(em)|f(utex)|g(raph)|p(ipe)|t(ty)]
-d[disable_options:t(ty)]

-a[show_allThreads]
-i[set_interval:sec]
-g[show_onlyGroup:comms]
-q[make_taskchain]

-w[show_threadDependency]
-p[show_preemptInfo:tids]
-t[trace_syscall:syscallNums]

-f[show_functionUsage:event]
-l[input_addr2linePath]
-j[input_targetRootPath]
```
