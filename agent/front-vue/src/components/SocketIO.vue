<template>
  <div>
    <b-row>
      <b-col sm="6">
        <b-form-input
          type="text"
          v-model="targetAddr"
          @keyup.enter="emitStart"
          aria-describedby="input-description-help"
        />
        <b-form-text id="input-description-help">
          Input the guider target IP addr and port (ex> 192.168.24.12:5000)
        </b-form-text>
      </b-col>
      <b-col sm="2">
        <b-btn id="emitStart" @click="emitStart">
          Start
        </b-btn>
      </b-col>
      <b-col sm="2">
        <b-btn id="disconnectSocket" @click="disconnectSocket">
          Stop
        </b-btn>
      </b-col>
    </b-row>
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
      EventBus.$emit("cpu_usage", msg.cpu);
      EventBus.$emit("mem_usage", msg.memory);
      // EventBus.$emit("proc_usage", procUsage);
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
    }
  }
};
</script>
