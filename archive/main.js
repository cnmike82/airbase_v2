// Initialize the map
const map = L.map('map').setView([48.8566, 2.3522], 5); // Set the initial view coordinates and zoom level
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map); // Add the base map

const pointsOfInterest = [
    { name: 'Paris', coordinates: [48.8566, 2.3522] },
    { name: 'Berlin', coordinates: [52.5200, 13.4050] },
    { name: 'Rome', coordinates: [41.9028, 12.4964] },
    // Add more points of interest as needed
];

// Create markers for points of interest
for (const poi of pointsOfInterest) {
    const marker = L.marker(poi.coordinates).addTo(map);
    marker.bindPopup(poi.name);
}

// Event listener for dropdown menu
const dropdown = document.getElementById('dropdown');
dropdown.addEventListener('change', function() {
  const selectedOption = dropdown.value;
  // Perform actions based on the selected option
  console.log('Selected option:', selectedOption);
});


