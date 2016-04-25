# guider
Are you struggle to improve system performance or to find root cause that makes system abnormal?
guider is made to measure system resource usage per thread and to give user hints to improve system performance.
you can use this tool if only some ftrace options are enabled in linux kernel.

guider persues three characteristics.
>1. easy to use: just run by linux shell without install or setting
>2. measure correct: measure time in ms and size in MB
>3. integrate function: show cpu / memory / disk usage per thread in a page 


How to use
=======

```
input command as bellow for starting profile
# guider.py record 

input "Ctrl + c" key for finishing profile
```


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
+ CONFIG_NOP_TRACER=y
+ CONFIG_HAVE_FUNCTION_TRACER=y
+ CONFIG_HAVE_DYNAMIC_FTRACE=y
+ CONFIG_HAVE_DYNAMIC_FTRACE_WITH_REGS=y
+ CONFIG_HAVE_FTRACE_MCOUNT_RECORD=y
+ CONFIG_HAVE_SYSCALL_TRACEPOINTS=y
+ CONFIG_HAVE_FENTRY=y
+ CONFIG_HAVE_C_RECORDMCOUNT=y
+ CONFIG_TRACER_MAX_TRACE=y
+ CONFIG_TRACE_CLOCK=y
+ CONFIG_RING_BUFFER=y
+ CONFIG_EVENT_TRACING=y
+ CONFIG_CONTEXT_SWITCH_TRACER=y
+ CONFIG_RING_BUFFER_ALLOW_SWAP=y
+ CONFIG_TRACING=y
+ CONFIG_GENERIC_TRACER=y
+ CONFIG_TRACING_SUPPORT=y
+ CONFIG_FTRACE=y
+ CONFIG_FUNCTION_TRACER=y
+ CONFIG_SCHED_TRACER=y
+ CONFIG_FTRACE_SYSCALLS=y
+ CONFIG_STACK_TRACER=y
+ CONFIG_BLK_DEV_IO_TRACE=y
+ CONFIG_DYNAMIC_FTRACE=y
+ CONFIG_DYNAMIC_FTRACE_WITH_REGS=y
+ CONFIG_FUNCTION_PROFILER=y
+ CONFIG_FTRACE_MCOUNT_RECORD=y
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
-c[ready_compareUsage]

-a[show_allThreads]
-i[set_interval:sec]
-g[show_onlyGroup:comms]
-q[make_taskchain]

-w[show_threadDependency]
-p[show_preemptInfo:tids]
-t[trace_syscall:syscallNums]

-f[run_functionProfileMode:event]
-l[input_addr2linePath:file]
-j[input_targetRootPath:dir]

-m[run_pageProfileMode]
```
