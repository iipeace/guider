<template>
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
      <sidebar-link
        to="/background"
        name="background"
        icon="tim-icons icon-chart-pie-36"
      />
    </template>
  </side-bar>
</template>

<script>
  export default {
    name: "SideNavBar"
  }
</script>

<style scoped>

</style>
