import React, { useState, useEffect } from "react";
import { useHistory } from "react-router";
import { Link as RouterLink } from "react-router-dom";
import validate from "validate.js";
import clsx from "clsx";
import PropTypes from "prop-types";
import { makeStyles } from "@material-ui/core/styles";
import routeUrls from "src/constants/routeUrls";
import {
  Button,
  Checkbox,
  FormHelperText,
  TextField,
  Typography,
  Link,
} from "@material-ui/core";

const schema = {
  firstName: {
    presence: { allowEmpty: false, message: "is required" },
    length: {
      maximum: 32,
    },
  },
  lastName: {
    presence: { allowEmpty: false, message: "is required" },
    length: {
      maximum: 32,
    },
  },
  email: {
    presence: { allowEmpty: false, message: "is required" },
    email: true,
    length: {
      maximum: 64,
    },
  },
  password: {
    presence: { allowEmpty: false, message: "is required" },
    length: {
      maximum: 128,
    },
  },
  policy: {
    presence: { allowEmpty: false, message: "is required" },
    checked: true,
  },
};

const useStyles = makeStyles(theme => ({
  root: {},
  fields: {
    margin: theme.spacing(-1),
    display: "flex",
    flexWrap: "wrap",
    "& > *": {
      flexGrow: 1,
      margin: theme.spacing(1),
    },
  },
  policy: {
    display: "flex",
    alignItems: "center",
  },
  policyCheckbox: {
    marginLeft: "-14px",
  },
  submitButton: {
    marginTop: theme.spacing(2),
    width: "100%",
  },
}));

function RegisterForm({ className, ...rest }) {
  const classes = useStyles();
  const history = useHistory();
  const [formState, setFormState] = useState({
    isValid: false,
    values: {},
    touched: {},
    errors: {},
  });

  const handleChange = event => {
    event.persist();

    setFormState(prevFormState => ({
      ...prevFormState,
      values: {
        ...prevFormState.values,
        [event.target.name]:
          event.target.type === "checkbox"
            ? event.target.checked
            : event.target.value,
      },
      touched: {
        ...prevFormState.touched,
        [event.target.name]: true,
      },
    }));
  };

  const handleSubmit = event => {
    event.preventDefault();
    history.push(routeUrls.ROOT);
  };

  const hasError = field =>
    !!(formState.touched[field] && formState.errors[field]);

  useEffect(() => {
    const errors = validate(formState.values, schema);

    setFormState(prevFormState => ({
      ...prevFormState,
      isValid: !errors,
      errors: errors || {},
    }));
  }, [formState.values]);

  return (
    <form
      {...rest}
      className={clsx(classes.root, className)}
      onSubmit={handleSubmit}
    >
      <div className={classes.fields}>
        <TextField
          error={hasError("firstName")}
          helperText={
            hasError("firstName") ? formState.errors.firstName[0] : null
          }
          label="First name"
          name="firstName"
          onChange={handleChange}
          value={formState.values.firstName || ""}
          variant="outlined"
        />
        <TextField
          error={hasError("lastName")}
          helperText={
            hasError("lastName") ? formState.errors.lastName[0] : null
          }
          label="Last name"
          name="lastName"
          onChange={handleChange}
          value={formState.values.lastName || ""}
          variant="outlined"
        />
        <TextField
          error={hasError("email")}
          fullWidth
          helperText={hasError("email") ? formState.errors.email[0] : null}
          label="Email address"
          name="email"
          onChange={handleChange}
          value={formState.values.email || ""}
          variant="outlined"
        />
        <TextField
          error={hasError("password")}
          fullWidth
          helperText={
            hasError("password") ? formState.errors.password[0] : null
          }
          label="Password"
          name="password"
          onChange={handleChange}
          type="password"
          value={formState.values.password || ""}
          variant="outlined"
        />
        <div>
          <div className={classes.policy}>
            <Checkbox
              checked={formState.values.policy || false}
              className={classes.policyCheckbox}
              color="primary"
              name="policy"
              onChange={handleChange}
            />
            <Typography color="textSecondary" variant="body1">
              I have read the{" "}
              <Link
                color="secondary"
                component={RouterLink}
                to="#"
                underline="always"
                variant="h6"
              >
                Terms and Conditions
              </Link>
            </Typography>
          </div>
          {hasError("policy") && (
            <FormHelperText error>{formState.errors.policy[0]}</FormHelperText>
          )}
        </div>
      </div>
      <Button
        className={classes.submitButton}
        color="secondary"
        disabled={!formState.isValid}
        size="large"
        type="submit"
        variant="contained"
      >
        Create account
      </Button>
    </form>
  );
}

RegisterForm.propTypes = {
  className: PropTypes.string,
};

RegisterForm.defaultProps = {
  className: "",
};

export default RegisterForm;
