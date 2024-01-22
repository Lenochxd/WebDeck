window.addEventListener("load", function() {
    var loadingScreen = document.getElementById("loading-screen");
    var serverDisconnected = document.getElementById("server-disconnected");

    loadingScreen.classList.add("hidden");
    setTimeout(function () {
        serverDisconnected.classList.remove("invisible");
        loadingScreen.classList.add("transparent");
        loadingScreen.style.pointerEvents = "none";
    }, 5000);
});