import "@babel/polyfill";
import "mutationobserver-shim";
import "babel-polyfill";
import Vue from "vue";
import "./plugins/bootstrap-vue";
import VueRouter from "vue-router";
import RouterPrefetch from "vue-router-prefetch";
import App from "./App";
import router from "./router/index";
import VueSocketIO from "vue-socket.io";
import { library } from "@fortawesome/fontawesome-svg-core";
import Datetime from "vue-datetime";
import "vue-datetime/dist/vue-datetime.css";
import {
  faBars,
  faCheck,
  faCircle,
  faPlus,
  faSave,
  faTimes
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import store from "./store";
import "@/assets/sass/black-dashboard.scss";
import "@/assets/css/nucleo-icons.css";

Vue.use(Datetime);
Vue.use(VueRouter);
Vue.use(RouterPrefetch);

Vue.config.productionTip = false;

const serverAddr =
  process.env.NODE_ENV === "development"
    ? "http://localhost:8000"
    : document.getElementById("serverAddr").value;


Vue.use(
  new VueSocketIO({
    debug: process.env.NODE_ENV !== "production",
    connection: serverAddr
  })
);

library.add(faPlus, faCircle, faTimes, faSave, faCheck, faBars);
Vue.component("font-awesome-icon", FontAwesomeIcon);

/* eslint-disable no-new */
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
