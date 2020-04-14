<template>
  <div>
    <nav-bar></nav-bar>
    <breadcrumb :list="list" />
    <router-view></router-view>
  </div>
</template>

<script>
import NavBar from "./layout/NavBar";
import Breadcrumb from "./layout/Breadcrumb";

export default {
  components: {
    Breadcrumb,
    NavBar
  },
  computed: {
    list() {
      return this.$route.matched.filter(
        route => route.name || route.meta.label
      );
    }
  },
  mounted() {
    const server = JSON.parse(sessionStorage.getItem("server"));
    if (server) {
      this.$store.commit("setServer", server);
    }
  }
};
</script>

<style lang="scss"></style>
