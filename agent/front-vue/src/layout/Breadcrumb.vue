<template>
  <b-row class="breadcrumb">
    <b-col
      :key="index"
      class="breadcrumb-item"
      v-for="(routeObject, index) in routeRecords"
    >
      <h4 class="active">{{ getName(routeObject) }}</h4>
    </b-col>
    <b-col class="text-right">
      <h4>{{ getTargetAddr }}</h4>
    </b-col>
  </b-row>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  props: {
    list: Array
  },
  computed: {
    routeRecords() {
      return this.list.filter(route => route.name || route.meta.label);
    },
    ...mapGetters(["getTargetAddr"])
  },
  methods: {
    getName(item) {
      return item.meta && item.meta.label ? item.meta.label : item.name || null;
    }
  }
};
</script>
