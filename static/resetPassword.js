document.getElementById('usernameForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent the default form submission
    const username = document.getElementById('usernameInput').value;
    clearMessages();  // Clear any existing messages
    fetchSecurityQuestion(username);
});

function fetchSecurityQuestion(username) {
    fetch(`/api/v1/music/get-security-question?username=${username}`, {
        method: 'GET'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Username not found.');
        }
        return response.json();
    })
    .then(data => {
        displaySecurityQuestionForm(data.security_question, username);
    })
    .catch(error => {
        displayError(error.message);  // Display error message
    });
}

function displaySecurityQuestionForm(question, username) {
    const formHTML = `
        <h2 style="text-align: center; color: #333; margin-top: 20px;">Security Question</h2>
        <div style="background: white; max-width: 350px; margin: 40px auto; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);">
            <label style="margin-bottom: 10px;">What is ${question}?</label>
            <input type="text" id="securityAnswer" required style="width: calc(100% - 24px); padding: 12px; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 4px;">
            <button onclick="verifyAnswer('${username}'); event.stopPropagation();" style="width: 100%; padding: 12px; background-color: #feacd0; color: black; border: none; border-radius: 4px; cursor: pointer; font-size: 20px; font-weight: 900; margin-top: 10px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">Submit</button>
        </div>
    `;
    document.getElementById('formContainer').innerHTML = formHTML;
    clearMessages();
}

function verifyAnswer(username) {
    event.preventDefault();
    const answer = document.getElementById('securityAnswer').value;
    fetch('/api/v1/music/verify-security-answer', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ username: username, answer: answer })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Incorrect security answer.');
        }
        return response.json();
    })
    .then(() => {
        showResetPasswordForm(username);
    })
    .catch(error => {
        displayError(error.message);
    });
}
function showResetPasswordForm(username) {
    const formHTML = `
        <h2 style="text-align: center; color: #333; margin-top: 20px;">Reset Your Password</h2>
        <div style="background: white; max-width: 350px; margin: 40px auto; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);">
            <input type="password" id="newPassword" placeholder="New Password" required style="width: calc(100% - 24px); padding: 12px; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 4px;">
            <input type="password" id="confirmPassword" placeholder="Confirm Password" required style="width: calc(100% - 24px); padding: 12px; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 4px;">
            <button onclick="resetPassword('${username}'); event.stopPropagation();" style="width: 100%; padding: 12px; background-color: #feacd0; color: black; border: none; border-radius: 4px; cursor: pointer; font-size: 20px; font-weight: 900; margin-top: 10px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">Reset Password</button>
        </div>
    `;
    document.getElementById('formContainer').innerHTML = formHTML;
    clearMessages();
}

function resetPassword(username) {
    event.preventDefault();
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    if (newPassword !== confirmPassword) {
        displayError("Passwords do not match.");
        return;
    }
    fetch(`/api/v1/music/reset-password?username=${username}&new_password=${newPassword}`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
    })
    .then(response => {
        if (!response.ok) throw new Error('Failed to reset password.');
        alert('Password has been reset. Please login with your new password.');
        window.location.href = '/login';  // Redirect to the login page
    })
    .catch(error => {
        displayError(error.message);  // Display error message
    });
}

function displayError(message) {
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = message;
    messageDiv.classList.add('visible', 'error-message');
}

function clearMessages() {
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = '';
    messageDiv.classList.remove('visible', 'error-message');
}
