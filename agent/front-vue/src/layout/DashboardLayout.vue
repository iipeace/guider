<template>
  <div class="wrapper">
    <side-bar>
      <template slot="links">
        <sidebar-link
          to="/dashboard"
          name="dashboard"
          icon="tim-icons icon-chart-pie-36"
        />
        <sidebar-link
          to="/command"
          name="command"
          icon="tim-icons icon-chart-pie-36"
        />
      </template>
    </side-bar>
    <div class="main-panel">
      <top-navbar></top-navbar>

      <dashboard-content @click.native="toggleSidebar"> </dashboard-content>

      <content-footer></content-footer>
    </div>
  </div>
</template>
<style lang="scss"></style>
<script>
import TopNavbar from "./TopNavbar.vue";
import DashboardContent from "./Content.vue";

export default {
  components: {
    TopNavbar,
    DashboardContent
  },
  methods: {
    toggleSidebar() {
      if (this.$sidebar.showSidebar) {
        this.$sidebar.displaySidebar(false);
      }
    }
  }
};
</script>
