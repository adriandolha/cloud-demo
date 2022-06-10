import authHeader from "./auth-header";
const API_URL = "https://localhost";
class WordService {
    get_all(limit, offset) {
        return fetch(`${API_URL}/words?limit=${limit}&offset=${offset}`, {
            method: 'get',
            headers: new Headers({
                'Content-Type': 'application/json',
                ...authHeader()
            })
        })
    }
}

export default new WordService();
