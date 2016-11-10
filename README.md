# guider
Are you struggle to improve system performance or to find root cause that makes system abnormal?   
Guider is made to measure system resource usage and to give user hints to improve system performance.   
You can profile resource usage of thread, process, function with this tool.   

Guider pursues three characteristics.
>1. easy to use: just run without install or setting
>2. measure correct: measure time in ms and size in MB/KB
>3. integrate functions: show cpu / memory / disk usage per thread / process / function


How to use
=======

```
Input command as bellow to start accurate profile
# guider.py record 

Input "Ctrl + c" key to finish accurate profile

Input command as bellow to start realtime profile
$ guider.py top 
```


Requirement
=======

```
- linux kernel (>= 3.0)
- python (>= 2.7)
- root permission (for recording thread activity)
```


Build
=======

```
Input command as bellow to make guider lighter
$ make

Then bytecode object and library are created
bytecode object (guider.pyc) is able to be launched by guider script
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

[ Optional ]
CONFIG_DYNAMIC_FTRACE
CONFIG_HAVE_DYNAMIC_FTRACE
CONFIG_FTRACE_SYSCALLS
CONFIG_HAVE_SYSCALL_TRACEPOINTS
CONFIG_TRACE_IRQFLAGS
CONFIG_TRACE_IRQFLAGS_SUPPORT
CONFIG_STACKTRACE
CONFIG_STACKTRACE_SUPPORT
CONFIG_USER_STACKTRACE_SUPPORT
```


Options
=======

* Use comma(,) as delimiter for multiple values

```
        [mode]
                    [thread]
                top [top]
                -y  [system]
                -f  [function]
                -F  [file]
        [record|top]
                -e  [enable_optionsPerMode:bellowCharacters]
                          [top] {t(hread)|d(isk)}
                          [function] {m(em)|b(lock)|h(eap)|p(ipe)}
                          [thread] {m(em)|b(lock)|i(rq)|p(ipe)|r(eset)|g(raph)|f(utex)}
                -d  [disable_optionsPerMode:bellowCharacters]
                          [function] {c(pu)|u(user)}
                -s  [save_traceData:dir/file]
                -S  [sort_output:c(pu)/m(em)/b(lock)/w(fc)]
                -u  [run_inBackground]
                -W  [wait_forSignal]
                -R  [record_repeatedly:interval,count]
                -b  [set_bufferSize:kb]
                -D  [trace_threadDependency]
                -t  [trace_syscall:syscalls]
        [analysis]
                -o  [save_outputData:dir]
                -a  [show_allInfo]
                -i  [set_interval:sec]
                -p  [show_preemptInfo:tids]
                -l  [input_addr2linePath:file]
                -r  [input_targetRootPath:dir]
                -q  [make_taskchain]
        [common]
                -g  [filter_specificGroup:comms|tids]
                -A  [set_arch:arm|x86|x64]
                -c  [set_customEvent:event:filter]
                -v  [verbose]
```
