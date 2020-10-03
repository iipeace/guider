import React from "react";
import PropTypes from "prop-types";
import clsx from "clsx";
import { makeStyles } from "@material-ui/core/styles";
import { colors } from "@material-ui/core";
import ReactPaginate from "react-paginate";

const useStyles = makeStyles(theme => ({
  root: {
    ...theme.typography.button,
    listStyle: "none",
    userSelect: "none",
    display: "flex",
    alignItems: "center",
  },
  active: {},
  activeLink: {},
  break: {},
  breakLink: {},
  disabled: {},
  next: {
    marginLeft: theme.spacing(1),
  },
  nextLink: {
    padding: "6px 16px",
    outline: "none",
    cursor: "pointer",
    borderRadius: 4,
    "&:hover": {
      backgroundColor: colors.blueGrey[50],
    },
  },
  page: {},
  pageLink: {
    color: theme.palette.text.secondary,
    padding: theme.spacing(1),
    outline: "none",
    cursor: "pointer",
    width: 40,
    height: 40,
    borderRadius: "50%",
    display: "block",
    textAlign: "center",
    "&:hover": {
      backgroundColor: colors.blueGrey[50],
      color: theme.palette.text.primary,
    },
    "&$activeLink": {
      backgroundColor: colors.blueGrey[50],
      color: theme.palette.text.primary,
    },
  },
  previous: {
    marginRight: theme.spacing(1),
  },
  previousLink: {
    padding: "6px 16px",
    outline: "none",
    cursor: "pointer",
    borderRadius: 4,
    "&:hover": {
      backgroundColor: colors.blueGrey[50],
    },
  },
}));

function Paginate({
  pageCount,
  pageRangeDisplayed,
  onPageChange,
  className,
  ...rest
}) {
  const classes = useStyles();

  return (
    <ReactPaginate
      activeClassName={classes.active}
      activeLinkClassName={classes.activeLink}
      breakClassName={classes.break}
      breakLabel="..."
      breakLinkClassName={classes.breakLink}
      containerClassName={clsx(classes.root, className)}
      disabledClassName={classes.disabled}
      marginPagesDisplayed={2}
      nextClassName={classes.next}
      nextLabel="next"
      nextLinkClassName={classes.nextLink}
      onPageChange={onPageChange}
      pageClassName={classes.page}
      pageCount={pageCount}
      pageLinkClassName={classes.pageLink}
      pageRangeDisplayed={pageRangeDisplayed}
      previousClassName={classes.previous}
      previousLabel="previous"
      previousLinkClassName={classes.previousLink}
      subContainerClassName="pages pagination"
      {...rest}
    />
  );
}

Paginate.propTypes = {
  className: PropTypes.string,
  onPageChange: PropTypes.func,
  pageCount: PropTypes.number,
  pageRangeDisplayed: PropTypes.number,
};

Paginate.defaultProps = {
  onPageChange: () => {},
  pageCount: 3,
  pageRangeDisplayed: 5,
};

export default Paginate;
