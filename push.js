const map = require("bluebird").map;
const axios = require("axios");
const fs = require("fs");

const files = fs.readdirSync("./jsons/");
const jsons = files
    .map(file => require(`./jsons/${file}`));

map(jsons, json => {
    console.log();
    return axios.post(process.env.API_URL, json)
        .then(res => {
            console.log(`OK ${json.sensorId}`);
        })
        .catch(err => {
            console.log(`FAIL ${json.sensorId}`);
        });
}, {concurrency: 10});
