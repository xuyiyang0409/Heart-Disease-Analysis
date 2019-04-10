// change this when you integrate with the real API, or when u start using the dev server
const API_URL = 'http://127.0.0.1:8888';

const getJSON = (path, options) => 
    fetch(path, options)
        .then(res => res.json())
        .catch(err => console.warn(`API_ERROR: ${err.message}`));


export default class API {
    constructor(url = API_URL) {
        this.url = url;
    } 

    makeAPIRequest(path, options) {
        return getJSON(`${this.url}/${path}`, options);
    }
}
