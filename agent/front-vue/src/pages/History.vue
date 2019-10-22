<template>
  <div class="container-fluid">
    <b-row>
      <b-col sm="12">
        <b-card style="background: white;">
          <b-form-select
            class="text-dark"
            v-model="device"
            :options="options"
            @change="getMetaData"
          ></b-form-select>
        </b-card>
        <b-card style="background: white; " v-if="device">
          <b-card v-if="count != -1">
            <b-card-text v-if="count != 0">
              There are {{ count }} pieces of information from {{ db_start }} to
              {{ db_end }}.
            </b-card-text>
            <b-card-text v-else>
              There are 0 pieces of information.
            </b-card-text>
          </b-card>
          <h4 style="color: black;">
            Browse the stored database.
          </h4>
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
      end: null,
      sampleNum: 40,
      errMsg: "",
      device: null,
      count: -1,
      db_start: null,
      options: [{ value: null, text: "Loading.." }],
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
    async getDevices() {
      try {
        const response = await fetch("http://localhost:8000/devices");
        const responseOK = response && response.status == 200;
        if (responseOK) {
          const body = await response.json();
          if (body && body.status == "ok") {
            const devices = body.devices || body.data;
            this.options = [{ value: null, text: "Select Device" }];
            for (let device of devices) {
              this.options.push({
                value: device,
                text: `${device.mac_addr}(${device.count})`
              });
            }
          }
          else throw Error(body.msg || "Internal Server Error");
        }
      }
      catch(e){
        this.options = [{ value:null, text: e}]
        this.errMsg = e
      }
    },
    getMetaData() {
      this.count = this.device.count || 0;
      this.db_start = this.tsToPrettyDate(this.device.start);
      this.start = this.tsToISOString(this.device.start);
      this.db_end = this.tsToPrettyDate(this.device.end);
      this.end = this.tsToISOString(this.device.end);
      this.sampleNum = this.count < 80 ? this.count : 80;
    },
    async getData() {
      // init values
      try {
        this.errMsg = "";
        this.dataSet = new GuiderGraphDataSet();
        let url = `http://localhost:8000/dataset?mac_addr=${this.device.mac_addr}`;
        if (this.start) {
          let timestamp = this.dateToTS(this.start);
          url += `&start=${timestamp}`;
        }
        if (this.end) {
          let timestamp = this.dateToTS(this.end);
          url += `&end=${timestamp}`;
        }
        if (this.sampleNum >= 1 && this.sampleNum <= 150) {
          url += `&num=${this.sampleNum}`;
        } else throw Error("Sample Number should be in range 1~150");
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
          } else throw Error( body.msg || "Internal Server Error");
        } else throw Error("Failed to load body");
      } catch (e) {
        this.errMsg = e;
      }
    }
  },
  async mounted() {
    await this.getDevices();
    await this.getData();
  },
  beforeDestroy() {}
};
</script>
<style scoped>
input {
  margin: 3px 0px;
}
b-form-select {
  margin: 5px 0px;
}
</style>
