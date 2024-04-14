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

document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission
    const formData = new FormData(event.target);
    fetch('/api/v1/music/register', {
        method: 'POST',
        body: new URLSearchParams(formData), // Encode as form data
    })
    .then(response => response.json())
    .then(data => {
        const messageDiv = document.getElementById('message');
        if (data.detail) {
            // Handle errors, like username/email already exists
            messageDiv.textContent = data.detail;
        } else {
            // Handle success, maybe clear the form or redirect
            messageDiv.textContent = data.message;
            // Optional: Redirect to login page or clear form
            location.href = '/home'; // Redirect to login page
        }
        messageDiv.classList.add('visible'); // Only make visible if there's a message

    })
    .catch(error => console.error('Error:', error));
});