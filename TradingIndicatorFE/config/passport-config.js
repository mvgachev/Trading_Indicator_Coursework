
const LocalStrategy = require('passport-local').Strategy
const fetch = require("node-fetch");
const { response } = require('../app');
const { getPlayerById } = require('../backend');
const backend = require("../backend");

const APP_KEY = "7y2Sjx4eq1Z/8DQtZA6LwZkIZ3QHa95380cCUW8VCO90UIi3EvhSTQ==";


function initialize(passport) {
    const authenticate = async (email, password, done) => {

        var credentials = {
            "email": email,
            "password": password
        }
        var response = await backend.playerLogin(credentials).catch((error) => {console.log(error)})
        
        if (response.success === 'true') {
            console.log(response.msg)
            console.log(response.user)
            return done(null, response.user)
        } else {
            console.log(response.msg)
            return done(null, false, { message: response.msg })
        }
    }

    passport.use(new LocalStrategy({ usernameField: 'email' }, authenticate))
    passport.serializeUser((user, done) => done(null, user.id))
    //Optimize code by storing all users in a global variable here 
    passport.deserializeUser(async (id, done) => {
        jsonId = {
            "userId": id
        }
        var response = await getPlayerById(jsonId).catch((error) => {console.log(error)});
        return done(null, response.user)
    })
}

module.exports = initialize