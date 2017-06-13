#!/usr/bin/python

__author__ = "Peace Lee"
__copyright__ = "Copyright 2015-2017, guider"
__module__ = "guider"
__credits__ = "Peace Lee"
__license__ = "GPLv2"
__version__ = "3.8.2"
__maintainer__ = "Peace Lee"
__email__ = "iipeace5@gmail.com"
__repository__ = "https://github.com/iipeace/guider"





try:
    import re
    import sys
    import signal
    import time
    import os
    import shutil
    import gc
    import imp
    import atexit
    import struct
except ImportError:
    err = sys.exc_info()[1]
    print("[Error] Fail to import default packages: " + err.args[0])
    sys.exit(0)





class ConfigManager(object):
    """ Manager for configuration """

    # Define color #
    if sys.platform.startswith('linux'):
        WARNING = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        SPECIAL = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
    else:
        WARNING = ''
        OKBLUE = ''
        OKGREEN = ''
        SPECIAL = ''
        FAIL = ''
        ENDC = ''
        BOLD = ''
        UNDERLINE = ''

    # Define state of process #
    procStatList = {
        'R': 'running',
        'S': 'sleep',
        'D': 'disk',
        'Z': 'zombie',
        'T': 'traced',
        'W': 'paging'
        }

    # Define syscall for ARM #
    sysList_arm = [
        'sys_restart_syscall', 'sys_exit', 'sys_fork', 'sys_read', 'sys_write', 'sys_open',
        'sys_close', 'sys_sys_waitpid', 'sys_creat', 'sys_link', 'sys_unlink', #10#
        'sys_execve', 'sys_chdir', 'sys_time', 'sys_mknod', 'sys_chmod',
        'sys_lchown16', 'sys_break', 'sys_sys_stat', 'sys_lseek', 'sys_getpid', #20#
        'sys_mount', 'sys_oldumount', 'sys_setuid16', 'sys_getuid16', 'sys_stime',
        'sys_ptrace', 'sys_alarm', 'sys_fstat', 'sys_pause', 'sys_utime', #30#
        'sys_stty', 'sys_getty', 'sys_access', 'sys_nice', 'sys_ftime',
        'sys_sync', 'sys_kill', 'sys_rename', 'sys_mkdir', 'sys_rmdir', #40#
        'sys_dup', 'sys_pipe', 'sys_times', 'sys_prof', 'sys_brk',
        'sys_setgid16', 'sys_getgid16', 'sys_signal', 'sys_geteuid16', 'sys_getegid16', #50#
        'sys_acct', 'sys_umount', 'sys_lock', 'sys_ioctl', 'sys_fcntl',
        'sys_mpx', 'sys_setpgid', 'sys_ulimit', 'sys_olduname', 'sys_umask', #60#
        'sys_chroot', 'sys_ustat', 'sys_dup2', 'sys_getppid', 'sys_getpgrp',
        'sys_setsid', 'sys_sigaction', 'sys_sgetmask', 'sys_ssetmask', 'sys_setreuid16', #70#
        'sys_setregid16', 'sys_sigsuspend', 'sys_sigpending', 'sys_sethostname', 'sys_setrlimit',
        'sys_old_getrlimit', 'sys_getrusage', 'sys_gettimeofday', 'sys_settimeofday', 'sys_getgroups16', #80#
        'sys_setgroups16', 'sys_old_select', 'sys_symlink', 'sys_lstat', 'sys_readlink',
        'sys_uselib', 'sys_swapon', 'sys_reboot', 'sys_old_readdir', 'sys_old_mmap', #90#
        'sys_munmap', 'sys_truncate', 'sys_ftruncate', 'sys_fchmod', 'sys_fchown16',
        'sys_getpriority', 'sys_setpriority', 'sys_profil', 'sys_statfs', 'sys_fstatfs', #100#
        'sys_ioperm', 'sys_socketcall', 'sys_syslog', 'sys_setitimer', 'sys_getitimer',
        'sys_newstat', 'sys_newlstat', 'sys_newfstat', 'sys_uname', 'sys_iopl', #110#
        'sys_vhangup', 'sys_ni_syscall', 'sys_syscall', 'sys_wait4', 'sys_swapoff',
        'sys_sysinfo', 'sys_ipc', 'sys_fsync', 'sys_sigreturn_wrapper', 'sys_clone', #120#
        'sys_setdomainname', 'sys_newuname', 'sys_modify_ldt', 'sys_adjtimex', 'sys_mprotect',
        'sys_sigprocmask', 'sys_create_module', 'sys_init_module', 'sys_delete_module', 'sys_get_kernel_syms', #130#
        'sys_quotactl', 'sys_getpgid', 'sys_fchdir', 'sys_bdflush', 'sys_sysfs',
        'sys_personality', 'sys_afs_syscall', 'sys_setfsuid16', 'sys_setfsgid16', 'sys_llseek', #140#
        'sys_getdents', 'sys_select', 'sys_flock', 'sys_msync', 'sys_readv',
        'sys_writev', 'sys_getsid', 'sys_fdatasync', 'sys_sysctl', 'sys_mlock', #150#
        'sys_munlock', 'sys_mlockall', 'sys_munlockall', 'sys_sched_setparam', 'sys_sched_getparam',
        'sys_sched_setscheduler', 'sys_sched_getscheduler', 'sys_sched_yield', 'sys_sched_get_priority_max', #159#
        'sys_sched_get_priority_min', 'sys_sched_rr_get_interval', 'sys_nanosleep', 'sys_mremap',
        'sys_setresuid16', 'sys_getresuid16', 'sys_vm86', 'sys_query_module', 'sys_poll', 'sys_nfsservctl', #169#
        'sys_setresgid16', 'sys_getresgid16', 'sys_prctl', 'sys_rt_sigreturn_wrapper', 'sys_rt_sigaction',
        'sys_rt_sigprocmask', 'sys_rt_sigpending', 'sys_rt_sigtimedwait', 'sys_rt_sigqueueinfo', #178#
        'sys_rt_sigsuspend', 'sys_pread64', 'sys_pwrite64', 'sys_chown16', 'sys_getcwd', 'sys_capget',
        'sys_capset', 'sys_sigaltstack', 'sys_sendfile', 'sys_getpmsg', 'sys_putpmsg', 'sys_vfork', #190#
        'sys_getrlimit', 'sys_mmap2', 'sys_truncate64', 'sys_ftruncate64', 'sys_stat64', 'sys_lstat64',
        'sys_fstat64', 'sys_lchown', 'sys_getuid', 'sys_getgid', 'sys_geteuid', 'sys_getegid', #203#
        'sys_setreuid', 'sys_setregid', 'sys_getgroups', 'sys_setgroups', 'sys_fchown', 'sys_setresuid', #208#
        'sys_getresuid', 'sys_setresgid', 'sys_getresgid', 'sys_chown', 'sys_setuid', 'sys_setgid',
        'sys_setfsuid', 'sys_setfsgid', 'sys_getdents64', 'sys_pivot_root', 'sys_mincore', 'sys_madvise', #220#
        'sys_fcntl64', 'sys_TUX', 'sys_ni_syscall', 'sys_gettid', 'sys_readahead', 'sys_setxattr', 'sys_lsetxattr',
        'sys_fsetxattr', 'sys_getxattr', 'sys_lgetxattr', 'sys_fgetxattr', 'sys_listxattr', 'sys_llistxattr', #233#
        'sys_flistxattr', 'sys_removexattr', 'sys_lremovexattr', 'sys_fremovexattr', 'sys_tkill', 'sys_sendfile64',
        'sys_futex', 'sys_sched_setaffinity', 'sys_sched_getaffinity', 'sys_io_setup', 'sys_io_destroy',
        'sys_io_getevents', 'sys_io_submit', 'sys_io_cancel', 'sys_exit_group', 'sys_lookup_dcookie', #249#
        'sys_epoll_create', 'sys_epoll_ctl', 'sys_epoll_wait', 'sys_remap_file_pages', 'sys_set_thread_area',
        'sys_get_thread_area', 'sys_set_tid_address', 'sys_timer_create', 'sys_timer_settime', 'sys_timer_gettime',
        'sys_timer_getoverrun', 'sys_timer_delete', 'sys_clock_settime', 'sys_clock_gettime', 'sys_clock_getres',
        'sys_clock_nanosleep', 'sys_statfs64_wrapper', 'sys_fstatfs64_wrapper', 'sys_tgkill', 'sys_utimes', #269#
        'sys_arm_fadvise64_64', 'sys_pciconfig_iobase', 'sys_pciconfig_read', 'sys_pciconfig_write', 'sys_mq_open',
        'sys_mq_unlink', 'sys_mq_timedsend', 'sys_mq_timedreceive', 'sys_mq_notify', 'sys_mq_getsetattr', 'sys_waitid', #280#
        'sys_socket', 'sys_bind', 'sys_connect', 'sys_listen', 'sys_accept', 'sys_getsockname', 'sys_getpeername',
        'sys_socketpair', 'sys_send', 'sys_sendto', 'sys_recv', 'sys_recvfrom', 'sys_shutdown', 'sys_setsockopt',
        'sys_getsockopt', 'sys_sendmsg', 'sys_recvmsg', 'sys_semop', 'sys_semget', 'sys_semctl', #300#
        'sys_msgsnd', 'sys_msgrcv', 'sys_msgget', 'sys_msgctl', 'sys_shmat', 'sys_shmdt', 'sys_shmget', 'sys_shmctl',
        'sys_add_key', 'sys_request_key', 'sys_keyctl', 'sys_semtimedop', 'sys_vserver', 'sys_ioprio_set',
        'sys_ioprio_get', 'sys_inotify_init', 'sys_inotify_add_watch', 'sys_inotify_rm_watch', 'sys_mbind', #319#
        'sys_get_mempolicy', 'sys_set_mempolicy', 'sys_openat', 'sys_mkdirat', 'sys_mknodat', 'sys_fchownat',
        'sys_futimesat', 'sys_fstatat64', 'sys_unlinkat', 'sys_renameat', 'sys_linkat', #330#
        'sys_symlinkat', 'sys_readlinkat', 'sys_fchmodat', 'sys_faccessat', 'sys_pselect6', 'sys_ppoll',
        'sys_unshare', 'sys_set_robust_list', 'sys_get_robust_list', 'sys_splice', #340#
        'sys_sync_file_range2', 'sys_tee', 'sys_vmsplice', 'sys_move_pages', 'sys_getcpu', 'sys_epoll_pwait',
        'sys_kexec_load', 'sys_utimensat', 'sys_signalfd', 'sys_timerfd_create', 'sys_eventfd', 'sys_fallocate',
        'sys_timerfd_settime', 'sys_timerfd_gettime', 'sys_signalfd4', 'sys_eventfd2', 'sys_epoll_create1', #357#
        'sys_dup3', 'sys_pipe2', 'sys_inotify_init1', 'sys_preadv', 'sys_pwritev', 'sys_rt_tgsigqueueinfo',
        'sys_perf_event_open', 'sys_recvmmsg', 'sys_accept4', 'sys_fanotify_init', 'sys_fanotify_mark', #368#
        'sys_prlimit64', 'sys_name_to_handle_at', 'sys_open_by_handle_at', 'sys_clock_adjtime', 'sys_syncfs',
        'sys_sendmmsg', 'sys_setns', 'sys_process_vm_readv', 'sys_process_vm_writev', 'sys_kcmp', 'sys_finit_module',
        'sys_sched_setattr', 'sys_sched_getattr', 'sys_renameat2', 'sys_seccomp', 'sys_getrandom', 'sys_memfd_create',
        'sys_bpf', 'sys_execveat', 'sys_userfaultfd', 'sys_membarrier', 'sys_mlock2', 'sys_copy_file_range' #391#
        ]

    # Define syscall for x86_32 #
    sysList_x86 = [
        'sys_restart_syscall', 'sys_exit', 'sys_fork', 'sys_read', 'sys_write', 'sys_open', 'sys_close', 'sys_waitpid',
        'sys_creat', 'sys_link', 'sys_unlink', 'sys_execve', 'sys_chdir', 'sys_time', 'sys_mknod', 'sys_chmod',
        'sys_lchown', 'sys_break', 'sys_oldstat', 'sys_lseek', 'sys_getpid', 'sys_mount', 'sys_umount', 'sys_setuid',
        'sys_getuid', 'sys_stime', 'sys_ptrace', 'sys_alarm', 'sys_oldfstat', 'sys_pause', 'sys_utime', 'sys_stty',
        'sys_gtty', 'sys_access', 'sys_nice', 'sys_ftime', 'sys_sync', 'sys_kill', 'sys_rename', 'sys_mkdir',
        'sys_rmdir', 'sys_dup', 'sys_pipe', 'sys_times', 'sys_prof', 'sys_brk', 'sys_setgid', 'sys_getgid', 'sys_signal',
        'sys_geteuid', 'sys_getegid', 'sys_acct', 'sys_umount2', 'sys_lock', 'sys_ioctl', 'sys_fcntl', 'sys_mpx',
        'sys_setpgid', 'sys_ulimit', 'sys_oldolduname', 'sys_umask', 'sys_chroot', 'sys_ustat', 'sys_dup2',
        'sys_getppid', 'sys_getpgrp', 'sys_setsid', 'sys_sigaction', 'sys_sgetmask', 'sys_ssetmask', 'sys_setreuid',
        'sys_setregid', 'sys_sigsuspend', 'sys_sigpending', 'sys_sethostname', 'sys_setrlimit', 'sys_getrlimit',
        'sys_getrusage', 'sys_gettimeofday', 'sys_settimeofday', 'sys_getgroups', 'sys_setgroups', 'sys_select',
        'sys_symlink', 'sys_oldlstat', 'sys_readlink', 'sys_uselib', 'sys_swapon', 'sys_reboot', 'sys_readdir',
        'sys_mmap', 'sys_munmap', 'sys_truncate', 'sys_ftruncate', 'sys_fchmod', 'sys_fchown', 'sys_getpriority',
        'sys_setpriority', 'sys_profil', 'sys_statfs', 'sys_fstatfs', 'sys_ioperm', 'sys_socketcall', 'sys_syslog',
        'sys_setitimer', 'sys_getitimer', 'sys_stat', 'sys_lstat', 'sys_fstat', 'sys_olduname', 'sys_iopl',
        'sys_vhangup', 'sys_idle', 'sys_vm86old', 'sys_wait4', 'sys_swapoff', 'sys_sysinfo', 'sys_ipc', 'sys_fsync',
        'sys_sigreturn', 'sys_clone', 'sys_setdomainname', 'sys_uname', 'sys_modify_ldt', 'sys_adjtimex', 'sys_mprotect',
        'sys_sigprocmask', 'sys_create_module', 'sys_init_module', 'sys_delete_module', 'sys_get_kernel_syms',
        'sys_quotactl', 'sys_getpgid', 'sys_fchdir', 'sys_bdflush', 'sys_sysfs', 'sys_personality', 'sys_afs_syscall',
        'sys_setfsuid', 'sys_setfsgid', 'sys__llseek', 'sys_getdents', 'sys__newselect', 'sys_flock', 'sys_msync',
        'sys_readv', 'sys_writev', 'sys_getsid', 'sys_fdatasync', 'sys__sysctl', 'sys_mlock', 'sys_munlock',
        'sys_mlockall', 'sys_munlockall', 'sys_sched_setparam', 'sys_sched_getparam', 'sys_sched_setscheduler',
        'sys_sched_getscheduler', 'sys_sched_yield', 'sys_sched_get_priority_max', 'sys_sched_get_priority_min',
        'sys_sched_rr_get_interval', 'sys_nanosleep', 'sys_mremap', 'sys_setresuid', 'sys_getresuid', 'sys_vm86',
        'sys_query_module', 'sys_poll', 'sys_nfsservctl', 'sys_setresgid', 'sys_getresgid', 'sys_prctl',
        'sys_rt_sigreturn', 'sys_rt_sigaction', 'sys_rt_sigprocmask', 'sys_rt_sigpending', 'sys_rt_sigtimedwait',
        'sys_rt_sigqueueinfo', 'sys_rt_sigsuspend', 'sys_pread64', 'sys_pwrite64', 'sys_chown', 'sys_getcwd',
        'sys_capget', 'sys_capset', 'sys_sigaltstack', 'sys_sendfile', 'sys_getpmsg', 'sys_putpmsg', 'sys_vfork',
        'sys_ugetrlimit', 'sys_mmap2', 'sys_truncate64', 'sys_ftruncate64', 'sys_stat64', 'sys_lstat64', 'sys_fstat64',
        'sys_lchown32', 'sys_getuid32', 'sys_getgid32', 'sys_geteuid32', 'sys_getegid32', 'sys_setreuid32',
        'sys_setregid32', 'sys_getgroups32', 'sys_setgroups32', 'sys_fchown32', 'sys_setresuid32', 'sys_getresuid32',
        'sys_setresgid32', 'sys_getresgid32', 'sys_chown32', 'sys_setuid32', 'sys_setgid32', 'sys_setfsuid32',
        'sys_setfsgid32', 'sys_pivot_root', 'sys_mincore', 'sys_madvise', 'sys_getdents64', 'sys_fcntl64', 'N/A',
        'N/A', 'sys_gettid', 'sys_readahead', 'sys_setxattr', 'sys_lsetxattr', 'sys_fsetxattr', 'sys_getxattr',
        'sys_lgetxattr', 'sys_fgetxattr', 'sys_listxattr', 'sys_llistxattr', 'sys_flistxattr', 'sys_removexattr',
        'sys_lremovexattr', 'sys_fremovexattr', 'sys_tkill', 'sys_sendfile64', 'sys_futex', 'sys_sched_setaffinity',
        'sys_sched_getaffinity', 'sys_set_thread_area', 'sys_get_thread_area', 'sys_io_setup', 'sys_io_destroy',
        'sys_io_getevents', 'sys_io_submit', 'sys_io_cancel', 'sys_fadvise64', 'N/A', 'sys_exit_group',
        'sys_lookup_dcookie', 'sys_epoll_create', 'sys_epoll_ctl', 'sys_epoll_wait', 'sys_remap_file_pages',
        'sys_set_tid_address', 'sys_timer_create', 'sys_timer_settime', 'sys_timer_gettime', 'sys_timer_getoverrun',
        'sys_timer_delete', 'sys_clock_settime', 'sys_clock_gettime', 'sys_clock_getres', 'sys_clock_nanosleep',
        'sys_statfs64', 'sys_fstatfs64', 'sys_tgkill', 'sys_utimes', 'sys_fadvise64_64', 'sys_vserver', 'sys_mbind',
        'sys_get_mempolicy', 'sys_set_mempolicy', 'sys_mq_open', 'sys_mq_unlink', 'sys_mq_timedsend',
        'sys_mq_timedreceive', 'sys_mq_notify', 'sys_mq_getsetattr', 'sys_kexec_load', 'sys_waitid',
        'sys_setaltroot', 'sys_add_key', 'sys_request_key', 'sys_keyctl', 'sys_ioprio_set', 'sys_ioprio_get',
        'sys_inotify_init', 'sys_inotify_add_watch', 'sys_inotify_rm_watch', 'sys_migrate_pages', 'sys_openat',
        'sys_mkdirat', 'sys_mknodat', 'sys_fchownat', 'sys_futimesat', 'sys_fstatat64', 'sys_unlinkat', 'sys_renameat',
        'sys_linkat', 'sys_symlinkat', 'sys_readlinkat', 'sys_fchmodat', 'sys_faccessat', 'sys_pselect6', 'sys_ppoll',
        'sys_unshare', 'sys_set_robust_list', 'sys_get_robust_list', 'sys_splice', 'sys_sync_file_range', 'sys_tee',
        'sys_vmsplice', 'sys_move_pages', 'sys_getcpu', 'sys_epoll_pwait', 'sys_utimensat', 'sys_signalfd',
        'sys_timerfd_create', 'sys_eventfd', 'sys_fallocate', 'sys_timerfd_settime', 'sys_timerfd_gettime', 'sys_signalfd4',
        'sys_eventfd2', 'sys_epoll_create1', 'sys_dup3', 'sys_pipe2', 'sys_inotify_init1', 'sys_preadv', 'sys_pwritev',
        'sys_rt_tgsigqueueinfo', 'sys_perf_event_open', 'sys_recvmmsg', 'sys_fanotify_init', 'sys_fanotify_mark',
        'sys_prlimit64', 'sys_name_to_handle_at', 'sys_open_by_handle_at', 'sys_clock_adjtime', 'sys_syncfs',
        'sys_sendmmsg', 'sys_setns', 'sys_process_vm_readv', 'sys_process_vm_writev', 'sys_kcmp', 'sys_finit_module',
        'sys_sched_setattr', 'sys_sched_getattr', 'sys_renameat2', 'sys_seccomp', 'sys_getrandom', 'sys_memfd_create',
        'sys_bpf', 'sys_execveat', 'sys_socket', 'sys_socketpair', 'sys_bind', 'sys_connect', 'sys_listen', 'sys_accept4',
        'sys_getsockopt', 'sys_setsockopt', 'sys_getsockname', 'sys_getpeername', 'sys_sendto', 'sys_sendmsg',
        'sys_recvfrom', 'sys_recvmsg', 'sys_shutdown', 'sys_userfaultfd', 'sys_membarrier', 'sys_mlock2', 'sys_copy_file_range'
        ]

    # Define syscall for x86_64 #
    sysList_x64 = [
        'sys_read', 'sys_write', 'sys_open', 'sys_close', 'sys_stat', 'sys_fstat', 'sys_lstat', 'sys_poll', 'sys_lseek',
        'sys_mmap', 'sys_mprotect', 'sys_munmap', 'sys_brk', 'sys_rt_sigaction', 'sys_rt_sigprocmask', 'sys_rt_sigreturn',
        'sys_ioctl', 'sys_pread64', 'sys_pwrite64', 'sys_readv', 'sys_writev', 'sys_access', 'sys_pipe', 'sys_select',
        'sys_sched_yield', 'sys_mremap', 'sys_msync', 'sys_mincore', 'sys_madvise', 'sys_shmget', 'sys_shmat', 'sys_shmctl',
        'sys_dup', 'sys_dup2', 'sys_pause', 'sys_nanosleep', 'sys_getitimer', 'sys_alarm', 'sys_setitimer', 'sys_getpid',
        'sys_sendfile', 'sys_socket', 'sys_connect', 'sys_accept', 'sys_sendto', 'sys_recvfrom', 'sys_sendmsg', 'sys_recvmsg',
        'sys_shutdown', 'sys_bind', 'sys_listen', 'sys_getsockname', 'sys_getpeername', 'sys_socketpair', 'sys_setsockopt',
        'sys_getsockopt', 'sys_clone', 'sys_fork', 'sys_vfork', 'sys_execve', 'sys_exit', 'sys_wait4', 'sys_kill',
        'sys_uname', 'sys_semget', 'sys_semop', 'sys_semctl', 'sys_shmdt', 'sys_msgget', 'sys_msgsnd', 'sys_msgrcv',
        'sys_msgctl', 'sys_fcntl', 'sys_flock', 'sys_fsync', 'sys_fdatasync', 'sys_truncate', 'sys_ftruncate',
        'sys_getdents', 'sys_getcwd', 'sys_chdir', 'sys_fchdir', 'sys_rename', 'sys_mkdir', 'sys_rmdir', 'sys_creat',
        'sys_link', 'sys_unlink', 'sys_symlink', 'sys_readlink', 'sys_chmod', 'sys_fchmod', 'sys_chown', 'sys_fchown',
        'sys_lchown', 'sys_umask', 'sys_gettimeofday', 'sys_getrlimit', 'sys_getrusage', 'sys_sysinfo', 'sys_times',
        'sys_ptrace', 'sys_getuid', 'sys_syslog', 'sys_getgid', 'sys_setuid', 'sys_setgid', 'sys_geteuid', 'sys_getegid',
        'sys_setpgid', 'sys_getppid', 'sys_getpgrp', 'sys_setsid', 'sys_setreuid', 'sys_setregid', 'sys_getgroups',
        'sys_setgroups', 'sys_setresuid', 'sys_getresuid', 'sys_setresgid', 'sys_getresgid', 'sys_getpgid', 'sys_setfsuid',
        'sys_setfsgid', 'sys_getsid', 'sys_capget', 'sys_capset', 'sys_rt_sigpending', 'sys_rt_sigtimedwait',
        'sys_rt_sigqueueinfo', 'sys_rt_sigsuspend', 'sys_sigaltstack', 'sys_utime', 'sys_mknod', 'sys_uselib',
        'sys_personality', 'sys_ustat', 'sys_statfs', 'sys_fstatfs', 'sys_sysfs', 'sys_getpriority', 'sys_setpriority',
        'sys_sched_setparam', 'sys_sched_getparam', 'sys_sched_setscheduler', 'sys_sched_getscheduler',
        'sys_sched_get_priority_max', 'sys_sched_get_priority_min', 'sys_sched_rr_get_interval', 'sys_mlock',
        'sys_munlock', 'sys_mlockall', 'sys_munlockall', 'sys_vhangup', 'sys_modify_ldt', 'sys_pivot_root',
        'sys__sysctl', 'sys_prctl', 'sys_arch_prctl', 'sys_adjtimex', 'sys_setrlimit', 'sys_chroot', 'sys_sync',
        'sys_acct', 'sys_settimeofday', 'sys_mount', 'sys_umount2', 'sys_swapon', 'sys_swapoff', 'sys_reboot',
        'sys_sethostname', 'sys_setdomainname', 'sys_iopl', 'sys_ioperm', 'sys_create_module', 'sys_init_module',
        'sys_delete_module', 'sys_get_kernel_syms', 'sys_query_module', 'sys_quotactl', 'sys_nfsservctl', 'sys_getpmsg',
        'sys_putpmsg', 'sys_afs_syscall', 'sys_tuxcall', 'sys_security', 'sys_gettid', 'sys_readahead', 'sys_setxattr',
        'sys_lsetxattr', 'sys_fsetxattr', 'sys_getxattr', 'sys_lgetxattr', 'sys_fgetxattr', 'sys_listxattr',
        'sys_llistxattr', 'sys_flistxattr', 'sys_removexattr', 'sys_lremovexattr', 'sys_fremovexattr', 'sys_tkill',
        'sys_time', 'sys_futex', 'sys_sched_setaffinity', 'sys_sched_getaffinity', 'sys_set_thread_area', 'sys_io_setup',
        'sys_io_destroy', 'sys_io_getevents', 'sys_io_submit', 'sys_io_cancel', 'sys_get_thread_area', 'sys_lookup_dcookie',
        'sys_epoll_create', 'sys_epoll_ctl_old', 'sys_epoll_wait_old', 'sys_remap_file_pages', 'sys_getdents64',
        'sys_set_tid_address', 'sys_restart_syscall', 'sys_semtimedop', 'sys_fadvise64', 'sys_timer_create',
        'sys_timer_settime', 'sys_timer_gettime', 'sys_timer_getoverrun', 'sys_timer_delete', 'sys_clock_settime',
        'sys_clock_gettime', 'sys_clock_getres', 'sys_clock_nanosleep', 'sys_exit_group', 'sys_epoll_wait',
        'sys_epoll_ctl', 'sys_tgkill', 'sys_utimes', 'sys_vserver', 'sys_mbind', 'sys_set_mempolicy', 'sys_get_mempolicy',
        'sys_mq_open', 'sys_mq_unlink', 'sys_mq_timedsend', 'sys_mq_timedreceive', 'sys_mq_notify', 'sys_mq_getsetattr',
        'sys_kexec_load', 'sys_waitid', 'sys_add_key', 'sys_request_key', 'sys_keyctl', 'sys_ioprio_set', 'sys_ioprio_get',
        'sys_inotify_init', 'sys_inotify_add_watch', 'sys_inotify_rm_watch', 'sys_migrate_pages', 'sys_openat',
        'sys_mkdirat', 'sys_mknodat', 'sys_fchownat', 'sys_futimesat', 'sys_newfstatat', 'sys_unlinkat', 'sys_renameat',
        'sys_linkat', 'sys_symlinkat', 'sys_readlinkat', 'sys_fchmodat', 'sys_faccessat', 'sys_pselect6', 'sys_ppoll',
        'sys_unshare', 'sys_set_robust_list', 'sys_get_robust_list', 'sys_splice', 'sys_tee', 'sys_sync_file_range',
        'sys_vmsplice', 'sys_move_pages', 'sys_utimensat', 'sys_epoll_pwait', 'sys_signalfd', 'sys_timerfd_create',
        'sys_eventfd', 'sys_fallocate', 'sys_timerfd_settime', 'sys_timerfd_gettime', 'sys_accept4', 'sys_signalfd4',
        'sys_eventfd2', 'sys_epoll_create1', 'sys_dup3', 'sys_pipe2', 'sys_inotify_init1', 'sys_preadv', 'sys_pwritev',
        'sys_rt_tgsigqueueinfo', 'sys_perf_event_open', 'sys_recvmmsg', 'sys_fanotify_init', 'sys_fanotify_mark',
        'sys_prlimit64', 'sys_name_to_handle_at', 'sys_open_by_handle_at', 'sys_clock_adjtime', 'sys_syncfs',
        'sys_sendmmsg', 'sys_setns', 'sys_getcpu', 'sys_process_vm_readv', 'sys_process_vm_writev', 'sys_kcmp',
        'sys_finit_module', 'sys_sched_setattr', 'sys_sched_getattr', 'sys_renameat2', 'sys_seccomp', 'sys_getrandom',
        'sys_memfd_create', 'sys_kexec_file_load', 'sys_bpf', 'sys_execveat', 'sys_userfaultfd', 'sys_membarrier',
        'sys_mlock2', 'sys_copy_file_range'
        ]

    # Set default syscall table to arm #
    sysList = sysList_arm

    # Define signal #
    sigList = [
        'SIGHUP', 'SIGINT', 'SIGQUIT', 'SIGILL', 'SIGTRAP', 'SIGABRT', 'SIGBUS', 'SIGFPE', 'SIGKILL', #9#
        'SIGUSR1', 'SIGSEGV', 'SIGUSR2', 'SIGPIPE', 'SIGALRM', 'SIGTERM', 'SIGSTKFLT', 'SIGCHLD', 'SIGCONT', #18#
        'SIGSTOP', 'SIGTSTP', 'SIGTTIN', 'SIGTTOU', 'SIGURG', 'SIGXCPU', 'SIGXFSZ', 'SIGVTALRM', 'SIGPROF', #27#
        'SIGWINCH', 'SIGIO', 'SIGPWR', 'SIGSYS' #31#
        ] + [ 'SIGRT%d' % idx for idx in xrange(0, 32, 1)]

    # stat list from http://linux.die.net/man/5/proc #
    statList = [
        'PID', 'COMM', 'STATE', 'PPID', 'PGRP', 'SESSIONID', 'NRTTY', 'TPGID', 'FLAGS', 'MINFLT', 'CMINFLT', #10#
        'MAJFLT', 'CMAJFLT', 'UTIME', 'STIME', 'CUTIME', 'CSTIME', 'PRIORITY', 'NICE', 'NRTHREAD', 'ITERALVAL', #20#
        'STARTTIME', 'VSIZE', 'RSS', 'RSSLIM', 'STARTCODE', 'ENDCODE', 'STARTSTACK', 'SP', 'PC', 'SIGNAL', #30#
        'BLOCKED', 'SIGIGNORE', 'SIGCATCH', 'WCHEN', 'NSWAP', 'CNSWAP', 'EXITSIGNAL', 'PROCESSOR', 'RTPRIORITY', #39#
        'POLICY', 'DELAYBLKTICK', 'GUESTTIME', 'CGUESTTIME' # 43 #
        ]

    schedList = [
        'C', # 0: CFS #
        'F', # 1: FIFO #
        'R', # 2: RR #
        'B', # 3: BATCH #
        'N', # 4: NONE #
        'I', # 5: IDLE #
        ]

    # Define statm of process #
    statmList = [
        'TOTAL',    # 0 #
        'RSS',      # 1 #
        'SHR',      # 2 #
        'TEXT',     # 3 #
        'DATA',     # 4 #
        'LIB',      # 5 #
        'DIRTY',    # 6 #
        ]

    taskChainEnable = None



    @staticmethod
    def readProcData(tid, path, num):
        path = '/proc/%s/%s' % (tid, path)

        try:
            f = open(path, 'r')
        except:
            SystemManager.printError("Fail to open %s" % path)
            return None

        if num == 0:
            return f.readline().replace('\n', '')
        else:
            return f.readline().replace('\n', '').split(' ')[num - 1]



    @staticmethod
    def getMmapId():
        if SystemManager.arch == 'arm':
            return ConfigManager.sysList.index('sys_mmap2')
        else:
            return ConfigManager.sysList.index('sys_mmap')



    @staticmethod
    def openConfFile(path):
        path += '.tc'
        if os.path.isfile(path):
            SystemManager.printWarning(\
                "%s already exists so that make new one" % path)

        try:
            fd = open(path, 'w')
        except:
            SystemManager.printError("Fail to open %s" % path)
            return None

        return fd




    @staticmethod
    def writeConfData(fd, line):
        if fd == None:
            SystemManager.printError("Fail to get file descriptor")
            return None

        fd.write(line)



    def __init__(self, mode):
        pass



    def __del__(self):
        pass



class NetworkManager(object):
    """ Manager for remote communication """

    def __init__(self, mode, ip, port):
        self.ip = None
        self.port = None
        self.socket = None
        self.request = None
        self.status = None
        self.ignore = 0

        try:
            from socket import socket, AF_INET, SOCK_DGRAM
        except ImportError:
            err = sys.exc_info()[1]
            print("[Error] Fail to import package: " + err.args[0])
            sys.exit(0)

        if mode is 'server':
            try:
                if ip is None:
                    self.ip = '0.0.0.0'
                else:
                    self.ip = ip

                self.port = port
                self.socket = socket(AF_INET, SOCK_DGRAM)
                self.socket.bind((self.ip, self.port))
                self.socket.setblocking(0)
            except:
                self.ip = None
                self.port = None
                SystemManager.printError("Fail to create socket as server")
                return None

        elif mode is 'client':
            try:
                self.ip = ip
                self.port = port
                self.socket = socket(AF_INET, SOCK_DGRAM)
            except:
                self.ip = None
                self.port = None
                SystemManager.printError("Fail to create socket as client")
                return None



    def send(self, message):
        if self.ip is None or self.port is None:
            SystemManager.printError("Fail to use IP address for client because it is not set")
            return False
        elif self.socket is None:
            SystemManager.printError("Fail to use socket for client because it is not set")
            return False

        try:
            if SystemManager.addrAsServer is not None:
                SystemManager.addrAsServer.socket.sendto(message, (self.ip, self.port))
            else:
                self.socket.sendto(message, (self.ip, self.port))

            if self.status is not 'ALWAYS':
                self.status = 'SENT'
            return True
        except:
            err = sys.exc_info()[1]
            SystemManager.printError(\
                ("Fail to send data to %s:%d as server, " % (self.ip, self.port)) + str(err.args))
            return False



    def sendto(self, message, ip, port):
        if ip is None or port is None:
            SystemManager.printError("Fail to use IP address for client because it is not set")
            return False
        elif self.socket is None:
            SystemManager.printError("Fail to use socket for client because it is not set")
            return False

        try:
            self.socket.sendto(message, (ip, port))
            return True
        except:
            err = sys.exc_info()[1]
            SystemManager.printError(\
                ("Fail to send data to %s:%d as client, " % (ip, port)) + str(err.args))
            return False



    def recv(self):
        if self.ip is None or self.port is None:
            SystemManager.printError("Fail to use IP address for server because it is not set")
            return False
        elif self.socket is None:
            SystemManager.printError("Fail to use socket for client because it is not set")
            return False

        try:
            message, address = self.socket.recvfrom(4096)
            return (message, address)
        except:
            return None



    def __del__(self):
        pass





class PageAnalyzer(object):
    """ Analyzer for kernel page """

    # page flags from kernel/include/uapi/linux/kernel-page-flags.h #
    flagList = [
            'KPF_LOCKED', #0#
            'KPF_ERROR', #1#
            'KPF_REFERENCED', #2#
            'KPF_UPTODATE', #3#
            'KPF_DIRTY', #4#
            'KPF_LRU', #5#
            'KPF_ACTIVE', #6#
            'KPF_SLAB', #7#
            'KPF_WRITEBACK', #8#
            'KPF_RECLAIM', #9#
            'KPF_BUDDY', #10#
            'KPF_MMAP', #11#
            'KPF_ANON', #12#
            'KPF_SWAPCACHE', #13#
            'KPF_SWAPBACKED', #14#
            'KPF_COMPOUND_HEAD', #15#
            'KPF_COMPOUND_TAIL', #16#
            'KPF_HUGE', #17#
            'KPF_UNEVICTABLE', #18#
            'KPF_HWPOISON', #19#
            'KPF_NOPAGE', #20#
            'KPF_KSM', #21#
            'KPF_THP', #22#
            'KPF_BALLOON', #23#
            'KPF_ZERO_PAGE', #24#
            'KPF_IDLE' #25#
            ]



    @staticmethod
    def getPageInfo(pid, vaddr):
        if os.geteuid() != 0:
            SystemManager.printError("Fail to get root permission")
            sys.exit(0)
        elif pid is False or vaddr is False:
            SystemManager.printError(\
                "Fail to recognize input, input pid with -g option and address with -I option")
            sys.exit(0)

        vrange = vaddr.split('-')
        rangeCnt = len(vrange)
        pageSize = os.sysconf("SC_PAGE_SIZE")

        if rangeCnt > 2:
            SystemManager.printError(\
                "Fail to recognize address, input address such as 0x1234 or 0x1234-0x4444")
            os._exit(0)
        else:
            try:
                if vrange[0].startswith("0x"):
                    addrType = 'hex'
                    addrs = long(vrange[0], base=16)
                    addre = addrs
                else:
                    addrType = 'dec'
                    addrs = long(vrange[0])
                    addre = addrs
            except:
                SystemManager.printError(\
                    "Fail to recognize address, input address such as 0xabcd or 78901234")
                os._exit(0)

            try:
                if rangeCnt == 2:
                    if vrange[1].startswith("0x"):
                        addrType = 'hex'
                        addre = long(vrange[1], base=16)
                    else:
                        addrType = 'dec'
                        addre = long(vrange[1])

                    offset = 0
                else:
                    offset = pageSize

                if addrs > addre:
                    SystemManager.printError(\
                        "Fail to recognize address, input bigger second address than first address")
                    os._exit(0)
            except:
                SystemManager.printError(\
                    "Fail to recognize address, input address such as 0x1234-0x4444")
                os._exit(0)

        print("\n[ PID: %s ] [ AREA: %s ] [ HELP: %s ]\n%s" % \
            (pid, vaddr, "kernel/Documentation/vm/pagemap.txt", twoLine))

        PageAnalyzer.printMemoryArea(pid, addrs, addre)
        print(twoLine)

        print("{0:^16}|{1:^16}|{2:^9}|{3:^6}|{4:^6}|{5:^5}|{6:^8}|{7:^7}| {8}({9})\n{10}".format(\
            "VADDR", "PFN", "PRESENT", "SWAP", "FILE", "REF",\
            "SDIRTY", "EXMAP", "FLAG", "FLAGS", oneLine))

        for addr in xrange(addrs, addre + offset, pageSize):
            entry = PageAnalyzer.get_pagemap_entry(pid, addr)

            pfn = PageAnalyzer.get_pfn(entry)

            isPresent = PageAnalyzer.is_present(entry)

            isSwapped = PageAnalyzer.is_swapped(entry)

            isSoftdirty = PageAnalyzer.is_softdirty(entry)

            isExmapped = PageAnalyzer.is_exmapped(entry)

            isFile = PageAnalyzer.is_file_page(entry)

            bflags = hex(PageAnalyzer.get_page_flags(pfn)).rstrip('L')

            sflags = PageAnalyzer.getFlagTypes(bflags)

            print("{0:^16}|{1:^16}|{2:^9}|{3:^6}|{4:^6}|{5:^5}|{6:^8}|{7:^7}| {8}({9} )".format(\
                hex(addr), hex(pfn).rstrip('L'), isPresent, isSwapped, isFile,\
                PageAnalyzer.get_pagecount(pfn), isSoftdirty, isExmapped, bflags, sflags)
            )
        print("%s\n" % oneLine)



    @staticmethod
    def printMemoryArea(pid, start, end):
        count = 0
        switch = 0
        fpath = '/proc/%s/maps' % pid

        try:
            with open(fpath, 'r') as fd:
                buf = fd.readlines()
        except:
            SystemManager.printError('Fail to open %s' % fpath)
            os._exit(0)

        start = hex(start).rstrip('L')
        end = hex(end).rstrip('L')

        # print menu #
        menuStr = ''
        menuList = ['AREA', 'PERM', 'INODE', 'DEV', 'OFFSET']
        menuBuf = str(buf[0]).split()
        for idx, value in enumerate(menuBuf):
            if idx < 5:
                text = menuList[idx]
            else:
                break

            value = ' ' * (len(value) - len(text) + 1)
            menuStr = '%s%s' % (menuStr, text + value)
        print('%s\t%s\n%s' % (menuStr, 'PROPERTY', oneLine))

        # print maps info #
        for line in buf:
            if line.find('-') >= 0:
                tmplist = line.split()

                soffset, eoffset = tmplist[0].split('-')

                soffset = hex(long(soffset, base=16)).rstrip('L')
                eoffset = hex(long(eoffset, base=16)).rstrip('L')

                if (start >= soffset and start < eoffset):
                    switch = 1
                elif switch == 0:
                    continue
                elif end < eoffset:
                    break

                print(line[:-1])
                count += 1

                if switch == 1 and end <= eoffset:
                    break

        if count == 0:
            print('No involved memory area')



    @staticmethod
    def getFlagTypes(flags):
        sflags = ' '

        for idx, val in enumerate(PageAnalyzer.flagList):
            if ((int(flags, 16) & (1 << int(idx))) != 0):
                sflags = "%s%s|" % (sflags, val[4:])

        return sflags[:-1]



    @staticmethod
    def read_entry(path, offset, size=8):
        with open(path, 'r') as f:
            f.seek(offset, 0)
            return struct.unpack('Q', f.read(size))[0]



    @staticmethod
    def get_pagemap_entry(pid, addr):
        maps_path = "/proc/{0}/pagemap".format(pid)
        if not os.path.isfile(maps_path):
            SystemManager.printError("Fail to find %s process" % pid)
            os._exit(0)

        page_size = os.sysconf("SC_PAGE_SIZE")
        pagemap_entry_size = 8
        offset  = (addr / page_size) * pagemap_entry_size

        return PageAnalyzer.read_entry(maps_path, offset)



    @staticmethod
    def get_pfn(entry):
        return entry & 0x7FFFFFFFFFFFFF



    @staticmethod
    def is_present(entry):
        return ((entry & (1 << 63)) != 0)



    @staticmethod
    def is_softdirty(entry):
        return ((entry & (1 << 55)) != 0)



    @staticmethod
    def is_exmapped(entry):
        return ((entry & (1 << 56)) != 0)



    @staticmethod
    def is_swapped(entry):
        return ((entry & (1 << 62)) != 0)



    @staticmethod
    def is_file_page(entry):
        return ((entry & (1 << 61)) != 0)



    @staticmethod
    def get_pagecount(pfn):
        file_path = "/proc/kpagecount"
        offset = pfn * 8
        return PageAnalyzer.read_entry(file_path, offset)



    @staticmethod
    def get_page_flags(pfn):
        file_path = "/proc/kpageflags"
        offset = pfn * 8
        return PageAnalyzer.read_entry(file_path, offset)





class FunctionAnalyzer(object):
    """ Analyzer for function profiling """

    symStackIdxTable = [
        'CPU_TICK', 'STACK', 'PAGE_ALLOC', 'PAGE_FREE', 'BLK_READ', \
        'ARGUMENT', 'HEAP_EXPAND', 'HEAP_REDUCE', 'IGNORE', 'BLK_WRITE', 'CUSTOM'
        ]



    def __init__(self, logFile):
        self.cpuEnabled = False
        self.memEnabled = False
        self.heapEnabled = False
        self.breadEnabled = False
        self.bwriteEnabled = False
        self.sigEnabled = False

        self.sort = 'sym'

        self.startTime = '0'
        self.finishTime = '0'
        self.totalTime = 0
        self.totalTick = 0
        self.prevTime = '0'
        self.prevTid = '0'

        self.lastCore = None
        self.coreCtx = {}
        self.nowCtx = None
        self.nowEvent = None
        self.savedEvent = None
        self.nestedEvent = None
        self.nowCnt = 0
        self.savedCnt = 0
        self.nestedCnt = 0
        self.nowArg = 0
        self.savedArg = 0
        self.nestedArg = 0

        self.duplicatedPos = 0
        self.periodicEventCnt = 0
        self.periodicContEventCnt = 0
        self.periodicEventInterval = 0
        self.heapExpEventCnt = 0
        self.heapExpSize = 0
        self.heapRedEventCnt = 0
        self.heapRedSize = 0
        self.pageAllocEventCnt = 0
        self.pageAllocCnt = 0
        self.pageFreeEventCnt = 0
        self.pageFreeCnt = 0
        self.pageUnknownFreeCnt = 0
        self.pageUsageCnt = 0
        self.blockRdEventCnt = 0
        self.blockRdUsageCnt = 0
        self.blockWrEventCnt = 0
        self.blockWrUsageCnt = 0
        self.customCnt = 0
        self.customTotal = 0

        self.customEventTable = {}
        self.ignoreTable = {}
        self.mapData = []
        self.pageTable = {}
        self.oldPageTable = {}
        self.heapTable = {}
        self.oldHeapTable = {}
        self.posData = {}
        self.userSymData = {}
        self.kernelSymData = {}
        self.threadData = {}
        self.customCallData = []
        self.userCallData = []
        self.kernelCallData = []
        '''
        userCallData = kernelCallData = [pos, stack, event, eventCnt, eventArg]
        '''

        self.init_threadData = \
            {'comm': '', 'tgid': '-'*5, 'target': False, 'cpuTick': int(0), \
            'die': False, 'new': False, 'nrPages': int(0), 'userPages': int(0), \
            'cachePages': int(0), 'kernelPages': int(0), 'heapSize': int(0), \
            'eventCnt': int(0), 'nrWrBlocks': int(0), 'nrUnknownFreePages': int(0), \
            'customCnt': int(0), 'nrRdBlocks': int(0), 'customTotal': int(0)}

        self.init_posData = \
            {'symbol': '', 'binary': '', 'origBin': '', 'offset': hex(0), 'posCnt': int(0), \
            'userPageCnt': int(0), 'cachePageCnt': int(0), 'kernelPageCnt': int(0), \
            'totalCnt': int(0), 'blockRdCnt': int(0), 'blockWrCnt': int(0), 'pageCnt': int(0), \
            'heapSize': int(0), 'unknownPageFreeCnt': int(0), 'src': '', 'customCnt': int(0), \
            'customTotal': int(0)}

        self.init_symData = \
            {'pos': '', 'origBin': '', 'tickCnt': int(0), 'blockRdCnt': int(0), \
            'pageCnt': int(0), 'unknownPageFreeCnt': int(0), 'stack': None, 'symStack': None, \
            'userPageCnt': int(0), 'cachePageCnt': int(0), 'kernelPageCnt': int(0), \
            'heapSize': int(0), 'blockWrCnt': int(0), 'customCnt': int(0), 'customTotal': int(0)}

        self.init_ctxData = \
            {'nestedEvent': None, 'savedEvent': None, 'nowEvent': None, 'nested': int(0), \
            'recStat': bool(False), 'nestedCnt': int(0), 'savedCnt': int(0), 'nowCnt': int(0), \
            'nestedArg': None, 'savedArg': None, 'prevMode': None, 'curMode': None, \
            'userLastPos': '', 'userCallStack': None, 'kernelLastPos': '', 'kernelCallStack': None, \
            'bakKernelLastPos': '', 'bakKernelCallStack': None, 'nowArg': None, \
            'prevTid': None, 'prevTime': None}

        self.init_pageLinkData = \
            {'sym': '0', 'subStackAddr': int(0), 'kernelSym': '0', 'kernelSubStackAddr': int(0), \
            'type': '0', 'time': '0'}

        self.init_heapSegData = {'tid': '0', 'size': int(0), 'sym': '0', 'subStackAddr': int(0), \
            'kernelSym': '0', 'kernelSubStackAddr': int(0)}

        self.init_pageData = {'tid': '0', 'page': '0', 'flags': '0', 'type': '0', 'time': '0'}

        self.init_subStackPageInfo = [0, 0, 0]
        # subStackPageInfo = [userPageCnt, cachePageCnt, kernelPageCnt]

        # Open log file #
        try:
            logFd = open(logFile, 'r')
        except:
            SystemManager.printError("Fail to open %s to create callstack information" % logFile)
            sys.exit(0)

        SystemManager.printStatus('start analyzing data... [ STOP(ctrl + c) ]')

        # Get binary and offset info #
        lines = logFd.readlines()

        # Save data and quit #
        SystemManager.saveAndQuit(lines)

        # Check target thread setting #
        if len(SystemManager.showGroup) == 0:
            SystemManager.showGroup.insert(0, '')
            self.target = []
        else:
            for tid in SystemManager.showGroup:
                try:
                    int(tid)
                except:
                    SystemManager.printError(\
                        "Fail to use filter value %s, use -g option with number as thread id" % tid)
                    sys.exit(0)
            self.target = SystemManager.showGroup

        # Check root path #
        if SystemManager.rootPath is None and SystemManager.userEnable:
            SystemManager.printError(\
                "Fail to recognize sysroot path of target for user mode, use also -r option")
            sys.exit(0)

        # Register None pos #
        self.posData['0'] = dict(self.init_posData)

        # get and remove process tree from data file #
        SystemManager.getProcTreeInfo()

        # Parse logs #
        SystemManager.totalLine = len(lines)
        self.parseLogs(lines, SystemManager.showGroup)

        # Check whether data of target thread is collected or nothing #
        if len(self.userCallData) == 0 and \
            len(self.kernelCallData) == 0 and \
            len(self.target) > 0:
            SystemManager.printError("No collected data related to %s" % self.target)
            sys.exit(0)
        elif SystemManager.userEnable and \
            len(self.userCallData) == 1 and \
            self.userCallData[0][0] == '0':
            SystemManager.printError("No user stack data related to %s, " % self.target + \
                "enable CONFIG_USER_STACKTRACE_SUPPORT option in kernel")
            sys.exit(0)

        # Get symbols from call address #
        SystemManager.printStatus('start resolving symbols... [ STOP(ctrl + c) ]')
        self.getSymbols()

        # Merge callstacks by symbol and address #
        SystemManager.printStatus('start summarizing functions... [ STOP(ctrl + c) ]')
        self.mergeStacks()



    def __del__(self):
        pass



    def handleHeapExpand(self, sym, kernelSym, stackAddr, kernelStackAddr, size, addr):
        self.userSymData[sym]['heapSize'] += size
        self.kernelSymData[kernelSym]['heapSize'] += size

        try:
            self.heapTable[addr]['size'] = size
        except:
            self.heapTable[addr] = dict(self.init_heapSegData)
            self.heapTable[addr]['size'] = size

        self.heapTable[addr]['sym'] = sym
        self.heapTable[addr]['kernelSym'] = kernelSym
        self.heapTable[addr]['subStackAddr'] = stackAddr
        self.heapTable[addr]['kernelSubStackAddr'] = kernelStackAddr

        # Set user target stack #
        if self.sort is 'sym':
            targetStack = self.userSymData[sym]['symStack']
        elif self.sort is 'pos':
            targetStack = self.userSymData[sym]['stack']



    def handleHeapReduce(self, size, addr):
        subStackIndex = FunctionAnalyzer.symStackIdxTable.index('STACK')
        heapExpIndex = FunctionAnalyzer.symStackIdxTable.index('HEAP_EXPAND')

        try:
            sym = self.heapTable[addr]['sym']
            kernelSym = self.heapTable[addr]['kernelSym']
            stackAddr = self.heapTable[addr]['subStackAddr']
            kernelStackAddr= self.heapTable[addr]['kernelSubStackAddr']

            self.userSymData[sym]['heapSize'] -= size
            self.kernelSymData[kernelSym]['heapSize'] -= size
        except:
            SystemManager.printWarning("Fail to find heap segment to be freed")
            return

        # Set user target stack #
        if self.sort is 'sym':
            targetStack = self.userSymData[sym]['symStack']
        elif self.sort is 'pos':
            targetStack = self.userSymData[sym]['stack']

        # Find subStack of symbol allocated this segment #
        for val in targetStack:
            if id(val[subStackIndex]) == stackAddr:
                # Increase heap count of subStack #
                val[heapExpIndex] -= size
                break

        # Set kernel target stack #
        kernelTargetStack = self.kernelSymData[kernelSym]['stack']

        # Find subStack of symbol allocated this segment #
        for val in kernelTargetStack:
            if id(val[subStackIndex]) == kernelStackAddr:
                # Increase heap count of subStack #
                val[heapExpIndex] -= size
                break

        del self.heapTable[addr]
        self.heapTable[addr] = {}



    def handlePageFree(\
        self, sym, kernelSym, stackAddr, kernelStackAddr, pageFreeCnt, pageType, pfn):

        subStackIndex = FunctionAnalyzer.symStackIdxTable.index('STACK')
        pageAllocIndex = FunctionAnalyzer.symStackIdxTable.index('PAGE_ALLOC')
        pageFreeIndex = FunctionAnalyzer.symStackIdxTable.index('PAGE_FREE')
        argIndex = FunctionAnalyzer.symStackIdxTable.index('ARGUMENT')

        for cnt in xrange(0, pageFreeCnt):
            pfnv = pfn + cnt
            subStackPageInfoIdx = 0

            try:
                # Decrease page count of symbol allocated page  #
                # toDo: fix bug about wrong count of pos #
                allocSym = self.pageTable[pfnv]['sym']
                allocStackAddr = self.pageTable[pfnv]['subStackAddr']
                allocKernelSym = self.pageTable[pfnv]['kernelSym']
                allocKernelStackAddr = self.pageTable[pfnv]['kernelSubStackAddr']


                self.pageUsageCnt -= 1
                self.userSymData[allocSym]['pageCnt'] -= 1
                self.kernelSymData[allocKernelSym]['pageCnt'] -= 1

                if pageType is 'USER':
                    self.userSymData[allocSym]['userPageCnt'] -= 1
                    self.kernelSymData[allocKernelSym]['userPageCnt'] -= 1
                    subStackPageInfoIdx = 0
                elif pageType is 'CACHE':
                    self.userSymData[allocSym]['cachePageCnt'] -= 1
                    self.kernelSymData[allocKernelSym]['cachePageCnt'] -= 1
                    subStackPageInfoIdx = 1
                elif pageType is 'KERNEL':
                    self.userSymData[allocSym]['kernelPageCnt'] -= 1
                    self.kernelSymData[allocKernelSym]['kernelPageCnt'] -= 1
                    subStackPageInfoIdx = 2

                # Set user target stack #
                if self.sort is 'sym':
                    targetStack = self.userSymData[allocSym]['symStack']
                elif self.sort is 'pos':
                    targetStack = self.userSymData[allocSym]['stack']

                # Find subStack allocated this page #
                for val in targetStack:
                    if id(val[subStackIndex]) == allocStackAddr:
                        val[pageAllocIndex] -= 1
                        val[argIndex][subStackPageInfoIdx] -= 1
                        break

                # Set kernel target stack #
                kernelTargetStack = self.kernelSymData[allocKernelSym]['stack']

                # Find subStack allocated this page #
                for val in kernelTargetStack:
                    if id(val[subStackIndex]) == allocKernelStackAddr:
                        val[pageAllocIndex] -= 1
                        val[argIndex][subStackPageInfoIdx] -= 1
                        break

                del self.pageTable[pfnv]
                self.pageTable[pfnv] = None
            except:
                # this page is allocated before starting profile #

                self.pageUnknownFreeCnt += 1
                self.userSymData[sym]['unknownPageFreeCnt'] += 1
                self.kernelSymData[kernelSym]['unknownPageFreeCnt'] += 1

                # Set user target stack #
                if self.sort is 'sym':
                    targetStack = self.userSymData[sym]['symStack']
                elif self.sort is 'pos':
                    targetStack = self.userSymData[sym]['stack']

                # Find subStack allocated this page #
                for val in targetStack:
                    if id(val[subStackIndex]) == stackAddr:
                        val[pageFreeIndex] += 1
                        break

                # Set kernel target stack #
                kernelTargetStack = self.kernelSymData[kernelSym]['stack']

                # Find subStack allocated this page #
                for val in kernelTargetStack:
                    if id(val[subStackIndex]) == kernelStackAddr:
                        val[pageFreeIndex] += 1
                        break

                continue



    def handlePageAlloc(\
        self, sym, kernelSym, stackAddr, kernelStackAddr, pageAllocCnt, pageType, pfn):

        subStackPageInfoIdx = 0

        subStackIndex = FunctionAnalyzer.symStackIdxTable.index('STACK')
        pageAllocIndex = FunctionAnalyzer.symStackIdxTable.index('PAGE_ALLOC')
        argIndex = FunctionAnalyzer.symStackIdxTable.index('ARGUMENT')

        # Increase counts of page to be allocated #
        self.userSymData[sym]['pageCnt'] += pageAllocCnt
        self.kernelSymData[kernelSym]['pageCnt'] += pageAllocCnt

        if pageType == 'USER':
            self.userSymData[sym]['userPageCnt'] += pageAllocCnt
            self.kernelSymData[kernelSym]['userPageCnt'] += pageAllocCnt
            subStackPageInfoIdx = 0
        elif pageType == 'CACHE':
            self.userSymData[sym]['cachePageCnt'] += pageAllocCnt
            self.kernelSymData[kernelSym]['cachePageCnt'] += pageAllocCnt
            subStackPageInfoIdx = 1
        elif pageType == 'KERNEL':
            self.userSymData[sym]['kernelPageCnt'] += pageAllocCnt
            self.kernelSymData[kernelSym]['kernelPageCnt'] += pageAllocCnt
            subStackPageInfoIdx = 2

        # Set user target stack #
        if self.sort is 'sym':
            targetStack = self.userSymData[sym]['symStack']
        elif self.sort is 'pos':
            targetStack = self.userSymData[sym]['stack']

        # Find subStack of symbol allocated this page #
        for val in targetStack:
            if id(val[subStackIndex]) == stackAddr:
                # Increase page count of subStack #
                val[argIndex][subStackPageInfoIdx] += pageAllocCnt
                break

        # Set kernel target stack #
        kernelTargetStack = self.kernelSymData[kernelSym]['stack']

        # Find subStack of symbol allocated this page #
        for val in kernelTargetStack:
            if id(val[subStackIndex]) == kernelStackAddr:
                # Increase page count of subStack #
                val[argIndex][subStackPageInfoIdx] += pageAllocCnt
                break

        # Make PTE in page table #
        for cnt in xrange(0, pageAllocCnt):
            pfnv = pfn + cnt
            subStackPageInfoIdx = 0

            try:
                # Check whether this page is already allocated #
                allocSym = self.pageTable[pfnv]['sym']

                allocStackAddr = self.pageTable[pfnv]['subStackAddr']
                allocKernelSym = self.pageTable[pfnv]['kernelSym']
                allocKernelStackAddr = self.pageTable[pfnv]['kernelSubStackAddr']

                # Decrease counts of page already allocated but no free log #
                self.pageUsageCnt -= 1
                self.userSymData[allocSym]['pageCnt'] -= 1
                self.kernelSymData[allocKernelSym]['pageCnt'] -= 1

                origPageType = self.pageTable[pfnv]['type']
                if origPageType == 'USER':
                    self.userSymData[allocSym]['userPageCnt'] -= 1
                    self.kernelSymData[allocKernelSym]['userPageCnt'] -= 1
                    subStackPageInfoIdx = 0
                elif origPageType == 'CACHE':
                    self.userSymData[allocSym]['cachePageCnt'] -= 1
                    self.kernelSymData[allocKernelSym]['cachePageCnt'] -= 1
                    subStackPageInfoIdx = 1
                elif origPageType == 'KERNEL':
                    self.userSymData[allocSym]['kernelPageCnt'] -= 1
                    self.kernelSymData[allocKernelSym]['kernelPageCnt'] -= 1
                    subStackPageInfoIdx = 2

                # Set user target stack #
                if self.sort is 'sym':
                    targetStack = self.userSymData[allocSym]['symStack']
                elif self.sort is 'pos':
                    targetStack = self.userSymData[allocSym]['stack']

                # Find user subStack of symbol allocated this page #
                for val in targetStack:
                    if id(val[subStackIndex]) == allocStackAddr:
                        # Decrease allocated page count of substack #
                        val[pageAllocIndex] -= 1
                        val[argIndex][subStackPageInfoIdx] -= 1
                        break

                # Set kernel target stack #
                kernelTargetStack = self.kernelSymData[allocKernelSym]['stack']

                # Find user subStack of symbol allocated this page #
                for val in kernelTargetStack:
                    if id(val[subStackIndex]) == allocKernelStackAddr:
                        # Decrease allocated page count of substack #
                        val[pageAllocIndex] -= 1
                        val[argIndex][subStackPageInfoIdx] -= 1
                        break
            except:
                self.pageTable[pfnv] = dict(self.init_pageLinkData)

            self.pageTable[pfnv]['sym'] = sym
            self.pageTable[pfnv]['kernelSym'] = kernelSym
            self.pageTable[pfnv]['type'] = pageType
            self.pageTable[pfnv]['subStackAddr'] = stackAddr
            self.pageTable[pfnv]['kernelSubStackAddr'] = kernelStackAddr



    def mergeStacks(self):
        sym = ''
        kernelSym = ''
        stackAddr = 0
        kernelStackAddr = 0
        lineCnt = -1
        lastIdx = len(self.userCallData)

        # Backup page table used previously and Initialize it #
        self.oldPageTable = self.pageTable
        self.pageTable = {}

        # Backup heap table used previously and Initialize it #
        self.oldHeapTable = self.heapTable
        self.heapTable = {}

        subStackIndex = FunctionAnalyzer.symStackIdxTable.index('STACK')
        argIndex = FunctionAnalyzer.symStackIdxTable.index('ARGUMENT')

        # Merge call data by symbol or address #
        for val in self.userCallData:
            lineCnt += 1
            SystemManager.printProgress(lineCnt, lastIdx)

            pos = val[0]
            stack = val[1]
            event = val[2]
            eventCnt = val[3]
            arg = val[4]

            # Do not merge PAGE_FREE count because it will be merged with unknownPageFreeCnt #
            if event == 'PAGE_FREE':
                savedEventCnt = eventCnt
                eventCnt = 0

            try:
                eventIndex = FunctionAnalyzer.symStackIdxTable.index(event)
            except:
                eventIndex = FunctionAnalyzer.symStackIdxTable.index('IGNORE')

            kernelPos = self.kernelCallData[lineCnt][0]
            kernelStack = self.kernelCallData[lineCnt][1]
            subStackPageInfo = list(self.init_subStackPageInfo)

            targetStack = []
            kernelTargetStack = []

            # Resolve user symbol #
            try:
                # No symbol related to last pos #
                if self.posData[pos]['symbol'] == '':
                    self.posData[pos]['symbol'] = pos
                    sym = pos
                else:
                    sym = self.posData[pos]['symbol']
            except:
                continue

            # Resolve kernel symbol #
            try:
                # No symbol related to last pos #
                if self.posData[kernelPos]['symbol'] == '':
                    self.posData[kernelPos]['symbol'] = kernelPos
                    kernelSym = kernelPos
                else:
                    kernelSym = self.posData[kernelPos]['symbol']
            except:
                continue

            # Make user symbol table of last pos in stack #
            try:
                self.userSymData[sym]
            except:
                self.userSymData[sym] = dict(self.init_symData)
                self.userSymData[sym]['stack'] = []
                self.userSymData[sym]['symStack'] = []
                self.userSymData[sym]['pos'] = pos
                self.userSymData[sym]['origBin'] = self.posData[pos]['origBin']

            # Make kenel symbol table of last pos in stack #
            try:
                self.kernelSymData[kernelSym]
            except:
                self.kernelSymData[kernelSym] = dict(self.init_symData)
                self.kernelSymData[kernelSym]['stack'] = []
                self.kernelSymData[kernelSym]['pos'] = kernelPos

            # Set target user stack #
            if self.sort is 'sym':
                tempSymStack = []
                # Make temporary symbol stack to merge stacks by symbol #
                for addr in stack:
                    tempSym = self.posData[addr]['symbol']

                    # Ignore this function if there is no symbol #
                    if SystemManager.showAll is False and \
                        self.posData[addr]['origBin'] == '??' and \
                        (tempSym == addr or tempSym == self.posData[addr]['offset']):
                        continue

                    # No symbol data #
                    if tempSym == '':
                        if self.posData[addr]['origBin'] == '??':
                            tempSym = '%x' % long(self.posData[addr]['pos'], 16)
                        else:
                            tempSym = '%x' % long(self.posData[addr]['offset'], 16)

                    try:
                        self.userSymData[tempSym]
                    except:
                        self.userSymData[tempSym] = dict(self.init_symData)
                        self.userSymData[tempSym]['stack'] = []
                        self.userSymData[tempSym]['symStack'] = []
                        self.userSymData[tempSym]['pos'] = addr
                        self.userSymData[tempSym]['origBin'] = self.posData[addr]['origBin']

                    tempSymStack.append(tempSym)

                # Switch input stack to symbol stack #
                stack = tempSymStack
                targetStack = self.userSymData[sym]['symStack']
            elif self.sort is 'pos':
                targetStack = self.userSymData[sym]['stack']

            # First user stack related to this symbol #
            if len(targetStack) == 0:
                tempList = [0] * len(FunctionAnalyzer.symStackIdxTable)
                tempList[eventIndex] = eventCnt
                tempList[subStackIndex] = stack
                tempList[argIndex] = list(subStackPageInfo)
                targetStack.append(tempList)

                stackAddr = id(stack)
            else:
                found = False

                # Find same stack by pos in stack list #
                for stackInfo in targetStack:
                    # Found same stack #
                    if len(list(set(stack) - set(stackInfo[subStackIndex]))) == 0 and \
                        len(list(set(stackInfo[subStackIndex]) - set(stack))) == 0:
                        found = True

                        stackInfo[eventIndex] += eventCnt
                        stackAddr = id(stackInfo[subStackIndex])

                        break

                # New stack related to this symbol #
                if found == False:
                    tempList = [0] * len(FunctionAnalyzer.symStackIdxTable)
                    tempList[eventIndex] = eventCnt
                    tempList[subStackIndex] = stack
                    tempList[argIndex] = list(subStackPageInfo)
                    targetStack.append(tempList)

                    stackAddr = id(stack)

            # Set target kernel stack #
            kernelTargetStack = self.kernelSymData[kernelSym]['stack']

            # First stack related to this symbol #
            if len(kernelTargetStack) == 0:
                tempList = [0] * len(FunctionAnalyzer.symStackIdxTable)
                tempList[eventIndex] = eventCnt
                tempList[subStackIndex] = kernelStack
                tempList[argIndex] = list(subStackPageInfo)
                kernelTargetStack.append(tempList)

                kernelStackAddr = id(kernelStack)
            else:
                found = False
                for stackInfo in kernelTargetStack:
                    # Found same stack  in stack list #
                    if len(list(set(kernelStack) - set(stackInfo[subStackIndex]))) == 0 and \
                        len(list(set(stackInfo[subStackIndex]) - set(kernelStack))) == 0:
                        found = True
                        stackInfo[eventIndex] += eventCnt
                        kernelStackAddr = id(stackInfo[subStackIndex])
                        break

                # New stack related to this symbol #
                if found == False:
                    tempList = [0] * len(FunctionAnalyzer.symStackIdxTable)
                    tempList[eventIndex] = eventCnt
                    tempList[subStackIndex] = kernelStack
                    tempList[argIndex] = list(subStackPageInfo)
                    kernelTargetStack.append(tempList)

                    kernelStackAddr = id(kernelStack)

            # Recover PAGE_FREE count to merge with unknownPageFreeCnt #
            if event == 'PAGE_FREE':
                eventCnt = savedEventCnt

            # memory allocation event #
            if event == 'PAGE_ALLOC':
                pageType = arg[0]
                pfn = arg[1]

                self.handlePageAlloc(\
                    sym, kernelSym, stackAddr, kernelStackAddr, eventCnt, pageType, pfn)

            # memory free event #
            elif event == 'PAGE_FREE':
                pageType = arg[0]
                pfn = arg[1]

                self.handlePageFree(\
                    sym, kernelSym, stackAddr, kernelStackAddr, eventCnt, pageType, pfn)

            # heap expand event #
            elif event == 'HEAP_EXPAND':
                addr = arg

                self.handleHeapExpand(sym, kernelSym, stackAddr, kernelStackAddr, eventCnt, addr)

            # heap expand event #
            elif event == 'HEAP_REDUCE':
                addr = arg

                self.handleHeapReduce(eventCnt, addr)

            # block read event #
            elif event == 'BLK_READ':
                self.userSymData[sym]['blockRdCnt'] += eventCnt
                self.kernelSymData[kernelSym]['blockRdCnt'] += eventCnt

            # block write event #
            elif event == 'BLK_WRITE':
                self.userSymData[sym]['blockWrCnt'] += eventCnt
                self.kernelSymData[kernelSym]['blockWrCnt'] += eventCnt

            # periodic event such as cpu tick #
            elif event == 'CPU_TICK':
                self.userSymData[sym]['tickCnt'] += 1
                self.kernelSymData[kernelSym]['tickCnt'] += 1

            # periodic event such as cpu tick #
            elif event == 'CUSTOM':
                if eventCnt > 0:
                    self.userSymData[sym]['customTotal'] += 1
                    self.kernelSymData[kernelSym]['customTotal'] += 1

                self.userSymData[sym]['customCnt'] += eventCnt
                self.kernelSymData[kernelSym]['customCnt'] += eventCnt

            # etc event #
            elif event is 'IGNORE':
                try:
                    self.ignoreTable[arg]['ignCnt'] += 1
                except:
                    self.ignoreTable[arg] = {'ignCnt': int(1)}

            else:
                SystemManager.printWarning("Fail to recognize event %s" % event)

        # Print summary about ignored events #
        self.printIgnoreEvents()



    def printIgnoreEvents(self):
        for idx, value in self.ignoreTable.items():
            SystemManager.printWarning("Ignore %s event %d times" % (idx, value['ignCnt']))



    def getSymbols(self):
        binPath = ''
        offsetList = []
        curIdx = 0
        lastIdx = len(self.posData)

        # Set alarm handler to handle hanged addr2line #
        signal.signal(signal.SIGALRM, SystemManager.timerHandler)

        # Get symbols and source pos #
        for idx, value in sorted(self.posData.items(), key=lambda e: e[1]['binary'], reverse=True):
            curIdx += 1
            SystemManager.printProgress(curIdx, lastIdx)

            # Handle thumbcode #
            if idx == '00c0ffee':
                value['binary'] = '??'
                value['origBin'] = '??'
                value['symbol'] = 'ThumbCode'
                continue

            if value['binary'] == '':
                # user pos without offset #
                if value['symbol'] == '' or value['symbol'] == '??':
                    # toDo: find binary path and symbol of pos #
                    value['binary'] = '??'
                    value['origBin'] = '??'
                    value['symbol'] = idx
                continue

            # Get symbols from address list of previous binary #
            if binPath != value['binary']:
                if binPath != '':
                    # Get symbols #
                    self.getSymbolInfo(binPath, offsetList)
                    offsetList = []

                if value['offset'] == hex(0):
                    offsetList.append(idx)
                else:
                    offsetList.append(value['offset'])

                # Set new binPath to find symbol from address #
                binPath = value['binary']
            # add address to offsetList #
            else:
                # not relocatable binary #
                if value['offset'] == hex(0):
                    offsetList.append(idx)
                # relocatable binary #
                else:
                    offsetList.append(value['offset'])

        # Get symbols and source path from last binary #
        if binPath != '':
            self.getSymbolInfo(binPath, offsetList)



    def getSymbolInfo(self, binPath, offsetList):
        try:
            import subprocess
        except ImportError:
            err = sys.exc_info()[1]
            SystemManager.printError("Fail to import package: " + err.args[0])
            sys.exit(0)

        # Recognize binary type #
        relocated = SystemManager.isRelocatableFile(binPath)

        # No file exist #
        if os.path.isfile(binPath) == False:
            SystemManager.printWarning("Fail to find %s" % binPath)

            for addr in offsetList:
                try:
                    if relocated is False:
                        self.posData[addr]['symbol'] = 'NoFile'
                        self.posData[addr]['src'] = 'NoFile'
                    else:
                        for idx, value in sorted(\
                            self.posData.items(), key=lambda e: e[1]['binary'], reverse=True):
                            if value['binary'] == binPath and value['offset'] == hex(int(addr, 16)):
                                self.posData[idx]['symbol'] = 'NoFile'
                                self.posData[idx]['src'] = 'NoFile'
                                break
                except:
                    SystemManager.printWarning("Fail to find address %s" % addr)
            return

        # Check addr2line path #
        if SystemManager.addr2linePath is None:
            SystemManager.printError(\
                "Fail to find addr2line, use also -l option with addr2line path for user mode")
            sys.exit(0)
        else:
            for path in SystemManager.addr2linePath:
                if os.path.isfile(path) is False:
                    SystemManager.printError(\
                        "Fail to find addr2line, use also -l option with addr2line path for user mode")
                    sys.exit(0)

        for path in SystemManager.addr2linePath:
            # Set addr2line command #
            args = [path, "-C", "-f", "-a", "-e", binPath]

            # Limit the number of arguments to be passed because of ARG_MAX #
            # ARG_MAX = $(getconf PAGE_SIZE)*32 = 131072 #
            listLen = len(offsetList)
            maxArgLine = 256
            offset = 0
            timeout = 10

            # Get symbol by address of every maxArgLine elements in list #
            while offset < listLen:
                # Launch addr2line #
                proc = subprocess.Popen(args + offsetList[offset:offset+maxArgLine-1], \
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                # Increase offset count in address list #
                offset += maxArgLine

                try:
                    # Set alarm to handle hanged addr2line #
                    signal.alarm(timeout)

                    # Wait for addr2line to finish its job #
                    proc.wait()

                    # Cancel alarm after addr2line respond #
                    signal.alarm(0)
                except:
                    SystemManager.printWarning('No response of addr2line for %s' % binPath)
                    continue

                while 1:
                    # Get return of addr2line #
                    addr = proc.stdout.readline().replace('\n', '')[2:]
                    symbol = proc.stdout.readline().replace('\n', '')
                    src = proc.stdout.readline().replace('\n', '')

                    err = proc.stderr.readline().replace('\n', '')
                    if len(err) > 0:
                        SystemManager.printWarning(err[err.find(':') + 2:])

                    if not addr:
                        # End of return #
                        break
                    elif symbol == '??':
                        symbol = addr

                    # Check whether the file is relocatable or not #
                    if relocated is False:
                        try:
                            savedSymbol = self.posData[addr]['symbol']
                        except:
                            continue

                        # Check whether saved symbol found by previous addr2line is right #
                        if savedSymbol == None or savedSymbol == '' or \
                            savedSymbol == addr or savedSymbol[0] == '$':
                            self.posData[addr]['symbol'] = symbol

                            if SystemManager.showAll:
                                self.posData[addr]['src'] = src
                            else:
                                fileIdx = src.rfind('/')
                                if fileIdx >= 0:
                                    self.posData[addr]['src'] = src[fileIdx + 1:]
                    else:
                        inBinArea = False

                        for idx, value in sorted(self.posData.items(), \
                            key=lambda e: e[1]['binary'], reverse=True):
                            if value['binary'] == binPath:
                                inBinArea = True

                                if value['offset'] == hex(int(addr, 16)):
                                    savedSymbol = self.posData[idx]['symbol']

                                    if savedSymbol == None or savedSymbol == '' or \
                                        savedSymbol == addr or savedSymbol[0] == '$':
                                        self.posData[idx]['symbol'] = symbol

                                        if SystemManager.showAll:
                                            self.posData[idx]['src'] = src
                                        else:
                                            fileIdx = src.rfind('/')
                                            if fileIdx >= 0:
                                                self.posData[idx]['src'] = src[fileIdx + 1:]

                                        break
                            elif inBinArea:
                                break



    def initStacks(self):
        self.nowCtx['userLastPos'] = '0'
        self.nowCtx['userCallStack'] = []
        self.nowCtx['kernelLastPos'] = '0'
        self.nowCtx['kernelCallStack'] = []



    def swapEvents(self):
        tempEvent = self.nowCtx['nowEvent']
        self.nowCtx['nowEvent'] = self.nowCtx['savedEvent']
        self.nowCtx['savedEvent'] = tempEvent

        tempCnt = self.nowCtx['nowCnt']
        self.nowCtx['nowCnt'] = self.nowCtx['savedCnt']
        self.nowCtx['savedCnt'] = tempCnt

        tempArg = self.nowCtx['nowArg']
        self.nowCtx['nowArg'] = self.nowCtx['savedArg']
        self.nowCtx['savedArg'] = tempArg



    def saveFullStack(\
        self, kernelPos, kernelStack, userPos, userStack, targetEvent, targetCnt, targetArg):

        # Save userstack #
        self.userCallData.append([userPos, userStack, targetEvent, targetCnt, targetArg])

        # Save kernelstack #
        self.kernelCallData.append([kernelPos, kernelStack, targetEvent, targetCnt, targetArg])

        # Save custom event stacks #
        if SystemManager.showAll and targetEvent == 'CUSTOM':
            self.customCallData.append(\
                [targetArg[0], targetArg[1], self.userCallData[-1], self.kernelCallData[-1]])



    def saveEventStack(self, targetEvent, targetCnt, targetArg):
        if targetEvent == 'CPU_TICK':
            self.periodicEventCnt += 1

        elif targetEvent == 'PAGE_ALLOC':
            self.pageAllocEventCnt += 1
            self.pageAllocCnt += targetCnt
            self.pageUsageCnt += targetCnt
            self.posData[self.nowCtx['kernelLastPos']]['pageCnt'] += targetCnt
            self.posData[self.nowCtx['userLastPos']]['pageCnt'] += targetCnt

            pageType = targetArg[0]
            pfn = targetArg[1]
            targetArg = [pageType, pfn]

        elif targetEvent == 'PAGE_FREE':
            self.pageFreeEventCnt += 1
            self.pageFreeCnt += targetCnt

            pageType = targetArg[0]
            pfn = targetArg[1]
            targetArg = [pageType, pfn]

        elif targetEvent == 'BLK_READ':
            self.blockRdEventCnt += 1
            self.blockRdUsageCnt += targetCnt
            self.posData[self.nowCtx['kernelLastPos']]['blockRdCnt'] += targetCnt
            self.posData[self.nowCtx['userLastPos']]['blockRdCnt'] += targetCnt

        elif targetEvent == 'BLK_WRITE':
            self.blockWrEventCnt += 1
            self.blockWrUsageCnt += targetCnt
            self.posData[self.nowCtx['kernelLastPos']]['blockWrCnt'] += targetCnt
            self.posData[self.nowCtx['userLastPos']]['blockWrCnt'] += targetCnt

        elif targetEvent == 'HEAP_EXPAND':
            self.heapExpEventCnt += 1
            self.heapExpSize += targetCnt
            self.posData[self.nowCtx['kernelLastPos']]['heapSize'] += targetCnt
            self.posData[self.nowCtx['userLastPos']]['heapSize'] += targetCnt

        elif targetEvent == 'HEAP_REDUCE':
            self.posData[self.nowCtx['kernelLastPos']]['heapSize'] += targetCnt
            self.posData[self.nowCtx['userLastPos']]['heapSize'] += targetCnt

        elif targetEvent == 'CUSTOM':
            if targetCnt > 0:
                self.customTotal += 1
                self.customCnt += targetCnt

                self.posData[self.nowCtx['kernelLastPos']]['customTotal'] += 1
                self.posData[self.nowCtx['userLastPos']]['customTotal'] += 1

                self.posData[self.nowCtx['kernelLastPos']]['customCnt'] += targetCnt
                self.posData[self.nowCtx['userLastPos']]['customCnt'] += targetCnt

        else:
            pass

        self.saveFullStack(self.nowCtx['kernelLastPos'], self.nowCtx['kernelCallStack'], \
            self.nowCtx['userLastPos'], self.nowCtx['userCallStack'], \
            targetEvent, targetCnt, targetArg)



    def saveCallStack(self):
        # stack of kernel thread #
        if self.nowCtx['prevMode'] != self.nowCtx['curMode'] == 'kernel':
            if len(self.nowCtx['userCallStack']) == 0 and \
                len(self.nowCtx['kernelCallStack']) > 0:
                    # Set userLastPos to None #
                self.nowCtx['userLastPos'] = '0'
                self.nowCtx['userCallStack'].append('0')
            if len(self.nowCtx['kernelCallStack']) == 0 and \
                len(self.nowCtx['userCallStack']) > 0:
                # Set kernelLastPos to None #
                self.nowCtx['kernelLastPos'] = '0'
                self.nowCtx['kernelCallStack'].append('0')

        # complicated situation ;( #
        elif self.nowCtx['prevMode'] == self.nowCtx['curMode']:
            # previous user stack loss or nested interval #
            if self.nowCtx['curMode'] is 'kernel':
                # nested interval #
                if self.nowCtx['nowEvent'] is 'CPU_TICK':
                # Backup kernel stack #
                    self.nowCtx['bakKernelLastPos'] = self.nowCtx['kernelLastPos']
                    self.nowCtx['bakKernelCallStack'] = self.nowCtx['kernelCallStack']

                    # Initialize both stacks #
                    self.initStacks()
                # previous user stack loss #
                else:
                    # Set userLastPos to None #
                    self.nowCtx['userLastPos'] = '0'
                    self.nowCtx['userCallStack'].append('0')
            # nested interval #
            elif self.nowCtx['curMode'] is 'user':
                '''
                CORE/0 EVENT0
                CORE/0 <kernel>
                CORE/0 <user>

                CORE/0 EVENT1
                CORE/0 <kernel>
                    CORE/0 EVENT2
                    CORE/0 <kernel>
                    CORE/0 <user>
                CORE/0 <user>
                '''
                # Swap nowEvent and savedEvent #
                self.swapEvents()

        # Save both stacks of previous event before starting to record new kernel stack #
        if (len(self.nowCtx['userCallStack']) > 0 and self.nowCtx['userLastPos'] != '') and \
            (len(self.nowCtx['kernelCallStack']) > 0 and self.nowCtx['kernelLastPos'] != ''):
                # Remove pc in each stacks #
            del self.nowCtx['kernelCallStack'][0], \
                self.nowCtx['userCallStack'][0]

            # Check whether there is nested event or not #
            if self.nowCtx['nested'] > 0:
                '''
                CORE/0 EVENT0
                CORE/0 <kernel>
                CORE/0 <user>

                CORE/0 EVENT1
                    CORE/0 EVENT2
                    CORE/0 <kernel>
                    CORE/0 <user>
                CORE/0 <kernel>
                CORE/0 <user>
                '''
                targetEvent = self.nowCtx['nestedEvent']
                targetCnt = self.nowCtx['nestedCnt']
                targetArg = self.nowCtx['nestedArg']

                # Swap nowEvent and savedEvent #
                self.swapEvents()
            else:
                targetEvent = self.nowCtx['savedEvent']
                targetCnt = self.nowCtx['savedCnt']
                targetArg = self.nowCtx['savedArg']

            # Save full stack of previous event #
            self.saveEventStack(targetEvent, targetCnt, targetArg)

            # Recover previous kernel stack after handling nested event #
            if self.nowCtx['prevMode'] == self.nowCtx['curMode'] == 'user' and \
                self.nowCtx['bakKernelLastPos'] != '0':
                self.nowCtx['kernelLastPos'] = self.nowCtx['bakKernelLastPos']
                self.nowCtx['kernelCallStack'] = self.nowCtx['bakKernelCallStack']
                self.nowCtx['bakKernelLastPos'] = '0'
                self.nowCtx['bakKernelCallStack'] = []
            else:
                self.nowCtx['kernelLastPos'] = ''
                self.nowCtx['kernelCallStack'] = []

            # Initialize user stack #
            self.nowCtx['userLastPos'] = ''
            self.nowCtx['userCallStack'] = []
            self.nowCtx['nestedEvent'] = ''
            self.nowCtx['nestedCnt'] = 0

        # On stack recording switch #
        self.nowCtx['recStat'] = True



    def savePosData(self, pos, path, offset):
        if self.nowCtx['nested'] > 0:
            targetEvent = self.nowCtx['savedEvent']
        else:
            targetEvent = self.nowCtx['nowEvent']

        # Register pos #
        try:
            self.posData[pos]
            if path is not None and path[0] == '/' and path != self.posData[pos]['origBin']:
                self.duplicatedPos += 1
                '''
                SystemManager.printWarning("duplicated address %s in both '%s' and '%s'" % \
                    (pos, path, self.posData[pos]['origBin']))
                '''
        except:
            self.posData[pos] = dict(self.init_posData)

        # user mode #
        if self.nowCtx['curMode'] is 'user':
            # Set path #
            if path is not None:
                self.posData[pos]['origBin'] = path
                self.posData[pos]['binary'] = SystemManager.rootPath + path
                self.posData[pos]['binary'] = self.posData[pos]['binary'].replace('//', '/')

                # Set offset #
                if offset is not None:
                    if SystemManager.isRelocatableFile(path):
                        self.posData[pos]['offset'] = offset

            # Save pos #
            if len(self.nowCtx['userCallStack']) == 0:
                self.nowCtx['userLastPos'] = pos

                if targetEvent == 'CPU_TICK':
                    self.posData[pos]['posCnt'] += 1

            self.nowCtx['userCallStack'].append(pos)
        # kernel mode #
        elif self.nowCtx['curMode'] is 'kernel':
            # Save pos #
            if len(self.nowCtx['kernelCallStack']) == 0:
                self.nowCtx['kernelLastPos'] = pos

                if targetEvent == 'CPU_TICK':
                    self.posData[pos]['posCnt'] += 1
            # Skip pos because it is usercall or no symbol #
            elif SystemManager.showAll is False and path is None:
                return

            self.posData[pos]['symbol'] = path

            self.nowCtx['kernelCallStack'].append(pos)

        # wrong mode #
        else:
            SystemManager.printWarning('wrong current mode %s' % self.nowCtx['curMode'])

        # Increase total call count #
        if self.nowEvent == 'CPU_TICK':
            self.posData[pos]['totalCnt'] += 1



    def allocHeapSeg(self, tid, size):
        try:
            self.heapTable[tid + '-ready']['size'] = size
            self.heapTable[tid + '-ready']['tid'] = tid
            self.threadData[thread]['heapSize'] -= size
            SystemManager.printWarning('Overwrite heap segment of %s(%s) at %s' % \
                (self.threadData[tid]['comm'], tid, SystemManager.dbgEventLine))
        except:
            self.heapTable[tid + '-ready'] = dict(self.init_heapSegData)
            self.heapTable[tid + '-ready']['size'] = size
            self.heapTable[tid + '-ready']['tid'] = tid



    def freeHeapSeg(self, addr):
        try:
            self.heapRedEventCnt += 1
            self.heapRedSize += self.heapTable[addr]['size']

            self.threadData[self.heapTable[addr]['tid']]['heapSize'] -= \
                self.heapTable[addr]['size']

            del self.heapTable[addr]
        except:
            SystemManager.printWarning('Fail to free heap segment %s of %s(%s) at %s' % \
                (addr, self.threadData[tid]['comm'], tid, SystemManager.dbgEventLine))



    def setHeapSegAddr(self, tid, addr):
        try:
            self.heapTable[addr] = dict(self.heapTable[tid + '-ready'])
            del self.heapTable[tid + '-ready']
        except:
            SystemManager.printWarning('Fail to set address of heap segment %s of %s(%s) at %s' % \
                (addr, self.threadData[tid]['comm'], tid, SystemManager.dbgEventLine))



    def parseLogs(self, lines, desc):
        curIdx = 0
        lastIdx = len(lines)

        # make custom event table #
        if SystemManager.customCmd is not None:
            for cmd in SystemManager.customCmd:
                cmd = cmd.split(':')

                if len(cmd) > 1:
                    self.customEventTable[cmd[0]] = cmd[1]
                else:
                    self.customEventTable[cmd[0]] = None
        if SystemManager.kernelCmd is not None:
            for cmd in SystemManager.kernelCmd:
                cmd = cmd.split(':')
                self.customEventTable[cmd[0]+'_enter'] = None
                self.customEventTable[cmd[0]+'_exit'] = None
        if SystemManager.userCmd is not None:
            for cmd in SystemManager.userCmd:
                cmd = cmd.split(':')
                self.customEventTable[cmd[0]+'_enter'] = None
                self.customEventTable[cmd[0]+'_exit'] = None

        # start to parse logs #
        for liter in lines:
            curIdx += 1
            SystemManager.logSize += len(liter)
            SystemManager.curLine += 1
            SystemManager.dbgEventLine += 1

            ret = self.parseEventLog(liter, desc)
            SystemManager.printProgress(curIdx, lastIdx)

            # Skip lines before first meaningful event #
            if self.lastCore is None:
                continue

            # Set context of current core #
            self.nowCtx = self.coreCtx[self.lastCore]

            # Save full stack to callData table #
            if ret is True:
                self.saveCallStack()

            # Ignore this log because its not event or stack info related to target thread #
            elif ret is False:
                self.nowCtx['recStat'] = False
                continue

            # Save pos into target stack #
            elif self.nowCtx['recStat']:
                # decode return value #
                (pos, path, offset) = ret

                self.savePosData(pos, path, offset)

        # Save stack of last events per core #
        for idx in self.coreCtx.keys():
            self.lastCore = idx
            self.nowCtx = self.coreCtx[idx]

            # Recover previous mode #
            if SystemManager.userEnable:
                self.nowCtx['prevMode'] = 'user'
            self.nowCtx['curMode'] = 'kernel'

            self.saveEventParam('IGNORE', 0, 0)
            self.nowCtx['nested'] -= 1
            self.saveCallStack()

        if self.duplicatedPos > 0:
            SystemManager.printWarning("Found %d addresses duplicated" % self.duplicatedPos)



    def getCustomEventValue(self, func, args, cond):
        if cond is None:
            return 1

        # set condition #
        if cond.find('>') >= 0:
            condVal = cond[cond.find('>') + 1:]
            condOp = '>'
            condStr = cond[:cond.find('>')]
        elif cond.find('<') >= 0:
            condVal = cond[cond.find('<') + 1:]
            condOp = '<'
            condStr = cond[:cond.find('<')]
        elif cond.find('==') >= 0:
            condVal = cond[cond.find('==') + 2:]
            condOp = '=='
            condStr = cond[:cond.find('==')]
        else:
            condStr = cond
            condOp = None
            condVal = None

        m = re.match(r'^.+%s=(?P<value>\S+)' % condStr, args)
        if m is not None:
            d = m.groupdict()

            value = d['value']

            if condOp is None and value is not None:
                try:
                    return int(value)
                except:
                    return 0
            elif condOp is '>':
                try:
                    if int(value) > int(condVal):
                        return int(value)
                except:
                    pass

                return 0
            elif condOp is '<':
                try:
                    if int(value) < int(condVal):
                        return int(value)
                except:
                    pass

                return 0
            elif condOp is '==':
                if value == condVal:
                    return 1
                else:
                    return 0
            else:
                return 0
        else:
            return 0



    def saveEventParam(self, event, count, arg):
        self.nowCtx['nestedEvent'] = self.nowCtx['savedEvent']
        self.nowCtx['savedEvent'] = self.nowCtx['nowEvent']
        self.nowCtx['nowEvent'] = event

        self.nowCtx['nestedCnt'] = self.nowCtx['savedCnt']
        self.nowCtx['savedCnt'] = self.nowCtx['nowCnt']
        self.nowCtx['nowCnt'] = count

        self.nowCtx['nestedArg'] = self.nowCtx['savedArg']
        self.nowCtx['savedArg'] = self.nowCtx['nowArg']
        self.nowCtx['nowArg'] = arg

        self.nowCtx['nested'] += 1

        if self.nowCtx['nested'] > 2:
            #self.printDbgInfo()
            SystemManager.printError(\
                "Fail to analyze because of corrupted data (over) at %s" % \
                SystemManager.dbgEventLine)
            sys.exit(0)


    def printDbgInfo(self):
        data = self.nowCtx

        print('[%s]' % self.lastCore, \
            '(now) %s/%s/%s' %(data['nowEvent'], data['nowCnt'], data['nowArg']), \
            '(saved) %s/%s/%s' %(data['savedEvent'], data['savedCnt'], data['savedArg']), \
            '(nested) %s/%s/%s' %(data['nestedEvent'], data['nestedCnt'], data['nestedArg']), \
            '(user) %s/%s' % (data['userLastPos'], len(data['userCallStack'])), \
            '(kernel) %s/%s' % (data['kernelLastPos'], len(data['kernelCallStack'])), \
            '(backup) %s/%s' % (data['bakKernelLastPos'], len(data['bakKernelCallStack'])), \
            'at %s' % SystemManager.dbgEventLine)



    def parseEventInfo(self, tid, func, args):
        if func[:-1] in self.customEventTable:
            isFixedEvent = False
        else:
            isFixedEvent = True

        # cpu tick event #
        # toDo: find shorter periodic event for sampling #
        if isFixedEvent and func == "hrtimer_start:" and args.rfind('tick_sched_timer') > -1:
            self.cpuEnabled = True

            self.saveEventParam('CPU_TICK', 1, 0)

            return False

        # memory allocation event #
        elif isFixedEvent and func == "mm_page_alloc:":
            m = re.match(\
                r'^\s*page=\s*(?P<page>\S+)\s+pfn=(?P<pfn>[0-9]+)\s+order=(?P<order>[0-9]+)\s+' + \
                r'migratetype=(?P<mt>[0-9]+)\s+gfp_flags=(?P<flags>\S+)', args)
            if m is not None:
                d = m.groupdict()

                # check whether it is huge page #
                if d['page'] == '(null)':
                    page = 'huge'
                else:
                    page = d['page']

                pfn = int(d['pfn'])
                flags = d['flags']
                pageCnt = pow(2, int(d['order']))

                # Increase page count of thread #
                self.threadData[tid]['nrPages'] += pageCnt

                # Increase page counts of thread #
                pageType = None
                if flags.find('NOFS') >= 0 or flags.find('GFP_WRITE') >= 0 or flags.find('0x1000000') >= 0:
                    pageType = 'CACHE'
                    self.threadData[tid]['cachePages'] += pageCnt
                elif flags.find('USER') >= 0:
                    pageType = 'USER'
                    self.threadData[tid]['userPages'] += pageCnt
                else:
                    pageType = 'KERNEL'
                    self.threadData[tid]['kernelPages'] += pageCnt

                # Make PTE in page table #
                for cnt in xrange(0, pageCnt):
                    pfnv = pfn + cnt

                    try:
                        '''
                        Decrease page count of it's owner \
                        because this page was already allocated but no free log
                        '''

                        ownerTid = self.pageTable[pfnv]['tid']
                        self.threadData[ownerTid]['nrPages'] -= 1

                        origPageType = self.pageTable[pfnv]['type']
                        if origPageType == 'USER':
                            self.threadData[ownerTid]['userPages'] -= 1
                        elif origPageType == 'CACHE':
                            self.threadData[ownerTid]['cachePages'] -= 1
                        elif origPageType == 'KERNEL':
                            self.threadData[ownerTid]['kernelPages'] -= 1
                    except:
                        self.pageTable[pfnv] = dict(self.init_pageData)

                    self.pageTable[pfnv]['tid'] = tid
                    self.pageTable[pfnv]['page'] = page
                    self.pageTable[pfnv]['flags'] = flags
                    self.pageTable[pfnv]['type'] = pageType
                    self.pageTable[pfnv]['time'] = time

                self.memEnabled = True

                self.saveEventParam('PAGE_ALLOC', pageCnt, [pageType, pfn])
            else:
                self.saveEventParam('IGNORE', 0, func[:-1])

                SystemManager.printWarning("Fail to recognize event %s at %d" % \
                        (func[:-1], SystemManager.dbgEventLine))

            return False

        # memory free event #
        elif isFixedEvent and func == "mm_page_free:":
            m = re.match(r'^\s*page=(?P<page>\S+)\s+pfn=(?P<pfn>[0-9]+)\s+' + \
                r'order=(?P<order>[0-9]+)', args)
            if m is not None:
                d = m.groupdict()

                page = d['page']
                pfn = int(d['pfn'])
                pageCnt = pow(2, int(d['order']))

                # Update page table #
                origPageType = None
                for cnt in xrange(0, pageCnt):
                    pfnv = pfn + cnt

                    try:
                        origPageType = self.pageTable[pfnv]['type']
                        self.threadData[self.pageTable[pfnv]['tid']]['nrPages'] -= 1

                        if origPageType is 'CACHE':
                            self.threadData[self.pageTable[pfnv]['tid']]['cachePages'] -= 1
                        elif origPageType is 'USER':
                            self.threadData[self.pageTable[pfnv]['tid']]['userPages'] -= 1
                        elif origPageType is 'KERNEL':
                            self.threadData[self.pageTable[pfnv]['tid']]['kernelPages'] -= 1

                        del self.pageTable[pfnv]
                        self.pageTable[pfnv] = None
                    except:
                        # this page was allocated before starting profile #

                        self.threadData[tid]['nrUnknownFreePages'] += 1
                        continue

                self.memEnabled = True

                self.saveEventParam('PAGE_FREE', pageCnt, [origPageType, pfn])

                return False

            SystemManager.printWarning("Fail to recognize event %s at %d" % \
                    (func[:-1], SystemManager.dbgEventLine))

            self.saveEventParam('IGNORE', 0, func[:-1])

            return False

        # heap increase start event #
        elif isFixedEvent and func == "sys_enter:":
            m = re.match(r'^\s*NR (?P<nr>[0-9]+) (?P<args>.+)', args)
            if m is not None:
                b = m.groupdict()

                if int(b['nr']) == ConfigManager.sysList.index('sys_brk') or \
                    int(b['nr']) == ConfigManager.getMmapId():
                    self.heapEnabled = True

                    try:
                        size = int(b['args'].split(',')[1], 16)

                        # just brk call to check data segment address #
                        if size == 0:
                            pass

                        self.threadData[tid]['heapSize'] += size
                    except:
                        self.saveEventParam('IGNORE', 0, func[:-1])

                        return False

                    # make heap segment tid-ready #
                    self.allocHeapSeg(tid, size)

                    self.saveEventParam('IGNORE', 0, func[:-1])

                    return False

                elif int(b['nr']) == ConfigManager.sysList.index('sys_munmap'):
                    self.heapEnabled = True

                    try:
                        addr = int(b['args'][1:].split(',')[0], 16)
                        size = self.heapTable[addr]['size']

                        # remove heap segment #
                        self.freeHeapSeg(addr)

                        self.saveEventParam('HEAP_REDUCE', size, addr)

                        return False
                    except:
                        pass

                else:
                    SystemManager.printWarning("Fail to recognize event %s at %d" % \
                            (func[:-1], SystemManager.dbgEventLine))

            self.saveEventParam('IGNORE', 0, func[:-1])

            return False

        # heap increase return event #
        elif isFixedEvent and func == "sys_exit:":
            m = re.match(r'^\s*NR (?P<nr>[0-9]+) = (?P<ret>.+)', args)
            if m is not None:
                b = m.groupdict()

                if int(b['nr']) == ConfigManager.sysList.index('sys_brk') or \
                    int(b['nr']) == ConfigManager.getMmapId():
                    self.heapEnabled = True

                    addr = int(b['ret'])

                    # rename heap segment from tid-ready to addr #
                    self.setHeapSegAddr(tid, addr)

                    try:
                        size = self.heapTable[addr]['size']

                        self.saveEventParam('HEAP_EXPAND', size, addr)

                        return False
                    except:
                        pass

            SystemManager.printWarning("Fail to recognize event %s at %d" % \
                    (func[:-1], SystemManager.dbgEventLine))

            self.saveEventParam('IGNORE', 0, func[:-1])

            return False

        # block read request event #
        elif isFixedEvent and func == "block_bio_remap:":
            m = re.match(r'^\s*(?P<major>[0-9]+),(?P<minor>[0-9]+)\s*(?P<operation>\S+)\s*' + \
                r'(?P<address>\S+)\s+\+\s+(?P<size>[0-9]+)', args)
            if m is not None:
                b = m.groupdict()

                if b['operation'][0] == 'R':
                    self.breadEnabled = True

                    blockRdCnt = int(b['size'])
                    self.threadData[tid]['nrRdBlocks'] += blockRdCnt

                    self.saveEventParam('BLK_READ', blockRdCnt, 0)

                    return False

            SystemManager.printWarning("Fail to recognize event %s at %d" % \
                    (func[:-1], SystemManager.dbgEventLine))

            self.saveEventParam('IGNORE', 0, func[:-1])

            return False

        # block write request event #
        elif isFixedEvent and func == "writeback_dirty_page:":
            m = re.match(r'^\s*bdi\s+(?P<major>[0-9]+):(?P<minor>[0-9]+):\s*' + \
                r'ino=(?P<ino>\S+)\s+index=(?P<index>\S+)', args)
            if m is not None:
                b = m.groupdict()
                self.bwriteEnabled = True

                self.threadData[tid]['nrWrBlocks'] += 1

                self.saveEventParam('BLK_WRITE', 1, 0)

                return False

            self.saveEventParam('IGNORE', 0, func[:-1])

            return False

        # block write request event #
        elif isFixedEvent and func == "wbc_writepage:":
            m = re.match(r'^\s*bdi\s+(?P<major>[0-9]+):(?P<minor>[0-9]+):\s*' + \
                r'towrt=(?P<towrt>\S+)\s+skip=(?P<skip>\S+)', args)
            if m is not None:
                d = m.groupdict()

                if d['skip'] == '0':
                    self.bwriteEnabled = True

                    self.threadData[tid]['nrWrBlocks'] += 1

                    self.saveEventParam('BLK_WRITE', 1, 0)

                    return False

            self.saveEventParam('IGNORE', 0, func[:-1])

            return False

        # segmentation fault generation event #
        elif isFixedEvent and func == "signal_generate:":
            m = re.match(r'^\s*sig=(?P<sig>[0-9]+) errno=(?P<err>[0-9]+) ' + \
                r'code=(?P<code>.*) comm=(?P<comm>.*) pid=(?P<pid>[0-9]+)', args)
            if m is not None:
                b = m.groupdict()

                if b['sig'] == str(ConfigManager.sigList.index('SIGSEGV')):
                    self.sigEnabled = True

                    self.saveEventParam('SIGSEGV_GEN', 0, 0)

                    return False

            SystemManager.printWarning("Fail to recognize event %s at %d" % \
                    (func[:-1], SystemManager.dbgEventLine))

            self.saveEventParam('IGNORE', 0, func[:-1])

            return False

        elif isFixedEvent and func == "signal_deliver:":
            m = re.match(r'^\s*sig=(?P<sig>[0-9]+) errno=(?P<err>[0-9]+) code=(?P<code>.*) ' + \
                r'sa_handler=(?P<handler>.*) sa_flags=(?P<flags>.*)', args)
            if m is not None:
                b = m.groupdict()

                if b['sig'] == str(ConfigManager.sigList.index('SIGSEGV')):
                    self.sigEnabled = True

                    self.saveEventParam('SIGSEGV_DLV', 0, 0)
                else:
                    self.saveEventParam('IGNORE', 0, func[:-1])
            else:
                self.saveEventParam('IGNORE', 0, func[:-1])

            return False

        # Start to record user stack #
        elif func == "<user":
            self.nowCtx['prevMode'] = self.nowCtx['curMode']
            self.nowCtx['curMode'] = 'user'

            return True

        # Start to record kernel stack #
        elif func == "<stack":
            self.nowCtx['prevMode'] = self.nowCtx['curMode']
            self.nowCtx['curMode'] = 'kernel'
            self.nowCtx['nested'] -= 1

            if self.nowCtx['nested'] < 0:
                #self.printDbgInfo()
                SystemManager.printError(\
                    "Fail to analyze data because of corrupted data (under) at %s" % \
                    SystemManager.dbgEventLine)
                sys.exit(0)

            return True

        # custom event #
        elif isFixedEvent is False:
            try:
                cond = self.customEventTable[func[:-1]]

                customCnt = self.getCustomEventValue(func, args, cond)

                if customCnt > 0:
                    self.threadData[tid]['customTotal'] += customCnt

                self.saveEventParam('CUSTOM', customCnt, [func[:-1], args])
            except:
                self.saveEventParam('IGNORE', 0, func[:-1])

            return False

        # Ignore event #
        else:
            self.saveEventParam('IGNORE', 0, func[:-1])

            return False



    def parseEventLog(self, string, desc):
        # Filter for event #
        if SystemManager.tgidEnable:
            m = re.match(r'^\s*(?P<comm>.+)-(?P<thread>[0-9]+)\s+\(\s*(?P<tgid>\S+)\)\s+' + \
                r'\[(?P<core>[0-9]+)\]\s+(?P<time>\S+):\s+(?P<func>\S+)(?P<etc>.+)', string)
        else:
            m = re.match(r'^\s*(?P<comm>.+)-(?P<thread>[0-9]+)\s+\[(?P<core>[0-9]+)\]\s+' + \
                r'(?P<time>\S+):\s+(?P<func>\S+)(?P<etc>.+)', string)

        if m is not None:
            d = m.groupdict()

            # Set time #
            if self.startTime == '0':
                self.startTime = d['time']
            else:
                self.finishTime = d['time']

            # Make thread entity #
            thread = d['thread']
            try:
                self.threadData[thread]['comm'] = d['comm']
            except:
                self.threadData[thread] = dict(self.init_threadData)
                self.threadData[thread]['comm'] = d['comm']

            # Set pid of thread #
            try:
                self.threadData[thread]['tgid'] = SystemManager.savedProcTree[thread]
            except:
                pass

            # increase event count #
            self.threadData[thread]['eventCnt'] += 1

            # set current core #
            self.lastCore = d['core']

            # Make core entity #
            try:
                self.coreCtx[self.lastCore]
            except:
                self.coreCtx[self.lastCore] = dict(self.init_ctxData)
                self.coreCtx[self.lastCore]['userCallStack'] = []
                self.coreCtx[self.lastCore]['kernelCallStack'] = []
                self.coreCtx[self.lastCore]['bakKernelCallStack'] = []

            # set context of current core #
            self.nowCtx = self.coreCtx[self.lastCore]

            # Calculate a total of cpu usage #
            if d['func'] == "hrtimer_start:" and d['etc'].rfind('tick_sched_timer') > -1:
                self.totalTick += 1
                self.threadData[thread]['cpuTick'] += 1

                # Set global interval #
                if self.nowCtx['prevTid'] is not None:
                    diff = float(d['time']) - float(self.nowCtx['prevTime'])
                    self.periodicEventInterval += diff
                    self.periodicContEventCnt += 1

                self.nowCtx['prevTid'] = thread
                self.nowCtx['prevTime'] = d['time']

                # Set max core to calculate cpu usage of thread #
                if SystemManager.maxCore < int(d['core']):
                    SystemManager.maxCore = int(d['core'])

            # Mark die flag of thread that is not able to be profiled #
            elif d['func'] == "sched_process_exit:":
                m = re.match(r'^\s*comm=(?P<comm>.*)\s+pid=(?P<pid>[0-9]+)', d['etc'])
                if m is not None:
                    p = m.groupdict()

                    pid = p['pid']

                    try:
                        self.threadData[pid]
                    except:
                        self.threadData[pid] = dict(self.init_threadData)
                        self.threadData[pid]['comm'] = p['comm']

                    self.threadData[pid]['die'] = True

            # Make thread name #
            elif d['func'] == "task_newtask:":
                m = re.match(r'^\s*pid=(?P<pid>[0-9]+)\s+comm=(?P<comm>\S+)', d['etc'])
                if m is not None:
                    p = m.groupdict()

                    pid = p['pid']

                    try:
                        self.threadData[pid]
                    except:
                        self.threadData[pid] = dict(self.init_threadData)
                        self.threadData[pid]['comm'] = p['comm']

                    self.threadData[pid]['new'] = True

            # Save user event #
            elif d['func'].startswith("tracing_mark_write"):
                m = re.match(r'^\s*\S*: EVENT_(?P<event>\S+)', d['etc'])
                if m is not None:
                    gd = m.groupdict()

                    ei.addEvent(d['time'], gd['event'])

            # Save tgid(pid) #
            if SystemManager.tgidEnable and self.threadData[thread]['tgid'] == '-----':
                self.threadData[thread]['tgid'] = d['tgid']

            # tid filter #
            found = False
            for val in desc:
                if val == thread or val == '':
                    self.threadData[thread]['target'] = True
                    found = True
                    break
                elif SystemManager.groupProcEnable:
                    try:
                        if self.threadData[thread]['tgid'] == SystemManager.savedProcTree[val]:
                            self.threadData[thread]['target'] = True
                            found = True
                            break
                    except:
                        pass

            if found is False:
                return False

            return self.parseEventInfo(thread, d['func'], d['etc'])

        # Parse call stack #
        else:
            pos = string.find('=>  <')
            m = re.match(r' => (?P<path>.+)\[\+0x(?P<offset>.\S*)\] \<(?P<pos>.\S+)\>', string)

            # exist path, offset, pos #
            if m is not None:
                d = m.groupdict()
                return (d['pos'], d['path'], hex(int(d['offset'], 16)))

            # exist only pos #
            elif pos > -1:
                return (string[pos+5:len(string)-2], None, None)

            # exist nothing #
            elif string.find('??') > -1:
                return ('0', None, None)

            else:
                m = re.match(r' => (?P<symbol>.+) \<(?P<pos>.\S+)\>', string)

                # exist symbol, pos #
                if m is not None:
                    d = m.groupdict()
                    return (d['pos'], d['symbol'], None)

                # garbage log #
                else:
                    return False



    def parseMapLine(self, string):
        m = re.match(r'^(?P<startAddr>.\S+)-(?P<endAddr>.\S+) (?P<permission>.\S+) ' + \
            r'(?P<offset>.\S+) (?P<devid>.\S+) (?P<inode>.\S+)\s*(?P<binName>.\S+)', string)
        if m is not None:
            d = m.groupdict()
            self.mapData.append(\
                {'startAddr': d['startAddr'], 'endAddr': d['endAddr'], 'binName': d['binName']})



    def getBinInfo(self, addr):
        if SystemManager.rootPath is None:
            SystemManager.printError(\
                "Fail to recognize sysroot path of target for user mode, use also -r option")
            sys.exit(0)

        for data in self.mapData:
            if int(data['startAddr'], 16) <= int(addr, 16) and \
                int(data['endAddr'], 16) >= int(addr, 16):
                if SystemManager.isRelocatableFile(data['binName']):
                        # Return full path and offset about address in mapping table
                    return SystemManager.rootPath + data['binName'], \
                        hex(int(addr, 16) - int(data['startAddr'], 16))
                else:
                    return SystemManager.rootPath + data['binName'], \
                        hex(int(addr, 16))
        SystemManager.printWarning("Fail to get the binary info of %s in mapping table" % addr)



    def printUsage(self):
        targetCnt = 0
        self.totalTime = float(self.finishTime) - float(self.startTime)

        SystemManager.printTitle()

        # print system information #
        SystemManager.printInfoBuffer()

        # Print profiled thread list #
        SystemManager.pipePrint(\
            "[%s] [ %s: %0.3f ] [ %s: %0.3f ] [ Threads: %d ] [ LogSize: %d KB ]" % \
            ('Function Thread Info', 'Elapsed', round(self.totalTime, 7), \
            'Start', round(float(self.startTime), 7), \
             len(self.threadData), SystemManager.logSize >> 10))
        SystemManager.pipePrint(twoLine)
        SystemManager.pipePrint(\
            ("{0:_^16}|{1:_^7}|{2:_^7}|{3:_^10}|{4:_^7}|" + \
            "{5:_^7}({6:_^7}/{7:_^7}/{8:_^7})|{9:_^7}|{10:_^8}|" + \
            "{11:_^8}|{12:_^8}|{13:_^8}|{14:_^5}|{15:_^5}|").\
            format("Name", "Tid", "Pid", "Target", "CPU", \
            "MEM", "USER", "BUF", "KERN", "UFREE", "HEAP", \
            "BLK_RD", "BLK_WR", "CUSTOM", "DIE", "NEW"))
        SystemManager.pipePrint(twoLine)

        # set sort value #
        if SystemManager.sort == 'm':
            sortedThreadData = sorted(self.threadData.items(), \
                key=lambda e: e[1]['nrPages'], reverse=True)
        elif SystemManager.sort == 'b':
            sortedThreadData = sorted(self.threadData.items(), \
                key=lambda e: e[1]['nrRdBlocks'], reverse=True)
        else:
            # set cpu usage as default #
            sortedThreadData = sorted(self.threadData.items(), \
                key=lambda e: e[1]['cpuTick'], reverse=True)

        for idx, value in sortedThreadData:
            targetMark = ''
            dieMark = ''
            newMark = ''

            # skip no event count thread #
            if value['eventCnt'] == 0:
                continue

            # check target thread #
            if value['target']:
                targetCnt += 1
                if targetCnt == 2:
                    SystemManager.printWarning("Multiple target threads are selected")
                targetMark = '*'

            # get cpu usage #
            if self.totalTick > 0:
                cpuPer = float(value['cpuTick']) / float(self.totalTick) * 100
            else:
                cpuPer = 0

            # set break condition #
            if SystemManager.sort == 'm':
                breakCond = value['nrPages']
            elif SystemManager.sort == 'b':
                breakCond = value['nrRdBlocks']
            else:
                breakCond = cpuPer

            if breakCond < 1 and SystemManager.showAll is False:
                pass

            if value['die']:
                dieMark = 'v'

            if value['new']:
                newMark = 'v'

            SystemManager.pipePrint(\
                ("{0:16}|{1:^7}|{2:^7}|{3:^10}|{4:6.1f}%|" + \
                "{5:6}k({6:6}k/{7:6}k/{8:6}k)|{9:6}k|{10:7}k|" + \
                "{11:7}k|{12:7}k|{13:8}|{14:^5}|{15:^5}|").\
                format(value['comm'], idx, value['tgid'], targetMark, cpuPer, \
                value['nrPages'] * 4, value['userPages'] * 4, value['cachePages'] * 4, \
                value['kernelPages'] * 4, value['nrUnknownFreePages'] * 4, value['heapSize'] >> 10, \
                int(value['nrRdBlocks'] * 0.5), int(value['nrWrBlocks'] * 4), \
                value['customTotal'], dieMark, newMark))

        SystemManager.pipePrint(oneLine + '\n\n\n')

        # Exit because of no target #
        if len(self.target) == 0:
            SystemManager.printWarning("No specific thread targeted, input tid with -g option")

        # Print resource usage of functions #
        self.printCpuUsage()
        self.printMemUsage()
        self.printHeapUsage()
        self.printBlockRdUsage()
        self.printBlockWrUsage()
        self.printCustomUsage()



    def printCustomUsage(self):
        # no effective custom event #
        if self.customTotal == 0:
            return

        subStackIndex = FunctionAnalyzer.symStackIdxTable.index('STACK')
        eventIndex = FunctionAnalyzer.symStackIdxTable.index('CUSTOM')

        # Make custom event list #
        customList = ', '.join(self.customEventTable.keys())

        if SystemManager.userEnable:
            # Print custom usage in user space #
            SystemManager.clearPrint()
            SystemManager.pipePrint('[Function %s Info] [Cnt: %d] [Total: %d] (USER)' % \
                (customList, self.customTotal, self.customCnt))

            SystemManager.pipePrint(twoLine)
            SystemManager.pipePrint("{0:_^9}|{1:_^47}|{2:_^48}|{3:_^47}".\
                format("Usage", "Function", "Binary", "Source"))
            SystemManager.pipePrint(twoLine)

            for idx, value in sorted(\
                self.userSymData.items(), key=lambda e: e[1]['customCnt'], reverse=True):

                if value['customCnt'] == 0:
                    break

                SystemManager.pipePrint(\
                    "{0:7}  |{1:^47}|{2:48}|{3:37}".format(value['customCnt'], idx, \
                    self.posData[value['pos']]['origBin'], self.posData[value['pos']]['src']))

                # Set target stack #
                targetStack = []
                if self.sort is 'sym':
                    targetStack = value['symStack']
                elif self.sort is 'pos':
                    targetStack = value['stack']

                # Sort by usage #
                targetStack = sorted(targetStack, key=lambda x: x[eventIndex], reverse=True)

                # Merge and Print symbols in stack #
                for stack in targetStack:
                    eventCnt = stack[eventIndex]
                    subStack = list(stack[subStackIndex])

                    if eventCnt == 0:
                        break

                    if len(subStack) == 0:
                        continue
                    else:
                        # Make stack info by symbol for print #
                        symbolStack = ''
                        stackIdx = 0
                        indentLen = len("\t" * 4 * 4)
                        appliedIndentLen = indentLen

                        if self.sort is 'sym':
                            for sym in subStack:
                                if sym is None:
                                    symbolSet = ' <- None'
                                else:
                                    symbolSet = ' <- ' + sym + \
                                        ' [' + self.userSymData[sym]['origBin'] + ']'

                                lpos = appliedIndentLen + len(symbolStack[stackIdx:]) + len(symbolSet)
                                if lpos > SystemManager.lineLength:
                                    stackIdx = len(symbolStack)
                                    symbolStack += '\n' + ' ' * indentLen
                                    appliedIndentLen = 0

                                symbolStack += symbolSet
                        elif self.sort is 'pos':
                            for pos in subStack:
                                if pos is None:
                                    symbolStack += ' <- None'
                                # No symbol so that just print pos #
                                elif self.posData[pos]['symbol'] == '':
                                    symbolStack += ' <- ' + hex(int(pos, 16)) + \
                                        ' [' + self.posData[pos]['origBin'] + ']'
                                # Print symbol #
                                else:
                                    symbolStack += ' <- ' + self.posData[pos]['symbol'] + \
                                        ' [' + self.posData[pos]['origBin'] + ']'

                    SystemManager.pipePrint("\t\t +{0:7} |{1:32}".format(eventCnt, symbolStack))

                SystemManager.pipePrint(oneLine)

            SystemManager.pipePrint('')

        # Print custom usage in kernel space #
        SystemManager.clearPrint()
        SystemManager.pipePrint('[Function %s Info] [Cnt: %d] [Total: %d] (KERNEL)' % \
            (customList, self.customTotal, self.customCnt))

        SystemManager.pipePrint(twoLine)
        SystemManager.pipePrint("{0:_^9}|{1:_^144}".format("Usage", "Function"))
        SystemManager.pipePrint(twoLine)

        # Print custom usage of stacks #
        for idx, value in sorted(\
            self.kernelSymData.items(), key=lambda e: e[1]['customCnt'], reverse=True):

            if value['customCnt'] == 0:
                break

            SystemManager.pipePrint("{0:7}  |{1:^134}".format(value['customCnt'], idx))

            # Sort stacks by usage #
            value['stack'] = sorted(value['stack'], key=lambda x: x[eventIndex], reverse=True)

            # Print stacks by symbol #
            for stack in value['stack']:
                eventCnt = stack[eventIndex]
                subStack = list(stack[subStackIndex])

                if eventCnt == 0:
                    break

                if len(subStack) == 0:
                    continue
                elif len(subStack) == 1 and SystemManager.showAll is False and \
                    (self.posData[subStack[0]]['symbol'] is None or \
                    self.posData[subStack[0]]['symbol'] == 'NoFile'):
                    # Pass unmeaningful part #
                    continue
                else:
                    # Make stack info by symbol for print #
                    symbolStack = ''
                    stackIdx = 0
                    indentLen = len("\t" * 4 * 4)
                    appliedIndentLen = indentLen

                    try:
                        for pos in subStack:
                            if self.posData[pos]['symbol'] == '':
                                symbolSet = ' <- ' + hex(int(pos, 16))
                            elif self.posData[pos]['symbol'] == None and SystemManager.showAll:
                                symbolSet = ' <- ' + hex(int(pos, 16))
                            else:
                                symbolSet = ' <- ' + str(self.posData[pos]['symbol'])

                            lpos = appliedIndentLen + len(symbolStack[stackIdx:]) + len(symbolSet)
                            if lpos > SystemManager.lineLength:
                                stackIdx = len(symbolStack)
                                symbolStack += '\n' + ' ' * indentLen
                                appliedIndentLen = 0

                            symbolStack += symbolSet
                    except:
                        continue

                SystemManager.pipePrint("\t\t +{0:7} |{1:32}".format(eventCnt, symbolStack))

            SystemManager.pipePrint(oneLine + '\n')

        # Print custom call history #
        if SystemManager.showAll and len(self.customCallData) > 0:
            SystemManager.clearPrint()
            SystemManager.pipePrint('[Function %s History] [Cnt: %d] [Total: %d]' % \
                (customList, self.customTotal, self.customCnt))

            SystemManager.pipePrint(twoLine)
            SystemManager.pipePrint("{0:_^32}|{1:_^121}".format("Event", "Info"))
            SystemManager.pipePrint(twoLine)

            for call in self.customCallData:
                event = call[0]
                info = call[1]
                userstack = call[2]
                kernelstack = call[3]

                SystemManager.pipePrint("{0:^32}|{1:<121}".format(event, info))

                indentLen = 32
                nowLen = indentLen
                try:
                    last = call[2][0]
                    stack = call[2][1]
                    userCall = ' %s[%s]' % \
                        (self.posData[last]['symbol'], self.posData[last]['binary'])
                    nowLen += len(userCall)
                    for subcall in stack:
                        try:
                            nextCall = ' <- %s[%s]' % \
                                (self.posData[subcall]['symbol'], self.posData[subcall]['binary'])
                            if SystemManager.lineLength > nowLen + len(nextCall):
                                userCall = '%s%s' % (userCall, nextCall)
                                nowLen += len(nextCall)
                            else:
                                userCall = '%s\n%s %s' % (userCall, ' ' * indentLen, nextCall)
                                nowLen = indentLen + len(nextCall)
                        except:
                            pass
                except:
                    pass

                indentLen = 32
                nowLen = indentLen
                try:
                    last = call[3][0]
                    stack = call[3][1]
                    kernelCall = ' %s' % (self.posData[last]['symbol'])
                    nowLen += len(kernelCall)
                    for subcall in stack:
                        try:
                            nextCall = ' <- %s' % (self.posData[subcall]['symbol'])
                            if SystemManager.lineLength > nowLen + len(nextCall):
                                kernelCall = '%s%s' % (kernelCall, nextCall)
                                nowLen += len(nextCall)
                            else:
                                kernelCall = '%s\n%s %s' % (kernelCall, ' ' * indentLen, nextCall)
                                nowLen = indentLen + len(nextCall)
                        except:
                            pass
                except:
                    pass

                SystemManager.pipePrint("{0:>32}|{1:<121}".format('[User] ', userCall))
                SystemManager.pipePrint("{0:>32}|{1:<121}".format('[Kernel] ', kernelCall))
                SystemManager.pipePrint(oneLine)

        SystemManager.pipePrint('\n\n')



    def printCpuUsage(self):
        # no cpu event #
        if self.cpuEnabled is False or self.periodicContEventCnt == 0:
            return

        subStackIndex = FunctionAnalyzer.symStackIdxTable.index('STACK')
        cpuTickIndex = FunctionAnalyzer.symStackIdxTable.index('CPU_TICK')

        # average tick interval #
        self.periodicEventInterval /= self.periodicContEventCnt

        if SystemManager.userEnable:
            # Print cpu usage in user space #
            SystemManager.clearPrint()
            SystemManager.pipePrint('[Function CPU Info] [Cnt: %d] [Interval: %dms] (USER)' % \
                (self.periodicEventCnt, self.periodicEventInterval * 1000))

            SystemManager.pipePrint(twoLine)
            SystemManager.pipePrint("{0:_^9}|{1:_^47}|{2:_^48}|{3:_^47}".\
                format("Usage", "Function", "Binary", "Source"))
            SystemManager.pipePrint(twoLine)

            for idx, value in sorted(\
                self.userSymData.items(), key=lambda e: e[1]['tickCnt'], reverse=True):

                if value['tickCnt'] == 0:
                    break

                cpuPer = round(float(value['tickCnt']) / float(self.periodicEventCnt) * 100, 1)
                if cpuPer < 1 and SystemManager.showAll is False:
                    break

                SystemManager.pipePrint("{0:7}% |{1:^47}|{2:48}|{3:37}".format(cpuPer, idx, \
                    self.posData[value['pos']]['origBin'], self.posData[value['pos']]['src']))

                # Set target stack #
                targetStack = []
                if self.sort is 'sym':
                    targetStack = value['symStack']
                elif self.sort is 'pos':
                    targetStack = value['stack']

                # Sort by usage #
                targetStack.sort(reverse=True)

                # Merge and Print symbols in stack #
                for stack in targetStack:
                    cpuCnt = stack[cpuTickIndex]
                    subStack = list(stack[subStackIndex])

                    if cpuCnt == 0:
                        break

                    if len(subStack) == 0:
                        continue
                    else:
                        cpuPer = round(float(cpuCnt) / float(value['tickCnt']) * 100, 1)
                        if cpuPer < 1 and SystemManager.showAll is False:
                            break

                        # Make stack info by symbol for print #
                        symbolStack = ''
                        stackIdx = 0
                        indentLen = len("\t" * 4 * 4)
                        appliedIndentLen = indentLen

                        if self.sort is 'sym':
                            for sym in subStack:
                                if sym is None:
                                    symbolSet = ' <- None'
                                else:
                                    symbolSet = ' <- ' + sym + \
                                        ' [' + self.userSymData[sym]['origBin'] + ']'

                                lpos = appliedIndentLen + len(symbolStack[stackIdx:]) + len(symbolSet)
                                if lpos > SystemManager.lineLength:
                                    stackIdx = len(symbolStack)
                                    symbolStack += '\n' + ' ' * indentLen
                                    appliedIndentLen = 0

                                symbolStack += symbolSet
                        elif self.sort is 'pos':
                            for pos in subStack:
                                if pos is None:
                                    symbolStack += ' <- None'
                                # No symbol so that just print pos #
                                elif self.posData[pos]['symbol'] == '':
                                    symbolStack += ' <- ' + hex(int(pos, 16)) + \
                                        ' [' + self.posData[pos]['origBin'] + ']'
                                # Print symbol #
                                else:
                                    symbolStack += ' <- ' + self.posData[pos]['symbol'] + \
                                        ' [' + self.posData[pos]['origBin'] + ']'

                    SystemManager.pipePrint("\t +{0:7}% |{1:32}".format(cpuPer, symbolStack))

                SystemManager.pipePrint(oneLine)

            SystemManager.pipePrint('')

        # Print cpu usage in kernel space #
        SystemManager.clearPrint()
        SystemManager.pipePrint('[Function CPU Info] [Cnt: %d] [Interval: %dms] (KERNEL)' % \
            (self.periodicEventCnt, self.periodicEventInterval * 1000))

        SystemManager.pipePrint(twoLine)
        SystemManager.pipePrint("{0:_^9}|{1:_^144}".format("Usage", "Function"))
        SystemManager.pipePrint(twoLine)

        # Make exception list to remove a redundant part of stack #
        exceptList = {}
        if SystemManager.showAll is False:
            for pos, value in self.posData.items():
                if value['symbol'] == '__irq_usr' or \
                    value['symbol'] == '__irq_svc' or \
                    value['symbol'] == '__hrtimer_start_range_ns' or \
                    value['symbol'] == 'hrtimer_start_range_ns' or \
                    value['symbol'] == 'apic_timer_interrupt':
                    try:
                        exceptList[pos]
                    except:
                        exceptList[pos] = dict()

        # Print cpu usage of stacks #
        for idx, value in sorted(\
            self.kernelSymData.items(), key=lambda e: e[1]['tickCnt'], reverse=True):

            if value['tickCnt'] == 0:
                break

            cpuPer = round(float(value['tickCnt']) / float(self.periodicEventCnt) * 100, 1)
            if cpuPer < 1 and SystemManager.showAll is False:
                break

            SystemManager.pipePrint("{0:7}% |{1:^134}".format(cpuPer, idx))

            # Sort stacks by usage #
            value['stack'].sort(reverse=True)

            # Print stacks by symbol #
            for stack in value['stack']:
                cpuCnt = stack[cpuTickIndex]
                subStack = list(stack[subStackIndex])

                if cpuCnt == 0:
                    break
                else:
                    cpuPer = round(float(cpuCnt) / float(value['tickCnt']) * 100, 1)
                    if cpuPer < 1 and SystemManager.showAll is False:
                        break

                    # Remove a redundant part #
                    for pos, val in exceptList.items():
                        try:
                            del subStack[0:subStack.index(pos)+1]
                        except:
                            continue

                if len(subStack) == 0:
                    continue
                elif len(subStack) == 1 and SystemManager.showAll is False and \
                    (self.posData[subStack[0]]['symbol'] is None or \
                    self.posData[subStack[0]]['symbol'] == 'NoFile'):
                    # Pass unmeaningful part #
                    continue
                else:
                    # Make stack info by symbol for print #
                    symbolStack = ''
                    stackIdx = 0
                    indentLen = len("\t" * 4 * 4)
                    appliedIndentLen = indentLen

                    try:
                        for pos in subStack:
                            if self.posData[pos]['symbol'] == '':
                                symbolSet = ' <- ' + hex(int(pos, 16))
                            elif self.posData[pos]['symbol'] == None and SystemManager.showAll:
                                symbolSet = ' <- ' + hex(int(pos, 16))
                            else:
                                symbolSet = ' <- ' + str(self.posData[pos]['symbol'])

                            lpos = appliedIndentLen + len(symbolStack[stackIdx:]) + len(symbolSet)
                            if lpos > SystemManager.lineLength:
                                stackIdx = len(symbolStack)
                                symbolStack += '\n' + ' ' * indentLen
                                appliedIndentLen = 0

                            symbolStack += symbolSet
                    except:
                        continue

                SystemManager.pipePrint("\t +{0:7}% |{1:32}".format(cpuPer, symbolStack))

            SystemManager.pipePrint(oneLine)

        SystemManager.pipePrint('\n\n')



    def printUnknownMemFree(self):
        # check memory event #
        if self.memEnabled is False:
            return

        subStackIndex = FunctionAnalyzer.symStackIdxTable.index('STACK')
        pageFreeIndex = FunctionAnalyzer.symStackIdxTable.index('PAGE_FREE')

        if SystemManager.userEnable:
            # Print unknown memory free info in user space #
            SystemManager.clearPrint()
            SystemManager.pipePrint('[Function Unknown Memory Free Info] [Size: %dKB] (USER)' % \
                (self.pageUnknownFreeCnt * 4))

            SystemManager.pipePrint(twoLine)
            SystemManager.pipePrint("{0:_^9}|{1:_^47}|{2:_^48}|{3:_^47}".\
                format("Free", "Function", "Binary", "Source"))
            SystemManager.pipePrint(twoLine)

            for idx, value in sorted(\
                self.userSymData.items(), key=lambda e: e[1]['unknownPageFreeCnt'], reverse=True):
                if value['unknownPageFreeCnt'] == 0:
                    break

                SystemManager.pipePrint("{0:7}K |{1:^47}|{2:48}|{3:37}".\
                    format(int(value['unknownPageFreeCnt'] * 4), idx, \
                    self.posData[value['pos']]['origBin'], self.posData[value['pos']]['src']))

                # Set target stack #
                targetStack = []
                if self.sort is 'sym':
                    targetStack = value['symStack']
                elif self.sort is 'pos':
                    targetStack = value['stack']

                # Sort by usage #
                targetStack = sorted(targetStack, key=lambda x: x[pageFreeIndex], reverse=True)

                # Merge and Print symbols in stack #
                for stack in targetStack:
                    pageFreeCnt = stack[pageFreeIndex]
                    subStack = list(stack[subStackIndex])

                    if pageFreeCnt == 0:
                        break

                    if len(subStack) == 0:
                        continue
                    else:
                        # Make stack info by symbol for print #
                        symbolStack = ''
                        stackIdx = 0
                        indentLen = len("\t" * 4 * 4)
                        appliedIndentLen = indentLen

                        if self.sort is 'sym':
                            for sym in subStack:
                                if sym is None:
                                    symbolSet = ' <- None'
                                else:
                                    symbolSet = ' <- ' + sym + \
                                        ' [' + self.userSymData[sym]['origBin'] + ']'

                                lpos = appliedIndentLen + len(symbolStack[stackIdx:]) + len(symbolSet)
                                if lpos > SystemManager.lineLength:
                                    stackIdx = len(symbolStack)
                                    symbolStack += '\n' + ' ' * indentLen
                                    appliedIndentLen = 0

                                symbolStack += symbolSet
                        elif self.sort is 'pos':
                            for pos in subStack:
                                if pos is None:
                                    symbolStack += ' <- None'
                                # No symbol so that just print pos #
                                elif self.posData[pos]['symbol'] == '':
                                    symbolStack += ' <- ' + hex(int(pos, 16)) + \
                                        ' [' + self.posData[pos]['origBin'] + ']'
                                # Print symbol #
                                else:
                                    symbolStack += ' <- ' + self.posData[pos]['symbol'] + \
                                        ' [' + self.posData[pos]['origBin'] + ']'

                    SystemManager.pipePrint("\t+ {0:7}K |{1:32}".\
                        format(int(pageFreeCnt * 4), symbolStack))

                SystemManager.pipePrint(oneLine)

            SystemManager.pipePrint('')

        # Print unknown memory free info in kernel space #
        SystemManager.clearPrint()
        SystemManager.pipePrint('[Function Unknown Memory Free Info] [Size: %dKB] (KERNEL)' % \
            (self.pageUnknownFreeCnt * 4))

        SystemManager.pipePrint(twoLine)
        SystemManager.pipePrint("{0:_^9}|{1:_^47}|{2:_^48}|{3:_^47}".\
            format("FREE", "Function", "Binary", "Source"))
        SystemManager.pipePrint(twoLine)

        # Make exception list to remove a redundant part of stack #
        '''
        exceptList = {}
        for pos, value in self.posData.items():
            if value['symbol'] == 'None':
                try:
                    exceptList[pos]
                except:
                    exceptList[pos] = dict()
        '''

        # Print block write usage of stacks #
        for idx, value in sorted(\
            self.kernelSymData.items(), key=lambda e: e[1]['unknownPageFreeCnt'], reverse=True):

            if value['unknownPageFreeCnt'] == 0:
                break

            SystemManager.pipePrint("{0:7}K |{1:^47}|{2:48}|{3:37}".\
                format(int(value['unknownPageFreeCnt'] * 4), idx, '', ''))

            # Sort stacks by usage #
            value['stack'] = \
                sorted(value['stack'], key=lambda x: x[pageFreeIndex], reverse=True)

            # Print stacks by symbol #
            for stack in value['stack']:
                pageFreeCnt = stack[pageFreeIndex]
                subStack = list(stack[subStackIndex])

                if pageFreeCnt == 0:
                    continue

                if len(subStack) == 0:
                    symbolStack = '\tNone'
                else:
                    # Make stack info by symbol for print #
                    symbolStack = ''
                    stackIdx = 0
                    indentLen = len("\t" * 4 * 4)
                    appliedIndentLen = indentLen

                    try:
                        for pos in subStack:
                            if self.posData[pos]['symbol'] == '':
                                symbolSet = ' <- ' + hex(int(pos, 16))
                            elif self.posData[pos]['symbol'] == None and SystemManager.showAll:
                                symbolSet = ' <- ' + hex(int(pos, 16))
                            else:
                                symbolSet = ' <- ' + str(self.posData[pos]['symbol'])

                            lpos = appliedIndentLen + len(symbolStack[stackIdx:]) + len(symbolSet)
                            if lpos > SystemManager.lineLength:
                                stackIdx = len(symbolStack)
                                symbolStack += '\n' + ' ' * indentLen
                                appliedIndentLen = 0

                            symbolStack += symbolSet
                    except:
                        continue

                SystemManager.pipePrint("\t+ {0:7}K |{1:32}".\
                    format(int(pageFreeCnt * 4), symbolStack))

            SystemManager.pipePrint(oneLine)

        SystemManager.pipePrint('\n\n')



    def printMemUsage(self):
        # check memory event #
        if self.memEnabled is False:
            return

        subStackIndex = FunctionAnalyzer.symStackIdxTable.index('STACK')
        pageAllocIndex = FunctionAnalyzer.symStackIdxTable.index('PAGE_ALLOC')
        argIndex = FunctionAnalyzer.symStackIdxTable.index('ARGUMENT')

        if SystemManager.userEnable:
            # Print mem usage in user space #
            SystemManager.clearPrint()
            SystemManager.pipePrint(\
                '[Function Memory Info] [Total: %dKB] [Alloc: %dKB(%d)] [Free: %dKB(%d)] (USER)' % \
                (self.pageUsageCnt * 4, self.pageAllocCnt * 4, self.pageAllocEventCnt, \
                self.pageFreeCnt * 4, self.pageFreeEventCnt))

            SystemManager.pipePrint(twoLine)
            SystemManager.pipePrint("{0:^7}({1:^6}/{2:^6}/{3:^6})|{4:_^47}|{5:_^48}|{6:_^27}".\
                format("Usage", "Usr", "Buf", "Ker", "Function", "Binary", "Source"))
            SystemManager.pipePrint(twoLine)

            for idx, value in sorted(\
                self.userSymData.items(), key=lambda e: e[1]['pageCnt'], reverse=True):

                if value['pageCnt'] == 0:
                    break

                SystemManager.pipePrint(\
                    "{0:6}K({1:6}/{2:6}/{3:6})|{4:^47}|{5:48}|{6:27}".\
                    format(value['pageCnt'] * 4, value['userPageCnt'] * 4, \
                    value['cachePageCnt'] * 4, value['kernelPageCnt'] * 4, idx, \
                    self.posData[value['pos']]['origBin'], self.posData[value['pos']]['src']))

                # Set target stack #
                targetStack = []
                if self.sort is 'sym':
                    targetStack = value['symStack']
                elif self.sort is 'pos':
                    targetStack = value['stack']

                # Sort by usage #
                targetStack = sorted(targetStack, key=lambda x: x[pageAllocIndex], reverse=True)

                # Merge and Print symbols in stack #
                for stack in targetStack:
                    subStack = list(stack[subStackIndex])
                    pageCnt = stack[pageAllocIndex]
                    userPageCnt = stack[argIndex][0]
                    cachePageCnt = stack[argIndex][1]
                    kernelPageCnt = stack[argIndex][2]

                    if pageCnt == 0:
                        break

                    if len(subStack) == 0:
                        continue
                    else:
                        # Make stack info by symbol for print #
                        symbolStack = ''
                        stackIdx = 0
                        indentLen = len("\t" * 4 * 9)
                        appliedIndentLen = indentLen

                        if self.sort is 'sym':
                            for sym in subStack:
                                if sym is None:
                                    symbolSet = ' <- None'
                                else:
                                    symbolSet = ' <- ' + sym + \
                                        ' [' + self.userSymData[sym]['origBin'] + ']'

                                lpos = appliedIndentLen + len(symbolStack[stackIdx:]) + len(symbolSet)
                                if lpos > SystemManager.lineLength:
                                    stackIdx = len(symbolStack)
                                    symbolStack += '\n' + ' ' * indentLen
                                    appliedIndentLen = 0

                                symbolStack += symbolSet
                        elif self.sort is 'pos':
                            for pos in subStack:
                                if pos is None:
                                    symbolStack += ' <- None'
                                # No symbol so that just print pos #
                                elif self.posData[pos]['symbol'] == '':
                                    symbolStack += ' <- ' + hex(int(pos, 16)) + \
                                        ' [' + self.posData[pos]['origBin'] + ']'
                                # Print symbol #
                                else:
                                    symbolStack += ' <- ' + self.posData[pos]['symbol'] + \
                                        ' [' + self.posData[pos]['origBin'] + ']'

                    SystemManager.pipePrint("\t+ {0:6}K({1:6}/{2:6}/{3:6})|{4:32}".\
                        format(pageCnt * 4, userPageCnt * 4, \
                        cachePageCnt * 4, kernelPageCnt * 4, symbolStack))

                SystemManager.pipePrint(oneLine)

            SystemManager.pipePrint('')

        # Print mem usage in kernel space #
        SystemManager.clearPrint()
        SystemManager.pipePrint(\
            '[Function Memory Info] [Total: %dKB] [Alloc: %dKB(%d)] [Free: %dKB(%d)] (KERNEL)' % \
            (self.pageUsageCnt * 4, self.pageAllocCnt * 4, self.pageAllocEventCnt, \
            self.pageFreeCnt * 4, self.pageFreeEventCnt))

        SystemManager.pipePrint(twoLine)
        SystemManager.pipePrint("{0:^7}({1:^6}/{2:^6}/{3:^6})|{4:_^124}".\
            format("Usage", "Usr", "Buf", "Ker", "Function"))
        SystemManager.pipePrint(twoLine)

        # Make exception list to remove a redundant part of stack #
        '''
        exceptList = {}
        for pos, value in self.posData.items():
            if value['symbol'] == 'None':
                try:
                    exceptList[pos]
                except:
                    exceptList[pos] = dict()
        '''

        # Print mem usage of stacks #
        for idx, value in sorted(\
            self.kernelSymData.items(), key=lambda e: e[1]['pageCnt'], reverse=True):

            if value['pageCnt'] == 0:
                break

            SystemManager.pipePrint(\
                "{0:6}K({1:6}/{2:6}/{3:6})|{4:^32}".format(value['pageCnt'] * 4, \
                value['userPageCnt'] * 4, value['cachePageCnt'] * 4, value['kernelPageCnt'] * 4, idx))

            # Sort stacks by usage #
            value['stack'] = sorted(value['stack'], key=lambda x: x[pageAllocIndex], reverse=True)

            # Print stacks by symbol #
            for stack in value['stack']:
                subStack = list(stack[subStackIndex])
                pageCnt = stack[pageAllocIndex]
                userPageCnt = stack[argIndex][0]
                cachePageCnt = stack[argIndex][1]
                kernelPageCnt = stack[argIndex][2]

                if pageCnt == 0:
                    continue

                if len(subStack) == 0:
                    continue
                else:
                    # Make stack info by symbol for print #
                    symbolStack = ''
                    stackIdx = 0
                    indentLen = len("\t" * 4 * 9)
                    appliedIndentLen = indentLen

                    try:
                        for pos in subStack:
                            if self.posData[pos]['symbol'] == '':
                                symbolSet = ' <- ' + hex(int(pos, 16))
                            elif self.posData[pos]['symbol'] == None and SystemManager.showAll:
                                symbolSet = ' <- ' + hex(int(pos, 16))
                            else:
                                symbolSet = ' <- ' + str(self.posData[pos]['symbol'])

                            lpos = appliedIndentLen + len(symbolStack[stackIdx:]) + len(symbolSet)
                            if lpos > SystemManager.lineLength:
                                stackIdx = len(symbolStack)
                                symbolStack += '\n' + ' ' * indentLen
                                appliedIndentLen = 0

                            symbolStack += symbolSet
                    except:
                        continue

                SystemManager.pipePrint("\t+ {0:6}K({1:6}/{2:6}/{3:6})|{4:32}".format(pageCnt * 4, \
                    userPageCnt * 4, cachePageCnt * 4, kernelPageCnt * 4, symbolStack))

            SystemManager.pipePrint(oneLine)

        SystemManager.pipePrint('')

        self.printUnknownMemFree()



    def printHeapUsage(self):
        # check heap memory event #
        if self.heapEnabled is False or SystemManager.userEnable is False:
            return

        subStackIndex = FunctionAnalyzer.symStackIdxTable.index('STACK')
        heapExpIndex = FunctionAnalyzer.symStackIdxTable.index('HEAP_EXPAND')

        # Print heap usage in user space #
        SystemManager.clearPrint()
        SystemManager.pipePrint(\
            '[Function Heap Info] [Total: %dKB] [Alloc: %dKB(%d)] [Free: %dKB(%d)] (USER)' % \
            ((self.heapExpSize - self.heapRedSize) >> 10, \
            self.heapExpSize >> 10, self.heapExpEventCnt, \
            self.heapRedSize >> 10, self.heapRedEventCnt))

        SystemManager.pipePrint(twoLine)
        SystemManager.pipePrint("{0:_^9}|{1:_^47}|{2:_^48}|{3:_^47}".\
            format("Usage", "Function", "Binary", "Source"))
        SystemManager.pipePrint(twoLine)

        for idx, value in sorted(\
            self.userSymData.items(), key=lambda e: e[1]['heapSize'], reverse=True):

            if value['heapSize'] == 0:
                break

            SystemManager.pipePrint("{0:7}K |{1:^47}|{2:48}|{3:37}".\
                format(int(value['heapSize'] >> 10), idx, \
                self.posData[value['pos']]['origBin'], self.posData[value['pos']]['src']))

            if idx == value['pos']:
                SystemManager.pipePrint(oneLine)
                continue

            # Set target stack #
            targetStack = []
            if self.sort is 'sym':
                targetStack = value['symStack']
            elif self.sort is 'pos':
                targetStack = value['stack']

            # Sort by usage #
            targetStack = sorted(targetStack, key=lambda x: x[heapExpIndex], reverse=True)

            # Merge and Print symbols in stack #
            for stack in targetStack:
                heapSize = stack[heapExpIndex]
                subStack = list(stack[subStackIndex])

                if heapSize == 0:
                    break

                if len(subStack) == 0:
                    continue
                else:
                    # Make stack info by symbol for print #
                    symbolStack = ''
                    stackIdx = 0
                    indentLen = len("\t" * 4 * 4)
                    appliedIndentLen = indentLen

                    if self.sort is 'sym':
                        for sym in subStack:
                            if sym is None:
                                symbolSet = ' <- None'
                            else:
                                symbolSet = ' <- ' + sym + \
                                    ' [' + self.userSymData[sym]['origBin'] + ']'

                            lpos = appliedIndentLen + len(symbolStack[stackIdx:]) + len(symbolSet)
                            if lpos > SystemManager.lineLength:
                                stackIdx = len(symbolStack)
                                symbolStack += '\n' + ' ' * indentLen
                                appliedIndentLen = 0

                            symbolStack += symbolSet
                    elif self.sort is 'pos':
                        for pos in subStack:
                            if pos is None:
                                symbolStack += ' <- None'
                            # No symbol so that just print pos #
                            elif self.posData[pos]['symbol'] == '':
                                symbolStack += ' <- ' + hex(int(pos, 16)) + \
                                    ' [' + self.posData[pos]['origBin'] + ']'
                            # Print symbol #
                            else:
                                symbolStack += ' <- ' + self.posData[pos]['symbol'] + \
                                    ' [' + self.posData[pos]['origBin'] + ']'

                SystemManager.pipePrint("\t+ {0:7}K |{1:32}".\
                    format(int(heapSize/ 1024), symbolStack))

            SystemManager.pipePrint(oneLine)

        SystemManager.pipePrint('\n\n')



    def printBlockWrUsage(self):
        # no block event #
        if self.bwriteEnabled is False:
            return

        subStackIndex = FunctionAnalyzer.symStackIdxTable.index('STACK')
        blkWrIndex = FunctionAnalyzer.symStackIdxTable.index('BLK_WRITE')

        if SystemManager.userEnable:
            # Print block write usage in user space #
            SystemManager.clearPrint()
            SystemManager.pipePrint('[Function BLK_WR Info] [Size: %dKB] [Cnt: %d] (USER)' % \
                (self.blockWrUsageCnt * 4, self.blockWrEventCnt))

            SystemManager.pipePrint(twoLine)
            SystemManager.pipePrint("{0:_^9}|{1:_^47}|{2:_^48}|{3:_^47}".\
                format("Usage", "Function", "Binary", "Source"))
            SystemManager.pipePrint(twoLine)

            for idx, value in sorted(\
                self.userSymData.items(), key=lambda e: e[1]['blockWrCnt'], reverse=True):

                if value['blockWrCnt'] == 0:
                    break

                SystemManager.pipePrint("{0:7}K |{1:^47}|{2:48}|{3:37}".\
                    format(int(value['blockWrCnt'] * 4), idx, \
                    self.posData[value['pos']]['origBin'], self.posData[value['pos']]['src']))

                # Set target stack #
                targetStack = []
                if self.sort is 'sym':
                    targetStack = value['symStack']
                elif self.sort is 'pos':
                    targetStack = value['stack']

                # Sort by usage #
                targetStack = sorted(targetStack, key=lambda x: x[blkWrIndex], reverse=True)

                # Merge and Print symbols in stack #
                for stack in targetStack:
                    blockWrCnt = stack[blkWrIndex]
                    subStack = list(stack[subStackIndex])

                    if blockWrCnt == 0:
                        break

                    if len(subStack) == 0:
                        continue
                    else:
                        # Make stack info by symbol for print #
                        symbolStack = ''
                        stackIdx = 0
                        indentLen = len("\t" * 4 * 4)
                        appliedIndentLen = indentLen

                        if self.sort is 'sym':
                            for sym in subStack:
                                if sym is None:
                                    symbolSet = ' <- None'
                                else:
                                    symbolSet = ' <- ' + sym + \
                                        ' [' + self.userSymData[sym]['origBin'] + ']'

                                lpos = appliedIndentLen + len(symbolStack[stackIdx:]) + len(symbolSet)
                                if lpos > SystemManager.lineLength:
                                    stackIdx = len(symbolStack)
                                    symbolStack += '\n' + ' ' * indentLen
                                    appliedIndentLen = 0

                                symbolStack += symbolSet
                        elif self.sort is 'pos':
                            for pos in subStack:
                                if pos is None:
                                    symbolStack += ' <- None'
                                # No symbol so that just print pos #
                                elif self.posData[pos]['symbol'] == '':
                                    symbolStack += ' <- ' + hex(int(pos, 16)) + \
                                        ' [' + self.posData[pos]['origBin'] + ']'
                                # Print symbol #
                                else:
                                    symbolStack += ' <- ' + self.posData[pos]['symbol'] + \
                                        ' [' + self.posData[pos]['origBin'] + ']'

                    SystemManager.pipePrint("\t+ {0:7}K |{1:32}".\
                        format(int(blockWrCnt * 4), symbolStack))

                SystemManager.pipePrint(oneLine)

            SystemManager.pipePrint('')

        # Print block write usage in kernel space #
        SystemManager.clearPrint()
        SystemManager.pipePrint('[Function BLK_WR Info] [Size: %dKB] [Cnt: %d] (KERNEL)' % \
            (self.blockWrUsageCnt * 4, self.blockWrEventCnt))

        SystemManager.pipePrint(twoLine)
        SystemManager.pipePrint("{0:_^9}|{1:_^47}|{2:_^48}|{3:_^47}".\
            format("Usage", "Function", "Binary", "Source"))
        SystemManager.pipePrint(twoLine)

        # Make exception list to remove a redundant part of stack #
        '''
        exceptList = {}
        for pos, value in self.posData.items():
            if value['symbol'] == 'None':
                try:
                    exceptList[pos]
                except:
                    exceptList[pos] = dict()
        '''

        # Print block write usage of stacks #
        for idx, value in sorted(\
            self.kernelSymData.items(), key=lambda e: e[1]['blockWrCnt'], reverse=True):

            if value['blockWrCnt'] == 0:
                break

            SystemManager.pipePrint("{0:7}K |{1:^47}|{2:48}|{3:37}".\
                format(int(value['blockWrCnt'] * 4), idx, '', ''))

            # Sort stacks by usage #
            value['stack'] = sorted(value['stack'], key=lambda x: x[blkWrIndex], reverse=True)

            # Print stacks by symbol #
            for stack in value['stack']:
                blockWrCnt = stack[blkWrIndex]
                subStack = list(stack[subStackIndex])

                if blockWrCnt == 0:
                    continue

                if len(subStack) == 0:
                    symbolStack = '\tNone'
                else:
                    # Make stack info by symbol for print #
                    symbolStack = ''
                    stackIdx = 0
                    indentLen = len("\t" * 4 * 4)
                    appliedIndentLen = indentLen

                    try:
                        for pos in subStack:
                            if self.posData[pos]['symbol'] == '':
                                symbolSet = ' <- ' + hex(int(pos, 16))
                            elif self.posData[pos]['symbol'] == None and SystemManager.showAll:
                                symbolSet = ' <- ' + hex(int(pos, 16))
                            else:
                                symbolSet = ' <- ' + str(self.posData[pos]['symbol'])

                            lpos = appliedIndentLen + len(symbolStack[stackIdx:]) + len(symbolSet)
                            if lpos > SystemManager.lineLength:
                                stackIdx = len(symbolStack)
                                symbolStack += '\n' + ' ' * indentLen
                                appliedIndentLen = 0

                            symbolStack += symbolSet
                    except:
                        continue

                SystemManager.pipePrint("\t+ {0:7}K |{1:32}".\
                    format(int(blockWrCnt * 4), symbolStack))

            SystemManager.pipePrint(oneLine)

        SystemManager.pipePrint('\n\n')



    def printBlockRdUsage(self):
        # no block event #
        if self.breadEnabled is False:
            return

        subStackIndex = FunctionAnalyzer.symStackIdxTable.index('STACK')
        blkRdIndex = FunctionAnalyzer.symStackIdxTable.index('BLK_READ')

        if SystemManager.userEnable:
            # Print block read usage in user space #
            SystemManager.clearPrint()
            SystemManager.pipePrint('[Function BLK_RD Info] [Size: %dKB] [Cnt: %d] (USER)' % \
                (self.blockRdUsageCnt * 0.5, self.blockRdEventCnt))

            SystemManager.pipePrint(twoLine)
            SystemManager.pipePrint("{0:_^9}|{1:_^47}|{2:_^48}|{3:_^47}".\
                format("Usage", "Function", "Binary", "Source"))
            SystemManager.pipePrint(twoLine)

            for idx, value in sorted(\
                self.userSymData.items(), key=lambda e: e[1]['blockRdCnt'], reverse=True):

                if value['blockRdCnt'] == 0:
                    break

                SystemManager.pipePrint("{0:7}K |{1:^47}|{2:48}|{3:37}".\
                    format(int(value['blockRdCnt'] * 0.5), idx, \
                    self.posData[value['pos']]['origBin'], self.posData[value['pos']]['src']))

                # Set target stack #
                targetStack = []
                if self.sort is 'sym':
                    targetStack = value['symStack']
                elif self.sort is 'pos':
                    targetStack = value['stack']

                # Sort by usage #
                targetStack = sorted(targetStack, key=lambda x: x[blkRdIndex], reverse=True)

                # Merge and Print symbols in stack #
                for stack in targetStack:
                    blockRdCnt = stack[blkRdIndex]
                    subStack = list(stack[subStackIndex])

                    if blockRdCnt == 0:
                        break

                    if len(subStack) == 0:
                        continue
                    else:
                        # Make stack info by symbol for print #
                        symbolStack = ''
                        stackIdx = 0
                        indentLen = len("\t" * 4 * 4)
                        appliedIndentLen = indentLen

                        if self.sort is 'sym':
                            for sym in subStack:
                                if sym is None:
                                    symbolSet = ' <- None'
                                else:
                                    symbolSet = ' <- ' + sym + \
                                        ' [' + self.userSymData[sym]['origBin'] + ']'

                                lpos = appliedIndentLen + len(symbolStack[stackIdx:]) + len(symbolSet)
                                if lpos > SystemManager.lineLength:
                                    stackIdx = len(symbolStack)
                                    symbolStack += '\n' + ' ' * indentLen
                                    appliedIndentLen = 0

                                symbolStack += symbolSet
                        elif self.sort is 'pos':
                            for pos in subStack:
                                if pos is None:
                                    symbolStack += ' <- None'
                                # No symbol so that just print pos #
                                elif self.posData[pos]['symbol'] == '':
                                    symbolStack += ' <- ' + hex(int(pos, 16)) + \
                                        ' [' + self.posData[pos]['origBin'] + ']'
                                # Print symbol #
                                else:
                                    symbolStack += ' <- ' + self.posData[pos]['symbol'] + \
                                        ' [' + self.posData[pos]['origBin'] + ']'

                    SystemManager.pipePrint("\t+ {0:7}K |{1:32}".\
                        format(int(blockRdCnt * 0.5), symbolStack))

                SystemManager.pipePrint(oneLine)

            SystemManager.pipePrint('')

        # Print block read usage in kernel space #
        SystemManager.clearPrint()
        SystemManager.pipePrint('[Function BLK_RD Info] [Size: %dKB] [Cnt: %d] (KERNEL)' % \
            (self.blockRdUsageCnt * 0.5, self.blockRdEventCnt))

        SystemManager.pipePrint(twoLine)
        SystemManager.pipePrint("{0:_^9}|{1:_^47}|{2:_^48}|{3:_^47}".\
            format("Usage", "Function", "Binary", "Source"))
        SystemManager.pipePrint(twoLine)

        # Make exception list to remove a redundant part of stack #
        '''
        exceptList = {}
        for pos, value in self.posData.items():
            if value['symbol'] == 'None':
                try:
                    exceptList[pos]
                except:
                    exceptList[pos] = dict()
        '''

        # Print block read usage of stacks #
        for idx, value in sorted(\
            self.kernelSymData.items(), key=lambda e: e[1]['blockRdCnt'], reverse=True):

            if value['blockRdCnt'] == 0:
                break

            SystemManager.pipePrint("{0:7}K |{1:^47}|{2:48}|{3:37}".\
                format(int(value['blockRdCnt'] * 0.5), idx, '', ''))

            # Sort stacks by usage #
            value['stack'] = sorted(value['stack'], key=lambda x: x[blkRdIndex], reverse=True)

            # Print stacks by symbol #
            for stack in value['stack']:
                blockRdCnt = stack[blkRdIndex]
                subStack = list(stack[subStackIndex])

                if blockRdCnt == 0:
                    continue

                if len(subStack) == 0:
                    symbolStack = '\tNone'
                else:
                    # Make stack info by symbol for print #
                    symbolStack = ''
                    stackIdx = 0
                    indentLen = len("\t" * 4 * 4)
                    appliedIndentLen = indentLen

                    try:
                        for pos in subStack:
                            if self.posData[pos]['symbol'] == '':
                                symbolSet = ' <- ' + hex(int(pos, 16))
                            elif self.posData[pos]['symbol'] == None and SystemManager.showAll:
                                symbolSet = ' <- ' + hex(int(pos, 16))
                            else:
                                symbolSet = ' <- ' + str(self.posData[pos]['symbol'])

                            lpos = appliedIndentLen + len(symbolStack[stackIdx:]) + len(symbolSet)
                            if lpos > SystemManager.lineLength:
                                stackIdx = len(symbolStack)
                                symbolStack += '\n' + ' ' * indentLen
                                appliedIndentLen = 0

                            symbolStack += symbolSet
                    except:
                        continue

                SystemManager.pipePrint("\t+ {0:7}K |{1:32}".\
                    format(int(blockRdCnt * 0.5), symbolStack))

            SystemManager.pipePrint(oneLine)

        SystemManager.pipePrint('\n\n')





class FileAnalyzer(object):
    """ Analyzer for file profiling """

    def __init__(self):
        self.libguider = None
        self.libguiderPath = 'libguider.so'

        self.startTime = None
        self.profSuccessCnt = 0
        self.profFailedCnt = 0
        self.profPageCnt = 0
        self.procData = {}
        self.fileData = {}
        self.inodeData = {}

        self.procList = {}
        self.fileList = {}

        self.intervalProcData = []
        self.intervalFileData = []

        self.init_procData = {'tids': None, 'pageCnt': int(0), 'procMap': None, 'comm': ''}
        self.init_threadData = {'comm': ''}
        self.init_inodeData = {}
        self.init_mapData = {'offset': int(0), 'size': int(0), 'pageCnt': int(0), 'fd': None, \
            'totalSize': int(0), 'fileMap': None, 'pids': None, 'linkCnt': int(0), 'inode': None, \
            'accessTime': None, 'devid': None, 'isRep': True, 'repFile': None, 'hardLink': int(1), \
            'linkList': None}

        try:
            import ctypes
            from ctypes import cdll, POINTER
        except ImportError:
            err = sys.exc_info()[1]
            SystemManager.printError("Fail to import package: " + err.args[0])
            sys.exit(0)

        # handle no target case #
        if len(SystemManager.showGroup) == 0:
            SystemManager.showGroup.insert(0, '')

        try:
            imp.find_module('ctypes')
        except:
            SystemManager.printError('Fail to find ctypes package')
            sys.exit(0)

        try:
            # load the library #
            self.libguider = cdll.LoadLibrary(self.libguiderPath)
        except:
            try:
                self.libguider = cdll.LoadLibrary('./%s' % self.libguiderPath)
            except:
                SystemManager.printError(\
                    'Fail to open %s, set LD_LIBRARY_PATH to use %s' % \
                    (self.libguiderPath, self.libguiderPath))
                sys.exit(0)

        # set the argument type #
        self.libguider.get_filePageMap.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
        # set the return type #
        self.libguider.get_filePageMap.restype = POINTER(ctypes.c_ubyte)

        try:
            import resource
            SystemManager.maxFd = resource.getrlimit(getattr(resource, 'RLIMIT_NOFILE'))[0]
        except:
            SystemManager.printWarning(\
                "Fail to get maxFd because of no resource package, use %d as default value" % \
                SystemManager.maxFd)

        self.startTime = time.time()

        while 1:
            # scan proc directory and save map information of processes #
            self.scanProcs()

            # merge maps of processes into a integrated file map #
            self.mergeFileMapInfo()

            # get file map info on memory #
            self.getFilePageMaps()

            # fill file map of each processes #
            self.fillFileMaps()

            if SystemManager.intervalEnable > 0:
                # save previous file usage and initialize all variables #
                self.intervalProcData.append(self.procData)
                self.intervalFileData.append(self.fileData)
                self.procData = {}
                self.fileData = {}
                self.inodeData = {}
                self.profSuccessCnt = 0
                self.profFailedCnt = 0

                # check exit condition for interval profile #
                if SystemManager.condExit is False:
                    signal.pause()
                else:
                    break
            else:
                break



    def __del__(self):
        pass



    def printUsage(self):
        if len(self.procData) == 0:
            SystemManager.printError('No process profiled')
            sys.exit(0)
        if len(self.fileData) == 0:
            SystemManager.printError('No file profiled')
            sys.exit(0)

        SystemManager.printTitle()

        # print system information #
        SystemManager.printInfoBuffer()

        # Print proccess list #
        SystemManager.pipePrint(\
            "[%s] [ Process : %d ] [ RAM: %d(KB) ][ Keys: Foward/Back/Save/Quit ] [ Capture: Ctrl+\\ ]" % \
            ('File Process Info', len(self.procData), self.profPageCnt * 4))
        SystemManager.pipePrint(twoLine)
        SystemManager.pipePrint("{0:_^16}({1:_^5})|{2:_^9}|{3:_^16}({4:_^5}) |".\
            format("Process", "Pid", "RAM(KB)", "Thread", "Tid"))
        SystemManager.pipePrint(twoLine)

        procInfo = "{0:^16}({0:^5})|{1:8} |".format('', '', '')
        threadInfo = " {0:^16}({1:^5}) |".format('', '')
        procLength = len(procInfo)
        threadLength = len(threadInfo)
        lineLength = SystemManager.lineLength

        for pid, val in sorted(self.procData.items(), key=lambda e: int(e[1]['pageCnt']), reverse=True):
            printMsg = "{0:>16}({1:>5})|{2:>8} |".\
                format(val['comm'], pid, val['pageCnt'] * SystemManager.pageSize >> 10)
            linePos = len(printMsg)

            for tid, threadVal in sorted(val['tids'].items(), reverse=True):
                threadInfo = "{0:^16}({1:^5}) |".format(threadVal['comm'], tid)

                linePos += threadLength

                if linePos > lineLength:
                    linePos = procLength + threadLength
                    printMsg += "\n" + (' ' * (procLength - 1)) + '|'

                printMsg += threadInfo

            SystemManager.pipePrint(printMsg)

        SystemManager.pipePrint(oneLine + '\n')

        # Print file list #
        SystemManager.pipePrint(\
            "[%s] [ File: %d ] [ RAM: %d(KB) ] [ Keys: Foward/Back/Save/Quit ]" % \
            ('File Usage Info', len(self.fileData), self.profPageCnt * 4))
        SystemManager.pipePrint(twoLine)
        SystemManager.pipePrint("{0:_^12}|{1:_^10}|{2:_^6}|{3:_^123}".\
            format("RAM(KB)", "File(KB)", "%", "Library & Process"))
        SystemManager.pipePrint(twoLine)

        for fileName, val in sorted(\
            self.fileData.items(), key=lambda e: int(e[1]['pageCnt']), reverse=True):
            memSize = val['pageCnt'] * SystemManager.pageSize >> 10
            fileSize = ((val['totalSize'] + SystemManager.pageSize - 1) / \
                SystemManager.pageSize) * SystemManager.pageSize >> 10

            if fileSize != 0:
                per = int(int(memSize) / float(fileSize) * 100)
            else:
                per = 0

            if val['isRep'] is False:
                continue
            else:
                SystemManager.pipePrint("{0:>11} |{1:>9} |{2:>5} | {3:1} [Proc: {4:1}] [Link: {5:1}]".\
                    format(memSize, fileSize, per, fileName, len(val['pids']), val['hardLink']))

            # prepare for printing process list #
            pidInfo = ''
            lineLength = SystemManager.lineLength
            pidLength = len(" %16s (%5s) |" % ('', ''))
            indentLength = len("{0:>11} |{1:>9} |{2:>5} ".format('','',''))
            linePos = indentLength + pidLength

            # print hard-linked list #
            if val['hardLink'] > 1:
                for fileLink, tmpVal in val['linkList'].items():
                    if fileName != fileLink:
                        SystemManager.pipePrint((' ' * indentLength) + '| -> ' + fileLink)

            # print process list #
            for pid, comm in val['pids'].items():
                if linePos > lineLength:
                    linePos = indentLength + pidLength
                    pidInfo += '\n' + (' ' * indentLength) + '|'

                pidInfo += " %16s (%5s) |" % (comm, pid)

                linePos += pidLength

            SystemManager.pipePrint((' ' * indentLength) + '|' + pidInfo)
            SystemManager.pipePrint(oneLine)

        SystemManager.pipePrint('\n\n\n')



    def printIntervalInfo(self):
        # Merge proccess info into a global list #
        for procData in self.intervalProcData:
            for pid, procInfo in procData.items():
                try:
                    if self.procList[pid]['pageCnt'] < procInfo['pageCnt']:
                        self.procList[pid]['pageCnt'] = procInfo['pageCnt']
                except:
                    self.procList[pid] = dict(self.init_procData)
                    self.procList[pid]['tids'] = {}
                    self.procList[pid]['pageCnt'] = procInfo['pageCnt']
                    self.procList[pid]['comm'] = procInfo['comm']

                for tid, val in procInfo['tids'].items():
                    try:
                        self.procList[pid]['tids'][tid]
                    except:
                        self.procList[pid]['tids'][tid] = dict(self.init_threadData)
                        self.procList[pid]['tids'][tid]['comm'] = val['comm']

        if len(self.procList) == 0:
            SystemManager.printError('No process profiled')
            sys.exit(0)

        # Merge file info into a global list #
        for fileData in self.intervalFileData:
            for fileName, fileStat in fileData.items():
                try:
                    if self.fileList[fileName]['pageCnt'] < fileStat['pageCnt']:
                        self.fileList[fileName]['pageCnt'] = fileStat['pageCnt']
                except:
                    self.fileList[fileName] = dict(self.init_mapData)
                    self.fileList[fileName]['pageCnt'] = fileStat['pageCnt']
                    self.fileList[fileName]['totalSize'] = fileStat['totalSize']

        if len(self.fileList) == 0:
            SystemManager.printError('No file profiled')
            sys.exit(0)

        SystemManager.printTitle()

        # Print system information #
        SystemManager.printInfoBuffer()

        # Print proccess list #
        SystemManager.pipePrint(\
            "[%s] [ Process : %d ] [ LastRAM: %d(KB) ][ Keys: Foward/Back/Save/Quit ] [ Capture: Ctrl+\\ ]" % \
            ('File Process Info', len(self.procList), self.profPageCnt * 4))
        SystemManager.pipePrint(twoLine)
        SystemManager.pipePrint("{0:_^16}({1:_^5})|{2:_^12}|{3:_^16}({4:_^5}) |".\
            format("Process", "Pid", "MaxRAM(KB)", "ThreadName", "Tid"))
        SystemManager.pipePrint(twoLine)

        procInfo = "{0:_^16}({1:^5})|{2:11} |".format('', '', '')
        threadInfo = " {0:^16}({1:^5}) |".format('', '')
        procLength = len(procInfo)
        threadLength = len(threadInfo)
        lineLength = SystemManager.lineLength

        for pid, val in sorted(self.procList.items(), key=lambda e: int(e[1]['pageCnt']), reverse=True):
            printMsg = "{0:>16}({1:>5})|{2:>11} |".\
                format(val['comm'], pid, val['pageCnt'] * SystemManager.pageSize >> 10)
            linePos = len(printMsg)

            for tid, threadVal in sorted(val['tids'].items(), reverse=True):
                threadInfo = "{0:>16}({1:>5}) |".format(threadVal['comm'], tid)

                linePos += threadLength

                if linePos > lineLength:
                    linePos = procLength + threadLength
                    printMsg += "\n" + (' ' * (procLength - 1)) + '|'

                printMsg += threadInfo

            SystemManager.pipePrint(printMsg)

        SystemManager.pipePrint(oneLine + '\n')

        # Print file list #
        SystemManager.pipePrint(\
            "[%s] [ File: %d ] [ LastRAM: %d(KB) ] [ Keys: Foward/Back/Save/Quit ]" % \
            ('File Usage Info', len(self.fileList), self.profPageCnt * 4))
        SystemManager.pipePrint(twoLine)

        printMsg = "{0:_^11}|{1:_^8}|{2:_^3}|".format("InitRAM(KB)", "File(KB)", "%")

        if len(self.intervalFileData) > 1:
            for idx in xrange(1, len(self.intervalFileData)):
                printMsg += "{0:_^15}|".format(str(idx))

        printMsg += "{0:_^11}|{1:_^3}|".format("LastRAM(KB)", "%")

        lineLength = SystemManager.lineLength

        printMsg += '_' * ((lineLength - len(printMsg)) / 2 - 2)
        printMsg += 'Library'
        printMsg += '_' * (lineLength - len(printMsg))

        SystemManager.pipePrint(printMsg)

        SystemManager.pipePrint(twoLine)

        for fileName, val in sorted(\
            self.fileList.items(), key=lambda e: int(e[1]['pageCnt']), reverse=True):
            try:
                memSize = \
                    self.intervalFileData[0][fileName]['pageCnt'] * SystemManager.pageSize >> 10
            except:
                memSize = 0
            try:
                fileSize = ((val['totalSize'] + SystemManager.pageSize - 1) / \
                    SystemManager.pageSize) * SystemManager.pageSize >> 10
            except:
                fileSize = 0

            # set percentage #
            if fileSize != 0:
                per = int(int(memSize) / float(fileSize) * 100)
            else:
                per = 0

            # check whether this file was profiled or not #
            isRep = False
            for fileData in reversed(self.intervalFileData):
                if fileName in fileData and fileData[fileName]['isRep']:
                    printMsg = "{0:>10} |{1:>7} |{2:>3}|".format(memSize, fileSize, per)
                    isRep = True
                    break

            if isRep is False:
                continue

            # calculate diff of on-memory file size #
            if len(self.intervalFileData) > 1:
                for idx in xrange(1, len(self.intervalFileData)):
                    diffNew = 0
                    diffDel = 0

                    try:
                        nowFileMap = self.intervalFileData[idx][fileName]['fileMap']
                    except:
                        nowFileMap = None
                    try:
                        prevFileMap = self.intervalFileData[idx - 1][fileName]['fileMap']
                    except:
                        prevFileMap = None

                    if nowFileMap is None:
                        if prevFileMap is not None:
                            diffDel = self.intervalFileData[idx - 1][fileName]['pageCnt']
                    else:
                        if prevFileMap is None:
                            diffNew = self.intervalFileData[idx][fileName]['pageCnt']
                        else:
                            if len(nowFileMap) == len(prevFileMap):
                                for i in xrange(len(nowFileMap)):
                                    if nowFileMap[i] > prevFileMap[i]:
                                        diffNew += 1
                                    elif nowFileMap[i] < prevFileMap[i]:
                                        diffDel += 1

                    diffNew = diffNew * SystemManager.pageSize >> 10
                    diffDel = diffDel * SystemManager.pageSize >> 10
                    printMsg += "+%6d/-%6d|" % (diffNew, diffDel)

            totalMemSize = val['pageCnt'] * SystemManager.pageSize >> 10

            if fileSize != 0:
                per = int(int(totalMemSize) / float(fileSize) * 100)
            else:
                per = 0

            printMsg += "{0:11}|{1:3}| {2:1}".format(totalMemSize, per, fileName)

            SystemManager.pipePrint(printMsg)

        SystemManager.pipePrint(oneLine + '\n\n\n')



    def makeReadaheadList(self):
        pass



    def scanProcs(self):
        # get process list in /proc directory #
        try:
            pids = os.listdir(SystemManager.procPath)
        except:
            SystemManager.printError('Fail to open %s' % (SystemManager.procPath))
            sys.exit(0)

        # scan comms include words in SystemManager.showGroup #
        for pid in pids:
            try:
                int(pid)
            except:
                continue

            # make path of comm #
            procPath = "%s/%s" % (SystemManager.procPath, pid)
            commPath = "%s/%s" % (procPath, 'comm')
            pidComm = ''

            # make comm path of process #
            try:
                self.procData[pid]['comm']
            except:
                try:
                    fd = open(commPath, 'r')
                    pidComm = fd.readline()
                    pidComm = pidComm[0:len(pidComm) - 1]
                    fd.close()
                except:
                    SystemManager.printWarning('Fail to open %s' % (commPath))
                    continue

            # make path of tid #
            taskPath = "%s/%s" % (procPath, 'task')

            try:
                tids = os.listdir(taskPath)
            except:
                SystemManager.printWarning('Fail to open %s' % (taskPath))
                continue

            # make thread list in process object #
            for tid in tids:
                try:
                    int(tid)
                except:
                    continue

                # make comm path of thread #
                threadPath = "%s/%s" % (taskPath, tid)
                commPath = "%s/%s" % (threadPath, 'comm')

                try:
                    fd = open(commPath, 'r')
                    comm = fd.readline()
                    comm = comm[0:len(comm) - 1]
                    fd.close()
                except:
                    SystemManager.printWarning('Fail to open %s' % (commPath))
                    continue

                # save process info #
                for val in SystemManager.showGroup:
                    if comm.rfind(val) > -1 or tid == val:
                        # access procData #
                        try:
                            self.procData[pid]
                        except:
                            self.procData[pid] = dict(self.init_procData)
                            self.procData[pid]['tids'] = {}
                            self.procData[pid]['procMap'] = {}
                            self.procData[pid]['comm'] = pidComm

                            # make or update mapInfo per process #
                            self.makeProcMapInfo(pid, threadPath + '/maps')

                        # access threadData #
                        try:
                            self.procData[pid]['tids'][tid]
                        except:
                            self.procData[pid]['tids'][tid] = dict(self.init_threadData)
                            self.procData[pid]['tids'][tid]['comm'] = comm



    def fillFileMaps(self):
        self.profPageCnt = 0

        for fileName, val in self.fileData.items():
            if val['fileMap'] is not None and val['isRep']:
                val['pageCnt'] = val['fileMap'].count(1)
                self.profPageCnt += val['pageCnt']

        for pid, val in self.procData.items():
            for fileName, mapInfo in val['procMap'].items():
                if self.fileData[fileName]['fileMap'] is None or mapInfo is None:
                    continue

                # convert address and size to index in mapping table #
                offset = mapInfo['offset'] - self.fileData[fileName]['offset']
                offset = (offset + SystemManager.pageSize - 1) / SystemManager.pageSize
                size = (mapInfo['size'] + SystemManager.pageSize - 1) / SystemManager.pageSize

                mapInfo['fileMap'] = list(self.fileData[fileName]['fileMap'][offset:size])
                mapInfo['pageCnt'] = mapInfo['fileMap'].count(1)
                val['pageCnt'] += mapInfo['pageCnt']



    def makeProcMapInfo(self, pid, path):
        # open maps #
        try:
            fd = open(path, 'r')
        except:
            SystemManager.printWarning('Fail to open %s' % (path))
            return

        # read maps #
        mapBuf = fd.readlines()

        # parse and merge lines in maps #
        for val in mapBuf:
            self.mergeMapLine(val, self.procData[pid]['procMap'])



    def mergeFileMapInfo(self):
        for pid, val in self.procData.items():
            for fileName, scope in val['procMap'].items():
                newOffset = scope['offset']
                newSize = scope['size']
                newEnd = newOffset + newSize

                # access fileData #
                try:
                    savedOffset = self.fileData[fileName]['offset']
                    savedSize = self.fileData[fileName]['size']
                    savedEnd = savedOffset + savedSize

                    # add pid into file info #
                    if not pid in self.fileData[fileName]['pids']:
                        self.fileData[fileName]['pids'][pid] = val['comm']

                    # bigger start address then saved one #
                    if savedOffset <= newOffset:
                        # merge bigger end address then saved one #
                        if savedEnd < newEnd:
                            self.fileData[fileName]['size'] += (newEnd - savedOffset - savedSize)
                        # ignore smaller end address then saved one #
                        else:
                            pass
                    # smaller start address then saved one #
                    else:
                        if savedEnd >= newEnd:
                            self.fileData[fileName]['size'] += (savedOffset - newOffset)
                        else:
                            self.fileData[fileName]['size'] = newSize

                        self.fileData[fileName]['offset'] = newOffset
                except:
                    self.fileData[fileName] = dict(self.init_mapData)
                    self.fileData[fileName]['offset'] = newOffset
                    self.fileData[fileName]['size'] = newSize
                    self.fileData[fileName]['pids'] = dict()
                    self.fileData[fileName]['pids'][pid] = val['comm']



    def mergeMapLine(self, string, procMap):
        m = re.match(r'^(?P<startAddr>.\S+)-(?P<endAddr>.\S+) (?P<permission>.\S+) ' + \
            r'(?P<offset>.\S+) (?P<devid>.\S+) (?P<inode>.\S+)\s*(?P<binName>.+)', string)
        if m is not None:
            d = m.groupdict()

            fileName = d['binName']
            startAddr = int(d['startAddr'], 16)
            endAddr = int(d['endAddr'], 16)

            newOffset = int(d['offset'], 16)
            newSize = endAddr - startAddr
            newEnd = newOffset + newSize

            try:
                savedOffset = procMap[fileName]['offset']
                savedSize = procMap[fileName]['size']
                savedEnd = savedOffset + savedSize

                # bigger start address then saved one #
                if savedOffset <= newOffset:
                    # merge bigger end address then saved one #
                    if savedEnd < newEnd:
                        procMap[fileName]['size'] += (newEnd - savedOffset - savedSize)
                    # ignore smaller end address then saved one #
                    else:
                        pass
                # smaller start address then saved one #
                else:
                    if savedEnd >= newEnd:
                        procMap[fileName]['size'] += (savedOffset - newOffset)
                    else:
                        procMap[fileName]['size'] = newSize

                    procMap[fileName]['offset'] = newOffset
            except:
                procMap[fileName] = dict(self.init_mapData)
                procMap[fileName]['offset'] = newOffset
                procMap[fileName]['size'] = newSize
        else:
            if SystemManager.showAll:
                SystemManager.printWarning("Fail to recognize '%s' line in maps" % string)



    def getFilePageMaps(self):
        self.profSuccessCnt = 0
        self.profFailedCnt = 0

        for fileName, val in self.fileData.items():
            if fileName.startswith('/dev'):
                SystemManager.printWarning("Skip to analize %s because it is device node" % fileName)
                continue

            if len(self.intervalFileData) > 0:
                # use file descriptor already saved as possible #
                try:
                    val['fd'] = \
                        self.intervalFileData[len(self.intervalFileData) - 1][fileName]['fd']
                    val['totalSize'] = \
                        self.intervalFileData[len(self.intervalFileData) - 1][fileName]['totalSize']
                    val['isRep'] = \
                        self.intervalFileData[len(self.intervalFileData) - 1][fileName]['isRep']
                except:
                    pass

                if val['isRep'] is False:
                    continue

            if val['fd'] is None:
                '''
                no fd related to this file
                case 1) no opened
                case 2) closed by mincore error
                case 3) closed because of rlimit
                '''

                try:
                    # open binary file to check whether pages are on memory or not #
                    stat = os.stat(fileName)

                    devid = stat.st_dev
                    inode = stat.st_ino

                    # check whether this file was profiled or not #
                    if inode in self.inodeData:
                        found = False
                        repFile = ''
                        fileList = {}
                        procList = dict(val['pids'].items())

                        for fileIdx, fileDevid in self.inodeData[inode].items():
                            # this file was already profiled with hard-linked others #
                            if devid == fileDevid:
                                found = True

                                # add file into same file list #
                                fileList[fileName] = True
                                fileList[fileIdx] = True

                                # merge process list related to this file #
                                procList = \
                                    dict(procList.items() + self.fileData[fileIdx]['pids'].items())

                                if self.fileData[fileIdx]['isRep']:
                                    repFile = fileIdx

                        if found:
                            self.inodeData[inode][fileName] = devid
                            self.fileData[fileName]['isRep'] = False
                            hardLinkCnt = len(fileList)

                            # set representative file #
                            for fileIdx, value in fileList.items():
                                self.fileData[fileIdx]['repFile'] = repFile
                                self.fileData[fileIdx]['hardLink'] = hardLinkCnt

                            # assign merged process list to representative file #
                            self.fileData[repFile]['pids'] = procList
                            self.fileData[repFile]['hardLink'] = hardLinkCnt

                            if self.fileData[repFile]['linkList'] is not None:
                                self.fileData[repFile]['linkList'] = \
                                    dict(self.fileData[repFile]['linkList'].items() + fileList.items())
                            else:
                                self.fileData[repFile]['linkList'] = fileList

                            continue
                        else:
                            self.inodeData[inode][fileName] = devid
                    else:
                        self.inodeData[inode] = dict(self.init_inodeData)
                        self.inodeData[inode][fileName] = devid

                    size = stat.st_size
                    linkCnt = stat.st_nlink
                    time = stat.st_atime

                    val['inode'] = inode
                    val['totalSize'] = size
                    val['linkCnt'] = linkCnt
                    val['accessTime'] = time

                    fd = open(fileName, "r")
                    val['fd'] = fd
                except:
                    self.profFailedCnt += 1
                    if SystemManager.warningEnable:
                        SystemManager.printWarning('Fail to open %s' % fileName)
                    continue

            # check file size whether it is readable or not #
            if val['totalSize'] <= 0:
                self.profFailedCnt += 1
                if SystemManager.warningEnable:
                    SystemManager.printWarning('Fail to mmap %s' % fileName)
                continue

            # prepare variables for mincore systemcall #
            fd = val['fd'].fileno()
            offset = val['offset']
            size = val['size']

            # call mincore systemcall #
            pagemap = self.libguider.get_filePageMap(fd, offset, size)

            # save the array of ctype into list #
            if pagemap is not None:
                try:
                    val['fileMap'] = \
                        [pagemap[i] for i in xrange(size / SystemManager.pageSize)]

                    self.profSuccessCnt += 1

                    # fd resource is about to run out #
                    if SystemManager.maxFd - 16 < fd:
                        val['fd'].close()
                        val['fd'] = None
                except:
                    SystemManager.printWarning('Fail to access %s' % fileName)
                    val['fileMap'] = None
                    self.profFailedCnt += 1
            else:
                val['fd'].close()
                val['fd'] = None

        if len(self.fileData) > 0:
            SystemManager.printGood('Profiled a total of %d files' % self.profSuccessCnt)
        else:
            SystemManager.printError('Fail to profile files')
            sys.exit(0)

        if self.profFailedCnt > 0:
            SystemManager.printWarning('Fail to open a total of %d files' % self.profFailedCnt)





class LogManager(object):
    """ Manager for error log """
    def __init__(self):
        self.terminal = sys.stderr
        self.error = False



    def write(self, message):
        self.terminal.write(message)

        if self.error:
            return

        try:
            with open(SystemManager.errorFile, 'a') as fd:
                fd.write(message)
        except:
            self.error = True
            SystemManager.printError('Fail to open %s for logging error' % SystemManager.errorFile)



    def flush(self):
        pass



    def __getattr__(self, attr):
        return getattr(self.terminal, attr)





class SystemManager(object):
    """ Manager for system setting """

    pageSize = 4096
    blockSize = 512
    bufferSize = '40960'
    ttyRows = '50'
    ttyRowsMargin = 6
    ttyCols = '156'
    magicString = '@@@@@'
    procPath = '/proc'
    imagePath = None
    launchBuffer = None
    maxFd = 1024
    lineLength = 154
    pid = 0
    depth = '0'

    HZ = 250 # 4ms tick #
    if sys.platform.startswith('linux'):
        TICK = os.sysconf(os.sysconf_names['SC_CLK_TCK'])
    else:
        TICK = int((1 / float(HZ)) * 1000)

    arch = 'arm'
    archOption = None
    mountPath = None
    mountCmd = None
    signalCmd = "trap 'kill $$' INT\nsleep 1d\n"
    saveCmd = None
    addr2linePath = None
    objdumpPath = None
    rootPath = None
    fontPath = None
    pipeForPrint = None
    fileForPrint = None
    inputFile = None
    outputFile = None
    errorFile = '/tmp/guider.err'
    sourceFile = None
    printFile = None
    optionList = None
    savedOptionList = None
    customCmd = None
    userCmd = None
    kernelCmd = None
    customEventList = []
    userEventList = []
    kernelEventList = []
    libcObj = None

    addrAsServer = None
    addrOfServer = None
    addrListForPrint = {}
    addrListForReport = {}
    jsonObject = None

    tgidEnable = True
    binEnable = False
    processEnable = True
    groupProcEnable = False

    maxCore = 0
    nrCore = 0
    logSize = 0
    curLine = 0
    totalLine = 0
    dbgEventLine = 0
    uptime = 0
    prevUptime = 0
    uptimeDiff = 0
    netstat = ''
    prevNetstat = ''
    netInIndex = -1

    reportEnable = False
    reportPath = None
    reportFileEnable = False
    imageEnable = False
    customImageEnable = False
    graphEnable = False
    procBuffer = []
    procInstance = None
    fileInstance = None
    sysInstance = None
    procBufferSize = 0
    bufferString = ''
    bufferRows = 0
    systemInfoBuffer = ''
    kerSymTable = {}
    reportData = {}

    eventLogFile = None
    eventLogFD = None

    showAll = False
    selectMenu = None
    intervalNow = 0
    recordStatus = False
    condExit = False
    sort = None

    statFd = None
    memFd = None
    vmstatFd = None
    swapFd = None
    uptimeFd = None
    netstatFd = None
    cmdFd = None

    irqEnable = False
    cpuEnable = True
    memEnable = False
    heapEnable = False
    diskEnable = False
    fileTopEnable = False
    ueventEnable = False
    keventEnable = False
    netEnable = False
    stackEnable = False
    wchanEnable = False
    wfcEnable = False
    blockEnable = False
    userEnable = True
    futexEnable = False
    pipeEnable = False
    depEnable = False
    sysEnable = False
    waitEnable = False
    cmdEnable = False
    backgroundEnable = False
    resetEnable = False
    warningEnable = False
    intervalEnable = 0

    functionEnable = False
    systemEnable = False
    fileEnable = False
    threadEnable = False

    repeatInterval = 0
    repeatCount = 0
    progressCnt = 0
    progressChar = {
            0: '|',
            1: '/',
            2: '-',
            3: '\\',
    }

    cmdList = {}
    rcmdList = {}
    savedProcTree = {}
    savedMountTree = {}
    preemptGroup = []
    showGroup = []
    syscallList = []



    def __init__(self):
        SystemManager.sysInstance = self

        self.memInfo = {}
        self.diskInfo = {}
        self.mountInfo = {}

        self.cpuData = None
        self.memBeforeData = None
        self.memAfterData = None
        self.diskBeforeData = None
        self.diskAfterData = None
        self.mountData = None
        self.uptimeData = None
        self.loadData = None
        self.cmdlineData = None
        self.osData = None
        self.devData = None
        self.procData = None

        self.cpuInfo = dict()
        self.memInfo['before'] = dict()
        self.memInfo['after'] = dict()
        self.diskInfo['before'] = dict()
        self.diskInfo['after'] = dict()
        self.systemInfo = dict()

        SystemManager.eventLogFile = None

        # Save storage info first #
        self.saveMemInfo()
        self.saveDiskInfo()



    def __del__(self):
        pass



    @staticmethod
    def setErrorLogger():
        sys.stderr = LogManager()



    @staticmethod
    def setComm():
        if sys.platform.startswith('linux'):
            try:
                import ctypes
                from ctypes import cdll, POINTER
            except ImportError:
                err = sys.exc_info()[1]
                print("[Warning] Fail to import package: " + err.args[0])

            try:
                SystemManager.libcObj = cdll.LoadLibrary('libc.so.6')
                SystemManager.libcObj.prctl(15, __module__, 0, 0, 0)
            except:
                print('[Warning] Fail to set comm because of prctl in libc')
        else:
            print('[Warning] Fail to set comm because this platform is not linux')



    @staticmethod
    def makeJsonString(dictObj):
        if SystemManager.jsonObject is None:
            return None
        else:
            return SystemManager.jsonObject.dumps(dictObj, indent=2)



    @staticmethod
    def writeJsonObject(jsonObj):
        if os.path.exists(SystemManager.reportPath):
            os.remove(SystemManager.reportPath)

        try:
            fd = open(SystemManager.reportPath, 'w')
        except:
            SystemManager.printWarning(\
                "Fail to open %s to write json data" % SystemManager.reportPath)
            return False

        try:
            fd.write(jsonObj)
            fd.close()
        except:
            SystemManager.printWarning(\
                "Fail to write json data to %s" % SystemManager.reportPath)
            return False

        return True



    @staticmethod
    def makeJsonDict(strObj):
        if SystemManager.jsonObject is None:
            return None
        else:
            try:
                strObj = strObj.replace("'", '"')
                return SystemManager.jsonObject.loads(strObj)
            except:
                return None



    @staticmethod
    def getProcTree():
        procTree = {}

        # get process list in /proc directory #
        try:
            pids = os.listdir(SystemManager.procPath)
        except:
            SystemManager.printError('Fail to open %s' % (SystemManager.procPath))
            return None

        # scan comms include words in SystemManager.showGroup #
        for pid in pids:
            try:
                int(pid)
            except:
                continue

            # make path of tid #
            procPath = "%s/%s" % (SystemManager.procPath, pid)
            taskPath = "%s/%s" % (procPath, 'task')

            try:
                tids = os.listdir(taskPath)
            except:
                SystemManager.printWarning('Fail to open %s' % (taskPath))
                continue

            for tid in tids:
                try:
                    int(tid)
                    procTree[tid] = pid
                except:
                    continue

        return procTree



    @staticmethod
    def submitSystemInfo():
        si = SystemManager()
        si.saveAllInfo()
        si.printAllInfoToBuf()
        SystemManager.pipePrint(SystemManager.systemInfoBuffer)
        SystemManager.clearInfoBuffer()



    @staticmethod
    def printOptions():
        if len(sys.argv) <= 1 or \
            sys.argv[1] == '-h' or \
            sys.argv[1] == '--help' or \
            SystemManager.findOption('h'):

            cmd = sys.argv[0]

            if cmd.find('.pyc') >= 0:
                cmd = cmd[:cmd.find('.pyc')]

            print('\n[ g.u.i.d.e.r \t%s ]\n\n' % __version__)

            print('Usage:')
            print('\t# %s [mode] [options]' % cmd)
            print('\t$ %s <file> [options]' % cmd)

            print('Example:')
            print('\t# %s record -s /var/log -e mi -g comm, 1243' % cmd)
            print('\t$ %s guider.dat -o /var/log -a -i' % cmd)
            print('\t$ %s top -i 2\n' % cmd)

            print('Options:')
            print('\t[record mode]')
            print('\t\ttop        [top]')
            print('\t\trecord     [thread]')
            print('\t\trecord -y  [system]')
            print('\t\trecord -f  [function]')
            print('\t\trecord -F  [file]')
            print('\t\tview       [page]')
            print('\t[control mode]')
            print('\t\tlist')
            print('\t\tstart|stop|send [pid]')
            print('\t[record options]')
            print('\t\t-e  [enable_optionsPerMode:bellowCharacters]')
            print('\t\t\t  [function] {m(em)|b(lock)|h(eap)|p(ipe)|g(raph)}')
            print('\t\t\t  [thread]   '\
                '{m(em)|b(lock)|i(rq)|l(og)|n(et)|p(ipe)|r(eset)|g(raph)|f(utex)}')
            print('\t\t\t  [top]      '\
                '{t(hread)|d(isk)|w(fc)|W(chan)|s(tack)|m(em)|I(mage)|g(raph)|r(eport)|f(ile)}')
            print('\t\t-d  [disable_optionsPerMode:bellowCharacters]')
            print('\t\t\t  [thread]   {c(pu)}')
            print('\t\t\t  [function] {c(pu)|u(ser)}')
            print('\t\t-s  [save_traceData:dir/file]')
            print('\t\t-S  [sort_output:c(pu)/m(em)/b(lock)/w(fc)/p(id)/n(ew)/r(untime)]')
            print('\t\t-u  [run_inBackground]')
            print('\t\t-W  [wait_forSignal]')
            print('\t\t-R  [record_repeatedly:interval,count]')
            print('\t\t-b  [set_bufferSize:kb]')
            print('\t\t-D  [trace_threadDependency]')
            print('\t\t-t  [trace_syscall:syscalls]')
            print('\t\t-H  [set_depth]')
            print('\t\t-T  [set_fontPath]')
            print('\t\t-j  [set_reportPath:dir]')
            print('\t\t-U  [set_userEvent:name:func|addr:file]')
            print('\t\t-K  [set_kernelEvent:name:func|addr{:%reg/argtype:rettype}]')
            print('\t\t-C  [set_commandScriptPath:file]')
            print('\t\t-w  [set_customRecordCommand:BEFORE|AFTER|STOP:file:value]')
            print('\t\t-x  [set_addressForLocalServer:{ip:}port]')
            print('\t\t-X  [set_requestToRemoteServer:{req@ip:port}]')
            print('\t\t-N  [set_addressForReport:req@ip:port]')
            print('\t\t-n  [set_addressForPrint:ip:port]')
            print('\t[analysis options]')
            print('\t\t-o  [save_outputData:dir]')
            print('\t\t-P  [group_perProcessBasis]')
            print('\t\t-p  [show_preemptInfo:tids]')
            print('\t\t-l  [set_addr2linePath:files]')
            print('\t\t-r  [set_targetRootPath:dir]')
            print('\t\t-I  [set_inputValue:file|addr]')
            print('\t\t-q  [configure_taskList]')
            print('\t\t-L  [convert_textToImage]')
            print('\t[common options]')
            print('\t\t-a  [show_allInfo]')
            print('\t\t-i  [set_interval:sec]')
            print('\t\t-g  [set_filter:comms|tids{:file}]')
            print('\t\t-A  [set_arch:arm|x86|x64]')
            print('\t\t-c  [set_customEvent:event:filter]')
            print('\t\t-E  [set_errorLogPath:file]')
            print('\t\t-m  [set_objdumpPath:file]')
            print('\t\t-v  [verbose]')
            if SystemManager.findOption('a'):
                print('\t[examples]')

                print('\t\t[thread mode]')
                print('\t\t\t- record cpu usage of threads')
                print('\t\t\t\t# %s record -s .' % cmd)
                print('\t\t\t- record all resource usage of threads in background')
                print('\t\t\t\t# %s record -s . -e mbi -u' % cmd)
                print('\t\t\t- record all resource usage excluding cpu of threads in background')
                print('\t\t\t\t# %s record -s . -e mbi -d c -u' % cmd)
                print('\t\t\t- record specific systemcalls of specific threads')
                print('\t\t\t\t# %s record -s . -t sys_read,sys_write -g 1234' % cmd)
                print('\t\t\t- record specific user function events')
                print('\t\t\t\t# %s record -s . -U evt1:func1:/tmp/a.out,evt2:0x1234:/tmp/b.out -m $(which objdump)' % cmd)
                print('\t\t\t- record specific kernel function events')
                print('\t\t\t\t# %s record -s . -K evt1:func1,evt2:0x1234' % cmd)
                print('\t\t\t- record specific kernel function events with register values')
                print('\t\t\t\t# %s record -s . -K evt1:func1:%%bp/u32.%%sp/s64,evt2:0x1234:$stack:NONE' % cmd)
                print('\t\t\t- record specific kernel function events with return value')
                print('\t\t\t\t# %s record -s . -K evt1:func1::*string,evt2:0x1234:NONE:**string' % cmd)
                print('\t\t\t- analize record data by expressing all possible information')
                print('\t\t\t\t# %s guider.dat -o . -a -i' % cmd)
                print('\t\t\t- analize record data including preemption info of specific threads')
                print('\t\t\t\t# %s guider.dat -o . -p 1234,4567' % cmd)
                print('\t\t\t- analize specific threads that are involved in the specific processes')
                print('\t\t\t\t# %s guider.dat -o . -P -g 1234,4567' % cmd)

                print('\n\t\t[function mode]')
                print('\t\t\t- record cpu usage of functions in all threads')
                print('\t\t\t\t# %s record -f -s .' % cmd)
                print('\t\t\t- record specific events of only kernel functions in all threads')
                print('\t\t\t\t# %s record -f -s . -d u -c sched/sched_switch' % cmd)
                print('\t\t\t- record all usage of functions in specific threads')
                print('\t\t\t\t# %s record -f -s . -e mbh -g 1234' % cmd)
                print('\t\t\t- analize record data by expressing all possible information')
                print('\t\t\t\t# %s guider.dat -o . -r /home/target/root -l $(which arm-addr2line) -a' % cmd)
                print('\t\t\t- record specific kernel functions in a specific thread')
                print('\t\t\t\t# %s record -f -s . -e g -c SyS_read -g 1234' % cmd)
                print('\t\t\t- record segmentation fault event in all threads')
                print('\t\t\t\t# %s record -f -s . -K segflt:bad_area -ep' % cmd)

                print('\n\t\t[top mode]')
                print('\t\t\t- show real-time resource usage of processes')
                print('\t\t\t\t# %s top' % cmd)
                print('\t\t\t- show real-time file usage of processes')
                print('\t\t\t\t# %s top -ef' % cmd)
                print('\t\t\t- show real-time resource usage of processes by sorting memory')
                print('\t\t\t\t# %s top -S m' % cmd)
                print('\t\t\t- show real-time resource usage including disk of threads per 2 sec interval')
                print('\t\t\t\t# %s top -e td -i 2 -a' % cmd)
                print('\t\t\t- show real-time resource usage of specific processes/threads involved in specific process group')
                print('\t\t\t\t# %s top -g 1234,4567 -P' % cmd)
                print('\t\t\t- record resource usage of processes to the specific file in background')
                print('\t\t\t\t# %s top -o . -u' % cmd)
                print('\t\t\t- record and report system status to the specific file in background')
                print('\t\t\t\t# %s top -o . -e r -j . -u' % cmd)
                print('\t\t\t- record and save system status to the specific file if some events occur')
                print('\t\t\t\t# %s top -o . -e r -e f' % cmd)
                print('\t\t\t- record and report system status to the specific image')
                print('\t\t\t\t# %s top -o . -e r -e f' % cmd)
                print('\t\t\t- convert a analysis text to a graph image')
                print('\t\t\t\t# %s top -I guider.out -e g' % cmd)
                print('\t\t\t- report system status to the specific server')
                print('\t\t\t\t# %s top -n 192.168.0.5:5555' % cmd)
                print('\t\t\t- report system status to the specific server if some events occur')
                print('\t\t\t\t# %s top -er -N REPORT_ALWAYS@192.168.0.5:5555' % cmd)
                print('\t\t\t- record and send analysis output to specific clients that asked dyanmic request')
                print('\t\t\t\t# %s top -x 5555' % cmd)
                print('\t\t\t- receive and print analysis output from client')
                print('\t\t\t\t# %s top -x 5555 -X' % cmd)
                print('\t\t\t- set event configuration file')
                print('\t\t\t\t# %s top -I guider.json' % cmd)

                print('\n\t\t[file mode]')
                print('\t\t\t- record memory usage of mapped files to the specific file')
                print('\t\t\t\t# %s record -F -o .' % cmd)
                print('\t\t\t- record memory usage of mapped files and compare each intervals')
                print('\t\t\t\t# %s record -F -i' % cmd)

                print('\n\t\t[etc]')
                print('\t\t\t- view page property of specific pages')
                print('\t\t\t\t# %s view -g 1234 -I 0x7abc1234-0x7abc6789' % cmd)
                print('\t\t\t- convert text to image')
                print('\t\t\t\t# %s guider.out -L' % cmd)
                print('\t\t\t- wait for signal')
                print('\t\t\t\t# %s record|top -W' % cmd)
                print('\t\t\t- show running guider processes')
                print('\t\t\t\t# %s list' % cmd)
                print('\t\t\t- send event signal to guider processes')
                print('\t\t\t\t# %s send' % cmd)
                print('\t\t\t- send stop signal to guider processes')
                print('\t\t\t\t# %s stop' % cmd)
                print('\t\t\t- send some signal to specific processes')
                print('\t\t\t\t# %s send -9 1234, 4567' % cmd)

            print("\nAuthor: \n\t%s(%s)" % (__author__, __email__))
            print("\nReporting bugs: \n\t%s or %s" % (__email__, __repository__))
            print("\nCopyright: ")
            print("\t%s." % (__copyright__))
            print("\tLicense %s." % (__license__))
            print("\tThis is free software.\n")

            sys.exit(0)



    @staticmethod
    def getArch():
        try:
            arch = os.uname()[4]

            if arch.startswith('arm'):
                return 'arm'
            elif arch.startswith('x86_64') or arch.startswith('ia64'):
                return 'x64'
            elif arch.startswith('i386') or arch.startswith('i686'):
                return 'x86'
            else:
                return arch
        except:
            return None



    @staticmethod
    def setArch(arch):
        if len(arch) == 0:
            return

        SystemManager.removeEmptyValue(arch)

        # set systemcall table #
        if arch == 'arm':
            SystemManager.arch = arch
            ConfigManager.sysList = ConfigManager.sysList_arm
        elif arch == 'x86':
            SystemManager.arch = arch
            ConfigManager.sysList = ConfigManager.sysList_x86
        elif arch == 'x64':
            SystemManager.arch = arch
            ConfigManager.sysList = ConfigManager.sysList_x64
        else:
            SystemManager.printError(\
                'Fail to set archtecture to %s, only arm / x86 / x64 supported' % arch)



    @staticmethod
    def writeKernelCmd():
        effectiveCmd = []

        if SystemManager.keventEnable is False:
            return
        elif len(SystemManager.kernelCmd) == 0:
            SystemManager.printError("wrong format used with -K option, NAME:FUNC|ADDR{:ARGS:RET}")
            sys.exit(0)
        elif os.path.isfile(SystemManager.mountPath + '../kprobe_events') is False:
            SystemManager.printError(\
                "enable CONFIG_KPROBES & CONFIG_KPROBE_EVENTS option in kernel")
            sys.exit(0)

        for cmd in SystemManager.kernelCmd:
            cmdFormat = cmd.split(':')

            # check command format #
            cmdCnt = len(cmdFormat)
            if 4 < cmdCnt or cmdCnt < 2:
                SystemManager.printError("wrong format used with -K option, NAME:FUNC|ADDR{:ARGS:RET}")
                sys.exit(0)

            for item in effectiveCmd:
                if cmdFormat[0] == item[0]:
                    SystemManager.printError("redundant kernel event name '%s'" % item[0])
                    sys.exit(0)

            effectiveCmd.append(cmdFormat)

        # print kprobe event list #
        SystemManager.printInfo("enabled kernel events [ %s ]" % \
            ', '.join([ ':'.join(cmd) for cmd in effectiveCmd ]))

        # clear kprobe event filter #
        SystemManager.writeCmd("../kprobe_events", '')

        # apply kprobe events #
        for cmd in effectiveCmd:
            # check redundant event name #
            if SystemManager.userCmd is not None and \
                cmd[0] in [ucmd.split(':')[0] for ucmd in SystemManager.userCmd]:
                SystemManager.printError(\
                    "redundant event name '%s' as user event and kernel event" % cmd[0])
                sys.exit(0)

            # make entry commands #
            pCmd = 'p:%s_enter %s' % (cmd[0], cmd[1])
            sCmd = ''
            try:
                # parse argument option #
                for rCmd in cmd[2].split('.'):
                    # check absolute argument #
                    if rCmd[0] == '#':
                        sCmd = '%s %s' % (sCmd, rCmd[1:])
                        continue
                    elif len(rCmd.split('/')) == 1:
                        sCmd = '%s %s' % (sCmd, rCmd)
                        continue

                    rVal = rCmd.split('/')
                    if len(rVal) > 2:
                        SystemManager.printError("wrong command '%s' with -K option" % rCmd)
                        os._exit(0)
                    tVal = rVal[1]

                    # count the number of prefix * #
                    wCnt = 0
                    for idx, ch in enumerate(tVal):
                        if ch != '*':
                            wCnt = idx
                            break

                    # make entry command #
                    tVal = '%s%s%s:%s' % ('+0(' * wCnt, rVal[0], ')' * wCnt, tVal[wCnt:])

                    # add argument command to entry command #
                    sCmd = '%s %s' % (sCmd, tVal)
            except:
                pass

            # apply entry command #
            if sCmd != ' NONE':
                pCmd = '%s %s' % (pCmd, sCmd)
                if SystemManager.writeCmd('../kprobe_events', pCmd, append=True) < 0:
                    SystemManager.printError("wrong command '%s' with -K option" % pCmd)
                    os._exit(0)

            # make return commands #
            rCmd = 'r:%s_exit %s' % (cmd[0], cmd[1])
            sCmd = ''

            try:
                tCmd = cmd[3]

                # check absolute argument #
                if tCmd[0] == '#':
                    sCmd = '%s' % (tCmd[1:])
                else:
                    rVal = tCmd.split('/')
                    if len(rVal) > 2:
                        SystemManager.printError("wrong command '%s' with -K option" % tCmd)
                        os._exit(0)
                    tVal = rVal[0]

                    # count the number of prefix * #
                    wCnt = 0
                    for idx, ch in enumerate(tVal):
                        if ch != '*':
                            wCnt = idx
                            break

                    if tCmd != 'NONE':
                        # make return command #
                        sCmd = '%s%s%s:%s' % ('+0(' * wCnt, '$retval', ')' * wCnt, tVal[wCnt:])
                    else:
                        sCmd = 'NONE'
            except:
                pass

            # apply return command #
            if sCmd != 'NONE':
                rCmd = '%s %s' % (rCmd, sCmd)
                if SystemManager.writeCmd('../kprobe_events', rCmd, append=True) < 0:
                    SystemManager.printError("wrong command '%s' with -K option" % rCmd)
                    sys.exit(0)

        # apply filter #
        if len(SystemManager.showGroup) > 0:
            cmd = "("
            for pid in SystemManager.showGroup:
                try:
                    int(pid)
                except:
                    SystemManager.printWarning(\
                            "wrong option value %s, input number in integer format" % pid)
                    continue
                cmd += "common_pid == %s || " % pid

            lastPos = cmd.rfind(" ||")
            if lastPos >= 0:
                cmd = cmd[:lastPos] + ")"
            else:
                cmd = ''

            if SystemManager.writeCmd("kprobes/filter", cmd) < 0:
                SystemManager.printError("Fail to apply kprobe filter '%s'" % cmd)
                sys.exit(0)

        # enable kprobe events #
        if SystemManager.writeCmd("kprobes/enable", '1') < 0:
            SystemManager.printError("Fail to apply kprobe events")
            sys.exit(0)



    @staticmethod
    def writeUserCmd():
        objdumpFound = False
        effectiveCmd = []

        if SystemManager.ueventEnable is False:
            return
        elif len(SystemManager.userCmd) == 0:
            SystemManager.printError("wrong format used with -U option, NAME:FUNC|ADDR:FILE")
            sys.exit(0)
        elif os.path.isfile(SystemManager.mountPath + '../uprobe_events') is False:
            SystemManager.printError(\
                "enable CONFIG_UPROBES & CONFIG_UPROBE_EVENT option in kernel")
            sys.exit(0)

        for cmd in SystemManager.userCmd:
            addr = None
            cvtCmd = cmd.replace("::", "#")
            cmdFormat = cvtCmd.split(':')
            cmdFormat = [ cmd.replace("#", "::") for cmd in cmdFormat ]

            if len(cmdFormat) == 3:
                # check redundant event name #
                if SystemManager.kernelCmd is not None and \
                    cmd[0] in [kcmd.split(':')[0] for kcmd in SystemManager.kernelCmd]:
                    SystemManager.printError(\
                        "redundant event name '%s' as user event and kernel event" % cmd[0])
                    sys.exit(0)

                # check binary file #
                if os.path.isfile(cmdFormat[2]) is False:
                    SystemManager.printError("Fail to find '%s' binary" % cmdFormat[2])
                    sys.exit(0)

                # symbol input #
                if cmdFormat[1].startswith('0x') is False:
                    # symbol input with no objdump #
                    if SystemManager.objdumpPath is None:
                        SystemManager.printError(\
                            "Fail to find objdump, use also -m option with objdump path")
                        sys.exit(0)
                    # symbol input with objdump #
                    elif objdumpFound is False and os.path.isfile(SystemManager.objdumpPath) is False:
                        SystemManager.printError("Fail to find %s to use objdump" % \
                            SystemManager.objdumpPath)
                        sys.exit(0)
                    else:
                        # get address of symbol in binary #
                        addr = SystemManager.getSymOffset(\
                            cmdFormat[1], cmdFormat[2], SystemManager.objdumpPath)
                        if addr is None:
                            SystemManager.printError("Fail to find '%s' in %s" % \
                                (cmdFormat[1], cmdFormat[2]))
                            sys.exit(0)
                else:
                    addr = cmdFormat[1]
                    try:
                        hex(long(addr, base=16)).rstrip('L')
                    except:
                        SystemManager.printError("Fail to recognize address %s" % addr)
                        sys.exit(0)

                for item in effectiveCmd:
                    if cmdFormat[0] == item[0]:
                        SystemManager.printError("redundant user event name '%s'" % item[0])
                        sys.exit(0)

                effectiveCmd.append([cmdFormat[0], addr, cmdFormat[2]])
            else:
                SystemManager.printError("wrong format used with -U option, NAME:FUNC|ADDR:FILE")
                sys.exit(0)

        # print uprobe event list #
        SystemManager.printInfo("enabled user events [ %s ]" % \
            ', '.join([ ':'.join(cmd) for cmd in effectiveCmd ]))

        # clear uprobe event filter #
        SystemManager.writeCmd("../uprobe_events", '')

        # apply uprobe events #
        for cmd in effectiveCmd:
            # apply entry events #
            pCmd = 'p:%s_enter %s:%s' % (cmd[0], cmd[2], cmd[1])
            if SystemManager.writeCmd('../uprobe_events', pCmd, append=True) < 0:
                SystemManager.printError("wrong command '%s' with -U option" % pCmd)
                sys.exit(0)
            # apply return events #
            rCmd = 'r:%s_exit %s:%s' % (cmd[0], cmd[2], cmd[1])
            if SystemManager.writeCmd('../uprobe_events', rCmd, append=True) < 0:
                SystemManager.printError("wrong command '%s' with -U option" % rCmd)
                sys.exit(0)

        # apply filter #
        if len(SystemManager.showGroup) > 0:
            cmd = "("
            for pid in SystemManager.showGroup:
                try:
                    int(pid)
                except:
                    SystemManager.printWarning(\
                            "wrong option value %s, input number in integer format" % pid)
                    continue
                cmd += "common_pid == %s || " % pid

            lastPos = cmd.rfind(" ||")
            if lastPos >= 0:
                cmd = cmd[:lastPos] + ")"
            else:
                cmd = ''

            if SystemManager.writeCmd("uprobes/filter", cmd) < 0:
                SystemManager.printError("Fail to apply uprobe filter '%s'" % cmd)
                sys.exit(0)

        # enable uprobe events #
        if SystemManager.writeCmd("uprobes/enable", '1') < 0:
            SystemManager.printError("Fail to apply uprobe events")
            sys.exit(0)



    @staticmethod
    def getSymOffset(symbol, binPath, objdumpPath):
        try:
            import subprocess
        except ImportError:
            err = sys.exc_info()[1]
            SystemManager.printError("Fail to import package: " + err.args[0])
            sys.exit(0)

        syms = []
        disline = []
        args = [objdumpPath, "-C", "-F", "-d", binPath]

        SystemManager.printStatus(\
            "start finding %s... [ STOP(ctrl + c) ]" % (symbol))

        # start objdump process #
        proc = subprocess.Popen(\
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1)

        while 1:
            try:
                # read a line from objdump process #
                line = proc.stdout.readline()
            except (OSError, IOError) as e:
                if e.errno == errno.EINTR:
                    continue

            # handle error #
            if not line:
                err = proc.stderr.read()
                if len(err) > 0:
                    proc.terminate()
                    SystemManager.printError(err[err.find(':') + 2:])
                    sys.exit(0)
                break

            # parse line to find offset of symbol #
            m = re.match(\
                r'\s*(?P<addr>\S*)\s*\<(?P<symbol>\S*)\>\s*\(File Offset:\s*(?P<offset>\S*)\s*\)', line)
            if m is not None:
                d = m.groupdict()
                if d['symbol'] == symbol:
                    proc.terminate()
                    return d['offset']
                elif d['symbol'].find(symbol) >= 0:
                    syms.append(d['symbol'])

        if len(syms) == 0:
            return None
        else:
            SystemManager.printError(\
                "Fail to find %s in %s, \n\tbut similar symbols [ %s ] are exist" % \
                (symbol, binPath, ', '.join(syms)))
            sys.exit(0)



    @staticmethod
    def writeCustomCmd():
        effectiveCmd = []

        if SystemManager.customCmd is None:
            return

        for cmd in SystemManager.customCmd:
            cmdFormat = cmd.split(':')

            if cmdFormat[0] == '':
                SystemManager.printError("wrong event '%s'" % cmdFormat[0])
                sys.exit(0)

            # check filter #
            if len(cmdFormat) == 1:
                origFilter = ''
                cmdFormat.append("common_pid != 0")
            else:
                origFilter = cmdFormat[1]
                cmdFormat[1] = "common_pid != 0 && " + cmdFormat[1]

            if SystemManager.isThreadMode() and cmdFormat[0] in SystemManager.cmdList:
                SystemManager.printError(\
                    "Fail to use default event '%s' as custom event" % cmdFormat[0])
                sys.exit(0)

            # check effective event #
            if SystemManager.writeCmd(cmdFormat[0] + '/enable', '0') < 0:
                SystemManager.printError("wrong event '%s'" % cmdFormat[0])
                sys.exit(0)

            # check and enable effective filter #
            if len(cmdFormat) > 1 and \
                SystemManager.writeCmd(cmdFormat[0] + '/filter', cmdFormat[1]) < 0:
                SystemManager.printError("wrong filter '%s' for '%s' event" % \
                    (origFilter, cmdFormat[0]))
                sys.exit(0)

            # check and enable effective event #
            if SystemManager.writeCmd(cmdFormat[0] + '/enable', '1') < 0:
                SystemManager.printError("wrong event '%s'" % cmdFormat[0])
                sys.exit(0)
            else:
                effectiveCmd.append(cmdFormat[0])

        if len(effectiveCmd) > 0:
            SystemManager.printInfo("enabled custom events [ %s ]" % ', '.join(effectiveCmd))



    @staticmethod
    def printAnalOption():
        enableStat = ''
        disableStat = ''

        if SystemManager.outputFile != None:
            return

        if SystemManager.isRecordMode() is False and SystemManager.isTopMode() is False:
            # common options #
            enableStat += SystemManager.arch.upper() + ' '
            if SystemManager.warningEnable:
                enableStat += 'WARNING '

        # function mode #
        if SystemManager.isFunctionMode():
            if SystemManager.heapEnable is False:
                disableStat += 'HEAP '
            else:
                enableStat += 'HEAP '

            if SystemManager.userEnable is False:
                disableStat += 'USER '
            else:
                enableStat += 'USER '

            if SystemManager.customCmd is not None:
                SystemManager.printInfo(\
                    "selected custom events [ %s ]" % ', '.join(SystemManager.customCmd))
        # thread mode #
        else:
            if SystemManager.intervalEnable > 0:
                enableStat += 'INTERVAL '
            else:
                disableStat += 'INTERVAL '

            if SystemManager.depEnable:
                enableStat += 'DEPENDENCY '
            else:
                disableStat += 'DEPENDENCY '

            if SystemManager.ueventEnable:
                enableStat += 'UEVENT '
            else:
                disableStat += 'UEVENT '

            if SystemManager.keventEnable:
                enableStat += 'KEVENT '
            else:
                disableStat += 'KEVENT '

            if SystemManager.graphEnable:
                enableStat += 'GRAPH '
            else:
                disableStat += 'GRAPH '

            if SystemManager.irqEnable:
                enableStat += 'IRQ '
            else:
                disableStat += 'IRQ '

            if SystemManager.netEnable:
                enableStat += 'NET '
            else:
                disableStat += 'NET '

            if SystemManager.sysEnable:
                enableStat += 'SYSCALL '
            else:
                disableStat += 'SYSCALL '

            if len(SystemManager.preemptGroup) > 0:
                enableStat += 'PREEMPT '
            else:
                disableStat += 'PREEMPT '

            if SystemManager.customCmd is not None:
                SystemManager.printInfo(\
                    "selected custom events [ %s ]" % ', '.join(SystemManager.customCmd))

        # common options #
        if SystemManager.showAll:
            enableStat += 'ALL '
        else:
            disableStat += 'ALL '

        if SystemManager.groupProcEnable:
            enableStat += 'PROCESS '
        else:
            disableStat += 'PROCESS '

        if SystemManager.cpuEnable is False:
            disableStat += 'CPU '
        else:
            enableStat += 'CPU '

        if SystemManager.memEnable is False:
            disableStat += 'MEMORY '
        else:
            enableStat += 'MEMORY '

        if SystemManager.blockEnable is False:
            disableStat += 'BLOCK '
        else:
            enableStat += 'BLOCK '

        # print options #
        if enableStat != '':
            SystemManager.printInfo("enabled analysis options [ %s]" % enableStat)

        if disableStat != '':
            SystemManager.printInfo("disabled analysis options [ %s]" % disableStat)



    @staticmethod
    def printRecordCmd():
        for idx, val in SystemManager.rcmdList.items():
            if len(val) == 0:
                continue

            cmds = []
            for item in val:
                cmds.append(':'.join(item))
            SystemManager.printInfo(\
                "user recording options on %s [ %s ]" % (idx, ', '.join(cmds)))



    @staticmethod
    def printRecordOption():
        enableStat = ''
        disableStat = ''

        # common options #
        enableStat += SystemManager.arch.upper() + ' '
        if SystemManager.warningEnable:
            enableStat += 'WARNING '
        if SystemManager.pipeEnable:
            enableStat += 'PIPE '

        # check current mode #
        if SystemManager.isTopMode():
            SystemManager.printInfo("TOP MODE")

            if SystemManager.fileTopEnable:
                enableStat += 'FILE '
            else:
                disableStat += 'FILE '

                if SystemManager.cpuEnable:
                    enableStat += 'CPU '
                else:
                    disableStat += 'CPU '

                if SystemManager.diskEnable:
                    enableStat += 'DISK '
                else:
                    disableStat += 'DISK '

                if SystemManager.stackEnable:
                    enableStat += 'STACK '
                else:
                    disableStat += 'STACK '

                if SystemManager.wchanEnable:
                    enableStat += 'WCHAN '
                else:
                    disableStat += 'WCHAN '

                if SystemManager.wfcEnable:
                    enableStat += 'WFC '
                else:
                    disableStat += 'WFC '

                if SystemManager.processEnable is False:
                    enableStat += 'THREAD '
                    disableStat += 'PROCESS '
                else:
                    disableStat += 'THREAD '
                    enableStat += 'PROCESS '

                if SystemManager.memEnable:
                    enableStat += 'MEMORY '
                else:
                    disableStat += 'MEMORY '

                if SystemManager.graphEnable:
                    enableStat += 'GRAPH '
                else:
                    disableStat += 'GRAPH '

                if SystemManager.imageEnable:
                    enableStat += 'IMAGE '
                else:
                    disableStat += 'IMAGE '

                if SystemManager.reportFileEnable:
                    enableStat += 'REPFILE '
                else:
                    disableStat += 'REPFILE '

                if SystemManager.groupProcEnable:
                    enableStat += 'GROUP '
                else:
                    disableStat += 'GROUP '

                if SystemManager.reportEnable:
                    enableStat += 'REPORT '
                else:
                    disableStat += 'REPORT '

        elif SystemManager.isFunctionMode():
            SystemManager.printInfo("FUNCTION MODE")

            if SystemManager.graphEnable:
                enableStat += 'GRAPH '
            else:
                disableStat += 'GRAPH '

                if SystemManager.cpuEnable is False:
                    disableStat += 'CPU '
                else:
                    enableStat += 'CPU '

                if SystemManager.memEnable is False:
                    disableStat += 'MEMORY '
                else:
                    enableStat += 'MEMORY '

                if SystemManager.heapEnable is False:
                    disableStat += 'HEAP '
                else:
                    enableStat += 'HEAP '

                if SystemManager.blockEnable is False:
                    disableStat += 'BLOCK '
                else:
                    enableStat += 'BLOCK '

                if SystemManager.userEnable is False:
                    disableStat += 'USER '
                else:
                    enableStat += 'USER '

        elif SystemManager.isFileMode():
            SystemManager.printInfo("FILE MODE")

        elif SystemManager.isSystemMode():
            SystemManager.printInfo("SYSTEM MODE")
            SystemManager.waitEnable = True

        else:
            SystemManager.printInfo("THREAD MODE")
            SystemManager.threadEnable = True

            if SystemManager.cpuEnable is False:
                disableStat += 'CPU '
            else:
                enableStat += 'CPU '

            if SystemManager.memEnable:
                enableStat += 'MEMORY '
            else:
                disableStat += 'MEMORY '

            if SystemManager.blockEnable:
                enableStat += 'BLOCK '
            else:
                disableStat += 'BLOCK '

            if SystemManager.irqEnable:
                enableStat += 'IRQ '
            else:
                disableStat += 'IRQ '

            if SystemManager.ueventEnable:
                enableStat += 'UEVENT '
            else:
                disableStat += 'UEVENT '

            if SystemManager.keventEnable:
                enableStat += 'KEVENT '
            else:
                disableStat += 'KEVENT '

            if SystemManager.netEnable:
                enableStat += 'NET '
            else:
                disableStat += 'NET '

            if SystemManager.repeatCount > 0:
                enableStat += 'REPEAT '
            else:
                disableStat += 'REPEAT '

            if SystemManager.depEnable:
                enableStat += 'DEPENDENCY '
            else:
                disableStat += 'DEPENDENCY '

            if SystemManager.sysEnable:
                enableStat += 'SYSCALL '
            else:
                disableStat += 'SYSCALL '

            if SystemManager.futexEnable:
                enableStat += 'FUTEX '
            else:
                disableStat += 'FUTEX '

            if SystemManager.resetEnable:
                enableStat += 'RESET '
            else:
                disableStat += 'RESET '

        # print options #
        if enableStat != '':
            SystemManager.printInfo("enabled recording options [ %s]" % enableStat)

        if disableStat != '':
            SystemManager.printInfo("disabled recording options [ %s]" % disableStat)



    @staticmethod
    def isThreadMode():
        return SystemManager.threadEnable



    @staticmethod
    def isFunctionMode():
        return SystemManager.functionEnable



    @staticmethod
    def isFileMode():
        return SystemManager.fileEnable



    @staticmethod
    def isSystemMode():
        return SystemManager.systemEnable



    @staticmethod
    def defaultHandler(signum, frame):
        return



    @staticmethod
    def stopHandler(signum, frame):
        if SystemManager.isFileMode():
            SystemManager.condExit = True
        elif SystemManager.isTopMode():
            if SystemManager.printFile is not None:
                SystemManager.printTitle()

                # submit system info #
                SystemManager.submitSystemInfo()

                # submit summarized report #
                ThreadAnalyzer.printIntervalUsage()

                # close log file to sync #
                SystemManager.fileForPrint.close()

                SystemManager.printInfo("saved top usage into %s successfully" % \
                    SystemManager.inputFile)

            if SystemManager.imageEnable:
                SystemManager.makeLogImage()

            os._exit(0)
        else:
            signal.signal(signal.SIGINT, signal.SIG_DFL)
            SystemManager.writeEvent("EVENT_STOP", False)
            SystemManager.runRecordStopCmd()

        # update record status #
        SystemManager.recordStatus = False

        SystemManager.repeatCount = 0

        SystemManager.printStatus('ready to save and analyze... [ STOP(ctrl + c) ]')



    @staticmethod
    def newHandler(signum, frame):
        SystemManager.condExit = False

        if SystemManager.isFileMode():
            SystemManager.printStatus("saved file usage successfully")
        elif SystemManager.isTopMode():
            if SystemManager.printFile is None:
                return

            SystemManager.printTitle()

            # submit system info #
            SystemManager.submitSystemInfo()

            # submit summarized report #
            ThreadAnalyzer.printIntervalUsage()

            try:
                SystemManager.fileForPrint.close()
            except:
                pass
            SystemManager.fileForPrint = None

            SystemManager.printStatus("saved top usage into %s successfully" % \
                SystemManager.inputFile)

            if SystemManager.imageEnable:
                SystemManager.makeLogImage()
        elif SystemManager.resetEnable:
            SystemManager.writeEvent("EVENT_START")
        else:
            SystemManager.writeEvent("EVENT_MARK")



    @staticmethod
    def exitHandler(signum, frame):
        SystemManager.printError('Terminated by user\n')
        os._exit(0)



    @staticmethod
    def isRelocatableFile(path):
        if path.find('.so') == -1 and \
            path.find('.ttf') == -1 and \
            path.find('.pak') == -1:
            return False
        else:
            return True



    @staticmethod
    def exitHandlerForPartInfo(signum, frame):
        for dirnames in os.walk('/sys/class/block'):
            for subdirname in dirnames[1]:
                devPath = '/sys/class/block/' + subdirname + '/dev'
                sizePath = '/sys/class/block/' + subdirname + '/size'
                devFd = open(devPath, 'r')
                sizeFd = open(sizePath, 'r')
                dev = devFd.readline().rstrip()
                size = sizeFd.readline().rstrip()



    @staticmethod
    def timerHandler(signum, frame):
        raise



    @staticmethod
    def alarmHandler(signum, frame):
        if SystemManager.pipeEnable:
            if SystemManager.repeatCount > 0:
                SystemManager.runRecordStopCmd()
                SystemManager.repeatInterval = 5
                SystemManager.repeatCount = 0
                signal.alarm(SystemManager.repeatInterval)
            else:
                sys.exit(0)
        elif SystemManager.repeatCount > 0:
            if SystemManager.outputFile != None:
                output = SystemManager.outputFile + str(SystemManager.repeatCount)
                try:
                    shutil.copy(os.path.join(SystemManager.mountPath + '../trace'), output)
                    SystemManager.printInfo('trace data is saved to %s' % output)
                except:
                    SystemManager.printWarning('Fail to save trace data to %s' % output)

                SystemManager.repeatCount -= 1
                signal.alarm(SystemManager.repeatInterval)
            else:
                SystemManager.printError('Fail to save trace data because output file is not set')
                sys.exit(0)
        else:
            sys.exit(0)



    @staticmethod
    def saveAndQuit(lines):
        # save trace data to file #
        if SystemManager.outputFile != None:
            try:
                # backup data file alread exist #
                if os.path.isfile(SystemManager.outputFile):
                    shutil.move(SystemManager.outputFile, \
                            os.path.join(SystemManager.outputFile + '.old'))

                f = open(SystemManager.outputFile, 'w')

                if SystemManager.systemInfoBuffer is not '':
                    f.writelines(SystemManager.magicString + '\n')
                    f.writelines(SystemManager.systemInfoBuffer)
                    f.writelines(SystemManager.magicString + '\n')

                f.writelines(lines)

                SystemManager.printInfo('trace data is saved to %s' % SystemManager.outputFile)
            except IOError:
                SystemManager.printError(\
                    "Fail to write trace data to %s" % SystemManager.outputFile)

            sys.exit(0)



    @staticmethod
    def writeRecordCmd(time):
        if SystemManager.rcmdList == {}:
            return

        for cmd in SystemManager.rcmdList[time]:
            path = cmd[0]
            val = cmd[1]

            try:
                with open(path, 'w') as fd:
                    fd.write(val)
                    SystemManager.printInfo(\
                        "applied command '%s' to %s successfully" % (val, path))
            except:
                SystemManager.printWarning("Fail to apply command '%s' to %s" % (val, path))



    @staticmethod
    def writeCmd(path, val, append = False):
        # set file open permission #
        if append:
            perm = 'a+'
        else:
            perm = 'w'

        # record command to file #
        if SystemManager.cmdEnable is not False:
            if SystemManager.cmdFd is None:
                try:
                    SystemManager.cmdFd = open(SystemManager.cmdEnable, perm)
                    SystemManager.cmdFd.write(SystemManager.mountCmd + ' 2>/dev/null\n')
                    SystemManager.cmdFd.write('echo "\nstart recording... [ STOP(ctrl + c) ]\n"\n')
                except:
                    SystemManager.printError("Fail to open %s to write command" %\
                            SystemManager.cmdEnable)
                    SystemManager.cmdEnable = False
            if SystemManager.cmdFd is not None:
                try:
                    cmd = 'echo "%s" > %s%s 2>/dev/null\n' %\
                        (str(val), SystemManager.mountPath, path)
                    SystemManager.cmdFd.write(cmd)
                except:
                    SystemManager.printError("Fail to write command")

        # open for applying command #
        try:
            target = '%s%s' % (SystemManager.mountPath, path)
            fd = open(target, perm)
        except:
            epath = path[0:path.rfind('/')]
            try:
                SystemManager.sysInstance.cmdList[epath] = False
            except:
                pass

            SystemManager.printWarning(\
                "Fail to use %s event, please confirm kernel configuration" % epath)
            return -1

        # apply command #
        try:
            fd.write(val)
            fd.close()
        except:
            SystemManager.printWarning("Fail to apply command '%s' to %s" % (val, path))
            return -2

        return 0



    @staticmethod
    def printProgress(current, dest):
        div = round((current / float(dest)) * 100, 1)
        percent = int(div)

        if div != percent:
            return

        mod = percent % 4

        sys.stdout.write('%3d' % percent + \
            ('% ' + SystemManager.progressChar[mod] + '\b' * 6))
        sys.stdout.flush()



    @staticmethod
    def addPrint(string, newline = 1):
        SystemManager.bufferString = "%s%s" % (SystemManager.bufferString, string)
        SystemManager.bufferRows += newline



    @staticmethod
    def clearPrint():
        del SystemManager.bufferString
        SystemManager.bufferString = ''
        SystemManager.bufferRows = 0



    @staticmethod
    def printTitle():
        if SystemManager.printFile is None:
            if sys.platform.startswith('linux'):
                sys.stdout.write("\x1b[2J\x1b[H")
            elif sys.platform.startswith('win'):
                os.system('cls')

        title = "/ g.u.i.d.e.r \tver.%s /" % __version__
        underline = '_' * (len(title))
        overline = '-' * (len(title))

        SystemManager.pipePrint(' %s\n%s\n%s' % (underline, title, overline))



    @staticmethod
    def printInfoBuffer():
        SystemManager.pipePrint(SystemManager.systemInfoBuffer)



    @staticmethod
    def parseCustomRecordCmd(cmdList):
        tempList = {'BEFORE': [], 'AFTER': [], 'STOP': []}

        if cmdList == None:
            return {}

        cmdList = cmdList.split(',')

        for item in cmdList:
            sitem = item.split(':')
            time = sitem[0]

            if len(sitem) != 3 or \
                (time != 'BEFORE' and time != 'AFTER' and time != 'STOP'):
                SystemManager.printError(\
                    "wrong format used, BEFORE|AFTER|STOP:file:value")
                sys.exit(0)

            tempList[time].append([sitem[1], sitem[2]])

        return tempList



    @staticmethod
    def removeEmptyValue(targetList):
        for val in targetList:
            if val == '':
                del targetList[targetList.index('')]



    @staticmethod
    def getMountInfo():
        # check whether there is mount info in saved buffer #
        if SystemManager.systemInfoBuffer == '':
            return
        mountPosStart = SystemManager.systemInfoBuffer.find('Disk Info')
        if mountPosStart == -1:
            return
        mountPosStart = SystemManager.systemInfoBuffer.find(oneLine, mountPosStart)
        if mountPosStart == -1:
            return
        mountPosStart = SystemManager.systemInfoBuffer.find('\n', mountPosStart)
        if mountPosStart == -1:
            return
        mountPosEnd = SystemManager.systemInfoBuffer.find(twoLine, mountPosStart)
        if mountPosEnd == -1:
            return

        init_mountData = {'dev': ' ', 'filesystem': ' ', 'mount': ' '}
        mountTable = SystemManager.systemInfoBuffer[mountPosStart:mountPosEnd].split('\n')
        for item in mountTable:
            m = re.match(r'(?P<dev>\S+)\s+(?P<maj>[0-9]+)\s+(?P<min>[0-9]+)\s+' + \
                r'(?P<readSize>[0-9]+)\s+(?P<readTime>[0-9]+)\s+(?P<writeSize>[0-9]+)\s+' + \
                r'(?P<writeTime>[0-9]+)\s+(?P<filesystem>\S+)\s+(?P<mount>.+)', item)
            if m is not None:
                d = m.groupdict()
                mid = d['maj'] + ':' + d['min']
                SystemManager.savedMountTree[mid] = dict(init_mountData)
                SystemManager.savedMountTree[mid]['dev'] = d['dev']
                SystemManager.savedMountTree[mid]['filesystem'] = d['filesystem']
                SystemManager.savedMountTree[mid]['mount'] = d['mount']



    @staticmethod
    def getProcTreeInfo():
        # check whether there is procTreeInfo in saved buffer #
        if SystemManager.systemInfoBuffer == '':
            return
        treePosStart = SystemManager.systemInfoBuffer.find('!!!!!')
        if treePosStart == -1:
            return

        # check whether there is procTreeInfo in saved buffer #
        procTree = SystemManager.systemInfoBuffer[treePosStart + len('!!!!!'):].split(',')
        for pair in procTree:
            try:
                ids = pair.split(':')
                tid = ids[0]
                pid = ids[1]
                SystemManager.savedProcTree[tid] = pid
            except:
                break

        # remove process tree info #
        SystemManager.systemInfoBuffer = SystemManager.systemInfoBuffer[:treePosStart]



    @staticmethod
    def applyLaunchOption():
        # check whether there is launch option in saved buffer #
        if SystemManager.systemInfoBuffer == '':
            return
        launchPosStart = SystemManager.systemInfoBuffer.find('Launch')
        if launchPosStart == -1:
            return
        launchPosEnd = SystemManager.systemInfoBuffer.find('\n', launchPosStart)
        if launchPosEnd == -1:
            return

        # get launch option recorded #
        SystemManager.launchBuffer = \
            SystemManager.systemInfoBuffer[launchPosStart:launchPosEnd]

        # apply arch type #
        if SystemManager.archOption is None:
            try:
                archPosStart = SystemManager.systemInfoBuffer.find('Arch')
                archPosEnd = SystemManager.systemInfoBuffer.find('\n', archPosStart)
                arch = SystemManager.systemInfoBuffer[archPosStart:archPosEnd].split()[1]
                SystemManager.setArch(arch)
            except:
                pass

        # add anlaysis option #
        archPosStart = SystemManager.systemInfoBuffer.find('Arch')
        archPosEnd = SystemManager.systemInfoBuffer.find('\n', archPosStart)
        if archPosStart >= 0 and archPosEnd >= 0:
            analOption = "{0:20} {1:<100}".format('Analysis', '# %s' % (' '.join(sys.argv)))
            SystemManager.systemInfoBuffer = '%s\n%s\n%s' % \
                (SystemManager.systemInfoBuffer[:archPosEnd], analOption, \
                SystemManager.systemInfoBuffer[archPosEnd+1:])

        # apply mode option #
        launchPosStart = SystemManager.launchBuffer.find(' -f')
        if launchPosStart > -1:
            SystemManager.functionEnable = True
            SystemManager.threadEnable = False

            SystemManager.printInfo("FUNCTION MODE")
        else:
            SystemManager.threadEnable = True
            SystemManager.printInfo("THREAD MODE")

        # apply filter option #
        filterList = None
        launchPosStart = SystemManager.launchBuffer.find(' -g')
        if SystemManager.isThreadMode() and launchPosStart > -1:
            filterList = SystemManager.launchBuffer[launchPosStart + 3:]
            filterList = filterList[:filterList.find(' -')].replace(" ", "")
            SystemManager.showGroup = filterList.split(',')
            SystemManager.removeEmptyValue(SystemManager.showGroup)
            SystemManager.printInfo("only specific threads [%s] were recorded" % \
                ', '.join(SystemManager.showGroup))

        # check filter list #
        if len(SystemManager.showGroup) > 0:
            if SystemManager.groupProcEnable is False:
                SystemManager.printInfo("only specific threads [%s] are shown" % \
                    ', '.join(SystemManager.showGroup))
            else:
                SystemManager.printInfo(\
                    "only specific threads that involved in [%s] process groups are shown" % \
                    ', '.join(SystemManager.showGroup))

        # apply dependency option #
        launchPosStart = SystemManager.launchBuffer.find(' -D')
        if launchPosStart > -1:
            SystemManager.depEnable = True

        # apply syscall option #
        launchPosStart = SystemManager.launchBuffer.find(' -t')
        if launchPosStart > -1:
            SystemManager.sysEnable = True

        # apply disable option #
        launchPosStart = SystemManager.launchBuffer.find(' -d')
        if launchPosStart > -1:
            filterList = SystemManager.launchBuffer[launchPosStart + 3:]
            filterList = filterList[:filterList.find(' -')].replace(" ", "")
            if filterList.find('u') > -1:
                SystemManager.userEnable = False
            if filterList.find('c') > -1:
                SystemManager.cpuEnable = False

        # apply enable option #
        launchPosStart = SystemManager.launchBuffer.find(' -e')
        if launchPosStart > -1:
            filterList = SystemManager.launchBuffer[launchPosStart + 3:]
            filterList = filterList[:filterList.find(' -')].replace(" ", "")
            if filterList.find('m') > -1:
                SystemManager.memEnable = True
            if filterList.find('b') > -1:
                SystemManager.blockEnable = True
            if filterList.find('h') > -1:
                SystemManager.heapEnable = True
            if filterList.find('i') > -1:
                SystemManager.irqEnable = True
            if filterList.find('n') > -1:
                SystemManager.netEnable = True

        # apply custom option #
        launchPosStart = SystemManager.launchBuffer.find(' -c')
        if launchPosStart > -1:
            filterList = SystemManager.launchBuffer[launchPosStart + 3:]
            endIdx = filterList.find(' -')
            if endIdx >= 0:
                filterList = filterList[:endIdx]
            filterList = filterList.strip().split(',')
            for idx, item in enumerate(filterList):
                tempItem = filterList[idx].split('/')
                if len(tempItem) == 2:
                    filterList[idx] = tempItem[1]
                    SystemManager.customEventList.append(tempItem[1])
                else:
                    filterList.pop(idx)
            if len(filterList) > 0:
                if SystemManager.isFunctionMode():
                    SystemManager.printInfo(\
                        "profiled custom events [ %s ], select them with -c option" % \
                        ', '.join(filterList))
                else:
                    SystemManager.printInfo(\
                        "profiled custom events [ %s ]" % ', '.join(filterList))
                    SystemManager.customCmd = filterList

        # apply user event option #
        launchPosStart = SystemManager.launchBuffer.find(' -U')
        if launchPosStart > -1:
            SystemManager.ueventEnable = True
            filterList = SystemManager.launchBuffer[launchPosStart + 3:]
            filterList = filterList[:filterList.find(' -')].replace(" ", "")
            SystemManager.userCmd = str(filterList).split(',')
            SystemManager.removeEmptyValue(SystemManager.userCmd)
            SystemManager.printInfo("profiled user events [ %s ]" % \
                ', '.join([ cmd for cmd in SystemManager.userCmd]))
            SystemManager.userEventList = \
                [ cmd.split(':')[0] for cmd in SystemManager.userCmd]

        # apply kernel event option #
        launchPosStart = SystemManager.launchBuffer.find(' -K')
        if launchPosStart > -1:
            SystemManager.keventEnable = True
            filterList = SystemManager.launchBuffer[launchPosStart + 3:]
            filterList = filterList[:filterList.find(' -')].replace(" ", "")
            SystemManager.kernelCmd = str(filterList).split(',')
            SystemManager.removeEmptyValue(SystemManager.kernelCmd)
            SystemManager.printInfo("profiled kernel events [ %s ]" % \
                ', '.join([ cmd for cmd in SystemManager.kernelCmd]))
            SystemManager.kernelEventList = \
                [ cmd.split(':')[0] for cmd in SystemManager.kernelCmd]

        # apply arch option #
        launchPosStart = SystemManager.launchBuffer.find(' -A')
        if launchPosStart > -1:
            filterList = SystemManager.launchBuffer[launchPosStart + 3:]
            filterList = filterList[:filterList.find(' -')].replace(" ", "")

            if SystemManager.arch != filterList:
                SystemManager.printError(\
                    "arch(%s) of recorded target is different with current arch(%s), use -A option with %s" % \
                    (filterList, SystemManager.arch, filterList))
                sys.exit(0)



    @staticmethod
    def writeEvent(message, show=True):
        if SystemManager.eventLogFD == None:
            if SystemManager.eventLogFile is None:
                SystemManager.eventLogFile = \
                    '%s%s' % (SystemManager.mountPath, '../trace_marker')

            try:
                SystemManager.eventLogFD = open(SystemManager.eventLogFile, 'w')
            except:
                SystemManager.printError("Fail to open %s to write event\n" % SystemManager.eventLogFile)

        if SystemManager.eventLogFD != None:
            try:
                SystemManager.eventLogFD.write(message)
                event = message[message.find('_')+1:]
                if show:
                    SystemManager.printInfo('wrote %s event' % event)
                SystemManager.eventLogFD.close()
                SystemManager.eventLogFD = None
            except:
                SystemManager.printError("Fail to write %s event\n" % (message))
        else:
            SystemManager.printError(\
                "Fail to write %s event because there is no file descriptor\n" % message)



    @staticmethod
    def infoBufferPrint(line):
        SystemManager.systemInfoBuffer = '%s%s\n' % (SystemManager.systemInfoBuffer, line)



    @staticmethod
    def clearInfoBuffer():
        SystemManager.systemInfoBuffer = ''



    @staticmethod
    def makeLogImage():
        try:
            with open(SystemManager.inputFile, 'r') as fd:
                textBuf = fd.read()
        except:
            SystemManager.printError("Fail to read log from %s\n" % SystemManager.inputFile)
            return

        # trim from process info in top mode #
        if SystemManager.isTopMode():
            textBuf = textBuf[:textBuf.find('[Top CPU Info]')]

        # make image path #
        SystemManager.imagePath = \
            SystemManager.inputFile[:SystemManager.inputFile.rfind('.')] + \
            '_' + str(long(SystemManager.uptime))

        # draw image #
        SystemManager.drawText(textBuf)



    @staticmethod
    def drawText(lines):
        imageType = None

        try:
            import textwrap
            from PIL import Image, ImageFont, ImageDraw
        except ImportError:
            err = sys.exc_info()[1]
            SystemManager.printError("Fail to import package: " + err.args[0])
            return

        try:
            # load jpeg plugin #
            from PIL import JpegImagePlugin
            imageType = 'jpg'
        except ImportError:
            err = sys.exc_info()[1]
            SystemManager.printWarning("Fail to import package: " + err.args[0])

            try:
                # load bmp plugin instead of jpeg #
                from PIL import BmpImagePlugin
                imageType = 'bmp'
            except ImportError:
                err = sys.exc_info()[1]
                SystemManager.printError("Fail to import package: " + err.args[0])
                return

        if SystemManager.imagePath is None:
            SystemManager.printError("Fail to load image path")
            return

        # set image file extention #
        SystemManager.imagePath += '.' + imageType

        if SystemManager.fontPath is not None:
            try:
                # load specific font #
                imageFont = ImageFont.truetype(SystemManager.fontPath, 10)
            except:
                SystemManager.printError("Fail to load font from %s" % SystemManager.fontPath)
                return
        else:
            try:
                # load default font #
                imageFont = ImageFont.load_default().font
            except:
                SystemManager.printError("Fail to load default font, try to use -T option")
                return

        # get default font size and image length #
        text = textwrap.fill('A', width=150)
        fontSizeX, fontSizeY = imageFont.getsize(text)

        # check input parameter #
        if type(lines) is list:
            lines = ''.join(lines)

        # convert string to list #
        lines = lines.split('\n')

        # calculate image size #
        imageSizeX = fontSizeX * SystemManager.lineLength
        imageSizeY = fontSizeY * len(lines) + (fontSizeY * 2)
        imagePosY = 1

        # make new blink image #
        if imageType is 'jpg':
            imageObject = Image.new("RGBA", (imageSizeX, imageSizeY), (255, 255, 255))
        elif imageType is 'bmp':
            imageObject = Image.new("RGB", (900, imageSizeY), (255, 255, 255))
        else:
            SystemManager.printError("No output image type")
            return

        # make palette #
        drawnImage = ImageDraw.Draw(imageObject)

        for line in lines:
            text = textwrap.fill(line, width=170)

            imagePosY += fontSizeY

            # write text on image #
            drawnImage.text((1, imagePosY), text, (0,0,0), font=imageFont)

        try:
            # save image as file #
            imageObject.save(SystemManager.imagePath)
        except:
            SystemManager.printError("Fail to save image as %s\n" % SystemManager.imagePath)
            return

        SystemManager.printStatus("saved image into %s successfully" % SystemManager.imagePath)



    @staticmethod
    def pipePrint(line):
        if SystemManager.pipeForPrint == None and SystemManager.selectMenu == None and \
            SystemManager.printFile == None and SystemManager.isTopMode() is False and \
            sys.platform.startswith('linux'):
            try:
                SystemManager.pipeForPrint = os.popen('less', 'w')
            except:
                SystemManager.printError(\
                    "Fail to find less util, use -o option to save output into file\n")
                sys.exit(0)

        if SystemManager.pipeForPrint != None:
            try:
                SystemManager.pipeForPrint.write(line + '\n')
                return
            except:
                SystemManager.printError("Fail to print to pipe\n")
                SystemManager.pipeForPrint = None

        if SystemManager.printFile != None and SystemManager.fileForPrint == None:
            if sys.platform.startswith('linux'):
                token = '/'
            else:
                token = '\\'

            if SystemManager.isRecordMode() is False and SystemManager.isTopMode() is False:
                fileNamePos = SystemManager.inputFile.rfind(token)
                if  fileNamePos >= 0:
                    SystemManager.inputFile = SystemManager.inputFile[fileNamePos + 1:]
                SystemManager.inputFile = \
                    SystemManager.printFile + token + SystemManager.inputFile.replace('dat', 'out')
            else:
                SystemManager.inputFile = SystemManager.printFile + token + 'guider.out'

            SystemManager.inputFile = SystemManager.inputFile.replace(token * 2, token)

            try:
                # backup output file #
                if os.path.isfile(SystemManager.inputFile):
                    shutil.move(\
                        SystemManager.inputFile, os.path.join(SystemManager.inputFile + '.old'))
            except:
                SystemManager.printWarning("Fail to backup %s" % SystemManager.inputFile)

            try:
                SystemManager.fileForPrint = open(SystemManager.inputFile, 'w')

                # print output file name #
                if SystemManager.printFile != None:
                    SystemManager.printInfo("write statistics to %s" % (SystemManager.inputFile))
            except:
                SystemManager.printError("Fail to open %s\n" % (SystemManager.inputFile))
                sys.exit(0)

        if SystemManager.fileForPrint != None:
            try:
                if SystemManager.isTopMode() is False:
                    SystemManager.fileForPrint.write(line + '\n')
                else:
                    SystemManager.fileForPrint.writelines(line)
            except:
                SystemManager.printError("Fail to print to file\n")
                sys.exit(0)
        else:
            print(line)



    @staticmethod
    def printWarning(line):
        if SystemManager.warningEnable:
            print('\n%s%s%s%s' % (ConfigManager.WARNING, '[Warning] ', line, ConfigManager.ENDC))



    @staticmethod
    def printError(line):
        print('\n%s%s%s%s\n' % (ConfigManager.FAIL, '[Error] ', line, ConfigManager.ENDC))



    @staticmethod
    def printInfo(line):
        print('\n%s%s%s%s' % (ConfigManager.BOLD, '[Info] ', line, ConfigManager.ENDC))



    @staticmethod
    def printGood(line):
        print('\n%s%s%s%s' % (ConfigManager.OKGREEN, '[Info] ', line, ConfigManager.ENDC))



    @staticmethod
    def printUnderline(line):
        print('\n%s%s%s' % (ConfigManager.UNDERLINE, line, ConfigManager.ENDC))



    @staticmethod
    def printStatus(line):
        print('\n%s%s%s%s' % (ConfigManager.SPECIAL, '[Step] ', line, ConfigManager.ENDC))



    @staticmethod
    def isEffectiveRequest(request):
        try:
            ThreadAnalyzer.requestType.index(request)

            if request.find('REPORT') >= 0 and SystemManager.jsonObject is None:
                try:
                    import json
                    SystemManager.jsonObject = json
                except ImportError:
                    err = sys.exc_info()[1]
                    SystemManager.printError("Fail to import package: " + err.args[0])
                    sys.exit(0)

            return True
        except SystemExit:
            sys.exit(0)
        except:
            return False



    @staticmethod
    def parseAddr(value):
        service = None
        ip = None
        port = None

        optDelimiterPos = value.find('@')
        if optDelimiterPos >= 0:
            service = value[:optDelimiterPos]
            addr = value[optDelimiterPos + 1:]
        else:
            addr = value

        addrDelimiterPos = addr.find(':')
        if addrDelimiterPos >= 0:
            try:
                ip = addr[:addrDelimiterPos]
                port = int(addr[addrDelimiterPos + 1:])
            except:
                pass
        else:
            try:
                port = int(addr)
            except:
                pass

        return (service, ip, port)



    @staticmethod
    def parseOption():
        if SystemManager.savedOptionList is not None:
            return

        usedOpt = {}
        SystemManager.savedOptionList = ' '.join(sys.argv[1:]).split(' -')[1:]
        for seq in xrange(0, len(SystemManager.savedOptionList)):
            SystemManager.savedOptionList[seq] = \
                SystemManager.savedOptionList[seq].replace(" ", "")
            try:
                usedOpt[SystemManager.savedOptionList[seq][0]]
                SystemManager.printError(\
                    "wrong -%s option because it is used more than once" %\
                        SystemManager.savedOptionList[seq][0])
                os._exit(0)
            except:
                try:
                    usedOpt[SystemManager.savedOptionList[seq][0]] = True
                except:
                    SystemManager.printError("wrong option used")
                    os._exit(0)



    @staticmethod
    def findOption(option):
        if len(sys.argv) <= 2:
            return False

        SystemManager.parseOption()

        for item in SystemManager.savedOptionList:
            if item == '':
                pass
            elif item[0] == option:
                return True

        return False



    @staticmethod
    def getOption(option):
        if len(sys.argv) <= 2:
            return False

        SystemManager.parseOption()

        for item in SystemManager.savedOptionList:
            if item == '':
                pass
            elif item[0] == option and len(item[1:]) > 0:
                return item[1:]

        return None



    @staticmethod
    def parseAnalOption():
        if len(sys.argv) <= 2:
            return

        SystemManager.optionList = ' '.join(sys.argv[1:]).split(' -')[1:]
        for seq in xrange(0, len(SystemManager.optionList)):
            SystemManager.optionList[seq] = SystemManager.optionList[seq].replace(" ", "")

        if SystemManager.findOption('v'):
            SystemManager.warningEnable = True

        for item in SystemManager.optionList:
            if item == '':
                continue

            option = item[0]
            value = item[1:]

            if option == 'i':
                if len(value) == 0:
                    SystemManager.intervalEnable = 1
                    continue

                try:
                    SystemManager.intervalEnable = int(value)

                    if SystemManager.intervalEnable <= 0:
                        SystemManager.printError(\
                            "wrong option value with -i option, input number bigger than 0")
                        sys.exit(0)
                except SystemExit:
                    sys.exit(0)
                except:
                    SystemManager.printError(\
                        "wrong option value with -i option, input number in integer format")
                    sys.exit(0)

            elif option == 'o':
                SystemManager.printFile = str(value)
                if os.path.isdir(SystemManager.printFile) == False:
                    SystemManager.printError(\
                        "wrong option value with -o option, use existing directory path")
                    sys.exit(0)

            elif option == 'I' and SystemManager.isTopMode():
                SystemManager.sourceFile = value

            elif option == 'L' and SystemManager.isTopMode() is False:
                SystemManager.customImageEnable = True

            elif option == 'a':
                SystemManager.showAll = True

            elif option == 'q':
                SystemManager.selectMenu = True
                ConfigManager.taskChainEnable = True

            elif option == 'D' and SystemManager.isTopMode() is False:
                SystemManager.depEnable = True

            elif option == 'P':
                if SystemManager.findOption('g') is False:
                    SystemManager.printError(\
                        "wrong option with -P, use also -g option to group threads as process")
                    sys.exit(0)

                SystemManager.groupProcEnable = True

            elif option == 'p' and SystemManager.isTopMode() is False:
                if SystemManager.findOption('i'):
                    SystemManager.printError("wrong option with -p, -i option is already enabled")
                    sys.exit(0)
                else:
                    SystemManager.preemptGroup = value.split(',')
                    SystemManager.removeEmptyValue(SystemManager.preemptGroup)

                    if len(SystemManager.preemptGroup) == 0:
                        SystemManager.printError(\
                            "No specific thread targeted, input tid with -p option")
                        sys.exit(0)

            elif option == 'd':
                options = value

            elif option == 'c':
                SystemManager.customCmd = str(value).split(',')
                SystemManager.removeEmptyValue(SystemManager.customCmd)

            elif option == 'g':
                SystemManager.showGroup = value.split(',')
                SystemManager.removeEmptyValue(SystemManager.showGroup)

            elif option == 'A':
                SystemManager.archOption = value
                SystemManager.setArch(value)

            elif option == 'E':
                SystemManager.errorFile = value
                SystemManager.printInfo("error log is wrote to %s" % SystemManager.errorFile)

            elif option == 'e':
                options = value
                if options.rfind('g') > -1:
                    SystemManager.graphEnable = True
                if options.rfind('d') > -1:
                    if os.geteuid() != 0:
                        SystemManager.printError("Fail to get root permission for disk analysis")
                        sys.exit(0)
                    else:
                        SystemManager.diskEnable = True
                if options.rfind('t') > -1:
                    SystemManager.processEnable = False
                if options.rfind('s') > -1:
                    if os.geteuid() != 0:
                        SystemManager.printError("Fail to get root permission for sampling stack")
                        sys.exit(0)
                    elif SystemManager.findOption('g') is False:
                        SystemManager.printError(\
                            "wrong option with -e + s, use also -g option to show stacks")
                        sys.exit(0)
                    else:
                        SystemManager.stackEnable = True
                if options.rfind('W') > -1:
                    SystemManager.wchanEnable = True
                if options.rfind('w') > -1:
                    SystemManager.wfcEnable = True
                if options.rfind('I') > -1:
                    SystemManager.imageEnable = True
                if options.rfind('f') > -1:
                    SystemManager.fileTopEnable = True
                if options.rfind('R') > -1:
                    SystemManager.reportFileEnable = True
                if options.rfind('m') > -1:
                    SystemManager.memEnable = True
                if options.rfind('r') > -1:
                    try:
                        import json
                        SystemManager.jsonObject = json
                        SystemManager.reportEnable = True
                    except ImportError:
                        err = sys.exc_info()[1]
                        SystemManager.printError("Fail to import package: " + err.args[0])
                        sys.exit(0)

            elif option == 'f' and SystemManager.isFunctionMode():
                # Handle error about record option #
                if SystemManager.outputFile is None:
                    SystemManager.printError(\
                        "wrong option with -f, use also -s option to save data")
                    sys.exit(0)
                else:
                    SystemManager.functionEnable = True

            elif option == 'l' and SystemManager.isTopMode() is False:
                SystemManager.addr2linePath = value.split(',')

            elif option == 'r' and SystemManager.isTopMode() is False:
                SystemManager.rootPath = value

            elif option == 'T':
                SystemManager.fontPath = value

            elif option == 'b':
                try:
                    bsize = int(value)
                    if bsize > 0:
                        SystemManager.bufferSize = str(value)

                        if SystemManager.isTopMode():
                            SystemManager.printInfo("set buffer size to %sKB" % (bsize * 10))
                    else:
                        SystemManager.printError(\
                            "wrong option value with -b option, input number bigger than 0")
                        sys.exit(0)
                except SystemExit:
                    sys.exit(0)
                except:
                    SystemManager.printError(\
                            "wrong option value with -b option, input number in integer format")
                    sys.exit(0)

            elif option == 'n' and SystemManager.isTopMode():
                ret = SystemManager.parseAddr(value)

                service = ret[0]
                ip = ret[1]
                port = ret[2]

                if ip is None or port is None:
                    SystemManager.printError( \
                        "wrong option value with -n option, input IP:PORT in format")
                    sys.exit(0)

                networkObject = NetworkManager('client', ip, port)
                if networkObject.ip is None:
                    sys.exit(0)
                else:
                    networkObject.status = 'ALWAYS'
                    SystemManager.addrListForPrint[ip + ':' + str(port)] = networkObject

                SystemManager.printInfo("use %s:%d as remote output address" % (ip, port))

            elif option == 'N' and SystemManager.isTopMode():
                ret = SystemManager.parseAddr(value)

                # enable report option #
                SystemManager.reportEnable = True

                service = ret[0]
                ip = ret[1]
                port = ret[2]

                if ip is None or port is None or \
                    SystemManager.isEffectiveRequest(service) is False:
                    reqList = ''
                    for req in ThreadAnalyzer.requestType:
                        if req.find('REPORT_') == 0:
                            reqList += req + '|'

                    SystemManager.printError(\
                        "wrong option value with -N option, input [%s]@IP:PORT in format" % \
                        reqList[:-1])
                    sys.exit(0)

                networkObject = NetworkManager('client', ip, port)
                if networkObject.ip is None:
                    sys.exit(0)
                else:
                    networkObject.status = 'ALWAYS'
                    networkObject.request = service
                    SystemManager.addrListForReport[ip + ':' + str(port)] = networkObject

                SystemManager.printInfo("use %s:%d as remote report address" % (ip, port))

            elif option == 'j' and SystemManager.isTopMode():
                SystemManager.reportPath = value
                SystemManager.reportPath = SystemManager.reportPath + '/guider.report'
                SystemManager.reportPath = SystemManager.reportPath.replace('//', '/')
                SystemManager.printInfo("use %s as local report file" % SystemManager.reportPath)

            elif option == 'x' and SystemManager.isTopMode():
                ret = SystemManager.parseAddr(value)

                service = ret[0]
                ip = ret[1]
                port = ret[2]

                if port is None:
                    SystemManager.printError( \
                        "wrong option value with -x option, input IP:PORT in format")
                    sys.exit(0)

                networkObject = NetworkManager('server', ip, port)
                if networkObject.ip is None:
                    sys.exit(0)
                else:
                    SystemManager.addrAsServer = networkObject

                SystemManager.printInfo("use %s:%d as server address" % \
                    (SystemManager.addrAsServer.ip, SystemManager.addrAsServer.port))

            elif option == 'X' and SystemManager.isTopMode():
                if SystemManager.findOption('x') is False:
                    SystemManager.printError(\
                        "wrong option with -X, use also -x option to request service")
                    sys.exit(0)

                # receive mode #
                if len(value) == 0:
                    SystemManager.addrOfServer = 'NONE'
                    continue
                # request mode #
                else:
                    ret = SystemManager.parseAddr(value)

                    service = ret[0]
                    ip = ret[1]
                    port = ret[2]

                    if service is None or ip is None or port is None or \
                        SystemManager.isEffectiveRequest(service) is False:
                        reqList = ''
                        for req in ThreadAnalyzer.requestType:
                            reqList += req + '|'

                        SystemManager.printError(\
                            "wrong option value with -X, input [%s]@IP:PORT as remote server address" % \
                            reqList[:-1])
                        sys.exit(0)

                networkObject = NetworkManager('client', ip, port)
                if networkObject.ip is None:
                    sys.exit(0)
                else:
                    networkObject.request = service
                    SystemManager.addrOfServer = networkObject

                SystemManager.printInfo("use %s:%d as remote server address" % (ip, port))

            elif option == 'S':
                SystemManager.sort = value
                if len(SystemManager.sort) > 0:
                    if SystemManager.sort == 'c':
                        SystemManager.printInfo("sorted by CPU")
                    elif SystemManager.sort == 'm':
                        SystemManager.printInfo("sorted by MEMORY")
                    elif SystemManager.sort == 'b':
                        SystemManager.printInfo("sorted by BLOCK")
                    elif SystemManager.sort == 'w':
                        SystemManager.wfcEnable = True
                        SystemManager.printInfo("sorted by CHILD")
                    elif SystemManager.sort == 'p':
                        SystemManager.printInfo("sorted by PID")
                    elif SystemManager.sort == 'n':
                        SystemManager.printInfo("sorted by NEW")
                    elif SystemManager.sort == 'r':
                        SystemManager.printInfo("sorted by RUNTIME")
                    else:
                        SystemManager.printError("wrong option value with -S option")
                        sys.exit(0)

            elif option == 'u':
                SystemManager.backgroundEnable = True

            elif option == 'W' or option == 'y' or option == 's' or \
                option == 'R' or option == 't' or option == 'C' or \
                option == 'v' or option == 'H' or option == 'F' or \
                option == 'U' or option == 'm' or option == 'K' or \
                option == 'w':
                continue

            else:
                SystemManager.printError("unrecognized option -%s for analysis" % option)
                sys.exit(0)

    @staticmethod
    def parseRecordOption():
        if len(sys.argv) <= 2:
            return

        SystemManager.optionList = ' '.join(sys.argv[1:]).split(' -')[1:]
        for seq in xrange(0, len(SystemManager.optionList)):
            SystemManager.optionList[seq] = SystemManager.optionList[seq].replace(" ", "")

        if SystemManager.findOption('v'):
            SystemManager.warningEnable = True

        for item in SystemManager.optionList:
            option = item[0]
            value = item[1:]

            if option == 'b':
                try:
                    bsize = int(value)
                    if bsize > 0:
                        SystemManager.bufferSize = str(value)

                        if SystemManager.isTopMode():
                            bsize *= 10

                        SystemManager.printInfo("set buffer size to %sKB" % bsize)
                    else:
                        SystemManager.printError(\
                            "wrong option value with -b option, input number bigger than 0")
                        sys.exit(0)
                except SystemExit:
                    sys.exit(0)
                except:
                    SystemManager.printError(\
                        "wrong option value with -b option, input number in integer format")
                    sys.exit(0)

            elif option == 'f':
                SystemManager.functionEnable = True

            elif option == 'u':
                SystemManager.backgroundEnable = True

            elif option == 'y':
                SystemManager.systemEnable = True

            elif option == 'A':
                SystemManager.archOption = value
                SystemManager.setArch(value)

            elif option == 'E':
                SystemManager.errorFile = value
                SystemManager.printInfo("error log is wrote to %s" % SystemManager.errorFile)

            elif option == 'e':
                options = value
                if options.rfind('i') > -1:
                    SystemManager.irqEnable = True
                if options.rfind('m') > -1:
                    SystemManager.memEnable = True
                if options.rfind('n') > -1:
                    SystemManager.netEnable = True
                if options.rfind('h') > -1:
                    SystemManager.heapEnable = True
                if options.rfind('b') > -1:
                    SystemManager.blockEnable = True
                if options.rfind('p') > -1:
                    SystemManager.pipeEnable = True
                if options.rfind('f') > -1:
                    SystemManager.futexEnable = True
                if options.rfind('r') > -1:
                    SystemManager.resetEnable = True
                if options.rfind('g') > -1:
                    SystemManager.graphEnable = True

            elif option == 'g':
                SystemManager.showGroup = value.split(',')
                SystemManager.removeEmptyValue(SystemManager.showGroup)
                if len(SystemManager.showGroup) == 0:
                    SystemManager.printError("Input value for filtering with -g option")
                    sys.exit(0)

                SystemManager.printInfo("only specific threads [%s] are recorded" % \
                    ', '.join(SystemManager.showGroup))

            elif option == 's':
                if SystemManager.isRecordMode() is False:
                    SystemManager.printError(\
                        "Fail to save data because it is not in recording mode")
                    sys.exit(0)

                SystemManager.outputFile = str(value)

                if os.path.isdir(SystemManager.outputFile):
                    SystemManager.outputFile = SystemManager.outputFile + '/guider.dat'
                elif os.path.isdir(SystemManager.outputFile[:SystemManager.outputFile.rfind('/')]):
                    continue
                else:
                    SystemManager.printError("wrong option value with -s option")
                    sys.exit(0)

                SystemManager.outputFile = SystemManager.outputFile.replace('//', '/')

            elif option == 'D':
                SystemManager.depEnable = True

            elif option == 'H':
                try:
                    SystemManager.depth = str(int(value))
                except:
                    SystemManager.printError(\
                        "wrong option value with -H option, input an integer value")
                    sys.exit(0)

            elif option == 'W':
                SystemManager.waitEnable = True

            elif option == 'w':
                SystemManager.rcmdList = SystemManager.parseCustomRecordCmd(value)

            elif option == 'U':
                SystemManager.ueventEnable = True
                SystemManager.userCmd = str(value).split(',')
                SystemManager.removeEmptyValue(SystemManager.userCmd)

            elif option == 'K':
                SystemManager.keventEnable = True
                SystemManager.kernelCmd = str(value).split(',')
                SystemManager.removeEmptyValue(SystemManager.kernelCmd)

            elif option == 'm':
                SystemManager.objdumpPath = value

            elif option == 'F':
                SystemManager.fileEnable = True

            elif option == 'C':
                SystemManager.cmdEnable = str(value)

            elif option == 't':
                SystemManager.sysEnable = True
                SystemManager.syscallList = value.split(',')
                SystemManager.removeEmptyValue(SystemManager.syscallList)
                enabledSyscall = []

                for val in SystemManager.syscallList:
                    try:
                        if val[0:4] == 'sys_':
                            nrSyscall = ConfigManager.sysList.index(val)
                        else:
                            nrSyscall = ConfigManager.sysList.index('sys_' + val)

                        enabledSyscall.append(ConfigManager.sysList[nrSyscall])
                        SystemManager.syscallList[SystemManager.syscallList.index(val)] = nrSyscall
                    except:
                        SystemManager.printError("No %s syscall in %s ABI" % (val, SystemManager.arch))
                        SystemManager.syscallList.remove(val)

                if len(enabledSyscall) == 0:
                    SystemManager.printInfo("enabled syscall list [ ALL ]")
                else:
                    SystemManager.printInfo("enabled syscall list [ %s ]" % ', '.join(enabledSyscall))

            elif option == 'R':
                repeatParams = value.split(',')
                if len(repeatParams) != 2:
                    SystemManager.printError(\
                        "wrong option value with -R, input INTERVAL,REPEAT in format")
                    sys.exit(0)
                else:
                    try:
                        SystemManager.repeatInterval = int(repeatParams[0])
                        SystemManager.repeatCount = int(repeatParams[1])
                    except:
                        SystemManager.printError("wrong option value with -R, input integer values")
                        sys.exit(0)

                if SystemManager.repeatInterval < 1 or SystemManager.repeatCount < 1:
                    SystemManager.printError("wrong option value with -R, input values bigger than 0")
                    sys.exit(0)

            elif option == 'o':
                SystemManager.printFile = str(value)

            elif option == 'c':
                SystemManager.customCmd = str(value).split(',')
                SystemManager.removeEmptyValue(SystemManager.customCmd)

            elif option == 'd':
                options = value
                if options.rfind('c') > -1:
                    SystemManager.cpuEnable = False
                if options.rfind('m') > -1:
                    SystemManager.memEnable = False
                if options.rfind('h') > -1:
                    SystemManager.heapEnable = False
                if options.rfind('b') > -1:
                    SystemManager.blockEnable = False
                if options.rfind('u') > -1:
                    SystemManager.userEnable = False

            # Ignore options #
            elif option == 'i' or option == 'a' or option == 'v' or \
                option == 'g' or option == 'p' or option == 'S' or \
                option == 'P' or option == 'T':
                continue

            else:
                SystemManager.printError("unrecognized option -%s for record" % option)
                sys.exit(0)



    @staticmethod
    def makeKerSymTable(symbol):
        try:
            f = open('/proc/kallsyms', 'r')
        except IOError:
            SystemManager.printWarning("Fail to open %s" % '/proc/kallsyms')

        ret = None
        startPos = len(SystemManager.kerSymTable)
        curPos = 0

        while 1:
            line = f.readline()
            curPos += 1

            if startPos > curPos:
                continue

            # Cache address and symbol #
            line = line.split()
            SystemManager.kerSymTable[line[2]] = line[0]

            if line[2] == symbol:
                ret = line[0]
                break

        f.close()
        return ret



    @staticmethod
    def getKerAddr(symbol):
        try:
            return SystemManager.kerSymTable[symbol]
        except:
            return SystemManager.makeKerSymTable(symbol)



    @staticmethod
    def isRecordMode():
        if sys.argv[1] == 'record':
            return True
        else:
            return False



    @staticmethod
    def isStartMode():
        if sys.argv[1] == 'start':
            return True
        else:
            return False


    @staticmethod
    def isListMode():
        if sys.argv[1] == 'list':
            return True
        else:
            return False



    @staticmethod
    def isStopMode():
        if sys.argv[1] == 'stop':
            return True
        else:
            return False


    @staticmethod
    def isSendMode():
        if sys.argv[1] == 'send':
            return True
        else:
            return False



    @staticmethod
    def isTopMode():
        if sys.argv[1] == 'top':
            return True
        else:
            return False



    @staticmethod
    def isViewMode():
        if sys.argv[1] == 'view':
            return True
        else:
            return False



    @staticmethod
    def printBackgroundProcs():
        nrProc = 0
        printBuf = ''
        myPid = str(SystemManager.pid)
        compLen = len(__module__)

        pids = os.listdir(SystemManager.procPath)
        for pid in pids:
            if myPid == pid:
                continue

            try:
                int(pid)
            except:
                continue

            # make comm path of pid #
            procPath = "%s/%s" % (SystemManager.procPath, pid)

            try:
                fd = open(procPath + '/comm', 'r')
                comm = fd.readline()[0:-1]
            except:
                continue

            if comm[0:compLen] == __module__:
                try:
                    cmdFd = open(procPath + '/cmdline', 'r')
                    cmdline = cmdFd.readline().replace("\x00", " ")
                    printBuf += '%6s\t%s\n' % (pid, cmdline)
                except:
                    continue

                nrProc += 1

        if nrProc == 0:
            SystemManager.printInfo("no running process in background")
        else:
            print('\n[Running Process]')
            print(twoLine)
            print('%6s\t%s' % ("PID", "COMMAND"))
            print(oneLine)
            print(printBuf + oneLine + '\n')



    @staticmethod
    def sendSignalProcs(nrSig, pidList):
        nrProc = 0
        myPid = str(SystemManager.pid)
        compLen = len(__module__)

        if type(pidList) is list and len(pidList) > 0:
            for pid in pidList:
                try:
                    os.kill(int(pid), nrSig)
                    SystemManager.printInfo(\
                        "sent signal %s to %s process" % \
                        (ConfigManager.sigList[nrSig-1], pid))
                except:
                    SystemManager.printError(\
                        "Fail to send signal %s to %s because of permission" % \
                        (ConfigManager.sigList[nrSig-1], pid))
            return

        commLocation = sys.argv[0].rfind('/')
        if commLocation >= 0:
            targetComm = sys.argv[0][commLocation + 1:]
        else:
            targetComm = sys.argv[0]

        pids = os.listdir(SystemManager.procPath)
        for pid in pids:
            if myPid == pid:
                continue

            try:
                int(pid)
            except:
                continue

            # make comm path of pid #
            procPath = "%s/%s" % (SystemManager.procPath, pid)

            try:
                fd = open(procPath + '/comm', 'r')
            except:
                continue

            comm = fd.readline()[0:-1]
            if comm[0:compLen] == __module__:
                if nrSig == signal.SIGINT:
                    waitStatus = False

                    try:
                        cmdFd = open(procPath + '/cmdline', 'r')
                        cmdList = cmdFd.readline().split('\x00')
                        for val in cmdList:
                            if val == '-c':
                                waitStatus = True
                    except:
                        continue

                    if SystemManager.isStartMode() and waitStatus:
                        try:
                            os.kill(int(pid), nrSig)
                            SystemManager.printInfo("started %s process to profile" % pid)
                        except:
                            SystemManager.printError(\
                                "Fail to send signal %s to %s because of permission" % \
                                (ConfigManager.sigList[nrSig-1], pid))
                    elif SystemManager.isStopMode():
                        try:
                            os.kill(int(pid), nrSig)
                            SystemManager.printInfo("terminated %s process" % pid)
                        except:
                            SystemManager.printError(\
                                "Fail to send signal %s to %s because of permission" % \
                                (ConfigManager.sigList[nrSig-1], pid))
                else:
                    try:
                        os.kill(int(pid), nrSig)
                        SystemManager.printInfo(\
                            "sent signal %s to %s process" % (ConfigManager.sigList[nrSig-1], pid))
                    except:
                        SystemManager.printError(\
                            "Fail to send signal %s to %s because of permission" % \
                            (ConfigManager.sigList[nrSig-1], pid))

                nrProc += 1

        if nrProc == 0:
            SystemManager.printInfo("no running process in background")



    @staticmethod
    def setRtPriority(pri):
        os.system('chrt -a -p %s %s 2> /dev/null &' % (pri, SystemManager.pid))



    @staticmethod
    def setIdlePriority():
        os.system('chrt -a -i -p %s %s 2> /dev/null &' % (0, SystemManager.pid))



    @staticmethod
    def setTtyCols(cols):
        os.system('stty cols %s' % (cols))



    @staticmethod
    def setTtyRows(rows):
        os.system('stty rows %s' % (rows))



    @staticmethod
    def getTty():
        try:
            SystemManager.ttyRows, SystemManager.ttyCols = \
                os.popen('stty size', 'r').read().split()
        except:
            SystemManager.printWarning("Fail to use stty")



    def saveSystemInfo(self):
        try:
            uptimeFile = '/proc/uptime'
            f = open(uptimeFile, 'r')
            self.uptimeData = f.readline()
            f.close()
        except:
            SystemManager.printWarning("Fail to open %s" % uptimeFile)

        self.uptimeData = self.uptimeData.split()
        # uptimeData[0] = running time in sec, [1]= idle time in sec * cores #

        try:
            cmdlineFile = '/proc/cmdline'
            f = open(cmdlineFile, 'r')
            self.cmdlineData = f.readline()[0:-1]
            f.close()
        except:
            SystemManager.printWarning("Fail to open %s" % cmdlineFile)

        try:
            loadFile = '/proc/loadavg'
            f = open(loadFile, 'r')
            self.loadData = f.readline()
            f.close()
        except:
            SystemManager.printWarning("Fail to open %s" % loadFile)

        self.loadData = self.loadData.split()
        '''
        loadData[0] = 1min usage, \
        [1] = 5min usage, \
        [2] = 15min usage, \
        [3] = running/total thread, \
        [4] = lastPid
        '''

        try:
            kernelVersionFile = '/proc/sys/kernel/osrelease'
            f = open(kernelVersionFile, 'r')
            self.systemInfo['kernelVer'] = f.readline().strip('\n')
            f.close()
        except:
            SystemManager.printWarning("Fail to open %s" % kernelVersionFile)

        try:
            osVersionFile = '/proc/sys/kernel/version'
            f = open(osVersionFile, 'r')
            self.systemInfo['osVer'] = f.readline().strip('\n')
            f.close()
        except:
            SystemManager.printWarning("Fail to open %s" % osVersionFile)

        try:
            osTypeFile = '/proc/sys/kernel/ostype'
            f = open(osTypeFile, 'r')
            self.systemInfo['osType'] = f.readline().strip('\n')
            f.close()
        except:
            SystemManager.printWarning("Fail to open %s" % osTypeFile)

        try:
            timeFile = '/proc/driver/rtc'
            f = open(timeFile, 'r')
            timeInfo = f.readlines()

            for val in timeInfo:
                timeEntity = val.split()

                if timeEntity[0] == 'rtc_time':
                    self.systemInfo['time'] = timeEntity[2]
                elif timeEntity[0] == 'rtc_date':
                    self.systemInfo['date'] = timeEntity[2]

            f.close()
        except:
            SystemManager.printWarning("Fail to open %s" % timeFile)



    def saveAllInfo(self):
        if SystemManager.isTopMode() is False:
            self.saveProcInfo()
        self.saveCpuInfo()
        self.saveMemInfo()
        self.saveDiskInfo()
        self.saveSystemInfo()
        self.saveWebOSInfo()



    def saveProcInfo(self):
        procTree = SystemManager.getProcTree()

        if procTree is not None:
            self.procData = '!!!!!'
            for tid, pid in procTree.items():
                self.procData += tid + ':' + pid + ','



    def saveWebOSInfo(self):
        OSFile = '/var/run/nyx/os_info.json'
        devFile = '/var/run/nyx/device_info.json'

        try:
            f = open(OSFile, 'r')
            self.osData = f.readlines()
            f.close()
        except:
            SystemManager.printWarning("Fail to open %s for webOS" % OSFile)

        try:
            f = open(devFile, 'r')
            self.devData = f.readlines()
            f.close()
        except:
            SystemManager.printWarning("Fail to open %s for webOS" % devFile)



    def saveCpuInfo(self):
        cpuFile = '/proc/cpuinfo'

        try:
            f = open(cpuFile, 'r')
            self.cpuData = f.readlines()
            f.close()
        except:
            SystemManager.printWarning("Fail to open %s" % cpuFile)



    def saveDiskInfo(self):
        diskFile = '/proc/diskstats'
        mountFile = '/proc/mounts'

        try:
            df = open(diskFile, 'r')

            if self.diskBeforeData is None:
                self.diskBeforeData = df.readlines()
            else:
                self.diskAfterData = df.readlines()

                try:
                    mf = open(mountFile, 'r')
                    self.mountData = mf.readlines()
                    mf.close()
                except:
                    SystemManager.printWarning("Fail to open %s" % mountFile)

            df.close()
        except:
            SystemManager.printWarning("Fail to open %s" % diskFile)



    def saveMemInfo(self):
        memFile = '/proc/meminfo'

        try:
            f = open(memFile, 'r')
            lines = f.readlines()

            if self.memBeforeData is None:
                self.memBeforeData = lines
            else:
                self.memAfterData = lines

            f.close()
        except:
            SystemManager.printWarning("Fail to open %s" % memFile)



    @staticmethod
    def getBufferSize():
        bufFile = "%s../buffer_size_kb" % SystemManager.mountPath

        try:
            f = open(bufFile, 'r')
            size = f.readlines()
            f.close()
        except:
            SystemManager.printWarning("Fail to open %s" % bufFile)
            return 0


        return int(size[0])



    @staticmethod
    def copyPipeToFile(pipePath, filePath):
        try:
            pd = open(pipePath, 'r')
        except:
            SystemManager.printError("Fail to open %s" % pipePath)
            sys.exit(0)

        try:
            # use os.O_DIRECT | os.O_RDWR | os.O_TRUNC | os.O_CREAT #
            fd = open(filePath, 'w')
        except:
            SystemManager.printError("Fail to open %s" % filePath)
            sys.exit(0)

        # save system information #
        si.saveAllInfo()

        while 1:
            try:
                if SystemManager.recordStatus:
                    fd.write(pd.read(SystemManager.pageSize))
                else:
                    raise
            except:
                # close files to sync disk buffer #
                pd.close()
                fd.close()

                # print system information to buffer #
                si.printAllInfoToBuf()

                rbuf = ''
                with open(SystemManager.outputFile, 'r') as fd:
                    rbuf = fd.read()

                with open(SystemManager.outputFile, 'w') as fd:
                    if SystemManager.systemInfoBuffer is not '':
                        fd.writelines(SystemManager.magicString + '\n')
                        fd.writelines(SystemManager.systemInfoBuffer)
                        fd.writelines(SystemManager.magicString + '\n')
                        fd.writelines(rbuf)

                SystemManager.printInfo(\
                    "wrote data to %s successfully" % SystemManager.outputFile)

                return



    @staticmethod
    def getMountPath():
        if SystemManager.mountPath is not None:
            return SystemManager.mountPath

        f = open('/proc/mounts', 'r')
        lines = f.readlines()

        for l in lines:
            m = re.match(r'(?P<dev>\S+)\s+(?P<dir>\S+)\s+(?P<fs>\S+)', l)
            if m is not None:
                d = m.groupdict()
                if d['fs'] == 'debugfs':
                    f.close()
                    SystemManager.mountPath = d['dir']
                    return d['dir']
        f.close()



    @staticmethod
    def clearTraceBuffer():
        SystemManager.writeCmd("../trace", '')



    def initCmdList(self):
        self.cmdList["sched/sched_switch"] = True
        self.cmdList["sched/sched_migrate_task"] = True
        self.cmdList["sched/sched_process_wait"] = True
        self.cmdList["sched/sched_process_exit"] = True
        self.cmdList["sched/sched_wakeup"] = SystemManager.depEnable
        self.cmdList["irq"] = SystemManager.irqEnable
        self.cmdList["signal"] = SystemManager.depEnable
        self.cmdList["raw_syscalls/sys_enter"] = SystemManager.depEnable
        self.cmdList["raw_syscalls/sys_exit"] = SystemManager.depEnable
        self.cmdList["raw_syscalls"] = SystemManager.sysEnable
        self.cmdList["kmem/mm_page_alloc"] = SystemManager.memEnable
        self.cmdList["kmem/mm_page_free"] = SystemManager.memEnable
        self.cmdList["kmem/kmalloc"] = SystemManager.memEnable
        self.cmdList["kmem/kfree"] = SystemManager.memEnable
        self.cmdList["filemap/mm_filemap_add_to_page_cache"] = False
        self.cmdList["filemap/mm_filemap_delete_from_page_cache"] = SystemManager.memEnable
        self.cmdList["timer/hrtimer_start"] = False
        self.cmdList["block/block_bio_remap"] = SystemManager.blockEnable
        self.cmdList["block/block_rq_complete"] = SystemManager.blockEnable
        self.cmdList["writeback/writeback_dirty_page"] = SystemManager.blockEnable
        self.cmdList["writeback/wbc_writepage"] = SystemManager.blockEnable
        self.cmdList["net/net_dev_xmit"] = SystemManager.netEnable
        self.cmdList["net/netif_receive_skb"] = SystemManager.netEnable
        self.cmdList["vmscan/mm_vmscan_direct_reclaim_begin"] = True
        self.cmdList["vmscan/mm_vmscan_direct_reclaim_end"] = True
        self.cmdList["task"] = True
        self.cmdList["signal"] = True
        self.cmdList["power/suspend_resume"] = True
        self.cmdList["printk"] = True
        self.cmdList["module/module_load"] = True
        self.cmdList["module/module_free"] = True
        self.cmdList["module/module_put"] = True
        self.cmdList["power/cpu_idle"] = True
        self.cmdList["power/cpu_frequency"] = True
        self.cmdList["vmscan/mm_vmscan_wakeup_kswapd"] = False
        self.cmdList["vmscan/mm_vmscan_kswapd_sleep"] = False
        self.cmdList["uprobes"] = SystemManager.ueventEnable
        self.cmdList["kprobes"] = SystemManager.keventEnable



    def runPeriodProc(self):
        pid = os.fork()

        if pid == 0:
            signal.signal(signal.SIGINT, 0)

            while 1:
                time.sleep(0.0001)

            sys.exit(0)



    def runRecordStartCmd(self):
        # run user command before recording #
        SystemManager.writeRecordCmd('BEFORE')

        SystemManager.mountPath = self.getMountPath()
        if SystemManager.mountPath is None:
            SystemManager.mountPath = "/sys/kernel/debug"
            SystemManager.mountCmd =\
                "mount -t debugfs nodev %s" % SystemManager.mountPath
            os.system(SystemManager.mountCmd)
        else:
            SystemManager.mountCmd =\
                "mount -t debugfs nodev %s" % SystemManager.mountPath

        SystemManager.mountPath = "%s/tracing/events/" % SystemManager.mountPath

        # check permission #
        if os.path.isdir(SystemManager.mountPath) == False:
            if os.geteuid() == 0:
                SystemManager.printError("Check whether ftrace options are enabled in kernel")
            else:
                SystemManager.printError("Fail to get root permission")

            sys.exit(0)

        # make trace buffer empty #
        self.clearTraceBuffer()

        # set size of trace buffer per core #
        SystemManager.writeCmd("../buffer_size_kb", SystemManager.bufferSize)
        setBufferSize = SystemManager.getBufferSize()
        if int(SystemManager.bufferSize) != setBufferSize:
            SystemManager.printWarning("Set buffer size(%s) is different with %s" % \
                (setBufferSize, SystemManager.bufferSize))

        # initialize event list to enable #
        self.initCmdList()

        # set log format #
        if SystemManager.graphEnable is False:
            SystemManager.writeCmd('../trace_options', 'noirq-info')
            SystemManager.writeCmd('../trace_options', 'noannotate')
            SystemManager.writeCmd('../trace_options', 'print-tgid')
            SystemManager.writeCmd('../current_tracer', 'nop')
            SystemManager.writeCmd('../tracing_on', '1')
        else:
            SystemManager.writeCmd('../tracing_on', '0')

        # FUNCTION MODE #
        if SystemManager.isFunctionMode():
            cmd = ""

            # check conditions for kernel function_graph #
            if SystemManager.graphEnable:
                if SystemManager.showGroup == []:
                    SystemManager.printError("Fail to get tid, use also -g option")
                    sys.exit(0)
                elif os.path.isfile(SystemManager.mountPath + '../set_ftrace_pid') is False:
                    SystemManager.printError("enable CONFIG_FUNCTION_GRAPH_TRACER option in kernel")
                    sys.exit(0)
                else:
                    try:
                        int(SystemManager.showGroup[0])
                    except:
                        SystemManager.printError(\
                            "wrong tid %s, input an integer value" % SystemManager.showGroup[0])
                        sys.exit(0)

                    # set target tid #
                    SystemManager.writeCmd('../set_ftrace_pid', SystemManager.showGroup[0])

                    # set function_graph tracer #
                    if SystemManager.writeCmd('../current_tracer', 'function_graph') < 0:
                        SystemManager.printError(\
                            "enable CONFIG_FUNCTION_GRAPH_TRACER option in kernel")
                        sys.exit(0)

                    SystemManager.writeCmd('../trace_options', 'nofuncgraph-proc')
                    SystemManager.writeCmd('../trace_options', 'funcgraph-abstime')
                    SystemManager.writeCmd('../trace_options', 'funcgraph-overhead')
                    SystemManager.writeCmd('../trace_options', 'funcgraph-duration')
                    SystemManager.writeCmd('../max_graph_depth', SystemManager.depth)

                    if SystemManager.customCmd is None:
                        SystemManager.writeCmd('../set_ftrace_filter', '')
                    else:
                        params = ' '.join(SystemManager.customCmd)
                        SystemManager.printStatus("wait for setting function filter [ %s ]" % params)
                        if SystemManager.writeCmd('../set_ftrace_filter', params) < 0:
                            SystemManager.printError("Fail to set function filter")
                            sys.exit(0)
                        else:
                            SystemManager.printStatus("finished function filter [ %s ]" % params)

                    SystemManager.writeCmd('../tracing_on', '1')

                    return

            # make filter command for function profiler #
            for cond in SystemManager.showGroup:
                try:
                    cmd += "common_pid == %s || " % int(cond)
                except:
                    if cond.find('>') == -1 and cond.find('<') == -1:
                        SystemManager.printError("wrong tid %s" % cond)
                        sys.exit(0)
                    else:
                        try:
                            if cond.find('>') >= 0:
                                cmd += "common_pid <= %s ||" % int(cond[:cond.find('>')])
                            elif cond.find('<') >= 0:
                                cmd += "common_pid >= %s ||" % int(cond[:cond.find('<')])
                        except:
                            SystemManager.printError("wrong condition %s" % cond)
                            sys.exit(0)

            if cmd == "":
                cmd = "(common_pid != 0)"
            else:
                cmd = "(" + cmd[:cmd.rfind('||')] + ")"

            if SystemManager.userEnable:
                SystemManager.writeCmd('../trace_options', 'userstacktrace')
                SystemManager.writeCmd('../trace_options', 'sym-userobj')
            else:
                SystemManager.writeCmd('../trace_options', 'nouserstacktrace')
                SystemManager.writeCmd('../trace_options', 'nosym-userobj')

            SystemManager.writeCmd('../trace_options', 'sym-addr')
            SystemManager.writeCmd('../options/stacktrace', '1')

            if SystemManager.cpuEnable:
                self.cmdList["timer/hrtimer_start"] = True

                addr = SystemManager.getKerAddr('tick_sched_timer')
                if addr is not None:
                    SystemManager.writeCmd(\
                        'timer/hrtimer_start/filter',\
                        '%s && function == 0x%s' % (cmd, addr))
                SystemManager.writeCmd('timer/hrtimer_start/enable', '1')
            else:
                SystemManager.writeCmd('timer/hrtimer_start/enable', '0')
                self.cmdList["timer/hrtimer_start"] = False

            if SystemManager.memEnable:
                self.cmdList["kmem/mm_page_alloc"] = True
                self.cmdList["kmem/mm_page_free"] = True
                SystemManager.writeCmd('kmem/mm_page_alloc/filter', cmd)
                SystemManager.writeCmd('kmem/mm_page_free/filter', cmd)
                SystemManager.writeCmd('kmem/mm_page_alloc/enable', '1')
                SystemManager.writeCmd('kmem/mm_page_free/enable', '1')
            else:
                SystemManager.writeCmd('kmem/mm_page_alloc/enable', '0')
                SystemManager.writeCmd('kmem/mm_page_free/enable', '0')
                self.cmdList["kmem/mm_page_alloc"] = False
                self.cmdList["kmem/mm_page_free"] = False

            if SystemManager.heapEnable:
                mmapId = ConfigManager.getMmapId()

                self.cmdList["raw_syscalls/sys_enter"] = True
                sysEnterCmd = "(id == %s || id == %s || id == %s)" % \
                    (ConfigManager.sysList.index('sys_brk'), mmapId, \
                    ConfigManager.sysList.index('sys_munmap'))
                SystemManager.writeCmd('raw_syscalls/sys_enter/filter', sysEnterCmd)
                SystemManager.writeCmd('raw_syscalls/sys_enter/enable', '1')

                self.cmdList["raw_syscalls/sys_exit"] = True
                sysExitCmd = "(id == %s || id == %s)" % \
                    (ConfigManager.sysList.index('sys_brk'), mmapId)

                SystemManager.writeCmd('raw_syscalls/sys_exit/filter', sysExitCmd)
                SystemManager.writeCmd('raw_syscalls/sys_exit/enable', '1')
            else:
                SystemManager.writeCmd('raw_syscalls/sys_enter/enable', '0')
                SystemManager.writeCmd('raw_syscalls/sys_exit/enable', '0')
                self.cmdList["raw_syscalls/sys_enter"] = False
                self.cmdList["raw_syscalls/sys_exit"] = False

            if SystemManager.blockEnable:
                self.cmdList["block/block_bio_remap"] = True
                blkCmd = cmd + " && (rwbs == R || rwbs == RA || rwbs == RM)"
                SystemManager.writeCmd('block/block_bio_remap/filter', blkCmd)
                SystemManager.writeCmd('block/block_bio_remap/enable', '1')

                self.cmdList["writeback/writeback_dirty_page"] = True
                self.cmdList["writeback/wbc_writepage"] = True
                SystemManager.writeCmd('writeback/writeback_dirty_page/filter', cmd)
                SystemManager.writeCmd('writeback/writeback_dirty_page/enable', '1')
                SystemManager.writeCmd('writeback/wbc_writepage/filter', cmd)
                SystemManager.writeCmd('writeback/wbc_writepage/enable', '1')
            else:
                self.cmdList["block/block_bio_remap"] = False
                SystemManager.writeCmd('block/block_bio_remap/enable', '0')

                self.cmdList["writeback/writeback_dirty_page"] = False
                self.cmdList["writeback/wbc_writepage"] = False
                SystemManager.writeCmd('writeback/writeback_dirty_page/enable', '0')
                SystemManager.writeCmd('writeback/wbc_writepage/enable', '0')

            self.cmdList["task"] = True
            SystemManager.writeCmd('task/enable', '1')
            self.cmdList["sched/sched_process_exit"] = True
            SystemManager.writeCmd('sched/sched_process_exit/enable', '1')

            # options for segmentation fault tracing #
            sigCmd = "sig == %d" % ConfigManager.sigList.index('SIGSEGV')
            self.cmdList["signal"] = True
            SystemManager.writeCmd('signal/filter', sigCmd)
            SystemManager.writeCmd('signal/enable', '1')

        # enable custom events #
        SystemManager.writeCustomCmd()

        # enable kernel events #
        SystemManager.writeKernelCmd()

        # enable user events #
        SystemManager.writeUserCmd()

        # FUNCTION MODE #
        if SystemManager.isFunctionMode():
            return

        # THREAD MODE #
        if SystemManager.cpuEnable:
            if self.cmdList["sched/sched_switch"]:
                if len(SystemManager.showGroup) > 0:
                    cmd = "prev_pid == 0 || next_pid == 0 || "

                    for comm in SystemManager.showGroup:
                        cmd += "prev_comm == \"*%s*\" || next_comm == \"*%s*\" || " % (comm, comm)
                        try:
                            int(comm)
                            cmd += "prev_pid == \"%s\" || next_pid == \"%s\" || " % (comm, comm)
                        except:
                            pass

                    cmd = cmd[0:cmd.rfind("||")]
                    if SystemManager.writeCmd('sched/sched_switch/filter', cmd) < 0:
                        SystemManager.printError(\
                            "Fail to set filter [ %s ]" % ' '.join(SystemManager.showGroup))
                        sys.exit(0)
                else:
                    SystemManager.writeCmd('sched/sched_switch/filter', '0')

                if SystemManager.writeCmd('sched/sched_switch/enable', '1') < 0:
                    SystemManager.printError("sched event of ftrace is not enabled in kernel")
                    sys.exit(0)

            if self.cmdList["sched/sched_wakeup"]:
                SystemManager.writeCmd('sched/sched_wakeup/enable', '1')
            if self.cmdList["sched/sched_migrate_task"]:
                SystemManager.writeCmd('sched/sched_migrate_task/enable', '1')
            if self.cmdList["sched/sched_process_exit"]:
                SystemManager.writeCmd('sched/sched_process_exit/enable', '1')
            if self.cmdList["sched/sched_process_wait"]:
                SystemManager.writeCmd('sched/sched_process_wait/enable', '1')

        # enable all irq events #
        if self.cmdList["irq"]:
            SystemManager.writeCmd('irq/enable', '1')

        # options for dependency tracing #
        if SystemManager.depEnable is False and SystemManager.futexEnable is False:
            SystemManager.writeCmd('raw_syscalls/sys_enter/filter', '0')
            SystemManager.writeCmd('raw_syscalls/sys_enter/enable', '0')
        elif SystemManager.depEnable:
            # toDo: support sys_recv systemcall for x86, x64 #
            if SystemManager.arch == 'arm':
                ecmd = \
                    "(id == %s || id == %s || id == %s || id == %s || id == %s || id == %s)" % \
                    (ConfigManager.sysList.index("sys_write"), \
                    ConfigManager.sysList.index("sys_poll"), \
                    ConfigManager.sysList.index("sys_epoll_wait"), \
                    ConfigManager.sysList.index("sys_select"), \
                    ConfigManager.sysList.index("sys_recv"), \
                    ConfigManager.sysList.index("sys_futex"))
                rcmd = \
                    "((id == %s || id == %s || id == %s || id == %s || id == %s || id == %s) && ret > 0)" % \
                    (ConfigManager.sysList.index("sys_write"), \
                    ConfigManager.sysList.index("sys_poll"), \
                    ConfigManager.sysList.index("sys_epoll_wait"), \
                    ConfigManager.sysList.index("sys_select"), \
                    ConfigManager.sysList.index("sys_recv"), \
                    ConfigManager.sysList.index("sys_futex"))

                if self.cmdList["sched/sched_switch"]:
                    SystemManager.writeCmd('sched/sched_switch/enable', '1')
                if self.cmdList["sched/sched_wakeup"]:
                    SystemManager.writeCmd('sched/sched_wakeup/enable', '1')

                SystemManager.writeCmd('raw_syscalls/sys_enter/filter', ecmd)
                SystemManager.writeCmd('raw_syscalls/sys_enter/enable', '1')
                SystemManager.writeCmd('raw_syscalls/sys_exit/filter', rcmd)
                SystemManager.writeCmd('raw_syscalls/sys_exit/enable', '1')
            else:
                SystemManager.printError(\
                    "tracing thread dependecy is not supported yet except for ARM")
                sys.exit(0)
        elif SystemManager.futexEnable:
            ecmd = "(id == %s)" % (ConfigManager.sysList.index("sys_futex"))
            SystemManager.writeCmd('raw_syscalls/sys_enter/filter', ecmd)
            SystemManager.writeCmd('raw_syscalls/sys_enter/enable', '1')
            self.cmdList["raw_syscalls/sys_enter"] = True

            rcmd = "(id == %s  && ret == 0)" % (ConfigManager.sysList.index("sys_futex"))
            SystemManager.writeCmd('raw_syscalls/sys_exit/filter', rcmd)
            SystemManager.writeCmd('raw_syscalls/sys_exit/enable', '1')
            self.cmdList["raw_syscalls/sys_exit"] = True

        # options for systemcall tracing #
        if self.cmdList["raw_syscalls"]:
            cmd = ''

            # tid filter #
            if len(SystemManager.showGroup) > 0:
                cmd += "("
                for comm in SystemManager.showGroup:
                    cmd += "common_pid == \"%s\" || " % comm
                cmd = cmd[:cmd.rfind(" ||")] + ") && "

            # syscall filter #
            if len(SystemManager.syscallList) > 0:
                cmd += "("
                for val in SystemManager.syscallList:
                    cmd += " id == %s ||" % val
                    if SystemManager.syscallList.index(val) == len(SystemManager.syscallList) - 1:
                        cmd += " id == %s)" % val
                cmd = cmd[:cmd.rfind(" ||")] + ")"
                SystemManager.writeCmd('raw_syscalls/filter', cmd)
            else:
                cmd = cmd[:cmd.rfind(" &&")]
                SystemManager.writeCmd('raw_syscalls/filter', cmd)

            if SystemManager.sysEnable and \
                len(SystemManager.showGroup) == 0 and len(SystemManager.syscallList) == 0:
                SystemManager.writeCmd('raw_syscalls/filter', '0')
                SystemManager.writeCmd('raw_syscalls/sys_enter/filter', '0')
                SystemManager.writeCmd('raw_syscalls/sys_exit/filter', '0')

            SystemManager.writeCmd('raw_syscalls/enable', '1')

        # options for signal tracing #
        if self.cmdList["signal"]:
            if SystemManager.depEnable:
                SystemManager.writeCmd('signal/enable', '1')

        # options for hibernation tracing #
        if self.cmdList["power/suspend_resume"]:
            SystemManager.writeCmd('power/suspend_resume/enable', '1')

        # options for memory tracing #
        if self.cmdList["kmem/mm_page_alloc"]:
            SystemManager.writeCmd('kmem/mm_page_alloc/enable', '1')
        if self.cmdList["kmem/mm_page_free"]:
            SystemManager.writeCmd('kmem/mm_page_free/enable', '1')
        if self.cmdList["kmem/kmalloc"]:
            SystemManager.writeCmd('kmem/kmalloc/enable', '1')
        if self.cmdList["kmem/kfree"]:
            SystemManager.writeCmd('kmem/kfree/enable', '1')
        if self.cmdList["filemap/mm_filemap_add_to_page_cache"]:
            SystemManager.writeCmd('filemap/mm_filemap_add_to_page_cache/enable', '1')
        if self.cmdList["filemap/mm_filemap_delete_from_page_cache"]:
            SystemManager.writeCmd('filemap/mm_filemap_delete_from_page_cache/enable', '1')

        # options for block tracing #
        if self.cmdList["block/block_bio_remap"]:
            cmd = "rwbs == R || rwbs == RA || rwbs == RM"
            SystemManager.writeCmd('block/block_bio_remap/filter', cmd)
            SystemManager.writeCmd('block/block_bio_remap/enable', '1')
        if self.cmdList["block/block_rq_complete"]:
            cmd = "rwbs == R || rwbs == RA || rwbs == RM"
            SystemManager.writeCmd('block/block_rq_complete/filter', cmd)
            SystemManager.writeCmd('block/block_rq_complete/enable', '1')

        # options for write event tracing #
        if self.cmdList["writeback/writeback_dirty_page"]:
            SystemManager.writeCmd('writeback/writeback_dirty_page/enable', '1')
        if self.cmdList["writeback/wbc_writepage"]:
            SystemManager.writeCmd('writeback/wbc_writepage/enable', '1')

        # options for net event tracing #
        if self.cmdList["net/net_dev_xmit"]:
            SystemManager.writeCmd('net/net_dev_xmit/enable', '1')
        if self.cmdList["net/netif_receive_skb"]:
            SystemManager.writeCmd('net/netif_receive_skb/enable', '1')

        # options for module event tracing #
        if self.cmdList["module/module_load"]:
            SystemManager.writeCmd('module/module_load/enable', '1')
        if self.cmdList["module/module_free"]:
            SystemManager.writeCmd('module/module_free/enable', '1')
        if self.cmdList["module/module_put"]:
            SystemManager.writeCmd('module/module_put/enable', '1')

        # options for power event tracing #
        if SystemManager.cpuEnable:
            if self.cmdList["power/cpu_idle"]:
                SystemManager.writeCmd('power/cpu_idle/enable', '1')
            if self.cmdList["power/cpu_frequency"]:
                SystemManager.writeCmd('power/cpu_frequency/enable', '1')

        # options for reclaim event tracing #
        if self.cmdList["vmscan/mm_vmscan_wakeup_kswapd"]:
            SystemManager.writeCmd('vmscan/mm_vmscan_wakeup_kswapd/enable', '1')
        if self.cmdList["vmscan/mm_vmscan_kswapd_sleep"]:
            SystemManager.writeCmd('vmscan/mm_vmscan_kswapd_sleep/enable', '1')

        if self.cmdList["vmscan/mm_vmscan_direct_reclaim_begin"]:
            SystemManager.writeCmd('vmscan/mm_vmscan_direct_reclaim_begin/enable', '1')
        if self.cmdList["vmscan/mm_vmscan_direct_reclaim_end"]:
            SystemManager.writeCmd('vmscan/mm_vmscan_direct_reclaim_end/enable', '1')

        # options for task event tracing #
        if self.cmdList["task"]:
            SystemManager.writeCmd('task/enable', '1')
        if self.cmdList["signal"]:
            SystemManager.writeCmd('signal/enable', '1')

        # options for printk event tracing #
        if self.cmdList["printk"]:
            SystemManager.writeCmd('printk/enable', '1')

        return



    @staticmethod
    def runRecordStopCmd():
        if SystemManager.isRecordMode() and \
            (SystemManager.isThreadMode() or SystemManager.isFunctionMode()):

            # write signal command #
            if SystemManager.cmdEnable is not False and SystemManager.cmdFd is not None:
                if SystemManager.signalCmd is not None:
                    try:
                        SystemManager.cmdFd.write(SystemManager.signalCmd)
                        SystemManager.signalCmd = None
                        SystemManager.printInfo("write commands to %s" %\
                            SystemManager.cmdEnable)
                    except:
                        SystemManager.printError("Fail to write signal command")
                elif SystemManager.outputFile is not None:
                    SystemManager.saveCmd =\
                        'cat ' + SystemManager.mountPath + '../trace > ' +\
                        SystemManager.outputFile + '\n'

            # disable all ftrace options registered #
            for idx, val in SystemManager.cmdList.items():
                if val is True:
                    SystemManager.writeCmd(str(idx) + '/enable', '0')
                    SystemManager.writeCmd(str(idx) + '/filter', '0')

            if SystemManager.graphEnable is False and SystemManager.customCmd is not None:
                for cmd in SystemManager.customCmd:
                    event = cmd.split(':')[0]
                    SystemManager.writeCmd(event + '/enable', '0')
                    SystemManager.writeCmd(event + '/filter', '0')

            if SystemManager.isFunctionMode():
                SystemManager.writeCmd('../options/stacktrace', '0')
                SystemManager.writeCmd('../trace_options', 'nouserstacktrace')
                SystemManager.writeCmd('../tracing_on', '0')

            # write save command #
            if SystemManager.saveCmd is not None:
                try:
                    SystemManager.cmdFd.write(SystemManager.saveCmd)
                    SystemManager.cmdFd.write("echo '\ntrace data is saved to %s\n'\n"\
                        % SystemManager.outputFile)
                except:
                    SystemManager.printError("Fail to write save command")

            # run user command after finishing recording #
            SystemManager.writeRecordCmd('STOP')



    def printAllInfoToBuf(self):
        self.printSystemInfo()
        self.printWebOSInfo()
        self.printCpuInfo()
        self.printMemInfo()
        self.printDiskInfo()
        self.printProcInfo()



    def printProcInfo(self):
        if self.procData is not None:
            SystemManager.infoBufferPrint(self.procData)



    def printWebOSInfo(self):
        if self.osData is None and self.devData is None:
            return

        SystemManager.infoBufferPrint('\n[System OS Info]')
        SystemManager.infoBufferPrint(twoLine)
        SystemManager.infoBufferPrint("{0:^35} {1:100}".format("TYPE", "Information"))
        SystemManager.infoBufferPrint(oneLine)

        for val in self.osData:
            try:
                val = val.split(':')
                if len(val) < 2:
                    continue
                name = val[0].replace('"', '')
                value = val[1].replace('"', '').replace('\n', '').replace(',', '')
                SystemManager.infoBufferPrint("{0:35} {1:<100}".format(name, value))
            except:
                SystemManager.printWarning("Fail to parse osData")

        for val in self.devData:
            try:
                val = val.split(':')
                if len(val) < 2:
                    continue
                name = val[0].replace('"', '')
                value = val[1].replace('"', '').replace('\n', '').replace(',', '')
                SystemManager.infoBufferPrint("{0:35} {1:<100}".format(name, value))
            except:
                SystemManager.printWarning("Fail to parse devData")

        SystemManager.infoBufferPrint(twoLine)



    def printSystemInfo(self):
        SystemManager.infoBufferPrint('\n\n[System General Info]')
        SystemManager.infoBufferPrint(twoLine)
        SystemManager.infoBufferPrint("{0:^20} {1:100}".format("TYPE", "Information"))
        SystemManager.infoBufferPrint(oneLine)

        try:
            SystemManager.infoBufferPrint("{0:20} {1:<100}".\
                format('Launch', '# ' + '%s%s' % (' '.join(sys.argv), ' -')))
        except:
            pass
        try:
            SystemManager.infoBufferPrint("{0:20} {1:<100}".\
                format('Arch', SystemManager.arch))
        except:
            pass
        try:
            SystemManager.infoBufferPrint("{0:20} {1:<100}".\
                format('Time', self.systemInfo['date'] + ' ' + self.systemInfo['time']))
        except:
            pass
        try:
            SystemManager.infoBufferPrint("{0:20} {1:<100}".format('OS', self.systemInfo['osVer']))
        except:
            pass
        try:
            SystemManager.infoBufferPrint("{0:20} {1:<100}".\
                format('Kernel', self.systemInfo['osType'] + ' ' + self.systemInfo['kernelVer']))
        except:
            pass
        try:
            RunningMin = int(float(self.uptimeData[0])) / 60
            RunningHour = RunningMin / 60
            if RunningHour > 0:
                RunningMin %= 60
            SystemManager.infoBufferPrint("{0:20} {1:<100}".\
                format('RunningTime', str(RunningHour) + ' hour  ' + str(RunningMin) + ' min'))
        except:
            pass
        try:
            SystemManager.infoBufferPrint("{0:20} {1:<10}\t/\t{2:<10}\t/\t{3:<10}".format('Load', \
                str(int(float(self.loadData[0]) * 100)) + '% (1 min)', \
                str(int(float(self.loadData[1]) * 100)) + '% (5 min)', \
                str(int(float(self.loadData[2]) * 100)) + '% (15 min)'))
        except:
            pass
        try:
            SystemManager.infoBufferPrint("{0:20} {1:<10}".format('Threads', \
                self.loadData[3] + ' (running/total)'))
        except:
            pass
        try:
            SystemManager.infoBufferPrint("{0:20} {1:<10}".format('LastPid', self.loadData[4]))
        except:
            pass
        try:
            title = 'Cmdline'
            splitLen = SystemManager.lineLength - 21
            cmdlineList = \
                [self.cmdlineData[i:i+splitLen] for i in xrange(0, len(self.cmdlineData), splitLen)]
            for string in cmdlineList:
                SystemManager.infoBufferPrint("{0:20} {1:<100}".format(title, string))
                title = ''
        except:
            pass

        SystemManager.infoBufferPrint(twoLine)

    def printCpuInfo(self):
        # parse data #
        if self.cpuData is not None:
            for l in self.cpuData:
                m = re.match(r'(?P<type>.*):\s+(?P<val>.*)', l)
                if m is not None:
                    d = m.groupdict()
                    self.cpuInfo[d['type'][0:len(d['type'])-1]] = d['val']
        else:
            return

        SystemManager.infoBufferPrint('\n[System CPU Info]')
        SystemManager.infoBufferPrint(twoLine)
        SystemManager.infoBufferPrint("{0:^20} {1:100}".format("TYPE", "Information"))
        SystemManager.infoBufferPrint(oneLine)

        try:
            SystemManager.infoBufferPrint("{0:20} {1:<100}".\
                format('Physical', int(self.cpuInfo['physical id']) + 1))
        except:
            pass
        try:
            SystemManager.infoBufferPrint("{0:20} {1:<100}".\
                format('CoresPerCPU', self.cpuInfo['cpu cores']))
        except:
            pass
        try:
            SystemManager.infoBufferPrint("{0:20} {1:<100}".\
                format('Logical', int(self.cpuInfo['processor']) + 1))
        except:
            pass

        try:
            SystemManager.infoBufferPrint("{0:20} {1:<100}".\
                format('Vendor', self.cpuInfo['vendor_id']))
        except:
            pass
        try:
            SystemManager.infoBufferPrint("{0:20} {1:<100}".\
                format('Model', self.cpuInfo['model name']))
        except:
            pass

        try:
            SystemManager.infoBufferPrint("{0:20} {1:<100}".\
                format('Cache(L2)', self.cpuInfo['cache size']))
        except:
            pass
        try:
            SystemManager.infoBufferPrint("{0:20} {1:<100}".\
                format('Perf', self.cpuInfo['bogomips']))
        except:
            pass
        try:
            SystemManager.infoBufferPrint("{0:20} {1:<100}".\
                format('Address', self.cpuInfo['address sizes']))
        except:
            pass

        SystemManager.infoBufferPrint(twoLine)



    def printDiskInfo(self):
        # parse data #
        if self.diskBeforeData is not None or self.diskAfterData is not None:
            time = 'before'
            for l in self.diskBeforeData:
                major, minor, name, readComplete, readMerge, sectorRead, readTime, \
                writeComplete, writeMerge, sectorWrite, writeTime, currentIO, ioTime, ioWTime = \
                l.split()

                name = '/dev/' + name
                self.diskInfo[time][name] = dict()
                diskInfoBuf = self.diskInfo[time][name]
                diskInfoBuf['major'] = major
                diskInfoBuf['minor'] = minor
                diskInfoBuf['readComplete'] = readComplete
                diskInfoBuf['readTime'] = readTime
                diskInfoBuf['writeComplete'] = writeComplete
                diskInfoBuf['writeTime'] = writeTime
                diskInfoBuf['currentIO'] = currentIO
                diskInfoBuf['ioTime'] = ioTime

            time = 'after'
            for l in self.diskAfterData:
                major, minor, name, readComplete, readMerge, sectorRead, readTime, \
                writeComplete, writeMerge, sectorWrite, writeTime, currentIO, ioTime, ioWTime = \
                l.split()

                name = '/dev/' + name
                self.diskInfo[time][name] = dict()
                diskInfoBuf = self.diskInfo[time][name]
                diskInfoBuf['major'] = major
                diskInfoBuf['minor'] = minor
                diskInfoBuf['readComplete'] = readComplete
                diskInfoBuf['readTime'] = readTime
                diskInfoBuf['writeComplete'] = writeComplete
                diskInfoBuf['writeTime'] = writeTime
                diskInfoBuf['currentIO'] = currentIO
                diskInfoBuf['ioTime'] = ioTime
        else:
            return

        if self.mountData is not None:
            for l in self.mountData:
                dev, path, fs, option, etc1, etc2 = l.split()

                self.mountInfo[dev] = dict()
                mountInfoBuf = self.mountInfo[dev]
                mountInfoBuf['path'] = path
                mountInfoBuf['fs'] = fs
                mountInfoBuf['option'] = option
        else:
            return

        # print disk info #
        SystemManager.infoBufferPrint('\n[System Disk Info] [ Unit: ms/KB ]')
        SystemManager.infoBufferPrint(twoLine)
        SystemManager.infoBufferPrint(\
            "{0:^16} {1:^5} {2:^5} {3:^6} {4:^6} {5:^6} {6:^6} {7:^10} {8:^20}". \
            format("Dev", "Maj", "Min", "RdSize", "RdTime", "WrSize", "WrTime", \
            "FileSystem", "MountPoint <Option>"))
        SystemManager.infoBufferPrint(oneLine)

        outputCnt = 0

        for key, val in self.mountInfo.items():
            try:
                beforeInfo = self.diskInfo['before'][key]
                afterInfo = self.diskInfo['after'][key]
                outputCnt += 1
            except:
                continue

            diskInfo = \
                "{0:<16} {1:^5} {2:^5} {3:^6} {4:^6} {5:^6} {6:^6} {7:^10} {8:<20}". \
                format(key, afterInfo['major'], afterInfo['minor'], \
                (int(afterInfo['readComplete']) - int(beforeInfo['readComplete'])) * 4, \
                (int(afterInfo['readTime']) - int(beforeInfo['readTime'])), \
                (int(afterInfo['writeComplete']) - int(beforeInfo['writeComplete'])) * 4, \
                (int(afterInfo['writeTime']) - int(beforeInfo['writeTime'])), \
                val['fs'], val['path'] + ' <' + val['option'] + '>')

            if len(diskInfo) > SystemManager.lineLength:
                try:
                    idt = ' ' * \
                        (SystemManager.lineLength - len(diskInfo[SystemManager.lineLength + 1:]))
                    diskInfo = '%s\n%s%s' %\
                        (diskInfo[:SystemManager.lineLength], idt, \
                        diskInfo[SystemManager.lineLength + 1:])
                except:
                    pass

            SystemManager.infoBufferPrint(diskInfo)

        if outputCnt == 0:
            SystemManager.infoBufferPrint('\tN/A')
        SystemManager.infoBufferPrint(twoLine + '\n\n')



    def printMemInfo(self):
        # parse data #
        if self.memBeforeData is not None or self.memAfterData is not None:
            time = 'before'
            for l in self.memBeforeData:
                m = re.match(r'(?P<type>\S+):\s+(?P<size>[0-9]+)', l)
                if m is not None:
                    d = m.groupdict()
                    self.memInfo[time][d['type']] = d['size']

            time = 'after'
            for l in self.memAfterData:
                m = re.match(r'(?P<type>\S+):\s+(?P<size>[0-9]+)', l)
                if m is not None:
                    d = m.groupdict()
                    self.memInfo[time][d['type']] = d['size']
        else:
            return

        beforeInfo = self.memInfo['before']
        afterInfo = self.memInfo['after']

        # check items for compatibility #
        try:
            beforeInfo['Shmem']
        except:
            beforeInfo['Shmem'] = '0'
            afterInfo['Shmem'] = '0'
        try:
            beforeInfo['SReclaimable']
        except:
            beforeInfo['SReclaimable'] = '0'
            afterInfo['SReclaimable'] = '0'
        try:
            beforeInfo['Sunreclaim']
        except:
            beforeInfo['Sunreclaim'] = '0'
            afterInfo['Sunreclaim'] = '0'
        try:
            beforeInfo['Mlocked']
        except:
            beforeInfo['Mlocked'] = '0'
            afterInfo['Mlocked'] = '0'

        # print memory info #
        SystemManager.infoBufferPrint('\n[System Memory Info] [ Unit: MB ]')
        SystemManager.infoBufferPrint(twoLine)
        SystemManager.infoBufferPrint(\
            "[%6s] %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s" % \
            ("DESC", "Memory", "Swap", "Buffer", "Cache", "Shared", "Mapped", \
            "Active", "Inactive", "PageTables", "Slab", "SReclaimable", "SUnreclaim", "Mlocked"))
        SystemManager.infoBufferPrint(oneLine)
        SystemManager.infoBufferPrint("[ TOTAL] %10s %10s" % \
            (int(beforeInfo['MemTotal']) >> 10, int(beforeInfo['SwapTotal']) >> 10))
        SystemManager.infoBufferPrint("[  FREE] %10s %10s" % \
            (int(beforeInfo['MemFree']) >> 10, int(beforeInfo['SwapFree']) >> 10))

        memBeforeUsage = int(beforeInfo['MemTotal']) - int(beforeInfo['MemFree'])
        swapBeforeUsage = int(beforeInfo['SwapTotal']) - int(beforeInfo['SwapFree'])
        memAfterUsage = int(afterInfo['MemTotal']) - int(afterInfo['MemFree'])
        swapAfterUsage = int(afterInfo['SwapTotal']) - int(afterInfo['SwapFree'])

        SystemManager.infoBufferPrint(\
            "[USAGE1] %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s" % \
                (memBeforeUsage >> 10, swapBeforeUsage >> 10, \
                int(beforeInfo['Buffers']) >> 10, int(beforeInfo['Cached']) >> 10, \
                int(beforeInfo['Shmem']) >> 10, int(beforeInfo['Mapped']) >> 10, \
                int(beforeInfo['Active']) >> 10, int(beforeInfo['Inactive']) >> 10, \
                int(beforeInfo['PageTables']) >> 10, int(beforeInfo['Slab']) >> 10, \
                int(beforeInfo['SReclaimable']) >> 10, int(beforeInfo['SUnreclaim']) >> 10, \
                int(beforeInfo['Mlocked']) >> 10))

        SystemManager.infoBufferPrint(\
            "[USAGE2] %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s" % \
                (memAfterUsage >> 10, swapAfterUsage >> 10, \
                int(afterInfo['Buffers']) >> 10, int(afterInfo['Cached']) >> 10, \
                int(afterInfo['Shmem']) >> 10, int(afterInfo['Mapped']) >> 10, \
                int(afterInfo['Active']) >> 10, int(afterInfo['Inactive']) >> 10, \
                int(afterInfo['PageTables']) >> 10, int(afterInfo['Slab']) >> 10, \
                int(afterInfo['SReclaimable']) >> 10, int(afterInfo['SUnreclaim']) >> 10, \
                int(afterInfo['Mlocked']) >> 10))

        SystemManager.infoBufferPrint(\
            "[  DIFF] %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s" % \
                ((memAfterUsage - memBeforeUsage ) >> 10, \
                (swapAfterUsage - swapBeforeUsage) >> 10, \
                (int(afterInfo['Buffers']) - int(beforeInfo['Buffers'])) >> 10, \
                (int(afterInfo['Cached']) - int(beforeInfo['Cached'])) >> 10, \
                (int(afterInfo['Shmem']) - int(beforeInfo['Shmem'])) >> 10, \
                (int(afterInfo['Mapped']) - int(beforeInfo['Mapped'])) >> 10, \
                (int(afterInfo['Active']) - int(beforeInfo['Active'])) >> 10, \
                (int(afterInfo['Inactive']) - int(beforeInfo['Inactive'])) >> 10, \
                (int(afterInfo['PageTables']) - int(beforeInfo['PageTables'])) >> 10, \
                (int(afterInfo['Slab']) - int(beforeInfo['Slab'])) >> 10, \
                (int(afterInfo['SReclaimable']) - int(beforeInfo['SReclaimable'])) >> 10, \
                (int(afterInfo['SUnreclaim']) - int(beforeInfo['SUnreclaim'])) >> 10, \
                (int(afterInfo['Mlocked']) - int(beforeInfo['Mlocked'])) >> 10))

        SystemManager.infoBufferPrint(twoLine)





class EventAnalyzer(object):
    """ Analyzer for event profiling """

    def __init__(self):
        self.eventData = {}



    def __del__(self):
        pass



    def addEvent(self, time, event):
        # ramdom event #
        if len(event.split('_')) == 1:
            name = event
            ID = None
        # sequantial event #
        else:
            name = event.split('_')[0]
            ID = event.split('_')[1]

        try:
            self.eventData[name]
            # {'list': [ID, time, number], 'summary': [ID, cnt, avr, min, max, first, last]} #
        except:
            self.eventData[name] = {'list': [], 'summary': []}

        self.eventData[name]['list'].append(\
            [ID, time, sum(t[0] == ID for t in self.eventData[name]['list']) + 1])

        if sum(id[0] == ID for id in self.eventData[name]['summary']) == 0:
            self.eventData[name]['summary'].append([ID, 1, -1, -1, -1, time, time])
        else:
            for n in self.eventData[name]['summary']:
                if n[0] == ID:
                    n[1] += 1
                    n[6] = time
                    break



    def printEventInfo(self, start):
        if len(self.eventData) > 0:
            SystemManager.pipePrint("\n\n\n[%s] [ Total: %d ]" % \
                ('Event Info', len(self.eventData)))
            SystemManager.pipePrint(twoLine)
            self.printEvent(start)
            SystemManager.pipePrint(twoLine)



    def printEvent(self, startTime):
        for key, value in sorted(self.eventData.items(), key=lambda e: e[1], reverse=True):
            string = ''
            head = '%10s: [total: %s] [subEvent: %s] ' % \
                (key, len(self.eventData[key]['list']), len(self.eventData[key]['summary']))
            for n in sorted(self.eventData[key]['summary'], key=lambda slist: slist[0]):
                if n[0] == None:
                    msg = head
                else:
                    msg = ' ' * len(head)

                string = \
                    '%s[%8s > cnt: %d, avr: %d, min: %d, max: %d, first: %.3f, last: %.3f]' % \
                    (msg, n[0], n[1], n[2], n[3], n[4], \
                    float(n[5]) - float(startTime), float(n[6]) - float(startTime))

                SystemManager.pipePrint("%s" % string)





class ThreadAnalyzer(object):
    """ Analyzer for thread profiling """

    reportData = {}
    procTotalData = {}
    procIntervalData = []

    # request type #
    requestType = [
        'PRINT',
        'REPORT_ALWAYS',
        'REPORT_BOUND',
    ]

    # default constant to check system status for reporting #
    reportBoundary = {
        'cpu' : {
            'total' : 80
        },
        'mem' : {
            'free' : 50
        },
        'swap' : {
            'usage' : 70
        },
        'block' : {
            'ioWait' : 10
        },
        'task' : {
            'nrCtx' : 5000
        }
    }

    init_procTotalData = {'comm': '', 'ppid': int(0), 'nrThreads': int(0), 'pri': '', \
        'startIdx': int(0), 'cpu': int(0), 'initMem': int(0), 'lastMem': int(0), \
        'memDiff': int(0), 'blk': int(0)}

    init_procIntervalData = {'cpu': int(0), 'mem': int(0), 'memDiff': int(0), 'blk': int(0)}



    def __init__(self, file):

        # thread mode #
        if file is not None:
            self.threadData = {}
            self.irqData = {}
            self.ioData = {}
            self.reclaimData = {}
            self.pageTable = {}
            self.kmemTable = {}
            self.blockTable = [{}, {}]
            self.moduleData = []
            self.intervalData = []
            self.depData = []
            self.sigData = []
            self.customEventData = []
            self.userEventData = []
            self.kernelEventData = []
            self.syscallData = []
            self.lastJob = {}
            self.preemptData = []
            self.suspendData = []
            self.markData = []
            self.consoleData = []

            self.stopFlag = False
            self.totalTime = 0
            self.totalTimeOld = 0
            self.cxtSwitch = 0
            self.nrNewTask = 0
            self.thisInterval = 0
            self.nrThread = 0
            self.nrProcess = 0

            self.threadDataOld = {}
            self.irqDataOld = {}
            self.ioDataOld = {}
            self.reclaimDataOld = {}
            self.customEventInfo = {}
            self.userEventInfo = {}
            self.kernelEventInfo = {}

            self.customInfo = {}
            self.userInfo = {}
            self.kernelInfo = {}

            self.init_threadData = {'comm': '', 'usage': float(0), 'cpuRank': int(0), \
                'yield': int(0), 'cpuWait': float(0), 'pri': '0', 'ioWait': float(0), \
                'reqBlock': int(0), 'readBlock': int(0), 'ioRank': int(0), 'irq': float(0), \
                'reclaimWait': float(0), 'reclaimCnt': int(0), 'ptid': '-'*5, 'new': ' ', \
                'die': ' ', 'preempted': int(0), 'preemption': int(0), 'start': float(0), \
                'stop': float(0), 'readQueueCnt': int(0), 'readStart': float(0), \
                'maxRuntime': float(0), 'coreSchedCnt': int(0), 'migrate': int(0), \
                'longRunCore': int(-1), 'dReclaimWait': float(0), 'dReclaimStart': float(0), \
                'dReclaimCnt': int(0), 'futexCnt': int(0), 'futexEnter': float(0), \
                'futexTotal': float(0), 'futexMax': float(0), 'lastStatus': 'N', \
                'offCnt': int(0), 'offTime': float(0), 'lastOff': float(0), 'nrPages': int(0), \
                'reclaimedPages': int(0), 'remainKmem': int(0), 'wasteKmem': int(0), \
                'kernelPages': int(0), 'childList': None, 'readBlockCnt': int(0), \
                'writeBlock': int(0), 'writeBlockCnt': int(0), 'cachePages': int(0), \
                'userPages': int(0), 'maxPreempted': float(0), 'anonReclaimedPages': int(0), \
                'lastIdleStatus': int(0), 'createdTime': float(0), 'waitStartAsParent': float(0), \
                'waitChild': float(0), 'waitParent': float(0), 'waitPid': int(0), 'tgid': '-'*5, \
                'irqList': None, 'customEvent': None, 'userEvent': None, 'kernelEvent': None, \
                'blkCore': int(0)}

            self.init_irqData = {'name': None, 'usage': float(0), 'start': float(0), \
                'max': float(0), 'min': float(0), 'maxPeriod': float(0), \
                'minPeriod': float(0), 'count': int(0)}

            self.init_intervalData = {'time': float(0), 'firstLogTime': float(0), \
                'totalUsage': float(0), 'cpuPer': float(0), 'totalMemUsage': int(0), \
                'brUsage': int(0), 'totalBrUsage': int(0), 'irqUsage': float(0), \
                'kmemUsage': int(0), 'totalKmemUsage': int(0), 'coreSchedCnt': int(0), \
                'totalCoreSchedCnt': int(0), 'preempted': float(0), 'totalBwUsage': int(0), \
                'totalPreempted': float(0), 'new': ' ', 'die': ' ', 'bwUsage': int(0), \
                'cpuUsage': float(0), 'memUsage': int(0)}

            self.init_eventData = {'count': int(0), 'start': float(0), 'usage': float(0), \
                'max': float(0), 'min': float(0), 'maxPeriod': float(0), 'minPeriod': float(0)}

            self.init_kmallocData = {'tid': '0', 'caller': '0', 'ptr': '0', 'req': int(0), \
                'alloc': int(0), 'time': '0', 'waste': int(0), 'core': int(0)}

            self.wakeupData = {'tid': '0', 'nr': '0', 'ret': '0', 'time': '0', 'args': '0', \
                'valid': int(0), 'from': '0', 'to': '0', 'corrupt': '0'}

            self.init_syscallInfo = {'usage': float(0), 'last': float(0), 'count': int(0), \
                'max': float(0), 'min': float(0)}

            self.init_pageData = {'tid': '0', 'page': '0', 'flags': '0', 'type': '0', 'time': '0'}
            self.init_lastJob = {'job': '0', 'time': '0', 'tid': '0', 'prevWakeupTid': '0'}
            self.init_preemptData = {'usage': float(0), 'count': int(0), 'max': float(0)}

            self.startTime = '0'
            self.finishTime = '0'
            self.lastTidPerCore = {}
            self.lastCore = '0'
            self.lastEvent = '0'

        # top mode #
        else:
            self.init_procData = {'isMain': bool(False), 'tids': None, 'stat': None, \
                'io': None, 'alive': False, 'runtime': float(0), 'changed': True, \
                'new': bool(False), 'majflt': long(0), 'ttime': float(0), 'cttime': float(0), \
                'utime': float(0), 'stime': float(0), 'preempted': long(0), 'taskPath': None, \
                'mainID': '', 'btime': float(0), 'read': long(0), 'write': long(0), \
                'maps': None, 'status': None, 'statm': None, 'yield': long(0)}

            self.init_cpuData = {'user': long(0), 'system': long(0), 'nice': long(0), \
                'idle': long(0), 'wait': long(0), 'irq': long(0), 'softirq': long(0)}

            self.nrThread = 0
            self.nrProcess = 0
            self.nrFd = 0
            self.procData = {}
            self.prevProcData = {}
            self.fileData = {}
            self.cpuData = {}
            self.prevCpuData = {}
            self.memData = {}
            self.vmData = {}
            self.prevVmData = {}
            self.stackTable = {}
            self.prevSwaps = None

            # set index of attributes #
            self.majfltIdx = ConfigManager.statList.index("MAJFLT")
            self.utimeIdx = ConfigManager.statList.index("UTIME")
            self.stimeIdx = ConfigManager.statList.index("STIME")
            self.cutimeIdx = ConfigManager.statList.index("CUTIME")
            self.cstimeIdx = ConfigManager.statList.index("CSTIME")
            self.btimeIdx = ConfigManager.statList.index("DELAYBLKTICK")
            self.commIdx = ConfigManager.statList.index("COMM")
            self.ppidIdx = ConfigManager.statList.index("PPID")
            self.nrthreadIdx = ConfigManager.statList.index("NRTHREAD")
            self.prioIdx = ConfigManager.statList.index("PRIORITY")
            self.policyIdx = ConfigManager.statList.index("POLICY")
            self.vsizeIdx = ConfigManager.statList.index("VSIZE")
            self.rssIdx = ConfigManager.statList.index("RSS")
            self.scodeIdx = ConfigManager.statList.index("STARTCODE")
            self.ecodeIdx = ConfigManager.statList.index("ENDCODE")
            self.statIdx = ConfigManager.statList.index("STATE")
            self.starttimeIdx = ConfigManager.statList.index("STARTTIME")
            self.shrIdx = ConfigManager.statmList.index("SHR")

            if SystemManager.graphEnable:
                # convert statistics in file to graph #
                if SystemManager.sourceFile is not None:
                    self.convertGraph(SystemManager.sourceFile)
                    sys.exit(0)
                # no path of statistics file #
                else:
                    SystemManager.printError(\
                        "wrong option with -e + g, use also -I option to load statistics data")
                    sys.exit(0)

            try:
                import resource
                SystemManager.maxFd = resource.getrlimit(getattr(resource, 'RLIMIT_NOFILE'))[0]
            except:
                SystemManager.printWarning(\
                    "Fail to get maxFd because of no resource package, use %d as default value" % \
                    SystemManager.maxFd)

            # set default interval #
            if SystemManager.intervalEnable == 0:
                SystemManager.intervalEnable = 1

            # remove wrong filter #
            if len(SystemManager.showGroup) > 0:
                for idx, val in enumerate(SystemManager.showGroup):
                    if len(val) == 0:
                        SystemManager.showGroup.pop(idx)
                    elif SystemManager.groupProcEnable:
                        try:
                            int(val)
                        except:
                            SystemManager.printError(\
                                "wrong id %s, input only integer values for grouping" % val)
                            sys.exit(0)

                taskList = ', '.join(SystemManager.showGroup)

                if SystemManager.groupProcEnable is False:
                    if SystemManager.processEnable is False:
                        SystemManager.printInfo("only specific threads [ %s ] are shown" % taskList)
                    else:
                        SystemManager.printInfo("only specific processes [ %s ] are shown" % taskList)
                else:
                    if SystemManager.processEnable is False:
                        SystemManager.printInfo(\
                            "only specific threads that are involved in a process groups [ %s ] are shown" \
                            % taskList)
                    else:
                        SystemManager.printInfo(\
                            "only specific processes that are involved in a process groups [ %s ] are shown" \
                            % taskList)

            # set configuration from file #
            self.getConf()

            if SystemManager.printFile is not None:
                SystemManager.printStatus(r"start profiling... [ STOP(ctrl + c), SAVE(ctrl + \) ]")

            # file top mode #
            if SystemManager.fileTopEnable:
                self.runFileTop()

            # request service to remote server #
            self.requestService()

            # process top mode #
            self.runProcTop()

            sys.exit(0)

        # change default cpu property #
        SystemManager.cpuEnable = False

        # initialize preempt thread list #
        if SystemManager.preemptGroup != None:
            for index in SystemManager.preemptGroup:
                # preempted state [preemptBit, threadList, startTime, core, totalUsage] #
                self.preemptData.append([False, {}, float(0), 0, float(0)])

        try:
            f = open(file, 'r')
            lines = f.readlines()
            f.close()
        except IOError:
            SystemManager.printError("Fail to open %s" % file)
            sys.exit(0)

        # save data and quit #
        SystemManager.saveAndQuit(lines)

        # get and remove process tree from data file #
        SystemManager.getProcTreeInfo()

        # start parsing logs #
        SystemManager.printStatus('start analyzing... [ STOP(ctrl + c) ]')
        SystemManager.totalLine = len(lines)

        for idx, log in enumerate(lines):
            self.parse(log)
            SystemManager.printProgress(SystemManager.curLine, SystemManager.totalLine)

            # save last job per core #
            try:
                self.lastJob[self.lastCore]
            except:
                self.lastJob[self.lastCore] = dict(self.init_lastJob)

            self.lastJob[self.lastCore]['job'] = self.lastEvent
            self.lastJob[self.lastCore]['time'] = self.finishTime

            if self.stopFlag:
                break

        # add comsumed time of jobs not finished yet to each threads #
        for idx, val in self.lastTidPerCore.items():
            if self.threadData[val]['lastStatus'] == 'S':
                # apply core off time #
                coreId = '0[%s]' % idx
                if self.threadData[coreId]['lastOff'] > 0:
                    self.threadData[coreId]['usage'] += \
                        float(self.finishTime) - self.threadData[coreId]['start']
                continue
            self.threadData[val]['usage'] += \
                (float(self.finishTime) - float(self.threadData[val]['start']))

        # add blocking time to read blocks from disk #
        if SystemManager.blockEnable:
            for idx, item in sorted(\
                self.threadData.items(), key=lambda e: e[1]['readStart'], reverse=True):
                if item['readStart'] > 0:
                    waitTime = float(self.finishTime) - item['readStart']
                    item['ioWait'] += waitTime
                    self.threadData[item['blkCore']]['ioWait'] += waitTime
                    item['readStart'] = 0
                else:
                    break

        # calculate usage of threads in last interval #
        self.processIntervalData(self.finishTime)

        if len(self.threadData) == 0:
            SystemManager.printError("No recognized data in %s" % SystemManager.inputFile)
            sys.exit(0)

        self.totalTime = round(float(self.finishTime) - float(self.startTime), 7)

        # apply filter #
        if len(SystemManager.showGroup) > 0:
            for key, value in sorted(self.threadData.items(), key=lambda e: e[1], reverse=False):
                checkResult = False
                for val in SystemManager.showGroup:
                    if value['comm'].rfind(val) > -1 or key == val:
                        checkResult = True
                    else:
                        try:
                            if SystemManager.groupProcEnable and \
                                (val == value['tgid'] or self.threadData[val]['tgid'] == value['tgid']):
                                checkResult = True
                        except:
                            pass

                # remove thread information #
                if checkResult == False and key[0:2] != '0[':
                    try:
                        del self.threadData[key]
                    except:
                        continue



    def __del__(self):
        pass



    def runFileTop(self):
        if os.geteuid() != 0:
            SystemManager.printError("Fail to get root permission")
            sys.exit(0)

        while 1:
            # collect file stats as soon as possible #
            self.saveFileStat()

            # save timestamp #
            prevTime = time.time()

            if SystemManager.printFile is None:
                SystemManager.printTitle()

            # print system status #
            self.printFileStat()

            # reset system status #
            del self.prevProcData
            self.prevProcData = self.procData
            self.procData = {}
            self.fileData = {}
            self.nrProcess = 0
            self.nrFd = 0

            # get delayed time #
            delayTime = time.time() - prevTime
            if delayTime > SystemManager.intervalEnable:
                waitTime = 0
            else:
                waitTime = SystemManager.intervalEnable - delayTime

            # wait for next interval #
            time.sleep(waitTime)



    def runProcTop(self):
        while 1:
            if SystemManager.addrOfServer is not None:
                # receive response from server #
                ret = SystemManager.addrAsServer.recv()

                # handle response from server #
                self.handleServerResponse(ret)

                continue

            # collect system stats as soon as possible #
            self.saveSystemStat()

            # save timestamp #
            prevTime = time.time()

            if self.prevProcData != {}:
                if SystemManager.printFile is None:
                    SystemManager.printTitle()

                # print system status #
                self.printSystemStat()

                # report system status #
                self.reportSystemStat()

            # reset system status #
            del self.prevProcData
            self.prevProcData = self.procData
            self.procData = {}
            self.nrThread = 0
            self.nrProcess = 0

            # get delayed time #
            delayTime = time.time() - prevTime
            if delayTime > SystemManager.intervalEnable:
                waitTime = 0
            else:
                waitTime = SystemManager.intervalEnable - delayTime

            if SystemManager.stackEnable and self.stackTable != {}:
                self.sampleStack(waitTime)
            else:
                # wait for next interval #
                time.sleep(waitTime)

            # check request from client #
            self.checkServer()



    def convertGraph(self, logFile):
        logBuf = None
        labelList = []

        timeline = []
        cpuUsage = []
        memFree = []
        swapUsage = []
        blkWait = []
        blkRead = []
        blkWrite = []
        netRead = []
        netWrite = []
        cpuProcUsage = {}
        blkProcUsage = {}

        try:
            with open(logFile, 'r') as fd:
                logBuf = fd.readlines()
        except:
            SystemManager.printError("Fail to read log from %s\n" % logFile)
            return

        # parse summary #
        interval = 0
        finalLine = 0
        compareString = '[Top CPU Info]'
        compareLen = len(compareString)
        nrStatistics = 12

        for line in logBuf:
            finalLine += 1
            summaryList = line.split('|')
            if len(summaryList) > nrStatistics:
                try:
                    idx = int(summaryList[0])
                except:
                    continue

                try:
                    timeline.append(int(float(summaryList[1].split('-')[1])))
                except:
                    timeline.append(0)
                try:
                    cpuUsage.append(int(summaryList[2]))
                except:
                    cpuUsage.append(0)
                try:
                    memFree.append(int(summaryList[3]))
                except:
                    memFree.append(0)
                try:
                    blkWait.append(int(summaryList[5]))
                except:
                    blkWait.append(0)
                try:
                    swapUsage.append(int(summaryList[6]))
                except:
                    swapUsage.append(0)
                try:
                    blkUsage = summaryList[4].split('/')
                    blkRead.append(int(blkUsage[0]))
                    blkWrite.append(int(blkUsage[1]))
                except:
                    blkRead.append(0)
                    blkWrite.append(0)
                try:
                    netstat = summaryList[12].strip().split('/')
                    if netstat[0] == '-':
                        raise

                    if netstat[0][-1] == 'M':
                        netRead.append(int(netstat[0][:-1]))
                    else:
                        netRead.append(0)
                    if netstat[1][-1] == 'M':
                        netWrite.append(int(netstat[1][:-1]))
                    else:
                        netWrite.append(0)
                except:
                    netRead.append(0)
                    netWrite.append(0)
            if line[:compareLen] == compareString:
                break

        # parse cpu usage of processes #
        compareString = '[Top Memory Info]'
        compareLen = len(compareString)
        pname = None
        pid = 0
        average = 0
        intervalList = None

        for line in logBuf[finalLine:]:
            if line[:compareLen] == compareString:
                break

            sline = line.split('|')
            slen = len(sline)

            if slen == 3:
                m = re.match(r'\s*(?P<comm>.+)\(\s*(?P<pid>[0-9]+)', line)
                if m is not None:
                    d = m.groupdict()
                    pname = d['comm'].strip() + '(' + d['pid'] + ')'
                    pid = d['pid']
                    average = int(sline[1])
                    intervalList = sline[2]
            elif slen == 2:
                if intervalList is not None:
                    intervalList += sline[1]
            elif intervalList is not None:
                # save previous info #
                cpuProcUsage[pname] = {}
                cpuProcUsage[pname]['pid'] = pid
                cpuProcUsage[pname]['average'] = average
                cpuProcUsage[pname]['usage'] = intervalList

        # parse memory usage of processes #
        compareString = '[Top Block Info]'
        compareLen = len(compareString)
        for line in logBuf[finalLine:]:
            finalLine += 1
            if line[:compareLen] == compareString:
                break

        # parse block wait of processes #
        compareString = '[Top Memory Details]'
        compareLen = len(compareString)
        pname = None
        pid = 0
        total = 0
        intervalList = None

        for line in logBuf[finalLine:]:
            if line[:compareLen] == compareString:
                break

            finalLine += 1

            sline = line.split('|')
            slen = len(sline)

            if slen == 3:
                m = re.match(r'\s*(?P<comm>.+)\(\s*(?P<pid>[0-9]+)', line)
                if m is not None:
                    d = m.groupdict()
                    pname = d['comm'].strip() + '(' + d['pid'] + ')'
                    pid = d['pid']
                    total = int(sline[1])
                    intervalList = sline[2]
            elif slen == 2:
                if intervalList is not None:
                    intervalList += sline[1]
            elif intervalList is not None:
                # save previous info #
                blkProcUsage[pname] = {}
                blkProcUsage[pname]['pid'] = pid
                blkProcUsage[pname]['total'] = total
                blkProcUsage[pname]['usage'] = intervalList

        # parse memory details of processes #
        compareString = '[Top Info]'
        compareLen = len(compareString)
        pname = None
        prop = {}
        pid = 0

        for line in logBuf[finalLine:]:
            if line[:compareLen] == compareString:
                break

            finalLine += 1

            sline = line.split('|')
            slen = len(sline)

            if slen == 12:
                m = re.match(r'\s*(?P<comm>.+)\(\s*(?P<pid>[0-9]+)', sline[0])
                if m is not None:
                    d = m.groupdict()
                    pid = d['pid']
                    pname = d['comm'].strip() + '(' + pid + ')'
                    prop[pname] = {}
                    prop[pname][sline[1].strip()] = map(int, sline[2:-1])
                elif pid > 0:
                    prop[pname][sline[1].strip()] = map(int, sline[2:-1])

        # get total size of RAM and swap #
        try:
            line = logBuf[finalLine]
        except:
            SystemManager.printError("Fail to find Detailed Statistics in %s" % logFile)
            sys.exit(0)

        strPos = line.find('[RAM')
        sline = line[strPos:].split()
        try:
            totalRAM = sline[1][:-1]
        except:
            totalRAM = None
        try:
            totalSwap = sline[3][:-1]
        except:
            totalSwap = None

        # draw graph and save it #
        try:
            self.drawGraph(timeline, labelList, cpuUsage, cpuProcUsage, blkWait,\
                blkProcUsage, blkRead, blkWrite, netRead, netWrite,\
                memFree, totalRAM, swapUsage, totalSwap)
        except:
            SystemManager.printError("Fail to draw graph while setting property")
            return
        self.saveImage(logFile, 'graph')

        # draw chart and save it #
        try:
            self.drawChart(prop)
        except:
            SystemManager.printError("Fail to draw chart while setting property")
            return
        self.saveImage(logFile, 'chart')



    def drawChart(self, data):
        seq = 0
        height = len(data) / 2
        colors = ['pink', 'lightgreen', 'skyblue', 'lightcoral', 'gold', 'yellowgreen']
        propList = ['count', 'vmem', 'rss', 'pss', 'swap', 'huge', 'locked', 'pdirty', 'sdirty']
        suptitle('guider top memory chart (ver %s)' % __version__, fontsize=8)

        def make_autopct(values):
            def autopct(pct):
                total = sum(values)
                val = int(round(pct*total/100.0))
                usage = '* {v:d}MB ({p:.0f}%)'.format(p=pct,v=val)
                line = '-' * len(usage) * 2
                string = '{s:1}\n{l:1}{d:1}'.\
                    format(s=usage,d=self.details[self.tmpCnt],l=line)
                self.tmpCnt += 1
                return string
            return autopct

        for idx, item in sorted(data.items(),\
            key=lambda e: e[1]['[TOTAL]'][propList.index('rss')] +\
            e[1]['[TOTAL]'][propList.index('swap')], reverse=True):
            labels = []
            sizes = []
            explode = []
            self.details = []
            self.tmpCnt = 0

            if item['[TOTAL]'][propList.index('count')] == 0:
                continue

            for prop, value in item.items():
                if prop != '[TOTAL]' and \
                    (value[propList.index('rss')] > 0 or value[propList.index('swap')] > 0):
                    labels.append('%s(%s)' % (prop, value[propList.index('count')]))
                    sizes.append(value[propList.index('rss')] + value[propList.index('swap')])

                    # set private dirty unit #
                    pdrt = value[propList.index('pdirty')]
                    if pdrt > 1 << 10:
                        pdrt = '%d MB' % (pdrt >> 10)
                    else:
                        pdrt = '%d KB' % (pdrt)

                    # set shared dirty unit #
                    sdrt = value[propList.index('sdirty')]
                    if sdrt > 1 << 10:
                        sdrt = '%d MB' % (sdrt >> 10)
                    else:
                        sdrt = '%d KB' % (sdrt)

                    self.details.append(\
                        '\n- RSS: %s MB\n- SWAP: %s MB\n- LOCK: %s KB\n- PDRT: %s\n- SDRT: %s' %\
                        (value[propList.index('rss')], value[propList.index('swap')],\
                        value[propList.index('locked')], pdrt, sdrt))

            # convert labels to tuple #
            labels = tuple(labels)

            # find index of max value and mark it #
            explode = [0] * len(sizes)
            explode[sizes.index(max(sizes))] = 0.03

            # set size and position of this chart #
            ypos = seq >> 1
            xpos = seq - (ypos << 1)
            ax = subplot2grid((height,2), (ypos,xpos), rowspan=1, colspan=1)
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))

            # get total size #
            line = '_' * len(idx) * 1
            rss = item['[TOTAL]'][propList.index('rss')]
            swap = item['[TOTAL]'][propList.index('swap')]
            vmem = item['[TOTAL]'][propList.index('vmem')]
            pss = item['[TOTAL]'][propList.index('pss')]
            lock = item['[TOTAL]'][propList.index('locked')]
            dirty = item['[TOTAL]'][propList.index('pdirty')] + \
                item['[TOTAL]'][propList.index('sdirty')]
            if dirty > 1 << 10:
                dirty = '%d MB' % (dirty >> 10)
            else:
                dirty = '%d KB' % (dirty)
            totalList =\
                [('\n%s\n%s\n\n- TOTAL: %s MB\n- RSS: %s MB\n- SWAP: %s MB\n%s\n\n'
                '- VIRT: %s MB\n- PSS: %s MB\n- LOCK: %s KB\n- DIRTY: %s') %\
                ('[%s] %s' % (str(seq+1), idx), line, rss+swap, \
                rss, swap, line, vmem, pss, lock, dirty)]

            # draw chart #
            patches, texts, autotexts = \
                pie(sizes, explode=explode, labels=labels, colors=colors,
                autopct=make_autopct(sizes), shadow=True, startangle=90, pctdistance=0.7)

            # set font size #
            for idx, val in enumerate(texts):
                val.set_fontsize(7)
                autotexts[idx].set_fontsize(3.5)
            axis('equal')

            # print total size in legend #
            legend(patches, totalList, loc="lower right", shadow=True,\
                fontsize=4.5, handlelength=0, bbox_to_anchor=(1.2, 0.01))

            seq += 1

        # draw image #
        figure(num=1, figsize=(10, 10), dpi=1000, facecolor='b', edgecolor='k').\
            subplots_adjust(left=0, top=0.9, bottom=0.02, hspace=0.1, wspace=0.1)



    def drawGraph(self, timeline, labelList, cpuUsage, cpuProcUsage,\
        blkWait, blkProcUsage, blkRead, blkWrite, netRead, netWrite,\
        memFree, totalRAM, swapUsage, totalSwap):
        # CPU total usage #
        ymax = 0
        ax = subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        suptitle('guider top graph (ver %s)' % __version__, fontsize=8)

        for idx, item in enumerate(blkWait):
            blkWait[idx] += cpuUsage[idx]
            if ymax < blkWait[idx]:
                ymax = blkWait[idx]

        plot(timeline, blkWait, '.-', c='pink', linewidth=3, solid_capstyle='round')
        labelList.append('[ CPU + I/O ]')
        plot(timeline, cpuUsage, '.-', c='red', linewidth=3, solid_capstyle='round')
        labelList.append('[ CPU Only ]')

        # initialize list that count the number of process using resource more than 1% #
        effectProcList = [0] * len(timeline)

        # CPU usage of processes #
        for idx, item in sorted(cpuProcUsage.items(), key=lambda e: e[1]['average'], reverse=True):
            usage = item['usage'].split()
            usage = map(int, usage)
            cpuUsage = list(usage)

            # merge cpu usage and wait time of processes #
            try:
                blkUsage = blkProcUsage[idx]['usage'].split()
                blkUsage = map(int, blkUsage)
                for interval, value in enumerate(blkUsage):
                    usage[interval] += value
            except:
                pass

            # increase effectProcList count #
            for seq, cnt in enumerate(usage):
                if cnt > 0:
                    effectProcList[seq] += 1

            # get max usage #
            maxusage = max(usage)
            if ymax < maxusage:
                ymax = maxusage

            maxIdx = usage.index(maxusage)
            color = plot(timeline, usage, '-')[0].get_color()

            ytick = yticks()[0]
            if len(ytick) > 1:
                margin = (ytick[1] - ytick[0]) / 10
            else:
                margin = 0

            maxCpuPer = str(cpuUsage[maxIdx])
            if idx in blkProcUsage:
                maxBlkPer = str(blkUsage[maxIdx])
            else:
                maxBlkPer = '0'
            maxPer = '[' + maxCpuPer + '+' + maxBlkPer + ']'
            text(timeline[maxIdx], usage[maxIdx] + margin, maxPer + idx,\
                    fontsize=3, color=color, fontweight='bold')
            labelList.append(idx)

        ylabel('CPU+I/O(%)', fontsize=8)
        legend(labelList, bbox_to_anchor=(1.12, 1.05), fontsize=3.5, loc='upper right')
        grid(which='both', linestyle=':', linewidth='0.2')
        tick_params(axis='x', direction='in')
        tick_params(axis='y', direction='in')
        xticks(fontsize=4)
        ylim([0, ymax])
        xlim([timeline[0], timeline[-1]])
        inc = ymax / 10
        if inc == 0:
            inc = 1
        yticks(xrange(0, ymax + inc, inc), fontsize=5)
        ticklabel_format(useOffset=False)
        locator_params(axis = 'x', nbins=30)
        figure(num=1, figsize=(10, 10), dpi=2000, facecolor='b', edgecolor='k').\
            subplots_adjust(left=0.06, top=0.95, bottom=0.04)
        labelList = []

        try:
            xtickLabel = ax.get_xticks().tolist()
            xlim([xtickLabel[0], xtickLabel[-1]])
            for seq, cnt in enumerate(xtickLabel):
                try:
                    xtickLabel[seq] = effectProcList[timeline.index(int(cnt))]
                except:
                    xtickLabel[seq] = ' '
            xtickLabel[-1] = '   TASK(NR)'
            ax.set_xticklabels(xtickLabel)
        except:
            pass

        # MEMORY usage #
        ax = subplot2grid((6,1), (5,0), rowspan=1, colspan=1)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        usage = map(int, memFree)
        minIdx = usage.index(min(usage))
        maxIdx = usage.index(max(usage))
        if usage[minIdx] == usage[maxIdx] == 0:
            pass
        else:
            if usage[minIdx] > 0:
                text(timeline[minIdx], usage[minIdx], usage[minIdx],\
                        fontsize=5, color='blue', fontweight='bold')
            if usage[maxIdx] > 0:
                text(timeline[maxIdx], usage[maxIdx], usage[maxIdx],\
                        fontsize=5, color='blue', fontweight='bold')
            if usage[-1] > 0:
                text(timeline[-1], usage[-1], usage[-1],\
                        fontsize=5, color='blue', fontweight='bold')
            plot(timeline, usage, '-', c='blue', linewidth=1)
            if totalRAM is not None:
                labelList.append('RAM Free (<' + totalRAM + ')')
            else:
                labelList.append('RAM Free')

        usage = map(int, swapUsage)
        minIdx = usage.index(min(usage))
        maxIdx = usage.index(max(usage))
        if usage[minIdx] == usage[maxIdx] == 0:
            pass
        else:
            if usage[minIdx] > 0:
                text(timeline[minIdx], usage[minIdx], usage[minIdx],\
                        fontsize=5, color='orange', fontweight='bold')
            if usage[maxIdx] > 0:
                text(timeline[maxIdx], usage[maxIdx], usage[maxIdx],\
                        fontsize=5, color='orange', fontweight='bold')
            if usage[-1] > 0:
                text(timeline[-1], usage[-1], usage[-1],\
                        fontsize=5, color='orange', fontweight='bold')
            plot(timeline, swapUsage, '-', c='orange', linewidth=1)
            if totalSwap is not None:
                labelList.append('Swap Usage (<' + totalSwap + ')')
            else:
                labelList.append('Swap Usage')

        usage = map(int, blkRead)
        minIdx = usage.index(min(usage))
        maxIdx = usage.index(max(usage))
        if usage[minIdx] == usage[maxIdx] == 0:
            pass
        else:
            if usage[minIdx] > 0:
                text(timeline[minIdx], usage[minIdx], usage[minIdx],\
                        fontsize=5, color='red', fontweight='bold')
            if usage[maxIdx] > 0:
                text(timeline[maxIdx], usage[maxIdx], usage[maxIdx],\
                        fontsize=5, color='red', fontweight='bold')
            if usage[-1] > 0:
                text(timeline[-1], usage[-1], usage[-1],\
                        fontsize=5, color='red', fontweight='bold')
            plot(timeline, blkRead, '-', c='red', linewidth=1)
            labelList.append('Block Read')

        usage = map(int, blkWrite)
        minIdx = usage.index(min(usage))
        maxIdx = usage.index(max(usage))
        if usage[minIdx] == usage[maxIdx] == 0:
            pass
        else:
            if usage[minIdx] > 0:
                text(timeline[minIdx], usage[minIdx], usage[minIdx],\
                        fontsize=5, color='green', fontweight='bold')
            if usage[maxIdx] > 0:
                text(timeline[maxIdx], usage[maxIdx], usage[maxIdx],\
                        fontsize=5, color='green', fontweight='bold')
            if usage[-1] > 0:
                text(timeline[-1], usage[-1], usage[-1],\
                        fontsize=5, color='green', fontweight='bold')
            plot(timeline, blkWrite, '-', c='green', linewidth=1)
            labelList.append('Block Write')

        usage = map(int, netRead)
        minIdx = usage.index(min(usage))
        maxIdx = usage.index(max(usage))
        if usage[minIdx] == usage[maxIdx] == 0:
            pass
        else:
            if usage[minIdx] > 0:
                text(timeline[minIdx], usage[minIdx], usage[minIdx],\
                        fontsize=5, color='purple', fontweight='bold')
            if usage[maxIdx] > 0:
                text(timeline[maxIdx], usage[maxIdx], usage[maxIdx],\
                        fontsize=5, color='purple', fontweight='bold')
            if usage[-1] > 0:
                text(timeline[-1], usage[-1], usage[-1],\
                        fontsize=5, color='purple', fontweight='bold')
            plot(timeline, netRead, '-', c='purple', linewidth=1)
            labelList.append('Network Recv')

        usage = map(int, netWrite)
        minIdx = usage.index(min(usage))
        maxIdx = usage.index(max(usage))
        if usage[minIdx] == usage[maxIdx] == 0:
            pass
        else:
            if usage[minIdx] > 0:
                text(timeline[minIdx], usage[minIdx], usage[minIdx],\
                        fontsize=5, color='skyblue', fontweight='bold')
            if usage[maxIdx] > 0:
                text(timeline[maxIdx], usage[maxIdx], usage[maxIdx],\
                        fontsize=5, color='skyblue', fontweight='bold')
            if usage[-1] > 0:
                text(timeline[-1], usage[-1], usage[-1],\
                        fontsize=5, color='skyblue', fontweight='bold')
            plot(timeline, netWrite, '-', c='skyblue', linewidth=1)
            labelList.append('Network Send')

        ylabel('MEMORY(MB)', fontsize=7)
        legend(labelList, bbox_to_anchor=(1.1, 0.45), fontsize=3.5, loc='upper right')
        grid(which='both', linestyle=':', linewidth='0.2')
        tick_params(axis='x', direction='in')
        tick_params(axis='y', direction='in')
        yticks(fontsize = 5)
        xticks(fontsize = 4)
        xlim([timeline[0], timeline[-1]])
        ticklabel_format(useOffset=False)
        locator_params(axis = 'x', nbins=30)
        figure(num=1, figsize=(10, 10), dpi=1000, facecolor='b', edgecolor='k')

        try:
            xtickLabel = ax.get_xticks().tolist()
            xtickLabel = map(int, xtickLabel)
            xlim([xtickLabel[0], xtickLabel[-1]])
            xtickLabel[-1] = '   TIME(Sec)'
            ax.set_xticklabels(xtickLabel)
        except:
            pass



    def saveImage(self, logFile, itype):
        try:
            # build output file name #
            outputFile = logFile

            dirPos = logFile.rfind('/')
            if dirPos < 0:
                expandPos = logFile.rfind('.')
                if expandPos < 0:
                    outputFile = 'guider.png'
                else:
                    outputFile = '%s_%s.png' % (outputFile[:expandPos], itype)
            else:
                dirPath = outputFile[:dirPos + 1]
                fileName = outputFile[dirPos + 1:]

                expandPos = fileName.rfind('.')
                if expandPos < 0:
                    outputFile = '%sguider_%s.png' % (dirPath, itype)
                else:
                    outputFile = '%s%s_%s.png' % (dirPath, fileName[:expandPos], itype)

            if SystemManager.printFile is not None:
                dirPath = os.path.dirname(SystemManager.printFile)
                if dirPath is '':
                    outputFile = SystemManager.printFile + '/' + os.path.basename(outputFile)
                else:
                    outputFile = dirPath + '/' + os.path.basename(outputFile)
        except:
            SystemManager.printError("Fail to draw image caused by wrong file path %s" % outputFile)
            return

        try:
            # save graph #
            savefig(outputFile, dpi=(300))
            clf()
            SystemManager.printStatus("write resource %s to %s" % (itype, outputFile))
        except:
            SystemManager.printError("Fail to draw image caused by save error")
            return



    def sampleStack(self, period):
        start = time.time()

        while 1:
            for idx, item in self.stackTable.items():
                try:
                    item['fd'].seek(0)
                    stack = item['fd'].read()
                except:
                    del self.stackTable[idx]

                try:
                    item['total'] += 1
                    item['stack'][stack] += 1
                except:
                    item['stack'][stack] = 1

            # set 1ms as sample rate #
            time.sleep(0.001)

            if time.time() - start >= period:
                return



    def makeTaskChainList(self):
        if ConfigManager.taskChainEnable != True:
            return

        while 1:
            eventInput = raw_input('\nInput event(file) name for taskchain: ')
            fd = ConfigManager.openConfFile(eventInput)
            if fd != None:
                break

        ConfigManager.writeConfData(fd, '[%s]\n' % (eventInput))
        threadInput = raw_input('Input id of target threads for taskchain (ex. 13,144,235): ')
        threadList = threadInput.split(',')
        ConfigManager.writeConfData(fd, 'nr_tid=' + str(len(threadList)) + '\n')

        for index, t in enumerate(threadList):
            cmdline = ConfigManager.readProcData(t, 'cmdline', 0)
            if cmdline == None:
                continue

            cmdline = cmdline[0:cmdline.find('\x00')]
            cmdline = cmdline[0:cmdline.rfind('/')]
            cmdline = cmdline.replace(' ', '-')
            if len(cmdline) > 256:
                cmdline = cmdline[0:255]

            try:
                self.threadData[t]
            except:
                SystemManager.printWarning("thread [%s] is not in profiled data" % t)
                continue

            ConfigManager.writeConfData(\
                fd, str(index) + '=' + ConfigManager.readProcData(t, 'stat', 2).replace('\x00', '-')\
                + '+' + cmdline + ' ' + str(self.threadData[t]['ioRank']) + ' ' + \
                str(self.threadData[t]['reqBlock']) + ' ' + \
                str(self.threadData[t]['cpuRank']) + ' ' + \
                str(self.threadData[t]['usage']) + '\n')

        SystemManager.pipePrint("%s.tc is written successfully" % eventInput)



    def getRunTaskNum(self):
        return len(self.threadData)



    def printCreationTree(self, tid, loc):
        childList = self.threadData[tid]['childList']
        threadName = "%s(%s)" % (self.threadData[tid]['comm'], tid)

        if self.threadData[tid]['createdTime'] > 0:
            threadName += " /%2.3f/" % (self.threadData[tid]['createdTime'] - float(self.startTime))
        if self.threadData[tid]['usage'] > 0:
            threadName += " <%2.3f>" % (self.threadData[tid]['usage'])
        if self.threadData[tid]['childList'] is not None:
            threadName += " |%d|" % (len(self.threadData[tid]['childList']))
        if self.threadData[tid]['waitChild'] > 0:
            threadName += " {%1.3f}" % (self.threadData[tid]['waitChild'])
        if self.threadData[tid]['waitParent'] > 0:
            threadName += " [%1.3f]" % (self.threadData[tid]['waitParent'])

        # set new position of line #
        newLoc = loc + 5

        if self.threadData[tid]['die'] == ' ':
            life = '+ '
        else:
            life = '- '

        SystemManager.pipePrint(' ' * loc + life + threadName)

        if childList != None:
            for thread in childList:
                self.printCreationTree(thread, newLoc)



    @staticmethod
    def getCoreId(string):
        try:
            offset = string.rfind('/')
            if offset >= 0:
                return int(string[offset+1:])
            else:
                return -1
        except:
            return -1



    def printComInfo(self):
        # print thread tree by creation #
        if SystemManager.showAll and len(SystemManager.showGroup) == 0 and self.nrNewTask > 0:
            SystemManager.clearPrint()
            SystemManager.pipePrint('\n' + \
                '[Thread Creation Info] [Alive: +] [Die: -] [CreatedTime: //] [ChildCount: ||] ' + \
                '[CpuUsage: <>] [WaitTimeForChilds: {}] [WaitTimeOfParent: []]')
            SystemManager.pipePrint(twoLine)

            for key, value in sorted(\
                self.threadData.items(), key=lambda e: e[1]['waitChild'], reverse=True):
                # print tree from root threads #
                if value['childList'] is not None and value['new'] is ' ':
                    self.printCreationTree(key, 0)
            SystemManager.pipePrint(oneLine)

        # print signal traffic #
        if SystemManager.showAll and len(self.sigData) > 0:
            SystemManager.clearPrint()
            SystemManager.pipePrint('\n' + '[Thread Signal Info]')
            SystemManager.pipePrint(twoLine)
            SystemManager.pipePrint("{0:^6} {1:^16} {2:>10}({3:>5}) {4:^10} {5:>16}({6:>5})".\
                format('TYPE', 'TIME', 'SENDER', 'TID', 'SIGNAL', 'RECEIVER', 'TID'))
            SystemManager.pipePrint(twoLine)

            for val in self.sigData:
                try:
                    ConfigManager.sigList[int(val[6])]
                except:
                    continue

                if val[0] == 'SEND':
                    SystemManager.pipePrint(\
                        "{0:^6} {1:>10.6f} {2:>16}({3:>5}) {4:^10} {5:>16}({6:>5})".\
                        format(val[0], val[1], val[2], val[3], \
                        ConfigManager.sigList[int(val[6])], val[4], val[5]))
                elif val[0] == 'RECV':
                    SystemManager.pipePrint(\
                        "{0:^6} {1:>10.6f} {2:>16} {3:>5}  {4:^10} {5:>16}({6:>5})".\
                        format(val[0], val[1], ' ', ' ', \
                        ConfigManager.sigList[int(val[6])], val[4], val[5]))
            SystemManager.pipePrint(oneLine)

        # print interrupt information #
        if len(self.irqData) > 0:
            totalCnt = int(0)
            totalUsage = float(0)

            SystemManager.pipePrint('\n' + '[Thread IRQ Info]')
            SystemManager.pipePrint(twoLine)
            SystemManager.pipePrint(\
                "{0:^16}({1:^62}): {2:^12} {3:^10} {4:^10} {5:^10} {6:^10} {7:^10}".\
                format("IRQ", "Name", "Count", "Usage", "ProcMax", \
                "ProcMin", "InterMax", "InterMin"))
            SystemManager.pipePrint(twoLine)

            SystemManager.clearPrint()
            for key in sorted(self.irqData.keys()):
                totalCnt += self.irqData[key]['count']
                totalUsage += self.irqData[key]['usage']
                SystemManager.addPrint(\
                    ("{0:>16}({1:^62}): {2:>12} {3:^10.6f} {4:^10.6f} "
                    "{5:^10.6f} {6:^10.6f} {7:^10.6f}\n").\
                    format(key, ' | '.join(self.irqData[key]['name'].keys()), \
                    self.irqData[key]['count'], self.irqData[key]['usage'], \
                    self.irqData[key]['max'], self.irqData[key]['min'], \
                    self.irqData[key]['maxPeriod'], self.irqData[key]['minPeriod']))

            SystemManager.pipePrint("%s# IRQ(%d) / Total(%6.3f) / Cnt(%d)\n" % \
                ('', len(self.irqData), totalUsage, totalCnt))
            SystemManager.pipePrint(SystemManager.bufferString)
            SystemManager.pipePrint(oneLine)



    def printEventInfo(self):
        # pick up event info from thread info #
        for key, value in sorted(self.threadData.items()):
            if value['customEvent'] is not None:
                self.customInfo[key] = value['customEvent']
            if value['userEvent'] is not None:
                self.userInfo[key] = value['userEvent']
            if value['kernelEvent'] is not None:
                self.kernelInfo[key] = value['kernelEvent']

        # print custom event info #
        if len(self.customEventInfo) > 0:
            SystemManager.clearPrint()
            SystemManager.pipePrint('\n' + '[Thread CUSTOM Event Info]')
            SystemManager.pipePrint(twoLine)
            SystemManager.pipePrint(\
                "{0:^32} {1:>16}({2:^5}) {3:>10} {4:>10} {5:>10}".\
                format('Event', 'Comm', 'Tid', 'Count', 'MaxPeriod', 'MinPeriod'))
            SystemManager.pipePrint(twoLine)

            newLine = False
            for idx, val in sorted(\
                self.customEventInfo.items(), key=lambda e: e[1]['count'], reverse=True):
                if newLine:
                    SystemManager.pipePrint("")
                else:
                    newLine = True

                SystemManager.pipePrint("{0:^32} {1:>16}({2:^5}) {3:>10} {4:>10.6f} {5:>10.6f}".\
                    format(idx, 'TOTAL', '-', val['count'], val['maxPeriod'], val['minPeriod']))
                for key, value in sorted(self.customInfo.items(), \
                    key=lambda e: 0 if not idx in e[1] else e[1][idx], reverse=True):
                    try:
                        SystemManager.pipePrint(\
                            "{0:^32} {1:>16}({2:>5}) {3:>10} {4:>10.6f} {5:>10.6f}".\
                            format(' ', self.threadData[key]['comm'], key, value[idx]['count'], \
                            value[idx]['maxPeriod'], value[idx]['minPeriod']))
                    except:
                        pass
            SystemManager.pipePrint(oneLine)

        # print custom event history #
        if SystemManager.showAll and len(self.customEventData) > 0:
            SystemManager.clearPrint()
            SystemManager.pipePrint('\n' + '[Thread CUSTOM Event History]')
            SystemManager.pipePrint(twoLine)
            SystemManager.pipePrint("{0:^32} {1:^10} {2:>16}({3:>5}) {4:<1}".\
                format('EVENT', 'TIME', 'COMM', 'TID', 'ARG'))
            SystemManager.pipePrint(twoLine)

            cnt = 0
            callTable = {}
            for val in self.customEventData:
                # apply filter #
                if SystemManager.showGroup != [] and not val[2] in SystemManager.showGroup:
                    continue

                SystemManager.pipePrint(\
                    "{0:^32} {1:>10.6f} {2:>16}({3:>5}) {4:<1}".\
                    format(val[0], val[3], val[1], val[2], val[4]))
                cnt += 1
            if cnt == 0:
                SystemManager.pipePrint("\tNone")
            SystemManager.pipePrint(oneLine)

        # print user event info #
        if len(self.userEventInfo) > 0:
            SystemManager.clearPrint()
            SystemManager.pipePrint('\n' + '[Thread USER Event Info]')
            SystemManager.pipePrint(twoLine)
            SystemManager.pipePrint(\
                "{0:^32} {1:>16}({2:^5}) {3:>10} {4:>10} {5:>10} {6:>10} {7:>10} {8:>10}".\
                format('Event', 'Comm', 'Tid', 'Usage', 'Count', \
                'ProcMax', 'ProcMin', 'InterMax', 'InterMin'))
            SystemManager.pipePrint(twoLine)

            newLine = False
            for idx, val in sorted(\
                self.userEventInfo.items(), key=lambda e: e[1]['usage'], reverse=True):
                if newLine:
                    SystemManager.pipePrint("")
                else:
                    newLine = True
                SystemManager.pipePrint(\
                    ("{0:^32} {1:>16}({2:^5}) {3:>10.6f} {4:>10} {5:>10.6f} "
                    "{6:>10.6f} {7:>10.6f} {8:>10.6f}").\
                    format(idx, 'TOTAL', '-', val['usage'], val['count'], val['max'], val['min'], \
                    val['maxPeriod'], val['minPeriod']))
                for key, value in sorted(self.userInfo.items(), \
                    key=lambda e: 0 if not idx in e[1] else e[1][idx]['usage'], reverse=True):
                    try:
                        SystemManager.pipePrint(\
                            ("{0:^32} {1:>16}({2:>5}) {3:>10.6f} {4:>10} {5:>10.6f} "
                            "{6:>10.6f} {7:>10.6f} {8:>10.6f}").\
                            format(' ', self.threadData[key]['comm'], key, value[idx]['usage'], \
                            value[idx]['count'], value[idx]['max'], value[idx]['min'], \
                            value[idx]['maxPeriod'], value[idx]['minPeriod']))
                    except:
                        pass
            SystemManager.pipePrint(oneLine)

        # print user event history #
        if SystemManager.showAll and len(self.userEventData) > 0:
            SystemManager.clearPrint()
            SystemManager.pipePrint('\n' + '[Thread USER Event History]')
            SystemManager.pipePrint(twoLine)
            SystemManager.pipePrint("{0:^32} {1:^6} {2:^10} {3:>16}({4:>5}) {5:^16} {6:>10}".\
                format('EVENT', 'TYPE', 'TIME', 'COMM', 'TID', 'CALLER', 'ELAPSED'))
            SystemManager.pipePrint(twoLine)

            cnt = 0
            callTable = {}
            for val in self.userEventData:
                elapsed = '-'
                # apply filter #
                if SystemManager.showGroup != [] and not val[3] in SystemManager.showGroup:
                    continue
                elif val[0] == 'ENTER':
                    cid = '%s%s' % (val[1], val[3])
                    callTable[cid] = val[4]
                elif val[0] == 'EXIT':
                    cid = '%s%s' % (val[1], val[3])
                    try:
                        elapsed = '%.6f' % (val[4] - callTable[cid])
                    except:
                        pass

                SystemManager.pipePrint(\
                    "{0:^32} {1:>6} {2:>10.6f} {3:>16}({4:>5}) {5:>16} {6:>10}".\
                    format(val[1], val[0], val[4], val[2], val[3], val[5], elapsed))
                cnt += 1
            if cnt == 0:
                SystemManager.pipePrint("\tNone")
            SystemManager.pipePrint(oneLine)

        # print kernel event info #
        if len(self.kernelEventInfo) > 0:
            SystemManager.clearPrint()
            SystemManager.pipePrint('\n' + '[Thread KERNEL Event Info]')
            SystemManager.pipePrint(twoLine)
            SystemManager.pipePrint(\
                "{0:^32} {1:>16}({2:^5}) {3:>10} {4:>10} {5:>10} {6:>10} {7:>10} {8:>10}".\
                format('Event', 'Comm', 'Tid', 'Usage', 'Count', 'ProcMax', \
                'ProcMin', 'InterMax', 'InterMin'))
            SystemManager.pipePrint(twoLine)

            newLine = False
            for idx, val in sorted(\
                self.kernelEventInfo.items(), key=lambda e: e[1]['usage'], reverse=True):
                if newLine:
                    SystemManager.pipePrint("")
                else:
                    newLine = True
                SystemManager.pipePrint(\
                    ("{0:^32} {1:>16}({2:^5}) {3:>10.6f} {4:>10} {5:>10.6f} "
                    "{6:>10.6f} {7:>10.6f} {8:>10.6f}").\
                    format(idx, 'TOTAL', '-', val['usage'], val['count'], val['max'], val['min'], \
                    val['maxPeriod'], val['minPeriod']))
                for key, value in sorted(self.kernelInfo.items(), \
                    key=lambda e: 0 if not idx in e[1] else e[1][idx]['usage'], reverse=True):
                    try:
                        SystemManager.pipePrint(\
                            ("{0:^32} {1:>16}({2:>5}) {3:>10.6f} {4:>10} {5:>10.6f} "
                            "{6:>10.6f} {7:>10.6f} {8:>10.6f}").\
                            format(' ', self.threadData[key]['comm'], key, value[idx]['usage'], \
                            value[idx]['count'], value[idx]['max'], value[idx]['min'], \
                            value[idx]['maxPeriod'], value[idx]['minPeriod']))
                    except:
                        pass
            SystemManager.pipePrint(oneLine)

        # print kernel event history #
        if SystemManager.showAll and len(self.kernelEventData) > 0:
            SystemManager.clearPrint()
            SystemManager.pipePrint('\n' + '[Thread KERNEL Event History]')
            SystemManager.pipePrint(twoLine)
            SystemManager.pipePrint(\
                "{0:^32} {1:^6} {2:^10} {3:>16}({4:>5}) {5:^22} {6:>10} {7:<1}".\
                format('EVENT', 'TYPE', 'TIME', 'COMM', 'TID', 'CALLER', 'ELAPSED', 'ARG'))
            SystemManager.pipePrint(twoLine)

            cnt = 0
            callTable = {}
            for val in self.kernelEventData:
                elapsed = '-'
                # apply filter #
                if SystemManager.showGroup != [] and not val[4] in SystemManager.showGroup:
                    continue
                elif val[0] == 'ENTER':
                    cid = '%s%s' % (val[1], val[4])
                    callTable[cid] = val[5]
                elif val[0] == 'EXIT':
                    cid = '%s%s' % (val[1], val[4])
                    try:
                        elapsed = '%.6f' % (val[5] - callTable[cid])
                    except:
                        pass

                args = (' '.join(val[7].split(' arg'))).replace('=','>')
                SystemManager.pipePrint(\
                    "{0:^32} {1:>6} {2:>10.6f} {3:>16}({4:>5}) {5:>22} {6:>10} {7:<1}".\
                    format(val[1], val[0], val[5], val[3], val[4], val[6], elapsed, args))
                cnt += 1
            if cnt == 0:
                SystemManager.pipePrint("\tNone")
            SystemManager.pipePrint(oneLine)



    def printUsage(self):
        SystemManager.printTitle()

        # print system information #
        SystemManager.printInfoBuffer()

        # print menu #
        SystemManager.pipePrint(("[%s] [ %s: %0.3f ] [ %s: %0.3f ] [ Running: %d ] " + \
            "[ CtxSwc: %d ] [ LogSize: %d KB ] [ Unit: Sec/MB ]") % \
            ('Thread Info', 'Elapsed', round(float(self.totalTime), 7), \
            'Start', round(float(self.startTime), 7), \
            self.getRunTaskNum(), self.cxtSwitch, SystemManager.logSize >> 10))
        SystemManager.pipePrint(twoLine)

        SystemManager.pipePrint("{0:_^32}|{1:_^35}|{2:_^22}|{3:_^26}|{4:_^34}|".\
            format("Thread Info", "CPU Info", "SCHED Info", "BLOCK Info", "MEM Info"))
        SystemManager.pipePrint("{0:^32}|{1:^35}|{2:^22}|{3:^26}|{4:^34}|".\
            format("", "", "", "", "", ""))

        SystemManager.pipePrint(("%16s(%5s/%5s)|%2s|%5s(%5s)|%5s(%5s)|%3s|%5s|" + \
            "%5s|%5s|%5s|%4s|%5s(%3s/%5s)|%4s(%3s)|%4s(%3s|%3s|%3s)|%3s|%3s|%4s(%2s)|") % \
            ('Name', 'Tid', 'Pid', 'LF', 'Usage', '%', 'Delay', 'Max', 'Pri', ' IRQ ', \
            'Yld', ' Lose', 'Steal', 'Mig', 'Read', 'MB', 'Cnt', 'WCnt', 'MB', \
            'Sum', 'Usr', 'Buf', 'Ker', 'Rcl', 'Wst', 'DRcl', 'Nr'))
        SystemManager.pipePrint(twoLine)

        # initialize swapper thread per core #
        for n in xrange(0, SystemManager.maxCore + 1):
            try:
                coreId = '0[%s]' % n
                self.threadData[coreId]
            except:
                self.threadData[coreId] = dict(self.init_threadData)
                self.threadData[coreId]['comm'] = 'swapper/' + str(n)
                self.threadData[coreId]['usage'] = 0

        # sort by size of io usage and convert read blocks to MB size #
        count = 0
        for key, value in sorted(\
            self.threadData.items(), key=lambda e: e[1]['readBlock'], reverse=True):
            value['ioRank'] = count + 1
            if value['readBlock'] > 0:
                value['readBlock'] = (value['readBlock'] * SystemManager.blockSize) >> 20
                count += 1
            if value['writeBlock'] > 0:
                value['writeBlock'] = (value['writeBlock'] * SystemManager.pageSize) >> 20

        # print total information after sorting by time of cpu usage #
        count = 0
        SystemManager.clearPrint()
        for key, value in sorted(self.threadData.items(), \
            key=lambda e: ThreadAnalyzer.getCoreId(e[1]['comm']), reverse=False):
            if key[0:2] == '0[':
                # change the name of swapper thread to CORE #
                value['comm'] = value['comm'].replace("swapper", "CORE")

                # modify idle time if this core is not woke up #
                if value['usage'] == 0 and value['coreSchedCnt'] == 0:
                    value['usage'] = self.totalTime

                # calculate total core usage percentage #
                try:
                    usagePercent = \
                        100 - (round(float(value['usage']) / float(self.totalTime), 7) * 100)
                except:
                    usagePercent = 0

                if value['lastOff'] > 0:
                    value['offTime'] += float(self.finishTime) - value['lastOff']

                SystemManager.addPrint(\
                    ("%16s(%5s/%5s)|%s%s|%5.2f(%5s)|%5.2f(%5.2f)|%3s|%5.2f|" + \
                    "%5d|%5s|%5s|%4s|%5.2f(%3d/%5d)|%4s(%3s)|%4s(%3s|%3s|%3s)|%3s|%3s|%4.2f(%2d)|\n") \
                        % (value['comm'], '-'*5, '-'*5, '-', '-', \
                        self.totalTime - value['usage'], str(round(float(usagePercent), 1)), \
                        round(float(value['offTime']), 7), 0, 0, value['irq'], \
                        value['offCnt'], '-', '-', '-', \
                        value['ioWait'], value['readBlock'], value['readBlockCnt'], \
                        value['writeBlockCnt'], value['writeBlock'], \
                        (value['nrPages'] >> 8) + (value['remainKmem'] >> 20), \
                        value['userPages'] >> 8, value['cachePages'] >> 8, \
                        value['kernelPages'] >> 8 + (value['remainKmem'] >> 20), \
                        (value['reclaimedPages'] >> 8), value['wasteKmem'] >> 20, \
                        value['dReclaimWait'], value['dReclaimCnt']))
                count += 1
            else:
                # convert priority #
                prio = int(value['pri']) - 120
                if prio >= -20:
                    value['pri'] = str(prio)
                else:
                    value['pri'] = 'R%2s' % abs(prio + 21)

        SystemManager.pipePrint("%s# %s: %d\n" % ('', 'CPU', count))
        SystemManager.pipePrint(SystemManager.bufferString)
        SystemManager.pipePrint(oneLine)

        # set sort value #
        if SystemManager.sort == 'm':
            sortedThreadData = sorted(self.threadData.items(), \
                key=lambda e: e[1]['nrPages'], reverse=True)
        elif SystemManager.sort == 'b':
            sortedThreadData = sorted(self.threadData.items(), \
                key=lambda e: e[1]['readBlock'], reverse=True)
        else:
            # set cpu usage as default #
            sortedThreadData = sorted(self.threadData.items(), \
                key=lambda e: e[1]['usage'], reverse=True)

        # print thread information after sorting by time of cpu usage #
        count = 0
        SystemManager.clearPrint()
        for key, value in sortedThreadData:
            if key[0:2] == '0[':
                continue

            try:
                usagePercent = \
                    round(float(value['usage']) / float(self.totalTime), 7) * 100
            except:
                usagePercent = 0

            # set break condition #
            if SystemManager.sort == 'm':
                breakCond = value['nrPages']
            elif SystemManager.sort == 'b':
                breakCond = value['readBlock']
            else:
                breakCond = usagePercent
                value['cpuRank'] = count + 1
                count += 1

            if breakCond < 1 and SystemManager.showAll is False and SystemManager.showGroup == []:
                break

            SystemManager.addPrint(\
                ("%16s(%5s/%5s)|%s%s|%5.2f(%5s)|%5.2f(%5.2f)|%3s|%5.2f|" + \
                "%5d|%5s|%5s|%4s|%5.2f(%3d/%5d)|%4s(%3s)|%4d(%3d|%3d|%3d)|%3d|%3d|%4.2f(%2d)|\n") % \
                (value['comm'], key, value['tgid'], value['new'], value['die'], value['usage'], \
                str(round(float(usagePercent), 1)), value['cpuWait'], value['maxPreempted'], \
                value['pri'], value['irq'], value['yield'], value['preempted'], value['preemption'], \
                value['migrate'], value['ioWait'], value['readBlock'], value['readBlockCnt'], \
                value['writeBlockCnt'], value['writeBlock'], \
                (value['nrPages'] >> 8) + (value['remainKmem'] >> 20), \
                value['userPages'] >> 8, value['cachePages'] >> 8, \
                value['kernelPages'] >> 8 + (value['remainKmem'] >> 20), \
                value['reclaimedPages'] >> 8, value['wasteKmem'] >> 20, \
                value['dReclaimWait'], value['dReclaimCnt']))

        SystemManager.pipePrint("%s# %s: %d\n" % ('', 'Hot', count))
        SystemManager.pipePrint(SystemManager.bufferString)
        SystemManager.pipePrint(oneLine)

        # print thread preempted information after sorting by time of cpu usage #
        for val in SystemManager.preemptGroup:
            index = SystemManager.preemptGroup.index(val)
            count = 0

            tid = SystemManager.preemptGroup[index]
            try:
                self.threadData[tid]
            except:
                SystemManager.printError("Fail to find \"%s\" thread" % tid)
                continue

            SystemManager.clearPrint()
            for key, value in sorted(\
                self.preemptData[index][1].items(), key=lambda e: e[1]['usage'], reverse=True):
                count += 1
                if float(self.preemptData[index][4]) == 0:
                    break
                SystemManager.addPrint("%16s(%5s/%5s)|%s%s|%5.2f(%5s)\n" \
                    % (self.threadData[key]['comm'], key, '0', self.threadData[key]['new'], \
                    self.threadData[key]['die'], value['usage'], \
                    str(round(float(value['usage']) / float(self.preemptData[index][4]) * 100, 1))))
            SystemManager.pipePrint("%s# %s: Tid(%s) / Comm(%s) / Total(%6.3f) / Threads(%d)\n" % \
                ('', 'PRT', tid, self.threadData[tid]['comm'], self.preemptData[index][4], count))
            SystemManager.pipePrint(SystemManager.bufferString)
            SystemManager.pipePrint(oneLine)

        # print new thread information after sorting by new thread flags #
        count = 0
        SystemManager.clearPrint()
        for key, value in sorted(self.threadData.items(), key=lambda e: e[1]['new'], reverse=True):
            if value['new'] == ' ' or SystemManager.selectMenu != None:
                break
            count += 1
            if SystemManager.showAll:
                SystemManager.addPrint(\
                    ("%16s(%5s/%5s)|%s%s|%5.2f(%5s)|%5.2f(%5.2f)|%3s|%5.2f|" + \
                    "%5d|%5s|%5s|%4s|%5.2f(%3d/%5d)|%4s(%3s)|%4d(%3d|%3d|%3d)|%3d|%3d|%4.2f(%2d)|\n") % \
                    (value['comm'], key, value['ptid'], value['new'], value['die'], \
                    value['usage'], str(round(float(usagePercent), 1)), \
                    value['cpuWait'], value['maxPreempted'], value['pri'], value['irq'], \
                    value['yield'], value['preempted'], value['preemption'], value['migrate'], \
                    value['ioWait'], value['readBlock'], value['readBlockCnt'], value['writeBlockCnt'], \
                    value['writeBlock'], (value['nrPages'] >> 8) + (value['remainKmem'] >> 20), \
                    value['userPages'] >> 8, value['cachePages'] >> 8, \
                    value['kernelPages'] >> 8 + (value['remainKmem'] >> 20), \
                    value['reclaimedPages'] >> 8, value['wasteKmem'] >> 20, \
                    value['dReclaimWait'], value['dReclaimCnt']))
        if count > 0:
            SystemManager.pipePrint("%s# %s: %d\n" % ('', 'New', count))
            SystemManager.pipePrint(SystemManager.bufferString)
            SystemManager.pipePrint(oneLine)

        # print terminated thread information after sorting by die flags #
        count = 0
        SystemManager.clearPrint()
        for key, value in sorted(self.threadData.items(), key=lambda e: e[1]['die'], reverse=True):
            if value['die'] == ' ' or SystemManager.selectMenu != None:
                break
            count += 1
            usagePercent = round(float(value['usage']) / float(self.totalTime), 7) * 100
            if SystemManager.showAll:
                SystemManager.addPrint(\
                    ("%16s(%5s/%5s)|%s%s|%5.2f(%5s)|%5.2f(%5.2f)|%3s|%5.2f|" + \
                    "%5d|%5s|%5s|%4s|%5.2f(%3d/%5d)|%4s(%3s)|%4d(%3d|%3d|%3d)|%3d|%3d|%4.2f(%2d)|\n") % \
                    (value['comm'], key, value['ptid'], value['new'], value['die'], \
                    value['usage'], str(round(float(usagePercent), 1)), \
                    value['cpuWait'], value['maxPreempted'], value['pri'], value['irq'], \
                    value['yield'], value['preempted'], value['preemption'], value['migrate'], \
                    value['ioWait'], value['readBlock'], value['readBlockCnt'], value['writeBlockCnt'], \
                    value['writeBlock'], (value['nrPages'] >> 8) + (value['remainKmem'] >> 20), \
                    value['userPages'] >> 8, value['cachePages'] >> 8, \
                    value['kernelPages'] >> 8 + (value['remainKmem'] >> 20), \
                    value['reclaimedPages'] >> 8, value['wasteKmem'] >> 20, \
                    value['dReclaimWait'], value['dReclaimCnt']))
        if count > 0:
            SystemManager.pipePrint("%s# %s: %d\n" % ('', 'Die', count))
            SystemManager.pipePrint(SystemManager.bufferString)
            SystemManager.pipePrint(oneLine)

        self.printComInfo()

        self.printEventInfo()

        # prepare to draw graph #
        if SystemManager.graphEnable:
            if SystemManager.intervalEnable > 0:
                os.environ['DISPLAY'] = 'localhost:0'
                rc('legend', fontsize=5)
                rcParams.update({'font.size': 8})
            else:
                SystemManager.printError("Use also -i option if you want to draw graph")
                SystemManager.graphEnable = False



    def getConf(self):
        if SystemManager.sourceFile is not None:
            confBuf = None
            confDict = None

            try:
                with open(SystemManager.sourceFile, 'r') as fd:
                    confBuf = fd.read()
            except:
                SystemManager.printError("Fail to open %s to set configuration" % \
                    SystemManager.sourceFile)
                sys.exit(0)

            if confBuf is None:
                SystemManager.printError("Fail to read %s to set configuration" % \
                    SystemManager.sourceFile)
                sys.exit(0)

            if SystemManager.jsonObject is None:
                try:
                    import json
                    SystemManager.jsonObject = json
                except ImportError:
                    err = sys.exc_info()[1]
                    SystemManager.printError("Fail to import package: " + err.args[0])

            try:
                confBuf = confBuf.replace("'", '"')
                confDict = SystemManager.jsonObject.loads(confBuf)

                if 'bound' in confDict:
                    ThreadAnalyzer.reportBoundary = confDict['bound']
                else:
                    raise
            except:
                SystemManager.printError("Fail to load configuration from %s" % \
                    SystemManager.sourceFile)
                sys.exit(0)



    def printModuleInfo(self):
        if len(self.moduleData) <= 0:
            return

        eventCnt = 0
        for val in self.moduleData:
            event = val[0]
            if event == 'load' or event == 'free':
                eventCnt += 1
        if eventCnt == 0:
            return

        moduleTable = {}
        init_moduleData = {'startTime': float(0), 'loadCnt': int(0), 'elapsed': float(0)}

        SystemManager.clearPrint()
        SystemManager.pipePrint('\n' + '[Thread Module Info]')
        SystemManager.pipePrint(twoLine)
        SystemManager.pipePrint("{0:_^6}|{1:_^6}|{2:_^16}|{3:_^16}({4:^5})|{5:_^6}|".\
            format("Type", "Time", "Module", "Thread Name", "Tid", "Elapsed"))
        SystemManager.pipePrint(twoLine)

        for val in self.moduleData:
            event = val[0]
            tid = val[1]
            time = val[2]
            module = val[3]

            if event is 'load':
                try:
                    moduleTable[module]
                except:
                    moduleTable[module] = dict(init_moduleData)

                moduleTable[module]['startTime'] = time
                moduleTable[module]['loadCnt'] += 1

            elif event is 'free':
                SystemManager.pipePrint("{0:^6}|{1:6.3f}|{2:^16}|{3:>16}({4:>5})|{5:7}".\
                    format('FREE', float(time) - float(self.startTime), module, \
                    self.threadData[tid]['comm'], tid, ''))
            elif event is 'put':
                try:
                    moduleTable[module]
                except:
                    continue

                moduleTable[module]['elapsed'] += \
                    (float(time) - float(moduleTable[module]['startTime']))
                moduleTable[module]['startTime'] = 0

                SystemManager.pipePrint("{0:^6}|{1:6.3f}|{2:^16}|{3:>16}({4:>5})|{5:7.3f}|".\
                    format('LOAD', float(time) - float(self.startTime), module, \
                    self.threadData[tid]['comm'], tid, moduleTable[module]['elapsed']))

        SystemManager.pipePrint(SystemManager.bufferString)
        SystemManager.pipePrint(oneLine)



    def printDepInfo(self):
        if SystemManager.depEnable is False:
            return

        SystemManager.clearPrint()
        SystemManager.pipePrint('\n' + '[Thread Dependency Info]')
        SystemManager.pipePrint(twoLine)
        SystemManager.pipePrint("\t%5s/%4s \t%16s(%4s) -> %16s(%4s) \t%5s" % \
            ("Total", "Inter", "From", "Tid", "To", "Tid", "Event"))
        SystemManager.pipePrint(twoLine)
        SystemManager.pipePrint("%s# %s: %d\n" % ('', 'Dep', len(self.depData)))

        for icount in xrange(0, len(self.depData)):
            SystemManager.addPrint(self.depData[icount] + '\n')

        SystemManager.pipePrint(SystemManager.bufferString)
        SystemManager.pipePrint(oneLine)



    def printSyscallInfo(self):
        SystemManager.clearPrint()

        if self.syscallData != []:
            outputCnt = 0
            SystemManager.pipePrint('\n' + '[Thread Syscall Info]')
            SystemManager.pipePrint(twoLine)
            SystemManager.pipePrint("%16s(%4s)\t%7s\t\t%5s\t\t%6s\t\t%6s\t\t%8s\t\t%8s\t\t%8s" % \
                ("Name", "Tid", "Syscall", "SysId", "Usage", "Count", "Min", "Max", "Avg"))
            SystemManager.pipePrint(twoLine)

            for key, value in sorted(self.threadData.items(), key=lambda e: e[1]['comm']):
                threadInfo = ''
                syscallInfo = ''

                if key[0:2] == '0[':
                    continue

                try:
                    if len(value['syscallInfo']) > 0:
                        threadInfo = "%16s(%4s)" % (value['comm'], key)
                    else:
                        continue
                except:
                    continue

                for sysId, val in sorted(\
                    value['syscallInfo'].items(), key=lambda e: e[1]['usage'], reverse=True):
                    try:
                        if val['count'] > 0:
                            val['average'] = val['usage'] / val['count']

                            syscallInfo += "%31s\t\t%5s\t\t%6.3f\t\t%6d\t\t%6.6f\t\t%6.6f\t\t%6.6f\n" % \
                                (ConfigManager.sysList[int(sysId)], sysId, val['usage'], \
                                 val['count'], val['min'], val['max'], val['average'])
                    except:
                        continue

                if syscallInfo != '':
                    outputCnt += 1
                    SystemManager.pipePrint(threadInfo)
                    SystemManager.pipePrint(syscallInfo)

            if outputCnt == 0:
                SystemManager.pipePrint('\tNone')

            SystemManager.pipePrint(oneLine)

            SystemManager.clearPrint()
            if SystemManager.showAll:
                SystemManager.pipePrint('\n' + '[Thread Syscall History]')
                SystemManager.pipePrint(twoLine)
                SystemManager.pipePrint(\
                    "%16s(%4s)\t%8s\t%8s\t%5s\t%16s\t%6s\t%4s\t%8s\t%s" % \
                    ("Name", "Tid", "Time", "Diff", "Type", "Syscall", \
                    "SysId", "Core", "Return", "Parameter"))
                SystemManager.pipePrint(twoLine)

                cnt = 0
                for icount in xrange(0, len(self.syscallData)):
                    try:
                        if self.syscallData[icount][0] == 'enter':
                            if self.syscallData[icount + 1][0] == 'exit' and \
                                self.syscallData[icount][4] == self.syscallData[icount + 1][4]:
                                eventType = 'both'
                                eventTime = float(self.syscallData[icount][1]) - float(self.startTime)
                                diffTime = float(self.syscallData[icount + 1][1]) - \
                                    float(self.syscallData[icount][1])
                                ret = self.syscallData[icount + 1][5]
                                param = self.syscallData[icount][5]
                            else:
                                eventType = self.syscallData[icount][0]
                                eventTime = float(self.syscallData[icount][1]) - float(self.startTime)
                                diffTime = float(0)
                                ret = '-'
                                param = self.syscallData[icount][5]
                        else:
                            if self.syscallData[icount - 1][0] == 'enter' and \
                                    self.syscallData[icount][4] == self.syscallData[icount - 1][4]:
                                continue
                            else:
                                eventType = self.syscallData[icount][0]
                                eventTime = float(self.syscallData[icount][1]) - float(self.startTime)
                                diffTime = float(0)
                                ret = self.syscallData[icount][5]
                                param = '-'

                        SystemManager.pipePrint("%16s(%4s)\t%6.6f\t%6.6f\t%5s\t%16s\t%6s\t%4s\t%8s\t%s" % \
                            (self.threadData[self.syscallData[icount][2]]['comm'], \
                            self.syscallData[icount][2], eventTime, diffTime, eventType, \
                            ConfigManager.sysList[int(self.syscallData[icount][4])], \
                            self.syscallData[icount][4], self.syscallData[icount][3], ret, param))
                        cnt += 1
                    except:
                        continue
                if cnt == 0:
                    SystemManager.pipePrint("\tNone")
                SystemManager.pipePrint(oneLine)



    def printConsoleInfo(self):
        if len(self.consoleData) > 0 and SystemManager.showAll:
            SystemManager.pipePrint('\n' + '[Thread Message Info]')
            SystemManager.pipePrint(twoLine)
            SystemManager.pipePrint(\
                "%16s %5s %4s %10s %30s" % ('Name', 'Tid', 'Core', 'Time', 'Console message'))
            SystemManager.pipePrint(twoLine)

            cnt = 0
            for msg in self.consoleData:
                try:
                    SystemManager.pipePrint("%16s %5s %4s %10.3f %s" % \
                        (self.threadData[msg[0]]['comm'], msg[0], msg[1], \
                        round(float(msg[2]) - float(self.startTime), 7), msg[3]))
                    cnt += 1
                except:
                    continue

            if cnt == 0:
                SystemManager.pipePrint("\tNone")
            SystemManager.pipePrint(twoLine)



    def printBlockInfo(self):
        if SystemManager.blockEnable is False:
            return

        SystemManager.pipePrint('\n' + '[Thread Block Info]')
        SystemManager.pipePrint(twoLine)
        SystemManager.pipePrint("{0:^8} {1:^8} {2:^12} {3:^16} {4:>32}".\
            format('ID', 'Size(KB)', 'Filesystem', 'Device', 'Mount'))
        SystemManager.pipePrint(oneLine)

        if len(self.blockTable[0]) > 0:
            SystemManager.pipePrint('# READ\n')
            for num, size in self.blockTable[0].items():
                try:
                    dev = SystemManager.savedMountTree[num]['dev']
                    filesystem = SystemManager.savedMountTree[num]['filesystem']
                    mount = SystemManager.savedMountTree[num]['mount']
                except:
                    dev = '\t\t\t?'
                    filesystem = '?'
                    mount = '\t\t\t?'

                SystemManager.pipePrint("{0:^8} {1:>8} {2:^12} {3:<16} {4:<32}".\
                    format(num, size >> 10, filesystem, dev, mount))
            SystemManager.pipePrint(oneLine)

        if len(self.blockTable[1]) > 0:
            SystemManager.pipePrint('# WRITE\n')
            for num, size in self.blockTable[1].items():
                try:
                    dev = SystemManager.savedMountTree[num]['dev']
                    filesystem = SystemManager.savedMountTree[num]['filesystem']
                    mount = SystemManager.savedMountTree[num]['mount']
                except:
                    dev = '\t\t\t?'
                    filesystem = '?'
                    mount = '\t\t\t?'

                SystemManager.pipePrint("{0:^8} {1:>8} {2:^12} {3:<16} {4:<32}".\
                    format(num, size >> 10, filesystem, dev, mount))
            SystemManager.pipePrint(oneLine)



    def printEventIntervalInfo(self):
        # timeline #
        timeLine = ''
        titleLine = "%16s(%5s/%5s):" % ('Name', 'Tid', 'Pid')
        maxLineLen = SystemManager.lineLength
        timeLineLen = titleLineLen = len(titleLine)

        # custom event usage on timeline #
        SystemManager.clearPrint()
        if len(SystemManager.customEventList) > 0:
            for idx, val in sorted(\
                self.customEventInfo.items(), key=lambda e: e[1]['count'], reverse=True):

                for key, value in sorted(self.customInfo.items(), \
                    key=lambda e: 0 if not idx in e[1] else e[1][idx], reverse=True):
                    timeLine = ''
                    timeLineLen = titleLineLen
                    lval = int(float(self.totalTime) / SystemManager.intervalEnable) + 1
                    for icount in xrange(0, lval):
                        newFlag = ' '
                        dieFlag = ' '

                        if timeLineLen + 4 > maxLineLen:
                            timeLine += ('\n' + (' ' * (titleLineLen + 1)))
                            timeLineLen = titleLineLen + 4
                        else:
                            timeLineLen += 4

                        try:
                            self.intervalData[icount][key]['customEvent']
                        except:
                            timeLine += '%3d ' % 0
                            continue

                        nowVal = self.intervalData[icount][key]

                        try:
                            prevVal = self.intervalData[icount - 1][key]
                        except:
                            prevVal = nowVal

                        if icount > 0:
                            try:
                                if nowVal['new'] != prevVal['new']:
                                    newFlag = self.intervalData[icount][key]['new']
                            except:
                                newFlag = nowVal['new']
                            try:
                                if nowVal['die'] != prevVal['die']:
                                    dieFlag = nowVal['die']
                            except:
                                dieFlag = nowVal['die']
                        else:
                            newFlag = nowVal['new']
                            dieFlag = nowVal['die']

                        cnt = str(self.intervalData[icount][key]['customEvent'][idx]['count'])

                        timeLine += '%4s' % (newFlag + cnt + dieFlag)

                    if (idx not in value or value[idx]['count'] == 0) and \
                        SystemManager.showAll == False:
                        break

                    SystemManager.addPrint("%16s(%5s/%5s): " % \
                        (self.threadData[key]['comm'], key, \
                        self.threadData[key]['tgid']) + timeLine + '\n')

                SystemManager.pipePrint("%s# %s\n" % ('', '%s(Cnt)' % idx))
                SystemManager.pipePrint(SystemManager.bufferString)
                SystemManager.pipePrint(oneLine)
                SystemManager.clearPrint()

        # user event usage on timeline #
        SystemManager.clearPrint()
        if len(SystemManager.userEventList) > 0:
            for idx, val in sorted(\
                self.userEventInfo.items(), key=lambda e: e[1]['count'], reverse=True):

                for key, value in sorted(self.userInfo.items(), \
                    key=lambda e: 0 if not idx in e[1] else e[1][idx], reverse=True):
                    timeLine = ''
                    timeLineLen = titleLineLen
                    lval = int(float(self.totalTime) / SystemManager.intervalEnable) + 1
                    for icount in xrange(0, lval):
                        newFlag = ' '
                        dieFlag = ' '

                        if timeLineLen + 4 > maxLineLen:
                            timeLine += ('\n' + (' ' * (titleLineLen + 1)))
                            timeLineLen = titleLineLen + 4
                        else:
                            timeLineLen += 4

                        try:
                            self.intervalData[icount][key]['userEvent']
                        except:
                            timeLine += '%3d ' % 0
                            continue

                        nowVal = self.intervalData[icount][key]

                        try:
                            prevVal = self.intervalData[icount - 1][key]
                        except:
                            prevVal = nowVal

                        if icount > 0:
                            try:
                                if nowVal['new'] != prevVal['new']:
                                    newFlag = self.intervalData[icount][key]['new']
                            except:
                                newFlag = nowVal['new']
                            try:
                                if nowVal['die'] != prevVal['die']:
                                    dieFlag = nowVal['die']
                            except:
                                dieFlag = nowVal['die']
                        else:
                            newFlag = nowVal['new']
                            dieFlag = nowVal['die']

                        res = str(self.intervalData[icount][key]['userEvent'][idx]['count'])

                        '''
                        res = str(self.intervalData[icount][key]['userEvent'][idx]['usage']) / \
                            SystemManager.intervalEnable * 100
                        '''

                        timeLine += '%4s' % (newFlag + res + dieFlag)

                    if (idx not in value or value[idx]['count'] == 0) and \
                        SystemManager.showAll == False:
                        break

                    SystemManager.addPrint("%16s(%5s/%5s): " % \
                        (self.threadData[key]['comm'], key, \
                        self.threadData[key]['tgid']) + timeLine + '\n')

                SystemManager.pipePrint("%s# %s\n" % ('', '%s(Cnt)' % idx))
                SystemManager.pipePrint(SystemManager.bufferString)
                SystemManager.pipePrint(oneLine)
                SystemManager.clearPrint()

        # kernel event usage on timeline #
        SystemManager.clearPrint()
        if len(SystemManager.kernelEventList) > 0:
            for idx, val in sorted(\
                self.kernelEventInfo.items(), key=lambda e: e[1]['count'], reverse=True):

                for key, value in sorted(self.kernelInfo.items(), \
                    key=lambda e: 0 if not idx in e[1] else e[1][idx], reverse=True):
                    timeLine = ''
                    timeLineLen = titleLineLen
                    lval = int(float(self.totalTime) / SystemManager.intervalEnable) + 1
                    for icount in xrange(0, lval):
                        newFlag = ' '
                        dieFlag = ' '

                        if timeLineLen + 4 > maxLineLen:
                            timeLine += ('\n' + (' ' * (titleLineLen + 1)))
                            timeLineLen = titleLineLen + 4
                        else:
                            timeLineLen += 4

                        try:
                            self.intervalData[icount][key]['kernelEvent']
                        except:
                            timeLine += '%3d ' % 0
                            continue

                        nowVal = self.intervalData[icount][key]

                        try:
                            prevVal = self.intervalData[icount - 1][key]
                        except:
                            prevVal = nowVal

                        if icount > 0:
                            try:
                                if nowVal['new'] != prevVal['new']:
                                    newFlag = self.intervalData[icount][key]['new']
                            except:
                                newFlag = nowVal['new']
                            try:
                                if nowVal['die'] != prevVal['die']:
                                    dieFlag = nowVal['die']
                            except:
                                dieFlag = nowVal['die']
                        else:
                            newFlag = nowVal['new']
                            dieFlag = nowVal['die']

                        res = str(self.intervalData[icount][key]['kernelEvent'][idx]['count'])

                        '''
                        res = str(self.intervalData[icount][key]['kernelEvent'][idx]['usage']) / \
                            SystemManager.intervalEnable * 100
                        '''

                        timeLine += '%4s' % (newFlag + res + dieFlag)

                    if (idx not in value or value[idx]['count'] == 0) and \
                        SystemManager.showAll == False:
                        break

                    SystemManager.addPrint("%16s(%5s/%5s): " % \
                        (self.threadData[key]['comm'], key, \
                        self.threadData[key]['tgid']) + timeLine + '\n')

                SystemManager.pipePrint("%s# %s\n" % ('', '%s(Cnt)' % idx))
                SystemManager.pipePrint(SystemManager.bufferString)
                SystemManager.pipePrint(oneLine)
                SystemManager.clearPrint()


    def printIntervalInfo(self):
        if SystemManager.intervalEnable <= 0 or \
            not (SystemManager.cpuEnable or SystemManager.memEnable or SystemManager.blockEnable):
            return

        SystemManager.pipePrint('\n' + '[Thread Interval Info] [ Unit: %s Sec ]' % \
            SystemManager.intervalEnable)
        SystemManager.pipePrint(twoLine)

        # graph list #
        cpuLabelList = []
        cpuUsageList = []
        cpuThrLabelList = []
        cpuThrUsageList = []
        ioLabelList = []
        ioUsageList = []

        # timeline #
        timeLine = ''
        titleLine = "%16s(%5s/%5s):" % ('Name', 'Tid', 'Pid')
        maxLineLen = SystemManager.lineLength
        timeLineLen = titleLineLen = len(titleLine)
        lval = int(float(self.totalTime) / SystemManager.intervalEnable) + 2
        for icount in xrange(1, lval):
            checkEvent = ' '
            cnt = icount - 1

            # check suspend event #
            for val in self.suspendData:
                if float(self.startTime) + cnt * SystemManager.intervalEnable < float(val[0]) < \
                    float(self.startTime) + ((cnt + 1) * SystemManager.intervalEnable):
                    if val[1] == 'S':
                        checkEvent = '!'
                    elif val[1] == 'F':
                        checkEvent = '^'
                    else:
                        checkEvent = '>'

            # check mark event #
            for val in self.markData:
                if float(self.startTime) + cnt * SystemManager.intervalEnable < float(val) < \
                    float(self.startTime) + ((cnt + 1) * SystemManager.intervalEnable):
                    checkEvent = 'v'

            if timeLineLen + 4 > maxLineLen:
                timeLine += ('\n' + (' ' * (titleLineLen + 1)))
                timeLineLen = titleLineLen + 4
            else:
                timeLineLen += 4

            # print timeline #
            if icount * SystemManager.intervalEnable < float(self.totalTime):
                timeLine += '%s%2d ' % (checkEvent, icount * SystemManager.intervalEnable)
            else:
                timeLine += '%s%.2f ' % (checkEvent, self.totalTime)

        SystemManager.pipePrint("%s %s" % (titleLine, timeLine))
        SystemManager.pipePrint(twoLine)
        SystemManager.clearPrint()

        # total CPU usage on timeline #
        for key, value in sorted(self.threadData.items(), \
            key=lambda e: ThreadAnalyzer.getCoreId(e[1]['comm']), reverse=False):
            if key[0:2] == '0[':
                timeLine = ''
                timeLineLen = titleLineLen
                lval = int(float(self.totalTime) / SystemManager.intervalEnable) + 1
                for icount in xrange(0, lval):
                    try:
                        self.intervalData[icount][key]
                        timeLine += '%3d ' % (100 - self.intervalData[icount][key]['cpuPer'])
                    except:
                        timeLine += '%3s ' % '0'

                    if timeLineLen + 4 >= maxLineLen:
                        timeLine += ('\n' + (' ' * (titleLineLen + 1)))
                        timeLineLen = titleLineLen + 4
                    else:
                        timeLineLen += 4

                SystemManager.addPrint("%16s(%5s/%5s): " % \
                    (value['comm'], '0', value['tgid']) + timeLine + '\n')

                # make cpu usage list for graph #
                if SystemManager.graphEnable and SystemManager.cpuEnable:
                    timeLine = timeLine.replace('N', '')
                    timeLine = timeLine.replace('D', '')
                    timeLine = timeLine.replace('F', '')
                    timeLineData = [int(n) for n in timeLine.split()]
                    cpuUsageList.append(timeLineData)
                    cpuLabelList.append('[' + value['comm'] + ']')

        # total memory usage on timeline #
        timeLine = ''
        timeLineLen = titleLineLen
        lval = int(float(self.totalTime) / SystemManager.intervalEnable) + 1
        for icount in xrange(0, lval):
            if timeLineLen + 4 > maxLineLen:
                timeLine += ('\n' + (' ' * (titleLineLen + 1)))
                timeLineLen = titleLineLen + 4
            else:
                timeLineLen += 4

            try:
                timeLine += '%3d ' % ((self.intervalData[icount]['toTal']['totalMem'] >> 8) + \
                    (self.intervalData[icount]['toTal']['totalKmem'] >> 20))
            except:
                timeLine += '%3d ' % (0)

        if SystemManager.memEnable:
            SystemManager.addPrint("\n%16s(%5s/%5s): " % ('MEM', '0', '-----') + timeLine + '\n')
            if SystemManager.graphEnable:
                timeLineData = [int(n) for n in timeLine.split()]
                ioUsageList.append(timeLineData)
                ioLabelList.append('RAM Usage')

        if SystemManager.blockEnable:
            # total block read usage on timeline #
            timeLine = ''
            timeLineLen = titleLineLen
            lval = int(float(self.totalTime) / SystemManager.intervalEnable) + 1
            for icount in xrange(0, lval):
                if timeLineLen + 4 > maxLineLen:
                    timeLine += ('\n' + (' ' * (titleLineLen + 1)))
                    timeLineLen = titleLineLen + 4
                else:
                    timeLineLen += 4

                try:
                    timeLine += '%3d ' % ((self.intervalData[icount]['toTal']['totalBr'] * \
                        SystemManager.blockSize) >> 20)
                except:
                    timeLine += '%3d ' % (0)

            SystemManager.addPrint("\n%16s(%5s/%5s): " % ('BLK_RD', '0', '-----') + timeLine + '\n')
            if SystemManager.graphEnable:
                timeLineData = [int(n) for n in timeLine.split()]
                ioUsageList.append(timeLineData)
                ioLabelList.append('Block Read')

            # total block write usage on timeline #
            timeLine = ''
            timeLineLen = titleLineLen
            lval = int(float(self.totalTime) / SystemManager.intervalEnable) + 1
            for icount in xrange(0, lval):
                if timeLineLen + 4 > maxLineLen:
                    timeLine += ('\n' + (' ' * (titleLineLen + 1)))
                    timeLineLen = titleLineLen + 4
                else:
                    timeLineLen += 4

                try:
                    timeLine += '%3d ' % ((self.intervalData[icount]['toTal']['totalBw'] * \
                        SystemManager.pageSize) >> 20)
                except:
                    timeLine += '%3d ' % (0)

            SystemManager.addPrint("%16s(%5s/%5s): " % ('BLK_WR', '0', '-----') + timeLine + '\n')
            if SystemManager.graphEnable:
                timeLineData = [int(n) for n in timeLine.split()]
                ioUsageList.append(timeLineData)
                ioLabelList.append('Block Write')

        # total custom event usage on timeline #
        newLine = True
        for evt, value in sorted(\
            self.customEventInfo.items(), key=lambda e: e[1]['count'], reverse=True):

            timeLine = ''
            timeLineLen = titleLineLen
            lval = int(float(self.totalTime) / SystemManager.intervalEnable) + 1
            for icount in xrange(0, lval):
                if timeLineLen + 4 > maxLineLen:
                    timeLine += ('\n' + (' ' * (titleLineLen + 1)))
                    timeLineLen = titleLineLen + 4
                else:
                    timeLineLen += 4

                try:
                    timeLine += '%3d ' % \
                        self.intervalData[icount]['toTal']['customEvent'][evt]['count']
                except:
                    timeLine += '%3d ' % (0)

            if newLine:
                SystemManager.addPrint("\n")
                newLine = False

            SystemManager.addPrint("%16s(%5s/%5s): " % (evt[:16], '0', '-----') + timeLine + '\n')

        # total user event usage on timeline #
        newLine = True
        for evt, value in sorted(\
            self.userEventInfo.items(), key=lambda e: e[1]['count'], reverse=True):

            timeLine = ''
            timeLineLen = titleLineLen
            lval = int(float(self.totalTime) / SystemManager.intervalEnable) + 1
            for icount in xrange(0, lval):
                if timeLineLen + 4 > maxLineLen:
                    timeLine += ('\n' + (' ' * (titleLineLen + 1)))
                    timeLineLen = titleLineLen + 4
                else:
                    timeLineLen += 4

                try:
                    timeLine += '%3d ' % \
                        self.intervalData[icount]['toTal']['userEvent'][evt]['count']

                    '''
                    timeLine += '%3d ' % \
                        (self.intervalData[icount]['toTal']['userEvent'][evt]['usage'] / \
                        SystemManager.intervalEnable * 100)
                    '''
                except:
                    timeLine += '%3d ' % (0)

            if newLine:
                SystemManager.addPrint("\n")
                newLine = False

            SystemManager.addPrint("%16s(%5s/%5s): " % (evt[:16], '0', '-----') + timeLine + '\n')

        # total kernel event usage on timeline #
        newLine = True
        for evt, value in sorted(\
            self.kernelEventInfo.items(), key=lambda e: e[1]['count'], reverse=True):

            timeLine = ''
            timeLineLen = titleLineLen
            lval = int(float(self.totalTime) / SystemManager.intervalEnable) + 1
            for icount in xrange(0, lval):
                if timeLineLen + 4 > maxLineLen:
                    timeLine += ('\n' + (' ' * (titleLineLen + 1)))
                    timeLineLen = titleLineLen + 4
                else:
                    timeLineLen += 4

                try:
                    timeLine += '%3d ' % \
                        self.intervalData[icount]['toTal']['kernelEvent'][evt]['count']

                    '''
                    timeLine += '%3d ' % \
                        (self.intervalData[icount]['toTal']['kernelEvent'][evt]['usage'] / \
                        SystemManager.intervalEnable * 100)
                    '''
                except:
                    timeLine += '%3d ' % (0)

            if newLine:
                SystemManager.addPrint("\n")
                newLine = False

            SystemManager.addPrint("%16s(%5s/%5s): " % (evt[:16], '0', '-----') + timeLine + '\n')

        # print buffered info #
        SystemManager.pipePrint("%s# %s\n" % ('', 'Total(%/MB/Cnt)'))
        SystemManager.pipePrint(SystemManager.bufferString)
        SystemManager.pipePrint(oneLine)
        SystemManager.clearPrint()

        # draw io graph #
        if SystemManager.graphEnable and len(ioUsageList) > 0:
            timelen = len(ioUsageList[0])
            ax = subplot2grid((6,1), (5,0), rowspan=1, colspan=1)
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))

            for idx, item in enumerate(ioUsageList):
                minIdx = item.index(min(item))
                maxIdx = item.index(max(item))
                nrColor = int(idx) % 3
                if nrColor == 0:
                    color = 'blue'
                elif nrColor == 1:
                    color = 'red'
                else:
                    color = 'green'

                plot(range(SystemManager.intervalEnable,\
                    (timelen+1)*SystemManager.intervalEnable,\
                    SystemManager.intervalEnable), item, '-', c=color)

                ytick = yticks()[0]
                if len(ytick) > 1:
                    margin = (ytick[1] - ytick[0]) / 2
                else:
                    margin = 0

                if minIdx > 0:
                    minUsage = str(item[minIdx])
                    text(minIdx + 1, item[minIdx] - margin, minUsage, fontsize=5,\
                        color=color, fontweight='bold')
                if maxIdx > 0:
                    maxUsage = str(item[maxIdx])
                    text(maxIdx + 1, item[maxIdx] - margin, maxUsage, fontsize=5,\
                        color=color, fontweight='bold')

            ylabel('Memory(MB)', fontsize=8)
            legend(ioLabelList, bbox_to_anchor=(1.1, 1), fontsize=3.5, loc='upper right')
            grid(which='both', linestyle=':', linewidth='0.2')
            yticks(fontsize = 7)
            xticks(fontsize = 5)
            ticklabel_format(useOffset=False)
            locator_params(axis='x', nbins=30)
            figure(num=1, figsize=(10, 10), dpi=2000, facecolor='b', edgecolor='k').\
                subplots_adjust(left=0.06, top=0.95, bottom=0.05)

        # CPU usage on timeline #
        for key, value in sorted(\
            self.threadData.items(), key=lambda e: e[1]['usage'], reverse=True):

            if key[0:2] != '0[':
                timeLine = ''
                timeLineLen = titleLineLen
                lval = int(float(self.totalTime) / SystemManager.intervalEnable) + 1
                for icount in xrange(0, lval):
                    newFlag = ' '
                    dieFlag = ' '

                    if timeLineLen + 4 > maxLineLen:
                        timeLine += ('\n' + (' ' * (titleLineLen + 1)))
                        timeLineLen = titleLineLen + 4
                    else:
                        timeLineLen += 4

                    try:
                        self.intervalData[icount][key]
                    except:
                        timeLine += '%3d ' % 0
                        continue

                    nowVal = self.intervalData[icount][key]

                    try:
                        prevVal = self.intervalData[icount - 1][key]
                    except:
                        prevVal = nowVal

                    if icount > 0:
                        try:
                            if nowVal['new'] != prevVal['new']:
                                newFlag = nowVal['new']
                        except:
                            newFlag = nowVal['new']
                        try:
                            if nowVal['die'] != prevVal['die']:
                                dieFlag = nowVal['die']
                        except:
                            dieFlag = nowVal['die']
                    else:
                        newFlag = self.intervalData[icount][key]['new']
                        dieFlag = self.intervalData[icount][key]['die']

                    # Do not use 100% becuase of output format #
                    cpuPer = str(int(self.intervalData[icount][key]['cpuPer']))
                    if cpuPer == '100':
                        cpuPer = '99'

                    timeLine += '%4s' % (newFlag + cpuPer + dieFlag)

                SystemManager.addPrint("%16s(%5s/%5s): " % \
                    (value['comm'], key, value['tgid']) + timeLine + '\n')

                if SystemManager.graphEnable and SystemManager.cpuEnable:
                    timeLine = timeLine.replace('N', '')
                    timeLine = timeLine.replace('D', '')
                    timeLine = timeLine.replace('F', '')
                    cpuThrUsageList.append([int(n) for n in timeLine.split()])
                    tinfo = '%s(%s)' % (value['comm'], key)
                    cpuThrLabelList.append(tinfo)

                if SystemManager.showAll is False and \
                    value['usage'] / float(self.totalTime) * 100 < 1:
                    break

        # draw cpu graph #
        if SystemManager.graphEnable and len(cpuUsageList) > 0:
            timelen = len(cpuUsageList[0])
            ax = subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            title('guider interval report')

            # cpu total usage #
            for item in cpuUsageList:
                plot(range(SystemManager.intervalEnable,\
                    (timelen+1)*SystemManager.intervalEnable,\
                    SystemManager.intervalEnable), item, '.-',\
                    linewidth=3, solid_capstyle='round')

            # cpu usage of threads #
            for idx, item in enumerate(cpuThrUsageList):
                maxIdx = item.index(max(item))

                color = plot(range(SystemManager.intervalEnable,\
                    (timelen+1)*SystemManager.intervalEnable,\
                    SystemManager.intervalEnable), item, '-')[0].get_color()

                ytick = yticks()[0]
                if len(ytick) > 1:
                    margin = (ytick[1] - ytick[0]) / (len(ytick) * 2)
                else:
                    margin = 0

                maxCpuPer = str(item[maxIdx])
                label = '[' + maxCpuPer + '%]' + cpuThrLabelList[idx]
                text(maxIdx + 1, item[maxIdx] + margin, label,\
                    fontsize=3, color=color, fontweight='bold')

            # draw cpu graph #
            ylabel('CPU(%)', fontsize=8)
            legend(cpuLabelList + cpuThrLabelList, bbox_to_anchor=(1.12, 1),\
                fontsize=3.5, loc='upper right')
            grid(which='both', linestyle=':', linewidth='0.2')
            yticks(fontsize = 7)
            xticks(fontsize = 5)
            ticklabel_format(useOffset=False)
            locator_params(axis='x', nbins=30)
            figure(num=1, figsize=(10, 10), dpi=2000, facecolor='b', edgecolor='k').\
                subplots_adjust(left=0.06, top=0.95, bottom=0.05)

        SystemManager.pipePrint("%s# %s\n" % ('', 'CPU(%)'))
        SystemManager.pipePrint(SystemManager.bufferString)
        SystemManager.pipePrint(oneLine)

        # preempted units on timeline #
        SystemManager.clearPrint()
        for key, value in sorted(\
            self.threadData.items(), key=lambda e: e[1]['cpuWait'], reverse=True):

            if key[0:2] != '0[':
                timeLine = ''
                timeLineLen = titleLineLen
                lval = int(float(self.totalTime) / SystemManager.intervalEnable) + 1
                for icount in xrange(0, lval):
                    newFlag = ' '
                    dieFlag = ' '

                    if timeLineLen + 4 > maxLineLen:
                        timeLine += ('\n' + (' ' * (titleLineLen + 1)))
                        timeLineLen = titleLineLen + 4
                    else:
                        timeLineLen += 4

                    try:
                        self.intervalData[icount][key]
                    except:
                        timeLine += '%3d ' % 0
                        continue

                    nowVal = self.intervalData[icount][key]

                    try:
                        prevVal = self.intervalData[icount - 1][key]
                    except:
                        prevVal = nowVal

                    if icount > 0:
                        try:
                            if nowVal['new'] != prevVal['new']:
                                newFlag = self.intervalData[icount][key]['new']
                        except:
                            newFlag = nowVal['new']
                        try:
                            if nowVal['die'] != prevVal['die']:
                                dieFlag = nowVal['die']
                        except:
                            dieFlag = nowVal['die']
                    else:
                        newFlag = nowVal['new']
                        dieFlag = nowVal['die']

                    # Do not use 100% becuase of output format #
                    prtPer = str(int(nowVal['preempted'] / float(SystemManager.intervalEnable) * 100))
                    if prtPer == '100':
                        prtPer = '99'

                    timeLine += '%4s' % (newFlag + prtPer + dieFlag)

                SystemManager.addPrint("%16s(%5s/%5s): " % \
                    (value['comm'], key, value['tgid']) + timeLine + '\n')

                if value['cpuWait'] / float(self.totalTime) * 100 < 1 and \
                    SystemManager.showAll is False:
                    break

        SystemManager.pipePrint("%s# %s\n" % ('', 'Delay(%)'))
        SystemManager.pipePrint(SystemManager.bufferString)
        SystemManager.pipePrint(oneLine)

        # memory usage on timeline #
        SystemManager.clearPrint()
        if SystemManager.memEnable:
            for key, value in sorted(\
                self.threadData.items(), key=lambda e: e[1]['nrPages'], reverse=True):

                if key[0:2] != '0[':
                    timeLine = ''
                    timeLineLen = titleLineLen
                    lval = int(float(self.totalTime) / SystemManager.intervalEnable) + 1
                    for icount in xrange(0, lval):
                        newFlag = ' '
                        dieFlag = ' '

                        if timeLineLen + 4 > maxLineLen:
                            timeLine += ('\n' + (' ' * (titleLineLen + 1)))
                            timeLineLen = titleLineLen + 4
                        else:
                            timeLineLen += 4

                        try:
                            self.intervalData[icount][key]
                        except:
                            timeLine += '%3d ' % 0
                            continue

                        nowVal = self.intervalData[icount][key]

                        try:
                            prevVal = self.intervalData[icount - 1][key]
                        except:
                            prevVal = nowVal

                        if icount > 0:
                            try:
                                if nowVal['new'] != prevVal['new']:
                                    newFlag = self.intervalData[icount][key]['new']
                            except:
                                newFlag = nowVal['new']
                            try:
                                if nowVal['die'] != prevVal['die']:
                                    dieFlag = nowVal['die']
                            except:
                                dieFlag = nowVal['die']
                        else:
                            newFlag = nowVal['new']
                            dieFlag = nowVal['die']

                        memUsage = self.intervalData[icount][key]['memUsage'] >> 8
                        kmemUsage = self.intervalData[icount][key]['kmemUsage'] >> 20
                        timeLine += '%4s' % (newFlag + str(memUsage + kmemUsage) + dieFlag)
                    SystemManager.addPrint("%16s(%5s/%5s): " % \
                        (value['comm'], key, value['tgid']) + timeLine + '\n')

                    if (value['nrPages'] >> 8) + (value['remainKmem'] >> 20) < 1 and \
                        SystemManager.showAll == False:
                        break

            SystemManager.pipePrint("%s# %s\n" % ('', 'MEM(MB)'))
            SystemManager.pipePrint(SystemManager.bufferString)
            SystemManager.pipePrint(oneLine)

        # block read usage on timeline #
        SystemManager.clearPrint()
        if SystemManager.blockEnable:
            for key, value in sorted(\
                self.threadData.items(), key=lambda e: e[1]['reqBlock'], reverse=True):

                if key[0:2] != '0[':
                    timeLine = ''
                    timeLineLen = titleLineLen
                    lval = int(float(self.totalTime) / SystemManager.intervalEnable) + 1
                    for icount in xrange(0, lval):
                        newFlag = ' '
                        dieFlag = ' '

                        if timeLineLen + 4 > maxLineLen:
                            timeLine += ('\n' + (' ' * (titleLineLen + 1)))
                            timeLineLen = titleLineLen + 4
                        else:
                            timeLineLen += 4

                        try:
                            self.intervalData[icount][key]
                        except:
                            timeLine += '%3d ' % 0
                            continue

                        nowVal = self.intervalData[icount][key]

                        try:
                            prevVal = self.intervalData[icount - 1][key]
                        except:
                            prevVal = nowVal

                        if icount > 0:
                            try:
                                if nowVal['new'] != prevVal['new']:
                                    newFlag = self.intervalData[icount][key]['new']
                            except:
                                newFlag = nowVal['new']
                            try:
                                if nowVal['die'] != prevVal['die']:
                                    dieFlag = nowVal['die']
                            except:
                                dieFlag = nowVal['die']
                        else:
                            newFlag = nowVal['new']
                            dieFlag = nowVal['die']

                        timeLine += '%4s' % (newFlag + \
                            str(int((self.intervalData[icount][key]['brUsage'] * \
                            SystemManager.blockSize) >> 20)) + dieFlag)

                    SystemManager.addPrint("%16s(%5s/%5s): " % \
                        (value['comm'], key, value['tgid']) + timeLine + '\n')

                    if value['readBlock'] < 1 and SystemManager.showAll == False:
                        break

            SystemManager.pipePrint("%s# %s\n" % ('', 'BLK_RD(MB)'))
            SystemManager.pipePrint(SystemManager.bufferString)
            SystemManager.pipePrint(oneLine)

        # block write usage on timeline #
        SystemManager.clearPrint()
        if SystemManager.blockEnable:
            for key, value in sorted(\
                self.threadData.items(), key=lambda e: e[1]['writeBlock'], reverse=True):

                if key[0:2] != '0[':
                    timeLine = ''
                    timeLineLen = titleLineLen
                    lval = int(float(self.totalTime) / SystemManager.intervalEnable) + 1
                    for icount in xrange(0, lval):
                        newFlag = ' '
                        dieFlag = ' '

                        if timeLineLen + 4 > maxLineLen:
                            timeLine += ('\n' + (' ' * (titleLineLen + 1)))
                            timeLineLen = titleLineLen + 4
                        else:
                            timeLineLen += 4

                        try:
                            self.intervalData[icount][key]
                        except:
                            timeLine += '%3d ' % 0
                            continue

                        nowVal = self.intervalData[icount][key]

                        try:
                            prevVal = self.intervalData[icount - 1][key]
                        except:
                            prevVal = nowVal

                        if icount > 0:
                            try:
                                if nowVal['new'] != prevVal['new']:
                                    newFlag = self.intervalData[icount][key]['new']
                            except:
                                newFlag = nowVal['new']
                            try:
                                if nowVal['die'] != prevVal['die']:
                                    dieFlag = nowVal['die']
                            except:
                                dieFlag = nowVal['die']
                        else:
                            newFlag = nowVal['new']
                            dieFlag = nowVal['die']

                        timeLine += '%4s' % (newFlag + \
                            str(int((self.intervalData[icount][key]['bwUsage'] * \
                            SystemManager.pageSize) >> 20)) + dieFlag)

                    SystemManager.addPrint("%16s(%5s/%5s): " % \
                        (value['comm'], key, value['tgid']) + timeLine + '\n')

                    if value['writeBlockCnt'] < 1 and SystemManager.showAll == False:
                        break

            SystemManager.pipePrint("%s# %s\n" % ('', 'BLK_WR(MB)'))
            SystemManager.pipePrint(SystemManager.bufferString)
            SystemManager.pipePrint(oneLine)

        # event usage on timeline #
        self.printEventIntervalInfo()

        # save graph #
        if SystemManager.graphEnable and\
            (len(cpuUsageList) > 0 or len(ioUsageList) > 0):
            dirPos = SystemManager.inputFile.rfind('/')
            if dirPos >= 0:
                graphPath = SystemManager.inputFile[:dirPos + 1] + 'guider.png'
                savefig(graphPath, dpi=(200))
                clf()
                SystemManager.printStatus("write resource graph to %s" % graphPath)
            else:
                SystemManager.printWarning("Fail to draw graph")



    def getNetworkUsage(self, prev, now):
        if prev == now:
            return ('-', '-')

        nowIn = nowOut = prevIn = prevOut = 0

        try:
            idx = -1

            for line in now:
                idx += 1
                if not line.startswith('IpExt'):
                    continue

                if SystemManager.netInIndex < 0:
                    SystemManager.netInIndex = line.split().index('InOctets')

                try:
                    nowStat = line.split()
                    nowIn = long(nowStat[SystemManager.netInIndex])
                    nowOut = long(nowStat[SystemManager.netInIndex + 1])

                    prevStat = prev[idx].split()
                    prevIn = long(prevStat[SystemManager.netInIndex])
                    prevOut = long(prevStat[SystemManager.netInIndex + 1])

                    inDiff = nowIn - prevIn
                    recv = inDiff >> 20
                    if recv > 0:
                        recv = '%sM' % recv
                    else:
                        recv = '%sK' % (inDiff >> 10)

                    outDiff = nowOut - prevOut
                    send = outDiff >> 20
                    if send > 0:
                        send = '%sM' % send
                    else:
                        send = '%sK' % (outDiff >> 10)

                    return (recv, send)
                except:
                    pass
        except:
            pass

        return ('-', '-')



    @staticmethod
    def parseProcLine(index, procLine):
        # Get time info #
        if 'time' not in ThreadAnalyzer.procIntervalData[index]:
            m = re.match(r'.+\[Time:\s*(?P<time>[0-9]+.[0-9]+)\].+' + \
                r'\[Ctxt:\s*(?P<nrCtxt>[0-9]+)\].+\[IRQ:\s*(?P<nrIrq>[0-9]+)\].+' + \
                r'\[Task:\s*(?P<nrProc>[0-9]+)/(?P<nrThread>[0-9]+)', procLine)
            if m is not None:
                d = m.groupdict()
                ThreadAnalyzer.procIntervalData[index]['time'] = d['time']
                ThreadAnalyzer.procIntervalData[index]['nrCtxt'] = d['nrCtxt']
                ThreadAnalyzer.procIntervalData[index]['nrIrq'] = d['nrIrq']
                ThreadAnalyzer.procIntervalData[index]['nrProc'] = d['nrProc']
                ThreadAnalyzer.procIntervalData[index]['nrThread'] = d['nrThread']
            return

        # Get total resource usage #
        if 'total' not in ThreadAnalyzer.procIntervalData[index]:
            tokenList = procLine.split('|')

            if len(tokenList) < 4 or tokenList[0].find('Total') < 0:
                return

            m = re.match(r'\s*(?P<cpu>\-*[0-9]+)\s*%\s*\(\s*(?P<user>\-*[0-9]+)\s*\/s*\s*' + \
                r'(?P<kernel>\-*[0-9]+)\s*\/s*\s*(?P<block>\-*[0-9]+)', tokenList[1])
            if m is not None:
                d = m.groupdict()

                ThreadAnalyzer.procTotalData['total']['cpu'] += int(d['cpu'])

                ThreadAnalyzer.procIntervalData[index]['total'] = \
                    dict(ThreadAnalyzer.init_procIntervalData)
                try:
                    ThreadAnalyzer.procIntervalData[index]['total']['cpu'] = int(d['cpu'])
                except:
                    ThreadAnalyzer.procIntervalData[index]['total']['cpu'] = 0

                try:
                    ThreadAnalyzer.procIntervalData[index]['total']['blkwait'] = int(d['block'])
                except:
                    ThreadAnalyzer.procIntervalData[index]['total']['blkwait'] = 0
            else:
                return

            m = re.match(r'\s*(?P<free>\-*[0-9]+)\s*\(\s*(?P<freeDiff>\-*[0-9]+)', tokenList[2])
            if m is not None:
                d = m.groupdict()

                freeMem = int(d['free'])
                freeMemDiff = int(d['freeDiff'])

                if ThreadAnalyzer.procTotalData['total']['initMem'] == 0:
                    ThreadAnalyzer.procTotalData['total']['initMem'] = freeMem

                ThreadAnalyzer.procTotalData['total']['lastMem'] = freeMem

                ThreadAnalyzer.procIntervalData[index]['total']['mem'] = freeMem
                ThreadAnalyzer.procIntervalData[index]['total']['memDiff'] = freeMemDiff
            else:
                return

            try:
                ThreadAnalyzer.procIntervalData[index]['total']['blk'] = tokenList[5]
            except:
                ThreadAnalyzer.procIntervalData[index]['total']['blk'] = '-'

            m = re.match(r'\s*(?P<swap>\-*[0-9]+)', tokenList[3])
            if m is not None:
                d = m.groupdict()

                ThreadAnalyzer.procIntervalData[index]['total']['swap'] = int(d['swap'])
            else:
                return

            try:
                ThreadAnalyzer.procIntervalData[index]['total']['rclm'] = tokenList[4].strip()
            except:
                ThreadAnalyzer.procIntervalData[index]['total']['rclm'] = '-'

            try:
                ThreadAnalyzer.procIntervalData[index]['total']['nrFlt'] = int(tokenList[6])
            except:
                ThreadAnalyzer.procIntervalData[index]['total']['nrFlt'] = '-'

            try:
                ThreadAnalyzer.procIntervalData[index]['total']['netIO'] = tokenList[11].strip()
            except:
                ThreadAnalyzer.procIntervalData[index]['total']['netIO'] = '-'

            return

        # Get process resource usage #
        m = re.match(r'\s*(?P<comm>.+) \(\s*(?P<pid>[0-9]+)\/\s*(?P<ppid>[0-9]+)' + \
            r'\/\s*(?P<nrThreads>[0-9]+)\/(?P<pri>.{4})\)\|\s*(?P<cpu>[0-9]+)' + \
            r'\(.+\)\|.+\(\s*(?P<rss>[0-9]+)\/.+\)\|\s*(?P<blk>[0-9]+)\(', procLine)
        if m is not None:
            d = m.groupdict()
            pid = d['pid']

            # ignore created / terminated process #
            if d['comm'][0:3] == '[+]' or d['comm'][0:3] == '[-]':
                return

            if pid not in ThreadAnalyzer.procTotalData:
                ThreadAnalyzer.procTotalData[pid] = dict(ThreadAnalyzer.init_procTotalData)
                ThreadAnalyzer.procTotalData[pid]['startIdx'] = index

            ThreadAnalyzer.procTotalData[pid]['comm'] = d['comm']
            ThreadAnalyzer.procTotalData[pid]['ppid'] = d['ppid']
            ThreadAnalyzer.procTotalData[pid]['nrThreads'] = d['nrThreads']
            ThreadAnalyzer.procTotalData[pid]['pri'] = d['pri']

            ThreadAnalyzer.procTotalData[pid]['cpu'] += int(d['cpu'])
            ThreadAnalyzer.procTotalData[pid]['blk'] += int(d['blk'])

            if ThreadAnalyzer.procTotalData[pid]['initMem'] == 0:
                ThreadAnalyzer.procTotalData[pid]['initMem'] = int(d['rss'])
                ThreadAnalyzer.procTotalData[pid]['lastMem'] = int(d['rss'])

            if pid not in ThreadAnalyzer.procIntervalData[index]:
                ThreadAnalyzer.procIntervalData[index][pid] = \
                    dict(ThreadAnalyzer.init_procIntervalData)
                ThreadAnalyzer.procIntervalData[index][pid]['cpu'] = int(d['cpu'])
                ThreadAnalyzer.procIntervalData[index][pid]['blk'] = int(d['blk'])
                ThreadAnalyzer.procIntervalData[index][pid]['mem'] = int(d['rss'])
                ThreadAnalyzer.procIntervalData[index][pid]['memDiff'] = \
                    int(d['rss']) - ThreadAnalyzer.procTotalData[pid]['lastMem']

                ThreadAnalyzer.procTotalData[pid]['lastMem'] = int(d['rss'])



    @staticmethod
    def summarizeIntervalUsage():
        if 'total' not in ThreadAnalyzer.procTotalData:
            ThreadAnalyzer.procTotalData['total'] = dict(ThreadAnalyzer.init_procTotalData)

        idx = 0
        for val in reversed(SystemManager.procBuffer):
            if len(ThreadAnalyzer.procIntervalData) < idx + 1:
                ThreadAnalyzer.procIntervalData.append({})

            procData = val.split('\n')

            for line in procData:
                ThreadAnalyzer.parseProcLine(idx, line)

            idx += 1

        if idx > 0:
            for pid, val in ThreadAnalyzer.procTotalData.items():
                val['cpu'] /= idx
                val['memDiff'] = val['lastMem'] - val['initMem']



    @staticmethod
    def printFileTable():
        if SystemManager.fileInstance is None:
            return

        nrEvent = nrSocket = nrDevice = nrPipe = nrProc = nrFile = 0
        for filename in SystemManager.fileInstance.keys():
            # increase type count per process #
            if filename.startswith('anon'):
                nrEvent  += 1
            elif filename.startswith('socket'):
                nrSocket += 1
            elif filename.startswith('/dev'):
                nrDevice += 1
            elif filename.startswith('pipe'):
                nrPipe += 1
            elif filename.startswith('/proc'):
                nrProc += 1
            else:
                nrFile += 1

        SystemManager.pipePrint(\
            ('\n[Top File Table] [TOTAL: %d] [FILE: %d] [EVENT: %d] '\
            '[SOCKET: %d] [DEV: %d] [PIPE: %d] [PROC: %d]\n') %\
            (len(SystemManager.fileInstance), nrFile, nrEvent,\
            nrSocket, nrDevice, nrPipe, nrProc))
        SystemManager.pipePrint(twoLine + '\n')
        SystemManager.pipePrint("{0:^5} | {1:^144} |\n".format('REF', 'FILE'))
        SystemManager.pipePrint(oneLine + '\n')

        for filename, value in sorted(SystemManager.fileInstance.items(),\
            key=lambda e: int(e[1]), reverse=True):
            SystemManager.pipePrint("{0:>5} | {1:<144} |\n".format(value, filename))

        if len(SystemManager.fileInstance) == 0:
            SystemManager.pipePrint('\tN/A\n')

        SystemManager.pipePrint(oneLine + '\n')



    @staticmethod
    def printTimeline():
        SystemManager.pipePrint('\n[Top Summary Info]\n')
        SystemManager.pipePrint(twoLine + '\n')

        SystemManager.pipePrint(("{0:^5} | {1:^27} | {2:^6} | {3:^8} | {4:^9} | {5:^10} | " +\
            "{6:^8} | {7:^8} | {8:^5} | {9:^6} | {10:^6} | {11:^8} | {12:^10} |\n").\
            format('IDX', 'Interval', 'CPU(%)', 'MEM(MB)', 'BlkRW(MB)', 'BlkWait(%)',\
            'SWAP(MB)', 'Rclm(MB)', 'NrFlt', 'NrCtxt', 'NrIRQ', 'NrTask', 'NetIO'))
        SystemManager.pipePrint(oneLine + '\n')

        for idx, val in list(enumerate(ThreadAnalyzer.procIntervalData)):
            if idx == 0:
                before = 'START'
            else:
                before = ThreadAnalyzer.procIntervalData[idx - 1]['time']

            if 'total' not in val:
                continue

            task = '%s/%s' % (val['nrProc'], val['nrThread'])
            SystemManager.pipePrint(("{0:>5} | {1:>12} - {2:>12} | {3:>6} | {4:>8} | {5:^9} | " +\
                "{6:>10} | {7:>8} | {8:^8} | {9:>5} | {10:>6} | {11:>6} | {12:>8} | {13:^10} |\n").\
                format(idx + 1, before, val['time'], val['total']['cpu'], val['total']['mem'],\
                val['total']['blk'], val['total']['blkwait'], val['total']['swap'], \
                val['total']['rclm'], val['total']['nrFlt'], val['nrCtxt'], val['nrIrq'], \
                task, val['total']['netIO']))

        if len(ThreadAnalyzer.procIntervalData) == 0:
            SystemManager.pipePrint('\tNone\n')

        SystemManager.pipePrint(oneLine + '\n')



    @staticmethod
    def printCpuInterval():
        # Print title #
        SystemManager.pipePrint('\n[Top CPU Info] [Unit: %]\n')
        SystemManager.pipePrint(twoLine + '\n')

        # Print menu #
        procInfo = "{0:^16} ({1:^5}/{2:^5}/{3:^4}/{4:>4})| {5:3} |".\
            format('COMM', "ID", "Pid", "Nr", "Pri", "Avg")
        procInfoLen = len(procInfo)
        maxLineLen = SystemManager.lineLength

        # Print timeline #
        timeLine = ''
        lineLen = len(procInfo)
        for i in xrange(1,len(ThreadAnalyzer.procIntervalData) + 1):
            if lineLen + 5 > maxLineLen:
                timeLine += ('\n' + (' ' * (procInfoLen - 1)) + '| ')
                lineLen = len(procInfo)

            timeLine += '{0:^5}'.format(i)
            lineLen += 5

        SystemManager.pipePrint(("{0:1} {1:1}\n").format(procInfo, timeLine))
        SystemManager.pipePrint(twoLine + '\n')

        # Print total cpu usage #
        value = ThreadAnalyzer.procTotalData['total']
        procInfo = "{0:^16} ({1:^5}/{2:^5}/{3:^4}/{4:>4})| {5:3} |".\
            format('[CPU]', '-', '-', '-', '-', value['cpu'])
        procInfoLen = len(procInfo)
        maxLineLen = SystemManager.lineLength

        timeLine = ''
        lineLen = len(procInfo)
        for idx in xrange(0,len(ThreadAnalyzer.procIntervalData)):
            if lineLen + 5 > maxLineLen:
                timeLine += ('\n' + (' ' * (procInfoLen - 1)) + '| ')
                lineLen = len(procInfo)

            if 'total' in ThreadAnalyzer.procIntervalData[idx]:
                usage = ThreadAnalyzer.procIntervalData[idx]['total']['cpu']
            else:
                usage = 0

            timeLine += '{0:^5}'.format(usage)
            lineLen += 5

        SystemManager.pipePrint(("{0:1} {1:1}\n").format(procInfo, timeLine))
        SystemManager.pipePrint(oneLine + '\n')

        # Print cpu usage of processes #
        for pid, value in sorted(\
            ThreadAnalyzer.procTotalData.items(), key=lambda e: e[1]['cpu'], reverse=True):

            if pid is 'total':
                continue

            procInfo = "{0:>16} ({1:>5}/{2:>5}/{3:>4}/{4:>4})| {5:3} |".\
                format(value['comm'], pid, value['ppid'], value['nrThreads'], \
                value['pri'], value['cpu'])
            procInfoLen = len(procInfo)
            maxLineLen = SystemManager.lineLength

            timeLine = ''
            lineLen = len(procInfo)
            total = 0
            for idx in xrange(0,len(ThreadAnalyzer.procIntervalData)):
                if lineLen + 5 > maxLineLen:
                    timeLine += ('\n' + (' ' * (procInfoLen - 1)) + '| ')
                    lineLen = len(procInfo)

                if pid in ThreadAnalyzer.procIntervalData[idx]:
                    usage = ThreadAnalyzer.procIntervalData[idx][pid]['cpu']
                    total += ThreadAnalyzer.procIntervalData[idx][pid]['cpu']
                else:
                    usage = 0

                timeLine += '{0:^5}'.format(usage)
                lineLen += 5

            # skip process used no cpu #
            if total == 0:
                continue

            SystemManager.pipePrint(("{0:1} {1:1}\n").format(procInfo, timeLine))
            SystemManager.pipePrint(oneLine + '\n')



    @staticmethod
    def printMemInterval():
        # Print title #
        SystemManager.pipePrint('\n[Top Memory Info] [Unit: MB]\n')
        SystemManager.pipePrint(twoLine + '\n')

        # Print menu #
        procInfo = "{0:^16} ({1:^5}/{2:^5}/{3:^4}/{4:>4})| {5:4} |".\
            format('COMM', "ID", "Pid", "Nr", "Pri", "Diff")
        procInfoLen = len(procInfo)
        maxLineLen = SystemManager.lineLength

        # Print timeline #
        timeLine = ''
        lineLen = len(procInfo)
        for i in xrange(1,len(ThreadAnalyzer.procIntervalData) + 1):
            if lineLen + 5 > maxLineLen:
                timeLine += ('\n' + (' ' * (procInfoLen - 1)) + '| ')
                lineLen = len(procInfo)

            timeLine += '{0:^5}'.format(i)
            lineLen += 5

        SystemManager.pipePrint(("{0:1} {1:1}\n").format(procInfo, timeLine))
        SystemManager.pipePrint(twoLine + '\n')

        # Print total memory usage #
        value = ThreadAnalyzer.procTotalData['total']
        procInfo = "{0:^16} ({1:^5}/{2:^5}/{3:^4}/{4:>4})| {5:4} |".\
            format('[FREE]', '-', '-', '-', '-', value['memDiff'])
        procInfoLen = len(procInfo)
        maxLineLen = SystemManager.lineLength

        timeLine = ''
        lineLen = len(procInfo)
        for idx in xrange(0,len(ThreadAnalyzer.procIntervalData)):
            if lineLen + 5 > maxLineLen:
                timeLine += ('\n' + (' ' * (procInfoLen - 1)) + '| ')
                lineLen = len(procInfo)

            if 'total' in ThreadAnalyzer.procIntervalData[idx]:
                usage = ThreadAnalyzer.procIntervalData[idx]['total']['memDiff']
            else:
                usage = 0

            timeLine += '{0:^5}'.format(usage)
            lineLen += 5

        SystemManager.pipePrint(("{0:1} {1:1}\n").format(procInfo, timeLine))
        SystemManager.pipePrint(oneLine + '\n')

        # Print memory usage of processes #
        for pid, value in sorted(\
            ThreadAnalyzer.procTotalData.items(), key=lambda e: e[1]['memDiff'], reverse=True):

            if pid is 'total' or value['memDiff'] == 0:
                continue

            procInfo = "{0:>16} ({1:>5}/{2:>5}/{3:>4}/{4:>4})| {5:4} |".\
                format(value['comm'], pid, value['ppid'], value['nrThreads'], value['pri'], value['memDiff'])
            procInfoLen = len(procInfo)
            maxLineLen = SystemManager.lineLength

            timeLine = ''
            lineLen = len(procInfo)
            for idx in xrange(0,len(ThreadAnalyzer.procIntervalData)):
                if lineLen + 5 > maxLineLen:
                    timeLine += ('\n' + (' ' * (procInfoLen - 1)) + '| ')
                    lineLen = len(procInfo)

                if pid in ThreadAnalyzer.procIntervalData[idx]:
                    usage = ThreadAnalyzer.procIntervalData[idx][pid]['memDiff']
                else:
                    usage = 0

                timeLine += '{0:^5}'.format(usage)
                lineLen += 5

            SystemManager.pipePrint(("{0:1} {1:1}\n").format(procInfo, timeLine))
            SystemManager.pipePrint(oneLine + '\n')



    @staticmethod
    def printBlkInterval():
        # Print title #
        SystemManager.pipePrint('\n[Top Block Info] [Unit: %]\n')
        SystemManager.pipePrint(twoLine + '\n')

        # Print menu #
        procInfo = "{0:^16} ({1:^5}/{2:^5}/{3:^4}/{4:>4})| {5:3} |".\
            format('COMM', "ID", "Pid", "Nr", "Pri", "Sum")
        procInfoLen = len(procInfo)
        maxLineLen = SystemManager.lineLength

        # Print timeline #
        timeLine = ''
        lineLen = len(procInfo)
        for i in xrange(1,len(ThreadAnalyzer.procIntervalData) + 1):
            if lineLen + 5 > maxLineLen:
                timeLine += ('\n' + (' ' * (procInfoLen - 1)) + '| ')
                lineLen = len(procInfo)

            timeLine += '{0:^5}'.format(i)
            lineLen += 5

        SystemManager.pipePrint(("{0:1} {1:1}\n").format(procInfo, timeLine))
        SystemManager.pipePrint(twoLine + '\n')

        # Print block usage of processes #
        itemCnt = 0
        for pid, value in sorted(\
            ThreadAnalyzer.procTotalData.items(), key=lambda e: e[1]['blk'], reverse=True):

            if pid is 'total' or value['blk'] == 0:
                continue

            procInfo = "{0:>16} ({1:>5}/{2:>5}/{3:>4}/{4:>4})| {5:3} |".\
                format(value['comm'], pid, value['ppid'], value['nrThreads'], value['pri'], value['blk'])
            procInfoLen = len(procInfo)
            maxLineLen = SystemManager.lineLength

            timeLine = ''
            lineLen = len(procInfo)
            for idx in xrange(0,len(ThreadAnalyzer.procIntervalData)):
                if lineLen + 5 > maxLineLen:
                    timeLine += ('\n' + (' ' * (procInfoLen - 1)) + '| ')
                    lineLen = len(procInfo)

                if pid in ThreadAnalyzer.procIntervalData[idx]:
                    usage = ThreadAnalyzer.procIntervalData[idx][pid]['blk']
                else:
                    usage = 0

                timeLine += '{0:^5}'.format(usage)
                lineLen += 5

            SystemManager.pipePrint(("{0:1} {1:1}\n").format(procInfo, timeLine))
            SystemManager.pipePrint(oneLine + '\n')
            itemCnt += 1

        if itemCnt == 0:
            SystemManager.pipePrint('\tNone\n')
            SystemManager.pipePrint(oneLine + '\n')



    @staticmethod
    def printIntervalUsage():
        if SystemManager.fileTopEnable:
            ThreadAnalyzer.printFileTable()
        else:
            # print summarized interval table #
            ThreadAnalyzer.summarizeIntervalUsage()

            # print interval info #
            ThreadAnalyzer.printTimeline()
            ThreadAnalyzer.printCpuInterval()
            ThreadAnalyzer.printMemInterval()
            ThreadAnalyzer.printBlkInterval()

        # print interval info #
        ThreadAnalyzer.printMemAnalysis()

        msg = ' Detailed Statistics '
        stars = '*' * ((int(SystemManager.lineLength) - len(msg)) / 2)
        SystemManager.pipePrint('\n\n\n\n%s%s%s\n' % (stars, msg, stars))

        # print detailed statistics #
        SystemManager.pipePrint(SystemManager.procBuffer)

        # initialize parse buffer #
        ThreadAnalyzer.procTotalData = {}
        ThreadAnalyzer.procIntervalData = []



    @staticmethod
    def printMemAnalysis():
        if SystemManager.procInstance is None:
            return

        # Print title #
        SystemManager.pipePrint('\n[Top Memory Details] [Unit: MB]\n')
        SystemManager.pipePrint(twoLine + '\n')

        # Print menu #
        SystemManager.pipePrint(("{0:^16} ({1:^5}/{2:^5}) | {3:^8} | {4:^5} | "
            "{5:^6} | {6:^6} | {7:^6} | {8:^6} | {9:^6} | {10:^10} | "
            "{11:^12} | {12:^12} |\n{13}\n").\
            format('COMM', 'ID', 'Pid', 'Type', 'Cnt', \
            'VIRT', 'RSS', 'PSS', 'SWAP', 'HUGE', 'LOCKED(KB)', \
            'PDIRTY(KB)', 'SDIRTY(KB)', twoLine))

        cnt = 1
        limitProcCnt = 6
        commIdx = ConfigManager.statList.index("COMM")
        ppidIdx = ConfigManager.statList.index("PPID")

        try:
            sortedList = sorted(SystemManager.procInstance.items(), \
                key=lambda e: long(e[1]['stat'][ConfigManager.statList.index("RSS")]), reverse=True)
        except:
            SystemManager.printWarning("Fail to get memory details because of sort error")
            SystemManager.pipePrint("\tNone\n%s\n" % oneLine)
            return

        for key, value in sortedList:
            # check filter #
            if SystemManager.showGroup != []:
                skip = True
                for item in SystemManager.showGroup:
                    if key == item or value['stat'][commIdx].find(item) >= 0:
                        skip = False
                        break
                if skip:
                    continue

            # only print memory details of top 4 processes #
            if cnt > limitProcCnt:
                break

            if value['maps'] is None:
                # get memory details #
                ThreadAnalyzer.saveProcSmapsData(value['taskPath'], key)

            if value['maps'] is not None:
                cnt += 1

                totalCnt = 0
                totalVmem = 0
                totalRss = 0
                totalPss = 0
                totalSwap = 0
                totalHuge = 0
                totalLock = 0
                totalPdirty = 0
                totalSdirty = 0

                procInfo = ' '
                procDetails = ''

                for idx, item in sorted(value['maps'].items(), reverse=True):
                    if len(item) == 0:
                        continue

                    totalCnt += item['count']

                    try:
                        vmem = item['Size:'] >> 10
                        totalVmem += vmem
                    except:
                        vmem = 0

                    try:
                        rss = item['Rss:'] >> 10
                        totalRss += rss
                    except:
                        rss = 0

                    try:
                        pss = item['Pss:'] >> 10
                        totalPss += pss
                    except:
                        pss = 0

                    try:
                        swap = item['Swap:'] >> 10
                        totalSwap += swap
                    except:
                        swap = 0

                    try:
                        huge = item['AnonHugePages:'] >> 10
                        totalHuge += huge
                    except:
                        huge = 0

                    try:
                        lock = item['Locked:']
                        totalLock += lock
                    except:
                        lock = 0

                    try:
                        pdirty = item['Private_Dirty:']
                        totalPdirty += pdirty
                    except:
                        pdirty = 0

                    try:
                        sdirty = item['Shared_Dirty:']
                        totalSdirty += sdirty
                    except:
                        sdirty = 0

                    procDetails = "%s%s" % (procDetails, ("{0:>30} | {1:>8} | {2:>5} | "
                        "{3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>10} | "
                        "{9:>12} | {10:>12} |\n").\
                        format(procInfo, idx, item['count'], \
                        vmem, rss, pss, swap, huge, lock, pdirty, sdirty))

                if SystemManager.processEnable:
                    ppid = value['stat'][ppidIdx]
                else:
                    ppid = value['mainID']

                procInfo = "{0:>16} ({1:>5}/{2:>5})".\
                        format(value['stat'][commIdx][1:-1], key, ppid)

                SystemManager.pipePrint(("{0:>30} | {1:>8} | {2:>5} | "
                    "{3:>6} | {4:>6} | {5:>6} | {6:>6} | {7:>6} | {8:>10} | "
                    "{9:>12} | {10:>12} |\n{11}").\
                    format(procInfo, '[TOTAL]', totalCnt, \
                    totalVmem, totalRss, totalPss, totalSwap, totalHuge, totalLock, \
                    totalPdirty, totalSdirty, procDetails))

                SystemManager.pipePrint('%s\n' % oneLine)

        if cnt == 1:
            SystemManager.pipePrint("\tNone\n%s\n" % oneLine)



    @staticmethod
    def getInitTime(file):
        systemInfoBuffer = ''

        if SystemManager.isRecordMode():
            nrLine = SystemManager.pageSize
        else:
            nrLine = 0

        while 1:
            start = end = -1
            buf = None

            # make delay because some filtered logs are not written soon #
            time.sleep(0.1)

            try:
                with open(file, 'r') as fd:
                    buf = fd.readlines(nrLine)
            except IOError:
                SystemManager.printError("Fail to open %s" % file)
                sys.exit(0)

            # verify log buffer #
            for idx, line in enumerate(buf):
                # check system info #
                if SystemManager.recordStatus is False:
                    if line[0:-1] == SystemManager.magicString:
                        if start == -1:
                            start = idx
                        elif end == -1:
                            end = idx
                            SystemManager.systemInfoBuffer = ''.join(buf[start+1:end])
                        continue

                m = re.match(r'^\s*(?P<comm>\S+)-(?P<thread>[0-9]+)\s+\(\s*(?P<tgid>\S+)\)' + \
                    r'\s+\[(?P<core>[0-9]+)\]\s+(?P<time>\S+):\s+(?P<func>\S+):(?P<etc>.+)', line)
                if m is not None:
                    d = m.groupdict()
                    return d['time']

                m = re.match(r'^\s*(?P<comm>\S+)-(?P<thread>[0-9]+)\s+\[(?P<core>[0-9]+)\]' + \
                    r'\s+(?P<time>\S+):\s+(?P<func>\S+):(?P<etc>.+)', line)
                if m is not None:
                    d = m.groupdict()
                    SystemManager.tgidEnable = False
                    return d['time']

            # check record status #
            if SystemManager.recordStatus is False:
                SystemManager.printError(\
                    "Fail to recognize format: corrupted log / no log collected")
                sys.exit(0)



    def savePartOpt(self, tid, comm, opt, major, minor, addr, size):
        # apply filter #
        if len(SystemManager.showGroup) > 0:
            found = False
            for val in SystemManager.showGroup:
                if comm.rfind(val) > -1 or tid == val:
                    found = True
                    break
            if found is False:
                return

        if opt == 'R':
            try:
                self.blockTable[0][major + ':' + minor] += int(size)
            except:
                self.blockTable[0][major + ':' + minor] = 0
                self.blockTable[0][major + ':' + minor] += int(size)
        elif opt == 'W':
            try:
                self.blockTable[1][major + ':' + minor] += int(size)
            except:
                self.blockTable[1][major + ':' + minor] = 0
                self.blockTable[1][major + ':' + minor] += int(size)
        else:
            SystemManager.printWarning("Fail to recognize operation of block event")



    def processIntervalData(self, time):
        if SystemManager.intervalEnable == 0:
            return

        intervalCnt = float(SystemManager.intervalNow + SystemManager.intervalEnable)

        if float(time) - float(self.startTime) > intervalCnt or self.finishTime != '0':
            SystemManager.intervalNow += SystemManager.intervalEnable

            # check change of all threads #
            for key, value in sorted(self.threadData.items(), \
                key=lambda e: e[1]['usage'], reverse=True):
                index = int(SystemManager.intervalNow / SystemManager.intervalEnable) - 1
                nextIndex = int(SystemManager.intervalNow / SystemManager.intervalEnable)

                try:
                    self.intervalData[index]
                except:
                    self.intervalData.append({})
                try:
                    self.intervalData[index][key]
                except:
                    self.intervalData[index][key] = dict(self.init_intervalData)

                try:
                    self.intervalData[index]['toTal']
                except:
                    self.intervalData[index]['toTal'] = \
                        {'totalBr': int(0), 'totalBw': int(0), \
                        'totalMem': int(0), 'totalKmem': int(0)}

                    # make total custom event list #
                    if len(SystemManager.customEventList) > 0:
                        self.intervalData[index]['toTal']['customEvent'] = {}
                        for evt in SystemManager.customEventList:
                            self.intervalData[index]['toTal']['customEvent'][evt] = \
                                dict(self.init_eventData)

                    # make user event list #
                    if len(SystemManager.userEventList) > 0:
                        self.intervalData[index]['toTal']['userEvent'] = {}
                        for evt in SystemManager.userEventList:
                            self.intervalData[index]['toTal']['userEvent'][evt] = \
                                dict(self.init_eventData)

                    # make kernel event list #
                    if len(SystemManager.kernelEventList) > 0:
                        self.intervalData[index]['toTal']['kernelEvent'] = {}
                        for evt in SystemManager.kernelEventList:
                            self.intervalData[index]['toTal']['kernelEvent'][evt] = \
                                dict(self.init_eventData)

                # define thread alias in this interval #
                intervalThread = self.intervalData[index][key]

                # save start time in this interval #
                intervalThread['firstLogTime'] = float(time)

                # make interval list #
                try:
                    self.intervalData[nextIndex]
                except:
                    self.intervalData.append({})
                try:
                    self.intervalData[nextIndex][key]
                except:
                    self.intervalData[nextIndex][key] = dict(self.init_intervalData)

                # save total usage in this interval #
                intervalThread['totalUsage'] = float(self.threadData[key]['usage'])
                intervalThread['totalPreempted'] = float(self.threadData[key]['cpuWait'])
                intervalThread['totalCoreSchedCnt'] = int(self.threadData[key]['coreSchedCnt'])
                intervalThread['totalBrUsage'] = int(self.threadData[key]['reqBlock'])
                intervalThread['totalBwUsage'] = int(self.threadData[key]['writeBlock'])
                intervalThread['totalMemUsage'] = int(self.threadData[key]['nrPages'])
                intervalThread['totalKmemUsage'] = int(self.threadData[key]['remainKmem'])

                # add core time not calculated yet in this interval #
                for idx, val in self.lastTidPerCore.items():
                    if self.threadData[val]['lastStatus'] == 'S':
                        # apply core off time #
                        coreId = '0[%s]' % idx
                        if self.threadData[coreId]['lastOff'] > 0:
                            diff = float(time) - self.threadData[coreId]['start']
                            self.threadData[coreId]['usage'] += diff
                            self.intervalData[index][coreId]['totalUsage'] += diff
                            self.threadData[coreId]['start'] = float(time)
                        continue

                    intervalThread['totalUsage'] += \
                        (float(time) - float(self.threadData[val]['start']))

                # mark life flag #
                if self.threadData[key]['new'] != ' ':
                    intervalThread['new'] = self.threadData[key]['new']
                if self.threadData[key]['die'] != ' ':
                    intervalThread['die'] = self.threadData[key]['die']

                # initialize custom event list #
                if len(SystemManager.customEventList) > 0:
                    intervalThread['customEvent'] = {}
                    intervalThread['totalCustomEvent'] = {}
                    for evt in SystemManager.customEventList:
                        intervalThread['customEvent'][evt] = dict(self.init_eventData)
                        intervalThread['totalCustomEvent'][evt] = dict(self.init_eventData)
                        try:
                            intervalThread['totalCustomEvent'][evt]['count'] = \
                                self.threadData[key]['customEvent'][evt]['count']
                        except:
                            pass

                # initialize user event list #
                if len(SystemManager.userEventList) > 0:
                    intervalThread['userEvent'] = {}
                    intervalThread['totalUserEvent'] = {}
                    for evt in SystemManager.userEventList:
                        intervalThread['userEvent'][evt] = dict(self.init_eventData)
                        intervalThread['totalUserEvent'][evt] = dict(self.init_eventData)
                        try:
                            intervalThread['totalUserEvent'][evt]['count'] = \
                                self.threadData[key]['userEvent'][evt]['count']

                            intervalThread['totalUserEvent'][evt]['usage'] = \
                                self.threadData[key]['userEvent'][evt]['usage']
                        except:
                            pass

                # initialize kernel event list #
                if len(SystemManager.kernelEventList) > 0:
                    intervalThread['kernelEvent'] = {}
                    intervalThread['totalKernelEvent'] = {}
                    for evt in SystemManager.kernelEventList:
                        intervalThread['kernelEvent'][evt] = dict(self.init_eventData)
                        intervalThread['totalKernelEvent'][evt] = dict(self.init_eventData)
                        try:
                            intervalThread['totalKernelEvent'][evt]['count'] = \
                                self.threadData[key]['kernelEvent'][evt]['count']

                            intervalThread['totalKernelEvent'][evt]['usage'] = \
                                self.threadData[key]['kernelEvent'][evt]['usage']
                        except:
                            pass

                # first interval #
                if SystemManager.intervalNow == SystemManager.intervalEnable:
                    intervalThread['cpuUsage'] = float(self.threadData[key]['usage'])
                    intervalThread['preempted'] = float(self.threadData[key]['cpuWait'])
                    intervalThread['coreSchedCnt'] = float(self.threadData[key]['coreSchedCnt'])
                    intervalThread['brUsage'] = int(self.threadData[key]['reqBlock'])
                    intervalThread['bwUsage'] = int(self.threadData[key]['writeBlock'])
                    intervalThread['memUsage'] = int(self.threadData[key]['nrPages'])
                    intervalThread['kmemUsage'] = int(self.threadData[key]['remainKmem'])

                # later intervals #
                else:
                    try:
                        self.intervalData[index - 1][key]
                    except:
                        self.intervalData[index - 1][key] = dict(self.init_intervalData)

                    # define thread alias in previous interval #
                    prevIntervalThread = self.intervalData[index - 1][key]

                    # calculate resource usage in this interval #
                    intervalThread['cpuUsage'] += \
                        intervalThread['totalUsage'] - prevIntervalThread['totalUsage']
                    intervalThread['preempted'] += \
                        intervalThread['totalPreempted'] - prevIntervalThread['totalPreempted']
                    intervalThread['coreSchedCnt'] = \
                        intervalThread['totalCoreSchedCnt'] - prevIntervalThread['totalCoreSchedCnt']
                    intervalThread['brUsage'] = \
                        intervalThread['totalBrUsage'] - prevIntervalThread['totalBrUsage']
                    intervalThread['bwUsage'] = \
                        intervalThread['totalBwUsage'] - prevIntervalThread['totalBwUsage']
                    intervalThread['memUsage'] = \
                        intervalThread['totalMemUsage'] - prevIntervalThread['totalMemUsage']
                    intervalThread['kmemUsage'] = \
                        intervalThread['totalKmemUsage'] - prevIntervalThread['totalKmemUsage']

                # calculate custom event usage in this interval #
                if 'totalCustomEvent' in intervalThread:
                    for evt in intervalThread['totalCustomEvent'].keys():
                        try:
                            intervalThread['customEvent'][evt]['count'] = \
                                intervalThread['totalCustomEvent'][evt]['count'] - \
                                    prevIntervalThread['totalCustomEvent'][evt]['count']
                        except:
                            intervalThread['customEvent'][evt]['count'] = \
                                intervalThread['totalCustomEvent'][evt]['count']

                        self.intervalData[index]['toTal']['customEvent'][evt]['count'] += \
                            intervalThread['customEvent'][evt]['count']

                # calculate user event usage in this interval #
                if 'totalUserEvent' in intervalThread:
                    for evt in intervalThread['totalUserEvent'].keys():
                        try:
                            intervalThread['userEvent'][evt]['count'] = \
                                intervalThread['totalUserEvent'][evt]['count'] - \
                                    prevIntervalThread['totalUserEvent'][evt]['count']

                            intervalThread['userEvent'][evt]['usage'] = \
                                intervalThread['totalUserEvent'][evt]['usage'] - \
                                    prevIntervalThread['totalUserEvent'][evt]['usage']
                        except:
                            intervalThread['userEvent'][evt]['count'] = \
                                intervalThread['totalUserEvent'][evt]['count']

                            intervalThread['userEvent'][evt]['usage'] = \
                                intervalThread['totalUserEvent'][evt]['usage']

                        self.intervalData[index]['toTal']['userEvent'][evt]['count'] += \
                            intervalThread['userEvent'][evt]['count']

                        self.intervalData[index]['toTal']['userEvent'][evt]['usage'] += \
                            intervalThread['userEvent'][evt]['usage']

                # calculate kernel event usage in this interval #
                if 'totalKernelEvent' in intervalThread:
                    for evt in intervalThread['totalKernelEvent'].keys():
                        try:
                            intervalThread['kernelEvent'][evt]['count'] = \
                                intervalThread['totalKernelEvent'][evt]['count'] - \
                                    prevIntervalThread['totalKernelEvent'][evt]['count']

                            intervalThread['kernelEvent'][evt]['usage'] = \
                                intervalThread['totalKernelEvent'][evt]['usage'] - \
                                    prevIntervalThread['totalKernelEvent'][evt]['usage']
                        except:
                            intervalThread['kernelEvent'][evt]['count'] = \
                                intervalThread['totalKernelEvent'][evt]['count']

                            intervalThread['kernelEvent'][evt]['usage'] = \
                                intervalThread['totalKernelEvent'][evt]['usage']

                        self.intervalData[index]['toTal']['kernelEvent'][evt]['count'] += \
                            intervalThread['kernelEvent'][evt]['count']

                        self.intervalData[index]['toTal']['kernelEvent'][evt]['usage'] += \
                            intervalThread['kernelEvent'][evt]['usage']

                # fix cpu usage exceed this interval #
                self.thisInterval = SystemManager.intervalEnable
                if intervalThread['cpuUsage'] > SystemManager.intervalEnable or self.finishTime != '0':
                    # first interval #
                    if index == 0:
                        self.thisInterval = float(time) - float(self.startTime)
                    # normal intervals #
                    elif float(self.intervalData[index - 1][key]['firstLogTime']) > 0:
                        self.thisInterval = \
                            float(time) - float(self.intervalData[index - 1][key]['firstLogTime'])
                    # long time running intervals #
                    else:
                        for idx in xrange(index - 1, -1, -1):
                            if float(self.intervalData[index - 1][key]['firstLogTime']) > 0:
                                self.thisInterval = \
                                    float(time) - float(self.intervalData[idx][key]['firstLogTime'])
                                break
                        if self.thisInterval != SystemManager.intervalEnable:
                            self.thisInterval = float(time) - float(self.startTime)

                    # recalculate previous intervals if no context switching since profile start #
                    remainTime = intervalThread['cpuUsage']
                    if intervalThread['cpuUsage'] > self.thisInterval:
                        for idx in xrange(\
                            int(intervalThread['cpuUsage'] / SystemManager.intervalEnable), -1, -1):
                            try:
                                self.intervalData[idx][key]
                            except:
                                if not idx in self.intervalData:
                                    continue
                                self.intervalData[idx][key] = dict(self.init_intervalData)
                            try:
                                self.intervalData[idx - 1][key]
                            except:
                                if not idx - 1 in self.intervalData:
                                    continue
                                self.intervalData[idx - 1][key] = dict(self.init_intervalData)
                            prevIntervalData = self.intervalData[idx - 1][key]

                            # make previous intervals of core there was no context switching #
                            longRunCore = self.threadData[key]['longRunCore']
                            if longRunCore >= 0:
                                longRunCoreId = '0[%s]' % longRunCore
                                try:
                                    self.intervalData[idx][longRunCoreId]
                                except:
                                    self.intervalData[idx][longRunCoreId] = \
                                        dict(self.init_intervalData)

                            if remainTime >= SystemManager.intervalEnable:
                                remainTime = \
                                    int(remainTime / SystemManager.intervalEnable) * \
                                    SystemManager.intervalEnable
                                prevIntervalData['cpuUsage'] = SystemManager.intervalEnable
                                prevIntervalData['cpuPer'] = 100
                            else:
                                if prevIntervalData['cpuUsage'] > remainTime:
                                    remainTime = prevIntervalData['cpuUsage']
                                else:
                                    prevIntervalData['cpuUsage'] = remainTime
                                prevIntervalData['cpuPer'] = \
                                    remainTime / SystemManager.intervalEnable * 100

                            remainTime -= SystemManager.intervalEnable

                # add remainter of cpu usage exceed interval in this interval to previous interval #
                if SystemManager.intervalNow - SystemManager.intervalEnable > 0 and \
                    self.thisInterval > SystemManager.intervalEnable:
                    diff = self.thisInterval - SystemManager.intervalEnable
                    if prevIntervalThread['cpuUsage'] + diff > SystemManager.intervalEnable:
                        diff = SystemManager.intervalEnable - prevIntervalThread['cpuUsage']

                    prevIntervalThread['cpuUsage'] += diff
                    prevIntervalThread['cpuPer'] = \
                        prevIntervalThread['cpuUsage'] / SystemManager.intervalEnable * 100

                # calculate percentage of cpu usage of this thread in this interval #
                if self.thisInterval > 0:
                    intervalThread['cpuPer'] = intervalThread['cpuUsage'] / self.thisInterval * 100
                else:
                    intervalThread['cpuPer'] = 0

                # revise thread interval usage in DVFS system #
                if intervalThread['cpuPer'] > 100:
                    intervalThread['cpuPer'] = 100
                elif intervalThread['cpuPer'] < 0:
                    intervalThread['cpuPer'] = 0

                # fix preempted time exceed this interval #
                if intervalThread['preempted'] > SystemManager.intervalEnable:
                    # recalculate previous intervals if no context switching since profile start #
                    remainTime = intervalThread['preempted']
                    if intervalThread['preempted'] > self.thisInterval:
                        for idx in xrange(index + 1, -1, -1):
                            try:
                                self.intervalData[idx][key]
                            except:
                                self.intervalData[idx][key] = dict(self.init_intervalData)
                            try:
                                self.intervalData[idx - 1][key]
                            except:
                                self.intervalData[idx - 1][key] = dict(self.init_intervalData)

                            if remainTime >= SystemManager.intervalEnable:
                                self.intervalData[idx - 1][key]['preempted'] = \
                                    SystemManager.intervalEnable
                            else:
                                self.intervalData[idx - 1][key]['preempted'] += remainTime

                            remainTime -= SystemManager.intervalEnable
                            if remainTime <= 0:
                                break

                # calculate total block usage in this interval #
                self.intervalData[index]['toTal']['totalBr'] += \
                    self.intervalData[index][key]['brUsage']
                self.intervalData[index]['toTal']['totalBw'] += \
                    self.intervalData[index][key]['bwUsage'] >> 1

                """
                calculate total memory usage in this interval \
                except for core(swapper) threads because its already calculated
                """
                if key[0:2] == '0[':
                    continue

                self.intervalData[index]['toTal']['totalMem'] += \
                    self.intervalData[index][key]['memUsage']
                self.intervalData[index]['toTal']['totalKmem'] += \
                    self.intervalData[index][key]['kmemUsage']



    def parse(self, string):
        SystemManager.curLine += 1

        if SystemManager.tgidEnable:
            m = re.match(r'^\s*(?P<comm>.+)-(?P<thread>[0-9]+)\s+\(\s*(?P<tgid>\S+)\)\s+' + \
                r'\[(?P<core>[0-9]+)\]\s+(?P<time>\S+):\s+(?P<func>\S+):(?P<etc>.+)', string)
        else:
            m = re.match(r'^\s*(?P<comm>.+)-(?P<thread>[0-9]+)\s+\[(?P<core>[0-9]+)\]\s+' + \
                r'(?P<time>\S+):\s+(?P<func>\S+):(?P<etc>.+)', string)
        if m is not None:
            d = m.groupdict()
            comm = d['comm']
            core = str(int(d['core']))
            func = d['func']
            etc = d['etc']
            time = d['time']

            SystemManager.logSize += len(string)

            self.lastCore = core
            self.lastEvent = func

            if SystemManager.maxCore < int(core):
                SystemManager.maxCore = int(core)

            # make core id #
            coreId = '0[%s]' % core
            if int(d['thread']) == 0:
                thread = coreId
                comm = comm.replace("<idle>", "swapper/" + core)
            else:
                thread = d['thread']

            # make core thread entity in advance for total irq per core #
            try:
                self.threadData[coreId]
            except:
                self.threadData[coreId] = dict(self.init_threadData)
                self.threadData[coreId]['comm'] = "swapper/" + core

            # make thread entity #
            try:
                self.threadData[thread]
            except:
                self.threadData[thread] = dict(self.init_threadData)
                self.threadData[thread]['comm'] = comm

            # set pid of thread #
            try:
                self.threadData[thread]['tgid'] = SystemManager.savedProcTree[thread]
            except:
                if SystemManager.tgidEnable:
                    self.threadData[thread]['tgid'] = d['tgid']

            # calculate usage of threads had been running longer than periodic interval #
            if SystemManager.intervalEnable > 0:
                for key, value in sorted(self.lastTidPerCore.items()):
                    try:
                        coreId = '0[%s]' % key
                        tid = self.lastTidPerCore[key]

                        # check cpu idle status #
                        if self.threadData[coreId]['lastStatus'] == 'R':
                            self.threadData[coreId]['usage'] += \
                                float(time) - self.threadData[coreId]['start']
                            self.threadData[coreId]['start'] = float(time)
                            continue

                        usage = float(time) - float(self.threadData[tid]['start'])
                        self.threadData[tid]['usage'] += usage
                        self.threadData[tid]['start'] = float(time)
                    except:
                        continue

            if self.startTime == '0':
                self.startTime = time
            else:
                # check whether this log is last one or not #
                if SystemManager.curLine >= SystemManager.totalLine:
                    self.finishTime = time

                # calculate usage of threads in interval #
                self.processIntervalData(time)

            if func == "sched_switch":
                m = re.match(\
                    r'^\s*prev_comm=(?P<prev_comm>.*)\s+prev_pid=(?P<prev_pid>[0-9]+)\s+' + \
                    r'prev_prio=(?P<prev_prio>\S+)\s+prev_state=(?P<prev_state>\S+)\s+==>\s+' + \
                    r'next_comm=(?P<next_comm>.*)\s+next_pid=(?P<next_pid>[0-9]+)\s+' + \
                    r'next_prio=(?P<next_prio>\S+)', etc)
                if m is not None:
                    d = m.groupdict()

                    SystemManager.cpuEnable = True

                    self.cxtSwitch += 1

                    prev_comm = d['prev_comm']
                    prev_pid = d['prev_pid']
                    prev_id = prev_pid

                    coreId = '0[%s]' % core

                    if int(d['prev_pid']) == 0:
                        prev_id = coreId
                    else:
                        prev_id = prev_pid

                    next_comm = d['next_comm']
                    next_pid = d['next_pid']

                    if int(d['next_pid']) == 0:
                        next_id = coreId
                    else:
                        next_id = next_pid

                    # check cpu wakeup #
                    if self.threadData[coreId]['lastOff'] > 0:
                        diff = float(time) - self.threadData[coreId]['lastOff']
                        self.threadData[coreId]['offTime'] += diff
                        self.threadData[coreId]['lastOff'] = 0

                    # make list #
                    try:
                        self.threadData[prev_id]
                    except:
                        self.threadData[prev_id] = dict(self.init_threadData)
                        self.threadData[prev_id]['comm'] = prev_comm
                    try:
                        self.threadData[next_id]
                    except:
                        self.threadData[next_id] = dict(self.init_threadData)
                        self.threadData[next_id]['comm'] = next_comm
                    try:
                        self.threadData[coreId]
                    except:
                        self.threadData[coreId] = dict(self.init_threadData)
                        self.threadData[coreId]['comm'] = 'swapper/' + core

                    if self.wakeupData['valid'] > 0 and self.wakeupData['tid'] == prev_id:
                        self.wakeupData['valid'] -= 1

                    # update anonymous comm #
                    if comm == '<...>':
                        comm = prev_comm
                    if self.threadData[prev_id]['comm'] == '<...>':
                        self.threadData[prev_id]['comm'] = prev_comm
                    if self.threadData[next_id]['comm'] == '<...>':
                        self.threadData[next_id]['comm'] = next_comm

                    # write current time #
                    self.threadData[prev_id]['stop'] = float(time)
                    self.threadData[next_id]['start'] = float(time)
                    self.threadData[next_id]['waitStartAsParent'] = float(0)

                    # update priority of thread to highest one #
                    if self.threadData[prev_id]['pri'] == '0' or \
                        int(self.threadData[prev_id]['pri']) > int(d['prev_prio']):
                        self.threadData[prev_id]['pri'] = d['prev_prio']
                    if self.threadData[next_id]['pri'] == '0' or \
                        int(self.threadData[next_id]['pri']) > int(d['next_prio']):
                        self.threadData[next_id]['pri'] = d['next_prio']

                    # calculate running time of previous thread #
                    diff = 0
                    if self.threadData[prev_id]['start'] == 0:
                        # calculate running time of previous thread started before starting to profile #
                        if self.threadData[coreId]['coreSchedCnt'] == 0:
                            diff = float(time) - float(self.startTime)
                            self.threadData[prev_id]['usage'] = diff
                        # it is possible that log was loss #
                        else:
                            pass
                    else:
                        diff = self.threadData[prev_id]['stop'] - self.threadData[prev_id]['start']
                        if diff >= 0:
                            self.threadData[prev_id]['usage'] += diff

                            if self.threadData[prev_id]['maxRuntime'] < diff:
                                self.threadData[prev_id]['maxRuntime'] = diff
                        else:
                            SystemManager.printWarning(\
                                "usage time of %s(%s) is negative at line %d" % \
                                (prev_comm, prev_id, SystemManager.curLine))

                    if diff > int(SystemManager.intervalEnable):
                        self.threadData[prev_id]['longRunCore'] = core

                    # update core info #
                    self.threadData[coreId]['coreSchedCnt'] += 1
                    self.lastTidPerCore[core] = next_id

                    # calculate preempted time of threads blocked #
                    if SystemManager.preemptGroup != None:
                        for value in SystemManager.preemptGroup:
                            index = SystemManager.preemptGroup.index(value)
                            if self.preemptData[index][0] and self.preemptData[index][3] == core:
                                try:
                                    self.preemptData[index][1][prev_id]
                                except:
                                    self.preemptData[index][1][prev_id] = dict(self.init_preemptData)

                                self.preemptData[index][1][prev_id]['usage'] +=  \
                                    self.threadData[prev_id]['stop'] - self.threadData[prev_id]['start']
                                self.preemptData[index][4] += \
                                    self.threadData[prev_id]['stop'] - self.threadData[prev_id]['start']

                    # set sched status #
                    if d['prev_state'][0] == 'R':
                        self.threadData[prev_id]['preempted'] += 1
                        self.threadData[next_id]['preemption'] += 1
                        self.threadData[prev_id]['lastStatus'] = 'P'

                        if SystemManager.preemptGroup != None:
                            # enable preempted bit #
                            try:
                                index = SystemManager.preemptGroup.index(prev_id)
                            except:
                                index = -1

                            if index >= 0:
                                self.preemptData[index][0] = True
                                try:
                                    self.preemptData[index][1][next_id]
                                except:
                                    self.preemptData[index][1][next_id] = dict(self.init_preemptData)

                                self.preemptData[index][2] = float(time)
                                self.preemptData[index][3] = core
                    elif d['prev_state'][0] == 'S':
                        self.threadData[prev_id]['yield'] += 1
                        self.threadData[prev_id]['stop'] = 0
                        self.threadData[prev_id]['lastStatus'] = 'S'
                    else:
                        self.threadData[prev_id]['stop'] = 0
                        self.threadData[prev_id]['lastStatus'] = d['prev_state'][0]

                    # calculate preempted time of next thread #
                    if self.threadData[next_id]['stop'] == 0:
                        # no stop time of next thread because of some reasons #
                        self.threadData[next_id]['stop'] = 0
                    elif self.threadData[next_id]['lastStatus'] == 'P':
                        preemptedTime = \
                            self.threadData[next_id]['start'] - self.threadData[next_id]['stop']
                        if preemptedTime >=0:
                            self.threadData[next_id]['cpuWait'] += preemptedTime
                        else:
                            SystemManager.printWarning(\
                                "preempted time of %s(%d) is negative at line %d" % \
                                (next_comm, next_id, SystemManager.curLine))

                        if preemptedTime > self.threadData[next_id]['maxPreempted']:
                            self.threadData[next_id]['maxPreempted'] = preemptedTime

                        try:
                            self.preemptData[SystemManager.preemptGroup.index(next_id)][0] = False
                        except:
                            pass

                    # set sched status of next thread #
                    self.threadData[next_id]['lastStatus'] = 'R'
                else:
                    SystemManager.printWarning(\
                        "Fail to recognize '%s' event at line %d" % (func, SystemManager.curLine))

            elif func == "irq_handler_entry":
                m = re.match(r'^\s*irq=(?P<irq>[0-9]+)\s+name=(?P<name>\S+)', etc)
                if m is not None:
                    d = m.groupdict()

                    irqId = 'irq/%s' % (d['irq'])

                    # make irq list #
                    try:
                        self.irqData[irqId]
                    except:
                        self.irqData[irqId] = dict(self.init_irqData)
                        self.irqData[irqId]['name'] = {}
                        self.irqData[irqId]['name'][d['name']] = 0
                    try:
                        self.irqData[irqId]['name'][d['name']]
                    except:
                        self.irqData[irqId]['name'][d['name']] = 0

                    # make per-thread irq list #
                    try:
                        self.threadData[thread]['irqList'][irqId]
                    except:
                        self.threadData[thread]['irqList'] = {}
                    try:
                        self.threadData[thread]['irqList'][irqId]
                    except:
                        self.threadData[thread]['irqList'][irqId] = dict(self.init_irqData)
                        self.threadData[thread]['irqList'][irqId]['name'] = d['name']

                    # save irq period per thread #
                    if self.threadData[thread]['irqList'][irqId]['start'] > 0:
                        diff = float(time) - self.threadData[thread]['irqList'][irqId]['start']
                        if diff > self.threadData[thread]['irqList'][irqId]['maxPeriod'] or \
                            self.threadData[thread]['irqList'][irqId]['maxPeriod'] <= 0:
                            self.threadData[thread]['irqList'][irqId]['maxPeriod'] = diff
                        if diff < self.threadData[thread]['irqList'][irqId]['minPeriod'] or \
                            self.threadData[thread]['irqList'][irqId]['minPeriod'] <= 0:
                            self.threadData[thread]['irqList'][irqId]['minPeriod'] = diff

                    # save irq period #
                    if self.irqData[irqId]['start'] > 0:
                        diff = float(time) - self.irqData[irqId]['start']
                        if diff > self.irqData[irqId]['maxPeriod'] or \
                            self.irqData[irqId]['maxPeriod'] <= 0:
                            self.irqData[irqId]['maxPeriod'] = diff
                        if diff < self.irqData[irqId]['minPeriod'] or \
                            self.irqData[irqId]['minPeriod'] <= 0:
                            self.irqData[irqId]['minPeriod'] = diff

                    self.irqData[irqId]['start'] = float(time)
                    self.irqData[irqId]['count'] += 1
                    self.threadData[thread]['irqList'][irqId]['start'] = float(time)
                    self.threadData[thread]['irqList'][irqId]['count'] += 1

            elif func == "irq_handler_exit":
                m = re.match(r'^\s*irq=(?P<irq>[0-9]+)\s+ret=(?P<return>\S+)', etc)
                if m is not None:
                    d = m.groupdict()

                    irqId = 'irq/%s' % (d['irq'])

                    # make list #
                    try:
                        self.irqData[irqId]
                    except:
                        self.irqData[irqId] = dict(self.init_irqData)

                    # make per-thread irq list #
                    try:
                        self.threadData[thread]['irqList'][irqId]
                    except:
                        self.threadData[thread]['irqList'] = {}
                    try:
                        self.threadData[thread]['irqList'][irqId]
                    except:
                        self.threadData[thread]['irqList'][irqId] = dict(self.init_irqData)
                        self.threadData[thread]['irqList'][irqId]['name'] = d['action']

                    if self.threadData[thread]['irqList'][irqId]['start'] > 0:
                        # save softirq usage #
                        diff = float(time) - self.threadData[thread]['irqList'][irqId]['start']
                        self.threadData[thread]['irqList'][irqId]['usage'] += diff
                        self.threadData[thread]['irq'] += diff
                        self.irqData[irqId]['usage'] += diff

                        # save softirq period per thread #
                        if diff > self.threadData[thread]['irqList'][irqId]['max'] or \
                            self.threadData[thread]['irqList'][irqId]['max'] <= 0:
                            self.threadData[thread]['irqList'][irqId]['max'] = diff
                        if diff < self.threadData[thread]['irqList'][irqId]['min'] or \
                            self.threadData[thread]['irqList'][irqId]['min'] <= 0:
                            self.threadData[thread]['irqList'][irqId]['min'] = diff

                    if self.irqData[irqId]['start'] > 0:
                        diff = float(time) - self.irqData[irqId]['start']
                        # save softirq period #
                        if diff > self.irqData[irqId]['max'] or self.irqData[irqId]['max'] <= 0:
                            self.irqData[irqId]['max'] = diff
                        if diff < self.irqData[irqId]['min'] or self.irqData[irqId]['min'] <= 0:
                            self.irqData[irqId]['min'] = diff
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "softirq_entry":
                m = re.match(r'^\s*vec=(?P<vector>[0-9]+)\s+\[action=(?P<action>\S+)\]', etc)
                if m is not None:
                    d = m.groupdict()

                    irqId = 'softirq/%s' % (d['vector'])

                    # make irq list #
                    try:
                        self.irqData[irqId]
                    except:
                        self.irqData[irqId] = dict(self.init_irqData)
                        self.irqData[irqId]['name'] = {}
                        self.irqData[irqId]['name'][d['action']] = 0
                    try:
                        self.irqData[irqId]['name'][d['action']]
                    except:
                        self.irqData[irqId]['name'][d['action']] = 0

                    # make per-thread irq list #
                    try:
                        self.threadData[thread]['irqList'][irqId]
                    except:
                        self.threadData[thread]['irqList'] = {}
                    try:
                        self.threadData[thread]['irqList'][irqId]
                    except:
                        self.threadData[thread]['irqList'][irqId] = dict(self.init_irqData)
                        self.threadData[thread]['irqList'][irqId]['name'] = d['action']

                    # save softirq period per thread #
                    if self.threadData[thread]['irqList'][irqId]['start'] > 0:
                        diff = float(time) - self.threadData[thread]['irqList'][irqId]['start']
                        if diff > self.threadData[thread]['irqList'][irqId]['maxPeriod'] or \
                            self.threadData[thread]['irqList'][irqId]['maxPeriod'] <= 0:
                            self.threadData[thread]['irqList'][irqId]['maxPeriod'] = diff
                        if diff < self.threadData[thread]['irqList'][irqId]['minPeriod'] or \
                            self.threadData[thread]['irqList'][irqId]['minPeriod'] <= 0:
                            self.threadData[thread]['irqList'][irqId]['minPeriod'] = diff

                    # save softirq period #
                    if self.irqData[irqId]['start'] > 0:
                        diff = float(time) - self.irqData[irqId]['start']
                        if diff > self.irqData[irqId]['maxPeriod'] or \
                            self.irqData[irqId]['maxPeriod'] <= 0:
                            self.irqData[irqId]['maxPeriod'] = diff
                        if diff < self.irqData[irqId]['minPeriod'] or \
                            self.irqData[irqId]['minPeriod'] <= 0:
                            self.irqData[irqId]['minPeriod'] = diff

                    self.irqData[irqId]['start'] = float(time)
                    self.irqData[irqId]['count'] += 1
                    self.threadData[thread]['irqList'][irqId]['start'] = float(time)
                    self.threadData[thread]['irqList'][irqId]['count'] += 1
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "softirq_exit":
                m = re.match(r'^\s*vec=(?P<vector>[0-9]+)\s+\[action=(?P<action>\S+)\]', etc)
                if m is not None:
                    d = m.groupdict()

                    irqId = 'softirq/%s' % (d['vector'])

                    # make list #
                    try:
                        self.irqData[irqId]
                    except:
                        self.irqData[irqId] = dict(self.init_irqData)
                        self.irqData[irqId]['name'] = {}
                        self.irqData[irqId]['name'][d['action']] = 0
                    try:
                        self.irqData[irqId]['name'][d['action']]
                    except:
                        self.irqData[irqId]['name'][d['action']] = 0

                    # make per-thread irq list #
                    try:
                        self.threadData[thread]['irqList'][irqId]
                    except:
                        self.threadData[thread]['irqList'] = {}
                    try:
                        self.threadData[thread]['irqList'][irqId]
                    except:
                        self.threadData[thread]['irqList'][irqId] = dict(self.init_irqData)
                        self.threadData[thread]['irqList'][irqId]['name'] = d['action']

                    if self.threadData[thread]['irqList'][irqId]['start'] > 0:
                        # save softirq usage #
                        diff = float(time) - self.threadData[thread]['irqList'][irqId]['start']
                        self.threadData[thread]['irqList'][irqId]['usage'] += diff
                        self.threadData[thread]['irq'] += diff
                        self.irqData[irqId]['usage'] += diff

                        # save softirq period per thread #
                        if diff > self.threadData[thread]['irqList'][irqId]['max'] or \
                            self.threadData[thread]['irqList'][irqId]['max'] <= 0:
                            self.threadData[thread]['irqList'][irqId]['max'] = diff
                        if diff < self.threadData[thread]['irqList'][irqId]['min'] or \
                            self.threadData[thread]['irqList'][irqId]['min'] <= 0:
                            self.threadData[thread]['irqList'][irqId]['min'] = diff

                    if self.irqData[irqId]['start'] > 0:
                        diff = float(time) - self.irqData[irqId]['start']
                        # save softirq period #
                        if diff > self.irqData[irqId]['max'] or self.irqData[irqId]['max'] <= 0:
                            self.irqData[irqId]['max'] = diff
                        if diff < self.irqData[irqId]['min'] or self.irqData[irqId]['min'] <= 0:
                            self.irqData[irqId]['min'] = diff
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "sched_migrate_task":
                m = re.match(\
                    r'^\s*comm=(?P<comm>.*)\s+pid=(?P<pid>[0-9]+)\s+prio=(?P<prio>[0-9]+)\s+' + \
                    r'orig_cpu=(?P<orig_cpu>[0-9]+)\s+dest_cpu=(?P<dest_cpu>[0-9]+)', etc)
                if m is not None:
                    d = m.groupdict()

                    pid = d['pid']

                    try:
                        self.threadData[pid]
                    except:
                        self.threadData[pid] = dict(self.init_threadData)
                        self.threadData[pid]['comm'] = d['comm']

                    self.threadData[pid]['migrate'] += 1

                    # update core data for preempted info #
                    if SystemManager.preemptGroup != None:
                        try:
                            index = SystemManager.preemptGroup.index(thread)
                        except:
                            index = -1

                        if index >= 0:
                            self.preemptData[index][3] = core
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "mm_page_alloc":
                m = re.match(\
                    r'^\s*page=\s*(?P<page>\S+)\s+pfn=(?P<pfn>[0-9]+)\s+order=(?P<order>[0-9]+)\s+' + \
                    r'migratetype=(?P<mt>[0-9]+)\s+gfp_flags=(?P<flags>\S+)', etc)
                if m is not None:
                    d = m.groupdict()

                    SystemManager.memEnable = True

                    # check whether it is huge page #
                    if d['page'] == '(null)':
                        page = 'huge'
                    else:
                        page = d['page']

                    pfn = int(d['pfn'])
                    flags = d['flags']
                    order = int(d['order'])

                    self.threadData[thread]['nrPages'] += pow(2, order)
                    self.threadData[coreId]['nrPages'] += pow(2, order)

                    if flags.find('NOFS') >= 0 or \
                        flags.find('GFP_WRITE') >= 0 or \
                        flags.find('0x1000000') >= 0:

                        pageType = 'CACHE'
                        self.threadData[thread]['cachePages'] += pow(2, order)
                        self.threadData[coreId]['cachePages'] += pow(2, order)
                    elif flags.find('USER') >= 0:
                        pageType = 'USER'
                        self.threadData[thread]['userPages'] += pow(2, order)
                        self.threadData[coreId]['userPages'] += pow(2, order)
                    else:
                        pageType = 'KERNEL'
                        self.threadData[thread]['kernelPages'] += pow(2, order)
                        self.threadData[coreId]['kernelPages'] += pow(2, order)

                    # make PTE in page table #
                    for cnt in xrange(0, pow(2, order)):
                        pfnv = pfn + cnt

                        try:
                            # this allocated page is not freed #
                            if self.pageTable[pfnv] == {}:
                                raise
                            else:
                                self.threadData[thread]['nrPages'] -= 1
                                self.threadData[coreId]['nrPages'] -= 1
                        except:
                            self.pageTable[pfnv] = dict(self.init_pageData)

                        self.pageTable[pfnv]['tid'] = thread
                        self.pageTable[pfnv]['page'] = page
                        self.pageTable[pfnv]['flags'] = flags
                        self.pageTable[pfnv]['type'] = pageType
                        self.pageTable[pfnv]['time'] = time
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "mm_page_free":
                m = re.match(\
                    r'^\s*page=(?P<page>\S+)\s+pfn=(?P<pfn>[0-9]+)\s+order=(?P<order>[0-9]+)', etc)
                if m is not None:
                    d = m.groupdict()

                    SystemManager.memEnable = True

                    page = d['page']
                    pfn = int(d['pfn'])
                    order = int(d['order'])

                    for cnt in xrange(0, pow(2, order)):
                        pfnv = pfn + cnt

                        try:
                            self.threadData[self.pageTable[pfnv]['tid']]['nrPages'] -= 1
                            self.threadData[coreId]['nrPages'] -= 1

                            if thread != self.pageTable[pfnv]['tid']:
                                self.threadData[self.pageTable[pfnv]['tid']]['reclaimedPages'] += 1
                                self.threadData[coreId]['reclaimedPages'] += 1

                            if self.pageTable[pfnv]['type'] is 'CACHE':
                                self.threadData[self.pageTable[pfnv]['tid']]['cachePages'] -= 1
                                self.threadData[coreId]['cachePages'] -= 1
                            elif self.pageTable[pfnv]['type'] is 'USER':
                                self.threadData[self.pageTable[pfnv]['tid']]['userPages'] -= 1
                                self.threadData[coreId]['userPages'] -= 1
                            elif self.pageTable[pfnv]['type'] is 'KERNEL':
                                self.threadData[self.pageTable[pfnv]['tid']]['kernelPages'] -= 1
                                self.threadData[coreId]['kernelPages'] -= 1

                            del self.pageTable[pfnv]
                            self.pageTable[pfnv] = {}
                        except:
                            # this page is allocated before starting profile #
                            self.threadData[thread]['anonReclaimedPages'] += 1
                            self.threadData[coreId]['anonReclaimedPages'] += 1
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "mm_filemap_delete_from_page_cache":
                m = re.match(r'^\s*dev (?P<major>[0-9]+):(?P<minor>[0-9]+) .+' + \
                    r'page=(?P<page>\S+)\s+pfn=(?P<pfn>[0-9]+)', etc)
                if m is not None:
                    d = m.groupdict()

                    SystemManager.memEnable = True

                    pfn = int(d['pfn'])

                    try:
                        # attribute of page is changed to file #
                        if self.pageTable[pfn]['type'] is 'USER':
                            self.threadData[self.pageTable[pfn]['tid']]['userPages'] -= 1
                            self.threadData[coreId]['userPages'] -= 1
                            self.threadData[self.pageTable[pfn]['tid']]['cachePages'] += 1
                            self.threadData[coreId]['cachePages'] += 1
                        elif self.pageTable[pfn]['type'] is 'KERNEL':
                            self.threadData[self.pageTable[pfn]['tid']]['kernelPages'] -= 1
                            self.threadData[coreId]['kernelPages'] -= 1
                            self.threadData[self.pageTable[pfn]['tid']]['cachePages'] += 1
                            self.threadData[coreId]['cachePages'] += 1

                        self.pageTable[pfn]['type'] = 'CACHE'
                    except:
                        return
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "kmalloc":
                m = re.match(\
                    r'^\s*call_site=(?P<caller>\S+)\s+ptr=(?P<ptr>\S+)\s+bytes_req=(?P<req>[0-9]+)\s+' + \
                    r'bytes_alloc=(?P<alloc>[0-9]+)\s+gfp_flags=(?P<flags>\S+)', etc)
                if m is not None:
                    d = m.groupdict()

                    SystemManager.memEnable = True

                    caller = d['caller']
                    ptr = d['ptr']
                    req = int(d['req'])
                    alloc = int(d['alloc'])

                    try:
                        self.kmemTable[ptr]
                        # some allocated object is not freed #
                    except:
                        self.kmemTable[ptr] = dict(self.init_kmallocData)

                    self.kmemTable[ptr]['tid'] = thread
                    self.kmemTable[ptr]['caller'] = caller
                    self.kmemTable[ptr]['req'] = req
                    self.kmemTable[ptr]['alloc'] = alloc
                    self.kmemTable[ptr]['waste'] = alloc - req
                    self.kmemTable[ptr]['core'] = coreId

                    self.threadData[thread]['remainKmem'] += alloc
                    self.threadData[thread]['wasteKmem'] += alloc - req
                    self.threadData[coreId]['remainKmem'] += alloc
                    self.threadData[coreId]['wasteKmem'] += alloc - req
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "kfree":
                m = re.match(r'^\s*call_site=(?P<caller>\S+)\s+ptr=\s*(?P<ptr>\S+)', etc)
                if m is not None:
                    d = m.groupdict()

                    SystemManager.memEnable = True

                    caller = d['caller']
                    ptr = d['ptr']

                    try:
                        self.threadData[self.kmemTable[ptr]['tid']]['remainKmem'] -= \
                            self.kmemTable[ptr]['alloc']
                        self.threadData[self.kmemTable[ptr]['core']]['remainKmem'] -= \
                            self.kmemTable[ptr]['alloc']
                        self.threadData[self.kmemTable[ptr]['tid']]['wasteKmem'] -= \
                            self.kmemTable[ptr]['waste']
                        self.threadData[self.kmemTable[ptr]['core']]['wasteKmem'] -= \
                            self.kmemTable[ptr]['waste']

                        self.kmemTable[ptr] = {}
                        del self.kmemTable[ptr]
                    except:
                        '''
                        this allocated object is not logged or \
                        this object is allocated before starting profile
                        '''
                        return
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "sched_wakeup":
                m = re.match(r'^\s*comm=(?P<comm>.*)\s+pid=(?P<pid>[0-9]+)\s+prio=(?P<prio>[0-9]+)\s+' + \
                    r'target_cpu=(?P<target>[0-9]+)', etc)
                if m is not None:
                    d = m.groupdict()

                    target_comm = d['comm']
                    pid = d['pid']

                    if self.wakeupData['tid'] == '0':
                        self.wakeupData['time'] = float(time) - float(self.startTime)
                    elif thread[0] == '0' or pid == '0':
                        return
                    elif self.wakeupData['valid'] > 0 \
                        and (self.wakeupData['from'] != self.wakeupData['tid'] or self.wakeupData['to'] != pid):
                        if self.wakeupData['valid'] == 1 and self.wakeupData['corrupt'] == '0':
                            try:
                                kicker = self.threadData[self.wakeupData['tid']]['comm']
                            except:
                                kicker = "NULL"

                            kicker_pid = self.wakeupData['tid']
                        else:
                            kicker = self.threadData[thread]['comm']
                            kicker_pid = thread

                        ntime = round(float(time) - float(self.startTime), 7)
                        self.depData.append("\t%.3f/%.3f \t%16s(%4s) -> %16s(%4s) \t%s" % \
                            (ntime, round(ntime - float(self.wakeupData['time']), 7), \
                            kicker, kicker_pid, target_comm, pid, "kick"))

                        self.wakeupData['time'] = float(time) - float(self.startTime)
                        self.wakeupData['from'] = self.wakeupData['tid']
                        self.wakeupData['to'] = pid
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "sys_enter":
                m = re.match(r'^\s*NR (?P<nr>[0-9]+) (?P<args>.+)', etc)
                if m is not None:
                    d = m.groupdict()

                    nr = d['nr']
                    args = d['args']

                    if nr == str(ConfigManager.sysList.index("sys_futex")):
                        n = re.match(\
                            r'^\s*(?P<uaddr>\S+), (?P<op>[0-9]+), (?P<val>\S+), (?P<timep>\S+),', d['args'])
                        if n is not None:
                            l = n.groupdict()

                            op = int(l['op']) % 10
                            if op == 0:
                                self.threadData[thread]['futexEnter'] = float(time)

                    if self.wakeupData['tid'] == '0':
                        self.wakeupData['time'] = float(time) - float(self.startTime)

                    if nr == str(ConfigManager.sysList.index("sys_write")):
                        self.wakeupData['tid'] = thread
                        self.wakeupData['nr'] = nr
                        self.wakeupData['args'] = args

                        if (self.wakeupData['valid'] > 0 and \
                            (self.wakeupData['tid'] == thread and \
                            self.wakeupData['from'] == comm)) is False:
                            self.wakeupData['valid'] += 1

                            if self.wakeupData['valid'] > 1:
                                self.wakeupData['corrupt'] = '1'
                            else:
                                self.wakeupData['corrupt'] = '0'

                    try:
                        self.threadData[thread]['syscallInfo']
                    except:
                        self.threadData[thread]['syscallInfo'] = {}
                    try:
                        self.threadData[thread]['syscallInfo'][nr]
                    except:
                        self.threadData[thread]['syscallInfo'][nr] = dict(self.init_syscallInfo)

                    self.threadData[thread]['syscallInfo'][nr]['last'] = float(time)

                    if len(SystemManager.syscallList) > 0:
                        try:
                            idx = SystemManager.syscallList.index(nr)
                        except:
                            idx = -1

                        if idx >= 0:
                            self.syscallData.append(['enter', time, thread, core, nr, args])
                    else:
                        self.syscallData.append(['enter', time, thread, core, nr, args])
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "sys_exit":
                m = re.match(r'^\s*NR (?P<nr>[0-9]+) = (?P<ret>.+)', etc)
                if m is not None:
                    d = m.groupdict()

                    nr = d['nr']
                    ret = d['ret']

                    if nr == str(ConfigManager.sysList.index("sys_futex")) and \
                        self.threadData[thread]['futexEnter'] > 0:
                        self.threadData[thread]['futexCnt'] += 1
                        futexTime = float(time) - self.threadData[thread]['futexEnter']
                        if futexTime > self.threadData[thread]['futexMax']:
                            self.threadData[thread]['futexMax'] = futexTime
                        self.threadData[thread]['futexTotal'] += futexTime
                        self.threadData[thread]['futexEnter'] = 0

                    try:
                        if SystemManager.depEnable is False:
                            raise
                        elif nr == str(ConfigManager.sysList.index("sys_write")) and \
                            self.wakeupData['valid'] > 0:
                            self.wakeupData['valid'] -= 1
                        elif nr == str(ConfigManager.sysList.index("sys_select")) or \
                            nr == str(ConfigManager.sysList.index("sys_poll")) or \
                            nr == str(ConfigManager.sysList.index("sys_epoll_wait")):
                            if (self.lastJob[core]['job'] == "sched_switch" or \
                                self.lastJob[core]['job'] == "sched_wakeup") and \
                                self.lastJob[core]['prevWakeupTid'] != thread:
                                ttime = float(time) - float(self.startTime)
                                itime = ttime - float(self.wakeupData['time'])
                                self.depData.append("\t%.3f/%.3f \t%16s %4s     %16s(%4s) \t%s" % \
                                    (round(ttime, 7), round(itime, 7), " ", " ", \
                                    self.threadData[thread]['comm'], thread, "wakeup"))

                                self.wakeupData['time'] = float(time) - float(self.startTime)
                                self.lastJob[core]['prevWakeupTid'] = thread
                        elif nr == str(ConfigManager.sysList.index("sys_recv")):
                            if self.lastJob[core]['prevWakeupTid'] != thread:
                                ttime = float(time) - float(self.startTime)
                                itime = ttime - float(self.wakeupData['time'])
                                self.depData.append("\t%.3f/%.3f \t%16s %4s     %16s(%4s) \t%s" % \
                                    (round(ttime, 7), round(itime, 7), " ", " ", \
                                    self.threadData[thread]['comm'], thread, "recv"))

                                self.wakeupData['time'] = float(time) - float(self.startTime)
                                self.lastJob[core]['prevWakeupTid'] = thread
                    except:
                        pass

                    try:
                        self.threadData[thread]['syscallInfo']
                    except:
                        self.threadData[thread]['syscallInfo'] = {}
                    try:
                        self.threadData[thread]['syscallInfo'][nr]
                    except:
                        self.threadData[thread]['syscallInfo'][nr] = dict(self.init_syscallInfo)

                    if self.threadData[thread]['syscallInfo'][nr]['last'] > 0:
                        diff = float(time) - self.threadData[thread]['syscallInfo'][nr]['last']
                        self.threadData[thread]['syscallInfo'][nr]['usage'] += diff
                        self.threadData[thread]['syscallInfo'][nr]['last'] = 0
                        self.threadData[thread]['syscallInfo'][nr]['count'] += 1

                        if self.threadData[thread]['syscallInfo'][nr]['max'] == 0 or \
                            self.threadData[thread]['syscallInfo'][nr]['max'] < diff:
                            self.threadData[thread]['syscallInfo'][nr]['max'] = diff
                        if self.threadData[thread]['syscallInfo'][nr]['min'] <= 0 or \
                            self.threadData[thread]['syscallInfo'][nr]['min'] > diff:
                            self.threadData[thread]['syscallInfo'][nr]['min'] = diff

                    if len(SystemManager.syscallList) > 0:
                        try:
                            idx = SystemManager.syscallList.index(nr)
                        except:
                            idx = -1

                        if idx >= 0:
                            self.syscallData.append(['exit', time, thread, core, nr, ret])
                    else:
                        self.syscallData.append(['exit', time, thread, core, nr, ret])
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "signal_generate":
                m = re.match(r'^\s*sig=(?P<sig>[0-9]+) errno=(?P<err>[0-9]+) ' + \
                        r'code=(?P<code>.*) comm=(?P<comm>.*) pid=(?P<pid>[0-9]+)', etc)
                if m is not None:
                    d = m.groupdict()

                    sig = d['sig']
                    target_comm = d['comm']
                    pid = d['pid']

                    self.depData.append("\t%.3f/%.3f \t%16s(%4s) -> %16s(%4s) \t%s(%s)" % \
                        (round(float(time) - float(self.startTime), 7), \
                        round(float(time) - float(self.startTime) - float(self.wakeupData['time']), 7), \
                        self.threadData[thread]['comm'], thread, target_comm, pid, "sigsend", sig))

                    self.sigData.append(('SEND', float(time) - float(self.startTime), \
                        self.threadData[thread]['comm'], thread, target_comm, pid, sig))

                    self.wakeupData['time'] = float(time) - float(self.startTime)

                    try:
                        # SIGCHLD #
                        if sig == str(ConfigManager.sigList.index('SIGCHLD')):
                            if self.threadData[pid]['waitStartAsParent'] > 0:
                                if self.threadData[pid]['waitPid'] == 0 or \
                                    self.threadData[pid]['waitPid'] == int(thread):
                                    diff = float(time) - self.threadData[pid]['waitStartAsParent']
                                    self.threadData[thread]['waitParent'] = diff
                                    self.threadData[pid]['waitChild'] += diff
                        elif sig == str(ConfigManager.sigList.index('SIGSEGV')):
                            self.threadData[pid]['die'] = 'F'
                    except:
                        return
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "signal_deliver":
                m = re.match(r'^\s*sig=(?P<sig>[0-9]+) errno=(?P<err>[0-9]+) code=(?P<code>.*) ' + \
                        r'sa_handler=(?P<handler>.*) sa_flags=(?P<flags>.*)', etc)
                if m is not None:
                    d = m.groupdict()

                    sig = d['sig']
                    flags = d['flags']

                    ttime = float(time) - float(self.startTime)
                    itime = float(time) - float(self.startTime) - float(self.wakeupData['time'])
                    self.depData.append("\t%.3f/%.3f \t%16s %4s     %16s(%4s) \t%s(%s)" % \
                        (round(ttime, 7), round(itime, 7), "", "", \
                        self.threadData[thread]['comm'], thread, "sigrecv", sig))

                    self.sigData.append(('RECV', float(time) - float(self.startTime), \
                        None, None, self.threadData[thread]['comm'], thread, sig))

                    self.wakeupData['time'] = float(time) - float(self.startTime)
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "block_bio_remap":
                m = re.match(r'^\s*(?P<major>[0-9]+),(?P<minor>[0-9]+)\s*(?P<operation>\S+)\s*' + \
                    r'(?P<address>\S+)\s+\+\s+(?P<size>[0-9]+)(?P<part>.+)', etc)
                if m is not None:
                    d = m.groupdict()

                    if d['operation'][0] == 'R':

                        SystemManager.blockEnable = True

                        bio = '%s/%s/%s/%s' % \
                            (d['major'], d['minor'], d['operation'][0], d['address'])

                        self.ioData[bio] = {'thread': thread, 'time': float(time), \
                            'major': d['major'], 'minor': d['minor'], \
                            'address': int(d['address']), 'size': int(d['size'])}

                        self.threadData[thread]['reqBlock'] += int(d['size'])
                        self.threadData[thread]['readQueueCnt'] += 1
                        self.threadData[thread]['readBlockCnt'] += 1
                        self.threadData[thread]['blkCore'] = coreId
                        self.threadData[coreId]['readBlockCnt'] += 1

                        try:
                            partInfo = d['part'].split()
                            partSet = partInfo[1].split(',')
                            major = partSet[0][1:]
                            minor = partSet[1][:-1]
                            addr = partInfo[2]

                            self.savePartOpt(thread, comm, 'R', major, minor, addr, \
                                SystemManager.blockSize * int(d['size']))
                        except:
                            SystemManager.printWarning("Fail to save partition info")

                        if self.threadData[thread]['readStart'] == 0:
                            self.threadData[thread]['readStart'] = float(time)
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "block_rq_complete":
                m = re.match(r'^\s*(?P<major>[0-9]+),(?P<minor>[0-9]+)\s*(?P<operation>\S+)' + \
                    r'\s*\(.*\)\s*(?P<address>\S+)\s+\+\s+(?P<size>[0-9]+)', etc)
                if m is not None:
                    d = m.groupdict()

                    address = d['address']
                    size = d['size']

                    bio = '%s/%s/%s/%s' % \
                        (d['major'], d['minor'], d['operation'][0], d['address'])

                    try:
                        self.threadData[self.ioData[bio]['thread']]
                        bioStart = int(address)
                        bioEnd = int(address) + int(size)
                    except:
                        return

                    for key, value in sorted(\
                        self.ioData.items(), key=lambda e: e[1]['address'], reverse=False):

                        if value['major'] == d['major'] and value['minor'] == d['minor']:
                            if bioStart <= value['address'] < bioEnd or \
                                bioStart < value['address'] + value['size'] <= bioEnd:

                                matchBlock = 0

                                if bioStart < value['address']:
                                    matchStart = value['address']
                                else:
                                    matchStart = bioStart

                                if bioEnd > value['address'] + value['size']:
                                    matchEnd = value['address'] + value['size']
                                else:
                                    matchEnd = bioEnd

                                if matchStart == value['address']:
                                    matchBlock = matchEnd - value['address']
                                    value['size'] = value['address'] + value['size'] - matchEnd
                                    value['address'] = matchEnd
                                elif matchStart > value['address']:
                                    if matchEnd == value['address'] + value['size']:
                                        matchBlock = matchEnd - matchStart
                                        value['size'] = matchStart - value['address']
                                    else:
                                        del value
                                        continue
                                else:
                                    del value
                                    continue

                                # just ignore error ;( #
                                if bioEnd < value['address'] + value['size']:
                                    pass

                                self.threadData[value['thread']]['readBlock'] += matchBlock
                                self.threadData[coreId]['readBlock'] += matchBlock

                                if value['size'] == 0:
                                    if self.threadData[value['thread']]['readQueueCnt'] > 0:
                                        self.threadData[value['thread']]['readQueueCnt'] -= 1

                                    """
                                    if error of size and time of block read is big then \
                                    consider inserting bellow condition
                                    # self.threadData[value['thread']]['readQueueCnt'] == 0 #
                                    """
                                    if self.threadData[value['thread']]['readStart'] > 0:
                                        waitTime = \
                                            float(time) - self.threadData[value['thread']]['readStart']
                                        self.threadData[coreId]['ioWait'] += waitTime
                                        self.threadData[value['thread']]['ioWait'] += waitTime
                                        self.threadData[value['thread']]['readStart'] = 0

                                    del value
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "writeback_dirty_page":
                m = re.match(r'^\s*bdi\s+(?P<major>[0-9]+):(?P<minor>[0-9]+):\s*' + \
                    r'ino=(?P<ino>\S+)\s+index=(?P<index>\S+)', etc)
                if m is not None:
                    d = m.groupdict()

                    SystemManager.blockEnable = True

                    self.threadData[thread]['writeBlock'] += 1
                    self.threadData[thread]['writeBlockCnt'] += 1
                    self.threadData[coreId]['writeBlock'] += 1
                    self.threadData[coreId]['writeBlockCnt'] += 1

                    self.savePartOpt(\
                        thread, comm, 'W', d['major'], d['minor'], None, SystemManager.pageSize)
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "wbc_writepage":
                m = re.match(r'^\s*bdi\s+(?P<major>[0-9]+):(?P<minor>[0-9]+):\s*' + \
                    r'towrt=(?P<towrt>\S+)\s+skip=(?P<skip>\S+)', etc)
                if m is not None:
                    d = m.groupdict()

                    if d['skip'] == '0':
                        SystemManager.blockEnable = True

                        self.threadData[thread]['writeBlock'] += 1
                        self.threadData[thread]['writeBlockCnt'] += 1
                        self.threadData[coreId]['writeBlock'] += 1
                        self.threadData[coreId]['writeBlockCnt'] += 1

                        self.savePartOpt(\
                            thread, comm, 'W', d['major'], d['minor'], None, SystemManager.pageSize)
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "mm_vmscan_wakeup_kswapd":
                try:
                    self.reclaimData[thread]
                except:
                    self.reclaimData[thread] = {'start': float(0)}

                if self.reclaimData[thread]['start'] <= 0:
                    self.reclaimData[thread]['start'] = float(time)

                self.threadData[thread]['reclaimCnt'] += 1

            elif func == "mm_vmscan_kswapd_sleep":
                for key, value in self.reclaimData.items():
                    try:
                        self.threadData[key]
                    except:
                        self.threadData[key] = dict(self.init_threadData)
                        self.threadData[key]['comm'] = comm

                    self.threadData[key]['reclaimWait'] += float(time) - float(value['start'])
                    del self.reclaimData[key]

            elif func == "mm_vmscan_direct_reclaim_begin":
                if self.threadData[thread]['dReclaimStart'] <= 0:
                    self.threadData[thread]['dReclaimStart'] = float(time)

                self.threadData[thread]['dReclaimCnt'] += 1
                self.threadData[coreId]['dReclaimCnt'] += 1

            elif func == "mm_vmscan_direct_reclaim_end":
                m = re.match(r'^\s*nr_reclaimed=(?P<nr>[0-9]+)', etc)
                if m is not None:
                    d = m.groupdict()

                    if self.threadData[thread]['dReclaimStart'] > 0:
                        self.threadData[thread]['dReclaimWait'] += \
                            float(time) - self.threadData[thread]['dReclaimStart']
                        self.threadData[coreId]['dReclaimWait'] += \
                            float(time) - self.threadData[thread]['dReclaimStart']

                    self.threadData[thread]['dReclaimStart'] = 0
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "task_newtask":
                m = re.match(r'^\s*pid=(?P<pid>[0-9]+)\s+comm=(?P<comm>\S+)', etc)
                if m is not None:
                    d = m.groupdict()

                    pid = d['pid']

                    try:
                        self.threadData[pid]
                    except:
                        self.threadData[pid] = dict(self.init_threadData)
                        self.threadData[pid]['comm'] = d['comm']
                        self.threadData[pid]['ptid'] = thread
                        self.threadData[pid]['new'] = 'N'
                        self.threadData[pid]['createdTime'] = float(time)

                    if self.threadData[thread]['childList'] is None:
                        self.threadData[thread]['childList'] = list()

                    self.threadData[thread]['childList'].append(pid)
                    self.nrNewTask += 1
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "task_rename":
                m = re.match(r'^\s*pid=(?P<pid>[0-9]+)\s+oldcomm=(?P<oldcomm>.*)\s+' + \
                    r'newcomm=(?P<newcomm>.*)\s+oom_score_adj', etc)
                if m is not None:
                    d = m.groupdict()

                    pid = d['pid']
                    newcomm = d['newcomm']

                    try:
                        self.threadData[pid]
                    except:
                        self.threadData[pid] = dict(self.init_threadData)
                        self.threadData[pid]['comm'] = newcomm
                        self.threadData[pid]['ptid'] = thread

                    self.threadData[pid]['comm'] = newcomm
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "sched_process_exit":
                m = re.match(r'^\s*comm=(?P<comm>.*)\s+pid=(?P<pid>[0-9]+)', etc)
                if m is not None:
                    d = m.groupdict()

                    pid = d['pid']

                    try:
                        self.threadData[pid]
                    except:
                        self.threadData[pid] = dict(self.init_threadData)
                        self.threadData[pid]['comm'] = d['comm']
                        self.threadData[pid]['die'] = 'D'

                    if self.threadData[pid]['die'] != 'F':
                        self.threadData[pid]['die'] = 'D'
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "sched_process_wait":
                m = re.match(r'^\s*comm=(?P<comm>.*)\s+pid=(?P<pid>[0-9]+)', etc)
                if m is not None:
                    d = m.groupdict()

                    self.threadData[thread]['waitStartAsParent'] = float(time)
                    self.threadData[thread]['waitPid'] = int(d['pid'])
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "suspend_resume":
                state = None

                if etc.rfind("suspend_enter") > 0:
                    if etc.rfind("begin") > 0:
                        state = 'S'
                elif etc.rfind("machine_suspend") > 0:
                    if etc.rfind("end") > 0:
                        state = 'F'
                # Complete a PM transition for all non-sysdev devices #
                elif etc.rfind("dpm_resume_user") > 0:
                    if etc.rfind("end") > 0:
                        state = 'R'

                if state is not None:
                    self.suspendData.append([time, state])

            elif func == "net_dev_xmit":
                pass

            elif func == "netif_receive_skb":
                pass

            elif func == "module_load":
                m = re.match(r'^\s*(?P<module>.*)\s+(?P<address>.*)', etc)
                if m is not None:
                    d = m.groupdict()

                    module = d['module']
                    address = d['address']

                    self.moduleData.append(['load', thread, time, module, address])
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "module_free":
                m = re.match(r'^\s*(?P<module>.*)', etc)
                if m is not None:
                    d = m.groupdict()

                    module = d['module']

                    self.moduleData.append(['free', thread, time, module, None])
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "module_put":
                m = re.match(\
                    r'^\s*(?P<module>.*)\s+call_site=(?P<site>.*)\s+refcnt=(?P<refcnt>[0-9]+)', etc)
                if m is not None:
                    d = m.groupdict()

                    module = d['module']
                    refcnt = int(d['refcnt'])

                    self.moduleData.append(['put', thread, time, module, refcnt])
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "cpu_idle":
                m = re.match(r'^\s*state=(?P<state>[0-9]+)\s+cpu_id=(?P<cpu_id>[0-9]+)', etc)
                if m is not None:
                    d = m.groupdict()

                    tid = '0[' + d['cpu_id']+ ']'

                    if self.threadData[tid]['lastIdleStatus'] == int(d['state']):
                        return
                    else:
                        self.threadData[tid]['lastIdleStatus'] = int(d['state'])

                    if self.threadData[tid]['coreSchedCnt'] == 0 and \
                        self.threadData[tid]['offTime'] == 0:
                        self.threadData[tid]['offTime'] = float(time) - float(self.startTime)

                    # Wake core up, but the number 3 as this condition is not certain #
                    if int(d['state']) < 3:
                        self.threadData[tid]['offCnt'] += 1
                        self.threadData[tid]['lastOff'] = float(time)
                    # Start to sleep #
                    elif self.threadData[tid]['lastOff'] > 0:
                        self.threadData[tid]['offTime'] += \
                            (float(time) - self.threadData[tid]['lastOff'])
                        self.threadData[tid]['lastOff'] = float(0)
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            elif func == "cpu_frequency":
                # toDo: calculate power consumption for DVFS system #
                return

            elif func == "console":
                m = re.match(r'^\s*\[\s*(?P<time>\S+)\s*\]\s+EVENT_(?P<event>\S+)', etc)
                if m is not None:
                    d = m.groupdict()

                    event = d['event']

                    # initialize ThreadAnalyzer data #
                    if event == 'START':
                        self.threadData = {}
                        self.irqData = {}
                        self.ioData = {}
                        self.reclaimData = {}
                        self.pageTable = {}
                        self.kmemTable = {}
                        self.intervalData = []
                        self.depData = []
                        self.syscallData = []
                        self.lastJob = {}
                        self.preemptData = []
                        self.suspendData = []
                        self.markData = []
                        self.consoleData = []
                        self.startTime = time
                        return
                    # finish data processing #
                    elif event == 'STOP':
                        self.finishTime = time
                        self.stopFlag = True
                        return
                    # restart data processing #
                    elif event == 'RESTART':
                        self.threadDataOld = self.threadData
                        self.threadData = {}
                        self.irqDataOld = self.irqData
                        self.irqData = {}
                        self.ioDataOld = self.ioData
                        self.ioData = {}
                        self.reclaimDataOld = self.reclaimData
                        self.reclaimData = {}

                        self.totalTimeOld = round(float(time) - float(self.startTime), 7)
                        self.startTime = time
                        return
                    # save mark event #
                    elif event == 'MARK':
                        self.markData.append(time)

                    ei.addEvent(time, event)
                else:
                    # process CPU shutdown event #
                    m = re.match(r'^\s*\[\s*(?P<time>\S+)\s*\]\s+CPU(?P<core>[0-9]+)\: shutdown', etc)
                    if m is not None:
                        ed = m.groupdict()

                        try:
                            # set status of thread #
                            lastTid = self.lastTidPerCore[ed['core']]
                            self.threadData[lastTid]['stop'] = float(ed['time'])
                            self.threadData[lastTid]['lastStatus'] = 'S'

                            # set status of core #
                            scoreId = '0[%s]' % ed['core']
                            self.threadData[scoreId]['offCnt'] += 1
                            self.threadData[scoreId]['lastOff'] = float(ed['time'])
                            self.threadData[scoreId]['start'] = float(ed['time'])
                            self.threadData[scoreId]['lastStatus'] = 'R'
                        except:
                            pass

                    # save consol log #
                    self.consoleData.append([d['thread'], core, time, etc])

            elif func == "tracing_mark_write":
                m = re.match(r'^\s*EVENT_(?P<event>\S+)', etc)
                if m is not None:
                    d = m.groupdict()

                    event = d['event']

                    # initialize ThreadAnalyzer data #
                    if event == 'START':
                        self.threadData = {}
                        self.irqData = {}
                        self.ioData = {}
                        self.reclaimData = {}
                        self.pageTable = {}
                        self.kmemTable = {}
                        self.intervalData = []
                        self.depData = []
                        self.syscallData = []
                        self.lastJob = {}
                        self.preemptData = []
                        self.suspendData = []
                        self.markData = []
                        self.consoleData = []
                        self.startTime = time
                        return
                    # finish data processing #
                    elif event == 'STOP':
                        self.finishTime = time
                        self.stopFlag = True
                        return
                    # restart data processing #
                    elif event == 'RESTART':
                        self.threadDataOld = self.threadData
                        self.threadData = {}
                        self.irqDataOld = self.irqData
                        self.irqData = {}
                        self.ioDataOld = self.ioData
                        self.ioData = {}
                        self.reclaimDataOld = self.reclaimData
                        self.reclaimData = {}

                        self.totalTimeOld = round(float(time) - float(self.startTime), 7)
                        self.startTime = time
                        return
                    # save mark event #
                    elif event == 'MARK':
                        self.markData.append(time)

                    ei.addEvent(time, event)
                else:
                    SystemManager.printWarning("Fail to recognize '%s' event" % func)

            # custom event #
            elif func in SystemManager.customEventList:
                # add data into list #
                ntime = float(time) - float(self.startTime)
                self.customEventData.append([func, comm, thread, ntime, etc.strip()])

                # make event list #
                if self.threadData[thread]['customEvent'] is None:
                    self.threadData[thread]['customEvent'] = {}

                try:
                    self.threadData[thread]['customEvent'][func]
                except:
                    self.threadData[thread]['customEvent'][func] = dict(self.init_eventData)
                try:
                    self.customEventInfo[func]
                except:
                    self.customEventInfo[func] = dict(self.init_eventData)

                self.threadData[thread]['customEvent'][func]['count'] += 1
                self.customEventInfo[func]['count'] += 1

                # get interval #
                interDiff = 0
                if self.threadData[thread]['customEvent'][func]['start'] > 0:
                    interDiff = float(time) - self.threadData[thread]['customEvent'][func]['start']

                # update period of thread #
                if interDiff > self.threadData[thread]['customEvent'][func]['maxPeriod'] or \
                    self.threadData[thread]['customEvent'][func]['maxPeriod'] == 0:
                    self.threadData[thread]['customEvent'][func]['maxPeriod'] = interDiff
                if interDiff < self.threadData[thread]['customEvent'][func]['minPeriod'] or \
                    self.threadData[thread]['customEvent'][func]['minPeriod'] == 0:
                    self.threadData[thread]['customEvent'][func]['minPeriod'] = interDiff

                # update period of system #
                if interDiff > self.customEventInfo[func]['maxPeriod'] or \
                    self.customEventInfo[func]['maxPeriod'] == 0:
                    self.customEventInfo[func]['maxPeriod'] = interDiff
                if interDiff < self.customEventInfo[func]['minPeriod'] or \
                    self.customEventInfo[func]['minPeriod'] == 0:
                    self.customEventInfo[func]['minPeriod'] = interDiff

                self.threadData[thread]['customEvent'][func]['start'] = float(time)

            else:
                # user event #
                for name in SystemManager.userEventList:
                    if func.startswith(name) is False:
                        continue

                    if self.threadData[thread]['userEvent'] is None:
                        self.threadData[thread]['userEvent'] = {}

                    try:
                        self.threadData[thread]['userEvent'][name]
                    except:
                        self.threadData[thread]['userEvent'][name] = dict(self.init_eventData)

                    try:
                        self.userEventInfo[name]
                    except:
                        self.userEventInfo[name] = dict(self.init_eventData)

                    if func == '%s_enter' % name:
                        # add data into list #
                        ntime = float(time) - float(self.startTime)
                        self.userEventData.append(['ENTER', name, comm, thread, ntime, ''])

                        # get interval #
                        interDiff = 0
                        if self.threadData[thread]['userEvent'][name]['start'] > 0:
                            interDiff = float(time) - self.threadData[thread]['userEvent'][name]['start']

                        self.threadData[thread]['userEvent'][name]['count'] += 1
                        self.threadData[thread]['userEvent'][name]['start'] = float(time)

                        # update period of thread #
                        if interDiff > self.threadData[thread]['userEvent'][name]['maxPeriod'] or \
                            self.threadData[thread]['userEvent'][name]['maxPeriod'] == 0:
                            self.threadData[thread]['userEvent'][name]['maxPeriod'] = interDiff
                        if interDiff < self.threadData[thread]['userEvent'][name]['minPeriod'] or \
                            self.threadData[thread]['userEvent'][name]['minPeriod'] == 0:
                            self.threadData[thread]['userEvent'][name]['minPeriod'] = interDiff

                        self.userEventInfo[name]['count'] += 1

                        # update period of system #
                        if interDiff > self.userEventInfo[name]['maxPeriod'] or \
                            self.userEventInfo[name]['maxPeriod'] == 0:
                            self.userEventInfo[name]['maxPeriod'] = interDiff
                        if interDiff < self.userEventInfo[name]['minPeriod'] or \
                            self.userEventInfo[name]['minPeriod'] == 0:
                            self.userEventInfo[name]['minPeriod'] = interDiff

                    elif func == '%s_exit' % name:
                        # add data into list #
                        ntime = float(time) - float(self.startTime)
                        self.userEventData.append(\
                            ['EXIT', name, comm, thread, ntime, etc[etc.find('(')+1:etc.rfind('<-')]])

                        # get usage #
                        usage = 0
                        if self.threadData[thread]['userEvent'][name]['start'] > 0:
                            usage = float(time) - self.threadData[thread]['userEvent'][name]['start']
                            self.threadData[thread]['userEvent'][name]['usage'] += usage
                            self.userEventInfo[name]['usage'] += usage

                            # update usage of thread #
                            if usage > self.threadData[thread]['userEvent'][name]['max'] or \
                                self.threadData[thread]['userEvent'][name]['max'] == 0:
                                self.threadData[thread]['userEvent'][name]['max'] = usage
                            if usage < self.threadData[thread]['userEvent'][name]['min'] or \
                                self.threadData[thread]['userEvent'][name]['min'] == 0:
                                self.threadData[thread]['userEvent'][name]['min'] = usage

                            # update usage of system #
                            if usage > self.userEventInfo[name]['max'] or \
                                self.userEventInfo[name]['max'] == 0:
                                self.userEventInfo[name]['max'] = usage
                            if usage < self.userEventInfo[name]['min'] or \
                                self.userEventInfo[name]['min'] == 0:
                                self.userEventInfo[name]['min'] = usage

                # kernel event #
                for name in SystemManager.kernelEventList:
                    if func.startswith(name) is False:
                        continue

                    if self.threadData[thread]['kernelEvent'] is None:
                        self.threadData[thread]['kernelEvent'] = {}

                    try:
                        self.threadData[thread]['kernelEvent'][name]
                    except:
                        self.threadData[thread]['kernelEvent'][name] = dict(self.init_eventData)

                    try:
                        self.kernelEventInfo[name]
                    except:
                        self.kernelEventInfo[name] = dict(self.init_eventData)

                    if func == '%s_enter' % name:
                        # add data into list #
                        ntime = float(time) - float(self.startTime)

                        isSaved = True
                        m = re.match(\
                            r'^\s*\((?P<name>.+)\+(?P<offset>.+) <(?P<addr>.+)>\)(?P<args>.*)', etc)
                        if m is not None:
                            d = m.groupdict()
                            self.kernelEventData.append(\
                                ['ENTER', name, d['addr'], comm, thread, ntime, '', d['args']])
                        else:
                            m = re.match(\
                                r'^\s*\((?P<name>.+)\+(?P<offset>.+)\)(?P<args>.*)', etc)
                            if m is not None:
                                d = m.groupdict()
                                self.kernelEventData.append(\
                                    ['ENTER', name, '', comm, thread, ntime, '', d['args']])
                            else:
                                isSaved = False
                                SystemManager.printWarning("Fail to recognize '%s' kernel event" % etc)

                        if isSaved:
                            # get interval #
                            interDiff = 0
                            if self.threadData[thread]['kernelEvent'][name]['start'] > 0:
                                interDiff = float(time) - \
                                    self.threadData[thread]['kernelEvent'][name]['start']

                            self.threadData[thread]['kernelEvent'][name]['count'] += 1
                            self.threadData[thread]['kernelEvent'][name]['start'] = float(time)

                            # update period of thread #
                            if interDiff > self.threadData[thread]['kernelEvent'][name]['maxPeriod'] or \
                                self.threadData[thread]['kernelEvent'][name]['maxPeriod'] == 0:
                                self.threadData[thread]['kernelEvent'][name]['maxPeriod'] = interDiff
                            if interDiff < self.threadData[thread]['kernelEvent'][name]['minPeriod'] or \
                                self.threadData[thread]['kernelEvent'][name]['minPeriod'] == 0:
                                self.threadData[thread]['kernelEvent'][name]['minPeriod'] = interDiff

                            self.kernelEventInfo[name]['count'] += 1

                            # update period of system #
                            if interDiff > self.kernelEventInfo[name]['maxPeriod'] or \
                                self.kernelEventInfo[name]['maxPeriod'] == 0:
                                self.kernelEventInfo[name]['maxPeriod'] = interDiff
                            if interDiff < self.kernelEventInfo[name]['minPeriod'] or \
                                self.kernelEventInfo[name]['minPeriod'] == 0:
                                self.kernelEventInfo[name]['minPeriod'] = interDiff

                    elif func == '%s_exit' % name:
                        # add data into list #
                        ntime = float(time) - float(self.startTime)

                        isSaved = True
                        m = re.match(\
                            (r'^\s*\((?P<caller>.+)\+(?P<offset>.+) <(?P<caddr>.+)> <- '
                            r'(?P<name>.+) <(?P<addr>.+)>\)(?P<args>.*)'), etc)
                        if m is not None:
                            d = m.groupdict()
                            self.kernelEventData.append(\
                                ['EXIT', name, d['addr'], comm, thread, ntime, d['caller'], \
                                d['args'], d['caddr']])
                        else:
                            m = re.match(\
                                r'^\s*\((?P<caller>.+)\+(?P<offset>.+) <- (?P<name>.+)\)(?P<args>.*)', etc)
                            if m is not None:
                                d = m.groupdict()
                                self.kernelEventData.append(\
                                    ['EXIT', name, '', comm, thread, ntime, d['caller'], \
                                    d['args'], ''])
                            else:
                                isSaved = False
                                SystemManager.printWarning("Fail to recognize '%s' kernel event" % etc)

                        if isSaved:
                            # get usage #
                            usage = 0
                            if self.threadData[thread]['kernelEvent'][name]['start'] > 0:
                                usage = float(time) - self.threadData[thread]['kernelEvent'][name]['start']
                                self.threadData[thread]['kernelEvent'][name]['usage'] += usage
                                self.kernelEventInfo[name]['usage'] += usage

                                # update usage of thread #
                                if usage > self.threadData[thread]['kernelEvent'][name]['max'] or \
                                    self.threadData[thread]['kernelEvent'][name]['max'] == 0:
                                    self.threadData[thread]['kernelEvent'][name]['max'] = usage
                                if usage < self.threadData[thread]['kernelEvent'][name]['min'] or \
                                    self.threadData[thread]['kernelEvent'][name]['min'] == 0:
                                    self.threadData[thread]['kernelEvent'][name]['min'] = usage

                                # update usage of system #
                                if usage > self.kernelEventInfo[name]['max'] or \
                                    self.kernelEventInfo[name]['max'] == 0:
                                    self.kernelEventInfo[name]['max'] = usage
                                if usage < self.kernelEventInfo[name]['min'] or \
                                    self.kernelEventInfo[name]['min'] == 0:
                                    self.kernelEventInfo[name]['min'] = usage
        else:
            # handle modified type of event #
            if SystemManager.tgidEnable:
                m = re.match(r'^\s*(?P<comm>.+)-(?P<thread>[0-9]+)\s+\(\s*(?P<tgid>\S+)\)\s+' + \
                    r'\[(?P<core>[0-9]+)\]\s+(?P<time>\S+):\s+(?P<func>.+):(?P<etc>.+)', string)
            else:
                m = re.match(r'^\s*(?P<comm>.+)-(?P<thread>[0-9]+)\s+\[(?P<core>[0-9]+)\]\s+' + \
                    r'(?P<time>\S+):\s+(?P<func>.+):(?P<etc>.+)', string)

            if m is not None:
                d = m.groupdict()
                comm = d['comm']
                core = str(int(d['core']))
                func = d['func']
                etc = d['etc']
                time = d['time']

                if func.find("tracing_mark_write") >= 0:
                    m = re.match(r'^\s*EVENT_(?P<event>\S+)', etc)
                    if m is not None:
                        d = m.groupdict()

                        event = d['event']

                        # initialize ThreadAnalyzer data #
                        if event == 'START':
                            self.threadData = {}
                            self.irqData = {}
                            self.ioData = {}
                            self.reclaimData = {}
                            self.pageTable = {}
                            self.kmemTable = {}
                            self.intervalData = []
                            self.depData = []
                            self.syscallData = []
                            self.lastJob = {}
                            self.preemptData = []
                            self.suspendData = []
                            self.markData = []
                            self.consoleData = []
                            self.startTime = time
                            return
                        # finish data processing #
                        elif event == 'STOP':
                            self.finishTime = time
                            self.stopFlag = True
                            return
                        # restart data processing #
                        elif event == 'RESTART':
                            self.threadDataOld = self.threadData
                            self.threadData = {}
                            self.irqDataOld = self.irqData
                            self.irqData = {}
                            self.ioDataOld = self.ioData
                            self.ioData = {}
                            self.reclaimDataOld = self.reclaimData
                            self.reclaimData = {}

                            self.totalTimeOld = round(float(time) - float(self.startTime), 7)
                            self.startTime = time
                            return
                        # saving mark event #
                        elif event == 'MARK':
                            self.markData.append(time)

                        ei.addEvent(time, event)



    def compareThreadData(self):
        for key, value in sorted(ti.threadData.items(), key=lambda e: e[1]['usage'], reverse=True):
            newPercent = round(float(value['usage']) / float(ti.totalTime), 7) * 100

            try:
                ti.threadDataOld[key]
            except:
                if int(newPercent) < 1:
                    del ti.threadData[key]
                continue

            oldPercent = \
                round(float(ti.threadDataOld[key]['usage']) / float(ti.totalTimeOld), 7) * 100
            if int(oldPercent) >= int(newPercent) or int(newPercent) < 1:
                del ti.threadData[key]



    def printFileStat(self):
        # save uptime #
        try:
            SystemManager.uptimeFd.seek(0)
            SystemManager.uptime = float(SystemManager.uptimeFd.readlines()[0].split()[0])
        except:
            try:
                uptimePath = "%s/%s" % (SystemManager.procPath, 'uptime')
                SystemManager.uptimeFd = open(uptimePath, 'r')
                SystemManager.uptime = float(SystemManager.uptimeFd.readlines()[0].split()[0])
            except:
                SystemManager.printWarning('Fail to open %s' % uptimePath)

        SystemManager.addPrint(\
            "\n[Top File Info] [Time: %7.3f] [Proc: %d] [FD: %d] [File: %d] [Unit: %%/MB]\n" % \
            (SystemManager.uptime, self.nrProcess, self.nrFd, len(self.fileData)))

        SystemManager.addPrint(twoLine + '\n' + \
            ("{0:^16} ({1:^5}/{2:^5}/{3:^4}/{4:>4})|{5:^4}|{6:^107}|\n{7:1}\n").\
            format("PROC", "ID", "Pid", "Nr", "Pri", "FD", "PATH", oneLine), newline = 3)

        # set sort value #
        if SystemManager.sort == 'p':
            sortedProcData = sorted(self.procData.items(), \
                key=lambda e: int(e[0]))
        else:
            # set cpu usage as default #
            sortedProcData = sorted(self.procData.items(), \
                key=lambda e: len(e[1]['fdList']), reverse=True)

        # set proc and file filter #
        procFilter = []
        fileFilter = []
        if SystemManager.showGroup != []:
            for fval in SystemManager.showGroup:
                pos = fval.find(':')
                if pos >= 0:
                    procItem = fval[:pos]
                    fileItem = fval[pos+1:]
                    if len(procItem) > 0:
                        procFilter.append(procItem)
                    if len(fileItem) > 0:
                        fileFilter.append(fileItem)
                else:
                    procFilter.append(fval)

        # print process info #
        procCnt = 0
        for idx, value in sortedProcData:
            # apply filter #
            if procFilter != []:
                if SystemManager.groupProcEnable:
                    if SystemManager.processEnable:
                        if value['stat'][self.ppidIdx] in procFilter:
                            pass
                        elif idx in procFilter:
                            pass
                        else:
                            continue
                    elif value['mainID'] not in procFilter:
                        continue
                else:
                    if idx in procFilter:
                        pass
                    elif True in [value['stat'][self.commIdx].find(val) >= 0 for val in procFilter]:
                        pass
                    else:
                        continue

            comm = value['stat'][self.commIdx][1:-1]

            pid = value['stat'][self.ppidIdx]

            if ConfigManager.schedList[int(value['stat'][self.policyIdx])] == 'C':
                schedValue = "%3d" % (int(value['stat'][self.prioIdx]) - 20)
            else:
                schedValue = "%3d" % (abs(int(value['stat'][self.prioIdx]) + 1))

            procInfo = ("{0:>16} ({1:>5}/{2:>5}/{3:>4}/{4:>4})").\
                format(comm, idx, pid, value['stat'][self.nrthreadIdx], \
                ConfigManager.schedList[int(value['stat'][self.policyIdx])] + str(schedValue))

            procInfoLen = len(procInfo)

            if 'fdInfo' in value:
                details = '   '.join(["%s: %s" % (fd,path) for fd, path in \
                    sorted(value['fdInfo'].items(), key=lambda e: int(e[1]), reverse=True)])
            else:
                details = ' '
            procInfo = "%s|%s\n" % \
                (procInfo, '{0:>4}|\t{1:<105}|'.format(len(value['fdList']), details))

            fdCnt = 0
            for fd, path in sorted(value['fdList'].items(), key=lambda e: int(e[0]), reverse=True):
                # cut by rows of terminal #
                if SystemManager.showAll is False and int(SystemManager.bufferRows) >= \
                    int(SystemManager.ttyRows) - SystemManager.ttyRowsMargin  - 2 and \
                    SystemManager.printFile is None:
                    break

                if fileFilter != []:
                    found = False
                    for fileItem in fileFilter:
                        if path.find(fileItem) >= 0:
                            found = True
                            break
                    if found is False:
                        continue

                if procInfo != '':
                    SystemManager.addPrint(procInfo)
                    procInfo = ''

                SystemManager.addPrint(\
                    ("{0:>1}|{1:>4}|\t{2:<105}|\n").format(' ' * procInfoLen, fd, path))

                fdCnt += 1

            if fdCnt > 0:
                procCnt += 1

            # cut by rows of terminal #
            if SystemManager.showAll is False and int(SystemManager.bufferRows) >= \
                int(SystemManager.ttyRows) - SystemManager.ttyRowsMargin  - 2 and \
                SystemManager.printFile is None:
                break

            if fdCnt > 0:
                SystemManager.addPrint(oneLine + '\n')

        if procCnt == 0:
            SystemManager.addPrint("{0:^16}\n{1:1}\n".format('None', oneLine))

        # realtime mode #
        if SystemManager.printFile is None:
            SystemManager.pipePrint(SystemManager.bufferString)
            SystemManager.clearPrint()
        # buffered mode #
        else:
            SystemManager.procBuffer[:0] = [SystemManager.bufferString]
            SystemManager.procBufferSize += len(SystemManager.bufferString)
            SystemManager.clearPrint()

            while SystemManager.procBufferSize > int(SystemManager.bufferSize) * 10:
                if len(SystemManager.procBuffer) == 1:
                    break
                SystemManager.procBufferSize -= len(SystemManager.procBuffer[-1])
                SystemManager.procBuffer.pop(-1)



    def saveFileStat(self):
        # save proc and file instance #
        SystemManager.procInstance = self.procData
        SystemManager.fileInstance = self.fileData

        # get process list #
        try:
           pids = os.listdir(SystemManager.procPath)
        except:
            SystemManager.printError('Fail to open %s' % SystemManager.procPath)
            sys.exit(0)

        # remove self info #
        try:
            del pids[pids.index(str(SystemManager.pid))]
        except:
            pass

        # get thread list #
        for pid in pids:
            try:
                int(pid)
                self.nrProcess += 1
            except:
                continue

            # make path of tid #
            procPath = "%s/%s" % (SystemManager.procPath, pid)
            fdlistPath = "%s/%s" % (procPath, 'fd')

            # make process object with constant value #
            self.procData[pid] = dict(self.init_procData)
            self.procData[pid]['mainID'] = pid
            self.procData[pid]['taskPath'] = procPath
            self.procData[pid]['fdList'] = {}

            # save stat of process #
            self.saveProcData(procPath, pid)

            # save file info per process #
            try:
                fdlist = os.listdir(fdlistPath)
            except:
                SystemManager.printWarning('Fail to open %s' % fdlistPath)
                continue

            # save fd info of process #
            for fd in fdlist:
                try:
                    int(fd)
                    self.nrFd += 1
                except:
                    continue

                try:
                    # add file info into fdList #
                    fdPath = "%s/%s" % (fdlistPath, fd)
                    filename = os.readlink(fdPath)
                    self.procData[pid]['fdList'][fd] = filename

                    # increase reference count of file #
                    try:
                        self.fileData[filename] += 1
                    except:
                        self.fileData[filename] = 1

                    # initialize fdinfo per process #
                    try:
                        self.procData[pid]['fdInfo']
                    except:
                        self.procData[pid]['fdInfo'] = {}
                        self.procData[pid]['fdInfo']['EVENT'] = 0
                        self.procData[pid]['fdInfo']['SOCKET'] = 0
                        self.procData[pid]['fdInfo']['DEVICE'] = 0
                        self.procData[pid]['fdInfo']['PIPE'] = 0
                        self.procData[pid]['fdInfo']['FILE'] = 0
                        self.procData[pid]['fdInfo']['PROC'] = 0

                    # increase type count per process #
                    if filename.startswith('anon'):
                        self.procData[pid]['fdInfo']['EVENT'] += 1
                    elif filename.startswith('socket'):
                        self.procData[pid]['fdInfo']['SOCKET'] += 1
                    elif filename.startswith('/dev'):
                        self.procData[pid]['fdInfo']['DEVICE'] += 1
                    elif filename.startswith('pipe'):
                        self.procData[pid]['fdInfo']['PIPE'] += 1
                    elif filename.startswith('/proc'):
                        self.procData[pid]['fdInfo']['PROC'] += 1
                    else:
                        self.procData[pid]['fdInfo']['FILE'] += 1
                except:
                    self.nrFd -= 1
                    SystemManager.printWarning('Fail to open %s' % fdPath)



    def saveSystemStat(self):
        # save cpu info #
        try:
            cpuBuf = None
            SystemManager.statFd.seek(0)
            cpuBuf = SystemManager.statFd.readlines()
        except:
            try:
                cpuPath = "%s/%s" % (SystemManager.procPath, 'stat')
                SystemManager.statFd = open(cpuPath, 'r')
                cpuBuf = SystemManager.statFd.readlines()
            except:
                SystemManager.printWarning('Fail to open %s' % cpuPath)

        if cpuBuf is not None:
            self.prevCpuData = self.cpuData
            self.cpuData = {}

            for line in cpuBuf:
                statList = line.split()
                cpuId = statList[0]
                if cpuId == 'cpu':
                    if not 'all' in self.cpuData:
                        # stat list from http://man7.org/linux/man-pages/man5/proc.5.html #
                        self.cpuData['all'] = {'user': long(statList[1]), \
                            'nice': long(statList[2]), 'system': long(statList[3]), \
                            'idle': long(statList[4]), 'iowait': long(statList[5]), \
                            'irq': long(statList[6]), 'softirq': long(statList[7])}
                elif cpuId.rfind('cpu') == 0:
                    if not int(cpuId[3:]) in self.cpuData:
                        self.cpuData[int(cpuId[3:])] = {'user': long(statList[1]), \
                            'nice': long(statList[2]), 'system': long(statList[3]), \
                            'idle': long(statList[4]), 'iowait': long(statList[5]), \
                            'irq': long(statList[6]), 'softirq': long(statList[7])}
                else:
                    if not cpuId in self.cpuData:
                        self.cpuData[cpuId] = {cpuId: long(statList[1])}

            # set the number of core #
            SystemManager.nrCore = 0
            for idx, val in sorted(self.cpuData.items(), reverse=False):
                try:
                    SystemManager.maxCore = int(idx)
                    SystemManager.nrCore += 1
                except:
                    continue

        # save mem info #
        try:
            memBuf = None
            SystemManager.memFd.seek(0)
            memBuf = SystemManager.memFd.readlines()
        except:
            try:
                memPath = "%s/%s" % (SystemManager.procPath, 'meminfo')
                SystemManager.memFd = open(memPath, 'r')

                memBuf = SystemManager.memFd.readlines()
            except:
                SystemManager.printWarning('Fail to open %s' % memPath)

        if memBuf is not None:
            self.memData = {}

            for line in memBuf:
                memList = line.split()
                self.memData[memList[0][:-1]] = long(memList[1])

        # save vmstat info #
        try:
            vmBuf = None
            SystemManager.vmstatFd.seek(0)
            vmBuf = SystemManager.vmstatFd.readlines()
        except:
            try:
                vmstatPath = "%s/%s" % (SystemManager.procPath, 'vmstat')
                SystemManager.vmstatFd = open(vmstatPath, 'r')

                # vmstat list from https://access.redhat.com/solutions/406773 #
                vmBuf = SystemManager.vmstatFd.readlines()
            except:
                SystemManager.printWarning('Fail to open %s' % vmstatPath)

        if vmBuf is not None:
            self.prevVmData = self.vmData
            self.vmData = {}

            for line in vmBuf:
                vmList = line.split()
                self.vmData[vmList[0]] = long(vmList[1])

        # save swaps info #
        try:
            swapBuf = None
            SystemManager.swapFd.seek(0)
            swapBuf = SystemManager.swapFd.readlines()
        except:
            try:
                swapPath = "%s/%s" % (SystemManager.procPath, 'swaps')
                SystemManager.swapFd = open(swapPath, 'r')

                swapBuf = SystemManager.swapFd.readlines()
            except:
                SystemManager.printWarning('Fail to open %s' % swapPath)

        # get swap usage if it changed #
        if self.prevSwaps != swapBuf and swapBuf is not None:
            swapTotal = 0
            swapUsed = 0

            for line in swapBuf:
                swapList = line.split()
                # swapList = [Filename, Type, Size, Used, Priority] #
                try:
                    swapTotal += int(swapList[2])
                    swapUsed += int(swapList[3])
                except:
                    continue

            self.vmData['swapTotal'] = swapTotal
            self.vmData['swapUsed'] = swapUsed

            self.prevSwaps = swapBuf
        else:
            try:
                self.vmData['swapTotal'] = self.prevVmData['swapTotal']
                self.vmData['swapUsed'] = self.prevVmData['swapUsed']
            except:
                self.vmData['swapTotal'] = 0
                self.vmData['swapUsed'] = 0

        # save netstat #
        try:
            SystemManager.netstatFd.seek(0)
            SystemManager.prevNetstat = SystemManager.netstat
            SystemManager.netstat = SystemManager.netstatFd.readlines()
        except:
            try:
                netstatPath = "%s/%s" % (SystemManager.procPath, 'net/netstat')
                SystemManager.netstatFd = open(netstatPath, 'r')
                SystemManager.netstat = SystemManager.netstatFd.readlines()
            except:
                SystemManager.printWarning('Fail to open %s' % netstatPath)

        # save uptime #
        try:
            SystemManager.uptimeFd.seek(0)
            SystemManager.prevUptime = SystemManager.uptime
            SystemManager.uptime = float(SystemManager.uptimeFd.readlines()[0].split()[0])
            SystemManager.uptimeDiff = SystemManager.uptime - SystemManager.prevUptime
        except:
            try:
                uptimePath = "%s/%s" % (SystemManager.procPath, 'uptime')
                SystemManager.uptimeFd = open(uptimePath, 'r')
                SystemManager.uptime = float(SystemManager.uptimeFd.readlines()[0].split()[0])
            except:
                SystemManager.printWarning('Fail to open %s' % uptimePath)

        # get process list #
        try:
            pids = os.listdir(SystemManager.procPath)
        except:
            SystemManager.printError('Fail to open %s' % SystemManager.procPath)

        # save proc instance #
        SystemManager.procInstance = self.procData

        # get thread list #
        for pid in pids:
            try:
                int(pid)
                self.nrProcess += 1
            except:
                continue

            # make path of tid #
            procPath = "%s/%s" % (SystemManager.procPath, pid)
            taskPath = "%s/%s" % (procPath, 'task')

            # save info per process #
            if SystemManager.processEnable:
                # make process object with constant value #
                self.procData[pid] = dict(self.init_procData)
                self.procData[pid]['mainID'] = pid
                self.procData[pid]['taskPath'] = procPath

                # save stat of process #
                self.saveProcData(procPath, pid)

                # calculate number of threads #
                if pid in self.procData:
                    self.nrThread += int(self.procData[pid]['stat'][self.nrthreadIdx])

                continue

            # save info per thread #
            try:
                tids = os.listdir(taskPath)
            except:
                SystemManager.printWarning('Fail to open %s' % taskPath)
                continue

            for tid in tids:
                try:
                    int(tid)
                    self.nrThread += 1
                except:
                    continue

                threadPath = "%s/%s" % (taskPath, tid)

                # make process object with constant value #
                self.procData[tid] = dict(self.init_procData)
                self.procData[tid]['mainID'] = pid
                self.procData[tid]['taskPath'] = threadPath

                # main thread #
                if pid == tid:
                    self.procData[tid]['isMain'] = True
                    self.procData[tid]['tids'] = []
                # sibling thread #
                else:
                    try:
                        self.procData[pid]['tids'].append(tid)
                    except:
                        self.procData[pid] = dict(self.init_procData)
                        self.procData[pid]['tids'] = []
                        self.procData[pid]['tids'].append(tid)

                # save stat of thread #
                self.saveProcData(threadPath, tid)



    @staticmethod
    def saveProcSmapsData(path, tid):
        buf = ''
        mtype = ''
        stable = {}
        ftable = {}
        fpath = '%s/%s' % (path, 'smaps')
        ptable = {'HEAP': {}, 'FILE': {}, 'STACK': {}, 'ETC': {}, 'SHM': {}}

        checkCnt = 0
        checklist = ['Size:', 'Rss:', 'Pss:', 'Shared_Dirty:', \
            'Private_Dirty:', 'AnonHugePages:', 'Swap:', 'Locked:']

        try:
            SystemManager.procInstance[tid]['maps'] = ptable
        except:
            SystemManager.printWarning('Fail to find %s process' % tid)
            return

        try:
            with open(fpath, 'r') as fd:
                buf = fd.readlines()
        except:
            SystemManager.procInstance[tid]['maps'] = None
            SystemManager.printWarning('Fail to open %s' % fpath)
            return

        # check kernel thread #
        if len(buf) == 0:
            return

        for line in buf:
            d = {}
            tmplist = line.split()

            # memory map info #
            if not line[0].isupper():
                checkCnt = 0

                d['range'] = tmplist[0]
                d['perm'] = tmplist[1]
                d['offset'] = tmplist[2]
                d['devid'] = tmplist[3]
                d['inode'] = tmplist[4]

                if len(tmplist) > 5:
                    ptype = tmplist[5]
                else:
                    ptype = ''

                # shared memory #
                if d['perm'][3] == 's':
                    mtype = 'SHM'
                    stable[ptype] = 0
                # file-mapped memory #
                elif ptype.startswith('/'):
                    mtype = 'FILE'
                    ftable[ptype] = 0
                # anonymous memory #
                elif ptype == '':
                    mtype = 'HEAP'
                # stack memory #
                elif ptype.startswith('[stack'):
                    mtype = 'STACK'
                # anonymous memory #
                elif ptype == '[heap]':
                    mtype = 'HEAP'
                else:
                    mtype = 'ETC'

                try:
                    ptable[mtype]['count'] += 1
                except:
                    ptable[mtype]['count'] = int(1)
            # memory detail info #
            else:
                prop = tmplist[0]
                val = tmplist[1]

                try:
                    if checklist[checkCnt] == prop:
                        checkCnt += 1

                        val = int(val)
                        try:
                            ptable[mtype][prop] += val
                        except:
                            ptable[mtype][prop] = val
                except:
                    pass

        # save the number of mapping #
        ptable['FILE']['count'] = len(ftable)
        ptable['SHM']['count'] = len(stable)

        del buf, ptable, ftable, stable



    def saveProcWchanData(self, path, tid):
        # save wait channel info #
        try:
            self.prevProcData[tid]['wchanFd'].seek(0)
            self.procData[tid]['wchanFd'] = self.prevProcData[tid]['wchanFd']
            wchanBuf = self.procData[tid]['wchanFd'].readlines()
        except:
            try:
                wchanPath = "%s/%s" % (path, 'wchan')
                self.procData[tid]['wchanFd'] = open(wchanPath, 'r')
                wchanBuf = self.procData[tid]['wchanFd'].readlines()

                # fd resource is about to run out #
                if SystemManager.maxFd - 16 < self.procData[tid]['wchanFd'].fileno():
                    self.procData[tid]['wchanFd'].close()
                    self.procData[tid]['wchanFd'] = None
            except:
                SystemManager.printWarning('Fail to open %s' % wchanPath)
                return

        try:
            if wchanBuf[0] == '0':
                self.procData[tid]['wchan'] = 'RUNNING'
            else:
                self.procData[tid]['wchan'] = wchanBuf[0]
        except:
            self.procData[tid]['wchan'] = ''



    def saveProcSchedData(self, path, tid):
        # save sched info #
        try:
            self.prevProcData[tid]['schedFd'].seek(0)
            self.procData[tid]['schedFd'] = self.prevProcData[tid]['schedFd']
            schedBuf = self.procData[tid]['schedFd'].readlines()
        except:
            try:
                schedPath = "%s/%s" % (path, 'schedstat')
                self.procData[tid]['schedFd'] = open(schedPath, 'r')
                schedBuf = self.procData[tid]['schedFd'].readlines()

                # fd resource is about to run out #
                if SystemManager.maxFd - 16 < self.procData[tid]['schedFd'].fileno():
                    self.procData[tid]['schedFd'].close()
                    self.procData[tid]['schedFd'] = None
            except:
                SystemManager.printWarning('Fail to open %s' % schedPath)
                return

        try:
            schedList = schedBuf[0].split()
            self.procData[tid]['execTime'] = float(schedList[0])
            self.procData[tid]['waitTime'] = float(schedList[1])
        except:
            self.procData[tid]['execTime'] = 0
            self.procData[tid]['waitTime'] = 0



    def saveProcStatusData(self, path, tid):
        # save status info #
        try:
            self.prevProcData[tid]['statusFd'].seek(0)
            self.procData[tid]['statusFd'] = self.prevProcData[tid]['statusFd']
            statusBuf = self.procData[tid]['statusFd'].readlines()
        except:
            try:
                statusPath = "%s/%s" % (path, 'status')
                self.procData[tid]['statusFd'] = open(statusPath, 'r')
                statusBuf = self.procData[tid]['statusFd'].readlines()

                # fd resource is about to run out #
                if SystemManager.maxFd - 16 < self.procData[tid]['statusFd'].fileno():
                    self.procData[tid]['statusFd'].close()
                    self.procData[tid]['statusFd'] = None
            except:
                SystemManager.printWarning('Fail to open %s' % statusPath)
                return

        if self.procData[tid]['status'] is None:
            self.procData[tid]['status'] = {}

        for line in statusBuf:
            if line.startswith('VmSwap') or \
                line.startswith('FDSize') or \
                line.startswith('SigCgt') or \
                line.startswith('voluntary_ctxt_switches') or \
                line.startswith('nonvoluntary_ctxt_switches'):
                statusList = line.split(':')
                self.procData[tid]['status'][statusList[0]] = statusList[1].strip()

        # save statm info #
        try:
            statmBuf = None
            self.prevProcData[tid]['statmFd'].seek(0)
            self.procData[tid]['statmFd'] = self.prevProcData[tid]['statmFd']
            statmBuf = self.procData[tid]['statmFd'].readlines()
        except:
            try:
                statmPath = "%s/%s" % (path, 'statm')
                self.procData[tid]['statmFd'] = open(statmPath, 'r')
                statmBuf = self.procData[tid]['statmFd'].readlines()

                # fd resource is about to run out #
                if SystemManager.maxFd - 16 < self.procData[tid]['statmFd'].fileno():
                    self.procData[tid]['statmFd'].close()
                    self.procData[tid]['statmFd'] = None
            except:
                SystemManager.printWarning('Fail to open %s' % statmPath)
                return

        if statmBuf is not None:
            self.procData[tid]['statm'] = statmBuf[0].split()



    def saveProcData(self, path, tid):
        # save stat info #
        try:
            self.prevProcData[tid]['statFd'].seek(0)
            self.procData[tid]['statFd'] = self.prevProcData[tid]['statFd']
            statBuf = self.procData[tid]['statFd'].readlines()[0]
            self.prevProcData[tid]['alive'] = True
        except:
            try:
                statPath = "%s/%s" % (path, 'stat')
                self.procData[tid]['statFd'] = open(statPath, 'r')
                statBuf = self.procData[tid]['statFd'].readlines()[0]

                if tid in self.prevProcData:
                    self.prevProcData[tid]['alive'] = True

                # fd resource is about to run out #
                if SystemManager.maxFd - 16 < self.procData[tid]['statFd'].fileno():
                    self.procData[tid]['statFd'].close()
                    self.procData[tid]['statFd'] = None
            except:
                SystemManager.printWarning('Fail to open %s' % statPath)
                del self.procData[tid]
                return

        # check change of stat #
        self.procData[tid]['statOrig'] = statBuf
        if tid in self.prevProcData and \
            self.prevProcData[tid]['statOrig'] == statBuf:
            self.procData[tid]['stat'] = self.prevProcData[tid]['stat']
            del self.prevProcData[tid]['statOrig']
            self.procData[tid]['changed'] = False
        else:
            # convert string to list #
            statList = statBuf.split()

            # merge comm parts that splited by space #
            commIndex = ConfigManager.statList.index("COMM")
            if statList[commIndex][-1] != ')':
                idx = ConfigManager.statList.index("COMM") + 1
                while 1:
                    tmpStr = str(statList[idx])
                    statList[commIndex] = "%s %s" % (statList[commIndex], tmpStr)
                    statList.pop(idx)
                    if tmpStr.rfind(')') > -1:
                        break

            # convert type of values #
            self.procData[tid]['stat'] = statList
            statList[self.majfltIdx] = long(statList[self.majfltIdx])
            statList[self.utimeIdx] = long(statList[self.utimeIdx])
            statList[self.stimeIdx] = long(statList[self.stimeIdx])
            statList[self.btimeIdx] = long(statList[self.btimeIdx])
            statList[self.cutimeIdx] = long(statList[self.cutimeIdx])
            statList[self.cstimeIdx] = long(statList[self.cstimeIdx])

        # save io info #
        if SystemManager.diskEnable:
            try:
                self.prevProcData[tid]['ioFd'].seek(0)
                self.procData[tid]['ioFd'] = self.prevProcData[tid]['ioFd']
                ioBuf = self.procData[tid]['ioFd'].readlines()
                self.prevProcData[tid]['alive'] = True
            except:
                try:
                    ioPath = "%s/%s" % (path, 'io')
                    self.procData[tid]['ioFd'] = open(ioPath, 'r')
                    ioBuf = self.procData[tid]['ioFd'].readlines()

                    if tid in self.prevProcData:
                        self.prevProcData[tid]['alive'] = True

                    # fd resource is about to run out #
                    if SystemManager.maxFd - 16 < self.procData[tid]['ioFd'].fileno():
                        self.procData[tid]['ioFd'].close()
                        self.procData[tid]['ioFd'] = None
                except:
                    SystemManager.printWarning('Fail to open %s' % ioPath)
                    del self.procData[tid]
                    return

            # parse io usage #
            for line in ioBuf:
                line = line.split()
                if line[0] == 'read_bytes:' or line[0] == 'write_bytes:':
                    try:
                        self.procData[tid]['io'][line[0][:-1]] = long(line[1])
                    except:
                        self.procData[tid]['io'] = {}
                        self.procData[tid]['io'][line[0][:-1]] = long(line[1])



    def printSystemUsage(self):
        try:
            # free memory #
            freeMem = self.vmData['nr_free_pages'] >> 8
            freeMemDiff = (self.vmData['nr_free_pages'] - self.prevVmData['nr_free_pages']) >> 8

            # anonymous memory #
            actAnonMem = self.vmData['nr_active_anon'] >> 8
            inactAnonMem = self.vmData['nr_inactive_anon'] >> 8
            totalAnonMem = self.vmData['nr_anon_pages'] >> 8
            anonMemDiff = (self.vmData['nr_anon_pages'] - self.prevVmData['nr_anon_pages']) >> 8

            # file memory #
            actFileMem = self.vmData['nr_active_file'] >> 8
            inactFileMem = self.vmData['nr_inactive_file'] >> 8
            totalFileMem = self.vmData['nr_file_pages'] >> 8
            fileMemDiff = (self.vmData['nr_file_pages'] - self.prevVmData['nr_file_pages']) >> 8
            nrDirty = self.vmData['nr_dirty']

            # dirty memory #
            dirtyMem = self.vmData['nr_dirty']
            '''
            dirtyRatio = \
                int((self.vmData['nr_dirty'] / float(self.vmData['nr_dirty_threshold'])) * 100)
            dirtyBgRatio = \
                int((self.vmData['nr_dirty'] / float(self.vmData['nr_dirty_background_threshold'])) * 100)
            '''

            # slab memory #
            slabReclm = self.vmData['nr_slab_reclaimable'] >> 8
            slabUnReclm = self.vmData['nr_slab_unreclaimable'] >> 8
            slabReclmDiff = \
                self.vmData['nr_slab_reclaimable'] - self.prevVmData['nr_slab_reclaimable']
            slabUnReclmDiff = \
                self.vmData['nr_slab_unreclaimable'] - self.prevVmData['nr_slab_unreclaimable']
            totalSlabMem = \
                (self.vmData['nr_slab_reclaimable'] + self.vmData['nr_slab_unreclaimable']) >> 8
            slabMemDiff = (slabReclmDiff + slabUnReclmDiff) >> 8

            # fault #
            nrMajFault = self.vmData['pgmajfault'] - self.prevVmData['pgmajfault']
            nrTotalFault = self.vmData['pgfault'] - self.prevVmData['pgfault']
            nrMinFault = nrTotalFault - nrMajFault

            # paged in/out from/to disk #
            pgInMemDiff = (self.vmData['pgpgin'] - self.prevVmData['pgpgin']) >> 10
            pgOutMemDiff = (self.vmData['pgpgout'] - self.prevVmData['pgpgout']) >> 10

            # swap memory #
            swapTotal = self.vmData['swapTotal'] >> 10
            swapUsage = self.vmData['swapUsed'] >> 10
            swapUsageDiff = (self.prevVmData['swapUsed'] - self.vmData['swapUsed']) >> 10
            swapInMem = (self.vmData['pswpin'] - self.prevVmData['pswpin']) >> 10
            swapOutMem = (self.vmData['pswpout'] - self.prevVmData['pswpout']) >> 10

            # background reclaim #
            bgReclaim = 0
            if 'pgsteal_kswapd_normal' in self.vmData:
                bgReclaim += \
                    self.vmData['pgsteal_kswapd_normal'] - self.prevVmData['pgsteal_kswapd_normal']
            if 'pgsteal_kswapd_high' in self.vmData:
                bgReclaim += \
                    self.vmData['pgsteal_kswapd_high'] - self.prevVmData['pgsteal_kswapd_high']
            if 'pgsteal_kswapd_dma' in self.vmData:
                bgReclaim += \
                    self.vmData['pgsteal_kswapd_dma'] - self.prevVmData['pgsteal_kswapd_dma']
            if 'pgsteal_kswapd_dma32' in self.vmData:
                bgReclaim += \
                    self.vmData['pgsteal_kswapd_dma32'] - self.prevVmData['pgsteal_kswapd_dma32']
            if 'pgsteal_kswapd_movable' in self.vmData:
                bgReclaim += \
                    self.vmData['pgsteal_kswapd_movable'] - self.prevVmData['pgsteal_kswapd_movable']
            bgReclaim = bgReclaim >> 8
            nrBgReclaim = self.vmData['pageoutrun'] - self.prevVmData['pageoutrun']

            # direct reclaim #
            drReclaim = 0
            if 'pgsteal_direct_normal' in self.vmData:
                drReclaim += \
                    self.vmData['pgsteal_direct_normal'] - self.prevVmData['pgsteal_direct_normal']
            if 'pgsteal_direct_high' in self.vmData:
                drReclaim += \
                    self.vmData['pgsteal_direct_high'] - self.prevVmData['pgsteal_direct_high']
            if 'pgsteal_direct_dma' in self.vmData:
                drReclaim += \
                    self.vmData['pgsteal_direct_dma'] - self.prevVmData['pgsteal_direct_dma']
            if 'pgsteal_direct_dma32' in self.vmData:
                drReclaim += \
                    self.vmData['pgsteal_direct_dma32'] - self.prevVmData['pgsteal_direct_dma32']
            if 'pgsteal_direct_movable' in self.vmData:
                drReclaim += \
                    self.vmData['pgsteal_direct_movable'] - self.prevVmData['pgsteal_direct_movable']
            drReclaim = drReclaim >> 8
            nrDrReclaim = self.vmData['allocstall'] - self.prevVmData['allocstall']


            # etc #
            nrMlock = self.vmData['nr_mlock']
            #mappedMem = self.vmData['nr_mapped'] >> 8

            nrBlocked = self.cpuData['procs_blocked']['procs_blocked']

            # total mem #
            totalMem = self.memData['MemTotal'] >> 10

            # cma mem #
            if 'CmaTotal' in self.memData:
                cmaTotalMem = self.memData['CmaTotal']

                if 'CmaFree' in self.memData:
                    cmaFreeMem = self.memData['CmaFree']
                else:
                    cmaFreeMem = 0
                if 'CmaDeviceAlloc' in self.memData:
                    cmaDevMem = self.memData['CmaDeviceAlloc']
                else:
                    cmaDevMem = 0
            else:
                cmaTotalMem = 0

            '''
            shMem = self.vmData['nr_shmem'] >> 8
            pageTableMem = self.vmData['nr_page_table_pages'] >> 8
            kernelStackMem = self.vmData['nr_kernel_stack'] * 8 >> 10
            '''
        except:
            SystemManager.printError("Fail to get all system stat")
            return

        # print system status menu #
        SystemManager.addPrint(('%s\n' % twoLine) + \
            ("{0:^7}|{1:^5}({2:^3}/{3:^3}/{4:^3}/{5:^3})|{6:^5}({7:^4}/{8:^4}/{9:^4}/{10:^4})|"\
            "{11:^6}({12:^4}/{13:^7})|{14:^10}|{15:^7}|{16:^7}|{17:^7}|{18:^9}|{19:^7}|{20:^8}|{21:^12}|\n").\
            format("ID", "CPU", "Usr", "Ker", "Blk", "IRQ", "Mem", "Free", "Anon", "File", "Slab",\
            "Swap", "Used", "InOut", "Reclaim", "BlkRW", "NrFlt", "NrBlk", "NrSIRQ", "NrMlk", "NrDrt",\
            "NetIO") + ('%s\n' % oneLine), newline = 3)

        interval = SystemManager.uptimeDiff
        ctxSwc = self.cpuData['ctxt']['ctxt'] - self.prevCpuData['ctxt']['ctxt']
        nrIrq = self.cpuData['intr']['intr'] - self.prevCpuData['intr']['intr']
        nrSoftIrq = self.cpuData['softirq']['softirq'] - self.prevCpuData['softirq']['softirq']

        # get total cpu usage #
        nowData = self.cpuData['all']
        prevData = self.prevCpuData['all']

        userUsage = int(((nowData['user'] - prevData['user'] + nowData['nice'] - prevData['nice']) \
            / SystemManager.nrCore) / interval)
        kerUsage = int(((nowData['system'] - prevData['system']) / SystemManager.nrCore) / interval)
        irqUsage = int(((nowData['irq'] - prevData['irq'] + nowData['softirq'] - prevData['softirq']) \
            / SystemManager.nrCore) / interval)

        ioUsage = 0
        for idx, value in self.cpuData.items():
            try:
                ioUsage += (self.cpuData[int(idx)]['iowait'] - self.prevCpuData[int(idx)]['iowait'])
            except:
                pass
        ioUsage = int((ioUsage / SystemManager.nrCore) / interval)

        totalUsage = int(userUsage + kerUsage + irqUsage)

        # get network usage #
        netIO = '%s/%s' % self.getNetworkUsage(SystemManager.prevNetstat, SystemManager.netstat)

        totalCoreStat = ("{0:<7}|{1:>5}({2:^3}/{3:^3}/{4:^3}/{5:^3})|{6:^5}({7:^4}/{8:^4}/{9:^4}/{10:^4})|" \
            "{11:^6}({12:^4}/{13:^7})|{14:^10}|{15:^7}|{16:^7}|{17:^7}|{18:^9}|{19:^7}|{20:^8}|{21:^12}|\n").\
            format("Total", \
            '%d %%' % totalUsage, userUsage, kerUsage, ioUsage, irqUsage, \
            freeMem, freeMemDiff, anonMemDiff, fileMemDiff, slabMemDiff, \
            swapUsage, swapUsageDiff, '%s/%s' % (swapInMem, swapOutMem), \
            '%s/%s' % (bgReclaim, drReclaim), '%s/%s' % (pgInMemDiff, pgOutMemDiff), \
            nrMajFault, nrBlocked, nrSoftIrq, nrMlock, nrDirty, netIO)

        SystemManager.addPrint(totalCoreStat)

        # save report data #
        if SystemManager.reportEnable:
            self.reportData = {}

            self.reportData['system'] = {}
            self.reportData['system']['pid'] = SystemManager.pid
            self.reportData['system']['uptime'] = SystemManager.uptime
            self.reportData['system']['interval'] = interval
            self.reportData['system']['nrIrq'] = nrIrq
            self.reportData['system']['nrSoftIrq'] = nrSoftIrq

            self.reportData['cpu'] = {}
            self.reportData['cpu']['total'] = totalUsage
            self.reportData['cpu']['user'] = userUsage
            self.reportData['cpu']['kernel'] = kerUsage
            self.reportData['cpu']['irq'] = irqUsage
            self.reportData['cpu']['nrCore'] = SystemManager.nrCore

            self.reportData['mem'] = {}
            self.reportData['mem']['total'] = totalMem
            self.reportData['mem']['free'] = freeMem
            self.reportData['mem']['anon'] = totalAnonMem
            self.reportData['mem']['file'] = totalFileMem
            self.reportData['mem']['slab'] = totalSlabMem
            self.reportData['mem']['dirty'] = dirtyMem
            self.reportData['mem']['freeDiff'] = freeMemDiff
            self.reportData['mem']['anonDiff'] = anonMemDiff
            self.reportData['mem']['fileDiff'] = fileMemDiff
            self.reportData['mem']['slabDiff'] = slabMemDiff
            if cmaTotalMem > 0:
                self.reportData['mem']['cmaTotal'] = cmaTotalMem
                self.reportData['mem']['cmaFree'] = cmaFreeMem
                self.reportData['mem']['cmaDev'] = cmaDevMem

            self.reportData['swap'] = {}
            self.reportData['swap']['total'] = swapTotal
            self.reportData['swap']['usage'] = swapUsage
            self.reportData['swap']['usageDiff'] = swapUsageDiff
            self.reportData['swap']['bgReclaim'] = bgReclaim
            self.reportData['swap']['drReclaim'] = drReclaim

            self.reportData['block'] = {}
            self.reportData['block']['ioWait'] = ioUsage
            self.reportData['block']['read'] = pgInMemDiff
            self.reportData['block']['write'] = pgOutMemDiff
            self.reportData['block']['nrFault'] = nrMajFault

            self.reportData['task'] = {}
            self.reportData['task']['nrBlocked'] = nrBlocked
            self.reportData['task']['nrProc'] = self.nrProcess
            self.reportData['task']['nrThread'] = self.nrThread
            self.reportData['task']['nrCtx'] = ctxSwc

        # print each cpu usage #
        if SystemManager.showAll:
            SystemManager.addPrint('%s\n' % oneLine)

            freqPath = '/sys/devices/system/cpu/cpu'

            for idx, value in sorted(self.cpuData.items(), reverse=False):
                try:
                    nowData = self.cpuData[int(idx)]

                    if not int(idx) in self.prevCpuData:
                        coreStat = "{0:<7}|{1:>5}({2:^3}/{3:^3}/{4:^3}/{5:^3})|".\
                            format("Core/" + str(idx), '- %', '-', '-', '-', '-')
                        SystemManager.addPrint('%s\n' % coreStat)
                        continue

                    prevData = self.prevCpuData[int(idx)]

                    userUsage = int((nowData['user'] - prevData['user'] + \
                        nowData['nice'] - prevData['nice']) / interval)
                    kerUsage = int((nowData['system'] - prevData['system']) / interval)
                    ioUsage = int((nowData['iowait'] - prevData['iowait']) / interval)
                    irqUsage = int((nowData['irq'] - prevData['irq'] + \
                        nowData['softirq'] - prevData['softirq']) / interval)
                    totalUsage = userUsage + kerUsage + irqUsage

                    # limit total usage of each cpus #
                    if totalUsage > 100:
                        totalUsage = 100

                    # limit total usage of each modes #
                    if userUsage > 100:
                        userUsage = 100
                    elif kerUsage > 100:
                        kerUsage = 100

                    coreStat = "{0:<7}|{1:>5}({2:^3}/{3:^3}/{4:^3}/{5:^3})|".\
                        format("Core/%s" % idx, '%s %%' % totalUsage,\
                        userUsage, kerUsage, ioUsage, irqUsage)

                    # get current cpu frequency #
                    curPath = '%s%s/cpufreq/cpuinfo_cur_freq' % (freqPath, idx)
                    try:
                        with open(curPath, 'r') as fd:
                            curFreq = fd.readline()[:-1]
                    except:
                        curFreq = None
                        pass

                    # get min cpu frequency #
                    minPath = '%s%s/cpufreq/cpuinfo_min_freq' % (freqPath, idx)
                    try:
                        with open(minPath, 'r') as fd:
                            minFreq = fd.readline()[:-1]
                    except:
                        minFreq = None
                        pass

                    # get max cpu frequency #
                    maxPath = '%s%s/cpufreq/cpuinfo_max_freq' % (freqPath, idx)
                    try:
                        with open(maxPath, 'r') as fd:
                            maxFreq = fd.readline()[:-1]
                    except:
                        maxFreq = None
                        pass

                    # set frequency info #
                    coreFreq = ''
                    if curFreq is not None:
                        coreFreq = '%d Mhz' % (int(curFreq) >> 10)
                    else:
                        coreFreq = '? Mhz'
                    if minFreq is not None and maxFreq is not None:
                        coreFreq = '%s [%d-%d]' % (coreFreq, int(minFreq) >> 10, int(maxFreq) >> 10)

                    # get length of string #
                    lenTotal = len(totalCoreStat)
                    lenCore = len(coreStat)
                    lenFreq = len(coreFreq)
                    lenLine = len(oneLine) - lenCore - lenFreq - 2

                    # print graph of per-core usage #
                    if totalUsage > 0:
                        coreGraph = '#' * (lenLine * totalUsage / 100)
                        coreGraph += (' ' * (lenLine - len(coreGraph)))
                    else:
                        coreGraph = ' ' * lenLine

                    SystemManager.addPrint('%s%s| %s\n' % (coreStat, coreGraph, coreFreq))
                except:
                    continue



    def printProcUsage(self):
        # calculate diff between previous and now #
        interval = SystemManager.uptimeDiff
        for pid, value in self.procData.items():
            try:
                nowData = value['stat']
                prevData = self.prevProcData[pid]['stat']

                value['runtime'] = int(SystemManager.uptime - (float(nowData[self.starttimeIdx]) / 100))

                if value['io'] is not None:
                    value['read'] = value['io']['read_bytes'] - \
                            self.prevProcData[pid]['io']['read_bytes']
                    value['write'] = value['io']['write_bytes'] - \
                            self.prevProcData[pid]['io']['write_bytes']

                # no changed value #
                if value['changed'] is False:
                    value['utime'] = value['stime'] = value['ttime'] = value['btime'] = value['cttime'] = 0
                    continue

                value['majflt'] = nowData[self.majfltIdx] - prevData[self.majfltIdx]
                value['utime'] = int((nowData[self.utimeIdx] - prevData[self.utimeIdx]) / interval)
                if value['utime'] > 100 and value['stat'][self.nrthreadIdx] == '1':
                    value['utime'] = 100
                value['stime'] = int((nowData[self.stimeIdx] - prevData[self.stimeIdx]) / interval)
                if value['stime'] > 100 and value['stat'][self.nrthreadIdx] == '1':
                    value['stime'] = 100
                value['ttime'] = value['utime'] + value['stime']
                if value['ttime'] > 100 and value['stat'][self.nrthreadIdx] == '1':
                    value['ttime'] = 100
                cutime = int((nowData[self.cutimeIdx] - prevData[self.cutimeIdx]) / interval)
                cstime = int((nowData[self.cstimeIdx] - prevData[self.cstimeIdx]) / interval)
                value['cttime'] = cutime + cstime
                value['btime'] = int((nowData[self.btimeIdx] - prevData[self.btimeIdx]) / interval)
                if value['ttime'] + value['btime'] > 100 and value['stat'][self.nrthreadIdx] == '1':
                    value['btime'] = 100 - value['ttime']
            except:
                value['new'] = True
                value['runtime'] = int(SystemManager.uptime - (float(nowData[self.starttimeIdx]) / 100))
                value['majflt'] = nowData[self.majfltIdx]
                value['utime'] = int(nowData[self.utimeIdx] / interval)
                if value['utime'] > 100 and value['stat'][self.nrthreadIdx] == '1':
                    value['utime'] = 100
                value['stime'] = int(nowData[self.stimeIdx] / interval)
                if value['stime'] > 100 and value['stat'][self.nrthreadIdx] == '1':
                    value['stime'] = 100
                value['ttime'] = value['utime'] + value['stime']
                if value['ttime'] > 100 and value['stat'][self.nrthreadIdx] == '1':
                    value['ttime'] = 100
                cutime = int(nowData[self.cutimeIdx] / interval)
                cstime = int(nowData[self.cstimeIdx] / interval)
                value['cttime'] = cutime + cstime
                value['btime'] = int(nowData[self.btimeIdx] / interval)
                if value['ttime'] + value['btime'] > 100 and value['stat'][self.nrthreadIdx] == '1':
                    value['btime'] = 100 - value['ttime']

                if value['io'] is not None:
                    value['read'] = value['io']['read_bytes']
                    value['write'] = value['io']['write_bytes']

        # get profile mode #
        if SystemManager.processEnable:
            mode = 'Process'
        else:
            mode = 'Thread'

        if SystemManager.wfcEnable is False:
            dprop = 'Dly'
        else:
            dprop = 'WFC'

        if SystemManager.wchanEnable:
            etc = 'WaitChannel'
        else:
            etc = 'SignalHandler'

        SystemManager.addPrint(twoLine + '\n' + \
            ("{0:^16} ({1:^5}/{2:^5}/{3:^4}/{4:>4})| {5:^3}({6:^3}/{7:^3}/{8:^3})| " \
            "{9:>4}({10:^3}/{11:^3}/{12:^3}/{13:^3})| {14:^3}({15:^4}/{16:^4}/{17:^5})|" \
            "{18:^5}|{19:^6}|{20:^4}|{21:>9}|{22:^21}|\n{23:1}\n").\
            format(mode, "ID", "Pid", "Nr", "Pri", "CPU", "Usr", "Ker", dprop, \
            "Mem", "RSS", "Txt", "Shr", "Swp", "Blk", "RD", "WR", "NrFlt",\
            "Yld", "Prmt", "FD", "LifeTime", etc, oneLine), newline = 3)

        # set sort value #
        if SystemManager.sort == 'm':
            sortedProcData = sorted(self.procData.items(), \
                key=lambda e: long(e[1]['stat'][self.rssIdx]), reverse=True)
        elif SystemManager.sort == 'b':
            sortedProcData = sorted(self.procData.items(), \
                key=lambda e: e[1]['btime'], reverse=True)
        elif SystemManager.sort == 'w':
            sortedProcData = sorted(self.procData.items(), \
                key=lambda e: e[1]['cttime'], reverse=True)
        elif SystemManager.sort == 'p':
            sortedProcData = sorted(self.procData.items(), \
                key=lambda e: int(e[0]))
        elif SystemManager.sort == 'n':
            sortedProcData = sorted(self.procData.items(), \
                key=lambda e: e[1]['new'], reverse=True)
        elif SystemManager.sort == 'r':
            sortedProcData = sorted(self.procData.items(), \
                key=lambda e: e[1]['runtime'], reverse=True)
        else:
            # set cpu usage as default #
            sortedProcData = sorted(self.procData.items(), \
                key=lambda e: e[1]['ttime'], reverse=True)

        # print process usage #
        procCnt = 0
        for idx, value in sortedProcData:
            # apply filter #
            if SystemManager.showGroup != []:
                if SystemManager.groupProcEnable:
                    if SystemManager.processEnable:
                        if value['stat'][self.ppidIdx] in SystemManager.showGroup:
                            pass
                        elif idx in SystemManager.showGroup:
                            pass
                        else:
                            continue
                    elif value['mainID'] not in SystemManager.showGroup:
                        continue
                else:
                    if idx in SystemManager.showGroup:
                        pass
                    elif True in [value['stat'][self.commIdx].find(val) >= 0 \
                        for val in SystemManager.showGroup]:
                        pass
                    else:
                        continue

                # add task into stack trace list #
                if SystemManager.stackEnable:
                    try:
                        self.stackTable[idx]
                    except:
                        self.stackTable[idx] = dict()

                    if not 'fd' in self.stackTable[idx]:
                        spath = '/proc/%s/stack' % idx
                        try:
                            self.stackTable[idx]['fd'] = open(spath, 'r')
                            self.stackTable[idx]['stack'] = {}
                            self.stackTable[idx]['total'] = 0
                        except:
                            SystemManager.printWarning("Fail to open %s" % spath)
                            del self.stackTable[idx]

            # cut by rows of terminal #
            if int(SystemManager.bufferRows) >= \
                int(SystemManager.ttyRows) - SystemManager.ttyRowsMargin and \
                SystemManager.printFile is None:
                return

            # set sort value #
            if SystemManager.sort == 'c' or SystemManager.sort is None:
                targetValue = value['ttime']
            elif SystemManager.sort == 'm':
                targetValue = long(value['stat'][self.rssIdx]) >> 8
            elif SystemManager.sort == 'b':
                targetValue = value['btime']
            elif SystemManager.sort == 'w':
                targetValue = value['cttime']
            elif SystemManager.sort == 'p':
                targetValue = idx
            elif SystemManager.sort == 'n':
                targetValue = value['new']
            elif SystemManager.sort == 'r':
                targetValue = value['runtime']

            # check limit #
            if SystemManager.showGroup == [] and \
                SystemManager.showAll is False and \
                targetValue == 0:
                break

            if value['new']:
                comm = '*' + value['stat'][self.commIdx][1:-1]
            else:
                comm = value['stat'][self.commIdx][1:-1]

            if SystemManager.processEnable:
                pid = value['stat'][self.ppidIdx]
            else:
                pid = value['mainID']

            codeSize = (long(value['stat'][self.ecodeIdx]) - \
                long(value['stat'][self.scodeIdx])) >> 20

            if ConfigManager.schedList[int(value['stat'][self.policyIdx])] == 'C':
                schedValue = "%3d" % (int(value['stat'][self.prioIdx]) - 20)
            else:
                schedValue = "%3d" % (abs(int(value['stat'][self.prioIdx]) + 1))

            runtimeSec = value['runtime']
            runtimeMin = runtimeSec / 60
            runtimeHour = runtimeMin / 60
            if runtimeHour > 0:
                runtimeMin %= 60
            runtimeSec %= 60
            lifeTime = "%3d:%2d:%2d" % (runtimeHour, runtimeMin, runtimeSec)

            # save status info to get memory status #
            self.saveProcStatusData(value['taskPath'], idx)

            # save sched info to get delayed time  #
            if SystemManager.wfcEnable is False:
                self.saveProcSchedData(value['taskPath'], idx)

            # save wait channel info  #
            if SystemManager.wchanEnable:
                self.saveProcWchanData(value['taskPath'], idx)

            # save memory map info to get memory details #
            if SystemManager.memEnable:
                ThreadAnalyzer.saveProcSmapsData(value['taskPath'], idx)

            try:
                vmswp = long(value['status']['VmSwap'].split()[0]) >> 10
            except:
                vmswp = '-'
            try:
                shr = long(value['statm'][self.shrIdx]) >> 8
            except:
                shr = '-'

            try:
                value['yield'] = value['status']['voluntary_ctxt_switches']
            except:
                value['yield'] = '-'
            try:
                value['preempted'] = value['status']['nonvoluntary_ctxt_switches']
            except:
                value['preempted'] = '-'

            # save size of file descriptor table #
            try:
                value['fdsize'] = value['status']['FDSize']
            except:
                value['fdsize'] = '-'

            try:
                yld = long(value['yield']) - \
                    long(self.prevProcData[idx]['status']['voluntary_ctxt_switches'])
            except:
                yld = '-'

            try:
                prtd = long(value['preempted']) - \
                    long(self.prevProcData[idx]['status']['nonvoluntary_ctxt_switches'])
            except:
                prtd = '-'

            try:
                execTime = value['execTime'] - self.prevProcData[idx]['execTime']
                waitTime = value['waitTime'] - self.prevProcData[idx]['waitTime']
                execPer = (execTime / (execTime + waitTime)) * 100
                totalTime = value['ttime'] * (100 / execPer)
                dtime = int(totalTime - value['ttime'])
            except:
                dtime = '-'

            if SystemManager.diskEnable:
                readSize = value['read'] >> 20
                writeSize = value['write'] >> 20
            else:
                readSize = '-'
                writeSize = '-'

            if SystemManager.wfcEnable:
                dtime = int(value['cttime'])

            if SystemManager.wchanEnable:
                try:
                    etc = value['wchan']
                except:
                    etc = ''
            else:
                try:
                    etc = value['status']['SigCgt'].lstrip('0')
                except:
                    etc = '-'

            SystemManager.addPrint(\
                ("{0:>16} ({1:>5}/{2:>5}/{3:>4}/{4:>4})| {5:>3}({6:>3}/{7:>3}/{8:>3})| " \
                "{9:>4}({10:>3}/{11:>3}/{12:>3}/{13:>3})| {14:>3}({15:>4}/{16:>4}/{17:>5})|" \
                "{18:>5}|{19:>6}|{20:>4}|{21:>9}|{22:^21}|\n").\
                format(comm, idx, pid, value['stat'][self.nrthreadIdx], \
                ConfigManager.schedList[int(value['stat'][self.policyIdx])] + str(schedValue), \
                value['ttime'], value['utime'], value['stime'], dtime, \
                long(value['stat'][self.vsizeIdx]) >> 20, \
                long(value['stat'][self.rssIdx]) >> 8, codeSize, shr, vmswp, \
                value['btime'], readSize, writeSize, value['majflt'],\
                yld, prtd, value['fdsize'], lifeTime, etc))

            if SystemManager.memEnable:
                if value['maps'] is not None:
                    for key, item in sorted(value['maps'].items(), reverse=True):
                        tmpstr = ''

                        if len(item) == 0 or item['count'] == 0:
                            continue

                        try:
                            prop = 'Size:'
                            tmpstr = "%s%s%4sM / " % (tmpstr, prop.upper(), item[prop] >> 10)
                        except:
                            tmpstr = "%s%s%4sM / " % (tmpstr, prop.upper(), 0)

                        try:
                            prop = 'Rss:'
                            tmpstr = "%s%s%4sM / " % (tmpstr, prop.upper(), item[prop] >> 10)
                        except:
                            tmpstr = "%s%s%4sM / " % (tmpstr, prop.upper(), 0)

                        try:
                            prop = 'Pss:'
                            tmpstr = "%s%s%4sM / " % (tmpstr, prop.upper(), item[prop] >> 10)
                        except:
                            tmpstr = "%s%s%4sM / " % (tmpstr, prop.upper(), 0)

                        try:
                            prop = 'Swap:'
                            tmpstr = "%s%s%4sM / " % (tmpstr, prop.upper(), item[prop] >> 10)
                        except:
                            tmpstr = "%s%s%4sM / " % (tmpstr, prop.upper(), 0)

                        try:
                            prop = 'AnonHugePages:'
                            tmpstr = "%s%s:%4sM / " % (tmpstr, 'HUGE', item[prop] >> 10)
                        except:
                            tmpstr = "%s%s:%4sM / " % (tmpstr, 'HUGE', 0)

                        try:
                            prop = 'Locked:'
                            tmpstr = "%s%s%4sK / " % (tmpstr, prop.upper(), item[prop])
                        except:
                            tmpstr = "%s%s%4sK / " % (tmpstr, prop.upper(), 0)

                        try:
                            prop = 'Shared_Dirty:'
                            if item[prop] > 9999:
                                item[prop] = item[prop] >> 10
                                tmpstr = "%s%s:%4sM / " % (tmpstr, 'SDIRTY', item[prop])
                            else:
                                tmpstr = "%s%s:%4sK / " % (tmpstr, 'SDIRTY', item[prop])
                        except:
                            tmpstr = "%s%s:%4sK / " % (tmpstr, 'SDIRTY', 0)

                        try:
                            prop = 'Private_Dirty:'
                            if item[prop] > 9999:
                                item[prop] = item[prop] >> 10
                                tmpstr = "%s%s:%4sM" % (tmpstr, 'PDIRTY', item[prop])
                            else:
                                tmpstr = "%s%s:%4sK" % (tmpstr, 'PDIRTY', item[prop])
                        except:
                            tmpstr = "%s%s:%4sK" % (tmpstr, 'PDIRTY', 0)

                        mtype = '(%s)[%s]' % (item['count'], key)
                        SystemManager.addPrint("{0:>39} | {1:1}\n".format(mtype, tmpstr))

                        # cut by rows of terminal #
                        if int(SystemManager.bufferRows) >= \
                            int(SystemManager.ttyRows) - SystemManager.ttyRowsMargin and \
                            SystemManager.printFile is None:
                            return

                SystemManager.addPrint(oneLine + '\n')

            if SystemManager.stackEnable:
                # set indent size including arrow #
                initIndent = 42
                indent = initIndent + 3

                try:
                    for stack, cnt in sorted(self.stackTable[idx]['stack'].items(), \
                        key=lambda e: e[1], reverse=True):

                        line = ''
                        fullstack = ''
                        per = int((cnt / float(self.stackTable[idx]['total'])) * 100)
                        self.stackTable[idx]['stack'][stack] = 0

                        if per == 0:
                            continue

                        for call in stack.split('\n'):
                            try:
                                astack = call.split()[1]

                                if astack.startswith('0xffffffff'):
                                    if fullstack == line == '':
                                        line = 'None'
                                    else:
                                        line = line[:line.rfind('<-')]
                                    break

                                if len(line) + len(astack) + indent >= SystemManager.lineLength:
                                    indent = 0
                                    fullstack = '%s%s\n' % (fullstack, line)
                                    line = ' ' * initIndent

                                line = '%s%s <- ' % (line, astack)
                            except:
                                pass

                        fullstack = '%s%s' % (fullstack, line)

                        SystemManager.addPrint("{0:>38}% | {1:1}\n".format(per, fullstack))
                except:
                    pass

                try:
                    if self.stackTable[idx]['total'] == 0:
                        SystemManager.addPrint("{0:>39} | {1:1}\n".format('', 'None'))
                    else:
                        self.stackTable[idx]['total'] = 0
                    SystemManager.addPrint(oneLine + '\n')
                except:
                    pass

            procCnt += 1

        if procCnt == 0:
            SystemManager.addPrint("{0:^16}\n{1:1}\n".format('None', oneLine))
        elif SystemManager.memEnable or SystemManager.stackEnable:
            pass
        else:
            SystemManager.addPrint(oneLine + '\n')

        self.printNewProcess()
        self.printDieProcess()



    def printNewProcess(self):
        newCnt = 0
        for idx, value in sorted(self.procData.items(), key=lambda e: e[1]['new'], reverse=True):
            if value['new']:
                comm = ('%s%s' % ('[+]', value['stat'][self.commIdx][1:-1]))[:16]

                if SystemManager.processEnable:
                    pid = value['stat'][self.ppidIdx]
                else:
                    pid = value['mainID']

                codeSize = (long(value['stat'][self.ecodeIdx]) - \
                    long(value['stat'][self.scodeIdx])) >> 20

                if ConfigManager.schedList[int(value['stat'][self.policyIdx])] == 'C':
                    schedValue = "%3d" % (int(value['stat'][self.prioIdx]) - 20)
                else:
                    schedValue = "%3d" % (abs(int(value['stat'][self.prioIdx]) + 1))

                runtimeSec = value['runtime'] + SystemManager.uptimeDiff
                runtimeMin = runtimeSec / 60
                runtimeHour = runtimeMin / 60
                if runtimeHour > 0:
                    runtimeMin %= 60
                runtimeSec %= 60
                lifeTime = "%3d:%2d:%2d" % (runtimeHour, runtimeMin, runtimeSec)

                try:
                    vmswp = long(value['status']['VmSwap'].split()[0]) >> 10
                except:
                    vmswp = '-'
                try:
                    shr = long(value['statm'][self.shrIdx]) >> 8
                except:
                    shr = '-'

                if SystemManager.diskEnable:
                    readSize = value['read'] >> 20
                    writeSize = value['write'] >> 20
                else:
                    readSize = '-'
                    writeSize = '-'

                # print new thread information #
                SystemManager.addPrint(\
                    ("{0:>16} ({1:>5}/{2:>5}/{3:>4}/{4:>4})| {5:>3}({6:>3}/{7:>3}/{8:>3})| " \
                    "{9:>4}({10:>3}/{11:>3}/{12:>3}/{13:>3})| {14:>3}({15:>4}/{16:>4}/{17:>5})|" \
                    "{18:>5}|{19:>6}|{20:>4}|{21:>9}|{22:^21}|\n").\
                    format(comm, idx, pid, value['stat'][self.nrthreadIdx], \
                    ConfigManager.schedList[int(value['stat'][self.policyIdx])] + str(schedValue), \
                    int(value['ttime']), int(value['utime']), int(value['stime']), '-', \
                    long(value['stat'][self.vsizeIdx]) >> 20, \
                    long(value['stat'][self.rssIdx]) >> 8, codeSize, shr, vmswp, \
                    int(value['btime']), readSize, writeSize, value['majflt'],\
                    '-', '-', '-', lifeTime, '-'))
                newCnt += 1

            else:
                if newCnt > 0:
                    SystemManager.addPrint(oneLine + '\n')
                break

            # cut by rows of terminal #
            if SystemManager.printFile is None and \
                int(SystemManager.bufferRows) >= \
                int(SystemManager.ttyRows) - SystemManager.ttyRowsMargin - 2:
                return



    def printDieProcess(self):
        dieCnt = 0
        for idx, value in sorted(\
            self.prevProcData.items(), key=lambda e: e[1]['alive'], reverse=False):

            if value['alive'] is False:
                comm = ('%s%s' % ('[-]', value['stat'][self.commIdx][1:-1]))[:16]

                if SystemManager.processEnable:
                    pid = value['stat'][self.ppidIdx]
                else:
                    pid = value['mainID']

                codeSize = (long(value['stat'][self.ecodeIdx]) - \
                    long(value['stat'][self.scodeIdx])) >> 20

                if ConfigManager.schedList[int(value['stat'][self.policyIdx])] == 'C':
                    schedValue = "%3d" % (int(value['stat'][self.prioIdx]) - 20)
                else:
                    schedValue = "%3d" % (abs(int(value['stat'][self.prioIdx]) + 1))

                runtimeSec = value['runtime'] + SystemManager.uptimeDiff
                runtimeMin = runtimeSec / 60
                runtimeHour = runtimeMin / 60
                if runtimeHour > 0:
                    runtimeMin %= 60
                runtimeSec %= 60
                lifeTime = "%3d:%2d:%2d" % (runtimeHour, runtimeMin, runtimeSec)

                try:
                    vmswp = long(value['status']['VmSwap'].split()[0]) >> 10
                except:
                    vmswp = '-'
                try:
                    shr = long(value['statm'][self.shrIdx]) >> 8
                except:
                    shr = '-'

                if SystemManager.diskEnable:
                    readSize = value['read'] >> 20
                    writeSize = value['write'] >> 20
                else:
                    readSize = '-'
                    writeSize = '-'

                # print terminated thread information #
                SystemManager.addPrint(\
                    ("{0:>16} ({1:>5}/{2:>5}/{3:>4}/{4:>4})| {5:>3}({6:>3}/{7:>3}/{8:>3})| " \
                    "{9:>4}({10:>3}/{11:>3}/{12:>3}/{13:>3})| {14:>3}({15:>4}/{16:>4}/{17:>5})|" \
                    "{18:>5}|{19:>6}|{20:>4}|{21:>9}|{22:^21}|\n").\
                    format(comm, idx, pid, value['stat'][self.nrthreadIdx], \
                    ConfigManager.schedList[int(value['stat'][self.policyIdx])] + str(schedValue), \
                    int(value['ttime']), int(value['utime']), int(value['stime']), '-', \
                    long(value['stat'][self.vsizeIdx]) >> 20, \
                    long(value['stat'][self.rssIdx]) >> 8, codeSize, shr, vmswp, \
                    int(value['btime']), readSize, writeSize, value['majflt'],\
                    '-', '-', '-', lifeTime, '-'))
                dieCnt += 1

                # close fd that thread who already termiated created because of limited resource #
                try:
                    if value['statFd'] is not None:
                        value['statFd'].close()
                except:
                    pass
                try:
                    if value['statusFd'] is not None:
                        value['statusFd'].close()
                except:
                    pass
                try:
                    if value['statmFd'] is not None:
                        value['statmFd'].close()
                except:
                    pass
                try:
                    if value['ioFd'] is not None:
                        value['ioFd'].close()
                except:
                    pass
            else:
                if dieCnt > 0:
                    SystemManager.addPrint(oneLine + '\n')
                return

            # cut by rows of terminal #
            if SystemManager.printFile is None and \
                int(SystemManager.bufferRows) >= \
                int(SystemManager.ttyRows) - SystemManager.ttyRowsMargin - 2:
                return



    def printReportStat(self, reportStat):
        if reportStat is None or type(reportStat) is not dict:
            SystemManager.printWarning("Fail to recognize report data")
            return

        printBuf = twoLine + '\n'

        if 'event' in reportStat:
            for event, proc in reportStat['event'].items():
                printBuf += '[event] (%s)\n' % (event)

                for rank, stat in sorted(proc.items(), key=lambda e: int(e[0]), reverse=False):
                    printBuf += '[%s] ' % (rank)

                    for item, val in stat.items():
                        printBuf += '(%s: %s) ' % (item, val)

                    printBuf += '\n'

                printBuf += oneLine + '\n'

            del reportStat['event']

        for idx, stat in reportStat.items():
            printBuf += '[%s] ' % idx

            for item, val in sorted(stat.items(), reverse=False):
                printBuf += '(%s: %s) ' % (item, val)

            printBuf += '\n'

        printBuf += twoLine + '\n'

        SystemManager.pipePrint(printBuf)



    def replyService(self, ip, port):
        if SystemManager.addrOfServer is None:
            SystemManager.printError("Fail to use server because it is not initialized")
            return

        # send reply message to server #
        message = 'ACK'
        SystemManager.addrAsServer.sendto(message, ip, port)



    def handleServerResponse(self, packet):
        # return by interrupt from recv #
        if packet is False or packet is None:
            sys.exit(0)

        if type(packet) is tuple:
            data = packet[0]
            addr = packet[1]
        else:
            return

        if type(data) is not str:
            SystemManager.printError("Fail to recognize data from server")
            return

        # get address info from server #
        try:
            ip = addr[0]
            port = int(addr[1])
        except:
            SystemManager.printError("Fail to recognize address from server")

        # wrong request from client #
        if SystemManager.addrOfServer == 'NONE' and data in ThreadAnalyzer.requestType:
            SystemManager.printError("Fail to handle %s request from client" % data)
            return

        # reply ACK to server #
        try:
            self.replyService(ip, port)
        except:
            SystemManager.printError("Fail to send ACK to server")

        # REPORT service #
        if data[0] == '{':
            if SystemManager.jsonObject is None:
                try:
                    import json
                    SystemManager.jsonObject = json
                except ImportError:
                    err = sys.exc_info()[1]
                    SystemManager.printError("Fail to import package: " + err.args[0])

            # convert report data to dictionary type #
            reportStat = SystemManager.makeJsonDict(data)

            # print report data #
            self.printReportStat(reportStat)
        # REFUSE response #
        elif data == 'REFUSE':
            SystemManager.printError("Fail to request service because of no support from server")
            sys.exit(0)
        # PRINT service #
        else:
            if SystemManager.printFile is None:
                SystemManager.printTitle()

            # realtime mode #
            if SystemManager.printFile is None:
                SystemManager.pipePrint(data)
                SystemManager.clearPrint()
            # buffered mode #
            else:
                SystemManager.procBuffer.insert(0, data)
                SystemManager.procBufferSize += len(data)
                SystemManager.clearPrint()

                while SystemManager.procBufferSize > int(SystemManager.bufferSize) * 10:
                    if len(SystemManager.procBuffer) == 1:
                        break
                    SystemManager.procBufferSize -= len(SystemManager.procBuffer[-1])
                    SystemManager.procBuffer.pop(-1)



    def requestService(self):
        if SystemManager.addrOfServer is None or SystemManager.addrAsServer is None:
            SystemManager.addrOfServer = None
            return

        try:
            # set non-block socket #
            SystemManager.addrAsServer.socket.setblocking(1)

            if SystemManager.addrOfServer is not 'NONE':
                # send request to server #
                SystemManager.addrAsServer.sendto(\
                    SystemManager.addrOfServer.request, \
                    SystemManager.addrOfServer.ip, \
                    SystemManager.addrOfServer.port)

            SystemManager.printStatus("wait for response from server")
        except:
            SystemManager.printError("Fail to send request '%s'" % SystemManager.addrOfServer.request)



    def checkServer(self):
        if SystemManager.addrAsServer is None:
            return

        # get message from clients #
        ret = SystemManager.addrAsServer.recv()

        # verify request type #
        if ret is False:
            SystemManager.addrAsServer = None
            return
        elif ret is None:
            return

        # handle request #
        if type(ret) is tuple and type(ret[0]) is str:
            message = ret[0]

            try:
                ip = ret[1][0]
                port = ret[1][1]
            except:
                SystemManager.printWarning("Fail to get ip address of client from message")
                return

            networkObject = NetworkManager('client', ip, port)
            if networkObject.ip is None:
                return

            if message == 'PRINT':
                index = ip + ':' + str(port)
                if not index in SystemManager.addrListForPrint:
                    SystemManager.addrListForPrint[index] = networkObject
                    SystemManager.printInfo("registered %s:%d as remote output address" % (ip, port))
                else:
                    SystemManager.printWarning("Duplicated %s:%d as remote output address" % (ip, port))
            elif message == 'REPORT_ALWAYS' or message == 'REPORT_BOUND':
                if SystemManager.reportEnable is False:
                    SystemManager.printWarning(\
                        "Ignored %s request from %s:%d because no report service" % (message, ip, port))
                    networkObject.send("REFUSE")
                    del networkObject
                    return

                networkObject.request = message

                index = ip + ':' + str(port)
                if not index in SystemManager.addrListForReport:
                    SystemManager.addrListForReport[index] = networkObject
                    SystemManager.printInfo("registered %s:%d as remote report address" % (ip, port))
                else:
                    SystemManager.addrListForReport[index] = networkObject
                    SystemManager.printInfo("updated %s:%d as remote report address" % (ip, port))
            elif message == 'ACK':
                index = ip + ':' + str(port)
                if index in SystemManager.addrListForPrint:
                    SystemManager.addrListForPrint[index].ignore -= 1
                    SystemManager.addrListForPrint[index].status = 'READY'
                elif index in SystemManager.addrListForReport:
                    SystemManager.addrListForReport[index].ignore -= 1
                    SystemManager.addrListForReport[index].status = 'READY'
                else:
                    SystemManager.printWarning("Fail to find %s:%d as remote report address" % (ip, port))
            # wrong request or just data from server #
            else:
                SystemManager.printError("Fail to request wrong service %s" % message)



    def reportSystemStat(self):
        if SystemManager.reportEnable is False:
            return

        # initialize report event list #
        # CPU_INTENSIVE, MEM_PRESSURE, SWAP_PRESSURE, IO_INTENSIVE, DISK_FULL, ... #
        self.reportData['event'] = {}

        # check image created #
        if SystemManager.imagePath is not None:
            self.reportData['event']['IMAGE_CREATED'] = SystemManager.imagePath
            SystemManager.imagePath = None

        # analyze cpu status #
        if 'cpu' in self.reportData:
            if ThreadAnalyzer.reportBoundary['cpu']['total'] < self.reportData['cpu']['total']:
                self.reportData['event']['CPU_INTENSIVE'] = {}

                rank = 1
                sortedProcData = sorted(self.procData.items(), \
                    key=lambda e: e[1]['ttime'], reverse=True)

                for pid, data in sortedProcData:
                    if data['ttime'] > 0:
                        evtdata = self.reportData['event']['CPU_INTENSIVE']
                        evtdata[rank] = {}
                        evtdata[rank]['pid'] = pid
                        evtdata[rank]['comm'] = data['stat'][self.commIdx][1:-1]
                        evtdata[rank]['ttime'] = data['ttime']
                        evtdata[rank]['utime'] = data['utime']
                        evtdata[rank]['stime'] = data['stime']

                        rank += 1
                    else:
                        break

        # analyze memory status #
        if 'mem' in self.reportData:
            if ThreadAnalyzer.reportBoundary['mem']['free'] > self.reportData['mem']['free']:
                self.reportData['event']['MEM_PRESSURE'] = {}

                rank = 1
                sortedProcData = sorted(self.procData.items(), \
                    key=lambda e: long(e[1]['stat'][self.rssIdx]), reverse=True)

                for pid, data in sortedProcData:
                    rss = long(data['stat'][self.rssIdx]) >> 8

                    if  rss > 0 and rank < 10:
                        text = (long(data['stat'][self.ecodeIdx]) - \
                            long(data['stat'][self.scodeIdx])) >> 20

                        evtdata = self.reportData['event']['MEM_PRESSURE']
                        evtdata[rank] = {}
                        evtdata[rank]['pid'] = pid
                        evtdata[rank]['comm'] = data['stat'][self.commIdx][1:-1]
                        evtdata[rank]['rss'] = rss
                        evtdata[rank]['text'] = text

                        try:
                            self.reportData['event']['MEM_PRESSURE'][rank]['swap'] = \
                                long(data['status']['VmSwap'].split()[0]) >> 10
                        except:
                            pass

                        try:
                            self.reportData['event']['MEM_PRESSURE'][rank]['shared'] = \
                                long(data['statm'][self.shrIdx]) >> 8
                        except:
                            pass

                        rank += 1
                    else:
                        break

        # analyze swap status #
        if 'swap' in self.reportData and self.reportData['swap']['total'] > 0:
            swapUsagePer = \
                int(self.reportData['swap']['usage'] / float(self.reportData['swap']['total']) * 100)

            if ThreadAnalyzer.reportBoundary['swap']['usage'] < swapUsagePer:
                self.reportData['event']['SWAP_PRESSURE'] = {}

                rank = 1
                sortedProcData = sorted(self.procData.items(), \
                    key=lambda e: long(e[1]['stat'][self.rssIdx]), reverse=True)

                for pid, data in sortedProcData:
                    rss = long(data['stat'][self.rssIdx]) >> 8

                    if  rss > 0 and rank < 10:
                        text = (long(data['stat'][self.ecodeIdx]) - \
                            long(data['stat'][self.scodeIdx])) >> 20

                        evtdata = self.reportData['event']['SWAP_PRESSURE']
                        evtdata[rank] = {}
                        evtdata[rank]['pid'] = pid
                        evtdata[rank]['comm'] = data['stat'][self.commIdx][1:-1]
                        evtdata[rank]['rss'] = rss
                        evtdata[rank]['text'] = text

                        try:
                            self.reportData['event']['SWAP_PRESSURE'][rank]['swap'] = \
                                long(data['status']['VmSwap'].split()[0]) >> 10
                        except:
                            pass

                        try:
                            self.reportData['event']['SWAP_PRESSURE'][rank]['shared'] = \
                                long(data['statm'][self.shrIdx]) >> 8
                        except:
                            pass

                        rank += 1
                    else:
                        break

        # analyze block status #
        if 'block' in self.reportData:
            if ThreadAnalyzer.reportBoundary['block']['ioWait'] < self.reportData['block']['ioWait']:
                self.reportData['event']['IO_INTENSIVE'] = {}

                rank = 1
                sortedProcData = sorted(self.procData.items(), \
                    key=lambda e: e[1]['btime'], reverse=True)

                for pid, data in sortedProcData:
                    if data['btime'] > 0:
                        evtdata = self.reportData['event']['IO_INTENSIVE']
                        evtdata[rank] = {}
                        evtdata[rank]['pid'] = pid
                        evtdata[rank]['comm'] = data['stat'][self.commIdx][1:-1]
                        evtdata[rank]['btime'] = data['btime']

                        rank += 1
                    else:
                        break

        # analyze system status #
        if 'system' in self.reportData:
            pass

        # analyze task status #
        if 'task' in self.reportData:
            pass

        # get event number #
        nrReason = len(self.reportData['event'])

        # print system status to file #
        if SystemManager.reportFileEnable and \
            SystemManager.printFile is not None and \
            nrReason > 0:

            # submit summarized report #
            ThreadAnalyzer.printIntervalUsage()

            # sync and close output file #
            if SystemManager.fileForPrint is not None:
                try:
                    SystemManager.fileForPrint.close()
                except:
                    pass
                SystemManager.fileForPrint = None

            # make output path #
            filePath = os.path.dirname(SystemManager.inputFile) + '/guider'
            for event in self.reportData['event'].keys():
                filePath += '_' + event
            filePath += '_' + str(long(SystemManager.uptime)) + '.out'

            try:
                # rename output file #
                os.rename(SystemManager.inputFile, filePath)
                SystemManager.printStatus(\
                    "saved top usage by report event into %s successfully" % filePath)
            except:
                SystemManager.printWarning(\
                    "Fail to rename %s to %s" % SystemManager.inputFile, filePath)

        # convert dict data to json data #
        jsonObj = SystemManager.makeJsonString(self.reportData)
        if jsonObj is None:
            SystemManager.printWarning("Fail to convert report data to json type")
            return

        # report system status to file #
        if SystemManager.reportPath is not None:
            ret = SystemManager.writeJsonObject(jsonObj)

        # report system status to socket #
        for addr, cli in SystemManager.addrListForReport.items():
            if cli.request == 'REPORT_ALWAYS' or nrReason > 0:
                if cli.status == 'SENT' and cli.ignore > 1:
                    SystemManager.printWarning(\
                        "Stop to send data for report to %s:%d because of no response" % \
                        (cli.ip, cli.port))
                    del SystemManager.addrListForReport[addr]
                else:
                    ret = cli.send(jsonObj)
                    if ret is False:
                        del SystemManager.addrListForReport[addr]
                    else:
                        cli.ignore += 1



    def printSystemStat(self):
        SystemManager.addPrint(\
            ("\n[Top Info] [Time: %7.3f] [Interval: %.1f] [Ctxt: %d] [Fork: %d] " \
            "[IRQ: %d] [Core: %d] [Task: %d/%d] [RAM: %d] [Swap: %d] [Unit: %%/MB]\n") % \
            (SystemManager.uptime, SystemManager.uptimeDiff, \
            self.cpuData['ctxt']['ctxt'] - self.prevCpuData['ctxt']['ctxt'], \
            self.cpuData['processes']['processes'] - self.prevCpuData['processes']['processes'], \
            self.cpuData['intr']['intr'] - self.prevCpuData['intr']['intr'], \
            SystemManager.nrCore, self.nrProcess, self.nrThread, \
            self.memData['MemTotal'] >> 10, self.memData['SwapTotal'] >> 10))

        # print system usage #
        self.printSystemUsage()

        # print process info #
        self.printProcUsage()

        # send packet to remote server #
        if len(SystemManager.addrListForPrint) > 0:
            for addr, cli in SystemManager.addrListForPrint.items():
                if cli.status == 'SENT' and cli.ignore > 1:
                    SystemManager.printWarning(\
                        "Stop to send data for print to %s:%d because of no response" % \
                        (cli.ip, cli.port))
                    del SystemManager.addrListForPrint[addr]
                else:
                    ret = cli.send(SystemManager.bufferString)
                    if ret is False:
                        del SystemManager.addrListForPrint[addr]
                    else:
                        cli.ignore += 1

        # realtime mode #
        if SystemManager.printFile is None:
            SystemManager.pipePrint(SystemManager.bufferString)
            SystemManager.clearPrint()
        # buffered mode #
        else:
            SystemManager.procBuffer[:0] = [SystemManager.bufferString]
            SystemManager.procBufferSize += len(SystemManager.bufferString)
            SystemManager.clearPrint()

            while SystemManager.procBufferSize > int(SystemManager.bufferSize) * 10:
                if len(SystemManager.procBuffer) == 1:
                    break
                SystemManager.procBufferSize -= len(SystemManager.procBuffer[-1])
                SystemManager.procBuffer.pop(-1)





if __name__ == '__main__':

    oneLine = "-" * SystemManager.lineLength
    twoLine = "=" * SystemManager.lineLength

    SystemManager.printOptions()

    SystemManager.inputFile = sys.argv[1]
    SystemManager.outputFile = None

    # set error logger #
    SystemManager.setErrorLogger()

    # set comm #
    SystemManager.setComm()

    # save pid #
    SystemManager.pid = os.getpid()

    # print backgroud process list #
    if SystemManager.isListMode():
        SystemManager.printBackgroundProcs()
        sys.exit(0)

    # make list for arguments #
    if len(sys.argv) > 2:
        argList = sys.argv[2:]
    else:
        argList = None

    # send start / stop signal to background process #
    if SystemManager.isStartMode() or SystemManager.isStopMode():
        SystemManager.sendSignalProcs(signal.SIGINT, argList)
        sys.exit(0)

    # send event signal to background process #
    if SystemManager.isSendMode():
        sig = signal.SIGQUIT
        if argList is not None:
            sigList = [item for item in argList if item.startswith('-')]
            if len(sigList) > 0:
                for val in sigList:
                    try:
                        sig = abs(int(val))
                        del argList[argList.index(val)]
                        break
                    except:
                        pass
        SystemManager.sendSignalProcs(sig, argList)
        sys.exit(0)

    # view system resource status #
    if SystemManager.isViewMode():
        pid = SystemManager.getOption('g')
        addr = SystemManager.getOption('I')

        if pid is None:
            SystemManager.printError("Fail to recognize pid, use also -g option")
        elif addr is None:
            SystemManager.printError("Fail to recognize address, use also -I option")
        else:
            PageAnalyzer.getPageInfo(pid, addr)

        sys.exit(0)

    # parse recording option #
    if SystemManager.isRecordMode():
        if sys.platform.startswith('linux') is False:
            print('[Error] Fail to record because this platform is not linux')
            sys.exit(0)

        # update record status #
        SystemManager.recordStatus = True
        SystemManager.inputFile = '/sys/kernel/debug/tracing/trace'

        # set this process to RT priority #
        SystemManager.setRtPriority('90')

        # set arch #
        SystemManager.setArch(SystemManager.getArch())

        # save system information #
        si = SystemManager()

        SystemManager.parseRecordOption()

        SystemManager.printRecordOption()

        SystemManager.printRecordCmd()

        # run in background #
        if SystemManager.backgroundEnable:
            pid = os.fork()

            if pid > 0:
                sys.exit(0)
            else:
                SystemManager.pid = os.getpid()
                SystemManager.printStatus("background running as process %s" % SystemManager.pid)

        # wait for signal #
        if SystemManager.waitEnable:
            SystemManager.printStatus("wait for starting profile... [ START(ctrl + c) ]")
            signal.signal(signal.SIGINT, SystemManager.defaultHandler)
            signal.signal(signal.SIGQUIT, SystemManager.defaultHandler)
            signal.pause()

        if SystemManager.isSystemMode():
            # save system info and write it to buffer #
            si.saveAllInfo()
            si.printAllInfoToBuf()

            # parse all options and make output file path #
            SystemManager.parseAnalOption()

            if SystemManager.printFile is not None:
                SystemManager.outputFile = SystemManager.printFile + '/guider.out'
            elif SystemManager.outputFile is not None:
                SystemManager.printFile = \
                    SystemManager.outputFile[:SystemManager.outputFile.rfind('/')]

            # get and remove process tree from data file #
            SystemManager.getProcTreeInfo()

            SystemManager.printTitle()

            # print system information #
            SystemManager.pipePrint(SystemManager.systemInfoBuffer)

            # close pipe for less util #
            if SystemManager.pipeForPrint is not None:
                SystemManager.pipeForPrint.close()

            sys.exit(0)

        # set signal #
        if SystemManager.repeatCount > 0 and SystemManager.repeatInterval > 0 and \
            SystemManager.isThreadMode():
            signal.signal(signal.SIGALRM, SystemManager.alarmHandler)
            signal.signal(signal.SIGINT, SystemManager.stopHandler)
            signal.alarm(SystemManager.repeatInterval)

            if SystemManager.outputFile is None:
                SystemManager.printError("wrong option with -s, input also path to save data")
                sys.exit(0)
        else:
            SystemManager.repeatInterval = 0
            SystemManager.repeatCount = 0
            signal.signal(signal.SIGINT, SystemManager.stopHandler)
            signal.signal(signal.SIGQUIT, SystemManager.newHandler)

        SystemManager.printStatus(r'start recording... [ STOP(ctrl + c), MARK(ctrl + \) ]')

        # create FileAnalyzer #
        if SystemManager.isFileMode():
            # check permission #
            if os.geteuid() != 0:
                SystemManager.printError("Fail to get root permission")
                sys.exit(0)

            # parse analysis option #
            SystemManager.parseAnalOption()

            # start file profiling #
            pi = FileAnalyzer()

            # save system info and write it to buffer #
            si.saveAllInfo()
            si.printAllInfoToBuf()

            # get and remove process tree from data file #
            SystemManager.getProcTreeInfo()

            # print total file usage per process #
            if SystemManager.intervalEnable == 0:
                pi.printUsage()
            # print file usage per process on timeline #
            else:
                pi.printIntervalInfo()

            # close pipe for less util #
            if SystemManager.pipeForPrint is not None:
                SystemManager.pipeForPrint.close()

            sys.exit(0)

        # register exit handler #
        atexit.register(SystemManager.runRecordStopCmd)

        # start recording #
        si.runRecordStartCmd()

        # run user command after starting recording #
        SystemManager.writeRecordCmd('AFTER')

        if SystemManager.pipeEnable:
            if SystemManager.outputFile is not None:
                SystemManager.copyPipeToFile(\
                    '%s%s' % (SystemManager.inputFile, '_pipe'), SystemManager.outputFile)
            else:
                SystemManager.printError("wrong option with -e + p, use also -s option to save data")

            sys.exit(0)

        # get init time from buffer for verification #
        if SystemManager.graphEnable is False:
            initTime = ThreadAnalyzer.getInitTime(SystemManager.inputFile)

        # enter loop to record and save data periodically #
        while SystemManager.repeatInterval > 0:
            if SystemManager.repeatCount == 0:
                sys.exit(0)

            # get init time in buffer for verification #
            initTime = ThreadAnalyzer.getInitTime(SystemManager.inputFile)

            # wait for timer #
            signal.pause()

            # compare init time with now time for buffer verification #
            if initTime < ThreadAnalyzer.getInitTime(SystemManager.inputFile):
                SystemManager.printError("buffer size is not enough (%s KB) to profile" % \
                    SystemManager.getBufferSize())
                sys.exit(0)
            else:
                SystemManager.clearTraceBuffer()

        # wait for user input #
        while 1:
            if SystemManager.recordStatus:
                SystemManager.condExit = True
                signal.pause()
                if SystemManager.condExit:
                    break
            else:
                break

        if SystemManager.graphEnable is False:
            # compare init time with now time for buffer verification #
            if initTime < ThreadAnalyzer.getInitTime(SystemManager.inputFile):
                SystemManager.printError("buffer size is not enough (%s KB) to profile" % \
                    SystemManager.getBufferSize())
                sys.exit(0)

            # save system information #
            si.saveAllInfo()

    # parse analysis option #
    SystemManager.parseAnalOption()

    # save kernel function_graph and terminate #
    if SystemManager.isRecordMode() and \
        SystemManager.isFunctionMode() and \
        SystemManager.graphEnable:
        ThreadAnalyzer(SystemManager.inputFile)

    # get tty setting #
    SystemManager.getTty()

    # import packages to draw graph #
    if SystemManager.graphEnable:
        try:
            import matplotlib
            matplotlib.use('Agg')
            from pylab import \
                rc, rcParams, subplot, plot, title, xlabel, ylabel, text, pie, axis,\
                subplots_adjust, legend, figure, savefig, clf, ticklabel_format, suptitle,\
                grid, yticks, xticks, locator_params, subplot2grid, ylim, xlim, tick_params
            from matplotlib.ticker import MaxNLocator
        except ImportError:
            err = sys.exc_info()[1]
            SystemManager.printError("Fail to import package: " + err.args[0])
            sys.exit(0)

    # convert txt to image #
    if SystemManager.customImageEnable:
        SystemManager.printStatus("start converting...")
        SystemManager.makeLogImage()
        sys.exit(0)

    if SystemManager.isTopMode():
        # set arch #
        SystemManager.setArch(SystemManager.getArch())

        # print record option #
        SystemManager.printRecordOption()

        # set handler for exit #
        if sys.platform.startswith('linux'):
            signal.signal(signal.SIGINT, SystemManager.stopHandler)
            signal.signal(signal.SIGQUIT, SystemManager.newHandler)

        # run in background #
        if SystemManager.backgroundEnable:
            pid = os.fork()

            if pid > 0:
                sys.exit(0)
            else:
                SystemManager.pid = os.getpid()
                SystemManager.printStatus("background running as process %s" % SystemManager.pid)

        # create ThreadAnalyzer using proc #
        ti = ThreadAnalyzer(None)

        # close pipe for less util #
        if SystemManager.pipeForPrint is not None:
            SystemManager.pipeForPrint.close()

        sys.exit(0)

    # set handler for exit #
    signal.signal(signal.SIGINT, SystemManager.exitHandler)

    # check log file is recoginizable #
    ThreadAnalyzer.getInitTime(SystemManager.inputFile)

    if SystemManager.isRecordMode():
        # write system info to buffer #
        si.printAllInfoToBuf()
    else:
        # apply launch option from data file #
        SystemManager.applyLaunchOption()

    # get mount info from data file #
    SystemManager.getMountInfo()

    # print analysis option #
    SystemManager.printAnalOption()

    # create Event Info #
    ei = EventAnalyzer()

    if SystemManager.functionEnable is not False:
        # create FunctionAnalyzer #
        fi = FunctionAnalyzer(SystemManager.inputFile)

        # print Function Info #
        fi.printUsage()

        start = fi.startTime
    else:
        # create ThreadAnalyzer #
        ti = ThreadAnalyzer(SystemManager.inputFile)

        # print thread usage #
        ti.printUsage()

        # print block usage #
        ti.printBlockInfo()

        # print resource usage of threads on timeline #
        ti.printIntervalInfo()

        # print module information #
        ti.printModuleInfo()

        # print dependency of threads #
        ti.printDepInfo()

        # print kernel messages #
        ti.printConsoleInfo()

        # print system call usage #
        ti.printSyscallInfo()

        start = ti.startTime

    # print event info #
    ei.printEventInfo(start)

    # close pipe for less util #
    if SystemManager.pipeForPrint is not None:
        SystemManager.pipeForPrint.close()

    # start input menu #
    if SystemManager.selectMenu != None:
        # make file related to taskchain #
        ti.makeTaskChainList()
