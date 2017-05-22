[![Build Status](https://travis-ci.org/iipeace/guider.svg?branch=master)](https://travis-ci.org/iipeace/guider) 
[![Join the chat at https://gitter.im/guiderchat/Lobby](https://badges.gitter.im/guiderchat/Lobby.svg)](https://gitter.im/guiderchat/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

guider
=======
Do you struggle to improve system performance or to find root cause that makes system abnormal?   
Guider is made to measure amount of system resource usage and to trace system behavior.   
You can analyze your performance issues effectively with this tool.   

Guider pursues three characteristics as bellow.
>1. easy to use: just run without installation or setting
>2. measure correctly: time in ms, size in MB
>3. integrate features: show as much information as possible


How to use
=======

```
Input command as bellow to start accurate profiling in thread mode
# guider.py record 

Input command as bellow to start realtime profiling in top mode
$ guider.py top 

Input "Ctrl + c" key to finish profiling 

Input command as bellow to see more examples
$ guider.py -h -a
```


Requirement
=======

```
- linux kernel (>= 3.0)
- python (>= 2.7)
- kernel configuration
```


Build & Installation
=======

```
If you can use PIP in your system then just input command as bellow
# pip install --pre guider

Otherwise download source file from https://github.com/iipeace/guider
And if you want to make guider lighter and faster then input command as bellow
# make && make install
Then you can use "guider" as launcher
```


Kernel Configuration
=======

```
Enable kernel options as bellow for thread / function mode

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
CONFIG_FUNCTION_TRACER
CONFIG_FUNCTION_GRAPH_TRACER
CONFIG_UPROBES
CONFIG_UPROBE_EVENT
CONFIG_KPROBES
CONFIG_KPROBE_EVENTS
```


Options
=======

* Use comma(,) as delimiter for multiple option values

```
[record mode]
    top        [top]
    record     [thread]
    record -y  [system]
    record -f  [function]
    record -F  [file]
    view       [page]
[control mode]
    list
    start|stop|send [pid]
[record options]
    -e  [enable_optionsPerMode:bellowCharacters]
          [function] {m(em)|b(lock)|h(eap)|p(ipe)|g(raph)}
          [thread]   {m(em)|b(lock)|i(rq)|p(ipe)|r(eset)|g(raph)|f(utex)}
          [top]      {t(hread)|d(isk)|w(fc)|W(chan)|I(mage)|f(ile)|g(raph)}
    -d  [disable_optionsPerMode:bellowCharacters]
          [thread]   {c(pu)}
          [function] {c(pu)|u(ser)}
    -s  [save_traceData:dir/file]
    -S  [sort_output:c(pu)/m(em)/b(lock)/w(fc)/p(id)/n(ew)/r(untime)]
    -u  [run_inBackground]
    -W  [wait_forSignal]
    -R  [record_repeatedly:interval,count]
    -b  [set_bufferSize:kb]
    -D  [trace_threadDependency]
    -t  [trace_syscall:syscalls]
    -H  [set_depth]
    -T  [set_fontPath]
    -j  [set_reportPath:dir]
    -C  [set_commandScriptPath:file]
    -x  [set_addressForLocalServer:{ip:}port]
    -X  [set_requestToRemoteServer:{req@ip:port}]
    -N  [set_addressForReport:req@ip:port]
    -n  [set_addressForPrint:ip:port]
[analysis options]
    -o  [save_outputData:dir]
    -P  [group_perProcessBasis]
    -p  [show_preemptInfo:tids]
    -l  [set_addr2linePath:file]
    -r  [set_targetRootPath:dir]
    -I  [set_inputValue:file|addr]
    -q  [configure_taskList]
    -L  [convert_textToImage]
[common options]
    -a  [show_allInfo]
    -i  [set_interval:sec]
    -g  [filter_specificGroup:comms|tids]
    -A  [set_arch:arm|x86|x64]
    -c  [set_customEvent:event:filter]
    -E  [set_errorLogPath:file]
    -v  [verbose]
```
