document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('button.button');

    buttons.forEach(button => {
        const buttonData = {
            clickInterval: null,
            isMouseDown: false,
            buttonID: button.getAttribute('edit_modal_ID')
        };

        button.addEventListener('mousedown', function(event) {
            event.preventDefault();
            buttonData.isMouseDown = true;
            simulateButtonClick(buttonData);

            setTimeout(function() {
                console.log("1 second passed");
                if (buttonData.isMouseDown) {
                    initiateClickInterval(buttonData);
                }
            }, 1000);
        });

        button.addEventListener('mouseup', function(event) {
            event.preventDefault();
            stopButtonClick(buttonData);
        });

        button.addEventListener('mouseout', function(event) {
            event.preventDefault();
            stopButtonClick(buttonData);
        });

        button.addEventListener('touchstart', function(event) {
            event.preventDefault();
            buttonData.isMouseDown = true;
            simulateButtonClick(buttonData);

            setTimeout(function() {
                console.log("1 second passed");
                if (buttonData.isMouseDown) {
                    initiateClickInterval(buttonData);
                }
            }, 1000);
        });

        button.addEventListener('touchend', function(event) {
            event.preventDefault();
            stopButtonClick(buttonData);
        });

        button.addEventListener('mouseleave', function(event) {
            event.preventDefault();
            stopButtonClick(buttonData);
        });
    });

    document.addEventListener('mouseup', function() {
        buttons.forEach(button => {
            const buttonData = {
                clickInterval: null,
                isMouseDown: false,
                buttonID: button.getAttribute('edit_modal_ID')
            };
            stopButtonClick(buttonData);
        });
    });
});

function stopButtonClick(buttonData) {
    console.log('stopButtonClick');
    buttonData.isMouseDown = false;
    clearInterval(buttonData.clickInterval);
}

function initiateClickInterval(buttonData) {
    buttonData.clickInterval = setInterval(function() {
        if (buttonData.isMouseDown) {
            simulateButtonClick(buttonData);
        } else {
            clearInterval(buttonData.clickInterval);
        }
    }, 100); // Répéter toutes les 100 ms
}

function simulateButtonClick(buttonData) {
    document.getElementById(`button_${buttonData.buttonID}`).click();
    console.log('clicked!');
    console.log(`#button_${buttonData.buttonID}`);
}

console.log('buttonclick.js loaded');
