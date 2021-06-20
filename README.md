[![Build Status](https://travis-ci.org/iipeace/guider.svg?branch=master)](https://travis-ci.org/iipeace/guider) 
[![license](http://img.shields.io/badge/license-GNU-blue.svg)](https://raw.githubusercontent.com/iipeace/guider/master/LICENSE)
[![Coverity](https://scan.coverity.com/projects/15302/badge.svg)](https://scan.coverity.com/projects/iipeace-guider) 
[![PyPI version](https://badge.fury.io/py/guider.svg)](https://badge.fury.io/py/guider)
[![Download guider](https://img.shields.io/sourceforge/dt/guider.svg)](https://sourceforge.net/projects/guider/files/latest/download)
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
It provides most of the functions required for measuring, analyzing, testing and verifying system performance.
Even now, its functions and usability are expanding.

The features of Guider are as follows.
* Monitoring
* Profiling
* Visualization
* Control
* Logging
* Test
* Util

Guider pursues characteristics as below.
1. Easy to use: just run without any setting and package installation
2. Measure correctly: count, time in from us, size in from byte
3. Provide all features: enough functions for experiment and analysis
4. Submit the report in detail: show as much information as possible

It supports almost all platforms based on the Linux kernel as shown below.
* Android
* distro (Ubuntu, CentOS, RHEL, Linux Mint, Arch Linux, ...)
* ccOS (Connected Car Operating System)
* webOS
* Tizen
* GENIVI Development Platform (GDP)
* Automotive Grade Linux (AGL) Platform
* Windows (Limited)
* macOS (Limited)

Output
=======
    $ guider/guider.py top -a

    [Top Info] [Time: 4588832.570] [Inter: 1.0] [Ctxt: 314463] [Life: +0/-0] [IRQ: 26606] [Core: 40] [Task: 498/625] [Load: 0/0/0] [RAM: 125.7G] [Swap: 4.0G]
               [Cycle: 8.3G / Inst: 5.7G / IPC: 0.69 / CacheMiss : 13.7M(23%) / BrcMiss: 25.7M(1%) / Clk: 38.7G / MinFlt: 358 / MajFlt: 0]
    ==========================================================================================================================================================
      ID   |  CPU(Usr/Ker/Blk/IRQ)|MemAvl( Per/ User/Cache/Kern)| Swap( Per/ In/Out)| PgRclm  | BlkRW | NrFlt | PrBlk | NrSIRQ | PgMlk | PgDirt |  Network   |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
    Total  | 10 %( 1 / 6 / 0 / 0 )|124649(  96/  453/ 5690/1787)|    0(   0/  0/  0)|   0/0   |  0/0  |   0   |   0   | 15889  | 4616  |   20   |    2K/0    |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
    Core/0 |100 %(66 /34 / 0 / 0 )|###################################################################|   powersave   |  0-0   |  24 C | 2874 Mhz [1171-3515]|
    Core/1 |  7 %( 0 / 6 / 0 / 0 )|####                                                               |   powersave   |  0-1   |  22 C | 2307 Mhz [1171-3515]|
    Core/2 |  0 %( 0 / 0 / 0 / 0 )|                                                                   |   powersave   |  0-2   |  23 C | 2165 Mhz [1171-3515]|
    Core/3 |  0 %( 0 / 0 / 0 / 0 )|                                                                   |   powersave   |  0-3   |  22 C | 2170 Mhz [1171-3515]|
    Core/4 | 22 %( 0 /21 / 0 / 0 )|##############                                                     |   powersave   |  0-4   |  20 C | 2763 Mhz [1171-3515]|
    Core/5 |  0 %( 0 / 0 / 0 / 0 )|                                                                   |   powersave   |  0-8   |  24 C | 2160 Mhz [1171-3515]|
    Core/6 | 33 %( 0 / 0 / 0 /32 )|######################                                             |   powersave   |  0-9   |  19 C | 2194 Mhz [1171-3515]|
    Core/7 |  0 %( 0 / 0 / 0 / 0 )|                                                                   |   powersave   |  0-10  |  17 C | 2160 Mhz [1171-3515]|
    Core/8 |  0 %( 0 / 0 / 0 / 0 )|                                                                   |   powersave   |  0-11  |  23 C | 2158 Mhz [1171-3515]|
    Core/9 |  0 %( 0 / 0 / 0 / 0 )|                                                                   |   powersave   |  0-12  |  18 C | 2164 Mhz [1171-3515]|
    Core/10|  0 %( 0 / 0 / 0 / 0 )|                                                                   |   powersave   |  1-0   |  21 C | 2907 Mhz [1171-3515]|
    Core/11|  0 %( 0 / 0 / 0 / 0 )|                                                                   |   powersave   |  1-1   |  18 C | 2903 Mhz [1171-3515]|
    Core/12| 11 %( 9 / 1 / 0 / 0 )|#######                                                            |   powersave   |  1-2   |  22 C | 2927 Mhz [1171-3515]|
    Core/13|  0 %( 0 / 0 / 0 / 0 )|                                                                   |   powersave   |  1-3   |  17 C | 2904 Mhz [1171-3515]|
    Core/14|  0 %( 0 / 0 / 0 / 0 )|                                                                   |   powersave   |  1-4   |  21 C | 2903 Mhz [1171-3515]|
    Core/15|  7 %( 0 / 6 / 0 / 0 )|####                                                               |   powersave   |  1-8   |  19 C | 2912 Mhz [1171-3515]|
    Core/16|  0 %( 0 / 0 / 0 / 0 )|                                                                   |   powersave   |  1-9   |  24 C | 2925 Mhz [1171-3515]|
    Core/17| 87 %( 0 /86 / 0 / 0 )|##########################################################         |   powersave   |  1-10  |  24 C | 2907 Mhz [1171-3515]|
    Core/18|100 %( 0 /100/ 0 / 0 )|###################################################################|   powersave   |  1-11  |  20 C | 2914 Mhz [1171-3515]|
    Core/19|  0 %( 0 / 0 / 0 / 0 )|                                                                   |   powersave   |  1-12  |  21 C | 2894 Mhz [1171-3515]|
    ==========================================================================================================================================================
         Process (    PID/   PPID/  Nr/ Pri)| CPU(Usr/Ker/Dly)| VSS( RSS/Txt/Shr/Swp)| Blk(  RD/  WR/NrFlt)| SID | USER | FD | LifeTime|       Parent        |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
          screen (   2451/      1/   1/C  0)| 100( 66/ 34/  0)|  11(   6/  0/  2/  0)|   0(   -/   -/    0)| 2451|peacel|  64|53d:00:22|           systemd(1)|
             yes (1341199/1340350/   1/C  0)|  99(  0/ 99/  0)|   5(   0/  0/  0/  0)|   0(   -/   -/    0)| 2452|peacel|  64| 00:00:03|          vi(1340350)|
    kworker/u80: (1341030/      2/   1/C  0)|  90(  0/ 90/  0)|   0(   0/  0/  -/  -)|   0(   -/   -/    0)|    -|  root|  64| 00:15:46|          kthreadd(2)|
    kworker/u80: (1340705/      2/   1/C  0)|  26(  0/ 26/  0)|   0(   0/  0/  -/  -)|   0(   -/   -/    0)|    -|  root|  64| 02:04:59|          kthreadd(2)|
    kworker/u80: (1340966/      2/   1/C  0)|  21(  0/ 21/  0)|   0(   0/  0/  -/  -)|   0(   -/   -/    0)|    -|  root|  64| 00:20:56|          kthreadd(2)|
                                   [ TOTAL ]| 344.0(  72/ 271)|RSS:   1G / Swp:    0)| 0.0(   -/   -/    0)|      Yld: -|       Prmt: -|            Task: 498|
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
         [Z]bash ( 820918/ 820917/   1/C  0)|   0(  0/  0/  -)|   0(   0/  0/  0/  -)|   0(   -/   -/    0)|    -|     -|   -| 3d:06:10| tmux: server(820917)|
    ----------------------------------------------------------------------------------------------------------------------------------------------------------

>>>
           
    $ guider/guider.py top -R 5 -o
    $ cat guider.out

    [Top Summary Info]
    ==========================================================================================================================================================
     IDX  |          Interval           | CPU |   Avl/User/Cache   |  BlkRW  | Blk | SWAP | NrPgRclm  | NrFlt | NrCtx  | NrIRQ  |  NrTask  | Core | Network  |
    ==========================================================================================================================================================
        1 |        START -   497231.500 |  98 |  124442/962/3854   |   0/0   |   0 |    0 |    0/0    |     0 |    631 |  10660 |  482/701 |  40  |  2K/156  |
        2 |   497231.500 -   497232.520 |  98 |  124440/963/3854   |   0/0   |   0 |    0 |    0/0    |     0 |    646 |  10506 |  482/701 |  40  |  1K/104  |
        3 |   497232.520 -   497233.540 |  98 |  124440/964/3854   |   0/0   |   0 |    0 |    0/0    |     0 |    741 |  10562 |  482/701 |  40  |  2K/104  |
        4 |   497233.540 -   497234.570 |  98 |  124440/964/3854   |   0/0   |   0 |    0 |    0/0    |     0 |    629 |  10489 |  482/701 |  40  |  1K/104  |
        5 |   497234.570 -   497235.590 |  98 |  124440/964/3854   |   0/0   |   0 |    0 |    0/0    |     0 |    699 |  10602 |  482/701 |  40  |  2K/208  |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
    
    [Top CPU Info] (Unit: %)
    ==========================================================================================================================================================
        COMM     (  PID  / PPID  / Nr / Pri)| Min/Avg/Max  |      1      2      3      4      5 
    ==========================================================================================================================================================
       [CPU]     (      -/      -/   -/   -)|  98/98.0/98  |     98     98     98     98     98 
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
      FahCore_a8 (  55469/  55465/  41/C 19)| 384/387.0/389|    384   3898   3898   3860   3883 
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
          guider (  55767/   9591/   1/C  0)|   1/1.6/3    |      1      1      2      3      1 
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
    
    [Top RSS Info] (Unit: MB)
    ==========================================================================================================================================================
        COMM     (  PID  / PPID  / Nr / Pri)|  Max  |      1      2      3      4      5 
    ==========================================================================================================================================================
     [FREE/MIN]  (      -/      -/   -/   -)|124440 | 124442 124440 124440 124440 124440 
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
      FahCore_a8 (  55469/  55465/  41/C 19)|   548 |    548    548    548    548    548 
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
          guider (  55767/   9591/   1/C  0)|    34 |     33     34     34     34     34 
    ----------------------------------------------------------------------------------------------------------------------------------------------------------

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

    [Top Breakcall Info] [Time: 4542869.660] [Interval: 1.001] [NrSamples: 994] [a.out(1219772): 7%(Usr/0%+Sys/6%)] [guider(1219775): 97%]
    ==========================================================================================================================================================
     Usage  | Function [PATH] <Interval>
    ==========================================================================================================================================================
      16.7% | __mempcpy_sse2_unaligned_erms [/lib/x86_64-linux-gnu/libc-2.31.so] <Cnt: 166, Avg: 0.005994, Min: 0.002999, Max: 0.012299]
               100.0% |  <- _IO_new_file_xsputn[/lib/x86_64-linux-gnu/libc-2.31.so] <- __vfprintf_internal[/lib/x86_64-linux-gnu/libc-2.31.so]
                         <- printf[/lib/x86_64-linux-gnu/libc-2.31.so]
                         <- asdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasd
                         <- printPeace2[/home/peacelee/test/a.out] <- printPeace[/home/peacelee/test/a.out] <- main[/home/peacelee/test/a.out]
                         <- __libc_start_main[/lib/x86_64-linux-gnu/libc-2.31.so] <- _start[/home/peacelee/test/a.out]
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
      16.7% | _IO_new_file_xsputn [/lib/x86_64-linux-gnu/libc-2.31.so] <Cnt: 166, Avg: 0.005997, Min: 0.002988, Max: 0.012302]
               100.0% |  <- __vfprintf_internal[/lib/x86_64-linux-gnu/libc-2.31.so] <- printf[/lib/x86_64-linux-gnu/libc-2.31.so]
                         <- asdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasd
                         <- printPeace2[/home/peacelee/test/a.out] <- printPeace[/home/peacelee/test/a.out] <- main[/home/peacelee/test/a.out]
                         <- __libc_start_main[/lib/x86_64-linux-gnu/libc-2.31.so] <- _start[/home/peacelee/test/a.out]
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
      11.2% | __strchrnul_sse2 [/lib/x86_64-linux-gnu/libc-2.31.so] <Cnt: 111, Avg: 0.008974, Min: 0.006034, Max: 0.012381]
               100.0% |  <- __vfprintf_internal[/lib/x86_64-linux-gnu/libc-2.31.so] <- printf[/lib/x86_64-linux-gnu/libc-2.31.so]
                         <- asdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasd
                         <- printPeace2[/home/peacelee/test/a.out] <- printPeace[/home/peacelee/test/a.out] <- main[/home/peacelee/test/a.out]
                         <- __libc_start_main[/lib/x86_64-linux-gnu/libc-2.31.so] <- _start[/home/peacelee/test/a.out]
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
       5.5% | close@GLIBC_2.4 [/lib/x86_64-linux-gnu/libc-2.31.so] <Cnt: 55, Avg: 0.017763, Min: 0.017895, Max: 0.018863]
               100.0% |  <- asdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasd
                         <- printPeace2[/home/peacelee/test/a.out] <- printPeace[/home/peacelee/test/a.out] <- main[/home/peacelee/test/a.out]
                         <- __libc_start_main[/lib/x86_64-linux-gnu/libc-2.31.so] <- _start[/home/peacelee/test/a.out]
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
       5.5% | __vfprintf_internal [/lib/x86_64-linux-gnu/libc-2.31.so] <Cnt: 55, Avg: 0.017764, Min: 0.017838, Max: 0.018741]
               100.0% |  <- printf[/lib/x86_64-linux-gnu/libc-2.31.so]
                         <- asdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasd
                         <- printPeace2[/home/peacelee/test/a.out] <- printPeace[/home/peacelee/test/a.out] <- main[/home/peacelee/test/a.out]
                         <- __libc_start_main[/lib/x86_64-linux-gnu/libc-2.31.so] <- _start[/home/peacelee/test/a.out]
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
       5.5% | _IO_file_overflow@GLIBC_2.2.5 [/lib/x86_64-linux-gnu/libc-2.31.so] <Cnt: 55, Avg: 0.017764, Min: 0.017924, Max: 0.018732]
               100.0% |  <- _IO_new_file_xsputn[/lib/x86_64-linux-gnu/libc-2.31.so] <- __vfprintf_internal[/lib/x86_64-linux-gnu/libc-2.31.so]
                         <- printf[/lib/x86_64-linux-gnu/libc-2.31.so]
                         <- asdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasd
                         <- printPeace2[/home/peacelee/test/a.out] <- printPeace[/home/peacelee/test/a.out] <- main[/home/peacelee/test/a.out]
                         <- __libc_start_main[/lib/x86_64-linux-gnu/libc-2.31.so] <- _start[/home/peacelee/test/a.out]
    ----------------------------------------------------------------------------------------------------------------------------------------------------------

>>>

    # guider/guider.py pytop -g iotop -H

    [Top Pycall Info] [Time: 7469667.000] [Interval: 1.003] [NrSamples: 283] [iotop(2943070): 13%(Usr/10%+Sys/2%)] [guider(2943073): 53%] [SampleRate: 0.001]
    ==========================================================================================================================================================
     Usage  | Function [PATH] <Sample>
    ==========================================================================================================================================================
      56.9% | WAIT(poll@GLIBC_2.2.5) [/usr/lib/x86_64-linux-gnu/libc-2.31.so] <Cnt: 161>
               100.0% |  <- run[/usr/lib/python3/dist-packages/iotop/ui.py] <- run_iotop_window[/usr/lib/python3/dist-packages/iotop/ui.py]
                         <- wrapper[/usr/lib/python3.8/curses/__init__.py] <- run_iotop[/usr/lib/python3/dist-packages/iotop/ui.py]
                         <- <lambda>[/usr/lib/python3/dist-packages/iotop/ui.py] <- main[/usr/lib/python3/dist-packages/iotop/ui.py]
                         <- <module>[/usr/sbin/iotop] <Cnt: 161>
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
      10.2% | parse_proc_pid_status [/usr/lib/python3/dist-packages/iotop/data.py] <Cnt: 29>
               100.0% |  <- get_cmdline[/usr/lib/python3/dist-packages/iotop/data.py] <- format[/usr/lib/python3/dist-packages/iotop/ui.py]
                         <- get_data[/usr/lib/python3/dist-packages/iotop/ui.py] <- refresh_display[/usr/lib/python3/dist-packages/iotop/ui.py]
                         <- run[/usr/lib/python3/dist-packages/iotop/ui.py] <- run_iotop_window[/usr/lib/python3/dist-packages/iotop/ui.py]
                         <- wrapper[/usr/lib/python3.8/curses/__init__.py] <- run_iotop[/usr/lib/python3/dist-packages/iotop/ui.py]
                         <- <lambda>[/usr/lib/python3/dist-packages/iotop/ui.py] <- main[/usr/lib/python3/dist-packages/iotop/ui.py]
                         <- <module>[/usr/sbin/iotop] <Cnt: 29>
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
       4.6% | read@GLIBC_2.26 [/usr/lib/x86_64-linux-gnu/libc-2.31.so] <Cnt: 13>
                76.9% |  <- parse_proc_pid_status[/usr/lib/python3/dist-packages/iotop/data.py] <- get_cmdline[/usr/lib/python3/dist-packages/iotop/data.py]
                         <- format[/usr/lib/python3/dist-packages/iotop/ui.py] <- get_data[/usr/lib/python3/dist-packages/iotop/ui.py]
                         <- refresh_display[/usr/lib/python3/dist-packages/iotop/ui.py] <- run[/usr/lib/python3/dist-packages/iotop/ui.py]
                         <- run_iotop_window[/usr/lib/python3/dist-packages/iotop/ui.py] <- wrapper[/usr/lib/python3.8/curses/__init__.py]
                         <- run_iotop[/usr/lib/python3/dist-packages/iotop/ui.py] <- <lambda>[/usr/lib/python3/dist-packages/iotop/ui.py]
                         <- main[/usr/lib/python3/dist-packages/iotop/ui.py] <- <module>[/usr/sbin/iotop] <Cnt: 10>
                23.1% |  <- get_cmdline[/usr/lib/python3/dist-packages/iotop/data.py] <- format[/usr/lib/python3/dist-packages/iotop/ui.py]
                         <- get_data[/usr/lib/python3/dist-packages/iotop/ui.py] <- refresh_display[/usr/lib/python3/dist-packages/iotop/ui.py]
                         <- run[/usr/lib/python3/dist-packages/iotop/ui.py] <- run_iotop_window[/usr/lib/python3/dist-packages/iotop/ui.py]
                         <- wrapper[/usr/lib/python3.8/curses/__init__.py] <- run_iotop[/usr/lib/python3/dist-packages/iotop/ui.py]
                         <- <lambda>[/usr/lib/python3/dist-packages/iotop/ui.py] <- main[/usr/lib/python3/dist-packages/iotop/ui.py]
                         <- <module>[/usr/sbin/iotop] <Cnt: 3>
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
       4.2% | format [/usr/lib/python3/dist-packages/iotop/ui.py] <Cnt: 12>
               100.0% |  <- get_data[/usr/lib/python3/dist-packages/iotop/ui.py] <- refresh_display[/usr/lib/python3/dist-packages/iotop/ui.py]
                         <- run[/usr/lib/python3/dist-packages/iotop/ui.py] <- run_iotop_window[/usr/lib/python3/dist-packages/iotop/ui.py]
                         <- wrapper[/usr/lib/python3.8/curses/__init__.py] <- run_iotop[/usr/lib/python3/dist-packages/iotop/ui.py]
                         <- <lambda>[/usr/lib/python3/dist-packages/iotop/ui.py] <- main[/usr/lib/python3/dist-packages/iotop/ui.py]
                         <- <module>[/usr/sbin/iotop] <Cnt: 12>
    ----------------------------------------------------------------------------------------------------------------------------------------------------------

>>>
           
    # guider/guider.py ftop -g nginx

    [Top File Info] [Time: 497555.620] [Proc: 41] [FD: 2,047] [File: 87] [CPU: 95%(Usr:54%/Sys:41%)] (Unit: %/MB/NR)
    ==========================================================================================================================================================
        Process      ( ID  / Pid / Nr / Pri)| FD |                                                   Path                                                    |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
               nginx ( 1348/ 1333/   1/C  0)|  49| SOCKET: 42   NORMAL: 3   DEVICE: 2   EVENT: 2   PIPE: 0   PROC: 0                                         |
                                            |  49| /var/log/nginx/error.log (0, O_WRONLY|O_APPEND|O_CLOEXEC)                                                 |
                                            |  48| socket:[32124]                                                                                            |
                                            |  37| socket:[32102]                                                                                            |
                                            |  36| anon_inode:[eventfd]                                                                                      |
                                            |  35| anon_inode:[eventpoll]                                                                                    |
                                            |  34| socket:[32073]                                                                                            |
                                            |   8| socket:[32074]                                                                                            |
                                            |   7| socket:[20935]                                                                                            |
                                            |   6| socket:[20934] (TCP:0.0.0.0:80/LISTEN)                                                                    |
                                            |   5| /var/log/nginx/access.log (0, O_WRONLY|O_APPEND|O_CLOEXEC)                                                |
                                            |   3| socket:[32046]                                                                                            |
                                            |   2| /var/log/nginx/error.log (0, O_WRONLY)                                                                    |
                                            |   1| /dev/null (0, O_RDWR)                                                                                     |
                                            |   0| /dev/null (0, O_RDWR)                                                                                     |
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
    Total  | 98 %(97 / 0 / 0 / 0 )|124431(  96/  994/ 3531/1733)|     0(   0/  0/  0)|   0/0   |  0/0  |   0   |   0   | 11620  | 4613  |   70   |    1K/0   |
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

             _start/0x55e321d151ee [/home/peacelee/test/a.out]
               __libc_start_main/0x7ffb520af0b3 [/lib/x86_64-linux-gnu/libc-2.31.so]
                 main/0x55e321d15478 [/home/peacelee/test/a.out]
                   printPeace/0x55e321d15451 [/home/peacelee/test/a.out]
                     printPeace2/0x55e321d15392 [/home/peacelee/test/a.out]
                       asdfasdfasdfasdfasdfasdfasfdasdfasdfasdfasdfasdfasdfas/0x55e321d152e2 [/home/peacelee/test/a.out]
    0.000384             read@GLIBC_2.26/0x7ffb52199130(-0x1,0x0,0x0,0x0,0x0,0x5) [/lib/x86_64-linux-gnu/libc-2.31.so]
    0.000391             close@GLIBC_2.4/0x7ffb52199970(-0x1,0x0,0xffffffffffffff80,0x0,0x0,0x5) [/lib/x86_64-linux-gnu/libc-2.31.so]
    0.000398             printf/0x7ffb520ece10(0x55e321d1600a,0x9,0xffffffffffffff80,0x0,0x0,0x5) [/lib/x86_64-linux-gnu/libc-2.31.so]
    0.000405               __vfprintf_internal/0x7ffb521019e0(0x7ffb522746a0,0x55e321d1600a,0x7fff41688b40,0x55e321d1600a,0x0,0x5) [/lib/x86_64-linux-gnu/libc-2.31.so]
    0.000412                 __strchrnul_sse2/0x7ffb5213c820(0x55e321d1600a,0x25,0x7fff41688b40,0x55e321d1600a,0x0,0x5) [/lib/x86_64-linux-gnu/libc-2.31.so]
    0.000420                 _IO_new_file_xsputn/0x7ffb5211a750(0x7ffb522746a0,0x55e321d1600a,0x3,0x55e321d1600a,0x0,0x5) [/lib/x86_64-linux-gnu/libc-2.31.so]
    0.000426                   __mempcpy_sse2_unaligned_erms/0x7ffb52146d00(0x55e322290330,0x55e321d1600a,0x3,0x55e321d1600a,0x0,0x5) [/lib/x86_64-linux-gnu/libc-2.31.so]
    0.000432                 _itoa_word/0x7ffb520e6760(0x9,0x7fff41688af8,0xa,0x55e321d1600e,-0x1,0x3) [/lib/x86_64-linux-gnu/libc-2.31.so]
    0.000439                 _IO_new_file_xsputn/0x7ffb5211a750(0x7ffb522746a0,0x7fff41688af7,0x1,0x55e321d1600e,0x0,0x3) [/lib/x86_64-linux-gnu/libc-2.31.so]
    0.000446                   __mempcpy_sse2_unaligned_erms/0x7ffb52146d00(0x55e322290333,0x7fff41688af7,0x1,0x55e321d1600e,0x0,0x3) [/lib/x86_64-linux-gnu/libc-2.31.so]
    0.000452                 __strchrnul_sse2/0x7ffb5213c820(0x55e321d1600f,0x25,0x1,0x55e321d1600f,0x0,0x4) [/lib/x86_64-linux-gnu/libc-2.31.so]
    0.000458                 _IO_new_file_xsputn/0x7ffb5211a750(0x7ffb522746a0,0x55e321d1600f,0x1,0x55e321d1600f,0x0,0x4) [/lib/x86_64-linux-gnu/libc-2.31.so]
    0.000464                   __mempcpy_sse2_unaligned_erms/0x7ffb52146d00(0x55e322290334,0x55e321d1600f,0x1,0x55e321d1600f,0x0,0x4) [/lib/x86_64-linux-gnu/libc-2.31.so]
    0.000471                   _IO_file_overflow@GLIBC_2.2.5/0x7ffb5211bf00(0x7ffb522746a0,-0x1,0xc00,0x55e321d1600f,0x0,0x4) [/lib/x86_64-linux-gnu/libc-2.31.so]
    0.000480                   _IO_do_write@GLIBC_2.2.5/0x7ffb5211ba20(0x7ffb522746a0,0x55e322290330,0x5,0x55e321d1600f,0x0,0x4) [/lib/x86_64-linux-gnu/libc-2.31.so]
    0.000486                     _IO_file_write@GLIBC_2.2.5/0x7ffb52119fe0(0x7ffb522746a0,0x55e322290330,0x5,0x55e321d1600f,0x0,0x4) [/lib/x86_64-linux-gnu/libc-2.31.so]
    0.000493                       write@GLIBC_2.2.5/0x7ffb521991d0(0x1,0x55e322290330,0x5,0x55e321d1600f,0x0,0x4) [/lib/x86_64-linux-gnu/libc-2.31.so]

>>>

    # guider/guider.py  btrace -g yes -H -c \|getret

    0.532473       0x2cf0/0x560d7fd28cf0(0x1,0x560d81815440,0x2000,0x7faab23c8640,0x560d81815440,0x7c) [/usr/bin/yes]
    0.532488         0x4c40/0x560d7fd2ac40(0x1,0x560d81815440,0x2000,0x7faab23c8640,0x560d81815440,0x7c) [/usr/bin/yes]
    0.532501           write@GLIBC_2.2.5/0x7faab22f1040(0x1,0x560d81815440,0x2000,0x7faab23c8640,0x560d81815440,0x7c) [/lib/x86_64-linux-gnu/libc-2.31.so]
    0.532516           write@GLIBC_2.2.5[RET]=0x2000(8192)/0.000015 -> 0x4c40/0x560d7fd26000 [/usr/bin/yes]
    0.532557         0x4c40[RET]=0x2000(8192)/0.000069 -> 0x2cf0/0x560d7fd26000 [/usr/bin/yes]
    0.532618       0x2cf0[RET]=0x2000(8192)/0.000145 -> 0x2580/0x560d7fd26000 [/usr/bin/yes]
    0.532678       0x2cf0/0x560d7fd28cf0(0x1,0x560d81815440,0x2000,0x7faab23c8640,0x560d81815440,0x7c) [/usr/bin/yes]
    0.532691         0x4c40/0x560d7fd2ac40(0x1,0x560d81815440,0x2000,0x7faab23c8640,0x560d81815440,0x7c) [/usr/bin/yes]
    0.532706           write@GLIBC_2.2.5/0x7faab22f1040(0x1,0x560d81815440,0x2000,0x7faab23c8640,0x560d81815440,0x7c) [/lib/x86_64-linux-gnu/libc-2.31.so]
    0.532721           write@GLIBC_2.2.5[RET]=0x2000(8192)/0.000015 -> 0x4c40/0x560d7fd26000 [/usr/bin/yes]
    0.532798         0x4c40[RET]=0x2000(8192)/0.000107 -> 0x2cf0/0x560d7fd26000 [/usr/bin/yes]
    0.532881       0x2cf0[RET]=0x2000(8192)/0.000204 -> 0x2580/0x560d7fd26000 [/usr/bin/yes]
    0.532946       0x2cf0/0x560d7fd28cf0(0x1,0x560d81815440,0x2000,0x7faab23c8640,0x560d81815440,0x7c) [/usr/bin/yes]
    0.532961         0x4c40/0x560d7fd2ac40(0x1,0x560d81815440,0x2000,0x7faab23c8640,0x560d81815440,0x7c) [/usr/bin/yes]
    0.532975           write@GLIBC_2.2.5/0x7faab22f1040(0x1,0x560d81815440,0x2000,0x7faab23c8640,0x560d81815440,0x7c) [/lib/x86_64-linux-gnu/libc-2.31.so]
    0.532990           write@GLIBC_2.2.5[RET]=0x2000(8192)/0.000015 -> 0x4c40/0x560d7fd26000 [/usr/bin/yes]
    0.533067         0x4c40[RET]=0x2000(8192)/0.000106 -> 0x2cf0/0x560d7fd26000 [/usr/bin/yes]
    0.533194       0x2cf0[RET]=0x2000(8192)/0.000248 -> 0x2580/0x560d7fd26000 [/usr/bin/yes]

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

    # guider/guider.py limitcpu -g 22371:50

    [Info] limited cpu usage of yes(22371) process to 50%, it used 50%

    [Info] limited cpu usage of yes(22371) process to 50%, it used 50%

>>>

    # guider/guider.py sigtrace -g a.out

	[INFO] start profiling a.out(3100585)...

	0.000130 [SIGUSR1] {si_code=SI_USER si_pid=a.out(3100585), si_uid=root(0)}
	0.000276 [SIGUSR2] {si_code=SI_USER si_pid=a.out(3100585), si_uid=root(0)}
	0.000287 [SIGRT1] {si_code=SI_USER si_pid=a.out(3100585), si_uid=root(0)}
	0.000307 [SIGUSR1] {si_code=SI_USER si_pid=a.out(3100585), si_uid=root(0)}
	0.000317 [SIGUSR2] {si_code=SI_USER si_pid=a.out(3100585), si_uid=root(0)}
	0.000326 [SIGRT2] {si_code=SI_USER si_pid=a.out(3100585), si_uid=root(0)}
	1.955804 [SIGCHLD] {si_code=CLD_EXITED si_pid=3100586, si_uid=0, si_status=0 si_utime=0, si_stime=0}
	1.955816 [SIGUSR1] {si_code=SI_USER si_pid=a.out(3100585), si_uid=root(0)}
	1.955826 [SIGUSR2] {si_code=SI_USER si_pid=a.out(3100585), si_uid=root(0)}
	1.955836 [SIGRT3] {si_code=SI_USER si_pid=a.out(3100585), si_uid=root(0)}
	1.955846 [SIGUSR1] {si_code=SI_USER si_pid=a.out(3100585), si_uid=root(0)}
	1.955856 [SIGUSR2] {si_code=SI_USER si_pid=a.out(3100585), si_uid=root(0)}
	1.955866 [SIGRT4] {si_code=SI_USER si_pid=a.out(3100585), si_uid=root(0)}
	1.955875 [SIGUSR1] {si_code=SI_USER si_pid=a.out(3100585), si_uid=root(0)}
	1.955884 [SIGUSR2] {si_code=SI_USER si_pid=a.out(3100585), si_uid=root(0)}
	1.955893 [SIGRT5] {si_code=SI_USER si_pid=a.out(3100585), si_uid=root(0)}
	1.955903 [SIGUSR1] {si_code=SI_USER si_pid=a.out(3100585), si_uid=root(0)}
	1.955912 [SIGUSR2] {si_code=SI_USER si_pid=a.out(3100585), si_uid=root(0)}
	1.955922 [SIGRT6] {si_code=SI_USER si_pid=a.out(3100585), si_uid=root(0)}
	1.955931 [SIGUSR1] {si_code=SI_USER si_pid=a.out(3100585), si_uid=root(0)}
	1.955941 [SIGUSR2] {si_code=SI_USER si_pid=a.out(3100585), si_uid=root(0)}
	1.955950 [SIGRT7] {si_code=SI_USER si_pid=a.out(3100585), si_uid=root(0)}
	1.955959 [SIGUSR1] {si_code=SI_USER si_pid=a.out(3100585), si_uid=root(0)}
	1.955969 [SIGUSR2] {si_code=SI_USER si_pid=a.out(3100585), si_uid=root(0)}
	1.955978 [SIGRT8] {si_code=SI_USER si_pid=a.out(3100585), si_uid=root(0)}
	1.955987 [SIGUSR1] {si_code=SI_USER si_pid=a.out(3100585), si_uid=root(0)}
	1.955997 [SIGUSR2] {si_code=SI_USER si_pid=a.out(3100585), si_uid=root(0)}
	1.956006 [SIGRT9] {si_code=SI_USER si_pid=a.out(3100585), si_uid=root(0)}
	1.956015 [SIGUSR1] {si_code=SI_USER si_pid=a.out(3100585), si_uid=root(0)}
	1.956025 [SIGSEGV] {si_code=SEGV_MAPERR si_addr=0x4d2}

	2.191489 +++ exited a.out(3100585) with 139 +++

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

    # guider/guider.py printbind -g yes

    [Function Bind Info] [Target: yes(410113)]
    ==========================================================================================================================================================
    Path      Type Sym[Bind/Vis] => Link
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
    [/usr/bin/yes]
    	NOTYPE _ITM_deregisterTMCloneTable@GLIBC_2.2.5[WEAK/DEFAULT] => NONE
    	NOTYPE _ITM_registerTMCloneTable@GLIBC_2.2.5[WEAK/DEFAULT] => NONE
    	  FUNC __ctype_b_loc@GLIBC_2.2.5[GLOBAL/DEFAULT] => __ctype_b_loc/0x7f474b600400[/usr/lib/x86_64-linux-gnu/libc-2.31.so/0x37400]
    	  FUNC __cxa_atexit@GLIBC_2.2.5[GLOBAL/DEFAULT] => __cxa_atexit@GLIBC_2.2.5/0x7f474b612f60[/usr/lib/x86_64-linux-gnu/libc-2.31.so/0x49f60]
    	  FUNC __cxa_finalize@GLIBC_2.2.5[WEAK/DEFAULT] => __cxa_finalize@GLIBC_2.2.5/0x7f474b613090[/usr/lib/x86_64-linux-gnu/libc-2.31.so/0x4a090]
    	  FUNC __fpending@GLIBC_2.2.5[GLOBAL/DEFAULT] => __fpending@GLIBC_2.2.5/0x7f474b658f80[/usr/lib/x86_64-linux-gnu/libc-2.31.so/0x8ff80]
    	  FUNC __fprintf_chk[GLOBAL/DEFAULT] => __fprintf_chk@GLIBC_2.14/0x7f474b6fa110[/usr/lib/x86_64-linux-gnu/libc-2.31.so/0x131110]
    	  FUNC __freading@GLIBC_2.2.5[GLOBAL/DEFAULT] => __freading@GLIBC_2.2.5/0x7f474b658e90[/usr/lib/x86_64-linux-gnu/libc-2.31.so/0x8fe90]
    	NOTYPE __gmon_start__@GLIBC_2.14[WEAK/DEFAULT] => NONE
    	  FUNC __libc_start_main@GLIBC_2.2.5[GLOBAL/DEFAULT] => __libc_start_main@GLIBC_2.2.5/0x7f474b5effc0[/usr/lib/x86_64-linux-gnu/libc-2.31.so/0x26fc0]
    	  FUNC __printf_chk@GLIBC_2.2.5[GLOBAL/DEFAULT] => __printf_chk@GLIBC_2.2.5/0x7f474b6fa040[/usr/lib/x86_64-linux-gnu/libc-2.31.so/0x131040]
    	  FUNC __stack_chk_fail@GLIBC_2.2.5[GLOBAL/DEFAULT] => __stack_chk_fail@GLIBC_2.2.5/0x7f474b6fbb00[/usr/lib/x86_64-linux-gnu/libc-2.31.so/0x132b00]
    	  FUNC _exit@GLIBC_2.2.5[GLOBAL/DEFAULT] => _Exit@GLIBC_2.3/0x7f474b6af290[/usr/lib/x86_64-linux-gnu/libc-2.31.so/0xe6290]
    	  FUNC abort@GLIBC_2.2.5[GLOBAL/DEFAULT] => abort@GLIBC_2.2.5/0x7f474b5ee72e[/usr/lib/x86_64-linux-gnu/libc-2.31.so/0x2572e]
    	  FUNC bindtextdomain@GLIBC_2.2.5[GLOBAL/DEFAULT] => bindtextdomain@GLIBC_2.2.5/0x7f474b600920[/usr/lib/x86_64-linux-gnu/libc-2.31.so/0x37920]
    	  FUNC calloc[GLOBAL/DEFAULT] => calloc@GLIBC_2.2.5/0x7f474b667c90[/usr/lib/x86_64-linux-gnu/libc-2.31.so/0x9ec90]
    ----------------------------------------------------------------------------------------------------------------------------------------------------------

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
       
    # guider/guider.py iorec -s
    # guider/guider.py report -a

    [Thread Block Info] (Unit: NR)
    ==========================================================================================================================================================
               ID               OPT    NrDev                TOTAL         SEQUENTIAL(    %)      FS              PATH        
                                                         [ACCESS]                     COUNT                                  
    ==========================================================================================================================================================
              TOTAL            READ      8:3               131.8M             131.3M( 99.6)      -       /dev/sda3
                                              [   4.0K -    7.0K]                       370                                  
                                              [  16.0K -   31.0K]                        11                                  
                                              [  32.0K -   63.0K]                         6                                  
                                              [  64.0K -  127.0K]                         5                                  
                                              [ 128.0K -  255.0K]                      1037                                  
                                       253:0               131.8M             131.3M( 99.6)     ext4     / <rw,relatime>
                                              [   4.0K -    7.0K]                       370                                  
                                              [  16.0K -   31.0K]                        11                                  
                                              [  32.0K -   63.0K]                         6                                  
                                              [  64.0K -  127.0K]                         5                                  
                                              [ 128.0K -  255.0K]                      1037                                  
                              WRITE    253:0                40.0K              20.0K( 50.0)     ext4     / <rw,relatime>
                                              [   4.0K -    7.0K]                        10                                  
                                         8:3                24.0K              20.0K( 83.3)      -       /dev/sda3
                                              [   4.0K -    7.0K]                         6                                  
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
              guider(4011197)  READ      8:3               100.0M             100.0M(100.0)      -       /dev/sda3
                                              [  16.0K -   31.0K]                         2                                  
                                              [  32.0K -   63.0K]                         1                                  
                                              [  64.0K -  127.0K]                         1                                  
                                              [ 128.0K -  255.0K]                       799                                  
                                       253:0               100.0M             100.0M(100.0)     ext4     / <rw,relatime>
                                              [  16.0K -   31.0K]                         2                                  
                                              [  32.0K -   63.0K]                         1                                  
                                              [  64.0K -  127.0K]                         1                                  
                                              [ 128.0K -  255.0K]                       799                                  
    ----------------------------------------------------------------------------------------------------------------------------------------------------------

    [Thread FS Info] (Unit: NR)
    ==========================================================================================================================================================
               ID                 OPT    NrDev        INODE         Size           FS PATH                                                                       
    ==========================================================================================================================================================
              TOTAL             WRITE                              16.0K 
                                         253:0                     16.0K         ext4 / <rw,relatime>                                                            
                                                          0        16.0K                                                                                         
                                 READ                             131.8M 
                                           0:3                      1.4M            ? ?                                                                          
                                                          0         1.4M                                                                                         
                                         253:0                    130.4M         ext4 / <rw,relatime>                                                            
                                                   24520383       100.0M              /home/peacelee/guider/guider/TEST2[100.0M]                                 
                                                   24520372        20.0M              /home/peacelee/guider/guider/TEST[20.0M]                                   
                                                   24520353        10.0M              /home/peacelee/guider/guider/TEST3[10.0M]                                  
                                                    6030383        84.0K                                                                                         
                                                    6819964        72.0K                                                                                         
                                                    6029790        68.0K                                                                                         
                                                    6031485        44.0K                                                                                         
                                                    6031543        40.0K                                                                                         
                                                    6819797        16.0K                                                                                         
                                                    6035523        16.0K                                                                                         
                                                          0        16.0K                                                                                         
                                                    6818557         4.0K                                                                                         
                                                    6818689         4.0K                                                                                         
                                                    7078584         4.0K                                                                                         
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
              guider(4011197)    READ                             100.0M 
                                         253:0                    100.0M         ext4 / <rw,relatime>                                                            
                                                   24520383       100.0M              /home/peacelee/guider/guider/TEST2[100.0M]                                 
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
              guider(4011193)    READ                              20.0M 
                                         253:0                     20.0M         ext4 / <rw,relatime>                                                            
                                                   24520372        20.0M              /home/peacelee/guider/guider/TEST[20.0M]                                   
    ----------------------------------------------------------------------------------------------------------------------------------------------------------
       
>>>
       
    # guider/guider.py iorec -s
    # guider/guider.py report -q RALIST
    # guider/guider.py readahead readahead.list

    [INFO] start readahead from '/home/peacelee/guider/guider/readahead.list'

    [INFO] changed the CPU scheduling priority for guider(4011281) to 10[C]

    [INFO] changed the I/O scheduling priority for guider(4011281) to IOPRIO_CLASS_IDLE(0)[IOPRIO_WHO_PROCESS]

    [INFO] finished readahead a total of 130.0M data for 0.002 sec
       
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
    # guider/guider.py report -a
    # cat guider.out

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
       
    # guider/guider.py funcrec -e m -s .
    # guider/guider.py report -a
    # cat guider.out

    [Function Page Info] [Total: 11.4M] [Alloc: 11.4M(817)] [Free: 188.0K(47)] (USER)
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
  
    [Function Page Info] [Total: 11.4K] [Alloc: 11.4K(817)] [Free: 188.0K(47)] (KERNEL)
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

    [File Usage Info] [ File: 281 ] [ RAM: 78.0M ] [ Keys: Foward/Back/Save/Quit ]
    ==========================================================================================================================================================
    ____RAM_____|___File___|__%___|_____________________________________________________Library & Process_____________________________________________________
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
![guider-timeline](https://github.com/iipeace/iipeace.github.io/blob/master/samples/guider_timeline.png)
![guider-flamegraph](https://github.com/iipeace/iipeace.github.io/blob/master/samples/guider_flamegraph.png)
![guider-average](https://github.com/iipeace/iipeace.github.io/blob/master/samples/guider_drawavg.svg)
![guider-request](https://github.com/iipeace/iipeace.github.io/blob/master/samples/guider_drawreq.svg)

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
If you can run 'pip' on your system then just enter the following commands:
    # pip install guider
    # pip3 install guider
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
    [CONTROL]       cli               <Client>
                    event             <Event>
                    list              <List>
                    send              <Signal>
                    server            <Server>
                    start             <Signal>

    [LOG]           logdlt            <DLT>
                    logjrl            <Journal>
                    logkmsg           <Kernel>
                    logsys            <Syslog>
                    printdlt          <DLT>
                    printjrl          <Journal>
                    printkmsg         <Kernel>
                    printsys          <Syslog>

    [MONITOR]       atop              <System>
                    bgtop             <Background>
                    btop              <Function>
                    cgtop             <Cgroup>
                    ctop              <Threshold>
                    dbustop           <D-Bus>
                    disktop           <Storage>
                    dlttop            <DLT>
                    ftop              <File>
                    mtop              <Memory>
                    ntop              <Network>
                    ptop              <PMU>
                    pytop             <Python>
                    rtop              <JSON>
                    stacktop          <Stack>
                    systop            <Syscall>
                    top               <Process>
                    ttop              <Thread>
                    utop              <Function>
                    wtop              <WSS>

    [PROFILE]       filerec           <File>
                    funcrec           <Function>
                    genrec            <System>
                    iorec             <I/O>
                    mem               <Page>
                    rec               <Thread>
                    report            <Report>
                    sysrec            <Syscall>

    [TEST]          cputest           <CPU>
                    iotest            <Storage>
                    memtest           <Memory>
                    nettest           <Network>

    [TRACE]         btrace            <Breakpoint>
                    pytrace           <Python>
                    sigtrace          <Signal>
                    strace            <Syscall>
                    utrace            <Function>

    [UTIL]          addr2sym          <Symbol>
                    comp              <Compress>
                    decomp            <Decompress>
                    dump              <Memory>
                    exec              <Command>
                    getafnt           <Affinity>
                    hook              <Function>
                    kill/tkill        <Signal>
                    leaktrace         <Leak>
                    limitcpu          <CPU>
                    mkcache           <Cache>
                    pause             <Thread>
                    ping              <PING>
                    printbind         <Funcion>
                    printcg           <Cgroup>
                    printdbus         <D-Bus>
                    printdbusintro    <D-Bus>
                    printdbusstat     <D-Bus>
                    printdbussub      <D-Bus>
                    printdir          <Dir>
                    printenv          <Env>
                    printext          <Ext4>
                    printinfo         <System>
                    printns           <Namespace>
                    printsig          <Signal>
                    printsvc          <systemd>
                    pstree            <Process>
                    readahead         <File>
                    readelf           <File>
                    remote            <Command>
                    req               <URL>
                    rlimit            <Resource>
                    setafnt           <Affinity>
                    setcpu            <Clock>
                    setsched          <Priority>
                    strings           <Text>
                    sym2addr          <Address>
                    systat            <Status>
                    topdiff           <Diff>
                    topsum            <Summary>
                    watch             <File>

    [VISUAL]        convert           <Text>
                    draw              <System>
                    drawavg           <Average>
                    drawcpu           <CPU>
                    drawcpuavg        <CPU>
                    drawdelay         <Delay>
                    drawflame         <Function>
                    drawio            <I/O>
                    drawleak          <Leak>
                    drawmem           <Memory>
                    drawmemavg        <Memory>
                    drawreq           <URL>
                    drawrss           <RSS>
                    drawrssavg        <RSS>
                    drawtime          <Timeline>
                    drawvss           <VSS>
                    drawvssavg        <VSS>

FILE:
    Profile file (e.g. guider.dat)
    Report  file (e.g. guider.out)

Options:
    Check COMMAND with --help (e.g. ./guider.py top --help)
```
