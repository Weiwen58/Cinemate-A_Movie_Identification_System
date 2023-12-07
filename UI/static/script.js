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

function validateInputs() {
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
        isValid = false;
      }
    }
  });

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
      }
    } else {
      alert('Please enter a valid 4-digit year.');
    }
  }
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
    return;
  }
};

function searchMovies() {
    validateInputs();
    validateFields();
    // Get all actor-input elements
    const actorInputs = document.querySelectorAll('.actor-input');

    // Extract actors and characters from each actor-input
    const dataToSend = Array.from(actorInputs).map(actorInput => {
      const actorSelect = actorInput.querySelector('input[name="actor[]"]');
      const characterSelect = actorInput.querySelector('input[name="character[]"]');

      return {
        actor: actorSelect.value.trim(),
        character: characterSelect.value.trim()
      };
    });

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
        // Handle the response from the server
        console.log('Response from server:', data);
      })
      .catch(error => {
        console.error('Error:', error);
      });
}



 
  // function addActor() {
  //       const container = document.querySelector('.search-container');
  //       const actorInputs = document.querySelectorAll('.actor-input');
  
  //       // Check if the last actor input is not empty before adding another box
  //       const num_actor_inputs = actorInputs.length;
  //       const lastActorInput = actorInputs[num_actor_inputs - 1];
  //       const lastActorSelect = lastActorInput.querySelector('input[name="actor[]"]');
  
  //       if (lastActorSelect.value.trim() === '') {
  //         alert("Please select an actor before adding another box");
  //         return;
  //       }
  
  //       // Limit the length to 5
  //       if (num_actor_inputs >= 5) {
  //         alert("You can't add more than 5 actors");
  //         return;
  //       }
  
  //       const actorInput = document.createElement('div');
  //       actorInput.classList.add('actor-input');
  
  //       actorInput.innerHTML = `
  //       <label for="actor${ num_actor_inputs + 1 }">Actor:</label>
  //       <input list="actors" name="actor[]" placeholder="Select an actor">
  //       <datalist id="actors_data">
  //       {% for actor in actors %}
  //       <option value="{{ actor }}">
  //       {% endfor %}
  // </datalist>
  
  // <label for="character${ num_actor_inputs + 1 }">Character:</label>
  // <input list="characters" name="character[]" placeholder="Select a character name">
  // <datalist id="characters">
  //     {% for character in characters %}
  //     <option value="{{ character }}">
  //     {% endfor %}
  // </datalist>
  
  //         <button class="remove-button" onclick="removeActor(this)">-</button>
  //     `;
  
  //       container.insertBefore(actorInput, document.querySelector('.add-button'));
  //     }
  
  
  //     function removeActor(button) {
  //       const container = document.querySelector('.search-container');
  //       const actorInputs = document.querySelectorAll('.actor-input');
  
  //       // Get the index of the removed actor input
  //       const removedIndex = Array.from(actorInputs).indexOf(button.parentNode);
  
  //       // Remove the actor and character data from the array
  //       enteredValues.splice(removedIndex, 1);
  
  //       // Check if there is only one input box
  //       if (actorInputs.length > 1) {
  //         const actorInput = button.parentNode;
  //         container.removeChild(actorInput);
  //       } else {
  //         alert("You must have at least one input box");
  //       }
  //     }

 // <button class="add-button" onclick="addActor()">Add Actor</button>
 // <button class="remove-button" onclick="removeActor(this)">-</button> 