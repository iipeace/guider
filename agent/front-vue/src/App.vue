<template>
  <div>
    <socket-io></socket-io>
    <notifications></notifications>
    <router-view :key="$route.fullPath"></router-view>
  </div>
</template>

<script>
import SocketIo from "./components/SocketIO";
import { EventBus } from "./event-bus";

export default {
  name: "App",
  components: { SocketIo },
  data() {
    return {
      // ***Usage : raw-data recieved from emit message.
      // **ChartDataset : refined (from ***Usage
      emitCount: 0,
      cpuChartData: {},
      flagCpuEmit: 0,
      cpuUsage: [],
      arrSize: 16,
      memUsage: {},
      memUsageTypeA: {},
      memUsageTypeB: {},
      procInfo: [],
      procInfoChart: {},
      procChartData: {},
      procDispBoundary: 5,
      lineChartOptions: {},
      memAChartData: {},
      memBChartData: {},
      // memTotalAmount: 0,
      cpuChartOptions: {},
      procChartOptions: {},
      memChartOptions: {},
      colorCodes: [
        "#DC143C",
        "#008000",
        "#000080",
        "#b07025",
        "#FFFF00",
        "#BFFF00",
        "#80FF00",
        "#40FF00",
        "#00FF00",
        "#00FF40",
        "#00FF80",
        "#00FFBF",
        "#00FFFF",
        "#00BFFF",
        "#0080FF",
        "#0040FF"
      ]
    };
  },
  methods: {
    disableRTL() {
      if (!this.$rtl.isRTL) {
        this.$rtl.disableRTL();
      }
    },
    toggleNavOpen() {
      let root = document.getElementsByTagName("html")[0];
      root.classList.toggle("nav-open");
    }
  },
  beforeUpdate: function() {
    this.memChartOptions.title.text =
      "Memory Usage [Total : " + this.memTotalAmount + "M]";
    this.cpuChartOptions.title.text =
      "CPU Usage [" + this.cpuUsage.length + " Cores]";
  },
  mounted: function() {
    // this.initChart();
    EventBus.$on("reset_data", () => {
      this.cpuUsage = [];
      this.memUsageTypeA = {};
      this.memUsageTypeB = {};
      this.procInfo = [];
      this.flasCpuEmit++;
    });
    EventBus.$on("cnt_emit", () => {
      this.emitCount = this.emitCount + 1;
    });
    EventBus.$on("cpu_usage", cpuTotal => {
      if (this.emitCount === 1) {
        // linechartArrSize = this.arrSize;
        this.cpuUsage = new Array(cpuTotal.length);
        for (let i = 0; i < cpuTotal.length; i++) {
          this.cpuUsage[i] = new Array(this.arrSize);
          for (let j = 0; j < this.arrSize; j++) {
            this.cpuUsage[i][j] = undefined;
          }
        }
      }
      for (let i = 0; i < cpuTotal.length; i++) {
        this.cpuUsage[i].shift();
        this.cpuUsage[i].push(cpuTotal[i]);
      }
      this.flagCpuEmit++;
    });
    EventBus.$on("mem_usage", memTotal => {
      // in this event handler, mem usage data is divided into two groups A(total/available) / B(the others)
      this.memUsage = memTotal;
      var memUsageAll = JSON.parse(JSON.stringify(this.memUsage));
      var memUsageTypeAMember = ["total", "available"];
      var memUsageTypeA = {};
      var memUsageTypeB = {};

      for (var i = 0; i < memUsageTypeAMember.length; i++) {
        var target = memUsageTypeAMember[i];
        memUsageTypeA[target] = memUsageAll[target];
        delete memUsageAll[target];
      }
      memUsageTypeB = memUsageAll;
      var sumUsageTypeB = 0;
      for (var key in memUsageTypeB) {
        sumUsageTypeB = sumUsageTypeB + memUsageTypeB[key];
      }

      memUsageTypeB["etc"] = memUsageTypeA["total"] - sumUsageTypeB;

      memUsageTypeA["used"] =
        this.memUsage["total"] - memUsageTypeA["available"];
      delete memUsageTypeA["total"];

      this.memUsageTypeA = memUsageTypeA;
      this.memUsageTypeB = memUsageTypeB;
    });
    EventBus.$on("proc_usage", procTotal => {
      this.procInfo = procTotal;
    });

    this.$watch("$route", this.disableRTL, { immediate: true });
    this.$watch("$sidebar.showSidebar", this.toggleNavOpen);
  }
};
</script>

<style lang="scss"></style>
