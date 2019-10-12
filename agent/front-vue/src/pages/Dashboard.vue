<template>
  <div>
    <b-row>
      <b-col sm="6">
        <b-card no-body>
          <b-card-header>
            <h4>NETWORK</h4>
          </b-card-header>
          <b-card-body>
            <vue-apex-charts type="line" :options="chartOptions" :series="networkSeries"/>
          </b-card-body>
        </b-card>
      </b-col>
      <b-col sm="6">
        <b-card no-body>
          <b-card-header>
            <h4>MEMORY</h4>
          </b-card-header>
          <b-card-body>
            <vue-apex-charts type="line" :options="chartOptions" :series="series"/>
          </b-card-body>
        </b-card>
      </b-col>
    </b-row>
  </div>
</template>
<script>

import {EventBus} from '../event-bus'
import VueApexCharts from 'vue-apexcharts'

export default {
  components: {
    VueApexCharts,
  },
  data: function () {
    return {
      chartOptions: {
        xaxis: {
          categories: []
        }
      },
      networkSeries: [
        {
          name: 'inbound',
          data: []
        },
        {
          name: 'outbound',
          data: []
        }
      ],
    }
  },
  computed: {
  },
  methods: {
    updateNetworkChart(networkInfo) {
      // this.networkSeries[0].data.push(networkInfo['inbound'])
      // this.networkSeries[1].data.push(networkInfo['outbound'])
    },
    // updateMemoryChart() {
    //   this.series.data = [0,1,2]
    // },
    // updateCpuChart() {
    //   this.series.data = [0,1,2]
    // },
    // updateStorageChart() {
    //   this.series.data = [0,1,2]
    // },
  },
  mounted() {
    EventBus.$on('setDashboardData', (data) => {
      console.log('www')
      // this.chartOptions.xaxis.categories.push(data['timestamp'])
      // this.updateNetworkChart(data['network'])
      // this.updateMemoryChart(data['memory'])
      // this.updateCpuChart(data['cpu'])
      // this.updateStorageChart(data['storage'])
    })
  },
  beforeDestroy() {
  }
};
</script>
<style></style>
