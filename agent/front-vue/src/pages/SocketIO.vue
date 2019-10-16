<template>
  <div class="container-fluid">
    <b-row>
      <b-col sm="6">
        <b-form-input
          type="text"
          v-model="targetAddr"
          @keyup.enter="emitStart"
          aria-describedby="input-description-help"
        ></b-form-input>
        <b-form-text id="input-description-help">
          Input the guider target IP addr and port (ex> 192.168.24.12:5000)
        </b-form-text>
      </b-col>
      <b-col sm="2">
        <b-btn v-if="!connected" id="emitStart" @click="emitStart">
          Connect
          <font-awesome-icon icon="circle" style="color:#00CC6A" />
        </b-btn>
        <b-btn v-else id="disconnectSocket" @click="disconnectSocket">
          Disconnect
          <font-awesome-icon icon="circle" style="color:#FF0000" />
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
      arrProcParam: ["nrThreads", "mem", "life", "comm", "ttime", "PPID"],
      targetAddr: "",
      connected: false
    };
  },
  sockets: {
    connect: function() {
      this.connectSocket();
    },
    server_response: function(data) {
      EventBus.$emit("setDashboardData", data);
    },
    request_stop_result: function(msg) {
      this.appendLog(msg);
    }
  },
  methods: {
    emitStart: function() {
      // if (!this.targetAddr) {
      //   alert("Enter Server Address");
      //   return false;
      // }
      this.connectSocket();
      const timestamp = new Date();
      this.targetTimestamp = String(timestamp);
      this.$socket.emit("request_start", this.targetTimestamp, this.targetAddr);
      this.connected = true;
    },
    emitStop: function() {
      this.$socket.emit("request_stop", this.targetTimestamp);
    },
    appendLog: function(newLog) {
      this.log += newLog + "\n";
    },
    disconnectSocket: function() {
      this.$socket.emit("request_stop", this.targetTimestamp);
      this.targetTimestamp = "";
      this.$socket.disconnect();
      this.connected = false;
    },
    connectSocket: function() {
      this.$socket.connect(); // if connection is not establised.
    }
  }
};
</script>
