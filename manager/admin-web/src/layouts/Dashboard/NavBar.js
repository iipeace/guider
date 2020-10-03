import React, { useEffect } from "react";
import { useLocation, matchPath } from "react-router";
import clsx from "clsx";
import PropTypes from "prop-types";
import { makeStyles } from "@material-ui/core/styles";
import { Drawer, List, ListSubheader, Hidden } from "@material-ui/core";
import NavItem from "src/components/NavItem";
import layoutProperties from "src/constants/layoutProperties";
import navConfig from "./navConfig";

const useStyles = makeStyles(theme => ({
  root: {
    display: "flex",
    flexDirection: "column",
    height: "100%",
  },
  mobileDrawer: {
    width: layoutProperties.NAVBAR_LAYOUT_WIDTH,
  },
  desktopDrawer: {
    width: layoutProperties.NAVBAR_LAYOUT_WIDTH,
    height: `calc(100% - ${layoutProperties.TOPBAR_LAYOUT_MEDIUM_HEIGHT}px)`,
    top: layoutProperties.TOPBAR_LAYOUT_MEDIUM_HEIGHT,
  },
  navigation: {
    flexGrow: 1,
    padding: theme.spacing(0, 2, 2, 2),
    overflow: "auto",
  },
}));

const reduceChildRoutes = ({ acc, pathname, item, depth = 0 }) => {
  if (item.items) {
    const open = matchPath(pathname, {
      path: item.href,
      exact: false,
    });

    acc.push(
      <NavItem
        depth={depth}
        icon={item.icon}
        key={item.href}
        label={item.label}
        isOpen={Boolean(open)}
        title={item.title}
      >
        {renderNavItems({
          depth: depth + 1,
          pathname,
          items: item.items,
        })}
      </NavItem>,
    );
  } else {
    acc.push(
      <NavItem
        depth={depth}
        href={item.href}
        icon={item.icon}
        key={item.href}
        label={item.label}
        title={item.title}
        isLink={item.isLink}
      />,
    );
  }

  return acc;
};

function renderNavItems({ items, subheader, key, ...rest }) {
  return (
    <List key={key}>
      {subheader && <ListSubheader disableSticky>{subheader}</ListSubheader>}
      {items.reduce(
        (acc, item) => reduceChildRoutes({ acc, item, ...rest }),
        [],
      )}
    </List>
  );
}

renderNavItems.propTypes = {
  items: PropTypes.array,
  subheader: PropTypes.string,
  key: PropTypes.string,
};

renderNavItems.defaultProps = {
  items: [],
  subheader: "",
  key: "",
};

function NavBar({ className, isOpenMobile, onMobileClose, ...rest }) {
  const classes = useStyles();
  const { pathname } = useLocation();

  useEffect(() => {
    if (isOpenMobile && onMobileClose) {
      onMobileClose();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pathname]);

  const content = (
    <div {...rest} className={clsx(classes.root, className)}>
      <nav className={classes.navigation}>
        {navConfig.map(list =>
          renderNavItems({
            items: list.items,
            subheader: list.subheader,
            pathname,
            key: list.subheader ? list.subheader : list.key,
          }),
        )}
      </nav>
    </div>
  );

  return (
    <>
      <Hidden lgUp>
        <Drawer
          anchor="left"
          classes={{
            paper: classes.mobileDrawer,
          }}
          onClose={onMobileClose}
          open={isOpenMobile}
          variant="temporary"
        >
          {content}
        </Drawer>
      </Hidden>
      <Hidden mdDown>
        <Drawer
          anchor="left"
          classes={{
            paper: classes.desktopDrawer,
          }}
          open
          variant="persistent"
        >
          {content}
        </Drawer>
      </Hidden>
    </>
  );
}

NavBar.propTypes = {
  className: PropTypes.string,
  isOpenMobile: PropTypes.bool,
  onMobileClose: PropTypes.func,
};

NavBar.defaultProps = {
  className: "",
  isOpenMobile: false,
  onMobileClose: () => {},
};

export default NavBar;
