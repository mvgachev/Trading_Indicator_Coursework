var socket = null;

var app = new Vue({
  el: "#page",
  data: {
    connected: false,
    loggedIn: false,
    username: "",
    password: "",
  },
  mounter: function () {
    connect();
  },
  methods: {
    login() {
      var credentials = { username: this.username, password: this.password };
      socket.emit("login", credentials);
    },
    persist() {
        localStorage.loggedIn = this.loggedIn;
        localStorage.username = this.username;
        localStorage.password = this.password;
    },
    handleLoggedIn() {
        this.loggedIn = true;
        this.persist();
    }
  },
});

function connect() {
  socket = io();

  //Connect
  socket.on("connect", function () {
    //Set connected state to true
    app.connected = true;
  });

  //Handle login attempt
  socket.on("login", function (response) {
    if (response.result == true) {
      window.location.replace("/")
      app.handleLoggedIn();
    } else {
      alert(response.msg);
    }
  });
}
