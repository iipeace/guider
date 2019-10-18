<template>
  <div>
    <top-navbar></top-navbar>
    <side-nav-bar></side-nav-bar>
    <div class="main-panel">
      <div class="content">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script>
import TopNavbar from "./layout/TopNavbar";
import SideNavBar from "./layout/SideNavBar";

export default {
  components: {
    SideNavBar,
    TopNavbar
  }
};
</script>

<style lang="scss"></style>
