import { settingActions } from "src/actions";
import produce from "immer";

const initialState = {
  language: "ko",
};

const settingReducer = (state = initialState, action) => {
  switch (action.type) {
    case settingActions.SETTING_CHANGE_LANGUAGE: {
      return produce(state, draft => {
        draft.language = action.language;
      });
    }

    default: {
      return state;
    }
  }
};

export default settingReducer;
