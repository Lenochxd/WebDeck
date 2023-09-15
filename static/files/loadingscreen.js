window.addEventListener("load", function() {
    var loadingScreen = document.getElementById("loading-screen");

    loadingScreen.classList.add("hidden");
    setTimeout(function () {
        loadingScreen.remove();
    }, 500);
});