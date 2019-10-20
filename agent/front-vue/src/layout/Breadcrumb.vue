<template>
  <b-row class="breadcrumb">
    <b-col
      :key="index"
      class="breadcrumb-item"
      v-for="(routeObject, index) in routeRecords"
    >
      <h4 class="active">{{ getName(routeObject) }}</h4>
    </b-col>
    <b-col class="text-right" v-if="server">
      <h4>
        {{ server.targetAddr }}
        <font-awesome-icon v-if="isStart" icon="circle" style="color:#00CC6A" />
        <font-awesome-icon
          v-if="isRunning"
          icon="circle"
          style="color:#0208CC"
        />
        <font-awesome-icon
          v-if="isSuspend"
          icon="circle"
          style="color:#FFFC0B"
        />
        <font-awesome-icon v-if="isStop" icon="circle" style="color:#FF0000" />
      </h4>
    </b-col>
  </b-row>
</template>

<script>
import { mapState } from "vuex";

export default {
  props: {
    list: Array
  },
  computed: {
    routeRecords() {
      return this.list.filter(route => route.name || route.meta.label);
    },
    ...mapState(["server"]),
    isStart() {
      return this.server.targetAddr && this.server.status === 0;
    },
    isRunning() {
      return this.server.targetAddr && this.server.status === 1;
    },
    isSuspend() {
      return this.server.targetAddr && this.server.status === 2;
    },
    isStop() {
      return this.server.targetAddr && this.server.status === 9;
    }
  },
  methods: {
    getName(item) {
      return item.meta && item.meta.label ? item.meta.label : item.name || null;
    }
  }
};
</script>
