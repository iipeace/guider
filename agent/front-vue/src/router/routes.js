// GeneralViews
import NotFound from "@/pages/NotFoundPage.vue";

// Admin pages
const Dashboard = () =>
  import(/* webpackChunkName: "dashboard" */ "@/pages/Dashboard.vue");
const Command = () =>
  import(/* webpackChunkName: "dashboard" */ "@/pages/Command.vue");
const History = () =>
  import(/* webpackChunkName: "dashboard" */ "@/pages/History.vue");

const routes = [
  {
    path: "/dashboard",
    name: "Dashboard",
    alias: "/",
    component: Dashboard
  },
  { path: "/command", name: "Command", component: Command },
  { path: "/history", name: "History", component: History },
  { path: "*", component: NotFound }
];

export default routes;
