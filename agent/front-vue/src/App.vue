<template>
  <div>
    <router-view :key="$route.fullPath"></router-view>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      colorCodes: [
        "#DC143C",
        "#008000",
        "#000080",
        "#b07025",
        "#FFFF00",
        "#BFFF00",
        "#80FF00",
        "#40FF00",
        "#00FF00",
        "#00FF40",
        "#00FF80",
        "#00FFBF",
        "#00FFFF",
        "#00BFFF",
        "#0080FF",
        "#0040FF"
      ]
    };
  },
  methods: {
    toggleNavOpen() {
      let root = document.getElementsByTagName("html")[0];
      root.classList.toggle("nav-open");
    }
  },
  mounted: function() {
    this.$watch("$sidebar.showSidebar", this.toggleNavOpen);
  }
};
</script>

<style lang="scss"></style>
