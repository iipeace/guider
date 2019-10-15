import DashboardLayout from "@/layout/DashboardLayout.vue";
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
  {
    path: "/",
    component: DashboardLayout,
    redirect: "/dashboard",
    children: [
      {
        path: "dashboard",
        name: "dashboard",
        component: Dashboard
      },
      {
        path: "command",
        name: "command",
        component: Command
      },
      {
        path: "background",
        name: "background",
        component: Background
      }
    ]
  },
  { path: "*", component: NotFound }
];

export default routes;
