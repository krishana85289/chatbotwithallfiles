document.addEventListener('DOMContentLoaded', function () {
  // Get references to the file input, form, and process button
  const fileInput = document.getElementById('file');
  const uploadForm = document.getElementById('uploadForm');
  const processButton = document.getElementById('processDocument');

  // Add an event listener to the file input
  fileInput.addEventListener('change', handleFileUpload);

  // Add an event listener to the process button
  processButton.addEventListener('click', processDocument);

  function handleFileUpload() {
    // Your existing file upload logic goes here
  }

  function processDocument() {
    // Your logic to process the document goes here
    // This could include making a request to your API endpoint
    // You can reuse the fetch code from the previous example
  }
});

document.getElementById('fileInput').addEventListener('change', handleFileSelect);

function handleFileSelect(event) {
  const fileName = event.target.files[0].name;
  document.getElementById('fileNameDisplay').innerText = `Selected file: ${fileName}`;
}

function uploadFiles() {
  const fileInput = document.getElementById('fileInput');
  const files = fileInput.files;

  if (files.length > 0) {
    const formData = new FormData();

    for (let i = 0; i < files.length; i++) {
      formData.append('files', files[i], files[i].name);
    }

    fetch('http://192.168.1.4:5000//upload-files', {
      method: 'POST',
      body: formData
    })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Upload successful:', data);
        document.getElementById('responseDisplay').innerText = JSON.stringify(data.Message, null, 2);
        alert('Files uploaded successfully!');
      })
      .catch(error => {
        console.error('Error uploading files:', error.message);
        alert('Error uploading files. Please try again.');
      });
  } else {
    alert('Please select one or more files before uploading.');
  }
}


function sendQuestion() {
  const questionInput = document.getElementById('input');
  const question = questionInput.value;

  if (question.trim() === '') {
    alert('Please enter a question before sending.');
    return;
  }

  // Display user's question
  displayOutput(question, 'user');

  const payload = {
    query: question
  };

  fetch('http://192.168.1.4:5000/qa', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })
    .then(response => {
      console.log('response', response)
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}, ${response.statusText}`);
      }
      return response.json();
    })
    .then(data => {
      console.log(data);
      // Display API response
      displayOutput(data.answer, 'api');
    })
    .catch(error => {
      console.error('Error:', error.message);
      alert(`Error: ${error.message}`);
    });

  // Clear input after sending
  questionInput.value = '';
}

function displayOutput(message, sender) {
  console.log('pop:', message,sender)
  const outputDiv = document.getElementById('output');
  const messageDiv = document.createElement('div');
  messageDiv.className = sender === 'user' ? 'user-message' : 'api-message';
  messageDiv.innerHTML = `<p>${message}</p>`;
  outputDiv.appendChild(messageDiv);
}
console.log('Response:', response);

