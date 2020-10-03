import React, { Suspense } from "react";
import { renderRoutes } from "react-router-config";
import PropTypes from "prop-types";
import { makeStyles } from "@material-ui/core/styles";
import { LinearProgress } from "@material-ui/core";
import { useSelector } from "react-redux";
import { Redirect } from "react-router";
import appConfig from "src/configs/appConfig";
import layoutProperties from "src/constants/layoutProperties";
import routeUrls from "src/constants/routeUrls";
import TopBar from "./TopBar";

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

    [theme.breakpoints.down("xs")]: {
      paddingTop: layoutProperties.TOPBAR_LAYOUT_SMALL_HEIGHT,
    },
  },
}));

function Auth({ route }) {
  const classes = useStyles();
  const { isLoggedIn } = useSelector(state => state.session);

  if (appConfig.isAuth) {
    // 인증 기능 지원여부 확인해서 로그인 되어있으면 ROOT 화면으로 이동
    if (isLoggedIn) return <Redirect to={routeUrls.ROOT} />;
  } else {
    // 인증 기능 미지원이면 ROOT 화면으로 이동
    return <Redirect to={routeUrls.ROOT} />;
  }

  return (
    <div className={classes.root}>
      <TopBar />
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

Auth.propTypes = {
  route: PropTypes.object,
};

Auth.defaultProps = {
  route: {},
};

export default Auth;
