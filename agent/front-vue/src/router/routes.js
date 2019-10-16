// GeneralViews
import NotFound from "@/pages/NotFoundPage.vue";

// Admin pages
const Dashboard = () =>
  import(/* webpackChunkName: "dashboard" */ "@/pages/Dashboard.vue");
const Command = () =>
  import(/* webpackChunkName: "dashboard" */ "@/pages/Command.vue");
const Background = () =>
  import(/* webpackChunkName: "dashboard" */ "@/pages/Background.vue");

const routes = [
  { path: "/dashboard", name: "Dashboard", alias: "/", component: Dashboard },
  { path: "/command", name: "Command", component: Command },
  { path: "/background", name: "Background", component: Background },
  { path: "*", component: NotFound }
];

export default routes;
