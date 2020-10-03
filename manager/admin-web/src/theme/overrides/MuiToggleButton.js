import palette from "../palette";

export default {
  root: {
    color: palette.icon,
    "&:hover": {
      backgroundColor: "rgba(208, 208, 208, 0.20)",
    },
    "&$selected": {
      backgroundColor: "rgba(208, 208, 208, 0.20)",
      color: palette.primary.main,
      "&:hover": {
        backgroundColor: "rgba(208, 208, 208, 0.30)",
      },
    },
    "&:first-child": {
      borderTopLeftRadius: 4,
      borderBottomLeftRadius: 4,
    },
    "&:last-child": {
      borderTopRightRadius: 4,
      borderBottomRightRadius: 4,
    },
  },
};
