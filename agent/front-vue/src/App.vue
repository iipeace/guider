<template>
  <div>
    <top-navbar></top-navbar>
    <side-nav-bar></side-nav-bar>
    <div class="main-panel">
      <div class="content">
        <router-view v-bind="getRouterData"></router-view>
      </div>
    </div>
  </div>
</template>

<script>
import TopNavbar from "./layout/TopNavbar";
import SideNavBar from "./layout/SideNavBar";
import { EventBus } from "./event-bus";

export default {
  data: function() {
    return {
      targetAddr: ""
    };
  },
  components: {
    SideNavBar,
    TopNavbar
  },
  computed: {
    getRouterData() {
      return { targetAddr: this.targetAddr };
    }
  },
  mounted() {
    EventBus.$on("setPropTargetAddr", addr => {
      this.targetAddr = addr;
    });
  }
};
</script>

<style lang="scss"></style>
