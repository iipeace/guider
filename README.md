[![Build Status](https://travis-ci.org/iipeace/guider.svg?branch=master)](https://travis-ci.org/iipeace/guider) 
[![license](http://img.shields.io/badge/license-GNU-blue.svg)](https://raw.githubusercontent.com/iipeace/guider/master/LICENSE)
[![Coverity](https://scan.coverity.com/projects/15302/badge.svg)](https://scan.coverity.com/projects/iipeace-guider) 
[![PyPI version](https://badge.fury.io/py/guider.svg)](https://badge.fury.io/py/guider)
[![Join the chat at https://gitter.im/guiderchat/Lobby](https://badges.gitter.im/guiderchat/Lobby.svg)](https://gitter.im/guiderchat/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

![Guider_Logo_mini](https://user-images.githubusercontent.com/15862689/69008465-3062aa80-098e-11ea-8185-cfb8d7c4aafe.png)

Table of contents
=================
<!--ts-->
   * [Guider](#Guider)
   * [Output](#Output)
   * [How to use](#How-to-use)
   * [Requirement](#Requirement)
   * [Build & Installation](#Build--Installation)
   * [Kernel Configuration](#Kernel-Configuration)
   * [Help](#Help)
<!--te-->

Guider
=======
Guider is an integrated performance analyzer.   
It provides most of the features needed for system performance measurement and analysis.   

The features of Guider are as follows.
* Monitoring
* Profiling
* Visualization
* Control
* Logging
* Test

Guider pursues characteristics as below.
1. Easy to use: just run without any setting and package installation
2. Measure correctly: count, time in from us, size in from byte
3. Provide all features: enough functions for experiment and analysis
4. Submit the report in detail: show as much information as possible

It usually supports all platforms based on the Linux kernel as shown below.
* Android
* distro (Ubuntu, CentOS, RHEL, Linux Mint, Arch Linux, ...)
* webOS
* ccOS
* Tizen
* Windows (Limited)
* macOS (Limited)

Output
=======
    $ guider/guider.py top -a

    [Top Info] [Time: 71406.120] [Interval: 1.0] [Ctxt: 52687] [Life: +0/-0] [IRQ: 12517] [Core: 24] [Task: 326/433] [Load: 0.2/0.4/0.5] [RAM: 63876] [Swap: 65491]
               [Cycle: 2G / Inst: 6G / IPC: 2.45 / CacheMiss: 77K(6%) / BranchMiss: 857K(0%) / Clock: 22G / MinFlt: 4 / MajFlt: 0]
    ==========================================================================================================================================================
      ID   | CPU (Usr/Ker/Blk/IRQ)| Mem (Diff/ User/Cache/Kern)| Swap (Diff/  I/O  )|NrPgRclm | BlkRW | NrFlt | NrBlk | NrSIRQ | NrMlk | NrDrt  |  Network   |
      
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
    Total  |  6 %( 4 / 0 / 0 / 0 )|11074(   0/  905/50751/1146)|  0   ( 0  /  0/0  )|   0/0   |  0/0  |   0   |   0   |  1658  |   0   |   7    |   1K/11K   |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
    Core/0 |  1 %( 0 / 0 / 0 / 0 )|                                                                   |   powersave   |  0-0   |   ? C | 1288 Mhz [1171-2441]|
    Core/1 |  1 %( 0 / 0 / 0 / 0 )|                                                                   |   powersave   |  0-1   |   ? C | 1530 Mhz [1171-2441]|
    Core/2 |  1 %( 0 / 0 / 0 / 0 )|                                                                   |   powersave   |  0-2   |   ? C | 1171 Mhz [1171-2441]|
    Core/3 |  1 %( 0 / 0 / 0 / 0 )|                                                                   |   powersave   |  0-3   |   ? C | 1173 Mhz [1171-2441]|
    Core/4 |  8 %( 1 / 2 / 0 / 0 )|#####                                                              |   powersave   |  0-4   |   ? C | 1171 Mhz [1171-2441]|
    Core/5 |  1 %( 0 / 0 / 0 / 0 )|                                                                   |   powersave   |  0-5   |   ? C | 1175 Mhz [1171-2441]|
    Core/6 |  1 %( 0 / 0 / 0 / 0 )|                                                                   |   powersave   |  1-0   |   ? C | 2330 Mhz [1171-2441]|
    Core/7 |  1 %( 0 / 0 / 0 / 0 )|                                                                   |   powersave   |  1-1   |   ? C | 2342 Mhz [1171-2441]|
    Core/8 |  1 %( 0 / 0 / 0 / 0 )|                                                                   |   powersave   |  1-2   |   ? C | 2367 Mhz [1171-2441]|
    Core/9 |  1 %( 0 / 0 / 0 / 0 )|                                                                   |   powersave   |  1-3   |   ? C | 2246 Mhz [1171-2441]|
    Core/10|100 %(99 / 0 / 0 / 0 )|###################################################################|   powersave   |  1-4   |   ? C | 2246 Mhz [1171-2441]|
    Core/11|  1 %( 0 / 0 / 0 / 0 )|                                                                   |   powersave   |  1-5   |   ? C | 2290 Mhz [1171-2441]|
    Core/12|  1 %( 0 / 0 / 0 / 0 )|                                                                   |   powersave   |  0-0   |   ? C | 1171 Mhz [1171-2441]|
    Core/13|  4 %( 3 / 0 / 0 / 0 )|##                                                                 |   powersave   |  0-1   |   ? C | 1953 Mhz [1171-2441]|
    Core/14|  1 %( 0 / 0 / 0 / 0 )|                                                                   |   powersave   |  0-2   |   ? C | 1952 Mhz [1171-2441]|
    Core/15|  1 %( 0 / 0 / 0 / 0 )|                                                                   |   powersave   |  0-3   |   ? C | 1171 Mhz [1171-2441]|
    Core/16| 12 %( 2 / 3 / 0 / 0 )|########                                                           |   powersave   |  0-4   |   ? C | 1953 Mhz [1171-2441]|
    Core/17|  1 %( 0 / 0 / 0 / 0 )|                                                                   |   powersave   |  0-5   |   ? C | 1846 Mhz [1171-2441]|
    Core/18|  1 %( 0 / 0 / 0 / 0 )|                                                                   |   powersave   |  1-0   |   ? C | 2278 Mhz [1171-2441]|
    Core/19|  1 %( 0 / 0 / 0 / 0 )|                                                                   |   powersave   |  1-1   |   ? C | 2243 Mhz [1171-2441]|
    Core/20|  1 %( 0 / 0 / 0 / 0 )|                                                                   |   powersave   |  1-2   |   ? C | 2247 Mhz [1171-2441]|
    Core/21|  1 %( 0 / 0 / 0 / 0 )|                                                                   |   powersave   |  1-3   |   ? C | 2246 Mhz [1171-2441]|
    Core/22|  1 %( 0 / 0 / 0 / 0 )|                                                                   |   powersave   |  1-4   |   ? C | 2440 Mhz [1171-2441]|
    Core/23|  1 %( 0 / 0 / 0 / 0 )|                                                                   |   powersave   |  1-5   |   ? C | 2393 Mhz [1171-2441]|
    ==========================================================================================================================================================
        Process      (  PID/ PPID/  Nr/ Pri)| CPU(Usr/Ker/Dly)|  Mem(RSS/Txt/Shr/Swp)| Blk( RD / WR /NrFlt)| Yld | Prmt | FD | LifeTime|     WaitChannel     |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
                 yes ( 2075/ 9085/   1/C  0)|  99( 99/  0/  0)|    8(  0/  0/  0/  0)|   0(   -/   -/    0)|    0|     0| 256|  0: 3:43|       RUNNING       |
               a.out ( 2082/ 9085/   3/C  0)|  16(  6/ 10/  -)|   30(  1/  0/  1/  0)|   0(   -/   -/    0)|    0|     0| 256|  0: 3:36| futex_wait_queue_me |
              guider ( 2182/ 9085/   1/C  0)|   3(  3/  0/  0)|  101( 62/  2/  5/  0)|   0(   -/   -/    0)|    1|     1|1024|  0: 0: 2|       RUNNING       |
                bash ( 6960/ 6959/   1/C  0)|   0(  0/  0/  -)|   24(  6/  0/  3/  0)|   0(   -/   -/    0)|    0|     0| 256| 20:26:27|       do_wait       |
                  vi ( 7200/ 7197/   1/C  0)|   0(  0/  0/  -)|   58(  8/  1/  5/  0)|   0(   -/   -/    0)|    0|     0|  64| 20:24:23|poll_schedule_timeout|
                bash ( 7916/ 6959/   1/C  0)|   0(  0/  0/  -)|   24(  6/  0/  3/  0)|   0(   -/   -/    0)|    0|     0| 256| 19:57:58|       do_wait       |
                nmbd ( 2960/    1/   1/C  0)|   0(  0/  0/  -)|   91(  4/  3/  4/  0)|   0(   -/   -/    0)|    0|     0|  64| 1K:20:52|poll_schedule_timeout|
               udevd ( 2222/    1/   1/C  0)|   0(  0/  0/  -)|   21(  2/  0/  1/  0)|   0(   -/   -/    0)|    0|     0|  64| 1K:20:53|       ep_poll       |
       kworker/14:1H ( 3288/    2/   1/C-20)|   0(  0/  0/  -)|    0(  0/  0/  0/  -)|   0(   -/   -/    0)|    0|     0|  64| 1K:20:51|    worker_thread    |
              bioset ( 1265/    2/   1/C-20)|   0(  0/  0/  -)|    0(  0/  0/  0/  -)|   0(   -/   -/    0)|    0|     0|  64| 1K:20:54|   rescuer_thread    |
       kworker/22:1H ( 1787/    2/   1/C-20)|   0(  0/  0/  -)|    0(  0/  0/  0/  -)|   0(   -/   -/    0)|    0|     0|  64| 1K:20:53|    worker_thread    |
     /usr/sbin/apach ( 7221/ 3817/   1/C  0)|   0(  0/  0/  -)|  250( 51/  0/ 12/  0)|   0(   -/   -/    0)|    0|     0|  64| 20:23:39|   inet_csk_accept   |
                sshd ( 1992/ 1977/   1/C  0)|   0(  0/  0/  0)|  131(  4/  0/  2/  0)|   0(   -/   -/    0)|    3|     1|  64|  0: 4:39|poll_schedule_timeout|
               netns (  130/    2/   1/C-20)|   0(  0/  0/  -)|    0(  0/  0/  0/  -)|   0(   -/   -/    0)|    0|     0|  64| 1K:20:54|   rescuer_thread    |
        kworker/20:2 ( 1962/    2/   1/C  0)|   0(  0/  0/  0)|    0(  0/  0/  0/  -)|   0(   -/   -/    0)|    1|     0|  64| 1K:20:53|    worker_thread    |
       kworker/13:1H ( 3286/    2/   1/C-20)|   0(  0/  0/  -)|    0(  0/  0/  0/  -)|   0(   -/   -/    0)|    0|     0|  64| 1K:20:51|    worker_thread    |
                bash ( 9085/ 9084/   1/C  0)|   0(  0/  0/  -)|   23(  5/  0/  3/  0)|   0(   -/   -/    0)|    0|     0| 256| 1K:47:24|       do_wait       |
     ext4-rsv-conver ( 2079/    2/   1/C-20)|   0(  0/  0/  -)|    0(  0/  0/  0/  -)|   0(   -/   -/    0)|    0|     0|  64| 1K:20:53|   rescuer_thread    |
       kworker/12:1H ( 3285/    2/   1/C-20)|   0(  0/  0/  -)|    0(  0/  0/  0/  -)|   0(   -/   -/    0)|    0|     0|  64| 1K:20:51|    worker_thread    |
    ---more---

>>>
           
    $ guider/guider.py ttop 

    [Top Info] [Time: 194025.590] [Interval: 1.0] [Ctxt: 4995] [Life: +0/-0] [OOM: 0] [IRQ: 1879] [Core: 8] [Task: 333/1188] [Load: 3.1/1.9/0.9] [RAM: 62.8G]
    ==========================================================================================================================================================
      ID   |  CPU(Usr/Ker/Blk/IRQ)|  Avl(Diff/ User/Cache/Kern)|  Swap(Diff/ In/Out)| PgRclm  | BlkRW | NrFlt | PrBlk | NrSIRQ | PgMlk | PgDrt  |  Network   |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
    Total  |  3 %( 1 / 0 /23 / 0 )|59874(  -3/ 3110/15153/ 355)|     0(   0/  0/  0)|   0/0   |  0/5  |   0   |   2   |  313   | 1607  | 939290 |    0/0     |
    ==========================================================================================================================================================
              Thread (  TID/  PID/  Nr/ Pri)| CPU(Usr/Ker/Dly)|  VSS(RSS/Txt/Shr/Swp)| Blk(  RD/  WR/NrFlt)| Yld | Prmt | FD | LifeTime|       Process       |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
              guider ( 8160/ 8160/   1/C  0)|   3(  2/  0/  0)|   66( 33/  2/  6/  0)|   0(   -/   -/    0)|    1|     0|2048| 00:00:02|         guider(8160)|
     gnome-terminal- ( 4864/ 4864/   4/C  0)|   1(  0/  0/  -)|  627( 57/  0/ 40/  0)|   0(   -/   -/    0)|    -|     -| 128| 2d:05:52|gnome-terminal-(4864)|
                Xorg ( 1525/ 1525/   2/C  0)|   1(  0/  0/  -)|  431( 84/  0/ 48/  0)|   0(   -/   -/    0)|    -|     -| 128| 2d:05:53|           Xorg(1525)|
                                   [ TOTAL ]|     5(   2/   0)|RSS: 174M / Swp:    0)| 0.0(   -/   -/    0)|      Yld: 1|       Prmt: 0|              Task: 3|
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
    [D]kworker/u16:0 ( 7784/ 7784/   1/C  0)|   0(  0/  0/  -)|    0(  0/  0/  -/  -)|   0(   -/   -/    0)|    -|     -|   -| 00:07:07|                    -|
             [D]pool ( 8024/ 2450/  13/C  0)|   0(  0/  0/  -)| 1025( 82/  1/  -/  -)|   0(   -/   -/    0)|    -|     -|   -| 00:04:31|                    -|
      [D]usb-storage ( 7825/ 7825/   1/C  0)|   0(  0/  0/  -)|    0(  0/  0/  -/  -)|   0(   -/   -/    0)|    -|     -|   -| 00:06:38|                    -|
    ----------------------------------------------------------------------------------------------------------------------------------------------------------

>>>

    # guider/guider.py utop -g yes -H

    [Top Usercall Info] [Time: 82094.260000] [Interval: 1.001784] [NrSamples: 955] [yes(7202): 28%(Usr/27%+Sys/0%)] [SampleTime: 0.000100]
    ==========================================================================================================================================================
     Usage  |                                                                 Function [Path]                                                                 
    ==========================================================================================================================================================
      35.6% | _IO_file_xsputn@GLIBC_2.17 [/lib/libc-2.24.so]                                                                                                  
               100.0% |  <- fputs_unlocked@GLIBC_2.17[/lib/libc-2.24.so] <- ??[/usr/bin/yes.coreutils] <- __libc_start_main@GLIBC_2.17[/lib/libc-2.24.so]
      17.8% | fputs_unlocked@GLIBC_2.17 [/lib/libc-2.24.so]                                                                                                   
               100.0% |  <- ??[/usr/bin/yes.coreutils] <- __libc_start_main@GLIBC_2.17[/lib/libc-2.24.so]
      16.1% | __libc_start_main@GLIBC_2.17 [/lib/libc-2.24.so]                                                                                                
      14.7% | memcpy@GLIBC_2.17 [/lib/libc-2.24.so]                                                                                                           
               100.0% |  <- _IO_file_xsputn@GLIBC_2.17[/lib/libc-2.24.so] <- fputs_unlocked@GLIBC_2.17[/lib/libc-2.24.so] <- ??[/usr/bin/yes.coreutils]
                         <- __libc_start_main@GLIBC_2.17[/lib/libc-2.24.so]
      12.3% | strlen@GLIBC_2.17 [/lib/libc-2.24.so]                                                                                                           
               100.0% |  <- fputs_unlocked@GLIBC_2.17[/lib/libc-2.24.so] <- ??[/usr/bin/yes.coreutils] <- __libc_start_main@GLIBC_2.17[/lib/libc-2.24.so]
       3.0% | _IO_file_write@GLIBC_2.17 [/lib/libc-2.24.so]                                                                                                   
               100.0% |  <- ??[/lib/libc-2.24.so] <- _IO_do_write@GLIBC_2.17[/lib/libc-2.24.so] <- _IO_file_xsputn@GLIBC_2.17[/lib/libc-2.24.so]
                         <- fputs_unlocked@GLIBC_2.17[/lib/libc-2.24.so] <- ??[/usr/bin/yes.coreutils]
                         <- __libc_start_main@GLIBC_2.17[/lib/libc-2.24.so]
    ----------------------------------------------------------------------------------------------------------------------------------------------------------

>>>

    # guider/guider.py systop -g yes -H

    [Top Syscall Info] [Time: 82043.230000] [Interval: 1.000940] [NrSamples: 634] [yes(7202): 5%(Usr/4%+Sys/0%)] 
    ==========================================================================================================================================================
     Usage  |                                                                 Function [Count]                                                                
    ==========================================================================================================================================================
     100.0% | write [Cnt: 634, Tot: 0.830203, Avg: 0.001309, Max: 0.005875, Err: 0]                                                                           
               100.0% |  <- ??[/lib/libc-2.24.so] <- _IO_file_write@GLIBC_2.17[/lib/libc-2.24.so] <- ??[/lib/libc-2.24.so]
                         <- _IO_do_write@GLIBC_2.17[/lib/libc-2.24.so] <- _IO_file_xsputn@GLIBC_2.17[/lib/libc-2.24.so]
                         <- fputs_unlocked@GLIBC_2.17[/lib/libc-2.24.so] <- ??[/usr/bin/yes.coreutils]
                         <- __libc_start_main@GLIBC_2.17[/lib/libc-2.24.so]
    ----------------------------------------------------------------------------------------------------------------------------------------------------------

>>>

    # guider/guider.py btop -g a.out -H

    [Top Breakcall Info] [Time: 1146111.080] [Interval: 1.001] [NrSamples: 2,386] [a.out(214460): 4%(Usr/1%+Sys/2%)] [guider(214459): 92%]
    ==========================================================================================================================================================
     Usage  |                                                            Function [PATH] <Interval>
    ==========================================================================================================================================================
      15.8% | __mempcpy_sse2_unaligned_erms [/lib/x86_64-linux-gnu/libc-2.31.so] <Cnt: 378, Avg: 0.002639, Min: 0.001029, Max: 0.006689]
               100.0% |  <- _IO_new_file_xsputn[/lib/x86_64-linux-gnu/libc-2.31.so]
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
      15.8% | _IO_new_file_xsputn [/lib/x86_64-linux-gnu/libc-2.31.so] <Cnt: 378, Avg: 0.002639, Min: 0.001026, Max: 0.006699]
               100.0% |  <- __vfprintf_internal[/lib/x86_64-linux-gnu/libc-2.31.so] <- printf[/lib/x86_64-linux-gnu/libc-2.31.so]
                         <- printPeace2[/home/peacelee/test/a.out] <- printPeace[/home/peacelee/test/a.out]
                         <- main[/home/peacelee/test/a.out] <- __libc_start_main[/lib/x86_64-linux-gnu/libc-2.31.so]
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
      10.6% | __strchrnul_sse2 [/lib/x86_64-linux-gnu/libc-2.31.so] <Cnt: 252, Avg: 0.003959, Min: 0.002209, Max: 0.006634]
               100.0% |  <- __vfprintf_internal[/lib/x86_64-linux-gnu/libc-2.31.so] <- printf[/lib/x86_64-linux-gnu/libc-2.31.so]
                         <- printPeace2[/home/peacelee/test/a.out] <- printPeace[/home/peacelee/test/a.out]
                         <- main[/home/peacelee/test/a.out] <- __libc_start_main[/lib/x86_64-linux-gnu/libc-2.31.so]
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
       5.3% | _itoa_word [/lib/x86_64-linux-gnu/libc-2.31.so] <Cnt: 126, Avg: 0.007900, Min: 0.007699, Max: 0.009268]
               100.0% |  <- __vfprintf_internal[/lib/x86_64-linux-gnu/libc-2.31.so] <- printf[/lib/x86_64-linux-gnu/libc-2.31.so]
                         <- printPeace2[/home/peacelee/test/a.out] <- printPeace[/home/peacelee/test/a.out]
                         <- main[/home/peacelee/test/a.out] <- __libc_start_main[/lib/x86_64-linux-gnu/libc-2.31.so]
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
       5.3% | usleep@GLIBC_2.2.5 [/lib/x86_64-linux-gnu/libc-2.31.so] <Cnt: 126, Avg: 0.007899, Min: 0.007766, Max: 0.009188]
               100.0% |
                         <- asdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfafda
                         <- printPeace2[/home/peacelee/test/a.out] <- printPeace[/home/peacelee/test/a.out]
                         <- main[/home/peacelee/test/a.out] <- __libc_start_main[/lib/x86_64-linux-gnu/libc-2.31.so]
    ----------------------------------------------------------------------------------------------------------------------------------------------------------

>>>
           
    # guider/guider.py ftop -g init

    [Top File Info] [Time: 7176036.720] [Proc: 322] [FD: 1323] [File: 400] (Unit: %/MB/NR)
    ==========================================================================================================================================================
          PROC       ( ID  / Pid / Nr / Pri)| FD |                                                   PATH                                                    |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
                init (    1/    0/   1/C  0)|  12|  SOCKET: 4   DEVICE: 3   PIPE: 2   EVENT: 2   NORMAL: 1   PROC: 0                                         |
                                            |  11|  /var/log/upstart/mysql.log.1 (deleted)                                                                   |
                                            |  10|  socket:[13414] (@/com/ubuntu/upstart)                                                                    |
                                            |   9|  socket:[23593] (@/com/ubuntu/upstart)                                                                    |
                                            |   8|  socket:[6241]                                                                                            |
                                            |   7|  socket:[3098] (@/com/ubuntu/upstart)                                                                     |
                                            |   6|  anon_inode:inotify                                                                                       |
                                            |   5|  anon_inode:inotify                                                                                       |
                                            |   4|  pipe:[3097]                                                                                              |
                                            |   3|  pipe:[3097]                                                                                              |
                                            |   2|  /dev/null                                                                                                |
                                            |   1|  /dev/null                                                                                                |
                                            |   0|  /dev/null                                                                                                |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------

>>>
           
    # guider/guider.py stacktop -g syslog

    [Top Info] [Time: 7176163.830] [Interval: 1.0] [Ctxt: 2914] [Life: +13/-12] [IRQ: 5103] [Core: 24] [Task: 328/435] [RAM: 63876] [Swap: 65491] (Unit: %/MB/NR)
               [Cycle: 2G / Inst: 3G / IPC: 1.34 / CacheMiss: 6M(34%) / BranchMiss: 4M(0%) / Clock: 23G / MinFlt: 53,257 / MajFlt: 0]
    ==========================================================================================================================================================
      ID   | CPU (Usr/Ker/Blk/IRQ)| Mem (Diff/ User/Cache/Kern)| Swap (Diff/  I/O  )|NrPgRclm | BlkRW | NrFlt | NrBlk | NrSIRQ | NrMlk | NrDrt  |  Network   |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
    Total  |  6 %( 3 / 1 / 0 / 0 )| 4913(-204/  974/56824/1165)|  0   ( 0  /  0/0  )|   0/0   | 0/42  |   0   |   0   |  3713  |   0   | 90901  |   2K/13K   |
    ==========================================================================================================================================================
         Thread      (  TID/  PID/  Nr/ Pri)| CPU(Usr/Ker/Dly)|  Mem(RSS/Txt/Shr/Swp)| Blk( RD / WR /NrFlt)| Yld | Prmt | FD | LifeTime|     WaitChannel     |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
            rsyslogd ( 2702/ 2702/   4/C  0)|   0(  0/  0/  -)|  244(  5/  0/  2/  0)|   0(   -/   -/    0)|    0|     0|  64| 1K:22:40|poll_schedule_timeout|
                                       100% | poll_schedule_timeout+0x43/0x70 <- do_select+0x711/0x7f0 <- core_sys_select+0x196/0x280 <-
                                              SyS_select+0xa6/0xe0 <- entry_SYSCALL_64_fastpath+0x1a/0xa5
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
            rsyslogd ( 2779/ 2702/   4/C  0)|   0(  0/  0/  -)|  244(  5/  0/  2/  0)|   0(   -/   -/    0)|    0|     0|  64| 1K:22:40|poll_schedule_timeout|
                                       100% | poll_schedule_timeout+0x43/0x70 <- do_select+0x711/0x7f0 <- core_sys_select+0x196/0x280 <-
                                              SyS_select+0xa6/0xe0 <- entry_SYSCALL_64_fastpath+0x1a/0xa5
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
            rsyslogd ( 2780/ 2702/   4/C  0)|   0(  0/  0/  0)|  244(  5/  0/  2/  0)|   0(   -/   -/    0)|  116|     0|  64| 1K:22:40|      do_syslog      |
                                        99% | do_syslog+0x446/0x4c0 <- kmsg_read+0x3f/0x50 <- proc_reg_read+0x3d/0x60 <- __vfs_read+0x23/0x110 <-
                                              vfs_read+0x91/0x130 <- SyS_read+0x41/0xa0 <- entry_SYSCALL_64_fastpath+0x1a/0xa5
    ----------------------------------------------------------------------------------------------------------------------------------------------------------

>>>
           
    # guider/guider.py ptop -g yes

    [Top Info] [Time: 7181955.420] [Interval: 1.0] [Ctxt: 121] [Life: +0/-0] [IRQ: 1947] [Core: 24] [Task: 317/424] [RAM: 63876] [Swap: 65491] (Unit: %/MB/NR)
    ==========================================================================================================================================================
      ID   | CPU (Usr/Ker/Blk/IRQ)| Mem (Diff/ User/Cache/Kern)| Swap (Diff/  I/O  )|NrPgRclm | BlkRW | NrFlt | NrBlk | NrSIRQ | NrMlk | NrDrt  |  Network   |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
    Total  |  5 %( 4 / 0 / 0 / 0 )| 3783(   0/  875/58078/1140)|  0   ( 0  /  0/0  )|   0/0   |  0/0  |   0   |   0   |  2023  |   0   |   0    |   1K/3K    |
    ==========================================================================================================================================================
        Process      (  PID/ PPID/  Nr/ Pri)| CPU(Usr/Ker/Dly)|  Mem(RSS/Txt/Shr/Swp)| Blk( RD / WR /NrFlt)| Yld | Prmt | FD | LifeTime|     WaitChannel     |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
                 yes (22371/ 9085/   1/R 90)|  99( 99/  0/  0)|    8(  0/  0/  0/  0)|   0(   -/   -/    0)|    0|     0| 256|  1:34:11|       RUNNING       |
                                            | [Cycle: 2G / Inst: 6G / IPC: 2.82 / CacheMiss: 11K(98%) / BranchMiss: 26K(0%) / Clock: 972M / MinFlt: 0 / MajFlt: 0]
    ----------------------------------------------------------------------------------------------------------------------------------------------------------

>>>
           
    # guider/guider.py mtop

    [Top Info] [Time: 1144292.910] [Inter: 1.0] [Ctxt: 739] [Life: +0/-0] [IRQ: 10740] [Core: 40] [Task: 509/725] [Load: 38/38/38] [RAM: 125.7G] [Swap: 4.0G]
               [N0-DMA     > diff:       0 / free:  15.5M / high:  32.0K / low:  20.0K / managed:  15.5M / min:   8.0K / present:  15.6M / spanned:  16.0M ]
               [N0-DMA32   > diff:       0 / free:   1.9G / high:   4.6M / low:   2.8M / managed:   1.9G / min: 956.0K / present:   1.9G / spanned:   4.0G ]
               [N0-Device  > diff:       0 / free:      0 / high:      0 / low:      0 / managed:      0 / min:      0 / present:      0 / spanned:      0 ]
               [N0-Movable > diff:       0 / free:      0 / high:      0 / low:      0 / managed:      0 / min:      0 / present:      0 / spanned:      0 ]
               [N0-Normal  > diff:   -3.9M / free: 113.4G / high: 318.7M / low: 191.9M / managed: 123.9G / min:  65.1M / present: 126.0G / spanned: 126.0G ]
    ==========================================================================================================================================================
      ID   |  CPU(Usr/Ker/Blk/IRQ)|  Avl( Per/ User/Cache/Kern)|  Swap( Per/ In/Out)| PgRclm  | BlkRW | NrFlt | PrBlk | NrSIRQ | PgMlk | PgDrt  |  Network   |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
    Total  | 98 %(97 / 0 / 0 / 0 )|12417(  96/ 1117/ 7915/1739)|     0(   0/  0/  0)|   0/0   |  0/0  |   0   |   0   | 12975  | 4613  |   67   |   2K/52    |
    ==========================================================================================================================================================
        Process      (  PID/ PPID/  Nr/ Pri)| CPU(Usr/Ker/Dly)|  Mem(RSS/Txt/Shr/Swp)| Blk( RD / WR /NrFlt)| Yld | Prmt | FD | LifeTime|     WaitChannel     |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
     FahCore_a8 ( 214159/ 214155/  41/C 19)|3792(3791/  0/  -)|3219( 548/ 14/ 13/  0)|   0(   -/   -/    0)| 1197|fahcli|  64| 00:20:54|FAHCoreWrapper(214155|
                               MEM(STACK/1) | VSS: 132.0K / RSS:  48.0K / PSS:  48.0K / SWAP:      0 / HUGE:    0 / LOCK:     0 / SDRT:      0 / PDRT:  48.0K|
                                MEM(FILE/6) | VSS:  20.4M / RSS:  13.2M / PSS:  10.7M / SWAP:      0 / HUGE:    0 / LOCK:     0 / SDRT:      0 / PDRT:  92.0K|
                                 MEM(ETC/3) | VSS:  20.0K / RSS:   4.0K / PSS:      0 / SWAP:      0 / HUGE:    0 / LOCK:     0 / SDRT:      0 / PDRT:      0|
                              MEM(ANON/165) | VSS:   3.1G / RSS: 539.7M / PSS: 539.7M / SWAP:      0 / HUGE:    0 / LOCK:     0 / SDRT:      0 / PDRT: 539.7M|
                                   MEM(SUM) | VmPeak: 4.0G, VmHWM: 548.6M, VmData: 948.2M, HugetlbPages: 0, RssAnon: 535.5M, RssFile: 13.2M, RssShmem: 0     |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------

>>>
           
    # guider/guider.py ntop

    [Top Info] [Time: 186473.960] [Interval: 1.0] [Ctxt: 7865] [Life: +0/-0] [OOM: 0] [IRQ: 4229] [Core: 8] [Task: 328/1171] [Load: 0.5/0.3/0.3] [RAM: 62.8G]
    ==========================================================================================================================================================
      ID   |  CPU(Usr/Ker/Blk/IRQ)|  Avl(Diff/ User/Cache/Kern)|  Swap(Diff/ In/Out)| PgRclm  | BlkRW | NrFlt | PrBlk | NrSIRQ | PgMlk | PgDrt  |  Network   |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
    Total  |  1 %( 0 / 0 / 0 / 0 )|59939(  -2/ 3054/ 6429/ 350)|     0(   0/  0/  0)|   0/0   |  0/0  |   0   |   0   |  1661  | 1607  |  343   |  652K/9K   |
    ==========================================================================================================================================================
                    Network                  |                        Receive                        |                       Transfer                        |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
          Dev        |          IP           |   Size   |  Packet  |  Error   |   Drop   | Multicast |   Size   |  Packet  |  Error   |   Drop   | Multicast |
    ==========================================================================================================================================================
             docker0 |        166.104.101.26 |        0 |        0 |        0 |        0 |         0 |        0 |        0 |        0 |        0 |         0 |
                eno1 |         166.104.101.1 |   665.9K |      475 |        0 |        0 |         1 |    12.0K |      168 |        0 |        0 |         0 |
     enx201601190a25 |        166.104.101.27 |       48 |        1 |        0 |        0 |         0 |        0 |        0 |        0 |        0 |         0 |
                  lo |             127.0.0.1 |        0 |        0 |        0 |        0 |         0 |        0 |        0 |        0 |        0 |         0 |
              virbr0 |                       |        0 |        0 |        0 |        0 |         0 |        0 |        0 |        0 |        0 |         0 |
          virbr0-nic |                       |        0 |        0 |        0 |        0 |         0 |        0 |        0 |        0 |        0 |         0 |
           [ TOTAL ] |                       |   666.0K |      476 |        0 |        0 |         1 |    12.0K |      168 |        0 |        0 |         0 |
    ==========================================================================================================================================================

>>>

    # guider/guider.py disktop
    
    [Top Info] [Time: 262411.830] [Inter: 1.0] [Ctxt: 802] [Life: +0/-0] [IRQ: 10675] [Core: 40] [Task: 481/700] [Load: 38/38/38] [RAM: 125.7G] [Swap: 4.0G]
    ==========================================================================================================================================================
      ID   |  CPU(Usr/Ker/Blk/IRQ)|  Avl( Per/ User/Cache/Kern)|  Swap( Per/ In/Out)| PgRclm  | BlkRW | NrFlt | PrBlk | NrSIRQ | PgMlk | PgDrt  |  Network   |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
    Total  | 98 %(97 / 0 / 0 / 0 )|124431(  96/  994/ 3531/1733)|     0(   0/  0/  0)|   0/0   |  0/0  |   0   |   0   | 11620  | 4613  |   70   |    1K/0    |
    ==========================================================================================================================================================
              DEV           |BUSY| AVQ | READ  | WRITE |   FREE(   DIFF)|USAGE| TOTAL |  AVF  |   FS   |                 MountPoint <Option>                 |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
    /dev/sda2               |  0%|    0|      0|      0| 670.6G(      0)|  28%| 937.4G|  57.6M|  ext4  | / <rw,relatime>                                     |
    /dev/loop4              |  0%|    0|      0|      0|      0(      0)| 100%|  30.0M|      0|squashfs| /snap/snapd/9279 <ro,nodev,relatime>                |
    /dev/loop5              |  0%|    0|      0|      0|      0(      0)| 100%|  70.0M|      0|squashfs| /snap/lxd/16922 <ro,nodev,relatime>                 |
    /dev/sda1               |  0%|    0|      0|      0| 503.0M(      0)|   1%| 510.0M|      0|  vfat  | /boot/efi <rw,relatime>                             |
    /dev/loop1              |  0%|    0|      0|      0|      0(      0)| 100%|  55.0M|      0|squashfs| /snap/core18/1885 <ro,nodev,relatime>               |
    /dev/loop2              |  0%|    0|      0|      0|      0(      0)| 100%|  70.0M|      0|squashfs| /snap/lxd/16894 <ro,nodev,relatime>                 |
    /dev/loop0              |  0%|    0|      0|      0|      0(      0)| 100%|  55.0M|      0|squashfs| /snap/core18/1880 <ro,nodev,relatime>               |
    /dev/loop3              |  0%|    0|      0|      0|      0(      0)| 100%|  30.0M|      0|squashfs| /snap/snapd/8790 <ro,nodev,relatime>                |
    /run/snapd/ns           |  0%|    0|      0|      0|  12.6G(      0)|   0%|  12.6G|  15.7M| tmpfs  | /run/snapd/ns                                       |
    /run/user/1004          |  0%|    0|      0|      0|  12.6G(      0)|   0%|  12.6G|  15.7M| tmpfs  | /run/user/1004 <rw,nosuid,nodev,relatime>           |
    /sys/fs/cgroup          |  0%|    0|      0|      0|  62.9G(      0)|   0%|  62.9G|  15.7M| tmpfs  | /sys/fs/cgroup <ro,nosuid,nodev,noexec>             |
    /run                    |  0%|    0|      0|      0|  12.6G(      0)|   0%|  12.6G|  15.7M| tmpfs  | /run <rw,nosuid,nodev,noexec,relatime>              |
    /run/lock               |  0%|    0|      0|      0|   5.0M(      0)|   0%|   5.0M|  15.7M| tmpfs  | /run/lock <rw,nosuid,nodev,noexec,relatime>         |
    /dev/shm                |  0%|    0|      0|      0|  62.9G(      0)|   0%|  62.9G|  15.7M| tmpfs  | /dev/shm <rw,nosuid,nodev>                          |
    ==========================================================================================================================================================

>>>

    # guider/guider.py wtop -g yes

    [Top Info] [Time: 7176629.490] [Interval: 1.0] [Ctxt: 195] [Life: +0/-0] [IRQ: 2688] [Core: 24] [Task: 327/434] [RAM: 63876] [Swap: 65491] (Unit: %/MB/NR)
               [Cycle: 2G / Inst: 6G / IPC: 2.75 / CacheMiss: 202K(19%) / BranchMiss: 325K(0%) / Clock: 23G / MinFlt: 4 / MajFlt: 0]
    ==========================================================================================================================================================
      ID   | CPU (Usr/Ker/Blk/IRQ)| Mem (Diff/ User/Cache/Kern)| Swap (Diff/  I/O  )|NrPgRclm | BlkRW | NrFlt | NrBlk | NrSIRQ | NrMlk | NrDrt  |  Network   |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
    Total  |  5 %( 4 / 0 / 0 / 0 )| 4719(   0/  856/57152/1149)|  0   ( 0  /  0/0  )|   0/0   |  0/0  |   0   |   0   |  2410  |   0   |   2    |   1K/5K    |
    ==========================================================================================================================================================
        Process      (  PID/ PPID/  Nr/ Pri)| CPU(Usr/Ker/Dly)|  Mem(RSS/Txt/Shr/Swp)| Blk( RD / WR /NrFlt)| Yld | Prmt | FD | LifeTime|     WaitChannel     |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
                 yes (22371/ 9085/   1/R 90)|  99( 99/  0/  0)|    8(  0/  0/  0/  0)|   0(   -/   -/    0)|    0|     0| 256|  0: 5:25|       RUNNING       |
                                 (1)[STACK] | SIZE:   0M / RSS:   0M / PSS:   0M / SWAP:   0M / HUGE:  0M / LOCK:   0K / SDRT:   0K / PDRT:   8K / NOPM:   0K|
                                            |  WSS: [   8K] ->    4K ->    4K ->    4K ->    4K ->    4K ->    4K ->    4K ->    4K ->    4K ->    4K ->    4K
                                  (4)[FILE] | SIZE:   7M / RSS:   1M / PSS:   0M / SWAP:   0M / HUGE:  0M / LOCK:   0K / SDRT:   0K / PDRT:  40K / NOPM:2048K|
                                            |  WSS: [   1M] ->    1M ->    1M ->    1M ->    1M ->    1M ->    1M ->    1M ->    1M ->    1M ->    1M ->    1M
                                   (3)[ETC] | SIZE:   0M / RSS:   0M / PSS:   0M / SWAP:   0M / HUGE:  0M / LOCK:   0K / SDRT:   0K / PDRT:   0K / NOPM:   0K|
                                            |  WSS: [   4K] ->    4K ->    4K ->    4K ->    4K ->     0 ->     0 ->     0 ->     0 ->     0 ->    4K ->    4K
                                  (5)[ANON] | SIZE:   0M / RSS:   0M / PSS:   0M / SWAP:   0M / HUGE:  0M / LOCK:   0K / SDRT:   0K / PDRT:  48K / NOPM:   0K|
                                            |  WSS: [  48K] ->    4K ->    4K ->    4K ->    4K ->    4K ->    4K ->    4K ->    4K ->    4K ->    4K ->    4K
    ----------------------------------------------------------------------------------------------------------------------------------------------------------

>>>
           
    # guider/guider.py btrace -g a.out -H

    0.505835   _int_malloc/0x7f94ed6cb2d0(0x7f94eda22c40L,0xaL,0x0L,0x0L,0xffffffffL,0x0L) [/lib/x86_64-linux-gnu/libc-2.27.so]
             __libc_start_main/0x7f94ed658b97 [/lib/x86_64-linux-gnu/libc-2.27.so]
               main/0x55f94081eb46 [/home/peacelee/test/a.out]
                 printPeace/0x55f94081eb23 [/home/peacelee/test/a.out]
                   printPeace2/0x55f94081ea6c [/home/peacelee/test/a.out]
                     asdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfafdasfdasdfasf
    0.506208           usleep@GLIBC_2.2.5/0x7f94ed74e820(0x64L,0x0L,0x55f941e71170L,0x55f941cb4010L,0xffffffffL,0x0L) [/lib/x86_64-linux-gnu/libc-2.27.so]
    0.506687           nanosleep@GLIBC_2.2.5/0x7f94ed71b990(0x7fff655f8910L,0x0L,0x0L,0x55f941cb4010L,0xffffffffL,0x0L) [/lib/x86_64-linux-gnu/libc-2.27.so]
    0.507276           open64@GLIBC_2.2.5/0x7f94ed746c40(0x55f94081ebd4L,0x0L,0x0L,0x55f941cb4010L,0xffffffffL,0x0L) [/lib/x86_64-linux-gnu/libc-2.27.so]
    0.507732           read@GLIBC_2.26/0x7f94ed747070(0xffffffffL,0x0L,0x0L,0x0L,0xffffffffL,0x0L) [/lib/x86_64-linux-gnu/libc-2.27.so]
    0.508231           close@GLIBC_2.4/0x7f94ed7478c0(0xffffffffL,0x0L,0xffffffffffffff80L,0x0L,0xffffffffL,0x0L) [/lib/x86_64-linux-gnu/libc-2.27.so]
    0.508699           malloc@GLIBC_2.2.5/0x7f94ed6ce070(0xaL,0x0L,0xffffffffffffff80L,0x0L,0xffffffffL,0x0L) [/lib/x86_64-linux-gnu/libc-2.27.so]
             malloc@GLIBC_2.2.5/0x7f94ed6ce0fc [/lib/x86_64-linux-gnu/libc-2.27.so]
    0.509156   _int_malloc/0x7f94ed6cb2d0(0x7f94eda22c40L,0xaL,0x0L,0x0L,0xffffffffL,0x0L) [/lib/x86_64-linux-gnu/libc-2.27.so]
             __libc_start_main/0x7f94ed658b97 [/lib/x86_64-linux-gnu/libc-2.27.so]
               main/0x55f94081eb46 [/home/peacelee/test/a.out]
                 printPeace/0x55f94081eb23 [/home/peacelee/test/a.out]
                   printPeace2/0x55f94081ea6c [/home/peacelee/test/a.out]
                     asdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfafdasfdasdfasf
    0.509532           usleep@GLIBC_2.2.5/0x7f94ed74e820(0x64L,0x0L,0x55f941e71190L,0x55f941cb4010L,0xffffffffL,0x0L) [/lib/x86_64-linux-gnu/libc-2.27.so]
    0.510032           nanosleep@GLIBC_2.2.5/0x7f94ed71b990(0x7fff655f8910L,0x0L,0x0L,0x55f941cb4010L,0xffffffffL,0x0L) [/lib/x86_64-linux-gnu/libc-2.27.so]
    0.510648           open64@GLIBC_2.2.5/0x7f94ed746c40(0x55f94081ebd4L,0x0L,0x0L,0x55f941cb4010L,0xffffffffL,0x0L) [/lib/x86_64-linux-gnu/libc-2.27.so]
    0.511155           read@GLIBC_2.26/0x7f94ed747070(0xffffffffL,0x0L,0x0L,0x0L,0xffffffffL,0x0L) [/lib/x86_64-linux-gnu/libc-2.27.so]
    0.511659           close@GLIBC_2.4/0x7f94ed7478c0(0xffffffffL,0x0L,0xffffffffffffff80L,0x0L,0xffffffffL,0x0L) [/lib/x86_64-linux-gnu/libc-2.27.so]
    0.512201           malloc@GLIBC_2.2.5/0x7f94ed6ce070(0xaL,0x0L,0xffffffffffffff80L,0x0L,0xffffffffL,0x0L) [/lib/x86_64-linux-gnu/libc-2.27.so]
             malloc@GLIBC_2.2.5/0x7f94ed6ce0fc [/lib/x86_64-linux-gnu/libc-2.27.so]

>>>
           
    $ guider/guider.py rtop &
    $ cat /tmp/guider.report

    {
      "task": {
        "nrThread": 397,
        "nrBlocked": 0,
        "nrCtx": 4290,
        "nrProc": 292
      },
      "mem": {
        "kernel": 1432,
        "anonDiff": -1,
        "pgRclmFg": 0,
        "cache": 35332,
        "slabDiff": 0,
        "free": 26929,
        "anon": 698,
        "pgDirty": 28,
        "file": 31751,
        "freeDiff": -1,
        "pgRclmBg": 0,
        "total": 64391,
        "slab": 3581,
        "fileDiff": -1
        "procs": {
          "1954": {
            "text": 0,
            "pid": 1954,
            "rank": 2,
            "comm": "ruby1.9.1",
            "runtime": "110:43:32",
            "rss": 104
          },
      },
      "storage": {
        "total": {
          "read": 0,
          "mount": {},
          "favail": 133443655,
          "free": 1141633,
          "write": 1,
          "usage": 1152423,
          "total": 2294056,
          "usageper": 50
        },
        "/dev/sdb1": {
          "read": 0,
          "mount": {
            "path": "/mnt/hdd1",
            "fs": "ext4",
            "option": "rw,relatime,data=ordered"
          },
          "favail": 50709466,
          "free": 293649,
          "write": 0,
          "usage": 645251,
          "total": 938900,
          "usageper": 68
        },
      },
      "system": {
        "load5m": 2.38,
        "uptime": 4191643.92,
        "nrSoftIrq": 7405,
        "nrIrq": 7289,
        "load15m": 0.84,
        "interval": 1.029999999795109,
        "pid": 14578,
        "load1m": 9.39
      },
      "event": {
        "CPU_INTENSIVE": {
          "14592": {
            "kernel": 0,
            "runtime": "0:0:47",
            "pid": 14592,
            "rank": 3,
            "comm": "yes",
            "user": 99,
            "total": 100
          },
          "14593": {
            "kernel": 0,
            "runtime": "0:0:46",
            "pid": 14593,
            "rank": 10,
            "comm": "yes",
            "user": 99,
            "total": 100
          },
      },
      "swap": {
        "usage": 76,
        "total": 65491,
        "usageDiff": 0
      },
      "net": {
        "inbound": 1479,
        "outbound": 392
      },
      "cpu": {
        "kernel": 0,
        "iowait": 0,
        "nrCore": 24,
        "idle": 8,
        "user": 91,
        "irq": 0,
        "total": 92,
        "procs": {
          "14592": {
            "kernel": 0,
            "runtime": "0:0:47",
            "pid": 14592,
            "rank": 3,
            "comm": "yes",
            "user": 99,
            "total": 100
          },
      },
      "block": {
        "read": 0,
        "write": 0,
        "procs": {},
        "nrMajFlt": 0,
        "ioWait": 0
      }
    }

>>>

    # guider/guider.py cpulimit -g 22371:50

    [Info] limited cpu usage of yes(22371) process to 50%, it used 50%

    [Info] limited cpu usage of yes(22371) process to 50%, it used 50%

>>>
           
    # guider/guider.py setsched r:90:22371

    [Info] changed the priority of guider(22371) to 90[R]

>>>
           
    # guider/guider.py remote -g a.out -c usercall:write#1#HOOK#4

    [usercall] write(7f94ed747140)(1, HOOK, 4) = 0x4(4)

>>>

    # guider/guider.py printenv -g systemd

    [ systemd(1) ]
    -----------------------------------------------------------------------------
    HOME=/
    init=/sbin/init
    NETWORK_SKIP_ENSLAVED=
    recovery=
    TERM=linux
    drop_caps=
    BOOT_IMAGE=/boot/vmlinuz-5.3.0-28-generic
    PATH=/sbin:/usr/sbin:/bin:/usr/bin
    PWD=/
    rootmnt=/root

    [ systemd(3310) ]
    -----------------------------------------------------------------------------
    LANG=en_US.UTF-8
    PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
    NOTIFY_SOCKET=/run/systemd/notify
    HOME=/home/syjung
    LOGNAME=syjung
    USER=syjung
    SHELL=/bin/bash
    INVOCATION_ID=bbc56cc8552e4a1d815197e0a6160270
    JOURNAL_STREAM=9:10617556
    XDG_RUNTIME_DIR=/run/user/1002

    [ systemd(7094) ]
    -----------------------------------------------------------------------------
    LANG=en_US.UTF-8
    PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
    NOTIFY_SOCKET=/run/systemd/notify
    HOME=/home/peacelee
    LOGNAME=peacelee
    USER=peacelee
    SHELL=/bin/bash
    INVOCATION_ID=be65ebdd72964e09a3ac06495261702b
    JOURNAL_STREAM=9:31410
    XDG_RUNTIME_DIR=/run/user/1004

>>>
           
    # guider/guider.py kill -stop yes

    [Info] sent signal SIGSTOP to yes(10594)

>>>
           
    # guider/guider.py rec -a -e m,b

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
       
    # guider/guider.py sysrec 

    [Thread Syscall Info] (Unit: Sec/NR)
    ==========================================================================================================================================================
                Name(  Tid)                        Syscall( ID)      Elapsed        Count        Error          Min          Max          Avg
    ==========================================================================================================================================================
     arm-linux-gnuea( 3000)
                                                     close(  3)     0.039396           69            0     0.000001     0.005353     0.000571
                                                      stat(  4)     0.011521           74            0     0.000001     0.009423     0.000156
                                                    fchmod( 91)     0.000046            3            0     0.000002     0.000039     0.000015
                                               getpriority(140)     0.000017           33            0     0.000000     0.000001     0.000001
                                                 lgetxattr(192)     0.000014            3            0     0.000003     0.000008     0.000005
                                                  recvfrom( 45)     0.000004            1            0     0.000004     0.000004     0.000004

    ----------------------------------------------------------------------------------------------------------------------------------------------------------
              guider( 3001)
                                                     pause( 34)     0.283474            1            1     0.283474     0.283474     0.283474
                                                    select( 23)     0.100122            1            0     0.100122     0.100122     0.100122
                                                     write(  1)     0.000234            6            0     0.000031     0.000059     0.000039
                                                      open(  2)     0.000084            7            0     0.000007     0.000038     0.000012
                                                     ioctl( 16)     0.000009           14           14     0.000001     0.000001     0.000001
                                                     fstat(  5)     0.000006           14            0     0.000001     0.000001     0.000000
                                                     lseek(  8)     0.000006           21            0     0.000000     0.000001     0.000000
                                                     close(  3)     0.000005            7            0     0.000000     0.000001     0.000001
                                              rt_sigaction( 13)     0.000001            1            0     0.000001     0.000001     0.000001

    ----------------------------------------------------------------------------------------------------------------------------------------------------------
              mysqld( 3237)
                                                     futex(202)     0.000000            1            0     0.000000     0.000000     0.000000

    ----------------------------------------------------------------------------------------------------------------------------------------------------------
              mysqld( 3238)
                                                     futex(202)     0.000002            1            0     0.000002     0.000002     0.000002

    ----------------------------------------------------------------------------------------------------------------------------------------------------------
              screen( 9045)
                                                    select( 23)     0.000082            4            0     0.000004     0.000069     0.000021
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
       
>>>
       
    # guider/guider.py rec -e b

    [Thread Block Info] (Unit: KB/NR)
    ==========================================================================================================================================================
              ID              OPT    NrDev            TOTAL       SEQUENTIAL(    %)      FS              PATH
                                                   [ACCESS]                   COUNT
    ==========================================================================================================================================================
             TOTAL           READ     8:33          170,624          158,356( 92.8)     ext4          /dev/sdc1
                                            [   4K -    7K]                   2,024
                                            [   8K -   15K]                      21
                                            [  16K -   31K]                      43
                                            [  32K -   63K]                      44
                                            [  64K -  127K]                     155
                                            [ 128K -  255K]                     112
                                            [ 256K -  511K]                     510
                                            [ 512K - 1023K]                       2

                            WRITE     8:33                8                4( 50.0)     ext4          /dev/sdc1
                                            [   4K -    7K]                       2
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
                 cron(3115)  READ     8:33              644              576( 89.4)     ext4          /dev/sdc1
                                            [   4K -    7K]                     161
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
                 cat(10392)  READ     8:33              604              404( 66.9)     ext4          /dev/sdc1
                                            [   4K -    7K]                     110
                                            [  16K -   31K]                       1
                                            [  32K -   63K]                       1
                                            [  64K -  127K]                       1
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
                 bash(9085)  READ     8:33               28                4( 14.3)     ext4          /dev/sdc1
                                            [   4K -    7K]                       7
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
                 cat(10395)  READ     8:33          169,348          157,384( 92.9)     ext4          /dev/sdc1
                                            [   4K -    7K]                   1,746
                                            [   8K -   15K]                      21
                                            [  16K -   31K]                      42
                                            [  32K -   63K]                      43
                                            [  64K -  127K]                     154
                                            [ 128K -  255K]                     112
                                            [ 256K -  511K]                     510
                                            [ 512K - 1023K]                       2
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
       kworker/u50:0(10304) WRITE     8:33                8                4( 50.0)     ext4          /dev/sdc1
                                            [   4K -    7K]                       2
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
       
>>>
       
    # guider/guider.py rec -e L

    [Thread Futex Lock Info] [ Elapsed : 1.225 ] (Unit: Sec/NR)
    ==========================================================================================================================================================
                Name(  Tid/  Pid)    Elapsed    Process      Block  NrBlock    CallMax       Lock    LockMax   NrLock   NrWait     LBlock NrLBlock   LastStat
    ==========================================================================================================================================================
              mysqld( 3236/ 3208)      0.469      0.000      0.469        1      0.469      0.000      0.000        0        1      0.000        0       Wait
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
              mysqld( 3237/ 3208)      0.890      0.000      0.890        1      0.890      0.000      0.000        0        1      0.000        0       Wait
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
              mysqld( 3238/ 3208)      1.075      0.000      1.075        1      1.075      0.000      0.000        0        1      0.000        0       Wait
    ----------------------------------------------------------------------------------------------------------------------------------------------------------

    [Thread File Lock Info] (Unit: Sec/NR)
    ==========================================================================================================================================================
                Name(  Tid)         Wait            Lock     nrTryLock    nrLocked
    ==========================================================================================================================================================
                smbd( 2631)        0.000           0.000             3           3
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
       
>>>
       
    # guider/guider.py rec -s . -K openfile:getname::**string

    [Thread KERNEL Event Info]
    ==========================================================================================================================================================
                 Event                           Comm( Tid )      Usage      Count    ProcMax    ProcMin   InterMax   InterMin
    ==========================================================================================================================================================
                openfile                        TOTAL(  -  )   0.000729       1012   0.000013   0.000001   1.979834   0.000109
                                                   ps(10728)   0.000640        968   0.000013   0.000000   0.001636   0.000006
                                              python2(10727)   0.000038         26   0.000004   0.000001   1.979834   0.000020
                                                 tmux( 6959)   0.000031          9   0.000006   0.000003   0.299492   0.201316
                                       PassengerAgent(23183)   0.000008          5   0.000002   0.000001   0.007375   0.000109
                                         sendmail-mta( 3419)   0.000007          2   0.000006   0.000001   0.000077   0.000077
                                       PassengerAgent(10729)   0.000003          1   0.000003   0.000003   0.000000   0.000000
                                                 smbd(11086)   0.000002          1   0.000002   0.000002   0.000000   0.000000
    ----------------------------------------------------------------------------------------------------------------------------------------------------------

    [Thread KERNEL Event History]
    ==========================================================================================================================================================
                 EVENT                TYPE     TIME                COMM(  TID)         CALLER            ELAPSED ARG
    ==========================================================================================================================================================
                openfile               EXIT   0.063942             tmux( 6959)      porch_do_sys_open   0.000003  1>"/proc/7969/cmdline"
                openfile              ENTER   0.137626          python2(10727)                                 -
                openfile               EXIT   0.137628          python2(10727)      porch_do_sys_open   0.000002  1>"/sys/kernel/debug/tracing/trace"
                openfile              ENTER   0.363431             tmux( 6959)                                 -
                openfile               EXIT   0.363437             tmux( 6959)      porch_do_sys_open   0.000006  1>"/proc/7197/cmdline"
                openfile              ENTER   0.510452             smbd(11086)                                 -
                openfile               EXIT   0.510454             smbd(11086)      porch_do_sys_open   0.000002  1>"/var/log/samba/log.jhkim-z97x-ud3h"
                openfile              ENTER   0.564845             tmux( 6959)                                 -
                openfile               EXIT   0.564848             tmux( 6959)      porch_do_sys_open   0.000003  1>"/proc/7969/cmdline"
                openfile              ENTER   0.864255             tmux( 6959)                                 -
                openfile               EXIT   0.864258             tmux( 6959)      porch_do_sys_open   0.000003  1>"/proc/7197/cmdline"
                openfile              ENTER   1.065571             tmux( 6959)                                 -
                openfile               EXIT   1.065574             tmux( 6959)      porch_do_sys_open   0.000003  1>"/proc/7969/cmdline"
                openfile              ENTER   1.364980             tmux( 6959)                                 -
                openfile               EXIT   1.364984             tmux( 6959)      porch_do_sys_open   0.000004  1>"/proc/7197/cmdline"
                openfile              ENTER   1.437128     sendmail-mta( 3419)                                 -
                openfile               EXIT   1.437134     sendmail-mta( 3419)      porch_do_sys_open   0.000006  1>"/proc/loadavg"
                openfile              ENTER   1.437205     sendmail-mta( 3419)                                 -
                openfile               EXIT   1.437206     sendmail-mta( 3419)      porch_do_sys_open   0.000001  1>"/proc/loadavg"
                openfile              ENTER   1.566369             tmux( 6959)                                 -
                openfile               EXIT   1.566372             tmux( 6959)      porch_do_sys_open   0.000003  1>"/proc/7969/cmdline"
                openfile              ENTER   1.865776             tmux( 6959)                                 -
                openfile               EXIT   1.865779             tmux( 6959)      porch_do_sys_open   0.000003  1>"/proc/7197/cmdline"
                openfile              ENTER   1.955265   PassengerAgent(10729)                                 -
                openfile               EXIT   1.955268   PassengerAgent(10729)      porch_do_sys_open   0.000003  1>"/dev/fd"
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
       
>>>
       
    # guider/guider.py funcrec -s .
    # guider/guider.py guider.dat -o . -a

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
       
    # guider/guider.py funcrecord -e m -s .
    # guider/guider.py guider.dat -a

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
       
>>>
       
    # guider/guider.py filerec 

    [File Usage Info] [ File: 281 ] [ RAM: 78056(KB) ] [ Keys: Foward/Back/Save/Quit ]
    ==========================================================================================================================================================
    __RAM(KB)___|_File(KB)_|__%___|_____________________________________________________Library & Process_____________________________________________________
    ==========================================================================================================================================================
          7,616 |    7,616 |  100 | /run/samba/locking.tdb [Proc: 10] [Link: 1]
                                  |             smbd ( 2937) |             smbd ( 9178) |             smbd (21387) |             smbd ( 3356) |
                                  |             smbd ( 2828) |             smbd ( 2417) |             smbd ( 3862) |             smbd ( 2631) |
                                  |             smbd (11086) |             smbd (  729) |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
          6,076 |    8,452 |   71 | /usr/lib/apache2/modules/libphp5.so [Proc: 11] [Link: 1]
                                  |  /usr/sbin/apach (13071) |  /usr/sbin/apach (13073) |  /usr/sbin/apach ( 3817) |  /usr/sbin/apach ( 9111) |
                                  |  /usr/sbin/apach (20085) |  /usr/sbin/apach ( 7221) |  /usr/sbin/apach (  345) |  /usr/sbin/apach (  346) |
                                  |  /usr/sbin/apach ( 7222) |  /usr/sbin/apach (14278) |  /usr/sbin/apach ( 9715) |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
          5,784 |    9,828 |   58 | /usr/sbin/smbd [Proc: 10] [Link: 1]
                                  |             smbd ( 2937) |             smbd ( 9178) |             smbd (21387) |             smbd ( 3356) |
                                  |             smbd ( 2828) |             smbd ( 2417) |             smbd ( 3862) |             smbd ( 2631) |
                                  |             smbd (11086) |             smbd (  729) |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
          4,800 |   25,880 |   18 | /var/lib/gems/1.9.1/gems/passenger-5.1.0/buildout/support-binaries/PassengerAgent [Proc: 3] [Link: 1]
                                  |   PassengerAgent (23161) |   PassengerAgent (23176) |   PassengerAgent (23191) |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
          3,612 |   12,016 |   30 | /usr/sbin/mysqld [Proc: 1] [Link: 1]
                                  |           mysqld ( 3208) |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
          2,988 |    2,988 |  100 | /usr/lib/libpython2.7.so.1.0 [Proc: 6] [Link: 1]
                                  |               vi (18865) |               vi (28546) |               vi ( 7200) |               vi (22546) |
                                  |               vi ( 8826) |               vi ( 8135) |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
          2,228 |    2,884 |   77 | /usr/bin/python3.2mu [Proc: 1] [Link: 1]
                                  |           guider (22637) |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
          2,016 |    2,016 |  100 | /usr/lib/libruby-1.9.1.so.1.9.1 [Proc: 1] [Link: 1]
                                  |        ruby1.9.1 (23294) |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
       
>>>
       
    # guider/guider.py draw guider.out

![guider-graph](https://user-images.githubusercontent.com/15862689/67160607-9b1fc680-f38d-11e9-988e-5d90729d983e.png)
![guider-chart](https://user-images.githubusercontent.com/15862689/67160609-9bb85d00-f38d-11e9-9280-9ab649bb56b1.png)
![guider-web-dashboard](https://user-images.githubusercontent.com/15862689/67160178-0024ed80-f389-11e9-9a09-6a8eb96e2785.png)
![guider-web-commandtab](https://user-images.githubusercontent.com/15862689/67160180-03b87480-f389-11e9-8a91-033f74d103dc.png)

How to use
=======

```
Enter the following command to see all commands supported by the guider:
    $ guider/guider.py --help
    $ python -m guider --help
    $ guider --help

Enter the following command to start tracing for all threads:
    # guider/guider.py record -a

Enter the following command to start monitoring for all processes:
    $ guider/guider.py top -a

Enter the command in the format shown bellow to see options and examples for each command:
    $ guider/guider.py record -h
    $ guider/guider.py top -h

Visit the following link to see the output of guider:
    - https://github.com/iipeace/guider/wiki
```


Requirement
=======

```
- Linux Kernel (>= 2.6)
- Python (>= 2.7)
```


Build & Installation
=======

```
If you can run 'pip' on your system then just enter the following command:
    # pip install guider
and just run the following commands:
    # python -m guider
    # guider

Otherwise, download the source from https://github.com/iipeace/guider,
and just run "guider/guider.py" on shell.

If you want to run guider faster and lighter after downloading the source,
then build and install it on your system as below.
    # cd guider && make && make install
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


Help
=======

```
Usage:
    $ ./guider.py COMMAND|FILE [OPTIONS] [--help]
                
COMMAND:
    [CONTROL]       client          <Client>
                    event           <Event>
                    list            <List>
                    send            <Signal>
                    server          <Server>
                    start           <Signal>

    [LOG]           logdlt          <DLT>
                    logjrl          <Journal>
                    logkmsg         <Kernel>
                    logsys          <Syslog>
                    printdlt        <DLT>
                    printjrl        <Journal>
                    printkmsg       <Kernel>
                    printsys        <Syslog>

    [MONITOR]       bgtop           <Background>
                    btop            <Function>
                    dbustop         <D-Bus>
                    disktop         <Storage>
                    dlttop          <DLT>
                    ftop            <File>
                    mtop            <Memory>
                    ntop            <Network>
                    ptop            <PMU>
                    rtop            <JSON>
                    smtop           <System>
                    stacktop        <Stack>
                    systop          <Syscall>
                    top             <Process>
                    ttop            <Thread>
                    utop            <Function>
                    wtop            <WSS>

    [PROFILE]       filerec         <File>
                    funcrec         <Function>
                    genrec          <System>
                    mem             <Page>
                    rec             <Thread>
                    report          <Report>
                    sysrec          <Syscall>

    [TEST]          cputest         <CPU>
                    iotest          <Storage>
                    memtest         <Memory>
                    nettest         <Network>

    [TRACE]         btrace          <Breakpoint>
                    sigtrace        <Signal>
                    strace          <Syscall>
                    utrace          <Function>

    [UTIL]          addr2sym        <Symbol>
                    dump            <Memory>
                    getafnt         <Affinity>
                    hook            <Function>
                    kill/tkill      <Signal>
                    leaktrace       <Leak>
                    limitcpu        <CPU>
                    pause           <Thread>
                    printcrp        <Cgroup>
                    printdbus       <D-Bus>
                    printdir        <Dir>
                    printenv        <Env>
                    printinfo       <System>
                    printns         <Namespace>
                    printsig        <Signal>
                    printsubsc      <D-Bus>
                    printsvc        <systemd>
                    pstree          <Process>
                    readelf         <File>
                    remote          <Command>
                    setafnt         <Affinity>
                    setcpu          <Clock>
                    setsched        <Priority>
                    strings         <Text>
                    sym2addr        <Address>
                    systat          <Status>
                    topdiff         <Diff>
                    topsum          <Summary>
                    watch           <File>

    [VISUAL]        convert         <Text>
                    draw            <System>
                    drawavg         <Average>
                    drawcpu         <CPU>
                    drawcpuavg      <CPU>
                    drawio          <I/O>
                    drawleak        <Leak>
                    drawmem         <Memory>
                    drawmemavg      <Memory>
                    drawrss         <RSS>
                    drawrssavg      <RSS>
                    drawvss         <VSS>
                    drawvssavg      <VSS>

FILE:
    Profile file (e.g. guider.dat)
    Report  file (e.g. guider.out)

Options:
    Check COMMAND with --help (e.g. ./guider.py top --help)
```
