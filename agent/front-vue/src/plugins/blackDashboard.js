import SideBar from "@/components/SidebarPlugin";

//css assets
import "@/assets/sass/black-dashboard.scss";
import "@/assets/css/nucleo-icons.css";
import "@/assets/demo/demo.css";

export default {
  install(Vue) {
    Vue.use(SideBar);
  }
};
