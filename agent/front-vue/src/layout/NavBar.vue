<template>
  <div>
    <b-navbar toggleable="sm" type="dark" variant="faded">
      <b-navbar-nav tag="h2" class="mb-0" href="#">
        Guider
      </b-navbar-nav>

      <b-navbar-nav>
        <b-nav-item to="/dashboard">DashBoard</b-nav-item>
        <b-nav-item to="/commandTabs">Command Tabs</b-nav-item>
        <b-nav-item to="/history">History</b-nav-item>
      </b-navbar-nav>

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <b-nav-item @click="$bvModal.show('bv-modal-setting')">
          Setting
        </b-nav-item>
      </b-navbar-nav>
    </b-navbar>
    <b-modal
      id="bv-modal-setting"
      size="lg"
      hide-footer
      title="Setting"
      header-bg-variant="dark"
      body-bg-variant="dark"
    >
      <template slot="modal-title">
        <h4>Setting</h4>
      </template>
      <setting></setting>
    </b-modal>
  </div>
</template>

<script>
import Setting from "../components/Setting.vue";

export default {
  name: "NavBar",
  components: {
    Setting
  }
};
</script>

<style scoped></style>
