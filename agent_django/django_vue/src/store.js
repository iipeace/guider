import Vue from "vue";
import Vuex from "vuex";
import createLogger from "vuex/dist/logger";
import { Server, Status } from "./model/server";

Vue.use(Vuex);

// root state object.
// each Vuex instance is just a single state tree.
const state = {
  server: new Server("", Status.STOP)
};

// mutations are operations that actually mutates the state.
// each mutation handler gets the entire state tree as the
// first argument, followed by additional payload arguments.
// mutations must be synchronous and can be recorded by plugins
// for debugging purposes.
const mutations = {
  setServer(state, server) {
    if (this.state.server) {
      if (this.state.server instanceof Server) {
        this.state.server.clear();
      }
    }
    this.state.server = server;
    sessionStorage.setItem("server", JSON.stringify(server));
  }
};

// actions are functions that cause side effects and can involve
// asynchronous operations.
const actions = {};

// getters are functions
const getters = {
  getServer: state => {
    const server = JSON.parse(sessionStorage.getItem("server"));
    if (server) {
      return server;
    }
    return state.server;
  }
};

// A Vuex instance is created by combining the state, mutations, actions,
// and getters.
const debug = process.env.NODE_ENV !== "production";

export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations,
  /*
   FIXME : "[vuex] do not mutate vuex store state outside mutation handlers." in server.js
           this issue occur because vuex using 'server'
           change strict mode false to debug
   */
  strict: false,
  plugins: debug ? [createLogger()] : []
});
