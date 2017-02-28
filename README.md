[![Build Status](https://travis-ci.org/iipeace/guider.svg?branch=master)](https://travis-ci.org/iipeace/guider) 
[![Join the chat at https://gitter.im/guiderchat/Lobby](https://badges.gitter.im/guiderchat/Lobby.svg)](https://gitter.im/guiderchat/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

guider
=======
Do you struggle to improve system performance or to find root cause that makes system abnormal?   
Guider is made to measure system resource usage and to give user hints to improve system performance.   
You can trace and analyze resource usage of thread, process, function with this tool.   

Guider pursues three characteristics.
>1. easy to use: just run without install or setting
>2. measure correct: measure time in ms and size in MB/KB
>3. integrate functions: show cpu / memory / disk usage per thread / process / function (user/kernel)


How to use
=======

```
Input command as bellow to start accurate profiling (thread mode)
# guider.py record 

Input "Ctrl + c" key to finish accurate profiling (thread mode)

Input command as bellow to start realtime profiling (top mode)
$ guider.py top 
```


Requirement
=======

```
- linux kernel (>= 3.0)
- python (>= 2.7)
- root permission (except for top mode)
- kernel configuration (except for top mode)
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
[record mode]
    top        [top]
    record     [thread]
    record -y  [system]
    record -f  [function]
    record -F  [file]
[control mode]
    list
    start|stop|send [pid]
[record options]
    -e  [enable_optionsPerMode:bellowCharacters]
          [function] {m(em)|b(lock)|h(eap)|p(ipe)}
          [top]      {t(hread)|d(isk)|I(mage)|f(ile)|g(raph)}
          [thread]   {m(em)|b(lock)|i(rq)|p(ipe)|r(eset)|g(raph)|f(utex)}
    -d  [disable_optionsPerMode:bellowCharacters]
          [thread]   {c(pu)}
          [function] {c(pu)|u(ser)}
    -s  [save_traceData:dir/file]
    -S  [sort_output:c(pu)/m(em)/b(lock)/w(fc)]
    -u  [run_inBackground]
    -W  [wait_forSignal]
    -R  [record_repeatedly:interval,count]
    -b  [set_bufferSize:kb]
    -D  [trace_threadDependency]
    -t  [trace_syscall:syscalls]
    -T  [set_fontPath]
    -x  [set_addressForLocalServer:ip:port]
    -X  [set_requestToRemoteServer:req@ip:port]
    -j  [set_reportPath:dir]
    -N  [set_addressForReport:req@ip:port]
    -n  [set_addressForPrint:ip:port]
    -C  [set_commandScriptPath:file]
[analysis options]
    -o  [save_outputData:dir]
    -P  [group_perProcessBasis]
    -p  [show_preemptInfo:tids]
    -l  [set_addr2linePath:file]
    -r  [set_targetRootPath:dir]
    -I  [set_inputPath:file]
    -q  [configure_taskList]
[common options]
    -a  [show_allInfo]
    -i  [set_interval:sec]
    -g  [filter_specificGroup:comms|tids]
    -A  [set_arch:arm|x86|x64]
    -c  [set_customEvent:event:filter]
    -v  [verbose]
```
