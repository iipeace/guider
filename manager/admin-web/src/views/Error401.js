import React, { useContext } from "react";
import { Link as RouterLink } from "react-router-dom";
import { makeStyles } from "@material-ui/core/styles";
import { Typography, Button, Box } from "@material-ui/core";
import routeUrls from "src/constants/routeUrls";
import Page from "src/components/Page";
import { StringsContext } from "src/App";

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

function Error401() {
  const classes = useStyles();

  const strings = useContext(StringsContext);

  return (
    <Page className={classes.root} title={`Error 401 | ${strings.webName}`}>
      <Box mb={6} textAlign="center">
        <img
          alt="Error 401"
          className={classes.image}
          src="/images/errors/error-401.png"
        />
      </Box>
      <Typography align="center" variant="h3" gutterBottom>
        권한을 확인해주세요.
      </Typography>
      <Typography align="center" variant="subtitle2">
        지금 입력하신 주소의 페이지에 접근할 권한이 없습니다. 계정의 권한을
        확인해주세요.
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

export default Error401;
