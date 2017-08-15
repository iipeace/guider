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

Visit a bellow link to see output of guider
- https://github.com/iipeace/guider/wiki
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
          [thread]   {m(em)|b(lock)|i(rq)|l(og)|n(et)|p(ipe)|r(eset)|g(raph)|f(utex)}
          [top]      {t(hread)|d(isk)|w(fc)|W(chan)|s(tack)|m(em)|I(mage)|g(raph)|r(eport)|f(ile)}
    -d  [disable_optionsPerMode:bellowCharacters]
          [thread]   {c(pu)}
          [function] {c(pu)|u(ser)}
          [top]      {r(ss)|v(ss)}
    -s  [save_traceData:dir/file]
    -S  [sort_output:c(pu)/m(em)/b(lock)/w(fc)/p(id)/n(ew)/r(untime)]
    -u  [run_inBackground]
    -W  [wait_forSignal]
    -R  [record_repeatedly:interval,count]
    -b  [set_bufferSize:kb]
    -D  [trace_threadDependency]
    -t  [trace_syscall:syscalls]
    -T  [set_fontPath]
    -H  [set_functionDepth]
    -j  [set_reportPath:dir]
    -U  [set_userEvent:name:func|addr:file]
    -K  [set_kernelEvent:name:func|addr{:%reg/argtype:rettype}]
    -C  [set_commandScriptPath:file]
    -w  [set_customRecordCommand:BEFORE|AFTER|STOP:file:value]
    -x  [set_addressForLocalServer:{ip:}port]
    -X  [set_requestToRemoteServer:{req@ip:port}]
    -N  [set_addressForReport:req@ip:port]
    -n  [set_addressForPrint:ip:port]
    -m  [set_objdumpPath:file]
[analysis options]
    -o  [save_outputData:dir]
    -P  [group_perProcessBasis]
    -p  [show_preemptInfo:tids]
    -l  [set_addr2linePath:files]
    -r  [set_targetRootPath:dir]
    -I  [set_inputValue:file|addr]
    -q  [configure_taskList]
    -L  [convert_textToImage]
[common options]
    -a  [show_allInfo]
    -Q  [print_allRows]
    -i  [set_interval:sec]
    -g  [set_filter:comms|tids{:file}]
    -A  [set_arch:arm|x86|x64]
    -c  [set_customEvent:event:filter]
    -E  [set_errorLogPath:file]
    -v  [verbose]
```



Examples
=======

```
[thread mode]
    - record cpu usage of threads
        # ./guider.py record -s .
    - record all resource usage of threads in background
        # ./guider.py record -s . -e mbi -u
    - record all resource usage excluding cpu of threads in background
        # ./guider.py record -s . -e mbi -d c -u
    - record specific systemcalls of specific threads
        # ./guider.py record -s . -t sys_read,sys_write -g 1234
    - record specific user function events
        # ./guider.py record -s . -U evt1:func1:/tmp/a.out,evt2:0x1234:/tmp/b.out -m $(which objdump)
    - record specific kernel function events
        # ./guider.py record -s . -K evt1:func1,evt2:0x1234
    - record specific kernel function events with register values
        # ./guider.py record -s . -K evt1:func1:%bp/u32.%sp/s64,evt2:0x1234:$stack:NONE
    - record specific kernel function events with return value
        # ./guider.py record -s . -K evt1:func1::*string,evt2:0x1234:NONE:**string
    - analize record data by expressing all possible information
        # ./guider.py guider.dat -o . -a -i
    - analize record data including preemption info of specific threads
        # ./guider.py guider.dat -o . -p 1234,4567
    - analize specific threads that are involved in the specific processes
        # ./guider.py guider.dat -o . -P -g 1234,4567
[function mode]
    - record cpu usage of functions in all threads
        # ./guider.py record -f -s .
    - record specific events of only kernel functions in all threads
        # ./guider.py record -f -s . -d u -c sched/sched_switch
    - record all usage of functions in specific threads
        # ./guider.py record -f -s . -e mbh -g 1234
    - analize record data by expressing all possible information
        # ./guider.py guider.dat -o . -r /home/target/root -l $(which arm-addr2line) -a
    - record specific kernel functions in a specific thread
        # ./guider.py record -f -s . -e g -c SyS_read -g 1234
    - record segmentation fault event in all threads
        # ./guider.py record -f -s . -K segflt:bad_area -ep
    - record blocking event without cpu usage in all threads
        # ./guider.py record -f -s . -dc -K block:schedule
[top mode]
    - show real-time resource usage of processes
        # ./guider.py top
    - show real-time file usage of processes
        # ./guider.py top -ef
    - show real-time resource usage of processes by sorting memory
        # ./guider.py top -S m
    - show real-time resource usage including disk of threads per 2 sec interval
        # ./guider.py top -e td -i 2 -a
    - show real-time resource usage of specific processes/threads involved in specific process group
        # ./guider.py top -g 1234,4567 -P
    - record resource usage of processes to the specific file in background
        # ./guider.py top -o . -u
    - record and report system status to the specific file in background
        # ./guider.py top -o . -e r -j . -u
    - record and save system status to the specific file if some events occur
        # ./guider.py top -o . -e r -e f
    - record and report system status to the specific image
        # ./guider.py top -o . -e r -e f
    - convert a analysis text to a graph image
        # ./guider.py top -I guider.out -e g
    - convert a analysis text to a graph image for specific process group
        # ./guider.py top -I guider.out -e g -g chrome
    - convert a analysis text to a graph image for specific process group except for VSS
        # ./guider.py top -I guider.out -e g -g chrome -d v
    - report system status to the specific server
        # ./guider.py top -n 192.168.0.5:5555
    - report system status to the specific server if some events occur
        # ./guider.py top -er -N REPORT_ALWAYS@192.168.0.5:5555
    - record and send analysis output to specific clients that asked dyanmic request
        # ./guider.py top -x 5555
    - receive and print analysis output from client
        # ./guider.py top -x 5555 -X
    - set event configuration file
        # ./guider.py top -I guider.json
[file mode]
    - record memory usage of mapped files to the specific file
        # ./guider.py record -F -o .
    - record memory usage of mapped files and compare each intervals
        # ./guider.py record -F -i
[etc]
    - view page property of specific pages
        # ./guider.py view -g 1234 -I 0x7abc1234-0x7abc6789
    - convert text to image
        # ./guider.py guider.out -L
    - wait for signal
        # ./guider.py record|top -W
    - show running guider processes
        # ./guider.py list
    - send event signal to guider processes
        # ./guider.py send
    - send stop signal to guider processes
        # ./guider.py stop
    - send some signal to specific processes
        # ./guider.py send -9 1234, 4567
```
