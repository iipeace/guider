const path = require("path");

module.exports = {
  extends: ["react-app", "airbnb", "prettier"],
  rules: {
    "react/prefer-stateless-function": "off",
    "react/jsx-filename-extension": "off",
    "react/jsx-one-expression-per-line": "off",
    "no-unused-vars": "warn",
    "react/jsx-props-no-spreading": "off",
    "no-shadow": "off",
    "no-use-before-define": "off",
    "import/prefer-default-export": "off",
    "no-param-reassign": "off",
    "jsx-a11y/media-has-caption": [
      "warn",
      {
        audio: ["Audio"],
        video: ["Video"],
        track: ["Track"],
      },
    ],
    "import/no-cycle": "off",
    "react/forbid-prop-types": "off",
    "react/jsx-wrap-multilines": "off",
  },
  env: {
    browser: true,
  },
  settings: {
    "import/resolver": {
      node: {
        paths: [""],
      },
    },
  },
};
