// Store the current scroll position in localStorage before the page reloads
window.addEventListener("beforeunload", function() {
  localStorage.setItem("scrollPosition", window.scrollY);
});

// Restore the scroll position after the page reloads
window.addEventListener("load", function() {
  const scrollPosition = localStorage.getItem("scrollPosition");
  if (scrollPosition) {
    window.scrollTo(0, parseInt(scrollPosition));
    localStorage.removeItem("scrollPosition"); // Remove after using it
  }
});

 // Initialize the Socket.IO connection
const socket = io();  // This connects to the Socket.IO server

// Function to toggle device state based on checkbox
function toggleDevice(deviceId) {
    const checkbox = document.getElementById(`device-${deviceId}`);
    const state = checkbox.checked ? 1 : 0;

    socket.emit('toggle_device', { device_id: deviceId, state: state });
}

// Function to adjust device brightness
function adjustBrightness(deviceId) {
  const brightness = document.getElementById(`brightness-${deviceId}`).value;
  socket.emit('adjust_brightness', { device_id: deviceId, brightness: brightness });
}

// Listen for state updates from the server
socket.on('device_state_updated', (data) => {
    const deviceId = data.device_id;
    const newState = data.new_state;

    // Update the checkbox based on the new state
    const checkbox = document.getElementById(`device-${deviceId}`);
    if (checkbox) {
        checkbox.checked = (newState >= 1);  // Set checkbox state
    }

    console.log(`Device ${deviceId} turned ${newState}`);
});

// Listen for brightness updates from the server
socket.on('brightness_updated', (data) => {
  const deviceId = data.device_id;
  const brightness = data.brightness;

  // Update the slider value for brightness on the UI
  const slider = document.getElementById(`brightness-${deviceId}`);
  if (slider) {
      slider.value = brightness;  // Set the slider's value to the updated brightness
  }

  console.log(`Device ${deviceId} brightness set to ${brightness}`);
});
