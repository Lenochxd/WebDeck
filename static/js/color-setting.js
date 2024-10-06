function handleInput(input, output) {
  input.addEventListener('input', function() {
    var colorValue = this.value;
    var hexValue = normalizeHexValue(colorValue);
    input.value = hexValue;
    output.value = hexValue;
  });
}

document.addEventListener('DOMContentLoaded', function() {
  // Input elements for names-color
  var namesColorTextInput = document.getElementById('names-color-input');
  var namesColorTextHex = document.getElementById('names-color-hex');
  handleInput(namesColorTextInput, namesColorTextHex);

  // Input elements for buttons-color
  var buttonsColorTextInput = document.getElementById('buttons-color-input');
  var buttonsColorTextHex = document.getElementById('buttons-color-hex');
  handleInput(buttonsColorTextInput, buttonsColorTextHex);
});
