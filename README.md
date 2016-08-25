# guider
Are you struggle to improve system performance or to find root cause that makes system abnormal?
guider is made to measure system resource usage per thread and to give user hints to improve system performance.
you can use this tool if only some ftrace options are enabled in linux kernel.

guider pursues three characteristics.
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
[ Default ]
CONFIG_RING_BUFFER
CONFIG_FTRACE
CONFIG_TRACING
CONFIG_TRACING_SUPPORT
CONFIG_EVENT_TRACING
CONFIG_NOP_TRACER
CONFIG_TRACEPOINTS
CONFIG_FTRACE_SYSCALLS
CONFIG_HAVE_SYSCALL_TRACEPOINTS
CONFIG_TRACE_IRQFLAGS
CONFIG_TRACE_IRQFLAGS_SUPPORT

[ Optional ]
CONFIG_STACKTRACE
CONFIG_STACKTRACE_SUPPORT
CONFIG_USER_STACKTRACE_SUPPORT
```


Options
=======

* Don't use space between option and values
* Use comma(,) as delimiter for multiple values

```
[mode]
        (default) [thread mode]
        -y [system mode]
        -f [function mode]
        -m [file mode]

[record]
        -b [set_perCpuBufferSize:kb]
        -s [save_traceData:dir]
        -r [record_repeatData:interval,count]
        -e [enable_options:i(rq)|m(em)|f(utex)|g(raph)|p(ipe)|t(ty)]
        -d [disable_options:c(pu)|b(lock)|t(ty)]
        -t [trace_syscall:syscallNums]

[analysis]
        -o [set_outputFile:dir]
        -a [show_allInfo]
        -i [set_interval:sec]
        -w [show_threadDependency]
        -p [show_preemptInfo:tids]
        -l [input_addr2linePath:path]
        -j [input_targetRootPath:dir]
        -q [make_taskchain]

[common]
        -g [filter_specificGroup:comms|tids]

```
