import React, { useContext } from "react";
import { Link as RouterLink } from "react-router-dom";
import clsx from "clsx";
import PropTypes from "prop-types";
import routeUrls from "src/constants/routeUrls";
import { makeStyles } from "@material-ui/core/styles";
import { AppBar, Toolbar, Typography, Box, Hidden } from "@material-ui/core";
import layoutProperties from "src/constants/layoutProperties";
import { StringsContext } from "src/App";

const useStyles = makeStyles(theme => ({
  root: {
    minWidth: layoutProperties.ROOT_LAYOUT_MIN_WIDTH,
    boxShadow: "none",
  },
  logoIcon: {
    width: "auto",
    height: 32,
    marginRight: theme.spacing(2),
  },
}));

function TopBar({ className, ...rest }) {
  const classes = useStyles();

  const strings = useContext(StringsContext);

  return (
    <AppBar {...rest} className={clsx(classes.root, className)} color="primary">
      <Toolbar>
        <RouterLink to={routeUrls.ROOT}>
          <Box display="flex" alignItems="center" color="primary.contrastText">
            <Hidden xsDown>
              <img
                className={classes.logoIcon}
                src="/images/logos/logo-guider.png"
                alt="로고"
              />
            </Hidden>
            <Typography variant="h5" component="h1" color="inherit">
              {strings.webName}
            </Typography>
          </Box>
        </RouterLink>
      </Toolbar>
    </AppBar>
  );
}

TopBar.propTypes = {
  className: PropTypes.string,
};

TopBar.defaultProps = {
  className: "",
};

export default TopBar;
