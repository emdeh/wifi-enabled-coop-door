// Function to send a request to the server to toggle the door
function toggleDoor(action) {
    fetch('/door', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ action: action })
    })
    .then(response => response.json())
    .then(data => {
        // Update the door status on the web page
        document.getElementById('doorStatus').innerText = data.status;
    })
    .catch(error => console.error('Error:', error));
}

// Function to update the timer settings
function updateTimerSettings() {
    const openTime = document.getElementById('openTime').value;
    const closeTime = document.getElementById('closeTime').value;
    fetch('/settings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            door: {
                open_time: openTime,
                close_time: closeTime
            }
        })
    })
    .then(response => response.json())
    .then(data => {
        // Handle response
        console.log('Settings updated:', data);
    })
    .catch(error => console.error('Error:', error));
}

// Function to get the current settings on page load
function getCurrentSettings() {
    fetch('/settings', {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        // Set the values in the form fields
        document.getElementById('openTime').value = data.door.open_time;
        document.getElementById('closeTime').value = data.door.close_time;
        // Update other settings and status indicators
    })
    .catch(error => console.error('Error:', error));
}

// Call the getCurrentSettings function when the page loads
document.addEventListener('DOMContentLoaded', getCurrentSettings);
