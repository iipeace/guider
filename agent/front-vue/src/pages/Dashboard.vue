<template>
  <div class="container-fluid">
    <b-row>
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
  data: function() {
    return {
      dataSet: new GuiderGraphDataSet()
    };
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
