import React, { Suspense, useState } from "react";
import { renderRoutes } from "react-router-config";
import { useLocation } from "react-router-dom";
import PropTypes from "prop-types";
import { makeStyles } from "@material-ui/core/styles";
import { LinearProgress } from "@material-ui/core";
import { useSelector } from "react-redux";
import { Redirect } from "react-router";
import routeUrls from "src/constants/routeUrls";
import appConfig from "src/configs/appConfig";
import layoutProperties from "src/constants/layoutProperties";
import TopBar from "./TopBar";
import NavBar from "./NavBar";

const useStyles = makeStyles(theme => ({
  root: {
    minWidth: layoutProperties.ROOT_LAYOUT_MIN_WIDTH,
  },
  container: {
    display: "flex",
    minHeight: "100vh",

    "@media all and (msHighContrast:none)": {
      height: 0, // IE11 fix
    },
  },
  content: {
    flexGrow: 1,
    maxWidth: "100%",
    paddingTop: layoutProperties.TOPBAR_LAYOUT_MEDIUM_HEIGHT,
    overflowX: "hidden",

    [theme.breakpoints.up("lg")]: {
      paddingLeft: layoutProperties.NAVBAR_LAYOUT_WIDTH,
    },
    [theme.breakpoints.down("xs")]: {
      paddingTop: layoutProperties.TOPBAR_LAYOUT_SMALL_HEIGHT,
    },
  },
}));

function Dashboard({ route }) {
  const classes = useStyles();
  const location = useLocation();
  const { isLoggedIn } = useSelector(state => state.session);

  const [isOpenNavBarMobile, setIsOpenNavBarMobile] = useState(false);

  if (appConfig.isAuth) {
    // 인증 기능 지원여부 확인해서 로그인 되지 않았다면 로그인 화면으로 이동
    if (!isLoggedIn)
      return (
        <Redirect
          to={{
            pathname: routeUrls.LOGIN,
            state: { from: location },
          }}
        />
      );
  }

  return (
    <div className={classes.root}>
      <TopBar onOpenNavBarMobile={() => setIsOpenNavBarMobile(true)} />
      <NavBar
        isOpenMobile={isOpenNavBarMobile}
        onMobileClose={() => setIsOpenNavBarMobile(false)}
      />
      <div className={classes.container}>
        <div className={classes.content}>
          <Suspense fallback={<LinearProgress />}>
            {renderRoutes(route.routes)}
          </Suspense>
        </div>
      </div>
    </div>
  );
}

Dashboard.propTypes = {
  route: PropTypes.object,
};

Dashboard.defaultProps = {
  route: {},
};

export default Dashboard;
