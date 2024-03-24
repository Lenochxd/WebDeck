function handleFilepathButtonClick(filetypes) {
    let filetypesString = ""
    if (filetypes != null && filetypes.length > 0) {
        filetypesString = `?filetypes=${filetypes}`
    }
    fetch(`/upload_filepath${filetypesString}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    })
    .then(response => response.text())
    .then(filePath => {
        console.log('File path:', filePath);
        const filepathText = document.querySelectorAll('input.filepath');
        if (filePath !== "") {
            filepathText.forEach(textElement => {
                textElement.value = filePath
            });
        }
    })
    .catch(error => {
        console.error('Error during request:', error);
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const filepathButtons = document.querySelectorAll('button.filepath');

    filepathButtons.forEach(button => {
        let filetypes = button.getAttribute('filetypes');
        button.addEventListener('click', () => {
            handleFilepathButtonClick(filetypes);
        });
    });

    console.log("filepath.js loaded");
});