export function getCookie(name) {
    const match = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
    return match ? match[2] : null;
};

export function setCookie(name, value, days = 1, domain = '/') {
    const date = new Date();
    date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);

    document.cookie = `${name}=${value};path=${domain};expires=${date.toGMTString()}`;
};

export function removeCookie(name) {
    setCookie(name, null, -1);
};
