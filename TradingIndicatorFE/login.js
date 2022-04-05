const submitButton = document.querySelector("login-submit-button");


function login(e) {
    console.log("login working");
    console.log(e);
    // try {
    //   backend.playerLogin(credentials, socket);
    // } catch (e) {
    //   socket.emit("login", `Login failed with exception ${e}`);
    // }
}

submitButton.addEventListener("onclick", login);

console.log("hero")