/**
 * 로컬 스토리지에 JSON 형태로 저장 / 불러오기 / 삭제 헬퍼
 */
export const localStorageHelper = {
  set: (key, object) => {
    if (!localStorage) return;
    localStorage[key] =
      typeof object === "string" ? object : JSON.stringify(object);
  },
  get: key => {
    if (!localStorage) return null;

    if (!localStorage[key]) {
      return null;
    }

    try {
      const parsed = JSON.parse(localStorage[key]);
      return parsed;
    } catch (e) {
      return localStorage[key];
    }
  },
  remove: key => {
    if (!localStorage) return;

    if (localStorage[key]) {
      localStorage.removeItem(key);
    }
  },
};

/**
 * 로컬 스토리지에 JSON 형태로 저장 / 불러오기 / 삭제 헬퍼
 */
export const sessionStorageHelper = {
  set: (key, object) => {
    if (!sessionStorage) return;
    sessionStorage[key] =
      typeof object === "string" ? object : JSON.stringify(object);
  },
  get: key => {
    if (!sessionStorage) return null;

    if (!sessionStorage[key]) {
      return null;
    }

    try {
      const parsed = JSON.parse(sessionStorage[key]);
      return parsed;
    } catch (e) {
      return sessionStorage[key];
    }
  },
  remove: key => {
    if (!sessionStorage) return;

    if (sessionStorage[key]) {
      sessionStorage.removeItem(key);
    }
  },
};
