// inMemoryJwt.js
export const inMemoryJWTManager = () => {
    let inMemoryJWT = null;

    const getToken = () => inMemoryJWT;

    const setToken = (token) => {
        inMemoryJWT = token;
        return true;
    };

    const eraseToken = () => {
        inMemoryJWT = null;
        return true;
    }

    return {
        eraseToken,
        getToken,
        setToken,
    }
};

export const getToken = async () => {
    let token = inMemoryJWTManager().getToken();
    if (! token) {
        return await fetch("/api/authenticate")
            .then(res => res.json())
            .then((res) => {
                if (res.Token != undefined) {
                    inMemoryJWTManager().setToken(res.Token);
                    return res.Token;
                } else {
                    return null;
                }
            })
    }
    return token;
}
