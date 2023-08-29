document.addEventListener('DOMContentLoaded', function() {
  //var buttonElement = document.getElementById('button-element');
  var buttonBackgroundTextInput = document.getElementById('names-color-input');
  var buttonBackgroundTextHex = document.getElementById('names-color-hex');

  buttonBackgroundTextInput.addEventListener('input', function() {
    var colorValue = this.value;
    var hexValue = normalizeHexValue(colorValue);
    buttonBackgroundTextInput.value = hexValue;
    buttonBackgroundTextHex.value = hexValue;
    // button['background-color'] = hexValue;
    // buttonElement.style.backgroundColor = hexValue;
    // buttonElement.style.boxShadow = "0 0 5px " + hexValue;
  });

  buttonBackgroundTextHex.addEventListener('input', function() {
    var hexValue = this.value;
    var normalizedHexValue = normalizeHexValue(hexValue);
    buttonBackgroundTextInput.value = normalizedHexValue;
    buttonBackgroundTextHex.value = normalizedHexValue;
    // button['background-color'] = normalizedHexValue;
    // buttonElement.style.backgroundColor = normalizedHexValue;
    // buttonElement.style.boxShadow = "0 0 5px " + normalizedHexValue;
  });
});