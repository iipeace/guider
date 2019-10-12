<template>
  <div>
    <b-row>
      <b-col sm="6">
        <b-card no-body>
          <b-card-header>
            <h4>NETWORK</h4>
          </b-card-header>
          <b-card-body>
            <vue-apex-charts type="line" :options="chartOptions" :series="network_series"/>
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
        chart: {
          id: 'basic-bar'
        },
        xaxis: {
          categories: []
        }
      },
      network_series: [
        {
          name: 'inbound',
          data: []
        },
        {
          name: 'outbound',
          data: []
        }
      ],
      labels: []
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
      this.labels.push(data['timestamp'])
      this.network_series[0].data.push(data['network']['inbound'])
      this.network_series[1].data.push(data['network']['outbound'])
    })
  },
  beforeDestroy() {
  }
};
</script>
<style></style>
