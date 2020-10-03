import palette from "./palette";

export default {
  fontFamily: [
    "'Noto Sans KR'",
    "'Roboto'",
    "'Helvetica'",
    "'Arial'",
    "sans-serif",
  ].join(","),
  h1: {
    color: palette.text.primary,
    fontWeight: 700,
    fontSize: "35px",
    lineHeight: "40px",
  },
  h2: {
    color: palette.text.primary,
    fontWeight: 700,
    fontSize: "29px",
    lineHeight: "32px",
  },
  h3: {
    color: palette.text.primary,
    fontWeight: 700,
    fontSize: "24px",
    lineHeight: "28px",
  },
  h4: {
    color: palette.text.primary,
    fontWeight: 700,
    fontSize: "20px",
    lineHeight: "24px",
  },
  h5: {
    color: palette.text.primary,
    fontWeight: 700,
    fontSize: "16px",
    lineHeight: "20px",
  },
  h6: {
    color: palette.text.primary,
    fontWeight: 700,
    fontSize: "14px",
    lineHeight: "20px",
  },
  subtitle1: {
    color: palette.text.primary,
    fontWeight: 500,
    fontSize: "16px",
    lineHeight: "25px",
  },
  subtitle2: {
    color: palette.text.secondary,
    fontWeight: 500,
    fontSize: "14px",
    lineHeight: "21px",
  },
  body1: {
    color: palette.text.primary,
    fontWeight: 500,
    fontSize: "14px",
    lineHeight: "21px",
  },
  body2: {
    color: palette.text.secondary,
    fontWeight: 500,
    fontSize: "12px",
    lineHeight: "18px",
  },
  button: {
    color: palette.text.primary,
    fontWeight: 700,
    fontSize: "14px",
  },
  caption: {
    color: palette.text.secondary,
    fontWeight: 500,
    fontSize: "12px",
    lineHeight: "14px",
  },
  overline: {
    color: palette.text.secondary,
    fontSize: "12px",
    fontWeight: 700,
    lineHeight: "14px",
    textTransform: "uppercase",
  },
};
