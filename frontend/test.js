import API from './api.js';

const api  = new API();

const path = 'predict?type=2';
const headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    "Access-Control-Allow-Methods": "DELETE, POST, GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
};
const method = 'POST';
const payload = {"ca": "1.2",
    "oldpeak": "2.34",
    "thalach": "152",
    "cp": "6.1",
    "exang": "0.23"};

api.makeAPIRequest(path, {
    method, headers,
    body: JSON.stringify(payload)
}).then(function (res) {
    console.log(res);
});