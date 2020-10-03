import React, { useContext } from "react";
import { Link as RouterLink } from "react-router-dom";
import { makeStyles } from "@material-ui/core/styles";
import { Typography, Button, Box } from "@material-ui/core";
import routeUrls from "src/constants/routeUrls";
import Page from "src/components/Page";
import { StringsContext } from "src/App";
import { getErrorImageFileName } from "src/utils/configs";
import appConfig from "src/configs/appConfig";

const useStyles = makeStyles(theme => ({
  root: {
    display: "flex",
    flexDirection: "column",
    alignContent: "center",
    padding: theme.spacing(3),
    paddingTop: "10vh",
  },
  image: {
    width: 200,
    height: "auto",
  },
}));

function Error500() {
  const classes = useStyles();

  const strings = useContext(StringsContext);

  return (
    <Page className={classes.root} title={`Error 500 | ${strings.webName}`}>
      <Box mb={6} textAlign="center">
        <img
          alt="Error 500"
          className={classes.image}
          src="/images/errors/error-500.png"
        />
      </Box>
      <Typography align="center" variant="h3" gutterBottom>
        잠시 후 다시 확인해주세요.
      </Typography>
      <Typography align="center" variant="subtitle2">
        지금 이 서비스와 연결할 수 없습니다. 문제를 해결하기 위해 열심히
        노력하고 있습니다. 잠시 후 다시 확인해주세요.
      </Typography>
      <Box mt={6} textAlign="center">
        <Button
          color="primary"
          component={RouterLink}
          to={routeUrls.ROOT}
          variant="contained"
        >
          홈으로 돌아가기
        </Button>
      </Box>
    </Page>
  );
}

export default Error500;
