import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Page from "src/components/Page";
import { Container } from "@material-ui/core";

const useStyles = makeStyles(() => ({
  root: {},
}));

function Home() {
  const classes = useStyles();

  return (
    <Page className={classes.root} title="Home">
      <Container maxWidth={false}>Home</Container>
    </Page>
  );
}

export default Home;
