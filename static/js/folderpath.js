function handleFolderpathButtonClick() {
    fetch("/upload_folderpath", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    })
    .then(response => response.text())
    .then(folderPath => {
        console.log('Dir path:', folderPath);
        const folderpathText = document.querySelectorAll('input.folderpath');
        if (folderPath !== "") {
            folderpathText.forEach(textElement => {
                textElement.value = folderPath;
            });
        }
    })
    .catch(error => {
        console.error('Error during request:', error);
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const folderpathButtons = document.querySelectorAll('button.folderpath');

    folderpathButtons.forEach(button => {
        button.addEventListener('click', () => {
            handleFolderpathButtonClick();
        });
    });

    console.log("folderpath.js loaded");
});