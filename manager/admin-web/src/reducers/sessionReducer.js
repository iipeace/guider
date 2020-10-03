import { sessionActions } from "src/actions";
import produce from "immer";

const initialState = {
  isLoggedIn: false,
  idToken: null,
  user: {
    email: "",
    role: "", // TODO yeombang87 : 역할 추가 필요 ["GUEST", "USER", "ADMIN"]
  },
};

const sessionReducer = (state = initialState, action) => {
  switch (action.type) {
    case sessionActions.SESSION_LOGIN: {
      return produce(state, draft => {
        draft.isLoggedIn = true;
        draft.idToken = action.idToken;
        draft.user.email = action.user.email;
      });
    }

    case sessionActions.SESSION_LOGOUT: {
      return initialState;
    }

    default: {
      return state;
    }
  }
};

export default sessionReducer;
