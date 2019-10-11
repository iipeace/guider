<template>
  <div>
    <div class="row">
      <div class="col-12">
        <span>NETWORK</span>
        <vue-apex-charts width="500" type="line" :options="chartOptions" :series="series"/>
      </div>
    </div>
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
        chart: {
          id: 'basic-bar'
        },
        xaxis: {
          categories: []
        }
      },
      series: [{
        name: 'inbound',
        data: []
      }]
    }
  },
  computed: {
  },
  methods: {
    updateChart() {
      this.series.data = [0,1,2]
    }
  },
  mounted() {
    EventBus.$on('setDashboardData', (data) => {
      console.log(data)
    })
  },
  beforeDestroy() {
  }
};
</script>
<style></style>
