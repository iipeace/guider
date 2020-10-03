import React, { useState, useCallback } from "react";
import { NavLink as RouterLink } from "react-router-dom";
import clsx from "clsx";
import PropTypes from "prop-types";
import { makeStyles } from "@material-ui/core/styles";
import { ListItem, Button, Collapse, Link } from "@material-ui/core";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";
import ExpandLessIcon from "@material-ui/icons/ExpandLess";

const useStyles = makeStyles(theme => ({
  item: {
    display: "block",
    paddingTop: 0,
    paddingBottom: 0,
  },
  itemLeaf: {
    display: "flex",
    paddingTop: 0,
    paddingBottom: 0,
  },
  button: {
    padding: "10px 8px",
    justifyContent: "flex-start",
    textTransform: "none",
    letterSpacing: 0,
    width: "100%",
  },
  buttonLeaf: {
    padding: "10px 8px",
    justifyContent: "flex-start",
    textTransform: "none",
    letterSpacing: 0,
    width: "100%",
    // backgroundColor: theme.palette.background.paper,
    fontWeight: theme.typography.fontWeightMedium,
    "&.depth-0": {
      fontWeight: theme.typography.fontWeightBold,
    },
  },
  icon: {
    display: "flex",
    alignItems: "center",
    marginRight: theme.spacing(1),
  },
  expandIcon: {
    marginLeft: "auto",
    height: 16,
    width: 16,
  },
  label: {
    display: "flex",
    alignItems: "center",
    marginLeft: "auto",
  },
  active: {
    backgroundColor: theme.palette.primary.main,
    fontWeight: theme.typography.fontWeightMedium,
    color: theme.palette.primary.contrastText,

    "& $icon": {
      color: theme.palette.primary.contrastText,
    },
    "&:hover": {
      backgroundColor: theme.palette.primary.main,
    },
  },
}));

function NavItem({
  className,
  children,
  title,
  href,
  depth,
  isOpen: isOpenProp,
  icon: Icon,
  label: Label,
  isLink,
  ...rest
}) {
  const classes = useStyles();
  const [isOpen, setIsOpen] = useState(isOpenProp);

  const handleToggle = useCallback(() => {
    setIsOpen(prevIsOpen => !prevIsOpen);
  }, []);

  let paddingLeft = 8;

  if (depth > 0) {
    paddingLeft = 32 + 8 * depth;
  }

  const style = {
    paddingLeft,
  };

  if (children) {
    return (
      <ListItem
        {...rest}
        className={clsx(classes.item, className)}
        disableGutters
        key={title}
      >
        <Button className={classes.button} onClick={handleToggle} style={style}>
          {Icon && <Icon className={classes.icon} />}
          {title}
          {isOpen ? (
            <ExpandLessIcon className={classes.expandIcon} color="inherit" />
          ) : (
            <ExpandMoreIcon className={classes.expandIcon} color="inherit" />
          )}
        </Button>
        <Collapse in={isOpen}>{children}</Collapse>
      </ListItem>
    );
  }

  return (
    <ListItem
      {...rest}
      className={clsx(classes.itemLeaf, className)}
      disableGutters
      key={title}
    >
      {isLink ? (
        <Button
          className={clsx(classes.buttonLeaf, `depth-${depth}`)}
          component={Link}
          style={style}
          underline="none"
          href={href}
          target="_blank"
          rel="noopener"
        >
          {Icon && <Icon className={classes.icon} />}
          {title}
          {Label && (
            <span className={classes.label}>
              <Label />
            </span>
          )}
        </Button>
      ) : (
        <Button
          activeClassName={classes.active}
          className={clsx(classes.buttonLeaf, `depth-${depth}`)}
          component={RouterLink}
          exact
          style={style}
          to={href}
        >
          {Icon && <Icon className={classes.icon} />}
          {title}
          {Label && (
            <span className={classes.label}>
              <Label />
            </span>
          )}
        </Button>
      )}
    </ListItem>
  );
}

NavItem.propTypes = {
  className: PropTypes.string,
  children: PropTypes.node,
  title: PropTypes.string.isRequired,
  href: PropTypes.string,
  depth: PropTypes.number.isRequired,
  isOpen: PropTypes.bool,
  icon: PropTypes.elementType,
  label: PropTypes.elementType,
  isLink: PropTypes.bool,
};

NavItem.defaultProps = {
  className: "",
  children: null,
  href: "",
  isOpen: false,
  icon: null,
  label: null,
  isLink: false,
};

export default NavItem;
