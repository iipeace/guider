<template>
  <div>
    <div>
      <font size="2"
        >Input the guider target IP addr and port (ex> 192.168.24.12:5000)
      </font>
      <input type="text" v-model="targetAddr" @keyup.enter="emitStart" />
      <button class="basic-button" id="emitStart" @click="emitStart">
        Start
      </button>
      <button
        class="basic-button"
        id="disconnectSocket"
        @click="disconnectSocket"
      >
        Stop
      </button>
    </div>
  </div>
</template>

<script>
import { EventBus } from "../event-bus";

export default {
  name: "socket-io",
  data() {
    return {
      clientMsg: "",
      log: "",
      targetTimestamp: "",
      emitCount: 0,
      arrProcParam: ["nrThreads", "mem", "life", "comm", "ttime", "PPID"],
      targetAddr: ""
    };
  },
  sockets: {
    connect: function() {
      this.connectSocket();
    },
    server_response: function(msg) {
      // msg is json
      EventBus.$emit("cnt_emit", this.emitCount);
      const cpuUsage = this.refineCpuPipe(msg.cpu_pipe);
      EventBus.$emit("cpu_usage", cpuUsage);
      const memUsage = this.refineMemPipe(msg.mem_pipe);
      EventBus.$emit("mem_usage", memUsage);
      const procUsage = this.refineProcPipe(msg.proc_pipe);
      EventBus.$emit("proc_usage", procUsage);
      this.emitCount = this.emitCount + 1;
    },
    request_stop_result: function(msg) {
      this.appendLog(msg);
    }
  },
  methods: {
    emitStart: function() {
      const timestamp = new Date();
      EventBus.$emit("reset_data");
      this.$socket.emit("request_start", String(timestamp), this.targetAddr);
    },
    emitStop: function() {
      this.$socket.emit("request_stop", this.targetTimestamp);
    },
    appendLog: function(newLog) {
      this.log += newLog + "\n";
    },
    disconnectSocket: function() {
      this.$socket.disconnect();
    },
    connectSocket: function() {
      this.$socket.connect(); // if connection is not establised.
    },
    refineCpuPipe: function(pipe) {
      const jsonObj = JSON.parse(pipe);
      const cpuTotal = [];
      const jsonPercore = jsonObj.percore;
      let logCpu = "Emit Count <" + String(this.emitCount) + ">    :  ";
      for (let i = 0; i < jsonObj.nrCore; i++) {
        cpuTotal.push(jsonPercore[i].total);
        logCpu =
          logCpu +
          "core[" +
          String(i + 1) +
          "] : " +
          jsonPercore[i].total +
          "     / ";
      }
      // this.appendLog(logCpu);
      return cpuTotal;
    },
    refineMemPipe: function(pipe) {
      const jsonObj = JSON.parse(pipe);
      const memTotal = {};
      const arrDisp = ["total", "available", "kernel", "anon", "cache", "free"];
      for (let key in jsonObj) {
        if (arrDisp.includes(key) === true) {
          memTotal[key] = jsonObj[key];
        }
      }
      return memTotal;
    },
    refineProcPipe: function(pipe) {
      const jsonObj = JSON.parse(pipe);
      const procTotal = []; // Json Array to return

      for (let keyPID in jsonObj) {
        // key is PID.
        const objPID = {};
        objPID["PID"] = keyPID;
        for (let keyParam in jsonObj[keyPID]) {
          if (this.arrProcParam.includes(keyParam) === true) {
            objPID[keyParam] = jsonObj[keyPID][keyParam];
          }
        }
        procTotal.push(objPID);
      }
      return procTotal;
    }
  }
};
</script>
