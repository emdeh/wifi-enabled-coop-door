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
        document.getElementById('doorStatus').innerText = data.status.replace('Door ', '');
        // Update the override status message based on the door state
        updateOverrideMessage();
    })
    .catch(error => console.error('Error:', error));
}

// Function to update the override status message
function updateOverrideMessage() {
    const overrideSwitch = document.getElementById('overrideSchedule');
    const doorStatus = document.getElementById('doorStatus').innerText;
    const actionWord = doorStatus === 'OPENED' ? 'close' : 'open';
    document.getElementById('overrideStatus').innerText = overrideSwitch.checked ? 
        `Auto schedule overridden. Door will not ${actionWord}` : 
        'Override schedule';
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

// Function to handle manual override switch
function toggleOverride() {
    const isChecked = document.getElementById('overrideSchedule').checked;
    fetch('/override', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ override: isChecked })
    })
    .then(response => response.json())
    .then(data => {
        // Update the override status message
        updateOverrideMessage();
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

// Event listeners for page load and toggle override
document.addEventListener('DOMContentLoaded', () => {
    getCurrentSettings();
    document.getElementById('overrideSchedule').addEventListener('change', toggleOverride);
});
