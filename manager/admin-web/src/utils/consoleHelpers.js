import { isDevelopment } from "src/utils/configs";

/**
 * development 에서만 console.log 이 동작하는 헬퍼
 * @param  {any} messages
 */
export const consoleLogHelper = messages => {
  if (isDevelopment()) {
    console.log(messages);
  }
};

/**
 * development 에서만 console.wran 이 동작하는 헬퍼
 * @param  {any} messages
 */
export const consoleWarnHelper = messages => {
  if (isDevelopment()) {
    console.warn(messages);
  }
};

/**
 * development 에서만 console.info 이 동작하는 헬퍼
 * @param  {any} messages
 */
export const consoleInfoHelper = messages => {
  if (isDevelopment()) {
    console.info(messages);
  }
};

/**
 * development 에서만 console.error 이 동작하는 헬퍼
 * @param  {any} messages
 */
export const consoleErrorHelper = messages => {
  if (isDevelopment()) {
    console.error(messages);
  }
};
