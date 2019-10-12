<template>
  <div>
    <b-row>
      <b-col lg="12">
        <b-card no-body>
          <b-card-header>
            <h4>CPU</h4>
          </b-card-header>
          <b-card-body>
            <vue-apex-charts width="100%" height="300" type="area" :options="chartOptions" :series="dataSet.cpuSeries"/>
          </b-card-body>
        </b-card>
      </b-col>
      <b-col lg="12">
        <b-card no-body>
          <b-card-header>
            <h4>MEMORY</h4>
          </b-card-header>
          <b-card-body>
            <vue-apex-charts width="100%" height="300" type="area" :options="chartOptions" :series="dataSet.memorySeries"/>
          </b-card-body>
        </b-card>
      </b-col>
      <b-col lg="12">
        <b-card no-body>
          <b-card-header>
            <h4>NETWORK</h4>
          </b-card-header>
          <b-card-body>
            <vue-apex-charts width="100%" height="300" type="line" :options="chartOptions" :series="dataSet.networkSeries"/>
          </b-card-body>
        </b-card>
      </b-col>
    </b-row>
  </div>
</template>
<script>

import {EventBus} from '../event-bus'
import VueApexCharts from 'vue-apexcharts'
import GuiderDataSet from '../model/guider-data-set'

export default {
  components: {
    VueApexCharts,
  },
  data: function () {
    return {
      dataSet: new GuiderDataSet(),
      chartOptions: {
        xaxis: {
          name: 'timestamp'
        }
      }
    }
  },
  mounted() {
    EventBus.$on('setDashboardData', (data) => {
      this.dataSet.setGuiderData(data)
    })
  },
  beforeDestroy() {
  }
};
</script>
<style></style>
