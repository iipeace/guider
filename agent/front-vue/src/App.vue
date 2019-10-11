<template>
  <div>
    <socket-io></socket-io>
    <notifications></notifications>
    <router-view :key="$route.fullPath"></router-view>
  </div>
</template>

<script>
import SocketIo from "./pages/SocketIO";
import { EventBus } from "./event-bus";

export default {
  name: "App",
  components: { SocketIo },
  data() {
    return {
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
  mounted: function() {
    this.$watch("$route", this.disableRTL, { immediate: true });
    this.$watch("$sidebar.showSidebar", this.toggleNavOpen);
  }
};
</script>

<style lang="scss"></style>
