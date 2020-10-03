// setting 관련 리덕스 액션타입과 액션 생성함수
export const SETTING_CHANGE_LANGUAGE = "SETTING_CHANGE_LANGUAGE";

export const changeLanguage = language => dispatch =>
  dispatch({
    type: SETTING_CHANGE_LANGUAGE,
    language,
  });
