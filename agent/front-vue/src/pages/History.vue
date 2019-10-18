<template>
  <div class="container-fluid">
    <b-row>
      <b-col sm="12">
        <b-card style="background: white; ">
          <b-card v-if="count != -1">
            <b-card-text v-if="count != 0">
              There are {{ count }} pieces of information from {{ db_start }} to
              {{ db_end }}.
            </b-card-text>
            <b-card-text v-else>
              There are 0 pieces of information.
            </b-card-text>
          </b-card>
          <h3 style="color: black;">
            Browse the stored database.
          </h3>
          <b-row>
            <b-col sm="6">
              From <br />
              <datetime type="datetime" v-model="start"></datetime>
            </b-col>
            <b-col sm="6">
              To <br />
              <datetime type="datetime" v-model="end"></datetime>
            </b-col>
            <b-col sm="6">
              Sample # <br />
              <input v-model="sampleNum" />
            </b-col>
          </b-row>
          <b-button type="button" @click="getData">Browse</b-button>
          {{ errMsg }}
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
      start: null,
      sampleNum: 40,
      errMsg: "",
      count: -1,
      db_start: null,
      db_end: null
    };
  },
  methods: {
    tsToPrettyDate(timestamp) {
      return new Date(timestamp * 1000).toLocaleString();
    },
    tsToISOString(timestamp) {
      return new Date(timestamp * 1000).toISOString();
    },
    dateToTS(date) {
      return Date.parse(date) / 1000;
    },
    async getMetaData() {
      const response = await fetch("http://localhost:8000/dataset");
      const responseOK = response && response.status == 200;
      if (responseOK) {
        const body = await response.json();
        if (body && body.status == "ok") {
          const { data, meta } = body;
          if (data.length) {
            this.count = meta.count || 0;
            this.db_start = this.tsToPrettyDate(meta.start);
            this.start = this.tsToISOString(meta.start);
            this.db_end = this.tsToPrettyDate(meta.end);
            this.end = this.tsToISOString(meta.end);
          } else {
            this.count = 0;
          }
        }
      }
    },
    async getData() {
      // init values
      this.errMsg = "";
      this.dataSet = new GuiderGraphDataSet();
      let url = "http://localhost:8000/dataset";
      let hasQuery = false;
      if (this.start) {
        let timestamp = this.dateToTS(this.start);
        url += `?start=${timestamp}`;
        hasQuery = true;
      }
      if (this.end) {
        let timestamp = this.dateToTS(this.end);
        url += (hasQuery ? "&" : "?") + `end=${timestamp}`;
        hasQuery = true;
      }
      if (this.sampleNum >= 20 && this.sampleNum <= 100) {
        url += (hasQuery ? "&" : "?") + `num=${this.sampleNum}`;
      } else throw Error("Sample Number should be in range 20~100");
      const response = await fetch(url);
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
    }
  },
  async mounted() {
    try {
      await this.getMetaData();
      await this.getData();
    } catch (e) {
      this.errMsg = e;
    }
  },
  beforeDestroy() {}
};
</script>
<style scoped>
input {
  margin: 3px 0px;
}
</style>
