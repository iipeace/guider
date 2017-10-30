[![Build Status](https://travis-ci.org/iipeace/guider.svg?branch=master)](https://travis-ci.org/iipeace/guider) 
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
       


How to use
=======

```
Input command as bellow to start accurate tracing in thread mode
# guider.py record 

Input "Ctrl + c" key to finish tracing

Input command as bellow to start realtime monitoring in top mode
$ guider.py top 

Input "Ctrl + c" key to finish monitoring 

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
