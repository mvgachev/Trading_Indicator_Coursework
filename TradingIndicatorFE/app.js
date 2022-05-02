// Copyright 2017 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

'use strict';

//Load environment variables
if (process.env.NODE_ENV !== 'production') {
  require('dotenv').config()
}



//Add constants
const express = require('express');
const app = express();
const flash = require('express-flash')
const session = require('express-session')
const passport = require('passport')
const configPassport = require('./config/passport-config.js')
const backend = require("./backend");




//Initialize passport
configPassport(
   passport
)

//Example database with users
const users = []


//Setup static page handling
app.set("view engine", "ejs");
app.use("/static", express.static("public"));


//Set up body parser
// const bodyParser = require("body-parser");
app.use(express.urlencoded({ extended: false }));


//Set up session key
app.use(flash())
app.use(session({
  secret: "1234",
  resave: false,
  saveUninitialized: false
}))
app.use(passport.initialize())
app.use(passport.session())




// View route for home page
app.get('/',  (req, res) => {
  console.log(req.user)
  console.log(req.isAuthenticated)
  if (req.isAuthenticated()) {
    res.render('home', { username: req.user.discord_username ,
      authenticated: true
    })
  } else {
    res.render('home', {
      authenticated: false
    })
  }
})

//Handle login interface on /login
app.get("/login", (req, res) => {
  res.render("login");
});

//Handle login interface on /login
app.get("/signup", (req, res) => {
  res.render("signup");
});

//Handle discord interface
app.get("/discord", authenticate, (req, res) => {
  res.render("discord", {authenticated: true});
});

app.get("/positions", authenticate, async (req, res) => {
  try{
    var pos = await backend.getKucoinPositions().catch((error) => {console.log(error)});
    res.render('positions', {positions: pos, authenticated: true});
  }
  catch (error){
    console.log(error)
  }

});

//Signup 
app.post('/signup', async (req, res) => {
  try {
    var credentials = {
      "email": req.body.email,
      "password": req.body.password,
      "discordUsername": req.body.discord_username
    }
    console.log(credentials)
    var response = await backend.playerRegister(credentials).catch((error) => {console.log(error)});
    console.log(response)
    console.log(`User with email: ${req.body.email} and password ${req.body.password}`);
    if (response.success === 'true') {
      res.redirect('/login')
    } else {
      console.log("Registration unsuccessful")
      res.render('signup', {msg: response.msg})
    }
  } catch {
    res.redirect('/signup')
  }
})

//Login
app.post('/login', passport.authenticate('local', {
  successRedirect: '/',
  failureRedirect: '/login',
  failureFlash: true
}))


//Logout
app.post('/logout', (req, res) => {
  req.logout()
  res.redirect('/')
})


//Authentication check
function authenticate(req, res, next) {
  if (req.isAuthenticated()) {
    console.log('User is authenticated.')

      return next()
  }
  console.log('User is not authenticated.')
  res.redirect('/login')
}


// Start the server
const PORT = parseInt(process.env.PORT) || 8080;
app.listen(PORT, () => {
  console.log(`App listening on port ${PORT}`);
  console.log('Press Ctrl+C to quit.');
});

module.exports = app;
