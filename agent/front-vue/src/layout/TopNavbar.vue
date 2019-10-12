<template>
  <div class="container-fluid">
    <b-row>
      <b-col sm="3">
        <h2>{{ routeName }}</h2>
      </b-col>
      <b-col>
        <socket-io></socket-io>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import SocketIo from "../components/SocketIO.vue";
import { EventBus } from "../event-bus";

export default {
  components: {
    SocketIo
  },
  computed: {
    routeName() {
      const { name } = this.$route;
      return this.capitalizeFirstLetter(name);
    }
  },
  data() {
    return {
      showMenu: false,
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
          memChartOptions: {}
        };
      }
    };
  },
  methods: {
    capitalizeFirstLetter(string) {
      return string.charAt(0).toUpperCase() + string.slice(1);
    },
    toggleNotificationDropDown() {
      this.activeNotifications = !this.activeNotifications;
    },
    closeDropDown() {
      this.activeNotifications = false;
    },
    toggleSidebar() {
      this.$sidebar.displaySidebar(!this.$sidebar.showSidebar);
    },
    hideSidebar() {
      this.$sidebar.displaySidebar(false);
    },
    toggleMenu() {
      this.showMenu = !this.showMenu;
    }
  },
  beforeUpdate: function() {
    this.memChartOptions.title.text =
      "Memory Usage [Total : " + this.memTotalAmount + "M]";
    this.cpuChartOptions.title.text =
      "CPU Usage [" + this.cpuUsage.length + " Cores]";
  },
  mounted: function() {
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
  }
};
</script>
<style></style>
