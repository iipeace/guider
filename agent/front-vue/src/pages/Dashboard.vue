<template>
  <div>
  </div>
</template>
<script>
import * as chartConfigs from "@/components/Charts/config";
import config from "@/config";

export default {
  components: {
  },
  data() {
  },
  computed: {
  },
  methods: {
  },
  mounted() {
    this.i18n = this.$i18n;
    if (this.enableRTL) {
      this.i18n.locale = "ar";
      this.$rtl.enableRTL();
    }
  },
  beforeDestroy() {
    if (this.$rtl.isRTL) {
      this.i18n.locale = "en";
      this.$rtl.disableRTL();
    }
  }
};
</script>
<style></style>
