function checkAccess(event) {
    event.preventDefault();
    fetch('/api/v1/music/protected', {
        method: 'GET',  // Explicitly stating the method type here
        credentials: 'include'  // Ensures cookies are sent with the request
    })
    .then(response => {
        if (response.ok) {
            // If the user is logged in, redirect to explore music page
            window.location.href = '/home';
        } else {
            alert('Please log in to explore music.');
        }
    })
    .catch(error => {
        console.error('Error verifying access:', error);
    });
}


document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
     const messageDiv = document.getElementById('message');
     messageDiv.textContent = ''; // Clear previous messages
     messageDiv.classList.remove('visible', 'error-message');
    const formData = new FormData(event.target);
    fetch('/api/v1/music/loginUser', {
        method: 'POST',
        body: new URLSearchParams(formData),
    })
    .then(response => response.json())
    .then(data => {
        const messageDiv = document.getElementById('message');
        if (data.detail) {
            messageDiv.textContent = data.detail;
            messageDiv.classList.add('error-message');
        } else {
            messageDiv.textContent = data.message;
            messageDiv.classList.remove('error-message');
            // Perform any action on successful login, like redirecting
            window.location.href = '/home'; // Redirect to a new page
        }
        messageDiv.classList.add('visible'); // Only make visible if there's a message

    })
    .catch(error => {
        console.error('Error:', error);
    });
});


