import { combineReducers } from "redux";
import { persistReducer } from "redux-persist";
import storage from "redux-persist/lib/storage";
import sessionStorage from "redux-persist/lib/storage/session";
import sessionReducer from "./sessionReducer";
import settingReducer from "./settingReducer";

const rootPersistConfig = {
  key: "root",
  storage,
  blacklist: ["session", "setting"],
};

const sessionPersistConfig = {
  key: "session",
  storage: sessionStorage,
};

const settingPersistConfig = {
  key: "setting",
  storage: sessionStorage,
};

const rootReducer = combineReducers({
  session: persistReducer(sessionPersistConfig, sessionReducer),
  setting: persistReducer(settingPersistConfig, settingReducer),
});

export default persistReducer(rootPersistConfig, rootReducer);
