import "@babel/polyfill";
import "mutationobserver-shim";
import "babel-polyfill";
import Vue from "vue";
import "./plugins/bootstrap-vue";
import VueRouter from "vue-router";
import RouterPrefetch from "vue-router-prefetch";
import App from "./App";
import router from "./router/index";
import BlackDashboard from "./plugins/blackDashboard";
import VueSocketIO from "vue-socket.io";

Vue.use(BlackDashboard);
Vue.use(VueRouter);
Vue.use(RouterPrefetch);

Vue.config.productionTip = false;
const serverAddr = "http://localhost:8000";

Vue.use(
  new VueSocketIO({
    debug: process.env.NODE_ENV !== "production",
    connection: serverAddr // 'http://localhost:5000'
  })
);

/* eslint-disable no-new */
new Vue({
  router,
  render: h => h(App)
}).$mount("#app");
