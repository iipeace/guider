<template>
  <div id='app'>


    <div class="small">
    <!--
      <line-chart
        :chart-data="chartData"
        :options="{responsive: true, maintainAspectRatio: false}">
      </line-chart>
-->
    <line-chart
      :chart-data="dataCollection"
      :options="chartOptions"
      :bind="true"
    ></line-chart>
    <socket-io></socket-io>
    </div>
  </div>
</template>

<script>
//import ReactiveBarChart from "./ReactiveBarChart.vue";
import LineChart from './LineChart.vue'
import SocketIO from './SocketIO.vue'
import { EventBus } from './event-bus';

export default {
  name: 'ChartContainer',
  components: {
      'socket-io':SocketIO, LineChart},
  data() {
    return {
      dataCollection : null,
      flagCpuEmit: 0,
      cpuUsage : [],
      emitCount: 0,
      arrSize: 8,
      chartOptions :
      {
          scales: {
              yAxes: [{
                      display: true,
                      ticks: {
                          min:0,
                          max:100
                      }
                  }]
          },
          responsive: true,
          maintainAspectRatio: false
      }
    }
  },
  watch: {
    flagCpuEmit: function(data) {
        console.log("watch entered!");
        this.initChart();
    }
  },
  methods: {
    initChart() {
      this.dataCollection = {
        labels: [this.lbM(-7), this.lbM(-6), this.lbM(-5), this.lbM(-4), this.lbM(-3), this.lbM(-2), this.lbM(-1), this.lbM(0)],
        datasets: [
          {
            label: "Core1",
            borderColor: "blue",
            fill: false,
            data: this.cpuUsage[0]
          },
          {
            label: "Core2",
            borderColor: "red",
            fill: false,
            data: this.cpuUsage[1]
          },
          {
            label: "Core3",
            borderColor: "purple",
            fill: false,
            data: this.cpuUsage[2]
          },
          {
            label: "Core4",
            borderColor: "black",
            fill: false,
            data: this.cpuUsage[3]
          },
        ]
      };
    },
    lbM(val){ // lbM = labelmake
      return String(this.emitCount + val -1 )
    }
  },
  created() {
    this.emitCount = 0;

  },
  mounted: function() {
    this.initChart();
    EventBus.$on("cpu_emit", cpu_emit => {
      this.emitCount = this.emitCount +1;
    });
    EventBus.$on("cpu_total", cpuTotal => {
      if(this.emitCount === 1) {
        //linechartArrSize = this.arrSize;
        this.cpuUsage = new Array(cpuTotal.length);
        for (var i = 0 ; i < cpuTotal.length ; i ++ ){
          this.cpuUsage[i] = new Array(this.arrSize);
          for(var j = 0 ; j < this.arrSize ; j ++ ){
            this.cpuUsage[i][j] = 0;
          }
        }
      }
      for (var i = 0 ; i < cpuTotal.length ; i ++ ){
        this.cpuUsage[i].shift();
        this.cpuUsage[i].push(cpuTotal[i]);
      }
      this.flagCpuEmit++;
    });
  }
}


</script>

<style lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
