<template>
  <div>
    <b-row>
      <b-col>
        <socket-io></socket-io>
      </b-col>
      <b-col sm="2">
        <h2>{{ routeName }}</h2>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import SocketIo from "../pages/SocketIO.vue";

export default {
  components: {
    SocketIo
  },
  computed: {
    routeName() {
      const { name } = this.$route;
      return this.capitalizeFirstLetter(name);
    }
  },
  data() {
    return {
      showMenu: false
    };
  },
  methods: {
    capitalizeFirstLetter(string) {
      return string.charAt(0).toUpperCase() + string.slice(1);
    },
    toggleNotificationDropDown() {
      this.activeNotifications = !this.activeNotifications;
    },
    closeDropDown() {
      this.activeNotifications = false;
    },
    toggleSidebar() {
      this.$sidebar.displaySidebar(!this.$sidebar.showSidebar);
    },
    hideSidebar() {
      this.$sidebar.displaySidebar(false);
    },
    toggleMenu() {
      this.showMenu = !this.showMenu;
    }
  },
  mounted: function() {}
};
</script>
<style></style>
