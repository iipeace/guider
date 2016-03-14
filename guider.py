#!/usr/bin/python

# Peace Lee, LGE, iipeace5@gmail.com, November 2015.

# This program is made for profiling the performance of system based on linux kernel.
# you can use this program if some ftrace options are enabled in linux kernel.





import re
import sys
import signal
import time
import os
import shutil





class ConfigInfo:

    makeConfig = None

    @staticmethod
    def readProcData(tid, file, num):
		file = '/proc/'+ tid + '/' + file

		try: f = open(file, 'r')
		except: 
			SystemInfo.pipePrint("[Error] Open %s" % (file))
			return None

		if num == 0: return f.readline().replace('\n','')
		else: return f.readline().replace('\n','').split(' ')[num - 1]



    @staticmethod
    def openConfFile(file):
			file += '.tc'
			if os.path.isfile(file) == True:
				SystemInfo.pipePrint("[Warning] %s exist, make new one" % (file))

			try: f = open(file, 'wt')
			except:
				SystemInfo.pipePrint("[Error] Open %s" % (file))
				return None

			return f




    @staticmethod
    def writeConfData(fd, line):
		if fd == None:
			SystemInfo.pipePrint("[Error] File is not open")
			return None

		fd.write(line)





class SystemInfo:

    version = "1.3.0"
    maxCore = 0
    mountPath = None
    pipeForPrint = None
    fileForPrint = None
    inputFile = None
    outputFile = None
    printFile = None
    ttyEnable = True
    graphEnable = False
    graphLabels= []
    bufferString = ''

    eventLogFile = None
    eventLogFD = None

    showAll = False
    selectMenu = None
    intervalNow = 0

    irqEnable = False
    memEnable = False 
    futexEnable = False 
    depEnable = False
    sysEnable = False
    intervalEnable = 0
    repeatInterval = 0
    repeatCount = 0

    cmdList = {}
    preemptGroup = []
    showGroup = []
    syscallList = []

    # systemcall numbers for ARM #
    sysWrite = '4'
    sysSelect = '142'
    sysPoll = '168'
    sysEpollwait = '252'
    sysRecv = '291'
    sysFutex = '240'

    def __init__(self):
		self.memData = {}
		self.bufferSize = '20480'

		self.memData['before'] = dict()
		self.memData['after'] = dict()

		eventLogFile = str(self.getMountPath()) + '/tracing/trace_marker'

		self.saveMeminfo()



    @staticmethod
    def stopHandler(signum, frame):
		signal.signal(signal.SIGINT, signal.SIG_DFL)
		print 'start analyzing... [ STOP(ctrl + c) ]'
	


    @staticmethod
    def newHandler(signum, frame):
		os.system('echo EVENT_RESTART > /dev/kmsg')
		print 'restart profiling... [ STOP(ctrl + c) ]'
		time.sleep(1024)



    @staticmethod
    def exitHandler(signum, frame):
		print '\n'
		sys.exit(0)



    @staticmethod
    def exitHandlerForFSinfo(signum, frame):
		for dirnames in os.walk('/sys/class/block'):
			for subdirname in dirnames[1]:
				devPath = '/sys/class/block/' + subdirname + '/dev'
				sizePath = '/sys/class/block/' + subdirname + '/size'
				devFd = open(devPath, 'r')
				sizeFd = open(sizePath, 'r')
				dev = devFd.readline().rstrip()
				size = sizeFd.readline().rstrip()



    @staticmethod
    def alarmHandler(signum, frame):
		if SystemInfo.repeatCount > 0:
                        if SystemInfo.outputFile != None:
			        output = SystemInfo.outputFile + str(SystemInfo.repeatCount)
                                try: 
                                        shutil.copy(os.path.join(SystemInfo.mountPath + '../trace'), output)
                                        print '[Info] trace data is saved to %s' % output
                                except: 
                                        print '[Warning] Fail to save trace data to %s' % output

                                SystemInfo.repeatCount -= 1
                                signal.alarm(SystemInfo.repeatInterval)
                        else:
                                print '[Error] Fail to save trace data because output file is not set'
                                si.runRecordStopCmd()
                                sys.exit(0)
		else:
                        si.runRecordStopCmd()
			sys.exit(0)


    @staticmethod
    def writeCmd(path, val):
                try: fd = open(SystemInfo.mountPath + path, 'w')
                except:
                        print "[Warning] Fail to use %s event, please confirm kernel configuration" % path[0:path.find('/')]
                        return -1
                try:
                        fd.write(val)
                        fd.close()
                except:
                        print "[Warning] Fail to apply command to %s becuase of BUG" % path
                        return -2

                return 0

    @staticmethod
    def addPrint(string):
		SystemInfo.bufferString += string



    @staticmethod
    def clearPrint():
		del SystemInfo.bufferString
		SystemInfo.bufferString = ''



    @staticmethod
    def writeEvent(message):
		if SystemInfo.eventLogFD == None:
			SystemInfo.eventLogFD = open(SystemInfo.eventLogFile, 'w')

		if SystemInfo.eventLogFD != None:
			SystemInfo.eventLogFD.write(message)
		else:
			print "[Error] event %s couldn't be open\n" % (message)


    @staticmethod
    def pipePrint(line):
		if SystemInfo.pipeForPrint == None and SystemInfo.selectMenu == None and SystemInfo.printFile == None: 
			try: SystemInfo.pipeForPrint = os.popen('less', 'w')
			except: print "[Error] less can not be found\n"

			if SystemInfo.ttyEnable == True:
				SystemInfo.setTtyCols('150')
				SystemInfo.setTtyRows('45')

		if SystemInfo.pipeForPrint != None:
			try: SystemInfo.pipeForPrint.write(line + '\n')
			except:
				print "[Error] printing to pipe failed\n"
				SystemInfo.pipeForPrint = None

		if SystemInfo.printFile != None and SystemInfo.fileForPrint == None:
			if sys.argv[1] != 'record':
				SystemInfo.inputFile = SystemInfo.inputFile.replace('dat', 'out')
			else: 
				SystemInfo.inputFile = SystemInfo.printFile + '/guider.out'

			try: SystemInfo.fileForPrint = open(SystemInfo.inputFile, 'w')
			except: print "[Error] less can not be found\n"

		if SystemInfo.fileForPrint != None:
			try: SystemInfo.fileForPrint.write(line + '\n')
			except:
				print "[Error] printing to file failed\n"
				SystemInfo.pipeForPrint = None
		else:
			print line



    @staticmethod
    def setRtPriority(pri):
		os.system('chrt -a -p %s %s' % (pri, os.getpid()))



    @staticmethod
    def setTtyCols(cols):
		os.system('stty cols %s' % (cols))



    @staticmethod
    def setTtyRows(rows):
		os.system('stty rows %s' % (rows))



    def saveMeminfo(self):
		f = open('/proc/meminfo', 'r')
		lines = f.readlines()

		if self.memData['before'] == {}: time = 'before'
		else: time = 'after'

		for l in lines:
			m = re.match('(?P<type>\S+):\s+(?P<size>[0-9]+)', l)
			if m is not None:
				d = m.groupdict()
				self.memData[time][d['type']] = d['size']
		f.close() 



    def getMeminfo(self, data):
		return str(self.memData[time][d['type']])



    def getBufferSize(self):
		f = open(SystemInfo.mountPath + "../buffer_total_size_kb", 'r')
		lines = f.readlines()

		return int(lines[0])



    @staticmethod
    def getMountPath():
		f = open('/proc/mounts', 'r')
		lines = f.readlines()

		for l in lines:
			m = re.match('(?P<dev>\S+)\s+(?P<dir>\S+)\s+(?P<fs>\S+)', l)
			if m is not None:
				d = m.groupdict()
				if d['fs'] == 'debugfs':
					f.close() 
					return d['dir']
		f.close() 




    @staticmethod
    def clearTraceBuffer():
                SystemInfo.writeCmd("../trace", '')



    def initCmdList(self):
                self.cmdList["sched/sched_switch"] = True
                self.cmdList["sched/sched_process_free"] = True
                self.cmdList["sched/sched_wakeup"] = SystemInfo.depEnable
                self.cmdList["irq"] = SystemInfo.irqEnable
                self.cmdList["signal"] = SystemInfo.depEnable
                self.cmdList["raw_syscalls/sys_enter"] = SystemInfo.depEnable
                self.cmdList["raw_syscalls/sys_exit"] = SystemInfo.depEnable
                self.cmdList["raw_syscalls"] = SystemInfo.sysEnable
                self.cmdList["kmem/mm_page_alloc"] = SystemInfo.memEnable
                self.cmdList["kmem/mm_page_free"] = SystemInfo.memEnable
                self.cmdList["kmem/kmalloc"] = SystemInfo.memEnable
                self.cmdList["kmem/kfree"] = SystemInfo.memEnable
                self.cmdList["block/block_bio_remap"] = True
                self.cmdList["block/block_rq_complete"] = True
                self.cmdList["vmscan/mm_vmscan_direct_reclaim_begin"] = True
                self.cmdList["vmscan/mm_vmscan_direct_reclaim_end"] = True
                self.cmdList["sched/sched_migrate_task"] = True
                self.cmdList["task"] = True
                self.cmdList["power/machine_suspend"] = True
                self.cmdList["printk"] = True
                self.cmdList["power/cpu_idle"] = True
                self.cmdList["power/power_frequency"] = True
                self.cmdList["vmscan/mm_vmscan_wakeup_kswapd"] = False
                self.cmdList["vmscan/mm_vmscan_kswapd_sleep"] = False



    def runRecordStartCmd(self):
		cmd = self.getMountPath()
		if cmd == None:
			SystemInfo.mountPath = "/sys/kernel/debug"
			cmd = "mount -t debugfs nodev " + SystemInfo.mountPath + ";"
			os.system(cmd)
		else: SystemInfo.mountPath = str(cmd)
			
		SystemInfo.mountPath += "/tracing/events/"

		if os.path.isdir(SystemInfo.mountPath) == False:
			print "[Error] ftrace option in kernel is not enabled"
			sys.exit(0)

                self.clearTraceBuffer()
                SystemInfo.writeCmd("../buffer_size_kb", self.bufferSize)
                self.initCmdList()

                if self.cmdList["sched/sched_switch"] is True:
                        if len(SystemInfo.showGroup) > 0:
                                cmd = "prev_pid == 0 || next_pid == 0 || "
                                for comm in SystemInfo.showGroup:
                                        cmd += "prev_comm == \"%s\" || next_comm == \"%s\" || " % (comm, comm)
                                cmd = cmd[0:cmd.rfind("||")]
                                SystemInfo.writeCmd('sched/sched_switch/filter', cmd)
                        else: SystemInfo.writeCmd('sched/sched_switch/filter', '0')

                        if SystemInfo.writeCmd('sched/sched_switch/enable', '1') < 0:
                            print "[Error] sched option in kernel is not enabled"
                            sys.exit(0)

                if self.cmdList["sched/sched_wakeup"] is True:
                        SystemInfo.writeCmd('sched/sched_wakeup/enable', '1')

                if self.cmdList["irq"] is True:
                        SystemInfo.writeCmd('irq/enable', '1')

                if self.cmdList["raw_syscalls/sys_enter"] is True:
                        cmd = "(id == %s || id == %s || id == %s || id == %s || id == %s || id == %s)" \
                        % (SystemInfo.sysWrite, SystemInfo.sysPoll, SystemInfo.sysEpollwait, SystemInfo.sysSelect, SystemInfo.sysRecv, SystemInfo.sysFutex)

                        SystemInfo.writeCmd('raw_syscalls/sys_enter/filter', cmd)
                        SystemInfo.writeCmd('raw_syscalls/sys_enter/enable', '1')
                elif SystemInfo.futexEnable is True:
                        cmd = "(id == %s)" % (SystemInfo.sysFutex)
                        SystemInfo.writeCmd('raw_syscalls/sys_enter/filter', cmd)
                        SystemInfo.writeCmd('raw_syscalls/sys_enter/enable', '1')
                        self.cmdList["raw_syscalls/sys_enter"] = True
                else:
                        SystemInfo.writeCmd('raw_syscalls/sys_enter/filter', '0')
                        SystemInfo.writeCmd('raw_syscalls/sys_enter/enable', '0')

                if self.cmdList["raw_syscalls/sys_exit"] is True:
                        cmd = "((id == %s || id == %s || id == %s || id == %s || id == %s || id == %s) && ret > 0)" \
                        % (SystemInfo.sysWrite, SystemInfo.sysPoll, SystemInfo.sysEpollwait, SystemInfo.sysSelect, SystemInfo.sysRecv, SystemInfo.sysFutex)

                        SystemInfo.writeCmd('raw_syscalls/sys_exit/filter', cmd)
                        SystemInfo.writeCmd('raw_syscalls/sys_exit/enable', '1')
                elif SystemInfo.futexEnable is True:
                        cmd = "(id == %s  && ret == 0)" % (SystemInfo.sysFutex)
                        SystemInfo.writeCmd('raw_syscalls/sys_exit/filter', cmd)
                        SystemInfo.writeCmd('raw_syscalls/sys_exit/enable', '1')
                        self.cmdList["raw_syscalls/sys_exit"] = True
                else:
                        SystemInfo.writeCmd('raw_syscalls/sys_exit/filter', '0')
                        SystemInfo.writeCmd('raw_syscalls/sys_exit/enable', '0')


                if self.cmdList["raw_syscalls"] is True:
                        if len(SystemInfo.syscallList) > 0:
				cmd = "("
				for val in SystemInfo.syscallList:
					cmd += " id == %s ||" % val
					if SystemInfo.syscallList.index(val) == len(SystemInfo.syscallList) - 1:
						cmd += " id == %s)" % val
                                SystemInfo.writeCmd('raw_syscalls/filter', cmd)

                        if SystemInfo.sysEnable is True and len(SystemInfo.syscallList) == 0: 
                                SystemInfo.writeCmd('raw_syscalls/filter', '0')
                                SystemInfo.writeCmd('raw_syscalls/sys_enter/filter', '0')
                                SystemInfo.writeCmd('raw_syscalls/sys_exit/filter', '0')

                        SystemInfo.writeCmd('raw_syscalls/enable', '1')

                if self.cmdList["signal"] is True:
			if SystemInfo.depEnable == True:
                                SystemInfo.writeCmd('signal/enable', '1')

                if self.cmdList["power/machine_suspend"] is True:
                        SystemInfo.writeCmd('power/machine_suspend/enable', '1')

                if self.cmdList["kmem/mm_page_alloc"] is True:
                        SystemInfo.writeCmd('kmem/mm_page_alloc/enable', '1')
                if self.cmdList["kmem/mm_page_free"] is True:
                        SystemInfo.writeCmd('kmem/mm_page_free/enable', '1')
                if self.cmdList["kmem/kmalloc"] is True:
                        SystemInfo.writeCmd('kmem/kmalloc/enable', '1')
                if self.cmdList["kmem/kfree"] is True:
                        SystemInfo.writeCmd('kmem/kfree/enable', '1')

                if self.cmdList["block/block_bio_remap"] is True:
                        SystemInfo.writeCmd('block/block_bio_remap/enable', '1')
                if self.cmdList["block/block_rq_complete"] is True:
                        SystemInfo.writeCmd('block/block_rq_complete/enable', '1')

                if self.cmdList["power/cpu_idle"] is True:
                        SystemInfo.writeCmd('power/cpu_idle/enable', '1')
                if self.cmdList["power/power_frequency"] is True:
                        SystemInfo.writeCmd('power/power_frequency/enable', '1')

                if self.cmdList["vmscan/mm_vmscan_wakeup_kswapd"] is True:
                        SystemInfo.writeCmd('vmscan/mm_vmscan_wakeup_kswapd/enable', '1')
                if self.cmdList["vmscan/mm_vmscan_kswapd_sleep"] is True:
                        SystemInfo.writeCmd('vmscan/mm_vmscan_kswapd_sleep/enable', '1')

                if self.cmdList["vmscan/mm_vmscan_direct_reclaim_begin"] is True:
                        SystemInfo.writeCmd('vmscan/mm_vmscan_direct_reclaim_begin/enable', '1')
                if self.cmdList["vmscan/mm_vmscan_direct_reclaim_end"] is True:
                        SystemInfo.writeCmd('vmscan/mm_vmscan_direct_reclaim_end/enable', '1')

                if self.cmdList["task"] is True:
                        SystemInfo.writeCmd('task/enable', '1')
                if self.cmdList["sched/sched_migrate_task"] is True:
                        SystemInfo.writeCmd('sched/sched_migrate_task/enable', '1')
                if self.cmdList["sched/sched_process_free"] is True:
                        SystemInfo.writeCmd('sched/sched_process_free/enable', '1')

                if self.cmdList["printk"] is True:
                        SystemInfo.writeCmd('printk/enable', '1')

		return 



    def runRecordStopCmd(self):
                for idx, val in SystemInfo.cmdList.items():
                        if val is True:
                                SystemInfo.writeCmd(str(idx) + '/enable', '0')





