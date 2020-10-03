import React, { lazy } from "react";
import { Redirect } from "react-router-dom";
import routeUrls from "src/constants/routeUrls";
import appConfig from "src/configs/appConfig";
import AuthLayout from "./layouts/Auth";
import ErrorLayout from "./layouts/Error";
import DashboardLayout from "./layouts/Dashboard";

/**
 * Auth 기반 path 의 조건에 따른 routes 반환
 */
const getAuthRoutes = () => {
  let routes = [];
  // Auth 를 지원해야만 routes 에 로그인/회원가입 등 추가
  if (appConfig.isAuth) {
    routes = [
      {
        path: routeUrls.LOGIN,
        exact: true,
        component: lazy(() => import("src/views/Login")),
      },
      {
        path: routeUrls.REGISTER,
        exact: true,
        component: lazy(() => import("src/views/Register")),
      },
    ];
  }

  return routes;
};

export default [
  {
    path: routeUrls.ROOT,
    exact: true,
    component: () => <Redirect to={routeUrls.HOME} />,
  },
  {
    path: routeUrls.AUTH,
    component: AuthLayout,
    routes: [
      ...getAuthRoutes(),
      {
        component: () => <Redirect to={routeUrls.ERROR_404} />,
      },
    ],
  },
  {
    path: routeUrls.ERRORS,
    component: ErrorLayout,
    routes: [
      {
        path: routeUrls.ERROR_401,
        exact: true,
        component: lazy(() => import("src/views/Error401")),
      },
      {
        path: routeUrls.ERROR_404,
        exact: true,
        component: lazy(() => import("src/views/Error404")),
      },
      {
        path: routeUrls.ERROR_500,
        exact: true,
        component: lazy(() => import("src/views/Error500")),
      },
      {
        component: () => <Redirect to={routeUrls.ERROR_404} />,
      },
    ],
  },
  {
    route: "*",
    component: DashboardLayout,
    routes: [
      {
        path: routeUrls.HOME,
        exact: true,
        component: lazy(() => import("src/views/Home")),
      },
      {
        component: () => <Redirect to={routeUrls.ERROR_404} />,
      },
    ],
  },
];
