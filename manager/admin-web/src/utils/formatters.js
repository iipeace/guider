/**
 * 숫자를 휴대폰 번호 형식으로 변환 (비밀모드에서는 중간 4자리 *로 표시)
 * @param {string} strNum
 * @param {boolean} isSecret
 */
export const phoneFormat = (strNum, isSecret = false) => {
  // 11자리 휴대폰번호
  if (strNum.length === 11) {
    if (isSecret) {
      return strNum.replace(/(\d{3})(\d{4})(\d{4})/, "$1-****-$3");
    }
    return strNum.replace(/(\d{3})(\d{4})(\d{4})/, "$1-$2-$3");
  }

  // 8자리 업체 번호
  if (strNum.length === 8) {
    if (isSecret) {
      return strNum.replace(/(\d{4})(\d{4})/, "$1-****");
    }
    return strNum.replace(/(\d{4})(\d{4})/, "$1-$2");
  }

  // 02-XXXX-XXXX : 10자리 서울 전화번호
  if (strNum.indexOf("02") === 0) {
    if (isSecret) {
      return strNum.replace(/(\d{2})(\d{4})(\d{4})/, "$1-****-$3");
    }
    return strNum.replace(/(\d{2})(\d{4})(\d{4})/, "$1-$2-$3");
  }

  // 031-XXX-XXXX :  10자리 서울 외 전화번호
  if (isSecret) {
    return strNum.replace(/(\d{3})(\d{3})(\d{4})/, "$1-***-$3");
  }
  return strNum.replace(/(\d{3})(\d{3})(\d{4})/, "$1-$2-$3");
};

/**
 * 숫자 세자리 마다 콤마를 넣는 형식으로 변환
 * @param {number} num
 * @param {string} local
 */
export const commaNumFormat = (num, local = "ko") => {
  return Number(num).toLocaleString(local);
};