class EventInfo:
    def __init__(self):
		self.eventData = {}



    def addEvent(self, time, event):
		# ramdom event #
		if len(event.split('_')) == 1:
			name = event
			ID = None
		# sequantial event #
		else:
			name = event.split('_')[0]
			ID = event.split('_')[1]

		try: self.eventData[name]
		# {'list': [ID, time, number], 'summary': [ID, cnt, avr, min, max, first, last]}
		except: self.eventData[name] = {'list': [], 'summary': []}

		self.eventData[name]['list'].append([ID, time, sum(t[0] == ID for t in self.eventData[name]['list']) + 1])	

		if sum(id[0] == ID for id in self.eventData[name]['summary']) == 0:
			self.eventData[name]['summary'].append([ID, 1, 0, 0, 0, time, 0])
		else:
			for n in self.eventData[name]['summary']:
				if n[0] == ID:
					n[1] += 1;
					n[6] = time;
					break;



    def printEvent(self, startTime):
		for key,value in sorted(self.eventData.items(), key=lambda e: e[1], reverse=True):
			if self.eventData[key]['summary'][0][0] == None:
				SystemInfo.pipePrint("%10s: [total: %s]" % (key, len(self.eventData[key]['list'])))
			else:
				string = ''
				for n in sorted(self.eventData[key]['summary'], key=lambda slist: slist[0]):
					string += '[%s: %d/%d/%d/%d/%.3f/%.3f] ' % (n[0], n[1], n[2], n[3], n[4], float(n[5]) - float(startTime), 0)
				SystemInfo.pipePrint("%10s: [total: %s] [subEvent: %s] %s" % (key, len(self.eventData[key]['list']), len(self.eventData[key]['summary']), string))




