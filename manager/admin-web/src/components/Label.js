import React from "react";
import PropTypes from "prop-types";
import clsx from "clsx";
import { makeStyles } from "@material-ui/core/styles";
import { Typography, colors } from "@material-ui/core";

const useStyles = makeStyles(theme => ({
  root: {
    display: "inline-flex",
    alignItems: "center",
    justifyContent: "center",
    flexGrow: 0,
    flexShrink: 0,
    borderRadius: 2,
    height: 24,
    minWidth: 24,
    whiteSpace: "nowrap",
    padding: theme.spacing(0.5, 1),
  },
  rounded: {
    borderRadius: 10,
    padding: theme.spacing(0.5),
  },
}));

function Label({ className, variant, color, shape, children, style, ...rest }) {
  const classes = useStyles();
  const rootClassName = clsx(
    {
      [classes.root]: true,
      [classes.rounded]: shape === "rounded",
    },
    className,
  );
  const finalStyle = { ...style };

  if (variant === "contained") {
    finalStyle.backgroundColor = color;
    finalStyle.color = "#FFF";
  } else {
    finalStyle.border = `1px solid ${color}`;
    finalStyle.color = color;
  }

  return (
    <Typography
      {...rest}
      className={rootClassName}
      style={finalStyle}
      variant="overline"
    >
      {children}
    </Typography>
  );
}

Label.propTypes = {
  children: PropTypes.node,
  className: PropTypes.string,
  style: PropTypes.object,
  color: PropTypes.string,
  shape: PropTypes.oneOf(["square", "rounded"]),
  variant: PropTypes.oneOf(["contained", "outlined"]),
};

Label.defaultProps = {
  children: null,
  className: "",
  style: {},
  color: colors.grey[600],
  shape: "square",
  variant: "contained",
};

export default Label;
