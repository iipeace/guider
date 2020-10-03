import "react-app-polyfill/ie11";
import "react-app-polyfill/stable";
import React from "react";
import ReactDOM from "react-dom";
import { createBrowserHistory } from "history";
import { Provider as StoreProvider } from "react-redux";
import { Router } from "react-router-dom";
import { PersistGate } from "redux-persist/integration/react";
import { persistStore } from "redux-persist";
import { configureStore } from "./store";
import App from "./App";
import * as serviceWorker from "./serviceWorker";

const history = createBrowserHistory();
export const store = configureStore(history);

ReactDOM.render(
  <StoreProvider store={store}>
    <PersistGate loading={null} persistor={persistStore(store)}>
      <Router history={history}>
        <App />
      </Router>
    </PersistGate>
  </StoreProvider>,

  document.getElementById("root"),
);

serviceWorker.unregister();