class ThreadInfo:
    def __init__(self, file):
		self.threadData = {}
		self.irqData = {}
		self.ioData = {}
		self.reclaimData = {}
		self.pageTable = {}
                self.kmallocTable = {}
		self.intervalData = []
		self.depData = []
		self.syscallData = []
		self.lastJob = {}
		self.preemptData = []
                self.suspendData = []
                self.consoleData = []

		self.stopFlag = False
		self.totalTime = 0
		self.totalTimeOld = 0
		self.logCnt = 0

		self.threadDataOld = {}
		self.irqDataOld = {}
		self.ioDataOld = {}
		self.reclaimDataOld = {}

		self.init_threadData = {'comm': '', 'usage': float(0), 'cpuRank': int(0), 'yield': int(0), 'cpuWait': float(0), 'pri': '0', \
                        'ioWait': float(0), 'reqBlock': int(0), 'readBlock': int(0), 'ioRank': int(0), 'irq': float(0), 'reclaimWait': float(0), \
                        'reclaimCnt': int(0), 'migrate': int(0), 'ppid': '0', 'new': ' ', 'die': ' ', 'preempted': int(0), 'preemption': int(0), \
                        'start': float(0), 'stop': float(0), 'io_cnt': int(0), 'io_start': float(0), 'maxRuntime': float(0), 'coreSchedCnt': int(0), \
                        'dReclaimWait': float(0), 'dReclaimStart': float(0), 'dReclaimCnt': int(0), 'futexCnt': int(0), 'futexEnter': float(0), \
                        'futexTotal': float(0), 'futexMax': float(0), 'lastStatus': 'N', 'offCnt': int(0), 'offTime': float(0), 'lastOff': float(0), \
                        'pages': int(0), 'usedMem': int(0), 'wasteMem': int(0), 'lastWakeup': float(0)}
		self.init_irqData = {'name': '', 'usage': float(0), 'start': float(0), 'max': float(0), 'min': float(0), \
                        'max_period': float(0), 'min_period': float(0), 'count': int(0)}
		self.init_intervalData = {'time': float(0), 'cpuUsage': float(0), 'totalUsage': float(0), 'cpuPer': float(0), 'ioUsage': float(0), \
                        'totalIoUsage': float(0),'irqUsage': float(0), 'memUsage': float(0), 'totalMemUsage': float(0), 'ioPer': int(0), 'memPer': int(0), \
                        'coreSchedCnt': int(0), 'totalCoreSchedCnt': int(0)}
		self.init_pageData = {'tid': '0', 'page': '0', 'flags': '0', 'time': '0'}
                self.init_kmallocData = {'tid': '0', 'caller': '0', 'ptr': '0', 'req': int(0), 'alloc': int(0), 'time': '0', 'waste': int(0)}
		self.init_lastJob = {'job': '0', 'time': '0', 'tid': '0', 'prevWakeupTid': '0'}
		self.wakeupData = {'tid': '0', 'nr': '0', 'ret': '0', 'time': '0', 'args': '0', 'valid': int(0), 'from': '0', 'to': '0', 'corrupt': '0'}
		self.init_preemptData = {'usage': float(0), 'count': int(0), 'max': float(0)}
                self.init_syscallInfo = {'usage': float(0), 'last': float(0), 'count': int(0), 'max': float(0), 'min': float(0)}

		self.startTime = '0'
		self.finishTime = '0'
		self.lastTid = {}

		if SystemInfo.preemptGroup != None:
			for index in SystemInfo.preemptGroup:
				# preempted state [preemptBit, threadList, startTime, core, totalUsage] #
				self.preemptData.append([False, {}, float(0), 0, float(0)])

		try:
                        f = open(file, 'r')
                        lines = f.readlines()
                        self.logCnt = len(lines)

		except IOError:
			print "[Error] Open %s", file
			sys.exit(0)

		# save trace data to file #
		try:
			if SystemInfo.outputFile != None:
                                f = open(SystemInfo.outputFile, 'wt')
                                f.writelines(lines)

				print '[Info] trace data is saved to %s' % (SystemInfo.outputFile)
				f.close()
				sys.exit(0)
		except IOError:
			print "[Error] Write %s", SystemInfo.outputFile
			sys.exit(0)

		# start parsing #
		for l in lines:
			self.parse(l)
			if self.stopFlag == True: break

		# process usage of threads in last interval #
		if SystemInfo.intervalEnable > 0:
			if float(self.finishTime) -  float(self.startTime) - float(SystemInfo.intervalNow) > 0:
				lastInterval = float(self.finishTime) -  float(self.startTime) - float(SystemInfo.intervalNow)
				SystemInfo.intervalNow += lastInterval

				for key,value in sorted(self.threadData.items(), key=lambda e: e[1]['usage'], reverse=True):
					index = int(SystemInfo.intervalNow / SystemInfo.intervalEnable)

					try: self.intervalData[index]
					except: self.intervalData.append({})
					try: self.intervalData[index][key]
					except: self.intervalData[index][key] = dict(self.init_intervalData)
					try: self.intervalData[index]['toTal']
                                        except: self.intervalData[index]['toTal'] = {'totalIo': int(0), 'totalMem': int(0)}

					if SystemInfo.intervalNow - SystemInfo.intervalEnable == 0:
						self.intervalData[index][key]['cpuUsage'] = float(self.threadData[key]['usage'])
						self.intervalData[index][key]['totalUsage'] = float(self.threadData[key]['usage'])
						self.intervalData[index][key]['ioUsage'] = float(self.threadData[key]['reqBlock'])
						self.intervalData[index][key]['totalIoUsage'] = float(self.threadData[key]['reqBlock'])
						self.intervalData[index][key]['memUsage'] = float(self.threadData[key]['pages'])
						self.intervalData[index][key]['totalMemUsage'] = float(self.threadData[key]['pages'])
						self.intervalData[index][key]['totalCoreSchedCnt'] = float(self.threadData[key]['coreSchedCnt'])
						self.intervalData[index][key]['coreSchedCnt'] = float(self.threadData[key]['coreSchedCnt'])
					else:
						self.intervalData[index][key]['totalUsage'] = float(self.threadData[key]['usage'])
						self.intervalData[index][key]['totalIoUsage'] = float(self.threadData[key]['reqBlock'])
						self.intervalData[index][key]['totalMemUsage'] = float(self.threadData[key]['pages'])
						self.intervalData[index][key]['totalCoreSchedCnt'] = float(self.threadData[key]['coreSchedCnt'])

						try: self.intervalData[index - 1][key]
						except: self.intervalData[index - 1][key] = dict(self.init_intervalData)

						self.intervalData[index][key]['cpuUsage'] = float(self.threadData[key]['usage']) - self.intervalData[index - 1][key]['totalUsage']
						self.intervalData[index][key]['ioUsage'] = float(self.threadData[key]['reqBlock']) - self.intervalData[index - 1][key]['totalIoUsage']
						self.intervalData[index][key]['memUsage'] = float(self.threadData[key]['pages']) - self.intervalData[index - 1][key]['totalMemUsage']
						self.intervalData[index][key]['coreSchedCnt'] = float(self.threadData[key]['coreSchedCnt']) - \
                                                        self.intervalData[index - 1][key]['totalCoreSchedCnt']

					self.intervalData[index][key]['cpuPer'] = \
						round(self.intervalData[index][key]['cpuUsage'], 7) / float(lastInterval) * 100
					self.intervalData[index]['toTal']['totalIo'] += self.intervalData[index][key]['ioUsage']
					self.intervalData[index]['toTal']['totalMem'] += self.intervalData[index][key]['memUsage']

		f.close() 

    def getRunTaskNum(self):
		return len(self.threadData)



    @staticmethod
    def getInitTime(file):
        try:
            f = open(file, 'r')

            while True:
            	l = f.readline()

                m = re.match('^\s*(?P<comm>\S+)-(?P<thread>[0-9]+)\s+\[(?P<core>[0-9]+)\]\s+\S+\s+(?P<time>\S+):\s+(?P<func>\S+):(?P<etc>.+)', l)
                if m is not None:
                    d = m.groupdict()
                    f.close() 
                    return d['time']

        except IOError: 
            print "[Error] Open %s", file
            sys.exit(0)



    def parse(self, string):   
        m = re.match('^\s*(?P<comm>.+)-(?P<thread>[0-9]+)\s+\[(?P<core>[0-9]+)\]\s+\S+\s+(?P<time>\S+):\s+(?P<func>\S+):(?P<etc>.+)', string)
        if m is not None:
			d = m.groupdict()
			comm = d['comm']
			core = str(int(d['core']))
			func = d['func']
			etc = d['etc']

                        if SystemInfo.maxCore < int(core):
                            SystemInfo.maxCore = int(core)

			if int(d['thread']) == 0:
				thread = d['thread'] + '['  + core + ']'
			else: thread = d['thread']
				
			comm = comm.replace("<idle>", "swapper/" + core);
			time = d['time']

                        try: self.threadData[thread]
                        except: 
                                self.threadData[thread] = dict(self.init_threadData)
                                self.threadData[thread]['comm'] = comm

			# process usage of threads is longtime running between interval #
			if SystemInfo.intervalEnable > 0:
				try:
					for key,value in sorted(self.lastTid.items()):
						if float(time) - float(self.threadData[self.lastTid[key]]['start']) > SystemInfo.intervalEnable / 1000:
							self.threadData[self.lastTid[key]]['usage'] += float(time) - float(self.threadData[self.lastTid[key]]['start'])
							self.threadData[self.lastTid[key]]['start'] = float(time)
				except: None

			if self.startTime == '0':
				self.startTime = time
			else:
				self.finishTime = time
				# process usage of threads between interval #
				if SystemInfo.intervalEnable > 0:
					if float(time) - float(self.startTime) > float(SystemInfo.intervalNow + SystemInfo.intervalEnable):
						SystemInfo.intervalNow += SystemInfo.intervalEnable

						for key,value in sorted(self.threadData.items(), key=lambda e: e[1]['usage'], reverse=True):
							index = int(SystemInfo.intervalNow / SystemInfo.intervalEnable) - 1

							try: self.intervalData[index]
							except: self.intervalData.append({})
							try: self.intervalData[index][key]
							except: self.intervalData[index][key] = dict(self.init_intervalData)
                                                        try: self.intervalData[index]['toTal']
                                                        except: self.intervalData[index]['toTal'] = {'totalIo': int(0), 'totalMem': int(0)}

							if SystemInfo.intervalNow - SystemInfo.intervalEnable == 0:
								self.intervalData[index][key]['cpuUsage'] = float(self.threadData[key]['usage'])
								self.intervalData[index][key]['totalUsage'] = float(self.threadData[key]['usage'])
								self.intervalData[index][key]['ioUsage'] = float(self.threadData[key]['reqBlock'])
								self.intervalData[index][key]['totalIoUsage'] = float(self.threadData[key]['reqBlock'])
								self.intervalData[index][key]['memUsage'] = float(self.threadData[key]['pages'])
								self.intervalData[index][key]['totalMemUsage'] = float(self.threadData[key]['pages'])
                                                                self.intervalData[index][key]['coreSchedCnt'] = float(self.threadData[key]['coreSchedCnt'])
                                                                self.intervalData[index][key]['totalCoreSchedCnt'] = float(self.threadData[key]['coreSchedCnt'])
							else:
								self.intervalData[index][key]['totalUsage'] = float(self.threadData[key]['usage'])
								self.intervalData[index][key]['totalIoUsage'] = float(self.threadData[key]['reqBlock'])
								self.intervalData[index][key]['totalMemUsage'] = float(self.threadData[key]['pages'])

								try: self.intervalData[index - 1][key]
								except: self.intervalData[index - 1][key] = dict(self.init_intervalData)

                                                                self.intervalData[index][key]['cpuUsage'] = \
                                                                        float(self.threadData[key]['usage']) - self.intervalData[index - 1][key]['totalUsage']
                                                                if self.intervalData[index][key]['cpuUsage'] > SystemInfo.intervalEnable:
                                                                        self.intervalData[index][key]['cpuUsage'] = SystemInfo.intervalEnable
								self.intervalData[index][key]['ioUsage'] = float(self.threadData[key]['reqBlock']) - self.intervalData[index - 1][key]['totalIoUsage']
								self.intervalData[index][key]['memUsage'] = float(self.threadData[key]['pages']) - self.intervalData[index - 1][key]['totalMemUsage']
                                                                self.intervalData[index][key]['coreSchedCnt'] = float(self.threadData[key]['coreSchedCnt']) - \
                                                                        self.intervalData[index - 1][key]['totalCoreSchedCnt']

							self.intervalData[index][key]['cpuPer'] = \
								round(self.intervalData[index][key]['cpuUsage'], 7) / float(SystemInfo.intervalEnable) * 100
                                                        self.intervalData[index]['toTal']['totalIo'] += self.intervalData[index][key]['ioUsage']
                                                        self.intervalData[index]['toTal']['totalMem'] += self.intervalData[index][key]['memUsage']

			if func == "sched_switch":
				m = re.match('^\s*prev_comm=(?P<prev_comm>.*)\s+prev_pid=(?P<prev_pid>[0-9]+)\s+prev_prio=(?P<prev_prio>\S+)\s+prev_state=(?P<prev_state>\S+)\s+==>\s+next_comm=(?P<next_comm>.*)\s+next_pid=(?P<next_pid>[0-9]+)\s+next_prio=(?P<next_prio>\S+)', etc)
				if m is not None:
					d = m.groupdict()

					prev_comm = d['prev_comm']
					prev_pid = d['prev_pid']
					prev_id = prev_pid
					prev_state = d['prev_state']

					if int(d['prev_pid']) == 0:
						prev_id = d['prev_pid'] + '[' + str(int(core)) + ']'
					else: prev_id = prev_pid
					
					next_comm = d['next_comm']
					next_pid = d['next_pid']
					if int(d['next_pid']) == 0:
						next_id = d['next_pid'] + '[' + str(int(core)) + ']'
					else: next_id = next_pid

					# make list #
					try: self.threadData[prev_id]
					except: 
						self.threadData[prev_id] = dict(self.init_threadData)
						self.threadData[prev_id]['comm'] = prev_comm
					try: self.threadData[next_id]
					except: 
						self.threadData[next_id] = dict(self.init_threadData)
						self.threadData[next_id]['comm'] = next_comm
					try: self.threadData['0[' + core + ']']
					except: 
						self.threadData['0[' + core + ']'] = dict(self.init_threadData)
						self.threadData['0[' + core + ']']['comm'] = 'swapper/' + core

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
					self.threadData[prev_id]['stop'] = round(float(time), 7)
					self.threadData[next_id]['start'] = round(float(time), 7)

					# update pid of thread to highest #
					if self.threadData[prev_id]['pri'] == '0' or int(self.threadData[prev_id]['pri']) > int(d['prev_prio']):
						self.threadData[prev_id]['pri'] = d['prev_prio']
					if self.threadData[next_id]['pri'] == '0' or int(self.threadData[next_id]['pri']) > int(d['next_prio']):
						self.threadData[next_id]['pri'] = d['next_prio']
						
					# process time of prev_process #
					if self.threadData[prev_id]['start'] <= 0:
						# there is no start time of prev_id #
						self.threadData[prev_id]['start'] = 0
					else:
                                                diff = self.threadData[prev_id]['stop'] - self.threadData[prev_id]['start']
						self.threadData[prev_id]['usage'] += diff 
                                                if self.threadData[prev_id]['maxRuntime'] < diff:
							self.threadData[prev_id]['maxRuntime'] = diff

                                        if prev_id[0:2] == '0[' and self.threadData['0[' + core + ']']['coreSchedCnt'] == 0:
                                                self.threadData['0[' + core + ']']['usage'] = float(time) - float(self.startTime)

					# update core scheduling count #
					self.threadData['0[' + core + ']']['coreSchedCnt'] += 1

					# process preempted time #
					if SystemInfo.preemptGroup != None:
						for value in SystemInfo.preemptGroup:
							index = SystemInfo.preemptGroup.index(value)
							if self.preemptData[index][0] == True and self.preemptData[index][3] == core:
								try: self.preemptData[index][1][prev_id]
								except: self.preemptData[index][1][prev_id] = dict(self.init_preemptData)

								self.preemptData[index][1][prev_id]['usage'] +=  \
								self.threadData[prev_id]['stop'] - self.threadData[prev_id]['start']
								self.preemptData[index][4] += self.threadData[prev_id]['stop'] - self.threadData[prev_id]['start']

					if d['prev_state'][0] == 'R':
						self.threadData[prev_id]['preempted'] += 1
						self.threadData[next_id]['preemption'] += 1
						self.threadData[prev_id]['lastStatus'] = 'P'

						if SystemInfo.preemptGroup != None:
							# enable preempted bit #
							try: index = SystemInfo.preemptGroup.index(prev_id)
							except: index = -1

							if index >= 0:
								self.preemptData[index][0] = True
								try: self.preemptData[index][1][next_id]
								except: self.preemptData[index][1][next_id] = dict(self.init_preemptData)

								self.preemptData[index][2] = round(float(time), 7)
								self.preemptData[index][3] = core

					elif d['prev_state'][0] == 'S':
						self.threadData[prev_id]['yield'] += 1
						self.threadData[prev_id]['stop'] = 0
						self.threadData[prev_id]['lastStatus'] = 'S'

					else: 
                                                self.threadData[prev_id]['stop'] = 0
						self.threadData[prev_id]['lastStatus'] = d['prev_state'][0]
						
					# process time of next_process #
					self.lastTid[core] = next_id
					if self.threadData[next_id]['stop'] <= 0:
						# there is no stop time of next_id #
						self.threadData[next_id]['stop'] = 0
					else:
						if self.threadData[next_id]['lastStatus'] == 'P':
							self.threadData[next_id]['cpuWait'] +=  self.threadData[next_id]['start'] - self.threadData[next_id]['stop']

							try: self.preemptData[SystemInfo.preemptGroup.index(next_id)][0] = False
							except: None

                                        if self.threadData[next_id]['lastWakeup'] > 0:
                                                self.threadData[next_id]['cpuWait'] += float(time) - self.threadData[next_id]['lastWakeup']
                                                self.threadData[next_id]['lastWakeup'] = 0

			elif func == "irq_handler_entry":
				m = re.match('^\s*irq=(?P<irq>[0-9]+)\s+name=(?P<name>\S+)', etc)
				if m is not None:
					d = m.groupdict()

					irqId = 'irq/' + d['irq']

					# make list #
					try: self.irqData[irqId]
					except: self.irqData[irqId] = dict(self.init_irqData)

					if self.irqData[irqId]['start'] > 0:
                                                diff = round(float(time), 7) - self.irqData[irqId]['start']
						if diff > self.irqData[irqId]['max_period'] or self.irqData[irqId]['max_period'] <= 0:
							self.irqData[irqId]['max_period'] = diff
						if diff < self.irqData[irqId]['min_period'] or self.irqData[irqId]['min_period'] <= 0:
							self.irqData[irqId]['min_period'] = diff

					self.irqData[irqId]['start'] = round(float(time), 7)
					self.irqData[irqId]['name'] = d['name']
					self.irqData[irqId]['count'] += 1

			elif func == "irq_handler_exit":
				m = re.match('^\s*irq=(?P<irq>[0-9]+)\s+ret=(?P<return>\S+)', etc)
				if m is not None:
					d = m.groupdict()

					irqId = 'irq/' + d['irq']

					# make list #
					try: self.irqData[irqId]
					except: self.irqData[irqId] = dict(self.init_irqData)

					if self.irqData[irqId]['start'] > 0:
                                                diff = round(float(time), 7) - self.irqData[irqId]['start']
						self.irqData[irqId]['usage'] += diff
						self.threadData[thread]['irq'] += diff

						if diff > self.irqData[irqId]['max'] or self.irqData[irqId]['max'] <= 0:
							self.irqData[irqId]['max'] = diff
						if diff < self.irqData[irqId]['min'] or self.irqData[irqId]['min'] <= 0:
							self.irqData[irqId]['min'] = diff

			elif func == "softirq_entry":
				m = re.match('^\s*vec=(?P<vector>[0-9]+)\s+\[action=(?P<action>\S+)]', etc)
				if m is not None:
					d = m.groupdict()

					irqId = 'softirq/' + d['vector']

					# make list #
					try: self.irqData[irqId]
					except: 
						self.irqData[irqId] = dict(self.init_irqData)
						self.irqData[irqId]['name'] = d['action']

					if self.irqData[irqId]['start'] > 0:
                                                diff = round(float(time), 7) - self.irqData[irqId]['start']
						if diff > self.irqData[irqId]['max_period'] or self.irqData[irqId]['max_period'] <= 0:
							self.irqData[irqId]['max_period'] = diff
						if diff < self.irqData[irqId]['min_period'] or self.irqData[irqId]['min_period'] <= 0:
							self.irqData[irqId]['min_period'] = diff

					self.irqData[irqId]['start'] = round(float(time), 7)
					self.irqData[irqId]['count'] += 1

			elif func == "softirq_exit":
				m = re.match('^\s*vec=(?P<vector>[0-9]+)\s+[action=(?P<action>\S+)]', etc)
				if m is not None:
					d = m.groupdict()

					irqId = 'softirq/' + d['vector']

					# make list #
					try: self.irqData[irqId]
					except: 
						self.irqData[irqId] = dict(self.init_irqData)
						self.irqData[irqId]['name'] = d['action']

					if self.irqData[irqId]['start'] > 0:
                                                diff = round(float(time), 7) - self.irqData[irqId]['start']
						self.irqData[irqId]['usage'] += diff
						self.threadData[thread]['irq'] += diff

						if diff > self.irqData[irqId]['max'] or self.irqData[irqId]['max'] <= 0:
							self.irqData[irqId]['max'] = diff
						if diff < self.irqData[irqId]['min'] or self.irqData[irqId]['min'] <= 0:
							self.irqData[irqId]['min'] = diff

			elif func == "sched_migrate_task":
				m = re.match('^\s*comm=(?P<comm>.*)\s+pid=(?P<pid>[0-9]+)\s+prio=(?P<prio>[0-9]+)\s+orig_cpu=(?P<orig_cpu>[0-9]+)\s+dest_cpu=(?P<dest_cpu>[0-9]+)', etc)
				if m is not None:
					d = m.groupdict()

					pid = d['pid']

					try: self.threadData[pid]
					except: 
						self.threadData[pid] = dict(self.init_threadData)
						self.threadData[pid]['comm'] = d['comm']

					self.threadData[pid]['migrate'] += 1

					# update core data for preempted info #
					if SystemInfo.preemptGroup != None:
						try: index = SystemInfo.preemptGroup.index(thread)
						except: index = -1

						if index >= 0: self.preemptData[index][3] = core

			elif func == "mm_page_alloc":
				m = re.match('^\s*page=(?P<page>\S+)\s+pfn=(?P<pfn>[0-9]+)\s+order=(?P<order>[0-9]+)\s+migratetype=(?P<mt>[0-9]+)\s+gfp_flags=(?P<flags>\S+)', etc)
				if m is not None:
					d = m.groupdict()

					SystemInfo.memEnable = True

					page = d['page']
					pfn = int(d['pfn'])
					flags = d['flags']
                                        order = int(d['order'])

					self.threadData[thread]['pages'] += pow(2, order)

                                        for cnt in range(0, pow(2, order)):
                                                pfnv = pfn + cnt

                                                try: 
                                                        self.pageTable[pfnv]
                                                        # some alloed page is not freed
                                                except: self.pageTable[pfnv] = dict(self.init_pageData)

                                                self.pageTable[pfnv]['tid'] = thread
                                                self.pageTable[pfnv]['page'] = page
                                                self.pageTable[pfnv]['flags'] = flags
                                                self.pageTable[pfnv]['time'] = time

			elif func == "mm_page_free":
				m = re.match('^\s*page=(?P<page>\S+)\s+pfn=(?P<pfn>[0-9]+)\s+order=(?P<order>[0-9]+)', etc)
				if m is not None:
					d = m.groupdict()

					SystemInfo.memEnable = True

					page = d['page']
					pfn = int(d['pfn'])
                                        order = int(d['order'])

                                        self.threadData[thread]['pages'] -= pow(2, order)

                                        for cnt in range(0, pow(2, order)):
                                                pfnv = pfn + cnt

                                                try: del self.pageTable[pfnv]
                                                except: 
                                                        # some freed page is not logged
                                                        None

			elif func == "kmalloc":
				m = re.match('^\s*call_site=(?P<caller>\S+)\s+ptr=(?P<ptr>\S+)\s+bytes_req=(?P<req>[0-9]+)\s+bytes_alloc=(?P<alloc>[0-9]+)\s+gfp_flags=(?P<flags>\S+)', etc)
				if m is not None:
					d = m.groupdict()

					SystemInfo.memEnable = True

					caller = d['caller']
					ptr = d['ptr']
					req = int(d['req'])
					alloc = int(d['alloc'])

                                        try: 
                                                self.kmallocTable[ptr]
                                                # some alloed object is not freed
                                        except: self.kmallocTable[ptr] = dict(self.init_kmallocData)

                                        self.kmallocTable[ptr]['tid'] = thread
                                        self.kmallocTable[ptr]['caller'] = caller
                                        self.kmallocTable[ptr]['req'] = req
                                        self.kmallocTable[ptr]['alloc'] = alloc
                                        self.kmallocTable[ptr]['waste'] = alloc - req

                                        self.threadData[thread]['usedMem'] += alloc
                                        self.threadData[thread]['wasteMem'] += alloc - req

			elif func == "kfree":
				m = re.match('^\s*call_site=(?P<caller>\S+)\s+ptr=(?P<ptr>\S+)', etc)
				if m is not None:
					d = m.groupdict()

					SystemInfo.memEnable = True

					caller = d['caller']
					ptr = d['ptr']

                                        try: 
                                                self.threadData[self.kmallocTable[ptr]['tid']]['usedMem'] -= self.kmallocTable[ptr]['alloc']
                                                self.threadData[self.kmallocTable[ptr]['tid']]['wasteMem'] -= self.kmallocTable[ptr]['waste']
                                        except: 
                                                # some alloed object is not logged
                                                return
                                                
			elif func == "sched_wakeup":
				m = re.match('^\s*comm=(?P<comm>.*)\s+pid=(?P<pid>[0-9]+)\s+prio=(?P<prio>[0-9]+)\s+success=(?P<success>[0-9]+)\s+target_cpu=(?P<target>[0-9]+)', etc)
				if m is not None:
					d = m.groupdict()

					target_comm = d['comm']
					pid= d['pid']
					prio = d['prio']
					success= d['success']

					if self.wakeupData['tid'] == '0':
						self.wakeupData['time'] = round(float(time) - float(self.startTime), 7)
					elif thread[0] == '0' or pid == '0': None
					elif self.wakeupData['valid'] > 0 \
						 and (self.wakeupData['from'] != self.wakeupData['tid'] or self.wakeupData['to'] != pid):
						if self.wakeupData['valid'] == 1 and self.wakeupData['corrupt'] == '0':
							try: kicker = self.threadData[self.wakeupData['tid']]['comm']
							except: kicker = "NULL"
							kicker_pid = self.wakeupData['tid']
						else:
							kicker = self.threadData[thread]['comm']
							kicker_pid = thread
						self.depData.append("\t%.3f/%.3f \t%16s(%4s) -> %16s(%4s) \t%s" % (round(float(time) - float(self.startTime), 7), \
						 round(float(time) - float(self.startTime) - float(self.wakeupData['time']), 7), kicker, \
						 kicker_pid, target_comm, pid, "kick"))

						self.wakeupData['time'] = float(time) - float(self.startTime)
						self.wakeupData['from'] = self.wakeupData['tid']
						self.wakeupData['to'] = pid

			elif func == "sys_enter":
				m = re.match('^\s*NR (?P<nr>[0-9]+) (?P<args>.+)', etc)
				if m is not None:
					d = m.groupdict()

					nr = d['nr']
					args = d['args']

					if nr == SystemInfo.sysFutex:
						self.threadData[thread]['futexEnter'] = float(time)

					if self.wakeupData['tid'] == '0':
						self.wakeupData['time'] = round(float(time) - float(self.startTime), 7)

					if nr == SystemInfo.sysWrite:
						self.wakeupData['tid'] = thread
						self.wakeupData['nr'] = nr
						self.wakeupData['args'] = args
						if self.wakeupData['valid'] > 0 and (self.wakeupData['tid'] == thread and self.wakeupData['from'] == comm): None
						else:
							self.wakeupData['valid'] += 1
							if self.wakeupData['valid'] > 1: self.wakeupData['corrupt'] = '1'
							else: self.wakeupData['corrupt'] = '0'

                                        try: self.threadData[thread]['syscallInfo']
                                        except: self.threadData[thread]['syscallInfo'] = {}
                                        try: self.threadData[thread]['syscallInfo'][nr]
                                        except: self.threadData[thread]['syscallInfo'][nr] = dict(self.init_syscallInfo)

                                        self.threadData[thread]['syscallInfo'][nr]['last'] = float(time)

                                        if len(SystemInfo.syscallList) > 0:
                                                try: idx = SystemInfo.syscallList.index(nr)
                                                except: idx = -1

                                                if idx >= 0: self.syscallData.append(['enter', time, thread, core, nr, args])
                                        else: self.syscallData.append(['enter', time, thread, core, nr, args])

			elif func == "sys_exit":
				m = re.match('^\s*NR (?P<nr>[0-9]+) = (?P<ret>[0-9]+)', etc)
				if m is not None:
					d = m.groupdict()

					nr = d['nr']
					ret = d['ret']

					if nr == SystemInfo.sysFutex and self.threadData[thread]['futexEnter'] > 0:
						self.threadData[thread]['futexCnt'] += 1
						futexTime = float(time) - self.threadData[thread]['futexEnter']
						if futexTime > self.threadData[thread]['futexMax']: 
							self.threadData[thread]['futexMax'] = futexTime
						self.threadData[thread]['futexTotal'] += futexTime

					if nr == SystemInfo.sysWrite and self.wakeupData['valid'] > 0:
						self.wakeupData['valid'] -= 1
					elif nr == SystemInfo.sysSelect or nr == SystemInfo.sysPoll or nr == SystemInfo.sysEpollwait:
						if (self.lastJob[core]['job'] == "sched_switch" or self.lastJob[core]['job'] == "sched_wakeup") and \
                                                        self.lastJob[core]['prevWakeupTid'] != thread:
							self.depData.append("\t%.3f/%.3f \t%16s %4s     %16s(%4s) \t%s" % (round(float(time) - float(self.startTime), 7), \
						 	round(float(time) - float(self.startTime) - float(self.wakeupData['time']), 7), " ", " ", self.threadData[thread]['comm'], \
						 	thread, "wakeup"))

							self.wakeupData['time'] = float(time) - float(self.startTime)
							self.lastJob[core]['prevWakeupTid'] = thread
					elif nr == SystemInfo.sysRecv:
						if self.lastJob[core]['prevWakeupTid'] != thread:
							self.depData.append("\t%.3f/%.3f \t%16s %4s     %16s(%4s) \t%s" % (round(float(time) - float(self.startTime), 7), \
						 	round(float(time) - float(self.startTime) - float(self.wakeupData['time']), 7), " ", " ", self.threadData[thread]['comm'], \
						 	thread, "recv"))

							self.wakeupData['time'] = float(time) - float(self.startTime)
							self.lastJob[core]['prevWakeupTid'] = thread

                                        try: self.threadData[thread]['syscallInfo']
                                        except: self.threadData[thread]['syscallInfo'] = {}
                                        try: self.threadData[thread]['syscallInfo'][nr]
                                        except: self.threadData[thread]['syscallInfo'][nr] = dict(self.init_syscallInfo)

                                        if self.threadData[thread]['syscallInfo'][nr]['last'] > 0:
                                                diff = float(time) - self.threadData[thread]['syscallInfo'][nr]['last']
                                                self.threadData[thread]['syscallInfo'][nr]['usage'] += diff
                                                self.threadData[thread]['syscallInfo'][nr]['last'] = 0

                                                if self.threadData[thread]['syscallInfo'][nr]['max'] == 0 or self.threadData[thread]['syscallInfo'][nr]['max'] < diff: 
                                                        self.threadData[thread]['syscallInfo'][nr]['max'] = diff
                                                if self.threadData[thread]['syscallInfo'][nr]['min'] <= 0 or self.threadData[thread]['syscallInfo'][nr]['min'] > diff: 
                                                        self.threadData[thread]['syscallInfo'][nr]['min'] = diff
                                                self.threadData[thread]['syscallInfo'][nr]['count'] += 1

					if len(SystemInfo.syscallList) > 0:
						try: idx = SystemInfo.syscallList.index(nr)
						except: idx = -1

						if idx >= 0: self.syscallData.append(['exit', time, thread, core, nr, ret])
                                        else: self.syscallData.append(['exit', time, thread, core, nr, ret])

			elif func == "signal_generate":
				m = re.match('^\s*sig=(?P<sig>[0-9]+) errno=(?P<err>[0-9]+) code=(?P<code>[0-9]+) comm=(?P<comm>.*) pid=(?P<pid>[0-9]+)', etc)
				if m is not None:
					d = m.groupdict()

					sig = d['sig']
					err = d['err']
					code = d['code']
					target_comm = d['comm']
					pid = d['pid']

					self.depData.append("\t%.3f/%.3f \t%16s(%4s) -> %16s(%4s) \t%s(%s)" % (round(float(time) - float(self.startTime), 7), \
					 round(float(time) - float(self.startTime) - float(self.wakeupData['time']), 7), self.threadData[thread]['comm'], \
					 thread, target_comm, pid, "sigsend", sig))

					self.wakeupData['time'] = float(time) - float(self.startTime)

			elif func == "signal_deliver":
				m = re.match('^\s*sig=(?P<sig>[0-9]+) errno=(?P<err>[0-9]+) code=(?P<code>[0-9]+) sa_handler=(?P<handler>[0-9]+) sa_flags=(?P<flags>[0-9]+)', etc)
				if m is not None:
					d = m.groupdict()

					sig = d['sig']
					err = d['err']
					code = d['code']
					handler = d['handler']
					flags = d['flags']

					self.depData.append("\t%.3f/%.3f \t%16s %4s     %16s(%4s) \t%s(%s)" % (round(float(time) - float(self.startTime), 7), \
					 round(float(time) - float(self.startTime) - float(self.wakeupData['time']), 7), "", "", \
					 self.threadData[thread]['comm'], thread, "sigrecv", sig))

					self.wakeupData['time'] = float(time) - float(self.startTime)

			elif func == "block_bio_remap":
				m = re.match('^\s*(?P<major>[0-9]+),(?P<minor>[0-9]+)\s*(?P<operation>\S+)\s*(?P<address>\S+)\s+\+\s+(?P<size>[0-9]+)', etc)
				if m is not None:
					d = m.groupdict()

					if d['operation'][0] != 'R': return
						
					bio = d['major'] + '/' + d['minor'] + '/' + d['operation'][0] + '/' + d['address']

                                        self.ioData[bio] = {'thread': thread, 'time': float(time), 'major': d['major'], 'minor': d['minor'], \
                                                'address': int(d['address']), 'size': int(d['size'])}

                                        self.threadData[thread]['reqBlock'] += int(d['size'])
                                        self.threadData[thread]['io_cnt'] += 1
                                        if self.threadData[thread]['io_start'] == 0:
                                                self.threadData[thread]['io_start'] = round(float(time), 7)

			elif func == "block_rq_complete":
				m = re.match('^\s*(?P<major>[0-9]+),(?P<minor>[0-9]+)\s*(?P<operation>\S+)\s*\(\S*\s*\)\s*(?P<address>\S+)\s+\+\s+(?P<size>[0-9]+)', etc)
				if m is not None:
					d = m.groupdict()

                                        address = d['address']
					size = d['size']

					bio = d['major'] + '/' + d['minor'] + '/' + d['operation'][0] + '/' + d['address']


                                        try:
                                                self.threadData[self.ioData[bio]['thread']]
                                                bioStart = int(address)
                                                bioEnd = int(address) + int(size)
                                        except: return

                                        for key, value in sorted(self.ioData.items(), key=lambda e: e[1]['address'], reverse=False):
                                                if self.ioData[key]['major'] == d['major'] and self.ioData[key]['minor'] == d['minor']:
                                                        if bioStart <= self.ioData[key]['address'] < bioEnd or \
                                                                bioStart < self.ioData[key]['address'] + self.ioData[key]['size'] <= bioEnd:

                                                                matchBlock = 0

                                                                if bioStart < self.ioData[key]['address']: matchStart = self.ioData[key]['address']
                                                                else: matchStart = bioStart

                                                                if bioEnd > self.ioData[key]['address'] + self.ioData[key]['size']: 
                                                                        matchEnd = self.ioData[key]['address'] + self.ioData[key]['size']
                                                                else: matchEnd = bioEnd

                                                                if matchStart == self.ioData[key]['address']:
                                                                        matchBlock = matchEnd - self.ioData[key]['address']
                                                                        self.ioData[key]['size'] = self.ioData[key]['address'] + self.ioData[key]['size'] - matchEnd
                                                                        self.ioData[key]['address'] = matchEnd 
                                                                elif matchStart > self.ioData[key]['address']:
                                                                        if matchEnd == self.ioData[key]['address'] + self.ioData[key]['size']:
                                                                                matchBlock = matchEnd - matchStart
                                                                                self.ioData[key]['size'] = matchStart - self.ioData[key]['address']
                                                                        else:
                                                                                del self.ioData[key]
                                                                                continue 
                                                                else: 
                                                                        del self.ioData[key]
                                                                        continue 

                                                                if bioEnd < self.ioData[key]['address'] + self.ioData[key]['size']: return

                                                                self.threadData[self.ioData[key]['thread']]['readBlock'] += matchBlock

                                                                if self.ioData[key]['size'] == 0:
                                                                        if self.threadData[self.ioData[key]['thread']]['io_cnt'] > 0:
                                                                                self.threadData[self.ioData[key]['thread']]['io_cnt'] -= 1

                                                                        if self.threadData[self.ioData[key]['thread']]['io_start'] > 0 and \
                                                                                self.threadData[self.ioData[key]['thread']]['io_cnt'] == 0:
                                                                                self.threadData[self.ioData[key]['thread']]['ioWait'] += \
                                                                                        round(float(time), 7) - self.threadData[self.ioData[key]['thread']]['io_start']
                                                                                self.threadData[self.ioData[key]['thread']]['io_start'] = 0

                                                                        del self.ioData[key]

			elif func == "mm_vmscan_wakeup_kswapd":
				try: self.reclaimData[thread]
				except: self.reclaimData[thread] = {'start': float(0)}

				if self.reclaimData[thread]['start'] <= 0:
					self.reclaimData[thread]['start'] = round(float(time), 7)

				self.threadData[thread]['reclaimCnt'] += 1

			elif func == "mm_vmscan_kswapd_sleep":
				for key,value in self.reclaimData.items():
					try: self.threadData[key]
					except: 
						self.threadData[key] = dict(self.init_threadData)
						self.threadData[key]['comm'] = comm

					self.threadData[key]['reclaimWait'] += round(float(time), 7) - round(float(value['start']), 7)
					del self.reclaimData[key]

			elif func == "mm_vmscan_direct_reclaim_begin":
				if self.threadData[thread]['dReclaimStart'] <= 0:
					self.threadData[thread]['dReclaimStart'] = round(float(time), 7)

				self.threadData[thread]['dReclaimCnt'] += 1

			elif func == "mm_vmscan_direct_reclaim_end":
				m = re.match('^\s*nr_reclaimed=(?P<nr>[0-9]+)', etc)
				if m is not None:
					d = m.groupdict()

					if self.threadData[thread]['dReclaimStart'] > 0:
						self.threadData[thread]['dReclaimWait'] += round(float(time), 7) - round(self.threadData[thread]['dReclaimStart'], 7)

					self.threadData[thread]['dReclaimStart'] = 0
					self.threadData[thread]['dReclaimCnt'] += int(d['nr'])

			elif func == "task_newtask":
				m = re.match('^\s*pid=(?P<pid>[0-9]+)\s+comm=(?P<comm>\S+)', etc)
				if m is not None:
					d = m.groupdict()

					pid = d['pid']

					try: self.threadData[pid]
					except: 
						self.threadData[pid] = dict(self.init_threadData)
						self.threadData[pid]['comm'] = d['comm']
						self.threadData[pid]['ppid'] = thread
						self.threadData[pid]['new'] = 'N'

			elif func == "task_rename":
				m = re.match('^\s*pid=(?P<pid>[0-9]+)\s+oldcomm=(?P<oldcomm>.*)\s+newcomm=(?P<newcomm>.*)\s+oom_score_adj', etc)
				if m is not None:
					d = m.groupdict()

					pid = d['pid']
					newcomm = d['newcomm']

					try: self.threadData[pid]
					except: 
						self.threadData[pid] = dict(self.init_threadData)
						self.threadData[pid]['comm'] = newcomm
						self.threadData[pid]['ppid'] = thread

					self.threadData[pid]['comm'] = newcomm

			elif func == "sched_process_free":
				m = re.match('^\s*comm=(?P<comm>.*)\s+pid=(?P<pid>[0-9]+)', etc)
				if m is not None:
					d = m.groupdict()

					pid = d['pid']

					try: self.threadData[pid]
					except: 
						self.threadData[pid] = dict(self.init_threadData)
						self.threadData[pid]['comm'] = d['comm']
						self.threadData[pid]['die'] = '1'

					self.threadData[pid]['die'] = 'D'

			elif func == "machine_suspend":
				m = re.match('^\s*state=(?P<state>[0-9]+)', etc)
				if m is not None:
					d = m.groupdict()

                                        if int(d['state']) == 3 : state = 'S'
                                        else: state = 'R'

                                        self.suspendData.append([time, state])

			elif func == "cpu_idle":
				m = re.match('^\s*state=(?P<state>[0-9]+)\s+cpu_id=(?P<cpu_id>[0-9]+)', etc)
				if m is not None:
					d = m.groupdict()

                                        tid = '0[' + d['cpu_id']+ ']'

                                        if self.threadData[tid]['coreSchedCnt'] == 0 and self.threadData[tid]['offTime'] == 0:
                                                self.threadData[tid]['offTime'] = float(time) - float(self.startTime)

                                        if int(d['state']) < 3:
                                                self.threadData[tid]['offCnt'] += 1 
                                                self.threadData[tid]['lastOff'] = float(time) 
                                        else:
                                                if self.threadData[tid]['lastOff'] > 0:
                                                        self.threadData[tid]['offTime'] += float(time) - self.threadData[tid]['lastOff']
                                                        self.threadData[tid]['lastOff'] = float(0)

			elif func == "power_frequency":
                                None

			elif func == "console":
				m = re.match('^\s*\[\s*(?P<time>\S+)\s*\]\s+EVENT_(?P<event>\S+)', etc)
				if m is not None:
					d = m.groupdict()

					event = d['event']

					# initialize ThreadInfo data #
					if event == 'START':
                                                self.threadData = {}
                                                self.irqData = {}
                                                self.ioData = {}
                                                self.reclaimData = {}
                                                self.pageTable = {}
                                                self.kmallocTable = {}
                                                self.intervalData = []
                                                self.depData = []
                                                self.syscallData = []
                                                self.lastJob = {}
                                                self.preemptData = []
                                                self.suspendData = []
                                                self.consoleData = []
						self.startTime = time
						ei.addEvent(time, event)
					# finish data processing #
					elif event == 'STOP':
						self.finishTime = time
						self.stopFlag = True
						ei.addEvent(time, event)
					# restart data processing for compare #
					elif event == 'RESTART':
						self.threadDataOld = self.threadData
						self.threadData = {}
						self.irqDataOld = self.irqData
						self.irqData = {}
						self.ioDataOld = self.ioData
						self.ioData = {}
						self.reclaimDataOld = self.reclaimData
						self.reclaimData = {}

						self.totalTimeOld = round(float(time), 7) - round(float(self.startTime), 7)
						self.startTime = time
						ei.addEvent(time, event)
					# process event #
					else: ei.addEvent(time, event)
                                else: self.consoleData.append([d['thread'], core, time, etc])

			elif func == "tracing_mark_write":
				m = re.match('^\s*EVENT_(?P<event>\S+)', etc)
				if m is not None:
					d = m.groupdict()

					event = d['event']

					# initialize ThreadInfo data #
					if event == 'START':
                                                self.threadData = {}
                                                self.irqData = {}
                                                self.ioData = {}
                                                self.reclaimData = {}
                                                self.pageTable = {}
                                                self.kmallocTable = {}
                                                self.intervalData = []
                                                self.depData = []
                                                self.syscallData = []
                                                self.lastJob = {}
                                                self.preemptData = []
                                                self.suspendData = []
                                                self.consoleData = []
						self.startTime = time
						ei.addEvent(time, event)
					# finish data processing #
					elif event == 'STOP':
						self.finishTime = time
						self.stopFlag = True
						ei.addEvent(time, event)
					# restart data processing for compare #
					elif event == 'RESTART':
						self.threadDataOld = self.threadData
						self.threadData = {}
						self.irqDataOld = self.irqData
						self.irqData = {}
						self.ioDataOld = self.ioData
						self.ioData = {}
						self.reclaimDataOld = self.reclaimData
						self.reclaimData = {}

						self.totalTimeOld = round(float(time), 7) - round(float(self.startTime), 7)
						self.startTime = time
						ei.addEvent(time, event)
					# process event #
					else: ei.addEvent(time, event)

			# save last job per core #
			try: self.lastJob[core]
			except: self.lastJob[core] = dict(self.init_lastJob)
				
			self.lastJob[core]['job'] = func
			self.lastJob[core]['time'] = time



    def compareThreadData(self):   
		for key,value in sorted(ti.threadData.items(), key=lambda e: e[1]['usage'], reverse=True):
			newPercent = round(float(value['usage']), 7) / round(float(ti.totalTime), 7) * 100

			try: ti.threadDataOld[key]
			except: 
				if int(newPercent) < 1:
					del ti.threadData[key]
				continue

			oldPercent = round(float(ti.threadDataOld[key]['usage']), 7) / round(float(ti.totalTimeOld), 7) * 100
			if int(oldPercent) >= int(newPercent) or int(newPercent) < 1:
				del ti.threadData[key]





