# guider
Are you struggle to improve system performance or to find root cause that makes system abnormal?
Guider is made to measure system resource usage and to give user hints to improve system performance.
You can profile resource usage of thread, process, file, function with this tool.

guider pursues three characteristics.
>1. easy to use: just run without install or setting
>2. measure correct: measure time in ms and size in MB/KB
>3. integrate functions: show cpu / memory / disk usage per thread / process / function


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
- root permission (for recording thread activity)
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

[ Optional ]
CONFIG_DYNAMIC_FTRACE
CONFIG_HAVE_DYNAMIC_FTRACE
CONFIG_TRACE_IRQFLAGS
CONFIG_TRACE_IRQFLAGS_SUPPORT
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
                top [top mode]
                -y [system mode]
                -f [function mode]
                -m [file mode]
        [record|top]
                -s [save_traceData:dir]
                -S [sort_output:c(pu),m(em),b(lock),w(fc)]
                -u [run_inBackground]
                -c [wait_forSignal]
                -e [enable_options:i(rq)|m(em)|f(utex)|g(raph)|p(ipe)|w(arning)|t(hread)|r(eset)|d(isk)]
                -d [disable_options:c(pu)|b(lock)]
                -r [record_repeatData:interval,count]
                -b [set_bufferSize:kb(record)|10b(top)]
                -w [trace_threadDependency]
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
