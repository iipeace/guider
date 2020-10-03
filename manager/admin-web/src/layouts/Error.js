import React, { Suspense } from "react";
import { renderRoutes } from "react-router-config";
import PropTypes from "prop-types";
import { makeStyles } from "@material-ui/core/styles";
import { LinearProgress } from "@material-ui/core";
import layoutProperties from "src/constants/layoutProperties";

const useStyles = makeStyles(() => ({
  root: {
    minWidth: layoutProperties.ROOT_LAYOUT_MIN_WIDTH,
    minHeight: "100vh",
    display: "flex",
    "@media all and (msHighContrast:none)": {
      height: 0, // IE11 fix
    },
  },
  content: {
    flexGrow: 1,
    maxWidth: "100%",
    overflowX: "hidden",
  },
}));

function Error({ route }) {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <div className={classes.content}>
        <Suspense fallback={<LinearProgress />}>
          {renderRoutes(route.routes)}
        </Suspense>
      </div>
    </div>
  );
}

Error.propTypes = {
  route: PropTypes.object,
};

Error.defaultProps = {
  route: {},
};

export default Error;
