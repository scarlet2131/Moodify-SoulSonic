const questions = {{ questions | tojson }};
const userInfoQuestions = {{ user_info_questions | tojson }};
const formContainer = document.getElementById('questionForm');
let currentQuestionIndex = 0;
const responses = [];

function addNextQuestion() {
    formContainer.innerHTML = ''; // Clear current form content

    let questionText = '';
    // This inputName is for debugging or future use; responses are now keyed by question text
    let inputName = `response${currentQuestionIndex + 1}`;

    // Determine if we're asking a general question or gathering user info
    if (currentQuestionIndex < questions.length) {
        questionText = questions[currentQuestionIndex];
    } else {
        const userInfoIndex = currentQuestionIndex - questions.length;
        const userInfoKeys = Object.keys(userInfoQuestions);
        if (userInfoIndex < userInfoKeys.length) {
            const key = userInfoKeys[userInfoIndex];
            questionText = userInfoQuestions[key];
        }
    }

    if (questionText) {
        // Create the next question
        const questionDiv = document.createElement('div');
        questionDiv.classList.add('question');
        questionDiv.innerHTML = `
            <label>${questionText}</label>
            <input type="text" name="${inputName}" data-question-text="${questionText}" placeholder="Your response" required>
            <button type="button" class="next-question">Next</button>
        `;
        formContainer.appendChild(questionDiv);

        document.querySelector('.next-question').addEventListener('click', handleNextQuestion);
    } else {
        // All questions answered, maybe send responses to server or show a completion message
        sendResponsesToServer();
    }
}

function handleNextQuestion(event) {
    event.preventDefault();
    const inputField = formContainer.querySelector('input[type="text"]');
    const inputValue = inputField.value;
    const questionText = inputField.getAttribute("data-question-text"); // Get the question text

    // Store the response along with its corresponding question text
    responses.push({ question: questionText, response: inputValue });

    currentQuestionIndex++;
    addNextQuestion();
}

function sendResponsesToServer() {
    const payload = {
        responses: responses
    };

    fetch('/api/v1/music/analyze-emotions', {
        method: 'POST',
        credentials: 'include',  // Ensures cookies are sent with the request
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        displayResults(data); // Function to display results

        // Here, you can handle the response data
        // For example, display the analyzed emotion and recommendations to the user
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Initial call to start displaying questions
addNextQuestion();



// Define your existing functions here like addNextQuestion, handleNextQuestion, sendResponsesToServer, etc.
function displayResults(data) {
    const resultsContainer = document.getElementById('results');

    if (data.recommendations && data.recommendations.length > 0) {
        const headingHTML = '<h2 class="recommendations-heading">Enjoy Your Recommendations</h2>';

        const gridHTML = data.recommendations.map(track => `
            <div class="recommendation-card">
                <img src="${track.image_url || '/path/to/default/image.png'}" alt="${track.name}">
                <div class="track-info">
                    <strong>${track.name}</strong>
                    <span>by ${track.artist}</span>
                    <a href="${track.spotify_url}" target="_blank">Listen on Spotify</a>
                </div>
            </div>
        `).join('');
<!--            resultsContainer.innerHTML = gridHTML;-->

        // Set the innerHTML of the resultsContainer to the heading followed by the grid
        resultsContainer.innerHTML = headingHTML + gridHTML;

        // Make the results container visible
        resultsContainer.style.visibility = 'visible';
        resultsContainer.style.opacity = 1;
    } else {
        resultsContainer.innerHTML = '<p style="text-align:center>No recommendations available. Try expressing your emotions differently!</p>';
         resultsContainer.style.visibility = 'hidden';
        resultsContainer.style.opacity = 0;
    }
}
function logout() {
    fetch('/api/v1/music/logout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        console.log('Logout successful', data);
        sessionStorage.removeItem('token'); // Clear the session storage
        window.location.href = '/login'; // Redirect to login page after logout
    })
    .catch(error => console.error('Error logging out:', error));
}

