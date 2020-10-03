import Qs from "qs";
import axios from "axios";
import { store } from "src";
import { sessionActions } from "src/actions";

const TIMEOUT_MS = 10000;
let axiosInterceptor = null;

/**
 * 에러 발생 후 각 상태에 대한 처리
 * @param {object} error
 */
const errorHandling = error => {
  const defaultMessage =
    "예상하지 못한 오류가 발생했습니다. 다시 시도해주세요.";

  if (error.response) {
    const { status } = error.response;

    switch (status) {
      case 400:
        error.message =
          "요청으로 전달한 데이터의 형식이 유효하지 않습니다. 다시 시도해주세요.";
        break;
      case 401:
        // redux 로 로그아웃 요청
        store.dispatch({
          type: sessionActions.SESSION_LOGOUT,
        });
        error.message =
          "인증이 유효하지 않거나 만료되었습니다. 다시 로그인해주세요.";
        break;
      case 403:
        error.message = "요청에 대한 권한이 없습니다.";
        break;
      case 404:
        error.message =
          "요청에 대한 응답을 찾을 수 없습니다. 다시 시도해주세요.";
        break;
      default:
        error.message = defaultMessage;
        break;
    }
  } else {
    const { message } = error;
    if (message === "Network Error") {
      error.message = "네트워크에 문제가 있습니다. 연결을 확인해주세요.";
    } else {
      error.message = defaultMessage;
    }
  }

  return error;
};

/**
 * Http 를 통한 데이터 요청 함수
 * @param {string} method
 * @param {string} baseURL
 * @param {string} idToken
 * @param {Object} queryParams
 * @param {Object} body
 * @param {Object} headers
 * @param {boolean} isMultipart
 */
export const request = (
  method,
  baseURL,
  queryParams,
  body,
  headers,
  isMultipart = false,
) => {
  const { session } = store.getState();
  const { idToken } = session;

  const config = {};
  config.timeout = TIMEOUT_MS;
  config.paramsSerializer = params =>
    Qs.stringify(params, { arrayFormat: "brackets" });

  if (idToken) {
    config.headers = {
      Authorization: idToken,
    };
  }

  if (headers) {
    config.headers = {
      ...config.headers,
      ...headers,
    };
  }
  if (isMultipart) {
    config.headers = {
      ...config.headers,
      "content-type": "multipart/form-data",
    };
  }

  if (queryParams) {
    config.params = {
      ...config.params,
      ...queryParams,
    };
  }

  if (axiosInterceptor !== null) {
    // 이미 등록된 Interceptor 가 있다면 제거하고 초기화
    axios.interceptors.response.eject(axiosInterceptor);
    axiosInterceptor = null;
  }

  axiosInterceptor = axios.interceptors.response.use(
    res => {
      return res;
    },
    error => {
      // 에러처리 공용화
      return Promise.reject(errorHandling(error));
    },
  );

  switch (method) {
    case "get":
      return axios.get(baseURL, config);
    case "post":
      return axios.post(baseURL, body, config);
    case "put":
      return axios.put(baseURL, body, config);
    case "delete":
      return axios.delete(baseURL, config);
    default:
      return axios.get(baseURL, config);
  }
};
