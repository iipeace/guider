import "moment/locale/ko";
import React, { createContext } from "react";
import { renderRoutes } from "react-router-config";
import moment from "moment";
import MomentAdapter from "@material-ui/pickers/adapter/moment";
import { LocalizationProvider } from "@material-ui/pickers";
import strings from "src/localization/strings";
import { useSelector } from "react-redux";
import { koKR } from "@material-ui/core/locale";
import { createMuiTheme, ThemeProvider } from "@material-ui/core/styles";
import { SnackbarProvider } from "notistack";
import { Helmet } from "react-helmet";
import theme from "./theme";
import "react-perfect-scrollbar/dist/css/styles.css";
import routes from "./routes";
import ScrollReset from "./components/ScrollReset";
import "./assets/scss/main.scss";

/**
 * 언어에 따른 Material-UI 의 theme locale 반환
 * @param {string} language
 */
const getThemeLocale = language => {
  const themeLocales = {
    ko: koKR,
  };

  return themeLocales[language];
};

// 다국어 스트링을 지원하기 위해 Context 에 추가
export const StringsContext = createContext(strings);

function App() {
  // redux 에 저장되어 있는 언어 상태 반환
  const { language } = useSelector(state => state.setting);

  // moment 의 locale 변경
  moment.locale(language);

  // material ui 의 theme 에서 locale 변경
  const themeLocale = getThemeLocale(language);
  const muiTheme = createMuiTheme(theme, themeLocale);

  // 언어 설정 변경에 따른 다국어 스트링 변경
  strings.setLanguage(language);

  return (
    <ThemeProvider theme={muiTheme}>
      <LocalizationProvider
        dateLibInstance={moment}
        dateAdapter={MomentAdapter}
        locale={language}
      >
        <StringsContext.Provider value={strings}>
          <SnackbarProvider
            maxSnack={3}
            anchorOrigin={{
              vertical: "top",
              horizontal: "center",
            }}
          >
            <ScrollReset />
            <Helmet>
              <title>{strings.webName}</title>
            </Helmet>
            {renderRoutes(routes)}
          </SnackbarProvider>
        </StringsContext.Provider>
      </LocalizationProvider>
    </ThemeProvider>
  );
}

export default App;
