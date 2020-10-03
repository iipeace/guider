import React from "react";
import { Link as RouterLink } from "react-router-dom";
import { makeStyles } from "@material-ui/core/styles";
import {
  Card,
  CardContent,
  CardMedia,
  Typography,
  Divider,
  Link,
  Avatar,
} from "@material-ui/core";
import PersonAddIcon from "@material-ui/icons/PersonAddOutlined";
import gradients from "src/utils/gradients";
import Page from "src/components/Page";
import RegisterForm from "./RegisterForm";

const useStyles = makeStyles(theme => ({
  root: {
    height: "100%",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    padding: theme.spacing(6, 2),
  },
  card: {
    width: theme.breakpoints.values.md,
    maxWidth: "100%",
    overflow: "visible",
    display: "flex",
    position: "relative",
    "& > *": {
      flexGrow: 1,
      flexBasis: "50%",
      width: "50%",
    },
  },
  content: {
    padding: theme.spacing(8, 4, 3, 4),
  },
  media: {
    borderTopRightRadius: 4,
    borderBottomRightRadius: 4,
    padding: theme.spacing(3),
    color: theme.palette.common.white,
    display: "flex",
    flexDirection: "column",
    justifyContent: "flex-end",
    [theme.breakpoints.down("md")]: {
      display: "none",
    },
  },
  icon: {
    backgroundImage: gradients.orange,
    color: theme.palette.common.white,
    borderRadius: theme.shape.borderRadius,
    padding: theme.spacing(1),
    position: "absolute",
    top: -32,
    left: theme.spacing(3),
    height: 64,
    width: 64,
    fontSize: 32,
  },
  registerForm: {
    marginTop: theme.spacing(3),
  },
  divider: {
    margin: theme.spacing(2, 0),
  },
  person: {
    marginTop: theme.spacing(2),
    display: "flex",
  },
  avatar: {
    marginRight: theme.spacing(2),
  },
}));

function Register() {
  const classes = useStyles();

  return (
    <Page className={classes.root} title="Register">
      <Card className={classes.card}>
        <CardContent className={classes.content}>
          <PersonAddIcon className={classes.icon} />
          <Typography gutterBottom variant="h3">
            Sign up
          </Typography>
          <Typography variant="subtitle2">
            Sign up on the internal platform
          </Typography>
          <RegisterForm className={classes.registerForm} />
          <Divider className={classes.divider} />
          <Link
            align="center"
            color="secondary"
            component={RouterLink}
            to="/auth/login"
            underline="always"
            variant="subtitle2"
          >
            Have an account?
          </Link>
        </CardContent>
        <CardMedia
          className={classes.media}
          image="/images/auth.png"
          title="Cover"
        >
          <Typography color="inherit" variant="subtitle1">
            Hella narvwhal Cosby sweater McSweeney&apos;s, salvia kitsch before
            they sold out High Life.
          </Typography>
          <div className={classes.person}>
            <Avatar
              alt="Person"
              className={classes.avatar}
              src="/images/avatars/avatar_2.png"
            />
            <div>
              <Typography color="inherit" variant="body1">
                Ekaterina Tankova
              </Typography>
              <Typography color="inherit" variant="body2">
                Manager at inVision
              </Typography>
            </div>
          </div>
        </CardMedia>
      </Card>
    </Page>
  );
}

export default Register;
