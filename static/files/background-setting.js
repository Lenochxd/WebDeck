document.addEventListener('DOMContentLoaded', function() {
    function toggleDisplay() {
        var chooseBackgroundElement = document.getElementById("choose-background");
        var configContainer = document.getElementById("config-container");
    
        if (chooseBackgroundElement.style.display === "none") {
            chooseBackgroundElement.style.display = "block";
            configContainer.style.display = "none";
        } else {
            chooseBackgroundElement.style.display = "none";
            configContainer.style.display = "block";
        }
    }
    document.getElementById("setting-background").addEventListener("click", toggleDisplay);
    document.getElementById("setting-background-back").addEventListener("click", toggleDisplay);



    var pageloadElements = document.querySelectorAll(".choose-bg-element-pageload");
        
    pageloadElements.forEach(function(element) {
        var computedStyle = getComputedStyle(element);
        var backgroundColor = computedStyle.backgroundColor;
        
        var brightness = calculateBrightness(backgroundColor);
        if (brightness > 125) {
            element.style.color = "black";
            element.classList.add("white-text");
        } else {
            element.style.color = "white";
        }
    });

    var buttonBackgroundColorInput = document.getElementById('background-color-input');
    var buttonBackgroundColorHex = document.getElementById('background-color-hex');

    buttonBackgroundColorInput.addEventListener('input', function() {
        var colorValue = this.value;
        var hexValue = normalizeHexValue(colorValue);
        buttonBackgroundColorInput.value = hexValue;
        buttonBackgroundColorHex.value = hexValue;
    });

    buttonBackgroundColorHex.addEventListener('input', function() {
        var hexValue = this.value;
        var normalizedHexValue = normalizeHexValue(hexValue);
        buttonBackgroundColorInput.value = normalizedHexValue;
        buttonBackgroundColorHex.value = normalizedHexValue;
    });

    var chooseBackground = document.getElementById("choose-background-handler");
    var backgroundsArrayString = chooseBackground.value;
    backgroundsArrayString = backgroundsArrayString.replace(/'/g, '"');
    var backgrounds_array = JSON.parse(backgroundsArrayString);

    document.getElementById("create-color-bg").addEventListener("click", function() {
        var colorHex = document.getElementById("background-color-hex").value;
        if (colorHex !== "") {
        
            var divElement = document.createElement("div");
            divElement.classList.add("choose-bg-element");
            divElement.classList.add("choose-bg-element-color");
            divElement.style.backgroundColor = colorHex;
            var createColorBgElement = document.getElementById("create-color-bg");
            if (createColorBgElement.classList.contains("black-theme")) {
                divElement.classList.add("black-theme");
            }
            
            var brightness = calculateBrightness(colorHex);
            if (brightness > 125) {
                divElement.style.color = "#141414";
            } else {
                divElement.style.color = "#fbfbfd";
            }
            
            backgrounds_array.push(colorHex);
            
            
            var container = document.getElementById('choose-backgrounds-container');
            var divs = container.getElementsByTagName('div');
            var background_color_text = divs[0].getAttribute("background_color_text");
            
            divElement.textContent = background_color_text + " : " + colorHex;
            divElement.setAttribute("background", colorHex);
            
            var chooseBackgroundsContainer = document.getElementById("choose-backgrounds-container");
            chooseBackgroundsContainer.appendChild(divElement);
            
            updateBackgroundsInputValue(backgrounds_array);
            
            
            var chooseBgButtonsDiv = document.querySelector(".choose-bg-buttons");
            var clonedChooseBgButtons = chooseBgButtonsDiv.cloneNode(true);
            divElement.appendChild(clonedChooseBgButtons);
            var activateButton = clonedChooseBgButtons.querySelector(".choose-bg-activate-button");
            activateButton.classList.add("choose-bg-activate-button-checked");
            

            var activateButtons = document.querySelectorAll(".choose-bg-activate-button");
            
            activateButtons.forEach(function(activateButton) {
                // Vérifier si un event listener "click" existe déjà
                var clickListenerExists = false;
                var clickListeners = getEventListeners(activateButton);
                if (clickListeners && clickListeners.click) {
                    for (var i = 0; i < clickListeners.click.length; i++) {
                        if (clickListeners.click[i].listener.toString() === activateButtonEvent.toString()) {
                            clickListenerExists = true;
                            break;
                        }
                    }
                }
            
                if (!clickListenerExists) {
                    activateButton.addEventListener("click", activateButtonEvent);
                }
            });
            
            var deleteButtons = document.querySelectorAll(".choose-bg-delete-button");
    
            deleteButtons.forEach(function(deleteButton) {
                // Vérifier si un event listener "click" existe déjà
                var clickListenerExists = false;
                var clickListeners = getEventListeners(deleteButton);
                if (clickListeners && clickListeners.click) {
                    for (var i = 0; i < clickListeners.click.length; i++) {
                        if (clickListeners.click[i].listener.toString() === deleteButton.toString()) {
                            clickListenerExists = true;
                            break;
                        }
                    }
                }

                if (!clickListenerExists) {
                    deleteButton.addEventListener("click", deleteButtonEvent);
                }
            });
            
            console.log(backgrounds_array.length + backgrounds_array);
        }
    });

    document.getElementById("create-image-bg").addEventListener("change", function() {
        var input = this;
        
        if (input.files && input.files[0]) {
            
            var file = input.files[0];
            var formData = new FormData();
            formData.append('file', file);
            formData.append('info', 'background_image');
            
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/upload_file', true);
            xhr.onload = function () {
                if (xhr.status === 200) {
                    console.log('Fichier téléchargé avec succès!');
                    var fileName = "**uploaded/" + input.files[0].name;
                    console.log('Image envoyée avec succès ! Nom du fichier :', fileName);
                    // Faire quelque chose avec le nom du fichier
                    // button.image = "**uploaded/" + fileName;

                    var imageFile = 'static/files/uploaded/' + input.files[0].name;

                    var divElement = document.createElement("div");
                    divElement.classList.add("choose-bg-element");
                    divElement.classList.add("choose-bg-element-image");
                    var createColorBgElement = document.getElementById("create-color-bg");
                    if (createColorBgElement.classList.contains("black-theme")) {
                        divElement.classList.add("black-theme");
                    }
                    
                    // Créer un pseudo-élément ::before pour contenir l'image de fond
                    var pseudoElement = document.createElement("div");
                    pseudoElement.classList.add("choose-bg-pseudo-element");
                    pseudoElement.style.backgroundImage = 'url("' + imageFile + '")';
                    divElement.appendChild(pseudoElement);
                    
                    
                    backgrounds_array.push(fileName);
                    //divElement.textContent = "Background image: " + input.files[0].name;
                    divElement.setAttribute("background", fileName);
                    
                    var chooseBackgroundsContainer = document.getElementById("choose-backgrounds-container");
                    chooseBackgroundsContainer.appendChild(divElement);
                    

                    var imgElement = document.createElement("img");
                    
                    imgElement.setAttribute("src", imageFile);
                    divElement.appendChild(imgElement);
                    

                    var chooseBgButtonsDiv = document.querySelector(".choose-bg-buttons");
                    var clonedChooseBgButtons = chooseBgButtonsDiv.cloneNode(true);
                    divElement.appendChild(clonedChooseBgButtons);
                    var activateButton = clonedChooseBgButtons.querySelector(".choose-bg-activate-button");
                    activateButton.classList.add("choose-bg-activate-button-checked");
                    
                    
                    var activateButtons = document.querySelectorAll(".choose-bg-activate-button");

                    activateButtons.forEach(function(activateButton) {
                        // Vérifier si un event listener "click" existe déjà
                        var clickListenerExists = false;
                        var clickListeners = getEventListeners(activateButton);
                        if (clickListeners && clickListeners.click) {
                            for (var i = 0; i < clickListeners.click.length; i++) {
                                if (clickListeners.click[i].listener.toString() === activateButtonEvent.toString()) {
                                    clickListenerExists = true;
                                    break;
                                }
                            }
                        }

                        if (!clickListenerExists) {
                            activateButton.addEventListener("click", activateButtonEvent);
                        }
                    });
                    
                    var deleteButtons = document.querySelectorAll(".choose-bg-delete-button");
    
                    deleteButtons.forEach(function(deleteButton) {
                        // Vérifier si un event listener "click" existe déjà
                        var clickListenerExists = false;
                        var clickListeners = getEventListeners(deleteButton);
                        if (clickListeners && clickListeners.click) {
                            for (var i = 0; i < clickListeners.click.length; i++) {
                                if (clickListeners.click[i].listener.toString() === deleteButton.toString()) {
                                    clickListenerExists = true;
                                    break;
                                }
                                }
                            }

                            if (!clickListenerExists) {
                                deleteButton.addEventListener("click", deleteButtonEvent);
                            }
                        });
                        removeBackgroundFromArray()
                } else {
                    console.error('Échec du téléchargement du fichier.');
                }
            }
            xhr.send(formData);
        }
    });

    var deleteButtons = document.querySelectorAll(".choose-bg-delete-button");
    
    deleteButtons.forEach(function(deleteButton) {
        // Vérifier si un event listener "click" existe déjà
        var clickListenerExists = false;
        var clickListeners = getEventListeners(deleteButton);
        if (clickListeners && clickListeners.click) {
            for (var i = 0; i < clickListeners.click.length; i++) {
                if (clickListeners.click[i].listener.toString() === deleteButton.toString()) {
                    clickListenerExists = true;
                    break;
                }
            }
        }

        if (!clickListenerExists) {
            deleteButton.addEventListener("click", deleteButtonEvent);
        }
    });
    
    var activateButtons = document.querySelectorAll(".choose-bg-activate-button");

    activateButtons.forEach(function(activateButton) {
        // Vérifier si un event listener "click" existe déjà
        var clickListenerExists = false;
        var clickListeners = getEventListeners(activateButton);
        if (clickListeners && clickListeners.click) {
            for (var i = 0; i < clickListeners.click.length; i++) {
                if (clickListeners.click[i].listener.toString() === activateButtonEvent.toString()) {
                    clickListenerExists = true;
                    break;
                }
            }
        }

        if (!clickListenerExists) {
            activateButton.addEventListener("click", activateButtonEvent);
        }
    });
});

function deleteButtonEvent(event) {
    backgrounds_array = removeBackgroundFromArray();
    if (backgrounds_array.length !== 1) {
        var divElement = event.target.closest(".choose-bg-element");
        var backgroundAttribute = divElement.getAttribute("background");
        var filteredBackgrounds = backgrounds_array.filter(item => !item.startsWith("//"))
        console.log(filteredBackgrounds.length);
        if (divElement && (!backgroundAttribute.startsWith("//") && filteredBackgrounds.length !== 1)) {
            divElement.remove();
            backgrounds_array = removeBackgroundFromArray();
        }
    }
}
function activateButtonEvent(event) {
    backgrounds_array = removeBackgroundFromArray();
    var divElement = event.target.closest(".choose-bg-element");
    if (divElement && backgrounds_array.length !== 1) {
        var backgroundAttribute = divElement.getAttribute("background");
        var activateButton = divElement.querySelector("div.choose-bg-buttons").querySelector(".choose-bg-activate-button");
        var filteredBackgrounds = backgrounds_array.filter(item => !item.startsWith("//"))
        if (backgroundAttribute.startsWith("//")) {
            if (filteredBackgrounds.length > 0) {
                divElement.setAttribute("background", backgroundAttribute.replace('//', ''));
                activateButton.classList.add("choose-bg-activate-button-checked");
                backgrounds_array = removeBackgroundFromArray();
            }
        }
        else if (filteredBackgrounds.length !==1) {
            divElement.setAttribute("background", "//" + backgroundAttribute);
            activateButton.classList.remove("choose-bg-activate-button-checked");
            backgrounds_array = removeBackgroundFromArray();
        }
    }
}

function getEventListeners(element) {
    return element.__events || (element.__events = {});
}

function updateBackgroundsInputValue(backgrounds_array) {
    var modifiedArray = backgrounds_array.toString().replace(/,/g, "','");
    document.getElementById("choose-background-handler").setAttribute("value", `['${modifiedArray}']`);
}

function removeBackgroundFromArray() {
    var container = document.getElementById('choose-backgrounds-container');
    var divs = container.getElementsByTagName('div');
    var backgrounds_array = [];

    for (var i = 0; i < divs.length; i++) {
        var background = divs[i].getAttribute("background");
        
        if (background) {
            backgrounds_array.push(background);
        }
    }
    console.log(backgrounds_array);
    updateBackgroundsInputValue(backgrounds_array);
    return backgrounds_array;
}

function calculateBrightness(hexColor) {
    // hex to RGB
    var r = parseInt(hexColor.substr(1, 2), 16);
    var g = parseInt(hexColor.substr(3, 2), 16);
    var b = parseInt(hexColor.substr(5, 2), 16);
    
    // Calculer la luminosité
    return (r * 299 + g * 587 + b * 114) / 1000;
}

console.log("background-setting.js loaded");