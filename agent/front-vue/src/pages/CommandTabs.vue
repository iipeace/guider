<template>
  <div>
    <b-card no-body>
      <b-tabs card>
        <!-- Render Tabs, supply a unique `key` to each tab -->
        <b-tab
          v-for="i in tabs"
          :key="'dyn-tab-' + i"
          :title="`Command ${i + 1}`"
        >
          <b-button
            size="sm"
            variant="danger"
            class="float-right"
            @click="closeTab(i)"
          >
            Close tab
          </b-button>
          <command :index="i"></command>
        </b-tab>

        <!-- New Tab Button (Using tabs-end slot) -->
        <template slot="tabs-end">
          <b-nav-item @click.prevent="newTab" href="#"><b>+</b></b-nav-item>
        </template>

        <!-- Render this if no tabs -->
        <template slot="empty">
          <div class="text-center text-muted">
            There are no open tabs<br />
            Open a new tab using the <b>+</b> button above.
          </div>
        </template>
      </b-tabs>
    </b-card>
  </div>
</template>

<script>
import Command from "../components/Command";

const MAX_TAB_COUNT = 5;

export default {
  components: {
    Command
  },
  data() {
    return {
      tabs: [],
      tabCounter: 0
    };
  },
  created() {
    this.newTab();
  },
  methods: {
    closeTab(x) {
      for (let i = 0; i < this.tabs.length; i++) {
        if (this.tabs[i] === x) {
          this.tabs.splice(i, 1);
        }
      }
    },
    newTab() {
      if (this.tabCounter >= MAX_TAB_COUNT) {
        alert("max tab count");
        return;
      }
      this.tabs.push(this.tabCounter++);
    }
  }
};
</script>

<style scoped></style>
