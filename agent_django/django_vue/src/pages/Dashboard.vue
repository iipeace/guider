<template>
  <div class="container-fluid">
    <b-row>
      <b-col sm="12">
        <b-btn v-if="isRun" @click="stopCommandRun" style="float: right;"
          >STOP</b-btn
        >
        <b-btn v-else @click="getDashboardData" style="float: right;"
          >START</b-btn
        >
      </b-col>
      <b-col sm="6">
        <b-card style="background: white; ">
          <vue-apex-charts
            height="auto"
            type="area"
            :options="dataSet.memoryChartOptions"
            :series="dataSet.memorySeries"
          />
        </b-card>
      </b-col>
      <b-col sm="6">
        <b-card style="background: white; ">
          <vue-apex-charts
            height="auto"
            type="area"
            :options="dataSet.cpuChartOptions"
            :series="dataSet.cpuSeries"
          />
        </b-card>
      </b-col>
      <b-col sm="6">
        <b-card style="background: white; ">
          <vue-apex-charts
            height="auto"
            type="area"
            :options="dataSet.storageChartOptions"
            :series="dataSet.storageSeries"
          />
        </b-card>
      </b-col>
      <b-col sm="6">
        <b-card style="background: white; ">
          <vue-apex-charts
            height="auto"
            type="line"
            :options="dataSet.networkChartOptions"
            :series="dataSet.networkSeries"
          />
        </b-card>
      </b-col>
    </b-row>
  </div>
</template>
<script>
import { EventBus } from "../event-bus";
import VueApexCharts from "vue-apexcharts";
import GuiderGraphDataSet from "../model/guider-graph-data-set";
import { mapState } from "vuex";

export default {
  components: {
    VueApexCharts
  },
  data: function() {
    return {
      dataSet: new GuiderGraphDataSet(),
      isRun: false,
      requestId: ""
    };
  },
  computed: {
    ...mapState(["server"])
  },
  sockets: {
    set_dashboard_data: function(data) {
      if (data.result === 0) {
        this.dataSet.setGuiderData(data.data);
      } else if (data.result < 0) {
        this.isRun = false;
        this.stopCommandRun();
        alert(data.errorMsg);
      }
    }
  },
  methods: {
    getDashboardData() {
      if (!this.server.hasTargetAddr()) {
        alert("please set target address");
        return false;
      }

      if (this.isRun) {
        alert("command alredy run");
        return false;
      }

      try {
        this.isRun = true;
        this.requestId = "dashboard" + String(new Date());
        this.$socket.emit(
          "get_dashboard_data",
          this.requestId,
          this.server.targetAddr
        );
      } catch (e) {
        this.isRun = false;
      }
    },
    stopCommandRun() {
      this.isRun = false;
      this.$socket.emit("stop_command_run", this.requestId);
      this.requestId = "";
    }
  },
  mounted() {
    EventBus.$on("setDashboardData", data => {
      this.dataSet.setGuiderData(data);
    });
  },
  beforeDestroy() {
    this.stopCommandRun();
  }
};
</script>
<style></style>
