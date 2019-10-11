<template>
  <div>
    <div>
      <span
        style="font-size: x-small; ">Input the guider target IP addr and port (ex> 192.168.24.12:5000)
      </span>
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
      arrProcParam: ["nrThreads", "mem", "life", "comm", "ttime", "PPID"],
      targetAddr: ""
    };
  },
  sockets: {
    connect: function() {
      this.connectSocket();
    },
    server_response: function(data) {
      EventBus.$emit('setDashboardData', data)
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
  }
};
</script>
