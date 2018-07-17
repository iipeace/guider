[![Build Status](https://travis-ci.org/iipeace/guider.svg?branch=master)](https://travis-ci.org/iipeace/guider) 
[![Coverity](https://scan.coverity.com/projects/15302/badge.svg)](https://scan.coverity.com/projects/iipeace-guider) 
[![PyPI](https://img.shields.io/pypi/v/guider.svg)](https://pypi.org/project/guider/)
[![license](http://img.shields.io/badge/license-GNU-blue.svg)](https://raw.githubusercontent.com/iipeace/guider/master/LICENSE)
[![Join the chat at https://gitter.im/guiderchat/Lobby](https://badges.gitter.im/guiderchat/Lobby.svg)](https://gitter.im/guiderchat/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

introduction
=======
<pre><code>
                _      _
   __ _  _   _ (_)  __| |   
  / _` || | | || | / _` | / _ \| '__|   
 | (_| || |_| || || (_| ||  __/| |   
  \__, | \__,_||_| \__,_| \___||_|   
   |___/   

</pre></code>

Do you struggle to improve system performance or to find root cause that makes system abnormal?   
Guider is made to measure amount of system resource usage and to trace system behavior.   
You can analyze your performance issues effectively with this tool.   

Guider pursues characteristics as bellow.
>1. Easy to use: just run without any setting and package installation
>2. Measure correctly: count, time in from us, size in from byte
>3. Integrate features: show as much information as possible
>4. Provides all functions for experiment and analysis 


Output
=======
    # guider.py top -a

    [Top Info] [Time: 7140056.120] [Interval: 1.0] [Ctxt: 52687] [Life: +0/─0] [IRQ: 12517] [Core: 24] [Task: 326/433] [RAM: 63876] [Swap: 65491] (Unit: %/MB/NR)
               [Cycle: 2G / Inst: 6G / IPC: 2.45 / CacheMiss: 77K(6%) / BranchMiss: 857K(0%) / Clock: 22G / MinFlt: 4 / MajFlt: 0]
    ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
      ID   │ CPU (Usr/Ker/Blk/IRQ)│ Mem (Diff/ User/Cache/Kern)│ Swap (Diff/  I/O  )│NrPgRclm │ BlkRW │ NrFlt │ NrBlk │ NrSIRQ │ NrMlk │ NrDrt  │  Network   │
    ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    Total  │  6 %( 4 / 0 / 0 / 0 )│11074(   0/  905/50751/1146)│  0   ( 0  /  0/0  )│   0/0   │  0/0  │   0   │   0   │  1658  │   0   │   7    │   1K/11K   │
    ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    Core/0 │  1 %( 0 / 0 / 0 / 0 )│                                                                   │   powersave   │  0─0   │   ? C │ 1288 Mhz [1171─2441]│
    Core/1 │  1 %( 0 / 0 / 0 / 0 )│                                                                   │   powersave   │  0─1   │   ? C │ 1530 Mhz [1171─2441]│
    Core/2 │  1 %( 0 / 0 / 0 / 0 )│                                                                   │   powersave   │  0─2   │   ? C │ 1171 Mhz [1171─2441]│
    Core/3 │  1 %( 0 / 0 / 0 / 0 )│                                                                   │   powersave   │  0─3   │   ? C │ 1173 Mhz [1171─2441]│
    Core/4 │  8 %( 1 / 2 / 0 / 0 )│#####                                                              │   powersave   │  0─4   │   ? C │ 1171 Mhz [1171─2441]│
    Core/5 │  1 %( 0 / 0 / 0 / 0 )│                                                                   │   powersave   │  0─5   │   ? C │ 1175 Mhz [1171─2441]│
    Core/6 │  1 %( 0 / 0 / 0 / 0 )│                                                                   │   powersave   │  1─0   │   ? C │ 2330 Mhz [1171─2441]│
    Core/7 │  1 %( 0 / 0 / 0 / 0 )│                                                                   │   powersave   │  1─1   │   ? C │ 2342 Mhz [1171─2441]│
    Core/8 │  1 %( 0 / 0 / 0 / 0 )│                                                                   │   powersave   │  1─2   │   ? C │ 2367 Mhz [1171─2441]│
    Core/9 │  1 %( 0 / 0 / 0 / 0 )│                                                                   │   powersave   │  1─3   │   ? C │ 2246 Mhz [1171─2441]│
    Core/10│100 %(99 / 0 / 0 / 0 )│###################################################################│   powersave   │  1─4   │   ? C │ 2246 Mhz [1171─2441]│
    Core/11│  1 %( 0 / 0 / 0 / 0 )│                                                                   │   powersave   │  1─5   │   ? C │ 2290 Mhz [1171─2441]│
    Core/12│  1 %( 0 / 0 / 0 / 0 )│                                                                   │   powersave   │  0─0   │   ? C │ 1171 Mhz [1171─2441]│
    Core/13│  4 %( 3 / 0 / 0 / 0 )│##                                                                 │   powersave   │  0─1   │   ? C │ 1953 Mhz [1171─2441]│
    Core/14│  1 %( 0 / 0 / 0 / 0 )│                                                                   │   powersave   │  0─2   │   ? C │ 1952 Mhz [1171─2441]│
    Core/15│  1 %( 0 / 0 / 0 / 0 )│                                                                   │   powersave   │  0─3   │   ? C │ 1171 Mhz [1171─2441]│
    Core/16│ 12 %( 2 / 3 / 0 / 0 )│########                                                           │   powersave   │  0─4   │   ? C │ 1953 Mhz [1171─2441]│
    Core/17│  1 %( 0 / 0 / 0 / 0 )│                                                                   │   powersave   │  0─5   │   ? C │ 1846 Mhz [1171─2441]│
    Core/18│  1 %( 0 / 0 / 0 / 0 )│                                                                   │   powersave   │  1─0   │   ? C │ 2278 Mhz [1171─2441]│
    Core/19│  1 %( 0 / 0 / 0 / 0 )│                                                                   │   powersave   │  1─1   │   ? C │ 2243 Mhz [1171─2441]│
    Core/20│  1 %( 0 / 0 / 0 / 0 )│                                                                   │   powersave   │  1─2   │   ? C │ 2247 Mhz [1171─2441]│
    Core/21│  1 %( 0 / 0 / 0 / 0 )│                                                                   │   powersave   │  1─3   │   ? C │ 2246 Mhz [1171─2441]│
    Core/22│  1 %( 0 / 0 / 0 / 0 )│                                                                   │   powersave   │  1─4   │   ? C │ 2440 Mhz [1171─2441]│
    Core/23│  1 %( 0 / 0 / 0 / 0 )│                                                                   │   powersave   │  1─5   │   ? C │ 2393 Mhz [1171─2441]│
    ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
        Process      (  PID/ PPID/  Nr/ Pri)│ CPU(Usr/Ker/Dly)│  Mem(RSS/Txt/Shr/Swp)│ Blk( RD / WR /NrFlt)│ Yld │ Prmt │ FD │ LifeTime│     WaitChannel     │
    ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
                 yes ( 2075/ 9085/   1/C  0)│  99( 99/  0/  0)│    8(  0/  0/  0/  0)│   0(   ─/   ─/    0)│    0│     0│ 256│  0: 3:43│       RUNNING       │
               a.out ( 2082/ 9085/   3/C  0)│  16(  6/ 10/  ─)│   30(  1/  0/  1/  0)│   0(   ─/   ─/    0)│    0│     0│ 256│  0: 3:36│ futex_wait_queue_me │
              guider ( 2182/ 9085/   1/C  0)│   3(  3/  0/  0)│  101( 62/  2/  5/  0)│   0(   ─/   ─/    0)│    1│     1│1024│  0: 0: 2│       RUNNING       │
                bash ( 6960/ 6959/   1/C  0)│   0(  0/  0/  ─)│   24(  6/  0/  3/  0)│   0(   ─/   ─/    0)│    0│     0│ 256│ 20:26:27│       do_wait       │
                  vi ( 7200/ 7197/   1/C  0)│   0(  0/  0/  ─)│   58(  8/  1/  5/  0)│   0(   ─/   ─/    0)│    0│     0│  64│ 20:24:23│poll_schedule_timeout│
                bash ( 7916/ 6959/   1/C  0)│   0(  0/  0/  ─)│   24(  6/  0/  3/  0)│   0(   ─/   ─/    0)│    0│     0│ 256│ 19:57:58│       do_wait       │
                nmbd ( 2960/    1/   1/C  0)│   0(  0/  0/  ─)│   91(  4/  3/  4/  0)│   0(   ─/   ─/    0)│    0│     0│  64│ 1K:20:52│poll_schedule_timeout│
               udevd ( 2222/    1/   1/C  0)│   0(  0/  0/  ─)│   21(  2/  0/  1/  0)│   0(   ─/   ─/    0)│    0│     0│  64│ 1K:20:53│       ep_poll       │
       kworker/14:1H ( 3288/    2/   1/C─20)│   0(  0/  0/  ─)│    0(  0/  0/  0/  ─)│   0(   ─/   ─/    0)│    0│     0│  64│ 1K:20:51│    worker_thread    │
              bioset ( 1265/    2/   1/C─20)│   0(  0/  0/  ─)│    0(  0/  0/  0/  ─)│   0(   ─/   ─/    0)│    0│     0│  64│ 1K:20:54│   rescuer_thread    │
       kworker/22:1H ( 1787/    2/   1/C─20)│   0(  0/  0/  ─)│    0(  0/  0/  0/  ─)│   0(   ─/   ─/    0)│    0│     0│  64│ 1K:20:53│    worker_thread    │
     /usr/sbin/apach ( 7221/ 3817/   1/C  0)│   0(  0/  0/  ─)│  250( 51/  0/ 12/  0)│   0(   ─/   ─/    0)│    0│     0│  64│ 20:23:39│   inet_csk_accept   │
                sshd ( 1992/ 1977/   1/C  0)│   0(  0/  0/  0)│  131(  4/  0/  2/  0)│   0(   ─/   ─/    0)│    3│     1│  64│  0: 4:39│poll_schedule_timeout│
               netns (  130/    2/   1/C─20)│   0(  0/  0/  ─)│    0(  0/  0/  0/  ─)│   0(   ─/   ─/    0)│    0│     0│  64│ 1K:20:54│   rescuer_thread    │
        kworker/20:2 ( 1962/    2/   1/C  0)│   0(  0/  0/  0)│    0(  0/  0/  0/  ─)│   0(   ─/   ─/    0)│    1│     0│  64│ 1K:20:53│    worker_thread    │
       kworker/13:1H ( 3286/    2/   1/C─20)│   0(  0/  0/  ─)│    0(  0/  0/  0/  ─)│   0(   ─/   ─/    0)│    0│     0│  64│ 1K:20:51│    worker_thread    │
                bash ( 9085/ 9084/   1/C  0)│   0(  0/  0/  ─)│   23(  5/  0/  3/  0)│   0(   ─/   ─/    0)│    0│     0│ 256│ 1K:47:24│       do_wait       │
     ext4─rsv─conver ( 2079/    2/   1/C─20)│   0(  0/  0/  ─)│    0(  0/  0/  0/  ─)│   0(   ─/   ─/    0)│    0│     0│  64│ 1K:20:53│   rescuer_thread    │
       kworker/12:1H ( 3285/    2/   1/C─20)│   0(  0/  0/  ─)│    0(  0/  0/  0/  ─)│   0(   ─/   ─/    0)│    0│     0│  64│ 1K:20:51│    worker_thread    │
    ───more───

>>>
           
    # guider.py record -a -e m b

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
       
    # guider.py record -f -a

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
       
    # guider.py record -f -a -e m

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
Input a command as bellow to start tracing for all threads.
    # guider.py record -a
And input 'Ctrl + c' on keyboard to finish tracing.

Input a command as bellow to start monitoring for all processes.
    $ guider.py top -a
And Input 'Ctrl + c' on keyboard to finish monitoring.

Input a command as bellow to see more instructions.
    $ guider.py -h

Visit a bellow link to see output of guider.
- https://github.com/iipeace/guider/wiki
```


Requirement
=======

```
- linux kernel (>= 2.6)
- python (>= 2.7)
```


Build & Installation
=======

```
If you can run 'pip' on your system then just input a command as bellow
    $ sudo pip install guider
Then you can use 'guider' command

Otherwise download source from https://github.com/iipeace/guider
Then you can just run "guider.py" but it is little bit heavy 
If you want to run guider lightly then input a command as bellow
    # make && make install
Then you can use 'guider' command
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

CONFIG_TASKSTATS
CONFIG_TASK_DELAY_ACCT
CONFIG_TASK_XACCT
CONFIG_TASK_IO_ACCOUNTING
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
    kill|setsched|cpulimit [proc]
[communication]
    list|start|stop|send|kill [proc]
[convenience]
    draw       [image]
    event      [event]
    threadtop  [thread]
    filetop    [file]
    stacktop   [stack]
```


Options
=======

* Use comma(,) as delimiter for multiple option values

```
[record]
    -e  [enable_optionsPerMode - belowCharacters]
          [function] {m(em)|b(lock)|h(eap)|l(ock)|p(ipe)|g(raph)}
          [thread]   {m(em)|b(lock)|i(rq)|l(ock)|n(et)|p(ipe)|
                      P(ower)|r(eset)|g(raph)}
          [top]      {t(hread)|b(lock)|wf(c)|s(tack)|m(em)|w(ss)|
                      P(erf)|G(pu)|i(rq)|ps(S)|u(ss)|I(mage)|a(ffinity)|
                      g(raph)|r(eport)|R(file)|r(ss)|v(ss)|l(leak)}
    -d  [disable_optionsPerMode - belowCharacters]
          [thread]   {c(pu)|a(ll)}
          [function] {c(pu)|a(ll)|u(ser)}
          [top]      {c(pu)|p(rint)|P(erf)|W(chan)|n(net)|e(ncoding)}
    -s  [save_traceData - path]
    -S  [sort - c(pu)/m(em)/b(lock)/w(fc)/p(id)/n(ew)/r(untime)/f(ile)]
    -u  [run_inBackground]
    -W  [wait_forSignal]
    -b  [set_bufferSize - kb]
    -D  [trace_threadDependency]
    -t  [trace_syscall - syscalls]
    -T  [set_fontPath]
    -j  [set_reportPath - path]
    -U  [set_userEvent - name:func|addr:file]
    -K  [set_kernelEvent - name:func|addr{:%reg/argtype:rettype}]
    -C  [set_commandScriptPath - file]
    -w  [set_customRecordCommand - BEFORE|AFTER|STOP:file{:value}]
    -x  [set_addressForLocalServer - {ip:port}]
    -X  [set_requestToRemoteServer - {req@ip:port}]
    -N  [set_addressForReport - req@ip:port]
    -n  [set_addressForPrint - ip:port]
    -M  [set_objdumpPath - file]
    -k  [set_killList - comms|tids]
[analysis]
    -o  [save_outputData - path]
    -O  [set_coreFilter - cores]
    -P  [group_perProcessBasis]
    -p  [show_preemptInfo - tids]
    -l  [set_addr2linePath - files]
    -r  [set_targetRootPath - dir]
    -I  [set_inputValue - file|addr]
    -q  [configure_taskList]
    -Z  [convert_textToImage]
    -L  [set_graphLayout - CPU|MEM|IO{:proportion}]
    -m  [set_terminalSize - {rows:cols}]
[common]
    -a  [show_allInfo]
    -Q  [print_allRowsInaStream]
    -i  [set_interval - sec]
    -R  [set_repeatCount - {interval,}count]
    -g  [set_filter - comms|tids{:files}]
    -A  [set_arch - arm|aarch64|x86|x64]
    -c  [set_customEvent - event:filter]
    -E  [set_errorLogPath - file]
    -H  [set_functionDepth]
    -Y  [set_schedPriority - policy:prio{:pid:CONT}]
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
    - change priority of task
        # ./guider.py setsched c:-19, r:90:1217, i:0:1209
    - change priority of tasks in a group
        # ./guider.py setsched c:-19, r:90:1217 -P
    - update priority of tasks continuously
        # ./guider.py top -Y r:90:task:ALL
    - limit cpu usage of specific processes
        # ./guider.py cpulimit 1234:40, 5678:10
    - limit cpu usage of specific threads
        # ./guider.py cpulimit 1234:40, 5678:10 -e t
```
