window.onload = function() {
    fetchHistory();
};

function fetchHistory() {
    fetch('/api/v1/music/history', {
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        displayHistory(data);
    })
    .catch(error => {
        console.error('Error fetching history:', error);
    });
}

function displayHistory(historyData) {
    const container = document.getElementById('historyContainer');
    if (historyData && historyData.length > 0) {
        let historyHTML = '';

        historyData.forEach(item => {
                    console.log('Timestamp from database:', item.timestamp);

            let tracksHTML = item.recommendations.map(track => `
                <div class="track-card">
                    <img src="${track.image_url || '/path/to/default/image.png'}" alt="${track.name}">
                    <strong>${track.name}</strong>
                    <span>by ${track.artist}</span>
                    <a href="${track.spotify_url}" target="_blank">Listen on Spotify</a>
                </div>
            `).join('');
             // Create a date object from the timestamp
            const date = new Date(item.timestamp);
            // Format the date as "12 April 2024"
            const formattedDate = `${date.getDate()} ${date.toLocaleString('default', { month: 'long' })} ${date.getFullYear()}`;


            historyHTML += `
                <div class="emotion-section">
                    <div class="emotion-title">Emotion: ${item.emotion}</div>
                    <div class="timestamp">Timestamp: ${formattedDate}</div>

                    <div class="tracks-grid">
                        ${tracksHTML}
                    </div>
                </div>
            `;
        });

        container.innerHTML = historyHTML;
    } else {
        container.innerHTML = '<p style="text-align:centre">No history available.</p>';
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
        window.location.href = '/login';
    })
    .catch(error => console.error('Error logging out:', error));
}

 function clearHistory() {
        // We don't need to pass the username as a parameter since it's extracted from the session token
        fetch('/api/v1/music/history', {
            method: 'DELETE',
            credentials: 'include', // This will ensure the session cookie is sent with the request
            headers: {
                'Content-Type': 'application/json',
                // Include other headers like authentication tokens if necessary
            }
        })
        .then(response => {
            if (!response.ok) {
                // If the response status code is not OK, throw an error to go to the catch block
                throw new Error('Error in response');
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'success') {
                alert('History cleared successfully.');
                window.location.reload(); // Reload the page to update the UI
            } else {
                alert('Error clearing history: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error clearing history. Please try again.');
        });
    }
