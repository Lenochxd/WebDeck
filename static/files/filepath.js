function handleFilepathButtonClick(button) {
    fetch('/upload_filepath', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    })
    .then(response => response.text())
    .then(filePath => {
        console.log('Chemin du fichier:', filePath);
        const filepathText = document.querySelectorAll('input.filepath');
        if (filePath !== "") {
            filepathText.forEach(textElement => {
                textElement.value = filePath
            });
        }
    })
    .catch(error => {
        console.error('Erreur lors de la requête:', error);
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const filepathButtons = document.querySelectorAll('button.filepath');

    filepathButtons.forEach(button => {
        button.addEventListener('click', () => {
            handleFilepathButtonClick(button);
        });
    });

    console.log("filepath.js loaded");
});