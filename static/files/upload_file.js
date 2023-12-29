function upload_file(element) {
    var file = element.files[0];
    var formData = new FormData();
    formData.append('file', file);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload_file', true);

    xhr.onload = function () {
        if (xhr.status === 200) {
            console.log('Fichier téléchargé avec succès!');
        } else {
            console.error('Échec du téléchargement du fichier.');
        }
    };

    xhr.send(formData);
}

// new audio file -> **uploaded
document.addEventListener('DOMContentLoaded', function() {
    var elements = document.querySelectorAll('.audio-input');
    elements.forEach(function(element) {
        element.addEventListener('change', function() {
            upload_file(element);
        });
    });
});