import React, { useState } from "react";
import PropTypes from "prop-types";
import { makeStyles } from "@material-ui/core/styles";
import { Button, TextField, CircularProgress, Box } from "@material-ui/core";
import clsx from "clsx";
import { useDispatch } from "react-redux";
import { useHistory } from "react-router";
import { useLocation } from "react-router-dom";
import { useFormik } from "formik";
import { useSnackbar } from "notistack";
import progressProperties from "src/constants/progressProperties";
import routeUrls from "src/constants/routeUrls";
import * as Yup from "yup";
import _ from "lodash";
import { sessionActions } from "src/actions";
import regexes from "src/constants/regexes";

const useStyles = makeStyles(theme => ({
  root: {},
  fields: {
    display: "flex",
    flexWrap: "wrap",
    margin: theme.spacing(-1),

    "& > *": {
      flexGrow: 1,
      margin: theme.spacing(1),
    },
  },
}));

function LoginForm({ className, ...rest }) {
  const classes = useStyles();
  const history = useHistory();
  const location = useLocation();
  const dispatch = useDispatch();
  const { enqueueSnackbar } = useSnackbar();

  const [isLoading, setIsLoading] = useState(false);

  /* 유효성 체크 */
  const formik = useFormik({
    initialValues: {
      email: "",
      password: "",
    },
    validationSchema: Yup.object({
      email: Yup.string()
        .email("이메일 형식으로 입력해주세요.")
        .required("아이디(이메일)를 입력해주세요."),
      password: Yup.string()
        .matches(regexes.PASSWORD_REGEX, {
          message:
            "비밀번호는 8자 이상이며 대소문자/숫자/특수문자를 모두 포함해야 합니다.",
          excludeEmptyString: false,
        })
        .required("비밀번호를 입력해주세요."),
    }),
    onSubmit: async values => {
      setIsLoading(true);

      const { email, password } = values;

      // 로그인 성공, 실패 동작
      try {
        // 계정 관리를 위한 모듈 필요(임시로 token 에 1234 저장)
        dispatch(sessionActions.login("1234", { email }));

        enqueueSnackbar("로그인에 성공했습니다. 메인화면으로 이동합니다.", {
          variant: "success",
          autoHideDuration: 3000,
        });

        // 접근주소가 있으면 해당 주소로 이동, 없다면 기본 홈으로 이동
        const { from } = location.state || {
          from: { pathname: routeUrls.ROOT },
        };
        history.push(from);
      } catch (error) {
        enqueueSnackbar(
          "로그인에 실패했습니다. 아이디와 비밀번호를 확인해주세요.",
          {
            variant: "error",
            autoHideDuration: 3000,
          },
        );
      } finally {
        setIsLoading(false);
      }
    },
  });

  return (
    <form
      {...rest}
      className={clsx(classes.root, className)}
      onSubmit={formik.handleSubmit}
      noValidate
    >
      <div className={classes.fields}>
        <TextField
          variant="outlined"
          required
          fullWidth
          id="email"
          name="email"
          type="email"
          label="아이디(이메일)"
          autoComplete="email"
          autoFocus
          error={!!(formik.touched.email && formik.errors.email)}
          helperText={
            formik.touched.email && formik.errors.email
              ? formik.errors.email
              : null
          }
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          value={formik.values.email}
        />
        <TextField
          variant="outlined"
          required
          fullWidth
          id="password"
          name="password"
          type="password"
          label="비밀번호"
          autoComplete="current-password"
          error={!!(formik.touched.password && formik.errors.password)}
          helperText={
            formik.touched.password && formik.errors.password
              ? formik.errors.password
              : null
          }
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          value={formik.values.password}
        />
      </div>
      <Box position="relative" mt={2}>
        <Button
          type="submit"
          variant="contained"
          size="large"
          color="primary"
          fullWidth
          disabled={isLoading}
          startIcon={
            isLoading && (
              <CircularProgress
                size={progressProperties.CIRCULAR_PROGRESS_MEDIUM}
              />
            )
          }
        >
          로그인
        </Button>
      </Box>
    </form>
  );
}

LoginForm.propTypes = {
  className: PropTypes.string,
};

LoginForm.defaultProps = {
  className: "",
};

export default LoginForm;
