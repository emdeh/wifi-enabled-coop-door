// Function to send a request to the server to toggle the door
function toggleDoor(action) {
    if (!isOverrideEnabled()) {
        alert('Please confirm schedule override to manually open/close the door.');
        return;
    }

    fetch('/door', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: action })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('doorStatus').innerText = data.status;
    })
    .catch(error => console.error('Error:', error));
}

// Function to check if override is enabled
function isOverrideEnabled() {
    return document.getElementById('overrideSchedule').checked;
}

// Function to update the timer settings
function updateTimerSettings() {
    const openTime = document.getElementById('openTime').value;
    const closeTime = document.getElementById('closeTime').value;

    fetch('/settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ door: { open_time: openTime, close_time: closeTime } })
    })
    .then(response => response.json())
    .then(data => console.log('Settings updated:', data))
    .catch(error => console.error('Error:', error));
}

// Function to handle manual override switch
function toggleOverride() {
    const isChecked = isOverrideEnabled();
    toggleDoorButtons(isChecked);

    fetch('/override', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ override: isChecked })
    })
    .catch(error => console.error('Error:', error));
}

// Function to toggle the door buttons
function toggleDoorButtons(enable) {
    document.getElementById('openButton').disabled = !enable;
    document.getElementById('closeButton').disabled = !enable;
}

// Function to get the current settings on page load
function getCurrentSettings() {
    fetch('/settings', { method: 'GET' })
    .then(response => response.json())
    .then(data => {
        document.getElementById('openTime').value = data.door.open_time;
        document.getElementById('closeTime').value = data.door.close_time;
        const overrideSwitch = document.getElementById('overrideSchedule');
        overrideSwitch.checked = data.override;
        toggleOverride();
    })
    .catch(error => console.error('Error:', error));
}

// Event listener for DOM content loaded
document.addEventListener('DOMContentLoaded', getCurrentSettings);
