/**
 * 개발 모드인지, 아닌지 확인 (true 면 개발모드, false 면 프로덕션 모드)
 */
export const isDevelopment = () => {
  if (process.env.NODE_ENV === "development") {
    return true;
  }

  return false;
};
