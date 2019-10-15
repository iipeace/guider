<template>
  <div class="container-fluid">
    <b-row>
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
  async mounted() {
    try {
      const response = await fetch("http://localhost:8000/dataset");
      const responseOK = response && response.status == 200;
      if (responseOK) {
        const body = await response.json();
        if (body && body.status == "ok") {
          const { data } = body;
          data
            .map(x => Object({ timestamp: x.timestamp, ...x.data }))
            .forEach(x => {
              this.dataSet.setGuiderData(x);
            });
        } else throw Error("Internal Server Error");
      } else throw Error("Failed to load body");
    } catch (e) {
      // TODO: Print Error!
    }
  },
  beforeDestroy() {}
};
</script>
<style></style>
