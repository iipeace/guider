<template>
  <div class="container-fluid">
    <b-row>
      <b-col sm="12">
        <b-btn v-if="isRun" @click="StopCommandRun" style="float: right;"
          >STOP</b-btn
        >
        <b-btn v-else @click="GetDashboardData" style="float: right;"
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

export default {
  components: {
    VueApexCharts
  },
  props: {
    targetAddr: String
  },
  data: function() {
    return {
      dataSet: new GuiderGraphDataSet(),
      isRun: false
    };
  },
  sockets: {
    set_dashboard_data: function(data) {
      if (data.result === 0) {
        this.dataSet.setGuiderData(data.data);
      } else if (data.result < 0){
        this.isRun = false;
        this.StopCommandRun();
        alert(data.errorMsg);
      }
    }
  },
  methods: {
    GetDashboardData() {
      if (!this.targetAddr) {
        alert("please set target address")
        return false;
      }

      if (this.isRun) {
        alert("command alredy run");
        return false;
      }

      try {
        this.isRun = true;
        this.$socket.connect();
        this.targetTimestamp = String(new Date());
        this.$socket.emit(
          "get_dashboard_data",
          this.targetTimestamp,
          this.targetAddr
        );
      } catch (e) {
        this.isRun = false;
      }
    },
    StopCommandRun() {
      this.isRun = false;
      this.$socket.emit("request_stop", this.targetTimestamp);
      this.targetTimestamp = "";
      this.$socket.disconnect();
    }
  },
  mounted() {
    EventBus.$on("setDashboardData", data => {
      this.dataSet.setGuiderData(data);
    });
  },
  beforeDestroy() {}
};
</script>
<style></style>
