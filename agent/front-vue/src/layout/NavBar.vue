<template>
  <div>
    <b-navbar toggleable="sm" type="dark" variant="faded">
      <b-navbar-nav tag="h2" class="mb-0" href="#">
        Guider
      </b-navbar-nav>

      <b-navbar-nav>
        <b-nav-item to="/dashboard">DashBoard</b-nav-item>
        <b-nav-item to="/command">Command</b-nav-item>
        <b-nav-item to="/history">History</b-nav-item>
      </b-navbar-nav>

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <b-nav-item @click="$bvModal.show('bv-modal-example')">
          Setting
        </b-nav-item>
      </b-navbar-nav>
    </b-navbar>
    <b-modal
      id="bv-modal-example"
      size="lg"
      hide-footer
      title="Setting"
      header-bg-variant="dark"
      body-bg-variant="dark"
    >
      <template slot="modal-title">
        <h4>Setting</h4>
      </template>
      <socket-io></socket-io>
    </b-modal>
  </div>
</template>

<script>
  import SocketIo from "../pages/SocketIO.vue";

  export default {
  name: "NavBar",
  components: {
    SocketIo
  },
  computed: {
    routeName() {
      const { name } = this.$route;
      return this.capitalizeFirstLetter(name);
    }
  },
  methods: {
    capitalizeFirstLetter(name) {
      if (!name) {
        return "";
      }
      return name.charAt(0).toUpperCase() + name.slice(1);
    }
  }
};
</script>

<style scoped></style>
