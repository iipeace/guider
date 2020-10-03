import { useEffect, useRef } from "react";

/**
 * 일정 시간 간격으로 작업을 수행하는 hook
 * @param {function} callback
 * @param {number} delay
 */
function useInterval(callback, delay) {
  const savedCallback = useRef();

  // 마지막 callback 기억
  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  // interval 설정
  // eslint-disable-next-line consistent-return
  useEffect(() => {
    function tick() {
      savedCallback.current();
    }
    if (delay !== null) {
      const id = setInterval(tick, delay);
      return () => clearInterval(id);
    }
  }, [delay]);
}

export default useInterval;
