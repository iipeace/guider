import React, { useContext } from "react";
import { makeStyles } from "@material-ui/core/styles";
import { Card, CardContent, Typography, Divider } from "@material-ui/core";
import LockIcon from "@material-ui/icons/Lock";
import Page from "src/components/Page";
import gradients from "src/utils/gradients";
import { StringsContext } from "src/App";
import LoginForm from "./LoginForm";

const useStyles = makeStyles(theme => ({
  root: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    height: "100%",
    padding: theme.spacing(6, 2),
  },
  card: {
    display: "flex",
    position: "relative",
    maxWidth: "100%",
    width: theme.breakpoints.values.sm,
    overflow: "visible",
  },
  content: {
    width: "100%",
    padding: theme.spacing(8, 4, 3, 4),
  },
  icon: {
    position: "absolute",
    top: -32,
    left: theme.spacing(3),
    height: 64,
    width: 64,
    padding: theme.spacing(1),
    backgroundImage: gradients.green,
    color: theme.palette.common.white,
    borderRadius: theme.shape.borderRadius,
    fontSize: 32,
  },
  loginForm: {
    marginTop: theme.spacing(3),
  },
  divider: {
    margin: theme.spacing(2, 0),
  },
}));

function Login() {
  const classes = useStyles();

  const strings = useContext(StringsContext);

  return (
    <Page className={classes.root} title={`로그인 | ${strings.webName}`}>
      <Card className={classes.card}>
        <CardContent className={classes.content}>
          <LockIcon className={classes.icon} />
          <Typography gutterBottom variant="h3">
            로그인
          </Typography>
          <Typography variant="subtitle2">
            아이디와 비밀번호를 입력해서 로그인해주세요.
          </Typography>
          <LoginForm className={classes.loginForm} />
          <Divider className={classes.divider} />
          <Typography align="center" variant="subtitle2">
            Copyright © 2020. Guider All rights reserved.
          </Typography>
        </CardContent>
      </Card>
    </Page>
  );
}

export default Login;
