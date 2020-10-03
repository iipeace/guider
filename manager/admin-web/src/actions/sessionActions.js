// session 관련 리덕스 액션타입과 액션 생성함수
export const SESSION_LOGIN = "SESSION_LOGIN";
export const SESSION_LOGOUT = "SESSION_LOGOUT";

export const login = (idToken, user) => dispatch =>
  dispatch({
    type: SESSION_LOGIN,
    idToken,
    user,
  });

export const logout = () => dispatch =>
  dispatch({
    type: SESSION_LOGOUT,
  });
