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
          Input the guider target IP addr and port (ex> 192.168.24.12:5000)
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
export default {
  name: "socket-io",
  data() {
    return {
      targetAddr: ""
    };
  },
  created() {
    this.targetAddr = this.$store.getters.getTargetAddr;
  },
  methods: {
    setTargetAddr: function() {
      this.$store.commit("setTargetAddr", this.targetAddr);
    }
  }
};
</script>
