<template>
  <div class="wrapper">
    <side-bar>
      <sidebar-link
        to="/dashboard"
        :name="$t('sidebar.dashboard')"
      />
    </side-bar>
    <div class="main-panel">
      <dashboard-content @click.native="toggleSidebar"> </dashboard-content>
    </div>
  </div>
</template>
<style lang="scss"></style>
<script>
import DashboardContent from "./Content.vue";
export default {
  components: {
    DashboardContent
  },
  methods: {
  }
};
</script>
