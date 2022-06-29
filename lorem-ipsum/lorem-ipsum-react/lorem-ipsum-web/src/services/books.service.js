import authHeader from "./auth-header";
const API_URL = "https://localhost";
class BookService {
    add(book_data) {
        return fetch(`${API_URL}/books`, {
            method: 'post',
            headers: new Headers({
                ...authHeader(),
                'Content-Type': 'application/json'
            }),
            body: JSON.stringify([book_data])
        })
    }
    random(noOfPages) {
        return fetch(`${API_URL}/books/random?no_of_pages=${noOfPages}`, {
            method: 'get',
            headers: new Headers({
                'Content-Type': 'application/json',
                ...authHeader()
            })
        })
    }
    get_all(limit, offset, includes) {
        const includes_param = (includes && `&includes=${includes}`) || ''
        return fetch(`${API_URL}/books?limit=${limit}&offset=${offset}${includes_param}`, {
            method: 'get',
            headers: new Headers({
                'Content-Type': 'application/json',
                ...authHeader()
            })
        })
    }
    search(query) {
        return fetch(`${API_URL}/books/search?query=${query}`, {
            method: 'get',
            headers: new Headers({
                'Content-Type': 'application/json',
                ...authHeader()
            })
        })
    }
}

export default new BookService();