if __name__ == '__main__':

	oneLine = "-"*144
	twoLine = "="*144

	# parse parameter #
	if len(sys.argv) <= 1:
		print("[ g.u.i.d.e.r \t%s ]" % SystemInfo.version)
		print '(ex.1) guider record'
		print '(ex.2) guider record -b[set_perCpu_buffer:kb] -q[make_taskchain] -e[enable_options:i|m]'
		print '(ex.2) guider record -s[save_traceData:dir] -o[set_outputFile:dir|file] -i[set_interval:sec]'
		print '(ex.2) guider record -f[show_threadflow] -p[show_preemptInfo:tids] -a[show_allThreads]'
		print '(ex.2) guider record -t[trace_syscall:syscallNums] -r[record_repeatData:interval,count]'
		print '(ex.2) guider record -d[disable_options:tty] -g[show_onlyGroup:comms]'
		print '(ex.3) guider [input file]'
		sys.exit(0)

	SystemInfo.inputFile = sys.argv[1]
	SystemInfo.outputFile = None

	# parse recording option #
	if sys.argv[1] == 'record':
		SystemInfo.inputFile = '/sys/kernel/debug/tracing/trace'

		# set this process RT priority #
		SystemInfo.setRtPriority('90')

		# save system information
		si = SystemInfo()

		if len(sys.argv) > 2:
			for n in range(2, len(sys.argv)):
				if sys.argv[n][0] == '-':
						if sys.argv[n][1] == 'b':
							try: int(sys.argv[n].lstrip('-b'))
							except: 
								print "[Error] wrong option value %s" % (sys.argv[n])
								sys.exit(0)
							if int(sys.argv[n].lstrip('-b')) > 0:
								si.bufferSize = str(sys.argv[n].lstrip('-b'))
							else:
								print "[Error] wrong option value %s" % (sys.argv[n].lstrip('-b'))
								sys.exit(0)
						elif sys.argv[n][1] == 'e':
							options = sys.argv[n].lstrip('-e')
							if options.rfind('i') != -1:
								SystemInfo.irqEnable = True 
								print "[Info] irq is enabled"
							if options.rfind('m') != -1:
								SystemInfo.memEnable = True 
								print "[Info] mem is enabled"
							if options.rfind('f') != -1:
								SystemInfo.futexEnable = True 
								print "[Info] futex is enabled"
						elif sys.argv[n][1] == 'g':
							if SystemInfo.outputFile != None:
								print "[Error] wrong option for -s, don't use -s option with -g option"
								sys.exit(0)
							SystemInfo.showGroup = sys.argv[n].lstrip('-g').split(',')
							SystemInfo.showAll = True
						elif sys.argv[n][1] == 's':
							if len(SystemInfo.showGroup) > 0:
								print "[Error] wrong option for -s, don't use -s option with -g option"
								sys.exit(0)
							SystemInfo.outputFile = str(sys.argv[n].lstrip('-s'))
                                                        if os.path.isdir(SystemInfo.outputFile) == True:
                                                                SystemInfo.outputFile = SystemInfo.outputFile + '/guider.dat'
                                                        elif os.path.isdir(SystemInfo.outputFile[:SystemInfo.outputFile.rfind('/')]) == True: None
                                                        else:
								print "[Error] wrong option value %s" % (sys.argv[n].lstrip('-s'))
								sys.exit(0)
						elif sys.argv[n][1] == 'f':
							SystemInfo.depEnable = True
						elif sys.argv[n][1] == 't':
                                                        SystemInfo.sysEnable = True
                                                        SystemInfo.syscallList = sys.argv[n].lstrip('-t').split(',')
                                                        for val in SystemInfo.syscallList:
                                                                try: int(val)
                                                                except: SystemInfo.syscallList.remove(val)
						elif sys.argv[n][1] == 'r':
							repeatParams = sys.argv[n].lstrip('-r').split(',')
							if len(repeatParams) != 2:
								print "[Error] wrong option for -r, use -r[interval],[repeat]"
								sys.exit(0)
							elif int(repeatParams[0]) < 1 or int(repeatParams[1]) < 1:
								print "[Error] wrong option for -r, use parameter bigger than 0"
								sys.exit(0)
							else:
								SystemInfo.repeatInterval = int(repeatParams[0])
								SystemInfo.repeatCount = int(repeatParams[1])
						elif sys.argv[n][1] == 'o':
							None
						elif sys.argv[n][1] == 'i':
							None
						elif sys.argv[n][1] == 'a':
							None
						elif sys.argv[n][1] == 'd':
							None
						elif sys.argv[n][1] == 'q':
							None
						elif sys.argv[n][1] == 'g':
							None
						elif sys.argv[n][1] == 'p':
							None
						else:
							print "[Error] wrong option -%s" % (sys.argv[n][1])
							sys.exit(0)
				else:
					print "[Error] wrong option %s" % (sys.argv[n])
					sys.exit(0)

		# set signal #
		if SystemInfo.repeatCount > 0 and SystemInfo.repeatInterval > 0:
			signal.signal(signal.SIGALRM, SystemInfo.alarmHandler)
			signal.alarm(SystemInfo.repeatInterval)
			if SystemInfo.outputFile is None:
				print "[Error] wrong option for -s, use parameter for saving data"
				sys.exit(0)
		else:
			signal.signal(signal.SIGINT, SystemInfo.stopHandler)
			signal.signal(signal.SIGQUIT, SystemInfo.newHandler)

		print 'start profiling... [ STOP(ctrl + c), COMPARE(ctrl + \) ]'
		si.runRecordStartCmd()

		#os.system('chrt -i 0 cat %s_pipe > %s &' % (SystemInfo.inputFile, SystemInfo.outputFile))

		# get init time in buffer for verification #
		initTime = ThreadInfo.getInitTime(SystemInfo.inputFile)

		while True:
			if SystemInfo.repeatInterval > 0:
				if SystemInfo.repeatCount == 0:
                                        si.runRecordStopCmd()
					sys.exit(0)

				# get init time in buffer for verification #
				initTime = ThreadInfo.getInitTime(SystemInfo.inputFile)

				signal.pause()

				if initTime != ThreadInfo.getInitTime(SystemInfo.inputFile):
					print "[Error] Buffer is not enough (%s KB) or Profile time is too long" % (si.getBufferSize())
                                        si.runRecordStopCmd()
					sys.exit(0)
                                else: SystemInfo.clearTraceBuffer()
			else: break

		signal.pause()

                si.runRecordStopCmd()

		if initTime != ThreadInfo.getInitTime(SystemInfo.inputFile):
			print "[Error] Buffer is not enough (%s KB) or Profile time is too long" % (si.getBufferSize())
			sys.exit(0)

		# save system information after profiling
		si.saveMeminfo()

	# parse default option #
	if len(sys.argv) > 2:
		for n in range(2, len(sys.argv)):
			if sys.argv[n][0] == '-':
					if sys.argv[n][1] == 'i':
						if len(sys.argv[n].lstrip('-i')) == 0:
							SystemInfo.intervalEnable = 1
							continue
						try: int(sys.argv[n].lstrip('-i'))
						except: 
							print "[Error] wrong option value %s" % (sys.argv[n])
                                                        si.runRecordStopCmd()
							sys.exit(0)
						if int(sys.argv[n].lstrip('-i')) >= 0:
							SystemInfo.intervalEnable = int(sys.argv[n].lstrip('-i'))
						else:
							print "[Error] wrong option value %s" % (sys.argv[n].lstrip('-i'))
                                                        si.runRecordStopCmd()
							sys.exit(0)
					elif sys.argv[n][1] == 'o':
						SystemInfo.printFile= str(sys.argv[n].lstrip('-o'))
						if os.path.isdir(SystemInfo.printFile) == False:
							print "[Error] wrong option value %s" % (sys.argv[n].lstrip('-o'))
                                                        si.runRecordStopCmd()
							sys.exit(0)
					elif sys.argv[n][1] == 'a':
						SystemInfo.showAll = True
					elif sys.argv[n][1] == 'q':
						SystemInfo.selectMenu = True
						ConfigInfo.makeConfig = True
					elif sys.argv[n][1] == 'f':
						SystemInfo.depEnable = True
					elif sys.argv[n][1] == 'p':
						if SystemInfo.intervalEnable != 1:
							SystemInfo.preemptGroup = sys.argv[n].lstrip('-p').split(',')
						else: print "[Warning] -i option is already enabled, -p option is disabled"
					elif sys.argv[n][1] == 'd':
						options = sys.argv[n].lstrip('-d')
						if options.rfind('tty') != -1:
							SystemInfo.ttyEnable = False
							print "[Info] tty is default"
					elif sys.argv[n][1] == 't':
                                                SystemInfo.sysEnable = True
                                                SystemInfo.syscallList = sys.argv[n].lstrip('-t').split(',')
                                                for val in SystemInfo.syscallList:
                                                        try: int(val)
                                                        except: SystemInfo.syscallList.remove(val)

					elif sys.argv[n][1] == 'g':
						SystemInfo.showGroup = sys.argv[n].lstrip('-g').split(',')
						SystemInfo.showAll = True
					elif sys.argv[n][1] == 'e':
						options = sys.argv[n].lstrip('-e')
                                                if options.rfind('g') != -1:
                                                    try:
                                                            from pylab import *
                                                            SystemInfo.graphEnable = True
                                                    except: 
                                                            print "[Warning] making graph is not supported"
                                                            SystemInfo.graphEnable = False
					elif sys.argv[n][1] == 'g':
						if SystemInfo.outputFile != None:
							print "[Error] wrong option for -s, don't use -s option with -g option"
                                                        si.runRecordStopCmd()
							sys.exit(0)
					elif sys.argv[n][1] == 'b':
						None
					elif sys.argv[n][1] == 's':
						None
					elif sys.argv[n][1] == 'r':
						None
					else:
						print "[Error] wrong option -%s" % (sys.argv[n][1])
                                                si.runRecordStopCmd()
						sys.exit(0)
			else:
				print "[Error] wrong option %s" % (sys.argv[n])
                                si.runRecordStopCmd()
				sys.exit(0)

	# Create Event Info #
	ei = EventInfo()

	# Create Thread Info #
	ti = ThreadInfo(SystemInfo.inputFile)
	count = 0
	hotLine = 20
	ti.totalTime = round(float(ti.finishTime), 7) - round(float(ti.startTime), 7)

        # filter group # 
	if len(SystemInfo.showGroup) > 0:
		for key,value in sorted(ti.threadData.items(), key=lambda e: e[1], reverse=False):
			checkResult = False
			for val in SystemInfo.showGroup:
				if value['comm'].rfind(val) != -1: checkResult = True
                        if checkResult == False and key[0:2] != '0[':
				try: del ti.threadData[key]
				except: None
        elif SystemInfo.sysEnable == True or len(SystemInfo.syscallList) > 0:
	        print "[Warning] -g option is not enabled, -t option is disabled"
                SystemInfo.sysEnable = False
                SystemInfo.syscallList = []

	# print title #
	if SystemInfo.printFile == None:
		os.system('clear')

	SystemInfo.pipePrint("[ g.u.i.d.e.r \tver.%s ]\n" % SystemInfo.version)

	if sys.argv[1] == 'record':
		# print memInfo #
		SystemInfo.pipePrint("(system)  MemSize: %9s  SwapSiz: %9s" % (si.memData['before']['MemTotal'], si.memData['before']['SwapTotal']))
		SystemInfo.pipePrint("(before)  MemFree: %9s  Buffers: %9s  Cached: %9s  SwapFree: %9s" % \
		(si.memData['before']['MemFree'], si.memData['before']['Buffers'], si.memData['before']['Cached'], si.memData['before']['SwapFree']))
		SystemInfo.pipePrint("( after)  MemFree: %9s  Buffers: %9s  Cached: %9s  SwapFree: %9s" % \
		(si.memData['after']['MemFree'], si.memData['after']['Buffers'], si.memData['after']['Cached'], si.memData['after']['SwapFree']))
		SystemInfo.pipePrint("(differ)  MemFree: %9s  Buffers: %9s  Cached: %9s  SwapFree: %9s" % \
		(int(si.memData['after']['MemFree']) - int(si.memData['before']['MemFree']), int(si.memData['after']['Buffers']) - \
		int(si.memData['before']['Buffers']), int(si.memData['after']['Cached']) - int(si.memData['before']['Cached']), \
		int(si.memData['after']['SwapFree']) - int(si.memData['before']['SwapFree'])))

	# print menu #
	SystemInfo.pipePrint("\n%0s[ %s: %0.3f ] [ Running: %d ] [ Logs : %d ] [ Keys: Foward / Back / Save / Quit ] [ Unit: Sec/MB ]" % \
	('', 'Elapsed time', round(float(ti.totalTime), 7), ti.getRunTaskNum(), ti.logCnt))
	SystemInfo.pipePrint(twoLine)
        SystemInfo.pipePrint("{0:_^29}|{1:_^25}|{2:_^24}|{3:_^11}|{4:_^25}|{5:_^24}|".\
                format("Thread Info", "CPU Info", "SCHED Info", "IO Info", "MEM Info", "ETC Info"))
        SystemInfo.pipePrint("{0:^29}|{1:^25}|{2:^24}|{3:^11}|{4:^25}|{5:^24}|".\
                format("", "", "", "", "", ""))
	SystemInfo.pipePrint("%16s(%5s/%5s)|%6s(%5s)|%6s(%3s)|%6s|%5s|%5s|%5s|%6s(%3s)|%6s|%5s|%7s(%3s)|%6s|%6s(%4s)|%2s|" % \
	('Name', 'Tid', 'PTid', 'Usage', '%', 'Delay', 'Pri', 'Yield', ' Lose', 'Steal', 'Mig', 'Read', 'MB', 'Alloc', 'Waste', 'Rclm', 'Cnt', \
    ' IRQ ', 'Futex', 'Cnt', 'Life'))
	SystemInfo.pipePrint(twoLine)

	# process idle time #
        for n in range(0, SystemInfo.maxCore + 1):
            try: ti.threadData['0[' + str(n) + ']']
            except: 
                ti.threadData['0[' + str(n) + ']'] = dict(ti.init_threadData)
                ti.threadData['0[' + str(n) + ']']['comm'] = 'swapper/' + str(n)
                ti.threadData['0[' + str(n) + ']']['usage'] = 0

	count = 0
	SystemInfo.clearPrint()
	for key,value in sorted(ti.threadData.items(), key=lambda e: e[1], reverse=False):
                if key[0:2] == '0[':
			value['comm'] = value['comm'].replace("swapper", "CORE");
			usagePercent = 100 - (round(float(value['usage']), 7) / round(float(ti.totalTime), 7) * 100)
                        if value['lastOff'] > 0:
                                value['offTime'] += float(ti.finishTime) - value['lastOff']
                        SystemInfo.addPrint("%16s(%5s/%5s)|%6.3f(%5s)|%6.3f(%3s)|%6d|%5d|%5d|%5s|%6.3f(%3d)|%6s|%5d|%7.3f(%3d)|%6.3f|%6.3f(%4d)| %s%s |\n" % \
                        (value['comm'], '0', '0', ti.totalTime - value['usage'], str(round(float(usagePercent), 1)), round(float(value['offTime']), 7), \
                        0, value['offCnt'], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ' ', ' '))
			count += 1
                else:
	            # convert priority #
                    prio = int(value['pri']) - 120
                    if prio >= -20: value['pri'] = str(prio)
                    else: value['pri'] = 'R%2s' % abs(prio + 21)

	SystemInfo.pipePrint("%s# %s: %d\n" % ('', 'CPU', count))
	SystemInfo.pipePrint(SystemInfo.bufferString)
	SystemInfo.pipePrint(oneLine)

	# compare thread information after sorting by time of cpu usage #
	if ti.threadDataOld != {}:
		ti.compareThreadData()

	# sorting by size of io usage and converting read blocks to MB size #
	count = 0
	for key,value in sorted(ti.threadData.items(), key=lambda e: e[1]['readBlock'], reverse=True):
		value['ioRank'] = count + 1
		if value['readBlock'] > 0:
		        value['readBlock'] =  value['readBlock'] * 512 / 1024 / 1024
			count += 1

	# print thread information after sorting by time of cpu usage #
	count = 0
	SystemInfo.clearPrint()
	for key,value in sorted(ti.threadData.items(), key=lambda e: e[1]['usage'], reverse=True):
                if key[0:2] == '0[': continue
		usagePercent = round(float(value['usage']), 7) / round(float(ti.totalTime), 7) * 100
		if round(float(usagePercent), 1) < 1 and SystemInfo.showAll == False: break
		else: 
			value['cpuRank'] = count + 1
			count += 1
	        SystemInfo.addPrint("%16s(%5s/%5s)|%6.3f(%5s)|%6.3f(%3s)|%6d|%5d|%5d|%5s|%6.3f(%3d)|%6s|%5d|%7.3f(%3d)|%6.3f|%6.3f(%4d)| %s%s |\n" % \
		(value['comm'], key, value['ppid'], value['usage'], str(round(float(usagePercent), 1)), value['cpuWait'], value['pri'], \
                value['yield'], value['preempted'], value['preemption'], value['migrate'], value['ioWait'], value['readBlock'], \
                (value['pages'] * 4 / 1024) + (value['usedMem'] / 1024 / 1024), value['wasteMem'] / 1024 / 1024, \
                value['dReclaimWait'], value['dReclaimCnt'], value['irq'], value['futexTotal'], value['futexCnt'], value['new'], value['die']))
	SystemInfo.pipePrint("%s# %s: %d\n" % ('', 'Hot', count))
	SystemInfo.pipePrint(SystemInfo.bufferString)
	SystemInfo.pipePrint(oneLine)

	# print thread preempted information after sorting by time of cpu usage #
	for val in SystemInfo.preemptGroup:
		index = SystemInfo.preemptGroup.index(val)
		count = 0
		SystemInfo.clearPrint()
		for key, value in sorted(ti.preemptData[index][1].items(), key=lambda e: e[1]['usage'], reverse=True):
			count += 1
			if float(ti.preemptData[index][4]) == 0: break
			SystemInfo.addPrint("%16s(%5s/%5s):  %6.3f(%.1f)\n" \
			% (ti.threadData[key]['comm'], key, '0', value['usage'], round(float(value['usage']), 7) / round(float(ti.preemptData[index][4]), 7) * 100))
		SystemInfo.pipePrint("%s# %s: Tid(%s) / Total(%6.3f) / Count(%d)\n" % ('', 'PRT', SystemInfo.preemptGroup[index], ti.preemptData[index][4], count))
		SystemInfo.pipePrint(SystemInfo.bufferString)
		SystemInfo.pipePrint(oneLine)

	# print new thread information after sorting by new thread flags #
	count = 0
	SystemInfo.clearPrint()
	for key,value in sorted(ti.threadData.items(), key=lambda e: e[1]['new'], reverse=True):
		if value['new'] == ' ' or SystemInfo.selectMenu != None: break
		count += 1
		if SystemInfo.showAll == True:
                        SystemInfo.addPrint("%16s(%5s/%5s)|%6.3f(%5s)|%6.3f(%3s)|%6d|%5d|%5d|%5s|%6.3f(%3d)|%6s|%5d|%7.3f(%3d)|%6.3f|%6.3f(%4d)| %s%s |\n" % \
                        (value['comm'], key, value['ppid'], value['usage'], str(round(float(usagePercent), 1)), value['cpuWait'], value['pri'], \
                        value['yield'], value['preempted'], value['preemption'], value['migrate'], value['ioWait'], value['readBlock'],\
                        (value['pages'] * 4 / 1024) + (value['usedMem'] / 1024 / 1024), value['wasteMem'] / 1024 / 1024, \
                        value['dReclaimWait'], value['dReclaimCnt'], value['irq'], value['futexTotal'], value['futexCnt'], value['new'], value['die']))
	if count > 0:
		SystemInfo.pipePrint("%s# %s: %d\n" % ('', 'New', count))
		SystemInfo.pipePrint(SystemInfo.bufferString)
		SystemInfo.pipePrint(oneLine)

	# print die thread information after sorting by die thread flags #
	count = 0
	SystemInfo.clearPrint()
	for key,value in sorted(ti.threadData.items(), key=lambda e: e[1]['die'], reverse=True):
		if value['die'] == ' ' or SystemInfo.selectMenu != None: break
		count += 1
		usagePercent = round(float(value['usage']), 7) / round(float(ti.totalTime), 7) * 100
		if SystemInfo.showAll == True:
                        SystemInfo.addPrint("%16s(%5s/%5s)|%6.3f(%5s)|%6.3f(%3s)|%6d|%5d|%5d|%5s|%6.3f(%3d)|%6s|%5d|%7.3f(%3d)|%6.3f|%6.3f(%4d)| %s%s |\n" % \
                        (value['comm'], key, value['ppid'], value['usage'], str(round(float(usagePercent), 1)), value['cpuWait'], value['pri'], \
                        value['yield'], value['preempted'], value['preemption'], value['migrate'], value['ioWait'], value['readBlock'],\
                        (value['pages'] * 4 / 1024) + (value['usedMem'] / 1024 / 1024), value['wasteMem'] / 1024 / 1024, \
                        value['dReclaimWait'], value['dReclaimCnt'], value['irq'], value['futexTotal'], value['futexCnt'], value['new'], value['die']))
	if count > 0:
		SystemInfo.pipePrint("%s# %s: %d\n" % ('', 'Die', count))
		SystemInfo.pipePrint(SystemInfo.bufferString)
		SystemInfo.pipePrint(oneLine)

	# print interrupt information #
        if len(ti.irqData) > 0: 
		SystemInfo.pipePrint('\n' + twoLine)
		SystemInfo.pipePrint("%16s(%16s): \t%6s\t\t%8s\t%8s\t%8s\t%8s\t%8s" % ("IRQ", "Name", "Count", "Usage", "ProcMax", "ProcMin", "InterMax", "InterMin"))
		SystemInfo.pipePrint(twoLine)

		SystemInfo.clearPrint()
		for key in sorted(ti.irqData.keys()):
			SystemInfo.addPrint("%16s(%16s): \t%6d\t\t%.6f\t%0.6f\t%0.6f\t%0.6f\t%0.6f\n" % \
			(key, ti.irqData[key]['name'], ti.irqData[key]['count'], ti.irqData[key]['usage'], ti.irqData[key]['max'], ti.irqData[key]['min'], \
			ti.irqData[key]['max_period'], ti.irqData[key]['min_period']))

		SystemInfo.pipePrint("%s# %s: %d\n" % ('', 'IRQ', len(ti.irqData)))
		SystemInfo.pipePrint(SystemInfo.bufferString)
		SystemInfo.pipePrint(oneLine)
	
	# set option for making graph #
	if SystemInfo.graphEnable == True and SystemInfo.intervalEnable > 0:
                print "[Info] graph is enabled"
                os.environ['DISPLAY'] = 'localhost:0'
		rc('legend', fontsize=5)
		rcParams.update({'font.size': 8})
        else: SystemInfo.graphEnable = False

	# process cpu usage time in timeline #
	if SystemInfo.intervalEnable > 0:
		SystemInfo.pipePrint('\n' + twoLine)
		# Total timeline #
		timeLine = ''
                checkSuspend = ' '
		for icount in range(1, int(float(ti.totalTime) / SystemInfo.intervalEnable) + 2):
                        for val in ti.suspendData:
                            if float(ti.startTime) + icount * SystemInfo.intervalEnable < float(val[0]) < float(ti.startTime) + 1 + icount * SystemInfo.intervalEnable:
                                if val[1] == 'S': checkSuspend = '!' 
                                else: checkSuspend = '>' 
                            else: checkSuspend = ' '
			timeLine += '%s%2d ' % (checkSuspend, icount * SystemInfo.intervalEnable)
		SystemInfo.pipePrint("%16s(%5s/%5s): %s" % ('Name', 'Tid', 'PTid', timeLine))
		SystemInfo.pipePrint(twoLine)
		SystemInfo.clearPrint()
		for key,value in sorted(ti.threadData.items(), key=lambda e: e[1], reverse=False):
                        if key[0:2] == '0[':
				icount = 0
				timeLine = ''
				for icount in range(0, int(float(ti.totalTime) / SystemInfo.intervalEnable) + 1):
					try: ti.intervalData[icount][key]
					except: 
						timeLine += '%3s ' % '0'
						continue
					timeLine += '%3d ' % (100 - ti.intervalData[icount][key]['cpuPer'])
				SystemInfo.addPrint("%16s(%5s/%5s): " % (value['comm'], '0', value['ppid']) + timeLine + '\n')
                
				if SystemInfo.graphEnable == True:
					subplot(2,1,1)
					timeLineData = [int(n) for n in timeLine.split()]
					range(SystemInfo.intervalEnable, (len(timeLineData)+1)*SystemInfo.intervalEnable, SystemInfo.intervalEnable)
					plot(range(SystemInfo.intervalEnable, (len(timeLineData)+1)*SystemInfo.intervalEnable, SystemInfo.intervalEnable), timeLineData, '.-') 
					SystemInfo.graphLabels.append(value['comm'])

		if SystemInfo.graphEnable == True:
			title('Core Usage')
			ylabel('Percentage(%)', fontsize=10)
			legend(SystemInfo.graphLabels, bbox_to_anchor=(1.135, 1.02))
			del SystemInfo.graphLabels[:]

	        # process total MEM in timeline #
                icount = 0
                timeLine = ''
		SystemInfo.addPrint('\n')
                for icount in range(0, int(float(ti.totalTime) / SystemInfo.intervalEnable) + 1):
                        try: timeLine += '%3d ' % (ti.intervalData[icount]['toTal']['totalMem'] * 4 / 1024)
                        except: timeLine += '%3d ' % (0)
                SystemInfo.addPrint("%16s(%5s/%5s): " % ('MEM', '0', value['ppid']) + timeLine + '\n')

	        # process total I/O in timeline #
                icount = 0
                timeLine = ''
                for icount in range(0, int(float(ti.totalTime) / SystemInfo.intervalEnable) + 1):
                        try: timeLine += '%3d ' % (ti.intervalData[icount]['toTal']['totalIo'] * 512 / 1024 / 1024)
                        except: timeLine += '%3d ' % (0)
                SystemInfo.addPrint("%16s(%5s/%5s): " % ('I/O', '0', value['ppid']) + timeLine + '\n')

		SystemInfo.pipePrint("%s# %s\n" % ('', 'Total(%/MB)'))
		SystemInfo.pipePrint(SystemInfo.bufferString)
		SystemInfo.pipePrint(oneLine)
		SystemInfo.clearPrint()
		tcount = 0;

		# CPU timeline #
		for key,value in sorted(ti.threadData.items(), key=lambda e: e[1]['usage'], reverse=True):
                        if key[0:2] != '0[':
				icount = 0
				timeLine = ''
				for icount in range(0, int(float(ti.totalTime) / SystemInfo.intervalEnable) + 1):
					try: ti.intervalData[icount][key]
					except: 
						timeLine += '%3d ' % 0
						continue
					timeLine += '%3d ' % (ti.intervalData[icount][key]['cpuPer'])
				SystemInfo.addPrint("%16s(%5s/%5s): " % (value['comm'], key, value['ppid']) + timeLine + '\n')

				if SystemInfo.graphEnable == True:
					subplot(2,1,2)
					timeLineData = [int(n) for n in timeLine.split()]
					plot(range(SystemInfo.intervalEnable, (len(timeLineData)+1)*SystemInfo.intervalEnable, SystemInfo.intervalEnable), timeLineData, '.-') 
					SystemInfo.graphLabels.append(value['comm'])

				try: ti.intervalData[icount][key]
				except: ti.intervalData[icount][key] = dict(ti.init_intervalData)
				if ti.intervalData[icount][key]['totalUsage'] / float(ti.totalTime) * 100 < 1 and SystemInfo.showAll == False:
					break;

		if SystemInfo.graphEnable == True:
			title('CPU Usage of Threads')
			ylabel('Percentage(%)', fontsize=10)
			legend(SystemInfo.graphLabels, bbox_to_anchor=(1.135, 1.02))
			del SystemInfo.graphLabels[:]
			figure(num=1, figsize=(20, 20), dpi=200, facecolor='b', edgecolor='k')
			savefig("cpuInfo.png",dpi=(200))
			clf()

		SystemInfo.pipePrint("%s# %s\n" % ('', 'CPU(%)'))
		SystemInfo.pipePrint(SystemInfo.bufferString)
		SystemInfo.pipePrint(oneLine)

		# IO timeline #
		SystemInfo.clearPrint()
		for key,value in sorted(ti.threadData.items(), key=lambda e: e[1]['reqBlock'], reverse=True):
                        if key[0:2] != '0[':
				icount = 0
				timeLine = ''
				for icount in range(0, int(float(ti.totalTime) / SystemInfo.intervalEnable) + 1):
					try: ti.intervalData[icount][key]
					except: 
						timeLine += '%3d ' % 0
						continue
					timeLine += '%3d ' % (ti.intervalData[icount][key]['ioUsage'] * 512 / 1024 / 1024)
				SystemInfo.addPrint("%16s(%5s/%5s): " % (value['comm'], key, value['ppid']) + timeLine + '\n')

				if SystemInfo.graphEnable == True:
					subplot(2,1,1)
					timeLineData = [int(n) for n in timeLine.split()]
					plot(range(SystemInfo.intervalEnable, (len(timeLineData)+1)*SystemInfo.intervalEnable, SystemInfo.intervalEnable), timeLineData, '.-') 
					SystemInfo.graphLabels.append(value['comm'])

				try: ti.intervalData[icount][key]
				except: ti.intervalData[icount][key] = dict(ti.init_intervalData)
				if ti.intervalData[icount][key]['totalIoUsage'] * 512 / 1024 / 1024 < 1 and SystemInfo.showAll == False:
					break;

		if SystemInfo.graphEnable == True:
			title('Disk Usage of Threads')
			ylabel('Size(MB)', fontsize=10)
			legend(SystemInfo.graphLabels, bbox_to_anchor=(1.135, 1.02))
			del SystemInfo.graphLabels[:]
	
		SystemInfo.pipePrint("%s# %s\n" % ('', 'I/O(MB)'))
		SystemInfo.pipePrint(SystemInfo.bufferString)
		SystemInfo.pipePrint(oneLine)

		# Memory timeline #
		SystemInfo.clearPrint()
		if SystemInfo.memEnable == True:
			for key,value in sorted(ti.threadData.items(), key=lambda e: e[1]['pages'], reverse=True):
                                if key[0:2] != '0[':
					icount = 0
					timeLine = ''
					for icount in range(0, int(float(ti.totalTime) / SystemInfo.intervalEnable) + 1):
						try: ti.intervalData[icount][key]
						except: 
							timeLine += '%3d ' % 0
							continue
						timeLine += '%3d ' % (ti.intervalData[icount][key]['memUsage'] * 4 / 1024)
					SystemInfo.addPrint("%16s(%5s/%5s): " % (value['comm'], key, value['ppid']) + timeLine + '\n')

					if SystemInfo.graphEnable == True:
						subplot(2,1,2)
						timeLineData = [int(n) for n in timeLine.split()]
						plot(range(SystemInfo.intervalEnable, (len(timeLineData)+1)*SystemInfo.intervalEnable, SystemInfo.intervalEnable), timeLineData, '.-') 
						SystemInfo.graphLabels.append(value['comm'])

					try: ti.intervalData[icount][key]
					except: ti.intervalData[icount][key] = dict(ti.init_intervalData)
					if ti.intervalData[icount][key]['totalMemUsage'] < 1024 and SystemInfo.showAll == False:
						break;

			SystemInfo.pipePrint("%s# %s\n" % ('', 'MEM(MB)'))
			SystemInfo.pipePrint(SystemInfo.bufferString)
			SystemInfo.pipePrint(oneLine)

			if SystemInfo.graphEnable == True:
				title('MEM Usage of Threads')
				ylabel('Size(MB)', fontsize=10)
				legend(SystemInfo.graphLabels, bbox_to_anchor=(1.135, 1.02))
				del SystemInfo.graphLabels[:]

		if SystemInfo.graphEnable == True:
			figure(num=1, figsize=(20, 20), dpi=200, facecolor='b', edgecolor='k')
			savefig("ioInfo.png",dpi=(200))

	# print Dependency #
	if SystemInfo.depEnable == True:
		SystemInfo.clearPrint()
		SystemInfo.pipePrint('\n' + twoLine)
		SystemInfo.pipePrint("\t%5s/%4s \t%16s(%4s) -> %16s(%4s) \t%5s" % ("Total", "Inter", "From", "Tid", "To", "Tid", "Event"))
		SystemInfo.pipePrint(twoLine)
		SystemInfo.pipePrint("%s# %s: %d\n" % ('', 'Dep', len(ti.depData)))

		for icount in range(0, len(ti.depData)):
			SystemInfo.addPrint(ti.depData[icount] + '\n')

		SystemInfo.pipePrint(SystemInfo.bufferString)
		SystemInfo.pipePrint(oneLine)

	# print Events #
	if len(ei.eventData) > 0:
		SystemInfo.pipePrint('\n' + twoLine)
		SystemInfo.pipePrint("%s# %s: %d\n" % ('', 'EVT', len(ei.eventData)))
		ei.printEvent(ti.startTime)
		SystemInfo.pipePrint(twoLine)

	# print console messages #
	if len(ti.consoleData) > 0 and SystemInfo.showAll == True:
		SystemInfo.pipePrint('\n' + twoLine)
		SystemInfo.pipePrint("%16s %5s %4s %10s %s" % ('Name', 'Tid', 'Core', 'Time', 'Console message'))
		SystemInfo.pipePrint(twoLine)
                for msg in ti.consoleData:
                    try:
		            SystemInfo.pipePrint("%16s %5s %4s %10.3f %s" % \
                                    (ti.threadData[msg[0]]['comm'], msg[0], msg[1], round(float(msg[2]) - float(ti.startTime), 7), msg[3]))
                    except: continue
		SystemInfo.pipePrint(twoLine)

	# print syscall log #
	count = 0
	SystemInfo.clearPrint()
	if ti.syscallData != []:
                if len(SystemInfo.showGroup) > 0:
                        SystemInfo.pipePrint('\n' + twoLine)
                        SystemInfo.pipePrint("%16s(%4s)\t%7s\t\t%6s\t\t%6s\t\t%6s\t\t%6s\t\t%6s" % ("Name", "Tid", "SysId", "Usage", "Count", "Min", "Max", "Avg"))
                        SystemInfo.pipePrint(twoLine)

                        for key,value in sorted(ti.threadData.items(), key=lambda e: e[1]['comm']):
                                if key[0:2] == '0[': continue
                                SystemInfo.pipePrint("%16s(%4s)" % (ti.threadData[key]['comm'], key))
                                try:
                                        for sysId,val in sorted(ti.threadData[key]['syscallInfo'].items(), key=lambda e: e[1]['usage'], reverse=True):
                                                if val['count'] > 0:
                                                        val['average'] = val['usage'] / val['count']
                                                        SystemInfo.pipePrint("\t%27s\t\t%6.3f\t\t%6d\t\t%6.3f\t\t%6.3f\t\t%6.3f\n" % \
                                                        (sysId, val['usage'], val['count'], val['min'], val['max'], val['average']))
                                except: continue
                        SystemInfo.pipePrint(SystemInfo.bufferString)
                        SystemInfo.pipePrint(oneLine)

	        SystemInfo.clearPrint()
                if SystemInfo.showAll == True:
                        SystemInfo.pipePrint('\n' + twoLine)
                        SystemInfo.pipePrint("%16s(%4s)\t%8s\t%5s\t%6s\t%4s\t%s" % ("Name", "Tid", "Time", "Type", "NR", "Core", "Value"))
                        SystemInfo.pipePrint(twoLine)

                        for icount in range(0, len(ti.syscallData)):
                                try:
                                        SystemInfo.addPrint("%16s(%4s)\t%6.6f\t%5s\t%6s\t%4s\t%s\n" % \
                                        (ti.threadData[ti.syscallData[icount][2]]['comm'], ti.syscallData[icount][2], round(float(ti.syscallData[icount][1]) - float(ti.startTime), 7), \
                                        ti.syscallData[icount][0], ti.syscallData[icount][4], ti.syscallData[icount][3], ti.syscallData[icount][5]))
                                        if ti.syscallData[icount][0] == 'enter':
                                                count += 1
                                except: None
                        SystemInfo.pipePrint("%s# %s: %d\n" % ('', 'Sys', count))
                        SystemInfo.pipePrint(SystemInfo.bufferString)
                        SystemInfo.pipePrint(oneLine)

	# set handler for exit #
	signal.signal(signal.SIGINT, SystemInfo.exitHandler)

	# get Input for taskchain #
	if SystemInfo.selectMenu != None:
		if ConfigInfo.makeConfig == True:
			while True:
				eventInput = raw_input('Input event name for taskchain: ')
				fd = ConfigInfo.openConfFile(eventInput)
				if fd != None: break
					
			ConfigInfo.writeConfData(fd, '[%s]\n' % (eventInput))
			threadInput = raw_input('Input tids of hot threads for taskchain (ex. 13,144,235): ')
			threadList = threadInput.split(',')
			ConfigInfo.writeConfData(fd, 'nr_tid=' + str(len(threadList)) + '\n')
			for index, t in enumerate(threadList):
				cmdline = ConfigInfo.readProcData(t, 'cmdline', 0)
				if cmdline == None: continue

				cmdline = cmdline[0:cmdline.find('\x00')]
				cmdline = cmdline[0:cmdline.rfind('/')]
				cmdline = cmdline.replace(' ','-')
				if len(cmdline) > 256: cmdline = cmdline[0:255]

				try: ti.threadData[t]
				except: 
					SystemInfo.pipePrint("[Warning] thread %s is not in profiled data" % t)
					continue

				ConfigInfo.writeConfData(fd, str(index) + '=' + ConfigInfo.readProcData(t, 'stat', 2).replace('\x00','-') + '+' + \
				cmdline + ' ' + str(ti.threadData[t]['ioRank']) + ' ' + str(ti.threadData[t]['reqBlock']) + ' ' + str(ti.threadData[t]['cpuRank']) + \
				' ' + str(ti.threadData[t]['usage']) + '\n')

			SystemInfo.pipePrint("%s.tc is wrote successfully" % eventInput)

	# print output file name #
	if SystemInfo.printFile != None:
		print "[Info] wrote output to %s successfully" % (SystemInfo.inputFile)
