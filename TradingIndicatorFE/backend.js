const { response } = require("express");
const fetch = require("node-fetch");

const APP_KEY = "7y2Sjx4eq1Z/8DQtZA6LwZkIZ3QHa95380cCUW8VCO90UIi3EvhSTQ==";

async function playerLogin(credentials) {
  return await fetch("https://tradingindicatorapplication.azurewebsites.net/api/login", {
    method: "POST",
    headers: { "x-functions-key": APP_KEY },
    body: JSON.stringify(credentials),
  }).then((response) => response.json());
}

async function playerRegister(credentials) {
  return await fetch("https://tradingindicatorapplication.azurewebsites.net/api/registration", {
    method: "POST",
    headers: { "x-functions-key": APP_KEY },
    body: JSON.stringify(credentials),
  }).then((response) => response.json());
}

async function getPlayerById(id) {
  return await fetch("https://tradingindicatorapplication.azurewebsites.net/api/getUserById", {
    method: "POST",
    headers: { "x-functions-key": APP_KEY },
    body: JSON.stringify(id),
  }).then((response) => response.json());
}

async function getKucoinPositions() {
  return await fetch("https://tradingindicatorapplication.azurewebsites.net/api/getKucoinPositions", {
    method: "GET",
    headers: { "x-functions-key": APP_KEY }
  }).then((response) => response.json());
}


module.exports = { playerLogin, playerRegister, getPlayerById, getKucoinPositions};
