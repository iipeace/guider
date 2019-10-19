// GeneralViews
import NotFound from "@/pages/NotFoundPage.vue";

// Admin pages
const Dashboard = () =>
  import(/* webpackChunkName: "dashboard" */ "@/pages/Dashboard.vue");
const CommandTabs = () =>
  import(/* webpackChunkName: "dashboard" */ "@/pages/CommandTabs.vue");
const History = () =>
  import(/* webpackChunkName: "dashboard" */ "@/pages/History.vue");

const routes = [
  {
    path: "/dashboard",
    name: "Dashboard",
    alias: "/",
    component: Dashboard
  },
  { path: "/commandTabs", name: "Command Tabs", component: CommandTabs },
  { path: "/history", name: "History", component: History },
  { path: "*", component: NotFound }
];

export default routes;
