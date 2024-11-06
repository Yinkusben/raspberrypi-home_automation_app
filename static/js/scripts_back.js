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
  
    // Toggle Device State
    function toggleDevice(deviceId) {
      fetch(`/toggle_device/${deviceId}`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') {
            document.getElementById(`device-${deviceId}-state`).innerText = data.new_state;
          } else {
            alert(data.message);
          }
        });
    }
  
    // Adjust Device Brightness
    function adjustBrightness(deviceId) {
      const brightness = document.getElementById(`brightness-${deviceId}`).value;
      fetch(`/adjust_brightness/${deviceId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `brightness=${brightness}`
      })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          alert(`Brightness set to ${data.brightness}`);
        } else {
          alert(data.message);
        }
      });
    }
  
    // Fetch Sensor Data (Temperature, Humidity, etc.)
    function fetchSensorData(deviceId) {
      fetch(`/fetch_sensor_data/${deviceId}`)
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') {
            document.getElementById(`sensor-${deviceId}-reading`).innerText = `${data.reading} ${data.unit}`;
          } else {
            alert(data.message);
          }
        });
    }