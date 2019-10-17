<template>
  <div class="container-fluid">
    <b-row>
      <b-col sm="12">
        <b-card style="background: white; ">
          Browse the stored database
          <b-row>
            <b-col sm="6">
              From <datetime type="datetime" v-model="fromDate"></datetime>
              
            </b-col>
            <b-col sm="6">
              To <datetime type="datetime" :value="now" disabled></datetime>
            </b-col>
            <b-col sm="6">
              Sample # <input v-model="sampleNum">
            </b-col>
          </b-row>
          <input type="button" value="Browse!" @click="getData"> {{errMsg}}
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
      dataSet: new GuiderGraphDataSet(),
      fromDate: '',
      sampleNum: 40,
      errMsg: ''
    };
  },
  computed: {
    now: function() {
      return new Date().toISOString()
    }
  },
  methods: {
    async getData() {
      // init values
      this.errMsg = ''
      this.dataSet = new GuiderGraphDataSet()
      try {
        let url = 'http://localhost:8000/dataset'
        let hasQuery = false
        if(this.fromDate){
          let timestamp = Date.parse(this.fromDate)/1000
          url += `?from=${timestamp}`
          hasQuery = true
        }
        if(this.sampleNum >= 20 && this.sampleNum <= 100){
          url += (hasQuery ? '&':'?') + `num=${this.sampleNum}`
        }
        else throw Error("Sample Number should be in range 20~100")
        const response = await fetch(url);
        console.log(url)
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
        this.errMsg = e
        // TODO: Print Error!
      }
    }
  },
  async mounted() {
    await this.getData()
  },
  beforeDestroy() {}
};
</script>
<style scoped>
input {
  margin: 3px 0px;
}
</style>
