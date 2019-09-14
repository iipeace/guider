<template>
  <div>
    <div>
        <font size=2>Input the guider target IP addr and port (ex> 192.168.24.12:5000) </font>
        <input type="text" v-model="targetAddr" @keyup.enter="emitStart"/>
        <button class="basic-button" id="emitStart" @click="emitStart">Start</button>
        <button class="basic-button" id="disconnectSocket" @click="disconnectSocket">Stop</button>
    </div>
  </div>
</template>

<script>
import { EventBus } from '../event-bus'

export default {
  name: 'socket-io',
  data () {
    return {
      clientMsg: '',
      log: '',
      targetTimestamp: '',
      emitCount: 0,
      arrProcParam: ['nrThreads', 'mem', 'life', 'comm', 'ttime', 'PPID'],
      targetAddr: ''
    }
  },
  sockets: {
    connect: function () {
      this.connectSocket()
    },
    server_response: function (msg) { // msg is json
      EventBus.$emit('cnt_emit', this.emitCount)
      var cpuUsage = this.refineCpuPipe(msg.cpu_pipe)
      EventBus.$emit('cpu_usage', cpuUsage)
      var memUsage = this.refineMemPipe(msg.mem_pipe)
      EventBus.$emit('mem_usage', memUsage)
      var procUsage = this.refineProcPipe(msg.proc_pipe)
      EventBus.$emit('proc_usage', procUsage)
      this.emitCount = this.emitCount + 1
    },
    request_stop_result: function (msg) {
      this.appendLog(msg)
    }
  },
  methods: {
    emitStart: function () {
      console.log('Start button Clicked!')
      var timestamp = +new Date()
      EventBus.$emit('reset_data')
      this.$socket.emit('request_start', String(timestamp), this.targetAddr)
    },
    emitStop: function () {
      console.log('Stop button Clicked!')
      this.$socket.emit('request_stop', this.targetTimestamp)
    },
    appendLog: function (newLog) {
      this.log += newLog + '\n'
    },
    disconnectSocket: function () {
      this.$socket.disconnect()
    },
    connectSocket: function () {
      this.$socket.connect() // if connection is not establised.
    },
    refineCpuPipe: function (cpu_pipe) {
      var jsonObj = JSON.parse(cpu_pipe)
      var cpuTotal = new Array()
      var jsonPercore = jsonObj.percore
      var logCpu = 'Emit Count <' + String(this.emitCount) + '>    :  '
      for (let i = 0; i < jsonObj.nrCore; i++) {
        cpuTotal.push(jsonPercore[i].total)
        logCpu = logCpu + 'core[' + String(i + 1) + '] : ' + jsonPercore[i].total + '     / '
      }
      // this.appendLog(logCpu);
      return cpuTotal
    },
    refineMemPipe: function (mem_pipe) {
      var jsonObj = JSON.parse(mem_pipe)
      var memTotal = {}
      var arrDisp = ['total', 'available', 'kernel', 'anon', 'cache', 'free']
      for (var key in jsonObj) {
        if (arrDisp.includes(key) === true) {
          memTotal[key] = jsonObj[key]
        }
      }
      return memTotal
    },
    refineProcPipe: function (proc_pipe) {
      var jsonObj = JSON.parse(proc_pipe)
      var procTotal = new Array() // Json Array to return

      for (var keyPID in jsonObj) { // key is PID.
        var objPID = {}
        objPID['PID'] = keyPID
        for (var keyParam in jsonObj[keyPID]) {
          if (this.arrProcParam.includes(keyParam) === true) {
            objPID[keyParam] = jsonObj[keyPID][keyParam]
          }
        }
        procTotal.push(objPID)
      }
      return procTotal
    }
  }
}
</script>
