import { applyMiddleware, createStore, compose } from "redux";
import thunk from "redux-thunk";
import logger from "redux-logger";
import rootReducer from "src/reducers";
import { isDevelopment } from "../utils/configs";

export default function configureStore(history) {
  let middlewares = [thunk.withExtraArgument({ history })];
  const enhancers = [];

  // 개발 모드에서만 적용
  if (isDevelopment()) {
    const devToolsExtension = window.__REDUX_DEVTOOLS_EXTENSION__;

    if (typeof devToolsExtension === "function") {
      enhancers.push(devToolsExtension());
    }

    middlewares = [...middlewares, logger];
  }

  const composedEnhancers = compose(
    applyMiddleware(...middlewares),
    ...enhancers,
  );

  return createStore(rootReducer, composedEnhancers);
}
