function toggleDisplay() {
  var chooseBackgroundElement = document.getElementById("choose-themes");
  var configContainer = document.getElementById("config-container");

  if (chooseBackgroundElement.style.display === "none") {
    chooseBackgroundElement.style.display = "block";
    configContainer.style.display = "none";
  } else {
    chooseBackgroundElement.style.display = "none";
    configContainer.style.display = "block";
  }
}

function getThemesArray() {
  let themesArray = document.getElementById("choose-themes-handler");
  const themesArrayString = themesArray.value.replace(/'/g, '"');
  themesArray = JSON.parse(themesArrayString);
  return themesArray
}

function updateThemesInputValue(themesArray) {
  var modifiedArray = themesArray.toString().replace(/,/g, "','");
  document.getElementById("choose-themes-handler").setAttribute("value", `['${modifiedArray}']`);
}

function swapElements(list, firstElement, secondElement) {
  let firstIndex = list.indexOf(firstElement);
  let secondIndex = list.indexOf(secondElement);

  // Check if both elements exist in the list
  if (firstIndex !== -1 && secondIndex !== -1) {
      // Swap the elements using a temporary variable
      let temp = list[firstIndex];
      list[firstIndex] = list[secondIndex];
      list[secondIndex] = temp;
      return list; // Return the modified list
  } else {
      console.log("One or both elements are not found in the list.");
      return null; // Return null if elements are not found
  }
}

// Function to swap two elements in the DOM
function swapDomElements(element1, element2) {
  const parent = element1.parentNode;
  const index1 = Array.prototype.indexOf.call(parent.children, element1);
  const index2 = Array.prototype.indexOf.call(parent.children, element2);
  parent.insertBefore(element1, parent.children[index2]);
  parent.insertBefore(element2, parent.children[index1]);

  var themesArray = getThemesArray(themesArray);
  swapElements(
    themesArray,
    element1.getAttribute('filename'),
    element2.getAttribute('filename')
  );
  updateThemesInputValue(themesArray);
}

// Function to handle click on arrows
function handleArrowClick(event) {
  const themeContainer = this.closest('.theme-container');
  const parentContainer = themeContainer.parentNode;

  if (event.target.classList.contains('arrow-up-hitbox')) {
    const prevSibling = themeContainer.previousElementSibling;
    if (prevSibling !== null && !prevSibling.hasAttribute('defaulttheme')) {
      swapDomElements(themeContainer, prevSibling);
    }
  } else if (event.target.classList.contains('arrow-down-hitbox')) {
    const nextSibling = themeContainer.nextElementSibling;
    if (nextSibling !== null && !nextSibling.hasAttribute('defaulttheme')) {
      swapDomElements(nextSibling, themeContainer);
    }
  }

  // Disable or enable arrows based on position and defaulttheme attribute
  const firstTheme = parentContainer.firstElementChild;
  const lastTheme = parentContainer.lastElementChild;
  const arrows = themeContainer.querySelectorAll('.arrow-up-hitbox, .arrow-down-hitbox');
  arrows.forEach(arrow => {
    if ((themeContainer === firstTheme || firstTheme.hasAttribute('defaulttheme')) && arrow.classList.contains('arrow-up-hitbox')) {
      arrow.classList.add('disabled');
    } else {
      arrow.classList.remove('disabled');
    }
    if ((themeContainer === lastTheme || lastTheme.hasAttribute('defaulttheme')) && arrow.classList.contains('arrow-down-hitbox')) {
      arrow.classList.add('disabled');
    } else {
      arrow.classList.remove('disabled');
    }
  });
}


document.addEventListener('DOMContentLoaded', function () {
  document.getElementById("setting-themes").addEventListener("click", toggleDisplay);
  document.getElementById("setting-themes-back").addEventListener("click", toggleDisplay);

  const containers = document.querySelectorAll('.theme-container');

  containers.forEach(container => {
    var moveArrow = container.querySelector('.disable-theme');
    var upDownArrows = container.querySelector('.arrows-container');
    if (moveArrow === null) {
      var moveArrow = container.querySelector('.enable-theme');
    }

    if (moveArrow !== null) {
      container.addEventListener('mouseenter', function () {
        moveArrow.classList.remove('invisible');
      });

      container.addEventListener('mouseleave', function () {
        moveArrow.classList.add('invisible');
      });
    }

    if (upDownArrows !== null) {
      container.addEventListener('mouseenter', function () {
        let parentDiv = document.getElementById('disabled-themes');
        let isChild = parentDiv.contains(upDownArrows);
        if (!isChild) {
          upDownArrows.classList.remove('invisible');
        }
      });

      container.addEventListener('mouseleave', function () {
          upDownArrows.classList.add('invisible');
      });
    }
  });

  // Add click event listeners to elements with the classes .disable-theme-hitbox and .enable-theme-hitbox
  document.querySelectorAll('.disable-theme-hitbox, .enable-theme-hitbox').forEach(hitbox => {
    hitbox.addEventListener('click', function () {
      // Get the parent .theme-container
      const themeContainer = this.closest('.theme-container');
      var arrow = themeContainer.querySelector('.disable-theme');
      var upDownArrows = themeContainer.querySelector('.arrows-container');
      if (arrow === null) {
        arrow = themeContainer.querySelector('.enable-theme');
      }

      console.log(arrow);
      console.log("Clicked:", this.classList.contains('disable-theme-hitbox') ? "Disable Theme" : "Enable Theme");
      console.log("Parent .theme-container:", themeContainer);

      let themePath = themeContainer.getAttribute("filename");
      var themesArray = getThemesArray(themesArray);
      var newElement

      console.log(themesArray);

      for (var i = 0; i < themesArray.length; i++) {
        if (themesArray[i].replace('//', '') === themePath.replace('//', '')) {
          if (!themesArray[i].startsWith("//")) {
            newElement = "//" + themesArray[i]
            themesArray.splice(i, 1);
            themesArray.unshift(newElement);
            document.getElementById('disabled-themes').prepend(themeContainer);

            this.classList.remove("disable-theme-hitbox");
            this.classList.add("enable-theme-hitbox");

            arrow.classList.remove("disable-theme");
            arrow.classList.add("enable-theme");

            upDownArrows.classList.add("invisible");
          } else {
            newElement = themesArray[i].replace("//", "")
            themesArray.splice(i, 1);
            themesArray.unshift(newElement);
            document.getElementById('enabled-themes').prepend(themeContainer);
            
            this.classList.remove("enable-theme-hitbox");
            this.classList.add("disable-theme-hitbox");

            arrow.classList.remove("enable-theme");
            arrow.classList.add("disable-theme");

            upDownArrows.classList.remove("invisible");
          }
        }
      }

      console.log(themesArray);

      updateThemesInputValue(themesArray)
    });
  });


  // Adding event listeners to the arrows
  const upDownArrows = document.querySelectorAll('.arrow-up-hitbox, .arrow-down-hitbox');
  upDownArrows.forEach(arrow => {
    arrow.addEventListener('click', handleArrowClick);
  });

});

console.log("themes-setting.js loaded");