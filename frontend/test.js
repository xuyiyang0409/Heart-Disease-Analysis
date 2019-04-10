import API from './api.js';

const api  = new API();

const path = 'attr?name='+ 'cp';
const headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    "Access-Control-Allow-Methods": "DELETE, POST, GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
};
const method = 'GET';

api.makeAPIRequest(path, {
    method, headers
}).then(function (res) {
    console.log(res);
    for (let i = 0; i < res.cp.length; i ++){
        console.log(res.cp[i]);
    }
});