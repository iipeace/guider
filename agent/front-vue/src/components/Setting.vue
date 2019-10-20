<template>
  <div class="container-fluid">
    <b-row>
      <b-col sm="8">
        <b-form-input
          type="text"
          v-model="targetAddr"
          aria-describedby="input-description-help"
        ></b-form-input>
        <b-form-text id="input-description-help">
          Input the Guider's IP and PORT to connect [ ex) 127.0.0.1:5555 ]
        </b-form-text>
      </b-col>
      <b-col>
        <b-btn @click="setTargetAddr">
          SET
        </b-btn>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import { mapState } from "vuex";
import { Server } from "../model/server";

export default {
  data() {
    return {
      targetAddr: "",
      healthCheckInterval: null,
      interval: 10000,
      retry: 0
    };
  },
  computed: {
    ...mapState(["server"])
  },
  created() {
    if (this.server) {
      this.targetAddr = this.server.targetAddr;
    }
  },
  methods: {
    setTargetAddr: function() {
      if (!this.targetAddr) {
        alert("this value must not empty");
        return;
      }
      const server = new Server(this.targetAddr);
      this.$store.commit("setServer", server);
      server.healthCheck(this.sockets, this.$socket);
    }
  }
};
</script>
