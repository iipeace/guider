[![Build Status](https://travis-ci.org/iipeace/guider.svg?branch=master)](https://travis-ci.org/iipeace/guider) 
[![Coverity](https://scan.coverity.com/projects/15302/badge.svg)](https://scan.coverity.com/projects/iipeace-guider) 
[![PyPI](https://img.shields.io/pypi/v/guider.svg)](https://pypi.org/project/guider/)
[![license](http://img.shields.io/badge/license-GNU-blue.svg)](https://raw.githubusercontent.com/iipeace/guider/master/LICENSE)
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


Output
=======
    [Top Info] [Time: 2863246.420] [Interval: 1.0] [Ctxt: 1711] [Fork: 0] [IRQ: 898] [Core: 12] [Task: 337/814] [RAM: 64374] [Swap: 65477] [Unit: %/MB/NR]
    ==========================================================================================================================================================
      ID   | CPU (Usr/Ker/Blk/IRQ)| Mem (Free/Anon/File/Slab)| Swap (Used/ InOut )| Reclaim  | BlkRW | NrFlt | NrBlk | NrSIRQ  | NrMlk | NrDrt  |   NetIO    |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
    Total  |  0 %( 0 / 0 / 0 / 0 )|60942( -2 / 0  / 0  / 0  )| 481  ( 0  /  0/0  )|   0/0    |  0/0  |   0   |   0   |   125   |  13   |   9    |   3K/2K    |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
    Core/0 |  0 %( 0 / 0 / 0 / 0 )|                                                                                                     | 1171 Mhz [1171-3418]
    Core/1 |  0 %( 0 / 0 / 0 / 0 )|                                                                                                     | 1171 Mhz [1171-3418]
    Core/2 |  0 %( 0 / 0 / 0 / 0 )|                                                                                                     | 1171 Mhz [1171-3418]
    Core/3 |  0 %( 0 / 0 / 0 / 0 )|                                                                                                     | 1171 Mhz [1171-3418]
    Core/4 |  0 %( 0 / 0 / 0 / 0 )|                                                                                                     | 1171 Mhz [1171-3418]
    Core/5 | 17 %(17 / 0 / 0 / 0 )|#################                                                                                    | 1171 Mhz [1171-3418]
    Core/6 |  0 %( 0 / 0 / 0 / 0 )|                                                                                                     | 3418 Mhz [1171-3418]
    Core/7 |  0 %( 0 / 0 / 0 / 0 )|                                                                                                     | 1171 Mhz [1171-3418]
    Core/8 |  0 %( 0 / 0 / 0 / 0 )|                                                                                                     | 1171 Mhz [1171-3418]
    Core/9 |  0 %( 0 / 0 / 0 / 0 )|                                                                                                     | 1171 Mhz [1171-3418]
    Core/10|  0 %( 0 / 0 / 0 / 0 )|                                                                                                     | 1171 Mhz [1171-3418]
    Core/11|  0 %( 0 / 0 / 0 / 0 )|                                                                                                     | 1171 Mhz [1171-3418]
    ==========================================================================================================================================================
        Process      ( ID  / Pid / Nr / Pri)| CPU(Usr/Ker/Dly)|  Mem(RSS/Txt/Shr/Swp)| Blk( RD / WR /NrFlt)| Yld | Prmt | FD | LifeTime|    SignalHandler    |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
            synergyc ( 3602/    1/   3/C  0)|  17( 17/  0/  -)|  285(152/  0/  1/  0)|   0(   -/   -/    0)|    -|     -|  64|795:19:42|      180000200      |
       firewire_ohci (  216/    2/   1/C-20)|   0(  0/  0/  -)|    0(  0/  0/  0/  -)|   0(   -/   -/    0)|    -|     -|  64|795:20:45|                     |
     chromium-browse ( 3715/ 3711/   1/C  0)|   0(  0/  0/  -)|  654(  3/ 40/  0/  7)|   0(   -/   -/    0)|    -|     -| 256|795:19:29|      1800104e8      |
              vsftpd ( 1306/    1/   1/C  0)|   0(  0/  0/  -)|   22(  0/  0/  0/  0)|   0(   -/   -/    0)|    -|     -|  64|795:20:41|        12001        |
            firewire (  215/    2/   1/C-20)|   0(  0/  0/  -)|    0(  0/  0/  0/  -)|   0(   -/   -/    0)|    -|     -|  64|795:20:45|                     |
           scsi_eh_5 (  224/    2/   1/C  0)|   0(  0/  0/  -)|    0(  0/  0/  0/  -)|   0(   -/   -/    0)|    -|     -|  64|795:20:45|                     |
      NetworkManager ( 1147/    1/   4/C  0)|   0(  0/  0/  -)|  335(  4/  1/  3/  0)|   0(   -/   -/    0)|    -|     -|  64|795:20:42|      180010000      |
     unity-panel-ser (11628/ 1803/   3/C  0)|   0(  0/  0/  -)|  476( 15/  0/ 10/  0)|   0(   -/   -/    0)|    -|     -|  64|  1:46:31|      180004002      |
     Plex Media Serv ( 2956/ 2931/  16/C  0)|   0(  0/  0/  -)|  436( 40/  9/  9/ 29)|   0(   -/   -/    0)|    -|     -| 128|795:20:34|      1800044ee      |
               getty ( 1785/    1/   1/C  0)|   0(  0/  0/  -)|   17(  0/  0/  0/  0)|   0(   -/   -/    0)|    -|     -|  64|795:20:41|                     |
     unity-scope-loa ( 8422/ 1803/   4/C  0)|   0(  0/  0/  -)|  652( 23/  0/ 11/  0)|   0(   -/   -/    0)|    -|     -| 128| 22:14:19|      180000000      |
           scsi_eh_0 (  219/    2/   1/C  0)|   0(  0/  0/  -)|    0(  0/  0/  0/  -)|   0(   -/   -/    0)|    -|     -|  64|795:20:45|                     |
     chromium-browse ( 4348/ 3715/  10/C  0)|   0(  0/  0/  -)| 1105( 31/ 40/ 13/ 23)|   0(   -/   -/    0)|    -|     -| 512|795:17:56|      1c0014eed      |
                bash ( 4027/ 3565/   1/C  0)|   0(  0/  0/  -)|   26(  3/  0/  1/  1)|   0(   -/   -/    0)|    -|     -| 256|795:19: 1|      4b817efb       |
     indicator-datet ( 2097/ 1803/   6/C  0)|   0(  0/  0/  -)| 1133(  4/  0/  3/  1)|   0(   -/   -/    0)|    -|     -|  64|795:20:41|      180000000      |
         gvfsd-trash ( 2658/ 1803/   4/C  0)|   0(  0/  0/  -)|  421(  2/  0/  2/  0)|   0(   -/   -/    0)|    -|     -|  64|795:20:39|      180000000      |
     indicator-bluet ( 2091/ 1803/   3/C  0)|   0(  0/  0/  -)|  256(  1/  0/  1/  0)|   0(   -/   -/    0)|    -|     -|  64|795:20:41|      180000000      |
               osspd ( 1610/    1/  12/C  0)|   0(  0/  0/  -)|  419(  0/  0/  0/  4)|   0(   -/   -/    0)|    -|     -|  64|795:20:41|      180004003      |
     indicator-power ( 2093/ 1803/   3/C  0)|   0(  0/  0/  -)|  270(  2/  0/  2/  0)|   0(   -/   -/    0)|    -|     -|  64|795:20:41|      180000000      |
     upstart-event-b ( 1910/ 1803/   1/C  0)|   0(  0/  0/  -)|   20(  1/  0/  0/  0)|   0(   -/   -/    0)|    -|     -|  64|795:20:41|      180014002      |
     chromium-browse ( 3711/ 3692/   1/C  0)|   0(  0/  0/  -)|  654(  7/ 40/  4/  7)|   0(   -/   -/    0)|    -|     -| 256|795:19:30|      1800104e8      |
     chromium-browse ( 4472/ 3715/  10/C  0)|   0(  0/  0/  -)| 1092( 43/ 40/ 23/ 10)|   0(   -/   -/    0)|    -|     -| 512|795:17:50|      1c0014eed      |
        rtkit-daemon ( 2189/    1/   3/C  1)|   0(  0/  0/  -)|  164(  1/  0/  0/  0)|   0(   -/   -/    0)|    -|     -|  64|795:20:41|      180000000      |
     chromium-browse ( 4306/ 3715/  10/C  0)|   0(  0/  0/  -)| 1310(152/ 40/ 77/ 18)|   0(   -/   -/    0)|    -|     -| 512|795:17:58|      1c0014eed      |
     ----------------------------------------------------------------------------------------------------------------------------------------------------------

>>>
           
    [Thread Info] [ Elapsed: 2.050 ] [ Start: 2849868.198 ] [ Running: 112 ] [ CtxSwc: 3357 ] [ LogSize: 4054 KB ] [ Unit: Sec/MB/NR ]
    ==========================================================================================================================================================
    __________Thread Info___________|_____________CPU Info______________|______SCHED Info______|________BLOCK Info________|_____________MEM Info_____________|
                                    |                                   |                      |                          |                                  |
                Name(  Tid/  Pid)|LF|Usage(    %)|Delay(  Max)|Pri| IRQ |  Yld| Lose|Steal| Mig| Read( MB/  Cnt)|WCnt( MB)| Sum(Usr/Buf/Ker)|Rcl|Wst|DRcl(Nr)|
    ==========================================================================================================================================================
    # CPU: 12
 
              CORE/0(-----/-----)|--| 0.00(  0.1)| 0.00( 0.00)|  0| 0.00|    7|    -|    -|   -| 0.00(  0/    1)|   0(  0)|   0(  0/  0/  0)|  0|  0|0.00( 0)|
              CORE/1(-----/-----)|--| 0.00(  0.1)| 0.10( 0.00)|  0| 0.00|  147|    -|    -|   -| 0.00(  0/    0)|   0(  0)|   0(  0/  0/  0)|  0|  0|0.00( 0)|
              CORE/2(-----/-----)|--| 0.00(  0.1)| 0.16( 0.00)|  0| 0.00|  211|    -|    -|   -| 0.00(  0/    0)|   0(  0)|   0(  0/  0/  0)|  0|  0|0.00( 0)|
              CORE/3(-----/-----)|--| 0.00(  0.1)| 0.11( 0.00)|  0| 0.00|  181|    -|    -|   -| 0.00(  0/    0)|  32(  0)|   0(  0/  0/  0)|  0|  0|0.00( 0)|
              CORE/4(-----/-----)|--| 0.00(  0.1)| 0.11( 0.00)|  0| 0.00|  232|    -|    -|   -| 0.00(  0/    0)|   0(  0)|   0(  0/  0/  0)|  0|  0|0.00( 0)|
              CORE/5(-----/-----)|--| 0.30( 14.8)| 0.18( 0.00)|  0| 0.00|  179|    -|    -|   -| 1.26(  6/  495)|  19(  0)|  61( 57/  0/  3)|  0|  0|0.00( 0)|
              CORE/6(-----/-----)|--| 0.00(  0.0)| 0.35( 0.00)|  0| 0.00|   57|    -|    -|   -| 0.00(  0/    0)|   0(  0)|   0(  0/  0/  0)|  0|  0|0.00( 0)|
              CORE/7(-----/-----)|--| 0.00(  0.0)| 0.60( 0.00)|  0| 0.00|  100|    -|    -|   -| 0.00(  0/    0)|   0(  0)|   0(  0/  0/  0)|  0|  0|0.00( 0)|
              CORE/8(-----/-----)|--| 0.00(  0.0)| 0.44( 0.00)|  0| 0.00|   59|    -|    -|   -| 0.00(  0/    0)|   0(  0)|   0(  0/  0/  0)|  0|  0|0.00( 0)|
              CORE/9(-----/-----)|--| 0.00(  0.0)| 1.94( 0.00)|  0| 0.00|   37|    -|    -|   -| 0.00(  0/    0)|   0(  0)|   0(  0/  0/  0)|  0|  0|0.00( 0)|
             CORE/10(-----/-----)|--| 0.07(  3.4)| 0.00( 0.00)|  0| 0.00|    2|    -|    -|   -| 0.00(  0/    0)|   0(  0)|   0(  0/  0/  0)|  0|  0|0.00( 0)|
             CORE/11(-----/-----)|--| 0.00(  0.0)| 2.05( 0.00)|  0| 0.00|   39|    -|    -|   -| 0.00(  0/    0)|   0(  0)|   0(  0/  0/  0)|  0|  0|0.00( 0)|
 
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
    # Hot: 4
 
            synergyc( 3604/ 3602)|  | 0.17(  8.5)| 0.00( 0.00)|  0| 0.00|    3|   14|    3|   0| 0.00(  0/    0)|   0(  0)|   0(  0/  0/  0)|  0|  0|0.00( 0)|
     arm-starfish-li(16087/16087)|  | 0.13(  6.3)| 0.00( 0.00)|  0| 0.00|    0|   20|  157|   4| 1.26(  6/  496)|   0(  0)|  61( 57/  0/  3)|  0|  0|0.00( 0)|
              guider(16088/16088)|  | 0.07(  3.4)| 0.00( 0.00)|R90| 0.00|    2|    0|    2|   0| 0.00(  0/    0)|   0(  0)|   0(  0/  0/  0)|  0|  0|0.00( 0)|
 
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
       
>>>
       
    [Function CPU Info] [Cnt: 394] [Interval: 8ms] (USER)
    ==========================================================================================================================================================
    __Usage__|___________________Function____________________|_____________________________________________Binary_____________________________________________
    ==========================================================================================================================================================
       99.0% |                    cpuTest                    | /media/disk/work/test/a.out
       +  100.0% | <- startTest [/media/disk/work/test/a.out] <- main [/media/disk/work/test/a.out]
                     <- __libc_start_main [/lib/x86_64-linux-gnu/libc-2.19.so]
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
        0.5% |                    memset                     | /lib/x86_64-linux-gnu/libc-2.19.so
       +  100.0% | <- startTest [/media/disk/work/test/a.out] <- main [/media/disk/work/test/a.out]
                     <- __libc_start_main [/lib/x86_64-linux-gnu/libc-2.19.so]
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
        0.3% |                  _int_malloc                  | /lib/x86_64-linux-gnu/libc-2.19.so
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
        0.3% |               00007f756e3e7ee4                | ??
       +  100.0% | <- 000000000044676f [/media/disk/work/test/a.out]
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
  
    [Function CPU Info] [Cnt: 394] [Interval: 8ms] (KERNEL)
    ==========================================================================================================================================================
    __Usage__|____________________________________________________________________Function____________________________________________________________________
    ==========================================================================================================================================================
      100.0% |                                                          hrtimer_interrupt
       +   99.5% | <- local_apic_timer_interrupt <- smp_apic_timer_interrupt <- apic_timer_interrupt
       +    0.3% | <- local_apic_timer_interrupt <- smp_apic_timer_interrupt <- apic_timer_interrupt <- do_page_fault <- page_fault
       +    0.3% | <- local_apic_timer_interrupt <- smp_apic_timer_interrupt <- apic_timer_interrupt <- __do_fault <- handle_mm_fault <- __do_page_fault
                     <- do_page_fault <- page_fault
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
       
>>>
       
    [Function Page Info] [Total: 11416KB] [Alloc: 11444KB(817)] [Free: 188KB(47)] (USER)
    ==========================================================================================================================================================
     Usage ( Usr  / Buf  / Ker  )|___________________Function____________________|________________LifeTime________________|______________Binary_______________
    ==========================================================================================================================================================
     10256K(  2048/     0/  8208)|                    memset                     | AVR: 1.563 / MIN: 1.560 / MAX: 1.568   | /lib/x86_64-linux-gnu/libc-2.19.so
      +  10256K(  2048/     0/  8208)| <- startTest [/media/disk/work/test/a.out] <- main [/media/disk/work/test/a.out]
                                         <- __libc_start_main [/lib/x86_64-linux-gnu/libc-2.19.so]
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
       960K(   956/     0/     4)|                  _int_malloc                  | AVR: 1.559 / MIN: 1.554 / MAX: 1.560   | /lib/x86_64-linux-gnu/libc-2.19.so
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
        56K(    16/     0/    40)|               00007f756e3e81e7                | AVR: 1.569 / MIN: 1.568 / MAX: 1.569   | ??
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
        44K(    36/     0/     8)|                   sysmalloc                   | AVR: 1.560 / MIN: 1.558 / MAX: 1.568   | /lib/x86_64-linux-gnu/libc-2.19.so
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
        12K(    12/     0/     0)|           elf_machine_rela_relative           | AVR: 1.568 / MIN: 1.568 / MAX: 1.568   | /lib/x86_64-linux-gnu/ld-2.19.so
      +     12K(    12/     0/     0)| <- dl_main [/lib/x86_64-linux-gnu/ld-2.19.so] <- _dl_sysdep_start [/lib/x86_64-linux-gnu/ld-2.19.so]
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
         8K(     8/     0/     0)|                    realloc                    | AVR: 1.568 / MIN: 1.568 / MAX: 1.568   | /lib/x86_64-linux-gnu/ld-2.19.so
      +      4K(     4/     0/     0)| <- _dl_map_object [/lib/x86_64-linux-gnu/ld-2.19.so]
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
         8K(     4/     0/     4)|                    dl_main                    | AVR: 1.568 / MIN: 1.568 / MAX: 1.568   | /lib/x86_64-linux-gnu/ld-2.19.so
      +      8K(     4/     0/     4)| <- _dl_sysdep_start [/lib/x86_64-linux-gnu/ld-2.19.so]
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
  
    [Function Page Info] [Total: 11416KB] [Alloc: 11444KB(817)] [Free: 188KB(47)] (KERNEL)
    ==========================================================================================================================================================
     Usage ( Usr  / Buf  / Ker  )|___________________Function____________________|__________________________________LifeTime__________________________________
    ==========================================================================================================================================================
      8192K(     0/     0/  8192)|          do_huge_pmd_anonymous_page           |                    AVR: 1.563 / MIN: 1.562 / MAX: 1.564
      +   8192K(     0/     0/  8192)| <- handle_mm_fault <- __do_page_fault <- do_page_fault <- page_fault
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
      3084K(  3084/     0/     0)|                handle_mm_fault                |                    AVR: 1.563 / MIN: 1.554 / MAX: 1.569
      +   3076K(  3076/     0/     0)| <- __do_page_fault <- do_page_fault <- page_fault
      +      4K(     4/     0/     0)| <- __get_user_pages <- get_user_pages <- copy_strings.isra.17 <- copy_strings_kernel <- do_execve_common.isra.23
                                         <- SyS_execve <- stub_execve
      +      4K(     4/     0/     0)| <- __do_page_fault <- do_page_fault <- page_fault <- load_elf_binary <- search_binary_handler
                                         <- do_execve_common.isra.23 <- SyS_execve <- stub_execve
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
![guider-graph-image](https://cloud.githubusercontent.com/assets/15862689/23285445/a03e0bf0-fa74-11e6-9f5a-872a3f10fe48.png)    
![guider-chart-image](https://cloud.githubusercontent.com/assets/15862689/24597375/67f31f22-1880-11e7-8290-64554ed2859c.png)

How to use
=======

```
Input command as bellow to start accurate tracing in thread mode
# guider.py record -a

Input "Ctrl + c" key to finish tracing

Input command as bellow to start realtime monitoring in top mode
$ guider.py top 

Input "Ctrl + c" key to finish monitoring 

Input command as bellow to see more examples
$ guider.py -h

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
Enable kernel options as below to take advantage of all the features
And if CONFIG_STRICT_MEMORY_RWX is enabled then disable it

CONFIG_RING_BUFFER
CONFIG_FTRACE
CONFIG_TRACING
CONFIG_TRACING_SUPPORT
CONFIG_EVENT_TRACING
CONFIG_NOP_TRACER
CONFIG_TRACEPOINTS
CONFIG_TASKSTATS
CONFIG_TASK_DELAY_ACCT
CONFIG_TASK_XACCT
CONFIG_TASK_IO_ACCOUNTING
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
CONFIG_PERF_EVENTS 
CONFIG_HW_PERF_EVENT
```


Modes
=======

```
[analysis]
     top        [realtime]
     record     [thread]
     record -y  [system]
     record -f  [function]
     record -F  [file]
     mem        [page]
 [control]
     list|start|stop|send|kill [proc]
 [convenience]
     draw       [image]
     event      [event]
     filetop    [fds]
```


Options
=======

* Use comma(,) as delimiter for multiple option values

```
[record]
     -e  [enable_optionsPerMode:belowCharacters]
           [function] {m(em)|b(lock)|h(eap)|l(ock)|p(ipe)|g(raph)}
           [thread]   {m(em)|b(lock)|i(rq)|l(ock)|n(et)|p(ipe)|
                       P(ower)|r(eset)|g(raph)}
           [top]      {t(hread)|b(lock)|wf(c)|s(tack)|m(em)|w(ss)|
                       P(erf)|G(pu)|i(rq)|ps(S)|u(ss)|I(mage)|a(ffinity)|
                       g(raph)|r(eport)|R(file)|r(ss)|v(ss)|l(leak)}
     -d  [disable_optionsPerMode:belowCharacters]
           [thread]   {c(pu)|a(ll)}
           [function] {c(pu)|a(ll)|u(ser)}
           [top]      {c(pu)|p(rint)|P(erf)|W(chan)|n(net)}
     -s  [save_traceData:path]
     -S  [sort:c(pu)/m(em)/b(lock)/w(fc)/p(id)/n(ew)/r(untime)/f(ile)]
     -u  [run_inBackground]
     -W  [wait_forSignal]
     -b  [set_bufferSize:kb]
     -D  [trace_threadDependency]
     -t  [trace_syscall:syscalls]
     -T  [set_fontPath]
     -j  [set_reportPath:path]
     -U  [set_userEvent:name:func|addr:file]
     -K  [set_kernelEvent:name:func|addr{:%reg/argtype:rettype}]
     -C  [set_commandScriptPath:file]
     -w  [set_customRecordCommand:BEFORE|AFTER|STOP:file{:value}]
     -x  [set_addressForLocalServer:{ip:port}]
     -X  [set_requestToRemoteServer:{req@ip:port}]
     -N  [set_addressForReport:req@ip:port]
     -n  [set_addressForPrint:ip:port]
     -M  [set_objdumpPath:file]
     -k  [set_killList:comms|tids]
 [analysis]
     -o  [save_outputData:path]
     -O  [set_coreFilter:cores]
     -P  [group_perProcessBasis]
     -p  [show_preemptInfo:tids]
     -l  [set_addr2linePath:files]
     -r  [set_targetRootPath:dir]
     -I  [set_inputValue:file|addr]
     -q  [configure_taskList]
     -Z  [convert_textToImage]
     -L  [set_graphLayout:CPU|MEM|IO{:proportion}]
     -m  [set_terminalSize:{rows:cols}]
 [common]
     -a  [show_allInfo]
     -Q  [print_allRowsInaStream]
     -i  [set_interval:sec]
     -R  [set_repeatCount:{interval,}count]
     -g  [set_filter:comms|tids{:files}]
     -A  [set_arch:arm|aarch64|x86|x64]
     -c  [set_customEvent:event:filter]
     -E  [set_errorLogPath:file]
     -H  [set_functionDepth]
     -Y  [set_schedPriority:policy:prio{:pid:ALL}]
     -v  [verbose]
```


Examples
=======

```
[thread mode examples]
     - record cpu usage of threads 
         # ./guider.py record -s .
     - record specific resource usage of threads in background
         # ./guider.py record -s . -e m b i -u 
     - record specific resource usage excluding cpu of threads in background
         # ./guider.py record -s . -e m b i -d c -u
     - record specific systemcalls of specific threads
         # ./guider.py record -s . -t sys_read, write -g 1234
     - record lock events of threads
         # ./guider.py record -s . -e l
     - record specific user function events
         # ./guider.py record -s . -U evt1:func1:/tmp/a.out, evt2:0x1234:/tmp/b.out -M $(which objdump)
     - record specific kernel function events
         # ./guider.py record -s . -K evt1:func1, evt2:0x1234
     - record specific kernel function events with register values
         # ./guider.py record -s . -K strace32:func1:%bp/u32.%sp/s64, strace:0x1234:$stack:NONE
     - record specific kernel function events with return value
         # ./guider.py record -s . -K openfile:getname::**string, access:0x1234:NONE:*string
     - excute special commands before recording
         # ./guider.py record -s . -w BEFORE:/tmp/started:1, BEFORE:ls
     - analyze data by expressing all possible information
         # ./guider.py guider.dat -o . -a -i
     - analyze data on specific interval
         # ./guider.py guider.dat -o . -R 3
     - analyze data including preemption info of specific threads
         # ./guider.py guider.dat -o . -p 1234, 4567
     - analyze specific threads that are involved in the specific processes
         # ./guider.py guider.dat -o . -P -g 1234, 4567
     - draw graph and chart in image file
         # ./guider.py draw guider.dat
 
 [function mode examples]
     - record cpu usage of functions in all threads
         # ./guider.py record -f -s .
     - record cpu usage of specific functions having tid bigger than 1024 in all threads
         # ./guider.py record -f -s . -g 1024\<
     - record specific events of functions of all threads in kernel level
         # ./guider.py record -f -s . -d u -c sched/sched_switch
     - record resource usage of functions of specific threads
         # ./guider.py record -f -s . -e m b h -g 1234
     - excute special commands before recording
         # ./guider.py record -s . -w BEFORE:/tmp/started:1, BEFORE:ls
     - analyze function data for all 
         # ./guider.py guider.dat -o . -r /home/target/root -l $(which arm-addr2line) -a
     - analyze function data for only lower than 3 levels
         # ./guider.py guider.dat -o . -r /home/target/root -l $(which arm-addr2line) -H 3
     - record segmentation fault event of all threads
         # ./guider.py record -f -s . -K segflt:bad_area -ep
     - record blocking event except for cpu usage of all threads
         # ./guider.py record -f -s . -dc -K block:schedule
 
[top mode examples] 
     - show resource usage of processes in real-time
         # ./guider.py top
     - show resource usage of processes with fixed terminal size in real-time
         # ./guider.py top -m
     - show files opened via processes in real-time
         # ./guider.py top -e f
     - show specific files opened via specific processes in real-time
         # ./guider.py top -e f -g init, lightdm : home, var
     - show performance stats of specific processes in real-time
         # ./guider.py top -e P -g init, lightdm
     - show resource usage of processes by sorting memory in real-time
         # ./guider.py top -S m
     - show resource usage of processes by sorting file in real-time
         # ./guider.py top -S f
     - show resource usage of processes only 5 times in real-time
         # ./guider.py top -R 5
     - show resource usage of processes only 5 times per 3 sec interval in real-time
         # ./guider.py top -R 3, 5
     - show resource usage including block of threads per 2 sec interval in real-time
         # ./guider.py top -e t b -i 2 -a
     - show resource usage of specific processes/threads involved in specific process group in real-time
         # ./guider.py top -g 1234,4567 -P
     - record resource usage of processes and write to specific file in real-time
         # ./guider.py top -o . -e p
     - record and print resource usage of processes
         # ./guider.py top -o . -Q
     - record resource usage of processes and write to specific file in background
         # ./guider.py top -o . -u
     - record resource usage of processes, system status and write to specific file in background
         # ./guider.py top -o . -e r -j . -u
     - record resource usage of processes, system status and write to specific file if some events occur
         # ./guider.py top -o . -e r R
     - record resource usage of processes, system status and write to specific image
         # ./guider.py top -o . -e r I
     - record resource usage of processes and write to specific file when specific conditions met
         # ./guider.py top -o . -e R
     - excute special commands every interval
         # ./guider.py top -w AFTER:/tmp/touched:1, AFTER:ls
     - trace memory working set for specific processes
         # ./guider.py top -e w -g chrome
     - draw graph and chart in image file
         # ./guider.py draw guider.out
         # ./guider.py top -I guider.out -e g
     - draw graph and chart for specific process group in image file
         # ./guider.py draw guider.out -g chrome
         # ./guider.py top -I guider.out -e g -g chrome
     - draw cpu and memory graphs of specific processes in image file propotionally
         # ./guider.py draw guider.out -g chrome -L cpu:5, mem:5
     - draw VSS graph and chart for specific processes in image file
         # ./guider.py draw guider.out -g chrome -e v
     - report system status to specific server
         # ./guider.py top -n 192.168.0.5:5555
     - report system status to specific server if only some events occur
         # ./guider.py top -er -N REPORT_ALWAYS@192.168.0.5:5555
     - report system status to specific clients that asked it
         # ./guider.py top -x 5555
     - receive report data from server
         # ./guider.py top -x 5555 -X
     - set configuration file path
         # ./guider.py top -I guider.json
 
 [file mode examples]
     - record memory usage of files mapped to processes
         # ./guider.py record -F -o .
     - record memory usage of files mapped to processes each intervals
         # ./guider.py record -F -i
 
 [etc examples]
     - check property of specific pages
         # ./guider.py mem -g 1234 -I 0x7abc1234-0x7abc6789
     - convert a text fle to a image file
         # ./guider.py guider.out -Z
     - wait for signal
         # ./guider.py record|top -W
     - show guider processes running
         # ./guider.py list
     - send noty signal to guider processes running
         # ./guider.py send
         # ./guider.py kill
     - send stop signal to guider processes running
         # ./guider.py stop
     - send specific signals to specific processes running
         # ./guider.py send -9 1234, 4567
         # ./guider.py kill -9 1234, 4567
     - change priority of tasks
         # ./guider.py record -Y c:-19, r:90:1217, i:0:1209
     - update priority of tasks continuously
         # ./guider.py record -Y r:90:task:ALL
```
