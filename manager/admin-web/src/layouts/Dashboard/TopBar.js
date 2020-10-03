import React, { useContext } from "react";
import { Link as RouterLink } from "react-router-dom";
import { useHistory } from "react-router";
import { useDispatch } from "react-redux";
import PropTypes from "prop-types";
import clsx from "clsx";
import { makeStyles } from "@material-ui/core/styles";
import {
  AppBar,
  IconButton,
  Toolbar,
  Hidden,
  Typography,
  Box,
} from "@material-ui/core";
import MenuIcon from "@material-ui/icons/Menu";
import ExitToAppIcon from "@material-ui/icons/ExitToApp";
import routeUrls from "src/constants/routeUrls";
import appConfig from "src/configs/appConfig";
import layoutProperties from "src/constants/layoutProperties";
import { sessionActions } from "src/actions";
import { StringsContext } from "src/App";

const useStyles = makeStyles(theme => ({
  root: {
    minWidth: layoutProperties.ROOT_LAYOUT_MIN_WIDTH,
    boxShadow: "none",
  },
  flexGrow: {
    flexGrow: 1,
  },
  logoIcon: {
    width: "auto",
    height: 32,
    marginRight: theme.spacing(1.5),
  },
  navBarMenuButton: {
    marginRight: theme.spacing(1),
  },
  logoutButton: {
    marginLeft: theme.spacing(1),
  },
}));

function TopBar({ className, onOpenNavBarMobile, ...rest }) {
  const classes = useStyles();
  const history = useHistory();
  const dispatch = useDispatch();

  const strings = useContext(StringsContext);

  // 로그아웃
  const handleLogout = () => {
    // 계정 관리를 위한 모듈 필요
    dispatch(sessionActions.logout());

    history.push(routeUrls.LOGIN);
  };

  return (
    <AppBar {...rest} className={clsx(classes.root, className)} color="primary">
      <Toolbar>
        <Hidden lgUp>
          <IconButton
            className={classes.navBarMenuButton}
            color="inherit"
            onClick={onOpenNavBarMobile}
          >
            <MenuIcon />
          </IconButton>
        </Hidden>
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
        <div className={classes.flexGrow} />
        {appConfig.isAuth && (
          <IconButton
            className={classes.logoutButton}
            color="inherit"
            onClick={handleLogout}
          >
            <ExitToAppIcon />
          </IconButton>
        )}
      </Toolbar>
    </AppBar>
  );
}

TopBar.propTypes = {
  className: PropTypes.string,
  onOpenNavBarMobile: PropTypes.func,
};

TopBar.defaultProps = {
  className: "",
  onOpenNavBarMobile: () => {},
};

export default TopBar;
