<template>
  <div>
    <b-row>
      <b-col sm="3">
        <h2 class="text-center">{{ routeName }}</h2>
      </b-col>
      <b-col>
        <socket-io></socket-io>
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
<style></style>
