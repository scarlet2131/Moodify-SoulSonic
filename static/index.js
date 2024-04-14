function redirectUser() {
    const email = document.getElementById('emailInput').value;
    if (email) {
        fetch('/api/v1/music/checkemail', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email: email }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'new') {
                window.location.href = '/register';
            } else {
                window.location.href = '/login';
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}
