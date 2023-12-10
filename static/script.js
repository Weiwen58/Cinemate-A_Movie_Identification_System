// The input fields' sizes are adjusted 
// according to their respective placeholders' length
window.onload = function() {
  const inputs = document.querySelectorAll('input');
  
  inputs.forEach(input => {
    const placeholderText = input.getAttribute('placeholder');
    const placeholderLength = placeholderText.length;
    const minWidth = 50; // Set a minimum width
    const width = Math.max(placeholderLength * 10, minWidth); // Adjust the multiplication factor as needed
    input.style.width = width + 'px';
  });
};

$(document).ready(function() {
  $('input[name^="actor"]').change(function() {
      var actorName = $(this).val();
      var characterField = $(this).attr('name').replace('actor', 'characters');

      $.ajax({
          type: "GET",
          url: "/get_characters", // Replace with the actual endpoint to retrieve characters by actor ID
          data: {
              actor_name: actorName
          },
          success: function(response) {
              var characters = response.characters;
              var characterDatalist = $('#' + characterField); // Use ID selector instead of name selector

              // Clear existing options before appending new ones
              characterDatalist.empty();

              characters.forEach(function(character) {
                  characterDatalist.append($('<option>', {
                      value: character
                  }));
              });
          }
      });
  });
});

function validateInputs() {
  let dataToSend = {};
  let errorFlag = false;
  let errorMsg = "";
  
  const inputs = document.querySelectorAll('input[list]');
  inputs.forEach(input => {
    const datalistId = input.getAttribute('list');
    const datalist = document.getElementById(datalistId);
    const enteredValue = input.value;

    // Only perform validation if the input field is not empty
    if (enteredValue.trim() !== '') {
      const options = Array.from(datalist.options).map(option => option.value);
      if (!options.includes(enteredValue)) {
        alert(`Please select a valid option for '${input.name}' from the list.`);
        errorFlag = true;
        errorMsg = input.name;
      } else {
        // Store validated value in dataToSend object
        dataToSend[input.name] = enteredValue;
      }
    } else {
        // Store validated value in dataToSend object
        dataToSend[input.name] = enteredValue;
    }
  });

  if(errorFlag){
    return {flag2: false, msg: errorMsg, dataToSend};
  }

  const currentDate = new Date();
  const currentYear = currentDate.getFullYear();
  const yearInput = document.getElementById('year');
  const enteredValue = yearInput.value;
  const yearRegex = /^[0-9]{4}$/; // Regex to match a 4-digit number
  

    // Only perform validation if the input field is not empty
  if (enteredValue.trim() !== '') {
    if (yearRegex.test(enteredValue)) {
      const year = parseInt(enteredValue, 10);
      if (year < 1874 || year > currentYear) {
        alert('Cinemate supports movies released between 1874 and 2017 (both inclusive) \nPlease enter a date between the above mentioned dates :)');
        return {flag: false, msg:"year", dataToSend};
      } else {
        dataToSend['year'] = enteredValue;
      }
    } else {
      alert('Please enter a valid 4-digit year.');
      return {flag2: false, dataToSend};
    }
  } else {
      dataToSend['year'] = '';
  }
  
  // Validate the single textarea element
  const textarea = document.querySelector('textarea');
  const textareaValue = textarea.value.trim();
  const textareaName = textarea.getAttribute('name');
  
  // Store validated textarea value in dataToSend
  dataToSend[textareaName] = textareaValue;

  return {flag2: true, msg: "tmam", dataToSend};
};

function validateFields() {
  const inputs = document.querySelectorAll('input[list], input[type="text"], textarea');
  let isValid = false;

  inputs.forEach(input => {
    if ((input.tagName === 'INPUT' && input.value.trim() !== '') || (input.tagName === 'TEXTAREA' && input.value.trim() !== '')) {
      isValid = true;
    }
  });

  if (!isValid) {
    alert('Please fill in at least one input field.');
    return false;
  }
  return true;
};

function displayMovies(data) {
  const moviesList = document.querySelector('.movie-list');
  moviesList.innerHTML = '';

  data.forEach(movie => {
    const listItem = document.createElement('li');
    listItem.textContent = `${movie.title}`;
    listItem.classList.add('movie-item');
    moviesList.appendChild(listItem);
  });
}
function searchMovies() {
    let flag1 = validateFields();

    if (!flag1){
      return;
    }

    const {flag2, msg, dataToSend} = validateInputs();

    if (!flag2){
      return;
    }

    // Send the data to the backend using Fetch API
    fetch('/your_backend_endpoint', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(dataToSend)
    })
    .then(response => response.json())
    .then(data => {
      console.log('Response from server:', data);
      displayMovies(data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
}