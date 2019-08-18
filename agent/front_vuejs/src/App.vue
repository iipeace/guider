<template>
  <div id='app'>
    <div class="page-title">
      GUIder - Web (v0.2)
      <socket-io>
      </socket-io>
    </div>

    <div class="small">

      <div class="line-chart">
        <line-chart :chart-data="cpuChartData" :options="cpuChartOptions" :bind="true" :width='1000' :height="300"></line-chart>
      </div>
      <div class="line-chart">
        <line-chart :chart-data="procChartData" :options="procChartOptions" :bind="true" :width='1000' :height="300"></line-chart>
      </div>
      <div class="pie-chart">
        <pie-chart :chart-data="memAChartData" :options="memChartOptions" :bind="true" :width='494' :height="300"></pie-chart>
      </div>
      <div class="pie-chart">
        <pie-chart :chart-data="memBChartData" :options="memChartOptions" :bind="true" :width='494' :height="300"></pie-chart>
      </div>
    </div>
  </div>
</template>

<script>
//import ReactiveBarChart from "./ReactiveBarChart.vue";
import LineChart from './LineChart.vue'
import PieChart from './PieChart.vue'
import SocketIO from './SocketIO.vue'
import { EventBus } from './event-bus';

export default {
  name: 'ChartContainer',
  components: {
      'socket-io':SocketIO, LineChart, PieChart},
  data() {
    return {
// ***Usage : raw-data recieved from emit message.
// **ChartDataset : refined (from ***Usage
      emitCount: 0,
      cpuChartData : {},
      flagCpuEmit: 0,
      cpuUsage : [],
      arrSize: 16,
      memUsage: {},
      memUsageTypeA: {},
      memUsageTypeB: {},
      procInfo: [],
      procInfoChart: {},
      procChartData : {},
      procDispBoundary : 5,
      lineChartOptions : {},
      memAChartData: {},
      memBChartData: {},
      //memTotalAmount: 0,
      cpuChartOptions : {},
      procChartOptions : {},
      memChartOptions : {},
      colorCodes:["#DC143C","#008000","#000080","#b07025", 
                  "#FFFF00","#BFFF00","#80FF00","#40FF00",
                  "#00FF00","#00FF40","#00FF80","#00FFBF",
                  "#00FFFF","#00BFFF","#0080FF","#0040FF",
                  ]
    }
  },
  watch: {
    flagCpuEmit: function(data) {
        this.initChart();
    }
  },
  computed: {
    lineChartLabels: function(){
      var arrLabel = new Array();
      for (var i=0; i < this.arrSize ; i ++ ){
          arrLabel.push(this.lbM((-1)*this.arrSize + i + 1));
      }
      return arrLabel;
    },
    cpuChartDatasets: function() {
      var arrJson = new Array();
      for (var i=0; i < this.cpuUsage.length ; i++){
        var objJson = new Object();
        objJson.label = "Core " + String(i+1);
        objJson.borderColor = this.colorCodes[(i%16)];
        objJson.fill = false;
        objJson.data = this.cpuUsage[i];
        arrJson.push(objJson);
      }
      return arrJson;
    },

    procChartDatasets: function() {
      var arrJson = new Array();
      var numData = 0;

      this.updateProcInfoChart(); // pick target PIDs to draw via the refining method

      for (var keyPID in this.procInfoChart){
        var objJson = new Object();
        objJson.label = "(PID:" + keyPID + ")" + this.procInfoChart[keyPID]["comm"];
        objJson.borderColor = this.colorCodes[(this.procInfoChart[keyPID]["colorCodeIndex"])%16];
        objJson.fill = false;
        objJson.data = this.procInfoChart[keyPID]["ttime"];
        arrJson.push(objJson);
        numData++;
      }
      return arrJson;

    },
    memTotalAmount: function() {
      return this.memUsage['total'];
    }
  },
  methods: {
    initChart() {
      this.cpuChartData = {
        labels: this.lineChartLabels,
        datasets: this.cpuChartDatasets
      };
      this.procChartData = {
        labels: this.lineChartLabels,
        datasets: this.procChartDatasets
      };
      this.memAChartData = {
        labels: this.memChartLabels(this.memUsageTypeA),
        datasets: this.memChartDatasets(this.memUsageTypeA)
      };
      this.memBChartData = {
        labels: this.memChartLabels(this.memUsageTypeB),
        datasets: this.memChartDatasets(this.memUsageTypeB)
      };
    },
    lbM(val){ // lbM = labelmake
      return String(this.emitCount + val - 1 )
    },
    tempHoverMethod(){
    },
    updateProcInfoChart() {
      var arrJson = new Array();
      var arrPIDinPIC = new Array();
      arrPIDinPIC = Object.keys(this.procInfoChart);
      var boundary = this.procDispBoundary;
// The structure of PIC(procInfoChart), Array of Objects
// params : {PID:{PID, [ttime], comm, lastEmitCnt, cntUnderBoundary(int)}}
      for (var i=0; i < this.procInfo.length ; i++){ // loop all procInfo
        if(arrPIDinPIC.includes(this.procInfo[i]["PID"]) === true ) {
        // if this procInfo's PID already exists among PIC then
          this.procInfoChart[this.procInfo[i]["PID"]]["ttime"].shift();
          this.procInfoChart[this.procInfo[i]["PID"]]["ttime"].push(this.procInfo[i]["ttime"]);
          this.procInfoChart[this.procInfo[i]["PID"]]["lastEmitCnt"] = this.emitCount; // let cnt zero
          // in PIC, data shift and push new one
          if (this.procInfo[i]["ttime"] > boundary) {
            this.procInfoChart[this.procInfo[i]["PID"]]["cntUnderBoundary"] = 0; // let lastEmitCnt = this.emitCount
          }
          else {
            this.procInfoChart[this.procInfo[i]["PID"]]["cntUnderBoundary"]++;
          }
        }
        else if (this.procInfo[i]["ttime"] > boundary) { // else, if this PID not exsit (new one)

          var arrTtime = new Array(this.arrSize);
          //arrTtime.fill(false);
          arrTtime[this.arrSize-1] = this.procInfo[i]["ttime"]
          // padding ttime to zero except the last one
          var objNewPID = {};
          // push this new one to PIC
          objNewPID["PID"] = this.procInfo[i]["PID"];
          objNewPID["ttime"] = arrTtime;
          objNewPID["comm"] = this.procInfo[i]["comm"];
          this.procInfoChart[this.procInfo[i]["PID"]] = objNewPID;
          this.procInfoChart[this.procInfo[i]["PID"]]["lastEmitCnt"] = this.emitCount; // let cnt zero
          this.procInfoChart[this.procInfo[i]["PID"]]["cntUnderBoundary"] = 0; // let lastEmitCnt = this.emitCount
          this.procInfoChart[this.procInfo[i]["PID"]]["colorCodeIndex"] = this.getColorCodeIndex(this.procInfoChart[this.procInfo[i]["PID"]]); // let lastEmitCnt = this.emitCount
        }
      }

      var arrPIDDel = new Array();
      for (var keyPID in this.procInfoChart) { //  loop all PIC to find which is already killed
        if (this.procInfoChart[keyPID]["lastEmitCnt"] !== this.emitCount) {  //    if each PIC's lastEmitCnt != this.emitCount
        // dealing with PIC members which has zero or none ttime in this turn
          this.procInfoChart[keyPID]["cntUnderBoundary"] = this.procInfoChart[keyPID]["cntUnderBoundary"] + 1;//parseInt(this.arrSize*(0.25)); //      cntUnderboundary ++
          this.procInfoChart[keyPID]["ttime"].shift();  //      ttime shift
          this.procInfoChart[keyPID]["ttime"].push(undefined);
        }
        if(this.procInfoChart[keyPID]["cntUnderBoundary"] > this.arrSize) {// if cntUnderboundary > 15 then
          arrPIDDel.push(parseInt(keyPID)); // pop target update
        }
      }
      for(var i=0 ; i < arrPIDDel.length ; i ++ ){
        delete (this.procInfoChart)[arrPIDDel[i]];
      }
    },
    getColorCodeIndex(targetPID) {
    // give procInfoChart the most smallest color code among which have not not been used.
    // this method is used for process chart, for the color of specific process NOT to be changed after flush action.
    // (flush happens after new/del process disp)

      var procInfoChartLength = Object.keys(this.procInfoChart).length;
      if(procInfoChartLength === 1) return 0;
      var arrColorUsed = new Array(procInfoChartLength-1);

      var i=0;
      for (var keyPID in this.procInfoChart) {
          if(parseInt(keyPID) !== parseInt(targetPID["PID"])) {
            arrColorUsed[i] = this.procInfoChart[keyPID]["colorCodeIndex"];
            i++;
          }
      }

      arrColorUsed.sort(function(a, b) { // acesending order
          return a - b;
      });

      var valCnt=0;
      for(var i = 0 ; i < arrColorUsed.length ; i++ ){
console.log("add/del test. valCnt, i, arrColorUsed[i] : ", valCnt, "/", i, "/", arrColorUsed[i]);
        if (valCnt !== arrColorUsed[i]) {
          return valCnt;
        }
        valCnt++;
      }
      return valCnt;
      // among process (in chart), if there is a skipped integer, pick this. else, pick the the last + 1
    },
    memChartLabels: function(memUsageTypeX){
      //var memObj = JSON.parse(this.memUsage);
      var arrReturn = new Array();
      memUsageTypeX = JSON.parse(JSON.stringify(memUsageTypeX))

      for(var key in memUsageTypeX) {

        var percentUsage = ((memUsageTypeX[key] / this.memUsage['total'])*100).toFixed(2);
        var label = key + " (" + String(memUsageTypeX[key]) + "M, " + String(percentUsage) + "%)"
        arrReturn.push(label);

      }
      return arrReturn;

    },
    memChartDatasets: function(memUsageTypeX) {

      var arrJson = new Array(1);
      var numMemInfo = Object.keys(memUsageTypeX).length;
      arrJson[0] = {};
      arrJson[0]["label"] = "Memory Usage";
      arrJson[0]["backgroundColor"] = new Array(numMemInfo);
      for (var i=0; i < numMemInfo ; i++){
        arrJson[0]["backgroundColor"][i] = this.colorCodes[i];
      }
      arrJson[0]["data"] = Object.values(memUsageTypeX);
      return arrJson;
    },

  },
  created() {
    this.emitCount = 0;
    this.lineChartOptions =
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
      maintainAspectRatio: false,
      //animation: {duration:1000}
    };

    this.cpuChartOptions = JSON.parse(JSON.stringify(this.lineChartOptions));
    var cpuChartAnimation = {'duration':1000};
    this.cpuChartOptions["animation"] = cpuChartAnimation;
    var cpuTitle = {'display':true, 'text':'CPU USage', 'fontSize':20};
    this.cpuChartOptions['title'] = cpuTitle;

    this.procChartOptions = JSON.parse(JSON.stringify(this.lineChartOptions));
    var procChartAnimation = {'duration':0};
    this.procChartOptions["animation"] = procChartAnimation;
    var procTitle = {'display':true, 'text':'Process Information [Display boundary(ttime) : ' + String(this.procDispBoundary) + '%]', 'fontSize':20};
    this.procChartOptions['title'] = procTitle;


    this.memChartOptions =
    {
      legend: {
        display: true,
        position: 'right',
        fontSize:16 ,
        //fullWidth: false,
        onHover: function (event, legendItem) {}
      },
      title: {
        display: true,
        text: 'Memory Usage',
        fontSize:20
      },
      responsive: true,
      maintainAspectRatio: false,
      aspectRatio: 2

    };

  },
  beforeUpdate: function() {
    this.memChartOptions.title.text = 'Memory Usage [Total : ' + this.memTotalAmount + 'M]';
    this.cpuChartOptions.title.text = 'CPU Usage [' + this.cpuUsage.length + ' Cores]';
  },
  mounted: function() {
    //this.initChart();
    EventBus.$on("reset_data", nothing => {
      this.cpuUsage = [];
      this.memUsageTypeA = {};
      this.memUsageTypeB = {};
      this.procInfo = [];
      this.flasCpuEmit++;
    });
    EventBus.$on("cnt_emit", cpu_emit => {
      this.emitCount = this.emitCount +1;
    });
    EventBus.$on("cpu_usage", cpuTotal => {
      if(this.emitCount === 1) {
        //linechartArrSize = this.arrSize;
        this.cpuUsage = new Array(cpuTotal.length);
        for (var i = 0 ; i < cpuTotal.length ; i ++ ){
          this.cpuUsage[i] = new Array(this.arrSize);
          for(var j = 0 ; j < this.arrSize ; j ++ ){
            this.cpuUsage[i][j] = undefined;
          }
        }
      }
      for (var i = 0 ; i < cpuTotal.length ; i ++ ){
        this.cpuUsage[i].shift();
        this.cpuUsage[i].push(cpuTotal[i]);
      }
      this.flagCpuEmit++;
    });
    EventBus.$on("mem_usage", memTotal => {
      // in this event handler, mem usage data is divided into two groups A(total/available) / B(the others)
      this.memUsage = memTotal;
      var memUsageAll = JSON.parse(JSON.stringify(this.memUsage));
      var memUsageTypeAMember = ['total', 'available'];
      var memUsageTypeA = {};
      var memUsageTypeB = {};

      for (var i=0 ; i < memUsageTypeAMember.length ; i++){
        var target = memUsageTypeAMember[i];
        memUsageTypeA[target] = memUsageAll[target];
        delete memUsageAll[target];
      }
      memUsageTypeB = memUsageAll;
      var sumUsageTypeB = 0;
      for (var key in memUsageTypeB) {
        sumUsageTypeB = sumUsageTypeB + memUsageTypeB[key];
      }

      memUsageTypeB['etc'] = memUsageTypeA['total'] - sumUsageTypeB;

      memUsageTypeA['used'] = this.memUsage['total'] - memUsageTypeA['available'];
      delete memUsageTypeA['total'];

      this.memUsageTypeA = memUsageTypeA;
      this.memUsageTypeB = memUsageTypeB;

    });
    EventBus.$on("proc_usage", procTotal => {
      this.procInfo = procTotal;
    });

  }
}


</script>

<style lang="scss">

.page-title {
  font-size:24px;
  margin-top:10px;
  margin-bottom:10px;
  font-weight:900;
  font-family: "Georgia", "serif"
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 10px;
}

#tooltip {
  position: absolute;
  z-index:999;
  color:white;
  font-size: 15px;
  width:200px;
  height:200px;

}

.line-chart {
    position:relative;
    display:inline-block;
    width:1000px;
    height:300px;
    border:1px solid #bcbcbc;
}

.pie-chart {
    position:relative;
    display:inline-block;
    width:498px;
    height:300px;
    border:1px solid #bcbcbc;
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
