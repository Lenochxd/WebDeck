function handleFolderpathButtonClick(filetypes) {
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
        let filetypes = button.getAttribute('filetypes');
        button.addEventListener('click', () => {
            handleFolderpathButtonClick(filetypes);
        });
    });

    console.log("folderpath.js loaded");
});